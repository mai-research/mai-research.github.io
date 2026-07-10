# TIMELY-Agent Website Replacement Design

## Summary

Replace METHOD as the visible flagship project on the MAI Research Group website with a concise, all-English TIMELY-Agent project presentation. METHOD source files and historical assets remain in the repository, but the public site must expose no navigation, card, biography, publication, or legacy-page path that presents METHOD as an active project. Requests to the former METHOD project page redirect to the new TIMELY-Agent page.

The new page uses the existing MAI visual language: Montserrat and Lato typography, the current dark blue and teal palette, white cards, restrained rounded corners, the existing header and footer, and the current responsive navigation. It presents TIMELY-Agent as an active research programme without publishing unpublished numerical results, detailed roadmaps, or links that do not yet exist.

## Goals

- Make TIMELY-Agent the first visible project on the homepage.
- Provide a dedicated, responsive TIMELY-Agent project page in English.
- Explain the research through a concise narrative that is understandable to clinical, research, and technical visitors.
- Preserve the distinction between the wider framework and its pilot implementations.
- Keep unpublished details private: no sample counts, model scores, directional audit results, or internal milestones.
- Hide METHOD throughout the public user journey while retaining its files and history in the repository.
- Preserve the website's current static architecture and visual identity.
- Verify the complete site on desktop and mobile and produce a separate audit summary for unrelated findings.

## Non-Goals

- Do not delete METHOD HTML, images, PDFs, publication data, talks, or Git history.
- Do not publish a TIMELY-Agent GitHub repository, preprint, DOI, or other external resource that does not yet exist.
- Do not add an interactive demo, CMS, framework, build system, backend, analytics, or new deployment platform.
- Do not redesign the MAI homepage or unrelated project, team, and publication sections.
- Do not publish a standalone Status or Roadmap section.
- Do not silently repair unrelated third-party links or research metadata; report those findings separately.

## Public Content Boundaries

The TIMELY-Agent page may communicate the following:

- TIMELY-Agent is an active MAI research project.
- It is an agentic framework for building clinically grounded, auditable multimodal reasoning benchmarks from longitudinal electronic health record data.
- It addresses the difficulty of reconstructing patient state from long, irregular, multimodal records.
- It uses a four-stage conceptual workflow:
  1. clinical knowledge specification;
  2. governed local retrieval;
  3. multimodal reasoning-episode construction;
  4. task synthesis and behavioural audit.
- It separates knowledge-facing work on public sources from patient-facing work inside governed local environments.
- Pilot implementations explore episode construction and behavioural auditing on critical-care data.
- Publications and project resources will be linked when they become public.

The public site must not disclose:

- exact cohort, prompt, task, model, or token counts;
- unpublished performance scores or model comparisons;
- counterfactual cue-execution results;
- internal funding, conference-submission, or fellowship plans;
- unannounced implementation partners or infrastructure commitments;
- claims that the entire framework is complete or clinically validated.

## Information Architecture

### Homepage project card

The first project card becomes TIMELY-Agent and contains:

- the title `TIMELY-Agent`;
- a concise image and accessible alternative text;
- a short summary of approximately 70–100 words;
- an `Open Project` link to `timely-agent.html`;
- no external repository, paper, or demo link.

The summary should explain that TIMELY-Agent converts longitudinal EHR data into auditable multimodal reasoning episodes and supports evaluation of temporal grounding, cross-modal consistency, and evidence use.

### TIMELY-Agent detail page

The page uses the existing MAI header, responsive navigation, footer, and global stylesheet. Its visible navigation contains only sections that exist on the page.

1. **Hero**
   - eyebrow label: `Active Research`;
   - title: `TIMELY-Agent`;
   - subtitle: `An agentic framework for building clinically grounded, auditable multimodal reasoning benchmarks from longitudinal EHR data.`

2. **Overview: From patient timelines to reasoning episodes**
   - explain that EHRs are long, irregular, and multimodal;
   - define a reasoning episode as a compact, provenance-preserving view of patient history centred on a meaningful clinical question;
   - avoid numerical results and dense terminology.

3. **Framework: How the framework works**
   - show four concise cards for clinical knowledge, governed retrieval, reasoning episodes, and tasks and audit;
   - keep detailed internal artefact names out of the primary visual treatment unless needed in supporting copy.

4. **Privacy: Privacy-aware by design**
   - explain the knowledge-facing and patient-facing separation;
   - show one-way transfer of reviewed specifications;
   - state that real patient data remain in governed local infrastructure;
   - avoid overclaiming formal privacy guarantees or deployment readiness.

5. **Research foundations**
   - state that pilot implementations explore multimodal episode construction and behavioural auditing on critical-care data;
   - label this as foundation work informing the wider framework;
   - contain no unpublished figures, scores, model names, or dataset sizes.

6. **Contact**
   - invite collaboration on trustworthy clinical agents, temporal reasoning, and multimodal benchmark design;
   - link to the existing MAI contact section or the established MAI contact email;
   - include the note: `Publications and project resources will be linked here when available.`

There is no dedicated Status, Roadmap, Publications, Talks, Demo, or Open Source section until public artefacts exist.

## Visual Design

- Reuse the existing CSS custom properties, especially `--primary-color`, `--accent-color`, `--card-bg`, `--bg-color`, `--text-color`, and `--border-color`.
- Reuse the current Montserrat heading and Lato body typography.
- Reuse the MAI logo, fixed header behaviour, rounded navigation treatment, and footer.
- Use the existing primary dark blue (`#005f73`) and accent teal (`#0a9396`) as the dominant colours.
- Use white cards on the existing light grey page background.
- Keep the hero visually related to the main site but simpler than the homepage background treatment.
- Use an existing TIMELY-Agent architecture image as the project image. Copy it into the repository's `images/` directory during implementation and provide meaningful alt text.
- Ensure cards stack cleanly on narrow screens and that text does not collapse into narrow columns.
- Respect reduced-motion preferences for smooth-scrolling or decorative transitions added by the page.

## Site Integration and Data Flow

The site remains plain static HTML, CSS, JavaScript, and JSON.

- `data/projects.json` gains a TIMELY-Agent record at the first visible position.
- The existing METHOD record remains in the JSON for historical retention but gains an explicit hidden state.
- The project renderer in `index.html` or its supporting script filters hidden project records before rendering.
- `data/team.json` replaces the METHOD reference in Linglong Qian's biography with a concise TIMELY-Agent reference.
- `data/publications.json` retains the METHOD publication record. Existing title filtering continues to exclude it from the homepage publication renderer.
- `timely-agent.html` is the canonical TIMELY-Agent detail page.
- `method.html` becomes a lightweight legacy redirect to `timely-agent.html`, using a canonical link and a visible fallback link for environments where automatic redirection is unavailable.
- `docs.html` and `people/zina.html` become lightweight redirects to the canonical homepage because they are obsolete duplicated snapshots that expose METHOD and contain broken relative asset paths.
- METHOD images, PDFs, and talk files remain in place and are no longer linked by visible pages.

## Failure Handling

- If homepage project JSON fails to load, the page should show a concise project-loading error instead of leaving a silent empty section.
- If the TIMELY-Agent project image cannot load, accessible alternative text must still communicate the project's subject.
- Legacy redirects must include a visible fallback link.
- Navigation links must target existing section IDs.
- All links that open new tabs must use `rel="noopener noreferrer"`.
- No TIMELY page control may depend on unavailable external APIs or third-party JavaScript.

## Accessibility and Responsive Behaviour

- Use semantic landmarks, headings in order, descriptive link text, and meaningful image alt text.
- Preserve keyboard access for navigation and the mobile menu.
- Preserve visible focus styles.
- Ensure the mobile navigation toggle has correct `aria-label` and `aria-expanded` values.
- Maintain readable line lengths and avoid justified text on narrow screens.
- Verify at desktop and representative phone viewports.
- Maintain sufficient contrast using the existing MAI palette.

## Adjacent Corrections Included

The implementation may correct only high-confidence issues directly adjacent to this replacement:

- fix the malformed King's College London link markup on the homepage;
- remove the public path to the broken METHOD detail layout by redirecting it;
- redirect obsolete duplicated pages whose relative asset paths are broken and whose content still exposes METHOD;
- add a graceful homepage projects-loading error if the current renderer fails silently.

All other findings, including suspicious third-party URLs, publication metadata quality, team copy inconsistencies, or broader design concerns, belong in the final audit report unless separately authorised.

## Verification

Verification must cover:

- JSON validity for all edited data files;
- search-based confirmation that no visible production page or rendered data contains METHOD references, excluding retained legacy files and hidden historical records;
- homepage project rendering and project order;
- TIMELY-Agent page navigation, headings, image, contact link, and footer;
- `method.html` redirect and fallback link;
- `docs.html` and `people/zina.html` redirects and fallback links;
- desktop and phone layouts;
- mobile-menu open and close behaviour;
- browser console errors and failed local asset requests;
- internal page and anchor links;
- absence of unpublished numerical results and unannounced external links;
- clean Git diff limited to intended files plus the design and plan documents.

## Acceptance Criteria

- TIMELY-Agent is the first visible homepage project and opens a dedicated English detail page.
- The detail page follows the approved concise research narrative and MAI visual style.
- The detail page contains no standalone Status or Roadmap section and no unpublished numerical results.
- METHOD is absent from visible homepage projects, team biographies, publications, current detail pages, and obsolete duplicated pages.
- Direct access to `method.html` redirects to `timely-agent.html` and offers a fallback link.
- Historical METHOD files and data remain in the repository.
- The site works without a build step and renders correctly at desktop and phone widths.
- The final handoff includes verification evidence and a separate site-audit summary for unrelated issues.
