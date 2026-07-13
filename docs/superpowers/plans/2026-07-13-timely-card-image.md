# TIMELY-Agent Homepage Card Image Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the simplified TIMELY-Agent homepage-card SVG with the supplied architecture PNG and give only that preview enough height to remain useful.

**Architecture:** Store the PNG as a normal site asset and describe its card-specific presentation through an optional data field. The existing project loader appends that trusted modifier to the image class; a scoped CSS rule increases only the architecture preview height while preserving `object-fit: contain`.

**Tech Stack:** Static HTML, CSS, JSON, PNG asset, Python `unittest` contract tests.

---

### Task 1: Define the TIMELY card image contract

**Files:**
- Modify: `tests/test_site_contract.py`

- [ ] **Step 1: Write the failing assertions**

Extend the visible-project contract to require the first TIMELY-Agent record to use `images/timely-agent.png`, an `image_class` value of `project-image--architecture`, and concise architecture alt text. Require the homepage loader to append `project.image_class` to the image class without replacing the base `project-image` class.

- [ ] **Step 2: Run the focused test and verify RED**

Run: `python3 -m unittest tests.test_site_contract.PublicSiteContractTests.test_visible_projects_lead_with_timely_agent_and_hide_method -v`

Expected: FAIL because the project still references the old SVG and the loader has no image-class modifier.

### Task 2: Add and render the new preview

**Files:**
- Create: `images/timely-agent.png`
- Modify: `data/projects.json`
- Modify: `index.html`
- Modify: `style.css`

- [ ] **Step 1: Copy the supplied source asset**

Copy `/Users/linglong/Documents/HealTAC/IJCAI__ECAI_26_TIMELY_Agent/timely-agent.png` to `images/timely-agent.png` without recompression or modification.

- [ ] **Step 2: Update the TIMELY-Agent project record**

Point `image` at the PNG, add `image_class: "project-image--architecture"`, and replace the alt text with a concise description of the knowledge-facing and patient-facing TIMELY-Agent architecture. Keep the project copy, ordering, link, and all other records unchanged.

- [ ] **Step 3: Support the optional image modifier**

Keep `project-image` as the base class in the homepage loader and append the optional trusted `project.image_class` value when present.

- [ ] **Step 4: Add scoped CSS**

Add `.project-image--architecture` with a moderately taller height around 240px. Retain `object-fit: contain`; do not change the shared `.project-image` dimensions or other cards.

- [ ] **Step 5: Verify GREEN**

Run:

```bash
python3 -m unittest tests.test_site_contract.PublicSiteContractTests.test_visible_projects_lead_with_timely_agent_and_hide_method -v
python3 -m unittest discover -s tests -v
node --check script.js
jq empty data/projects.json data/publications.json data/team.json
git diff --check
```

Expected: focused test PASS; all 9 contract tests PASS; syntax, JSON, and format checks exit 0.

### Task 3: Browser QA and commit

**Files:**
- Verify: `index.html`
- Verify: `timely-agent.html`

- [ ] **Step 1: Inspect the homepage**

At desktop and mobile widths, confirm the PNG loads, remains fully contained, produces no horizontal overflow, and does not change the image heights of PyPOTS, CSAI, or DEARI.

- [ ] **Step 2: Confirm the detail-page boundary**

Confirm `timely-agent.html` still contains no hero image or `.timely-hero-visual` element.

- [ ] **Step 3: Commit**

```bash
git add images/timely-agent.png data/projects.json index.html style.css tests/test_site_contract.py
git commit -m "style: use TIMELY architecture preview"
```
