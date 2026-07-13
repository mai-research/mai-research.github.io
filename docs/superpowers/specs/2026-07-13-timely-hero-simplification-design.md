# TIMELY-Agent Hero Simplification Design

## Decision

Remove the workflow illustration from the TIMELY-Agent hero and do not replace it. The illustration repeats the Framework section, reads as placeholder artwork, and weakens the otherwise restrained MAI visual language.

## Layout

The hero becomes a single left-aligned text column within the existing 1100px page container. The text block is capped at approximately 850px so the title and research statement remain readable without spanning the full viewport. The hero height and vertical padding are reduced slightly to reflect the lower information density while preserving a deliberate opening section.

## Scope

- Remove the hero image markup from `timely-agent.html`.
- Replace the two-column hero grid with a single-column layout in `style.css`.
- Remove hero-image-only styles and obsolete responsive overrides.
- Keep the overview SVG because it remains the TIMELY-Agent project-card image on the homepage.
- Leave all research copy, navigation, downstream sections, and homepage project rendering unchanged.

## Verification

- Add a contract assertion that the project page contains no hero visual or hero image.
- Run the complete public-site contract suite and JavaScript/format checks.
- Inspect the page at desktop, mid-width, mobile, and the 768/769px breakpoint boundary for balance, wrapping, overflow, and asset failures.
