#!/usr/bin/env python3
"""ole_package.py — 把任意文件封装成 OLE "Package"（Object Packager）复合文档字节流，
供 PowerPoint 作为 OLE 对象嵌入，双击即可释放到临时文件并用默认程序打开。

产物 = CFBF 复合文件，内含单个流 "\\x01Ole10Native"，其内容为 Object Packager 结构：
  UInt32 native_data_size   # 后续全部字节数
  UInt16 flags = 0x0002
  CStr   label              # 显示名（带扩展名，决定双击用什么程序打开）
  CStr   src_path           # 原始路径
  UInt32 reserved
  CStr   temp_path          # 临时路径
  UInt32 data_size (N)
  bytes  data (N)
读取逻辑与 oletools.oleobj / Office 一致。
"""
import struct

FREESECT   = 0xFFFFFFFF
ENDOFCHAIN = 0xFFFFFFFE
FATSECT    = 0xFFFFFFFD
DIFSECT    = 0xFFFFFFFC
NOSTREAM   = 0xFFFFFFFF
SECTOR     = 512


def _ole10native(data: bytes, label: str) -> bytes:
    """构造 \\x01Ole10Native 流内容（Object Packager 格式）。"""
    def ansi(s):
        try:
            return s.encode("latin-1")
        except UnicodeEncodeError:
            return s.encode("gbk", "replace")  # 中文 Windows 的 ANSI 代码页
    src = "C:\\" + label
    tmp = "C:\\Users\\Public\\" + label
    body  = struct.pack("<H", 0x0002)
    body += ansi(label) + b"\x00"
    body += ansi(src) + b"\x00"
    body += struct.pack("<I", 0x00000000)          # reserved
    body += ansi(tmp) + b"\x00"
    body += struct.pack("<I", len(data)) + data
    return struct.pack("<I", len(body)) + body


# Package 对象（Object Packager）的 CLSID = {0003000C-0000-0000-C000-000000000046}
# Windows PowerPoint 靠 Root Entry 的这个 CLSID 找到 OLE 处理器；为空会报错打不开。
# CFBF CLSID 字节序：data1(LE u32) data2(LE u16) data3(LE u16) data4(8B)
PACKAGE_CLSID = bytes([0x0C, 0x00, 0x03, 0x00, 0x00, 0x00, 0x00, 0x00,
                       0xC0, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x46])


def _dir_entry(name: str, obj_type: int, start_sector: int, size: int,
               child=NOSTREAM, left=NOSTREAM, right=NOSTREAM,
               clsid: bytes = b"\x00" * 16) -> bytes:
    name_utf16 = name.encode("utf-16-le") + b"\x00\x00"
    if len(name_utf16) > 64:
        raise ValueError("directory name too long")
    name_field = name_utf16 + b"\x00" * (64 - len(name_utf16))
    e  = name_field
    e += struct.pack("<H", len(name_utf16))         # name length incl null
    e += struct.pack("<B", obj_type)                # 5=root,1=storage,2=stream,0=empty
    e += struct.pack("<B", 1)                        # color = black
    e += struct.pack("<I", left)
    e += struct.pack("<I", right)
    e += struct.pack("<I", child)
    e += clsid[:16].ljust(16, b"\x00")              # CLSID
    e += struct.pack("<I", 0)                        # state bits
    e += b"\x00" * 8                                 # creation time
    e += b"\x00" * 8                                 # modified time
    e += struct.pack("<I", start_sector)            # starting sector
    e += struct.pack("<Q", size)                     # stream size
    assert len(e) == 128
    return e


def build_ole_package(data: bytes, label: str) -> bytes:
    """把 data（文件字节）封装为完整 CFBF OLE Package，返回 .bin 字节。"""
    stream = _ole10native(data, label)
    data_sectors = (len(stream) + SECTOR - 1) // SECTOR

    # 布局：先估算 DIFAT/FAT 数量（存在相互依赖，迭代到稳定）
    D = 0
    while True:
        # 1(dir) + D(difat) + F(fat) + data_sectors
        # F 需覆盖全部扇区
        F = 1
        while True:
            total = 1 + D + F + data_sectors
            need_F = (total + 127) // 128
            if need_F <= F:
                break
            F = need_F
        need_D = 0 if F <= 109 else (F - 109 + 126) // 127
        if need_D == D:
            break
        D = need_D

    dir_sector    = 0
    difat_sectors = list(range(1, 1 + D))
    fat_sectors   = list(range(1 + D, 1 + D + F))
    first_data    = 1 + D + F
    data_sec_ids  = list(range(first_data, first_data + data_sectors))
    total_sectors = 1 + D + F + data_sectors

    # ---- FAT 内容 ----
    fat = [FREESECT] * (F * 128)
    fat[dir_sector] = ENDOFCHAIN
    for s in difat_sectors:
        fat[s] = DIFSECT
    for s in fat_sectors:
        fat[s] = FATSECT
    for i, s in enumerate(data_sec_ids):
        fat[s] = data_sec_ids[i + 1] if i + 1 < len(data_sec_ids) else ENDOFCHAIN

    # ---- DIFAT（FAT 扇区定位表）----
    header_difat = fat_sectors[:109] + [FREESECT] * (109 - min(109, len(fat_sectors)))
    header_difat = header_difat[:109]
    rest = fat_sectors[109:]
    difat_sector_data = []
    for i in range(D):
        chunk = rest[i * 127:(i + 1) * 127]
        chunk = chunk + [FREESECT] * (127 - len(chunk))
        nxt = difat_sectors[i + 1] if i + 1 < D else ENDOFCHAIN
        difat_sector_data.append(chunk + [nxt])

    # ---- 目录 ----
    root   = _dir_entry("Root Entry", 5, ENDOFCHAIN, 0, child=1, clsid=PACKAGE_CLSID)
    stream_entry = _dir_entry("\x01Ole10Native", 2, data_sec_ids[0], len(stream))
    empty  = _dir_entry("", 0, 0, 0)
    dir_bytes = root + stream_entry + empty + empty
    dir_bytes += b"\x00" * (SECTOR - len(dir_bytes))

    # ---- Header ----
    h  = bytes.fromhex("d0cf11e0a1b11ae1")
    h += b"\x00" * 16                                 # CLSID
    h += struct.pack("<H", 0x003E)                    # minor version
    h += struct.pack("<H", 0x0003)                    # major version (v3, 512B)
    h += struct.pack("<H", 0xFFFE)                    # byte order
    h += struct.pack("<H", 0x0009)                    # sector shift = 512
    h += struct.pack("<H", 0x0006)                    # mini sector shift = 64
    h += b"\x00" * 6                                  # reserved
    h += struct.pack("<I", 0)                         # num dir sectors (v3=0)
    h += struct.pack("<I", F)                         # num FAT sectors
    h += struct.pack("<I", dir_sector)               # first dir sector
    h += struct.pack("<I", 0)                         # transaction sig
    h += struct.pack("<I", 0x00001000)               # mini stream cutoff
    h += struct.pack("<I", ENDOFCHAIN)               # first miniFAT sector
    h += struct.pack("<I", 0)                         # num miniFAT sectors
    h += struct.pack("<I", difat_sectors[0] if D else ENDOFCHAIN)  # first DIFAT
    h += struct.pack("<I", D)                         # num DIFAT sectors
    h += b"".join(struct.pack("<I", v) for v in header_difat)
    assert len(h) == SECTOR

    # ---- 组装文件（按扇区顺序）----
    out = bytearray()
    out += h
    out += dir_bytes                                  # sector 0
    for chunk in difat_sector_data:                   # difat sectors
        out += b"".join(struct.pack("<I", v) for v in chunk)
    fat_bytes = b"".join(struct.pack("<I", v) for v in fat)
    out += fat_bytes                                  # fat sectors
    padded = stream + b"\x00" * (data_sectors * SECTOR - len(stream))
    out += padded                                     # data sectors
    assert len(out) == (1 + total_sectors) * SECTOR, (len(out), (1 + total_sectors) * SECTOR)
    return bytes(out)


if __name__ == "__main__":
    # 自测：构造后用 olefile 回读校验
    import olefile, io
    payload = ("<!DOCTYPE html><html><body>hello 世界</body></html>" * 5000).encode("utf-8")
    blob = build_ole_package(payload, "训练Infra课程.html")
    of = olefile.OleFileIO(io.BytesIO(blob))
    assert of.exists("\x01Ole10Native"), "stream missing"
    raw = of.openstream("\x01Ole10Native").read()
    size = struct.unpack("<I", raw[:4])[0]
    assert size == len(raw) - 4, (size, len(raw) - 4)
    # 解析取回数据
    off = 6
    def rd(o):
        e = raw.index(b"\x00", o); return raw[o:e], e + 1
    label, off = rd(off); src, off = rd(off); off += 4
    tmp, off = rd(off)
    n = struct.unpack("<I", raw[off:off+4])[0]; off += 4
    got = raw[off:off+n]
    assert got == payload, "roundtrip data mismatch"
    print("OK: container valid, label=%r, data=%d bytes recovered intact" % (label.decode("gbk"), n))
