# TIMELY-Agent Homepage Card Image Design

## Decision

Use the supplied `timely-agent.png` as the visual reference for a public-safe TIMELY-Agent homepage project-card image. The source is visually stronger than the simplified workflow SVG, but it contains internal component names that must not be published and remains too information-dense for the existing 180px image slot.

## Presentation

- Create a simplified public derivative at `images/timely-agent-public.png`; do not copy the internal source PNG into the website repository.
- Use it only on the TIMELY-Agent homepage card; the detail-page hero remains text-only.
- Give this image a scoped project-card modifier with a moderately taller preview area so the overall architecture remains legible without changing other project cards.
- Use `object-fit: contain` and preserve the complete diagram; do not crop or distort it.
- Update the image alternative text to describe the two-environment TIMELY-Agent architecture at a useful, concise level.
- Use only generic public labels and exclude `FastOMOP`, `OMCP`, `CRES`, `OMOP-compatible`, unpublished metrics, dataset details, and other internal identifiers.
- Load the below-the-fold preview lazily and decode it asynchronously.

## Boundaries

- Keep `images/timely-agent-overview.svg` in the repository for history and existing SVG validation coverage.
- Keep the supplied internal PNG only in its source research folder outside the website repository.
- Do not place the detailed diagram in `timely-agent.html`.
- Do not change the TIMELY-Agent research copy, project ordering, or other project-card images.

## Verification

- Add a contract assertion for the public PNG path, reviewed-asset checksum, modifier class, public-label boundary, lazy-loading attributes, and alt text.
- Confirm the PNG exists and loads on the homepage.
- Inspect the homepage at desktop and mobile widths for containment, card balance, overflow, and image failures.
- Run the complete public-site contract suite, JavaScript syntax check, JSON validation, and Git format check.
