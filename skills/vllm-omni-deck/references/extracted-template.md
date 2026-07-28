# Source-Derived Template

## Sources

- Content and visual source: [vLLM-Omni Slides (Public) 2026-04 latest.pptx](https://docs.google.com/presentation/d/111-L8zF7A1j_YI_cR8JsblofdScdRr2f/edit?rtpof=true)
- Structural reference: [Huawei internal PPT template](https://docs.google.com/presentation/d/1IARhAvaKk1v3dNTO3q66cWxONh0tNsYs/edit?slide=id.p1#slide=id.p1)

The structural reference is access-controlled. The extracted asset follows its
five-slide form without copying Huawei branding or embedded media.

## Slide Mapping

| Output slide | Role | Public source exemplar |
| --- | --- | --- |
| 1 | Cover | Slide 1 |
| 2 | Contents | Slide 34 |
| 3 | Standard body | Slide 9 |
| 4 | Chart color guidance | Slide 42 |
| 5 | Closing | Slide 45 |

The extraction keeps the source deck's `simple-light-2` master, 10 x 5.625 inch
canvas, footer wordmarks, and theme palette. It replaces topic-specific content
with editable placeholders, embeds a self-contained native chart, adds an
editable palette table, and removes QR codes, external links, and source
benchmarks.

## Regeneration

Download the public source as a PowerPoint file, then run:

```bash
.venv/bin/python scripts/extract_source_template.py \
  --source /path/to/vllm-omni-public.pptx \
  --output assets/vllm-omni-extracted-template.pptx \
  --force
```

The script intentionally checks source slide titles before extraction. Reinspect
and update the mapping when a newer public deck changes those signatures.
