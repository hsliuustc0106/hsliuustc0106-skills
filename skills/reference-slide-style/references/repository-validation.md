# Repository integration validation

The source-only build was run after removing all PPTX/POTX seed files and using
an unrelated working directory. Python 3.13 with python-pptx 1.0.2 was used.

- Six regression tests passed (`tests/test_templates.py`).
- The six generated PPTX/POTX files passed `scripts/check_templates.py`.
- Each output contains 14 slides, 14 custom layouts, 233 slide placeholders,
  133 fixed layout shapes, and one editable five-column table.
- Every ZIP entry in each regenerated Office file was byte-identical to the
  corresponding entry in the original v2 downloadable kit. ZIP container
  timestamps/compression metadata were not required to match.
- Original research slides, branding, cover imagery, and font binaries are not
  included in this repository source distribution.

This comparison establishes that the source-only bootstrap reproduces the v2
Office parts; it is not a new visual-rendering test. The historical visual checks
are recorded separately in `validation.md`. Microsoft PowerPoint was not tested.
GitHub Actions results, once available, are separate from these local checks.
