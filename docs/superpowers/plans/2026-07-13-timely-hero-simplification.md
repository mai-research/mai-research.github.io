# TIMELY-Agent Hero Simplification Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Remove the weak hero illustration and rebalance the TIMELY-Agent opening section as a restrained single-column research statement.

**Architecture:** Keep the existing hero section and content hierarchy, but remove the visual child and change its layout container from a two-column grid to a single text column. Retain the SVG asset and homepage project data because the homepage still uses it as the TIMELY-Agent project-card image.

**Tech Stack:** Static HTML, CSS, Python `unittest` contract tests, local browser QA.

---

### Task 1: Define the no-hero-visual contract

**Files:**
- Modify: `tests/test_site_contract.py:359-419`

- [ ] **Step 1: Write the failing contract assertion**

In `test_timely_page_has_required_sections_and_resource_note`, assert that `timely-agent.html` contains neither the `timely-hero-visual` class nor an image inside `#timely-hero`. Continue to leave `test_timely_svg_is_sanitized_and_uses_approved_labels` unchanged because the shared SVG remains a homepage asset.

- [ ] **Step 2: Run the focused test to verify it fails**

Run: `python3 -m unittest tests.test_site_contract.PublicSiteContractTests.test_timely_page_has_required_sections_and_resource_note -v`

Expected: FAIL because the current hero still contains `.timely-hero-visual` and its image.

### Task 2: Remove the illustration and rebalance the hero

**Files:**
- Modify: `timely-agent.html:52-63`
- Modify: `style.css:587-643`
- Modify: `style.css:760-766`
- Modify: `style.css:847-868`

- [ ] **Step 1: Remove the hero visual markup**

Delete the `.timely-hero-visual` element and its image. Keep the eyebrow, heading, and lead paragraph unchanged.

- [ ] **Step 2: Convert the hero to a single-column layout**

Change `.timely-hero-content` to a block container capped at 1100px. Cap its direct text wrapper at approximately 850px. Reduce the hero minimum height and vertical padding enough to suit the simpler composition while keeping the title visually dominant.

- [ ] **Step 3: Remove obsolete visual and breakpoint rules**

Delete `.timely-hero-visual` rules, the tablet-only hero gap override, the mobile `.timely-hero-content` grid/gap override, and the mobile visual padding override. Preserve the mobile hero padding and typography rules that still apply.

- [ ] **Step 4: Run the focused and complete tests**

Run:

```bash
python3 -m unittest tests.test_site_contract.PublicSiteContractTests.test_timely_page_has_required_sections_and_resource_note -v
python3 -m unittest discover -s tests -v
node --check script.js
git diff --check
```

Expected: focused test PASS; all 8 contract tests PASS; syntax and format checks exit 0.

### Task 3: Verify the rendered result and commit

**Files:**
- Verify: `timely-agent.html`
- Verify: `index.html`

- [ ] **Step 1: Run local browser QA**

Inspect TIMELY-Agent at 1280px, 900px, 769px, 768px, and 390px widths. Confirm the hero is a balanced single column, the title and lead wrap cleanly, the removed image leaves no empty column, there is no horizontal overflow, and the navigation still behaves at its breakpoint.

- [ ] **Step 2: Verify homepage asset retention**

Confirm the homepage TIMELY-Agent project card still loads `images/timely-agent-overview.svg` successfully.

- [ ] **Step 3: Commit**

```bash
git add timely-agent.html style.css tests/test_site_contract.py
git commit -m "style: simplify TIMELY hero"
```
