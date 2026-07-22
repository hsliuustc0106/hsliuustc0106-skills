# huawei-refs — 华为官方 PPT 提取素材库

从源仓库提供的 6 份华为官方 PPT/PDF 中逐页目检后精选提取的封面、logo、组件素材。
配套的排版与文案风格分析见 `references/huawei-style.md`；给 deck 换品牌图用 `scripts/apply_bg.py` 或 `eb.embed_image()`（见 `references/branding.md`）。

## 来源材料

| 简称 | 原件 | 特征 |
|---|---|---|
| template-light | PPT模板-浅色版16-9 (2).pptx | 华为官方标准空白模板（封面/目录/图表配色示范/Thank you） |
| ekit | HUAWEI eKit_KV_16-9 PPT.pptx | 单页全幅 KV 封面 |
| gaokong | 高空抛物治理解决方案主打PPT.pptx | 浅色方案汇报（分销） |
| dme | iMasterCloud DME IQ 主打胶片.pptx | **深色系**产品胶片（黑底+金强调） |
| ict-academy | 华为ICT学院课程业务主打胶片.pptx | 浅色业务主打胶片 |
| ict-talent | 2025 华为ICT人才生态主打胶片.pdf | 浅色 62 页大型胶片 |
| storage-en | Commercial Market Data Storage.pdf | 英文发布会风格（IDF 彩色星球 KV） |

## 目录

### covers/ — 封面 KV 与背景

| 文件 | 来源 | 用途 |
|---|---|---|
| 封面-雪山红伞KV.png | template-light 封面 | 华为最经典封面画（雪山云海+红色滑翔伞），透明 PNG |
| 封面-草原日出KV.jpg | ekit 封面 | 草原日出全幅 KV，适合叠白色大标题 |
| 封底-金色稻田收割机KV.png | dme 封底 | 金色稻田+红色收割机，封底/结尾页画 |
| 封面-灯塔星空.jpeg | gaokong | 灯塔星空夜景，深色封面可用 |
| 封面-彩色星球飘带KV.jpeg | storage-en 封面 | IDF 彩色星球飘带，发布会风格右侧半幅 |
| 封面-深蓝金光轨KV.jpeg | 研究报告封面 | 深蓝紫渐变 + 金色光轨光球，研究报告 / 技术分享深色封面（tech-share 模板封面在用） |
| 背景-帆船海洋-目录页.jpeg | gaokong 目录页 | 蓝色帆船竖构图，目录页左侧图 |
| 背景-雪山登山队.jpg | template-light | 雪山滑雪登山队，团队/征程隐喻 |
| 背景-浅蓝天空.jpeg / 背景-浅粉光晕.png / 背景-白色波纹.jpeg / 背景-深灰纹理.jpeg | ict-academy | 内容页/章节页底纹四件套（浅色×3 + 深色×1） |

### logos/ — 品牌标识

| 文件 | 说明 |
|---|---|
| huawei-横版logo-透明.png | 花瓣+HUAWEI 字标横版，透明底（页脚右下角用） |
| huawei-横版logo-白底.jpeg | 同上白底版 |
| huawei-花瓣-大.png / huawei-花瓣-红.png | 单独花瓣图形，透明底两种尺寸 |
| ICT学院-桂冠徽章-白底.png / -深底.png | HUAWEI ICT Academy 红色桂冠徽章 |
| tech/ | 华为技术品牌 logo：kunpeng / ascend / mindspore / cangjie / harmonyos / opengauss / cann / huaweicloud / kirin（cangjie、opengauss 为白底，其余透明） |

### components/ — 插画、装饰与图标

| 文件 | 说明 |
|---|---|
| 插画-红色线稿园区-白底.png | 华为红单色线稿园区建筑插画（4000px，透明底），章节页/封面装饰 |
| 插画-红色线稿园区-黑底.png | 同款线稿深底配色版 |
| 装饰-白色几何线框1/2.png | 白色六边形几何线框（透明底），深色页角落装饰 |
| 图形-莫比乌斯环3D白.jpg | 白色 3D ∞ 环，「双轮驱动/闭环」类观点页主图 |
| 图形-红色渐变圆环.png | 红色渐变圆环，数据大字外圈 |
| icons-gray/ | 华为官方灰色线框图标（2500px 透明底）：调节器/硬盘/饼图/扫描识别/AI芯片/趋势屏/时钟——deck 深浅两色系均可用 |

### 整页参考与官方模板

| 文件 | 说明 |
|---|---|
| 官方PPT模板-浅色16-9.pptx | 华为官方空白模板原件（需交付 PPTX 且要官方母版时用） |
| pages/官方模板-封面页.jpg | 封面版式参考（部门/作者/日期占位 + 红色角线 + Security Level） |
| pages/官方模板-目录页.jpg | 目录页版式（浅灰底 + 黑「目录」+ 红短下划线） |
| pages/官方模板-图表配色示范页.jpg | **官方图表配色规范**：灰阶做底、华为红做强调、琥珀色点缀 |
| pages/官方模板-ThankYou页.jpg | 结尾页版式（左黑色大字 + 右使命宣言/版权/免责声明） |

## 使用注意

- 本目录是**素材库**，不会被自动打包进 deck；选用后经 `eb.embed_image()` 内联进 bundle 才生效。
- 部分 logo（tech/ 下 cangjie、opengauss）为白底 JPEG 转存 PNG，深色页使用前需抠底。
- 本库的提取工具链：pptx 经 `soffice --headless --convert-to pdf` 转 PDF → PyMuPDF 渲染逐页图目检；内嵌媒体用 Python `zipfile` 解包 `ppt/media/`；PDF 内嵌图用 PyMuPDF `extract_image`。PDF 进阶处理按需使用单独安装的 PDF skill。
- 原始参考包中另有 36 个 `.wdp`（JPEG-XR）背景图未提取（macOS 无原生解码器）。
