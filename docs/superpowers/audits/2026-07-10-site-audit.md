# MAI Research Website Audit

## Scope and method

This audit covers the public homepage, the TIMELY-Agent project page, project and team data, publication rendering, shared navigation, and the three legacy entry points (`method.html`, `docs.html`, and `people/zina.html`). The review combined source inspection, repository-wide content searches, local HTTP response checks for pages and assets, JSON and JavaScript validation, and the automated public-site contract suite.

The required live browser connection was unavailable in the review environment, so final visual and interaction checks at desktop and mobile widths remain a release check rather than a completed part of this audit.

## Verified release behaviour

- TIMELY-Agent is the first public project and links internally to `timely-agent.html` without forcing a new tab.
- The retained METHOD project record is marked as hidden and is filtered out before homepage cards are rendered.
- The TIMELY-Agent page uses concise English research-facing copy, a restrained MAI visual system, accessible section navigation, and no unpublished metrics, internal dataset names, or roadmap claims.
- The shared mobile navigation exposes its expanded state, moves focus into the open menu, closes on Escape, restores focus to the toggle, and resets when the viewport returns to desktop width.
- Project loading checks unsuccessful responses and presents a readable status message if project data cannot be loaded.
- Legacy METHOD and superseded profile/document pages contain minimal canonical meta-refresh redirects with visible fallback links; historical METHOD assets and records remain in the repository.

## Prioritised follow-up findings

### P1 — Correct or document the DEARI repository link

`data/projects.json` sends both the CSAI and DEARI cards to the CSAI repository. Confirm the intended DEARI destination and update the link, or explicitly document why the shared destination is correct.

### P1 — Resolve the dormant dark-mode implementation

The JavaScript applies `dark-mode` to the root `html` element, while the theme variables and logo rules are scoped to `body.dark-mode`. The theme button is also forcibly hidden in CSS. Decide whether dark mode remains a supported feature; then either align the class target and expose an accessible control, or remove the unused implementation.

### P2 — Validate publication author aliases

The homepage highlights `zhangzhu Joshua` and `haoyu wu`, while the team data names the corresponding members as `Dr Zhangshu Joshua Jiang` and `Mr Haoyu Wang`. Confirm the intended publication-name variants so the correct authors are highlighted consistently; stable identifiers would be safer than free-text matching.

### P2 — Curate publication metadata

The publication dataset contains entries with missing venue metadata and many truncated author lists. Review titles, authors, venues, dates, and links against an authoritative source before treating the list as a maintained scholarly record.

### P3 — Add an explicit site icon

A browser-style homepage request asks for `/favicon.ico`, which currently returns 404. Add an intentional favicon and declare it in the document head to remove the missing-resource request.

### P3 — Clean repository-only artefacts

Tracked `.DS_Store` files and two `Untitled*.rtf` files appear unrelated to the public site. Confirm that the RTF files are not required, remove unnecessary artefacts, and add suitable ignore rules to prevent them from returning.
