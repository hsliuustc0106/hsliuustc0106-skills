"""Regression tests for the contact-sheet utility."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from PIL import Image

SKILL_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SKILL_ROOT / "scripts"))

from build_contact_sheets import build_contact_sheets


class ContactSheetTests(unittest.TestCase):
    """Exercise output-set replacement and render validation."""

    def make_slides(self, root: Path, count: int, size: tuple[int, int]) -> list[Path]:
        """Create numbered dummy slide renders."""

        paths = []
        for index in range(1, count + 1):
            path = root / f"slide-{index:02d}.png"
            Image.new("RGB", size, "white").save(path)
            paths.append(path)
        return paths

    def test_force_removes_obsolete_sheets(self) -> None:
        """A smaller forced rebuild must not leave a stale final sheet."""

        with TemporaryDirectory() as temporary:
            root = Path(temporary)
            input_dir = root / "slides"
            output_dir = root / "contacts"
            input_dir.mkdir()
            slides = self.make_slides(input_dir, 13, (960, 540))
            build_contact_sheets(
                slides,
                output_dir,
                columns=3,
                rows=4,
                thumb_width=160,
                force=False,
            )
            self.assertEqual(len(list(output_dir.glob("contact-sheet-*.png"))), 2)
            manual = output_dir / "contact-sheet-manual.png"
            Image.new("RGB", (960, 540), "white").save(manual)

            build_contact_sheets(
                slides[:12],
                output_dir,
                columns=3,
                rows=4,
                thumb_width=160,
                force=True,
            )
            self.assertEqual(
                [path.name for path in output_dir.glob("contact-sheet-[0-9][0-9].png")],
                ["contact-sheet-01.png"],
            )
            self.assertTrue(manual.exists())

    def test_rejects_non_widescreen_render(self) -> None:
        """Letterboxing must not hide an invalid source-render aspect ratio."""

        with TemporaryDirectory() as temporary:
            root = Path(temporary)
            slides = self.make_slides(root, 1, (960, 720))
            with self.assertRaisesRegex(ValueError, "is not 16:9"):
                build_contact_sheets(
                    slides,
                    root / "contacts",
                    columns=3,
                    rows=4,
                    thumb_width=160,
                    force=False,
                )

    def test_rejects_inconsistent_render_dimensions(self) -> None:
        """A contact sheet must not mask mixed-resolution slide renders."""

        with TemporaryDirectory() as temporary:
            root = Path(temporary)
            slides = self.make_slides(root, 2, (960, 540))
            Image.new("RGB", (1280, 720), "white").save(slides[1])
            with self.assertRaisesRegex(ValueError, "inconsistent dimensions"):
                build_contact_sheets(
                    slides,
                    root / "contacts",
                    columns=3,
                    rows=4,
                    thumb_width=160,
                    force=False,
                )

    def test_rejects_low_resolution_render(self) -> None:
        """Full-slide QA requires enough pixels to inspect dense content."""

        with TemporaryDirectory() as temporary:
            root = Path(temporary)
            slides = self.make_slides(root, 1, (320, 180))
            with self.assertRaisesRegex(ValueError, "too small for layout QA"):
                build_contact_sheets(
                    slides,
                    root / "contacts",
                    columns=3,
                    rows=4,
                    thumb_width=160,
                    force=False,
                )


if __name__ == "__main__":
    unittest.main()
