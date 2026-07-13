# TIMELY-Agent Homepage Card Image Design

## Decision

Use the supplied `timely-agent.png` as the TIMELY-Agent homepage project-card image. The new architecture diagram is visually stronger and more representative than the simplified workflow SVG, but it remains too information-dense for the existing 180px image slot.

## Presentation

- Copy the supplied PNG into `images/timely-agent.png` inside the website repository.
- Use it only on the TIMELY-Agent homepage card; the detail-page hero remains text-only.
- Give this image a scoped project-card modifier with a moderately taller preview area so the overall architecture remains legible without changing other project cards.
- Use `object-fit: contain` and preserve the complete diagram; do not crop or distort it.
- Update the image alternative text to describe the two-environment TIMELY-Agent architecture at a useful, concise level.

## Boundaries

- Keep `images/timely-agent-overview.svg` in the repository for history and existing SVG validation coverage.
- Do not place the detailed diagram in `timely-agent.html`.
- Do not change the TIMELY-Agent research copy, project ordering, or other project-card images.

## Verification

- Add a contract assertion for the TIMELY-Agent PNG path, modifier class, and alt text.
- Confirm the PNG exists and loads on the homepage.
- Inspect the homepage at desktop and mobile widths for containment, card balance, overflow, and image failures.
- Run the complete public-site contract suite, JavaScript syntax check, JSON validation, and Git format check.
