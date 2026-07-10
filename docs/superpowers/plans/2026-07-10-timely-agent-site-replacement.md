# TIMELY-Agent Website Replacement Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace METHOD across the visible MAI website with a concise, all-English TIMELY-Agent presentation while retaining METHOD history and assets in the repository.

**Architecture:** Preserve the repository's plain static HTML/CSS/JavaScript/JSON structure. Add one dedicated TIMELY-Agent page and one sanitized SVG overview, make visibility explicit in project data, reuse and harden the shared navigation script, and convert obsolete METHOD-bearing pages into relative redirects. Add a small standard-library test suite that enforces public-copy boundaries, asset integrity, and redirect contracts.

**Tech Stack:** HTML5, CSS custom properties and responsive media queries, vanilla JavaScript, JSON, SVG, Python 3 `unittest`, local HTTP server, in-app browser QA.

---

## File Map

**Create**

- `timely-agent.html` — canonical public TIMELY-Agent project page.
- `images/timely-agent-overview.svg` — sanitized four-stage public overview graphic.
- `tests/test_site_contract.py` — standard-library contract tests for content, redirects, assets, and integration hooks.
- `docs/superpowers/audits/2026-07-10-site-audit.md` — durable audit of unrelated issues found during the whole-site review.

**Modify**

- `data/projects.json` — add TIMELY-Agent first; mark METHOD hidden without deleting it.
- `data/team.json` — replace the METHOD reference in Linglong Qian's biography.
- `index.html` — fix the KCL link; filter hidden projects; handle project-loading failure; keep internal project links in the same tab.
- `style.css` — add TIMELY page styles and the missing responsive rules needed by the homepage and mobile navigation.
- `script.js` — make shared navigation initialisation defensive and honour reduced-motion preferences.
- `method.html` — replace deployed content with a redirect to `timely-agent.html` plus a fallback link.
- `docs.html` — replace obsolete duplicated content with a redirect to `index.html` plus a fallback link.
- `people/zina.html` — replace obsolete duplicated content with a redirect to `../index.html` plus a fallback link.

**Retain unchanged**

- `images/method.png`, `docs/method.pdf`, `talks/*.pdf`, and the METHOD record in `data/publications.json`.

## Public Copy to Use

### Homepage project summary

> TIMELY-Agent is an agentic framework for building clinically grounded, auditable multimodal reasoning benchmarks from longitudinal electronic health records. It turns irregular patient timelines into compact, provenance-preserving reasoning episodes and supports evaluation of temporal grounding, cross-modal consistency, and evidence use. The framework separates public knowledge synthesis from governed local work with patient data, helping researchers inspect how benchmark tasks are specified, assembled, and audited.

### Linglong Qian biography

> Linglong's research bridges deep learning, symbolic reasoning, and medical data science, with a focus on temporal dynamics, multimodal signals, and clinical text. He is developing TIMELY-Agent, a framework for constructing auditable multimodal clinical reasoning benchmarks, and contributes to open-source tools for time-series imputation and benchmarking.

### TIMELY page section copy

**Hero**

- Eyebrow: `Active Research`
- Title: `TIMELY-Agent`
- Subtitle: `An agentic framework for building clinically grounded, auditable multimodal reasoning benchmarks from longitudinal EHR data.`

**Overview**

> Electronic health records are long, irregular and multimodal. Static question answering and endpoint prediction can hide whether a model used the right evidence at the right time. TIMELY-Agent reconstructs clinically meaningful patient state before evaluation begins.

> A reasoning episode is a compact, provenance-preserving view of patient history centred on a clinically meaningful question. It brings together temporally bounded structured data and relevant clinical text without reducing the record to a single label or exposing an entire admission at once.

**Framework cards**

- `Clinical knowledge` — `Define meaningful conditions, anchor events and temporal patterns from reviewed clinical sources.`
- `Governed retrieval` — `Retrieve relevant evidence through controlled interfaces inside secure local environments.`
- `Reasoning episodes` — `Align structured trajectories with clinical note fragments around meaningful questions.`
- `Tasks and audit` — `Evaluate temporal grounding, cross-modal consistency and the use of supporting evidence.`

**Privacy**

> TIMELY-Agent separates knowledge-facing work from patient-facing computation. Public clinical sources can support benchmark specification, while patient-level data remain within governed local infrastructure.

> Reviewed specifications may cross into the local environment; real patient data do not cross out. This separation supports traceability without claiming that the current research prototype is a complete deployment or privacy guarantee.

**Research foundations**

> Pilot implementations explore multimodal episode construction and behavioural auditing on critical-care data. These foundations inform the wider TIMELY-Agent framework while the research programme continues to develop.

**Contact**

> Interested in trustworthy clinical agents, temporal reasoning or multimodal benchmark design? Contact the MAI Research Group.

Footer note: `Publications and project resources will be linked here when available.`

---

### Task 1: Add Failing Public-Site Contract Tests

**Files:**

- Create: `tests/test_site_contract.py`
- Reference: `docs/superpowers/specs/2026-07-10-timely-agent-site-replacement-design.md`

- [ ] **Step 1: Create the standard-library test module**

Implement the following complete test structure. Use `HTMLParser` so the suite has no third-party dependency:

```python
import json
import re
import unittest
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit


ROOT = Path(__file__).resolve().parents[1]
BANNED_PUBLIC_TERMS = {
    "METHOD",
    "FastOMOP",
    "OMCP",
    "CRES",
    "12,000",
    "9,587",
    "53,070",
    "0.655",
    "0.535",
}


class VisibleTextParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.hidden_depth = 0
        self.parts = []

    def handle_starttag(self, tag, attrs):
        if tag in {"script", "style", "template"}:
            self.hidden_depth += 1

    def handle_endtag(self, tag):
        if tag in {"script", "style", "template"} and self.hidden_depth:
            self.hidden_depth -= 1

    def handle_data(self, data):
        if not self.hidden_depth:
            self.parts.append(data)

    @property
    def text(self):
        return " ".join(self.parts)


class AssetParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.references = []

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        for key in ("href", "src"):
            if values.get(key):
                self.references.append(values[key])


def read(path):
    return (ROOT / path).read_text(encoding="utf-8")


def read_json(path):
    return json.loads(read(path))


def visible_text(path):
    parser = VisibleTextParser()
    parser.feed(read(path))
    return parser.text


class SiteContractTests(unittest.TestCase):
    def test_projects_make_timely_first_and_hide_method(self):
        projects = read_json("data/projects.json")
        visible = [project for project in projects if not project.get("hidden", False)]
        self.assertEqual("TIMELY-Agent", visible[0]["title"])
        self.assertEqual("timely-agent.html", visible[0]["link"])
        method = next(project for project in projects if project["title"] == "METHOD")
        self.assertTrue(method["hidden"])

    def test_public_copy_does_not_expose_method_or_unpublished_details(self):
        visible_projects = [
            project for project in read_json("data/projects.json")
            if not project.get("hidden", False)
        ]
        public_text = " ".join([
            visible_text("index.html"),
            visible_text("timely-agent.html"),
            " ".join(member.get("bio", "") for member in read_json("data/team.json")),
            " ".join(
                f'{project.get("title", "")} {project.get("text", "")}'
                for project in visible_projects
            ),
        ])
        for term in BANNED_PUBLIC_TERMS:
            self.assertNotIn(term.casefold(), public_text.casefold())

    def test_timely_page_has_approved_sections_and_no_roadmap(self):
        page = read("timely-agent.html")
        for section_id in ("overview", "framework", "privacy", "foundations", "contact"):
            self.assertRegex(page, rf'id=["\']{section_id}["\']')
        self.assertNotIn("Status & Roadmap", page)
        self.assertIn("Publications and project resources will be linked here when available.", page)

    def test_sanitized_svg_uses_only_public_workflow_labels(self):
        svg = read("images/timely-agent-overview.svg")
        for label in ("Clinical knowledge", "Governed retrieval", "Reasoning episodes", "Tasks and audit"):
            self.assertIn(label, svg)
        for term in BANNED_PUBLIC_TERMS:
            self.assertNotIn(term.casefold(), svg.casefold())

    def test_legacy_pages_redirect_with_fallback_links(self):
        redirects = {
            "method.html": "timely-agent.html",
            "docs.html": "index.html",
            "people/zina.html": "../index.html",
        }
        for path, destination in redirects.items():
            page = read(path)
            self.assertRegex(page, rf'http-equiv=["\']refresh["\']')
            self.assertRegex(
                page,
                rf'content=["\']0;\s*url={re.escape(destination)}["\']',
            )
            self.assertRegex(
                page,
                rf'<link[^>]+rel=["\']canonical["\'][^>]+href=["\']{re.escape(destination)}["\']',
            )
            self.assertRegex(page, rf'<a[^>]+href=["\']{re.escape(destination)}["\']')

    def test_homepage_filters_hidden_projects_and_reports_load_failure(self):
        page = read("index.html")
        self.assertIn(".filter(project => !project.hidden)", page)
        self.assertIn("Unable to load projects", page)
        self.assertIn('href="https://www.kcl.ac.uk/"', page)

    def test_internal_page_assets_exist(self):
        for page_path in ("index.html", "timely-agent.html"):
            parser = AssetParser()
            parser.feed(read(page_path))
            base = (ROOT / page_path).parent
            for reference in parser.references:
                parsed = urlsplit(reference)
                if parsed.scheme or reference.startswith(("#", "mailto:", "data:")):
                    continue
                target = (base / parsed.path).resolve()
                self.assertTrue(target.exists(), f"Missing {reference} referenced by {page_path}")

    def test_responsive_contract_exists(self):
        css = read("style.css")
        self.assertIn("@media (max-width: 768px)", css)
        self.assertIn(".timely-workflow-grid", css)
        self.assertIn("body.mobile-nav-open .nav-right-group", css)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the contract suite and verify the expected baseline failure**

Run:

```bash
python3 -m unittest tests.test_site_contract -v
```

Expected: FAIL because `timely-agent.html` and `images/timely-agent-overview.svg` do not exist, METHOD is still visible, project hiding is not implemented, and responsive rules are missing.

- [ ] **Step 3: Commit the failing tests**

```bash
git add tests/test_site_contract.py
git commit -m "test: define TIMELY public site contract"
```

---

### Task 2: Add TIMELY Project Data and Sanitized Visual

**Files:**

- Modify: `data/projects.json:1-38`
- Modify: `data/team.json:13-23`
- Create: `images/timely-agent-overview.svg`
- Test: `tests/test_site_contract.py`

- [ ] **Step 1: Add the TIMELY-Agent project record before METHOD**

Use the approved homepage copy above and this record shape:

```json
{
  "title": "TIMELY-Agent",
  "text": "TIMELY-Agent is an agentic framework for building clinically grounded, auditable multimodal reasoning benchmarks from longitudinal electronic health records. It turns irregular patient timelines into compact, provenance-preserving reasoning episodes and supports evaluation of temporal grounding, cross-modal consistency, and evidence use. The framework separates public knowledge synthesis from governed local work with patient data, helping researchers inspect how benchmark tasks are specified, assembled, and audited.",
  "image": "images/timely-agent-overview.svg",
  "image_alt": "Four-stage TIMELY-Agent workflow from clinical knowledge to audited reasoning tasks",
  "link": "timely-agent.html",
  "link_label": "Open Project",
  "title_link": "timely-agent.html"
}
```

Add `"hidden": true` to the retained METHOD record. Do not modify its other fields.

- [ ] **Step 2: Replace the METHOD reference in Linglong Qian's biography**

Use the exact approved biography in the Public Copy section. Do not modify other team records.

- [ ] **Step 3: Create the sanitized SVG overview**

Create a 1200×630 accessible SVG using only the existing MAI palette and these visible labels:

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 630" role="img" aria-labelledby="title desc">
  <title id="title">TIMELY-Agent workflow</title>
  <desc id="desc">Four stages connect clinical knowledge, governed retrieval, reasoning episodes, and tasks and audit.</desc>
  <!-- Background: #f1f3f5; heading and borders: #005f73; accent: #0a9396; cards: #ffffff. -->
  <!-- Render the four approved labels as equal cards joined by simple right arrows. -->
</svg>
```

Do not include standards, infrastructure, model names, internal artefact names, results, status, or acronyms such as CRES, OMOP, or OMCP.

- [ ] **Step 4: Validate JSON and run the targeted data/visual tests**

Run:

```bash
python3 -m json.tool data/projects.json >/dev/null
python3 -m json.tool data/team.json >/dev/null
python3 -m unittest \
  tests.test_site_contract.SiteContractTests.test_projects_make_timely_first_and_hide_method \
  tests.test_site_contract.SiteContractTests.test_sanitized_svg_uses_only_public_workflow_labels -v
```

Expected: PASS.

- [ ] **Step 5: Commit data and visual assets**

```bash
git add data/projects.json data/team.json images/timely-agent-overview.svg
git commit -m "feat: add TIMELY project data and public visual"
```

---

### Task 3: Build the TIMELY Detail Page and Responsive Shared Styles

**Files:**

- Create: `timely-agent.html`
- Modify: `style.css:102-573`
- Modify: `script.js:1-128`
- Test: `tests/test_site_contract.py`

- [ ] **Step 1: Create the semantic TIMELY page shell**

Build `timely-agent.html` with:

- the same MAI inline SVG logo used by `index.html`;
- `<body class="timely-page">`;
- fixed header navigation to `#overview`, `#framework`, `#privacy`, `#foundations`, and `#contact`;
- `<section id="timely-hero">` with the approved eyebrow, title, subtitle, and sanitized SVG;
- sections in the approved order using the exact Public Copy above;
- four `<article class="timely-workflow-card">` elements inside `.timely-workflow-grid`;
- a two-panel `.privacy-boundary` treatment with a one-way arrow;
- a contact button linking to `mailto:zina.ibrahim@kcl.ac.uk`;
- the established MAI footer and `script.js`;
- no Publications, Talks, Demo, Open Source, Status, or Roadmap section;
- no external TIMELY project or paper URL.

The page `<head>` must include:

```html
<title>TIMELY-Agent | MAI Research Group</title>
<meta name="description" content="TIMELY-Agent is an MAI framework for building clinically grounded, auditable multimodal reasoning benchmarks from longitudinal electronic health records.">
<link rel="stylesheet" href="style.css?v=3">
```

- [ ] **Step 2: Add scoped TIMELY styles using existing variables**

Add focused styles for:

```css
.timely-page
#timely-hero
.timely-hero-content
.timely-eyebrow
.timely-hero-visual
.timely-content
.timely-lead
.timely-workflow-grid
.timely-workflow-card
.privacy-boundary
.privacy-panel
.privacy-arrow
.timely-contact
.timely-resource-note
```

Use only existing MAI variables and the approved palette. Keep body copy left-aligned with a readable maximum width; do not justify text.

- [ ] **Step 3: Add the missing responsive navigation and grid rules**

Add `@media (max-width: 768px)` rules that:

- show `#mobile-menu-toggle`;
- move `.nav-right-group` into a full-width fixed dropdown panel;
- stack `.nav-links` vertically;
- reveal the panel only through `body.mobile-nav-open .nav-right-group`;
- override the unscrolled-header link colour and text shadow inside the mobile dropdown so links remain dark and readable on the light panel;
- change `.projects-grid`, `.timely-workflow-grid`, and `.privacy-boundary` to one column;
- resize hero headings and section padding;
- keep all text at readable widths.

Add an intermediate breakpoint for the homepage project grid:

```css
@media (max-width: 1100px) and (min-width: 769px) {
  .projects-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
}
```

Add reduced-motion handling:

```css
@media (prefers-reduced-motion: reduce) {
  html { scroll-behavior: auto; }
  *, *::before, *::after { transition-duration: 0.01ms !important; }
}
```

- [ ] **Step 4: Harden the shared navigation script**

In `script.js`:

- return early from theme-toggle setup if the button or icon is missing;
- guard `mainHeader` and `mobileMenuToggle` before attaching listeners;
- remove unused variables;
- set smooth-scroll behaviour to `auto` when `prefers-reduced-motion: reduce` matches;
- retain existing footer-year and mobile-menu ARIA updates.

- [ ] **Step 5: Run detail-page, asset, and responsive tests**

Run:

```bash
node --check script.js
python3 -m unittest \
  tests.test_site_contract.SiteContractTests.test_timely_page_has_approved_sections_and_no_roadmap \
  tests.test_site_contract.SiteContractTests.test_internal_page_assets_exist \
  tests.test_site_contract.SiteContractTests.test_responsive_contract_exists -v
```

Expected: PASS.

- [ ] **Step 6: Commit the detail page and responsive foundation**

```bash
git add timely-agent.html style.css script.js
git commit -m "feat: build responsive TIMELY project page"
```

---

### Task 4: Integrate TIMELY on the Homepage

**Files:**

- Modify: `index.html:54-61`
- Modify: `index.html:173-211`
- Test: `tests/test_site_contract.py`

- [ ] **Step 1: Fix the malformed King's College London link**

Replace the invalid `<href>` element with:

```html
<a href="https://www.kcl.ac.uk/" target="_blank" rel="noopener noreferrer">King's College London</a>
```

Also normalise the BHI and PHI links to `target="_blank" rel="noopener noreferrer"`.

- [ ] **Step 2: Filter hidden projects before rendering**

Change the project pipeline to:

```javascript
const visibleProjects = projects.filter(project => !project.hidden);
container.innerHTML = visibleProjects.map(project => /* existing card template */).join('');
```

- [ ] **Step 3: Keep internal project links in the current tab**

Add a small helper:

```javascript
function externalLinkAttributes(url = '') {
  return /^https?:\/\//i.test(url)
    ? ' target="_blank" rel="noopener noreferrer"'
    : '';
}
```

Use it for both `title_link` and footer `link` templates. This keeps `timely-agent.html` in the current tab and preserves new-tab behaviour for GitHub links.

- [ ] **Step 4: Add explicit project-loading failure handling**

Wrap the fetch and render path in `try/catch`, check `response.ok`, and render:

```html
<p class="load-error" role="status">Unable to load projects right now. Please try again later.</p>
```

Log the caught error to the console for maintainers.

- [ ] **Step 5: Run homepage integration and full contract tests**

Run:

```bash
python3 -m unittest tests.test_site_contract.SiteContractTests.test_homepage_filters_hidden_projects_and_reports_load_failure -v
python3 -m unittest tests.test_site_contract -v
```

Expected: redirect tests still FAIL; all other tests PASS.

- [ ] **Step 6: Commit homepage integration**

```bash
git add index.html
git commit -m "feat: surface TIMELY and hide METHOD on homepage"
```

---

### Task 5: Replace Legacy METHOD-Bearing Pages with Redirects

**Files:**

- Modify: `method.html:1-150`
- Modify: `docs.html:1-354`
- Modify: `people/zina.html:1-364`
- Test: `tests/test_site_contract.py`

- [ ] **Step 1: Replace `method.html` with a TIMELY redirect**

Use a complete, valid HTML document with:

```html
<meta http-equiv="refresh" content="0; url=timely-agent.html">
<link rel="canonical" href="timely-agent.html">
<title>Project moved | MAI Research Group</title>
```

The body must contain one plain-English fallback sentence and `<a href="timely-agent.html">Continue to TIMELY-Agent</a>`. Do not present or repeat historical METHOD content.

- [ ] **Step 2: Replace obsolete duplicate pages with homepage redirects**

Use the same minimal pattern:

- `docs.html` → `index.html` with `Continue to the MAI Research Group website`;
- `people/zina.html` → `../index.html` with `Continue to the MAI Research Group website`.

Do not create archive copies and do not delete any METHOD binary asset or historical data record.

- [ ] **Step 3: Run redirect and full contract tests**

Run:

```bash
python3 -m unittest tests.test_site_contract.SiteContractTests.test_legacy_pages_redirect_with_fallback_links -v
python3 -m unittest tests.test_site_contract -v
```

Expected: PASS.

- [ ] **Step 4: Confirm retained METHOD assets still exist**

Run:

```bash
test -f images/method.png
test -f docs/method.pdf
test -f talks/aifestival.pdf
test -f talks/cogstack.pdf
test -f talks/dsit.pdf
```

Expected: exit status 0.

- [ ] **Step 5: Commit legacy redirects**

```bash
git add method.html docs.html people/zina.html
git commit -m "feat: redirect legacy METHOD pages"
```

---

### Task 6: Perform Browser QA and Record the Whole-Site Audit

**Files:**

- Create: `docs/superpowers/audits/2026-07-10-site-audit.md`
- Verify: `index.html`, `timely-agent.html`, legacy redirects, all edited assets and data.

- [ ] **Step 1: Start the static site locally**

Run:

```bash
python3 -m http.server 4173 --bind 127.0.0.1
```

Expected: site available at `http://127.0.0.1:4173/`.

- [ ] **Step 2: Verify desktop rendering with the Browser skill**

Use `@browser:control-in-app-browser` at a representative desktop viewport and inspect:

- homepage hero, TIMELY card order, project links, team biography, publication filtering, contact, and footer;
- TIMELY hero, navigation anchors, sanitized visual, workflow cards, privacy panels, foundations copy, contact, and footer;
- console warnings/errors and failed local requests;
- legacy redirect destinations and fallback content.

Expected: no horizontal overflow, no collapsed text columns, no failed local assets, and no METHOD visible in the user journey.

- [ ] **Step 3: Verify phone rendering and mobile navigation**

Use a representative 390×844 viewport. Open and close the mobile menu with keyboard-accessible controls, follow one section link, and confirm `aria-expanded` returns to `false` after navigation.

Expected: one-column project/workflow/privacy layouts; readable text; no clipped header, cards, or contact button.

- [ ] **Step 4: Write the audit report without changing unrelated content**

Create `docs/superpowers/audits/2026-07-10-site-audit.md` with:

- scope and verification date;
- issues fixed as part of this task;
- unresolved findings with severity and evidence;
- explicit note that unresolved items were not changed.

Include, if still confirmed, these already observed candidates:

- DEARI links to the CSAI repository rather than a DEARI-specific destination;
- the hidden theme toggle and mismatch between `html.dark-mode` JavaScript and `body.dark-mode` CSS variables;
- likely misspelled highlighted-author entries (`zhangzhu Joshua`, `haoyu wu`);
- publication-list length and incomplete metadata quality concerns;
- repository hygiene issues such as `.DS_Store` and untitled RTF files.

Do not assert an issue unless rechecked against the final state.

- [ ] **Step 5: Commit the audit report**

```bash
git add docs/superpowers/audits/2026-07-10-site-audit.md
git commit -m "docs: record MAI website audit findings"
```

---

### Task 7: Final Verification and Review

**Files:**

- Verify all modified files.
- Reference: `docs/superpowers/specs/2026-07-10-timely-agent-site-replacement-design.md`

- [ ] **Step 1: Run all automated checks from a clean local state**

Run:

```bash
python3 -m unittest discover -s tests -v
python3 -m json.tool data/projects.json >/dev/null
python3 -m json.tool data/team.json >/dev/null
python3 -m json.tool data/publications.json >/dev/null
node --check script.js
git diff --check
```

Expected: all tests PASS; JSON and JavaScript checks exit 0; no whitespace errors.

- [ ] **Step 2: Run focused content-boundary searches**

Run:

```bash
rg -n -i '12,000|9,587|53,070|0\.655|0\.535|FastOMOP|OMCP|CRES|Status & Roadmap' \
  index.html timely-agent.html images/timely-agent-overview.svg data/team.json
```

Expected: no matches.

Run:

```bash
rg -n -i 'METHOD' index.html timely-agent.html data/team.json docs.html people/zina.html
```

Expected: only the deliberate publication-filter token inside the non-visible `index.html` script may remain; no visible HTML or biography match.

- [ ] **Step 3: Confirm intended repository changes and retained history**

Run:

```bash
git status --short
git diff --stat origin/main...HEAD
git log --oneline --decorate -10
```

Expected: no uncommitted implementation files; commits are scoped; historical METHOD assets remain tracked.

- [ ] **Step 4: Request code review**

Use `@superpowers:requesting-code-review` with the design spec, implementation plan, and complete diff. Resolve blocking findings and rerun the relevant checks.

- [ ] **Step 5: Verify before claiming completion**

Use `@superpowers:verification-before-completion` and rerun the final commands after the last change. Record the actual pass counts and browser QA observations in the handoff.
