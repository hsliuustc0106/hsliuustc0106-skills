#!/usr/bin/env python3
"""Build labeled contact sheets from rendered slide images."""

from __future__ import annotations

import argparse
import os
import re
from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageDraw

BACKGROUND = "#E9EDF3"
INK = "#172033"
TILE_BACKGROUND = "#FFFFFF"
EXPECTED_ASPECT_RATIO = 16 / 9
ASPECT_RATIO_TOLERANCE = 0.01
MIN_RENDER_WIDTH = 960
MIN_RENDER_HEIGHT = 540
OUTPUT_NAME_PATTERN = re.compile(r"contact-sheet-\d+\.png\Z")


@dataclass(frozen=True)
class CliArgs:
    """Command-line arguments."""

    input_dir: Path
    output_dir: Path
    pattern: str
    columns: int
    rows: int
    thumb_width: int
    force: bool


def natural_key(path: Path) -> list[int | str]:
    """Return a human-friendly sort key for numbered slide filenames."""

    return [
        int(part) if part.isdigit() else part.casefold()
        for part in re.split(r"(\d+)", path.name)
    ]


def render_tile(path: Path, thumb_width: int) -> Image.Image:
    """Render one labeled 16:9 thumbnail tile."""

    thumb_height = round(thumb_width * 9 / 16)
    label_height = 28
    padding = 12
    tile = Image.new(
        "RGB",
        (thumb_width + 2 * padding, thumb_height + label_height + 2 * padding),
        TILE_BACKGROUND,
    )
    with Image.open(path) as source:
        image = source.convert("RGB")
        image.thumbnail((thumb_width, thumb_height))
        x = padding + (thumb_width - image.width) // 2
        y = padding + label_height + (thumb_height - image.height) // 2
        tile.paste(image, (x, y))
    ImageDraw.Draw(tile).text((padding, 8), path.stem, fill=INK)
    return tile


def validate_slide_images(slide_paths: list[Path]) -> None:
    """Require valid 16:9 renders before composing a contact sheet."""

    expected_size: tuple[int, int] | None = None
    for path in slide_paths:
        with Image.open(path) as image:
            width, height = image.size
        if width < 1 or height < 1:
            raise ValueError(f"rendered slide has invalid dimensions: {path}")
        if width < MIN_RENDER_WIDTH or height < MIN_RENDER_HEIGHT:
            raise ValueError(
                f"rendered slide is too small for layout QA: {path} "
                f"({width}x{height}; minimum {MIN_RENDER_WIDTH}x{MIN_RENDER_HEIGHT})"
            )
        ratio = width / height
        relative_error = abs(ratio / EXPECTED_ASPECT_RATIO - 1)
        if relative_error > ASPECT_RATIO_TOLERANCE:
            raise ValueError(f"rendered slide is not 16:9: {path} ({width}x{height})")
        if expected_size is None:
            expected_size = (width, height)
        elif (width, height) != expected_size:
            raise ValueError(
                f"rendered slides have inconsistent dimensions: expected "
                f"{expected_size[0]}x{expected_size[1]}, got {width}x{height} for {path}"
            )


def build_contact_sheets(
    slide_paths: list[Path],
    output_dir: Path,
    *,
    columns: int,
    rows: int,
    thumb_width: int,
    force: bool,
) -> list[Path]:
    """Build one or more contact sheets and return their paths."""

    if columns < 1 or rows < 1:
        raise ValueError("columns and rows must be positive")
    if thumb_width < 160:
        raise ValueError("thumb-width must be at least 160 pixels")
    if not slide_paths:
        raise ValueError("no rendered slide images matched the requested pattern")
    validate_slide_images(slide_paths)

    output_dir.mkdir(parents=True, exist_ok=True)
    capacity = columns * rows
    sheet_count = (len(slide_paths) + capacity - 1) // capacity
    outputs = [
        output_dir / f"contact-sheet-{index:02d}.png"
        for index in range(1, sheet_count + 1)
    ]
    existing = [path for path in outputs if path.exists()]
    if existing and not force:
        raise FileExistsError(
            f"Refusing to overwrite {existing[0]}; pass --force to replace it"
        )

    generated: list[tuple[Path, Image.Image]] = []
    temporary_paths: list[Path] = []
    try:
        for output_path, start in zip(outputs, range(0, len(slide_paths), capacity)):
            paths = slide_paths[start : start + capacity]
            tiles = [render_tile(path, thumb_width) for path in paths]
            tile_width, tile_height = tiles[0].size
            sheet = Image.new(
                "RGB",
                (columns * tile_width, rows * tile_height),
                BACKGROUND,
            )
            for index, tile in enumerate(tiles):
                sheet.paste(
                    tile,
                    (
                        (index % columns) * tile_width,
                        (index // columns) * tile_height,
                    ),
                )
                tile.close()
            generated.append((output_path, sheet))

        for output_path, sheet in generated:
            temporary_path = output_path.with_name(
                f".{output_path.name}.tmp-{os.getpid()}"
            )
            sheet.save(temporary_path, format="PNG")
            temporary_paths.append(temporary_path)
        for temporary_path, output_path in zip(temporary_paths, outputs):
            temporary_path.replace(output_path)

        if force:
            for stale_path in output_dir.glob("contact-sheet-*.png"):
                if (
                    OUTPUT_NAME_PATTERN.fullmatch(stale_path.name)
                    and stale_path not in outputs
                ):
                    stale_path.unlink()
    finally:
        for _, sheet in generated:
            sheet.close()
        for temporary_path in temporary_paths:
            if temporary_path.exists():
                temporary_path.unlink()

    return outputs


def parse_args() -> CliArgs:
    """Parse command-line arguments."""

    parser = argparse.ArgumentParser(
        description="Build labeled contact sheets from rendered slide PNGs."
    )
    parser.add_argument("--input-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--pattern", default="*.png")
    parser.add_argument("--columns", type=int, default=3)
    parser.add_argument("--rows", type=int, default=4)
    parser.add_argument("--thumb-width", type=int, default=480)
    parser.add_argument("--force", action="store_true")
    namespace = parser.parse_args()
    return CliArgs(
        input_dir=namespace.input_dir,
        output_dir=namespace.output_dir,
        pattern=str(namespace.pattern),
        columns=int(namespace.columns),
        rows=int(namespace.rows),
        thumb_width=int(namespace.thumb_width),
        force=bool(namespace.force),
    )


def main() -> int:
    """Run the contact-sheet builder."""

    args = parse_args()
    input_dir = args.input_dir.expanduser().resolve()
    if not input_dir.is_dir():
        raise NotADirectoryError(f"Input directory does not exist: {input_dir}")
    slide_paths = sorted(
        (
            path
            for path in input_dir.glob(args.pattern)
            if not path.name.startswith("contact-sheet-")
        ),
        key=natural_key,
    )
    outputs = build_contact_sheets(
        slide_paths,
        args.output_dir.expanduser().resolve(),
        columns=args.columns,
        rows=args.rows,
        thumb_width=args.thumb_width,
        force=args.force,
    )
    for output in outputs:
        print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
