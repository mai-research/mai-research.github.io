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

Extend the visible-project contract to require the first TIMELY-Agent record to use `images/timely-agent.png`, an `image_class` value of `project-image--architecture`, and this exact alt text: `TIMELY-Agent architecture separating knowledge-facing agents from governed patient-facing local computation`.

Require all of the following before implementation:

- `images/timely-agent.png` exists as a file.
- `.project-image--architecture` has exactly `height: 240px`.
- The shared `.project-image` rule still has `object-fit: contain`.
- The loader preserves `project-image` unconditionally and uses an exact allowlist helper: `project.image_class === 'project-image--architecture'` adds the modifier, while every other value adds no class.

- [ ] **Step 2: Run the focused test and verify RED**

Run: `python3 -m unittest tests.test_site_contract.PublicSiteContractTests.test_visible_projects_lead_with_timely_agent_and_hide_method -v`

Expected: FAIL because the project still references the old SVG, the PNG is absent, and the allowlisted modifier/CSS rule do not exist.

### Task 2: Add and render the new preview

**Files:**
- Create: `images/timely-agent.png`
- Modify: `data/projects.json`
- Modify: `index.html`
- Modify: `style.css`

- [ ] **Step 1: Copy the supplied source asset**

Run:

```bash
cp /Users/linglong/Documents/HealTAC/IJCAI__ECAI_26_TIMELY_Agent/timely-agent.png images/timely-agent.png
cmp /Users/linglong/Documents/HealTAC/IJCAI__ECAI_26_TIMELY_Agent/timely-agent.png images/timely-agent.png
```

Expected: `cmp` exits 0, proving the repository copy is byte-for-byte identical.

- [ ] **Step 2: Update the TIMELY-Agent project record**

Point `image` at the PNG, add `image_class: "project-image--architecture"`, and set `image_alt` to `TIMELY-Agent architecture separating knowledge-facing agents from governed patient-facing local computation`. Keep the project copy, ordering, link, and all other records unchanged.

- [ ] **Step 3: Support the optional image modifier**

Add this allowlist helper near the project loader:

```javascript
function projectImageClass(project = {}) {
  return project.image_class === 'project-image--architecture'
    ? ' project-image--architecture'
    : '';
}
```

Render the image with `class="project-image${projectImageClass(project)}"`. This preserves the base class and rejects every unrecognised data value.

- [ ] **Step 4: Add scoped CSS**

Add the exact scoped rule below. Do not change the shared `.project-image` dimensions or other cards.

```css
.project-image--architecture {
  height: 240px;
}
```

- [ ] **Step 5: Verify GREEN**

Run:

```bash
python3 -m unittest tests.test_site_contract.PublicSiteContractTests.test_visible_projects_lead_with_timely_agent_and_hide_method -v
python3 -m unittest discover -s tests -v
node --check script.js
node -e 'const fs=require("fs");const h=fs.readFileSync("index.html","utf8");for(const m of h.matchAll(/<script(?:\s[^>]*)?>([\s\S]*?)<\/script>/gi)){if(m[1].trim())new Function(m[1]);}'
jq empty data/projects.json data/publications.json data/team.json
git diff --check
```

Expected: focused test PASS; all contract tests PASS; shared JavaScript, inline-script compilation, JSON, and format checks exit 0.

### Task 3: Browser QA and commit

**Files:**
- Verify: `index.html`
- Verify: `timely-agent.html`

- [ ] **Step 1: Inspect the homepage**

Start the site with `python3 -m http.server 4177 --bind 127.0.0.1` and open `http://127.0.0.1:4177/`. Inspect at 1280×900 and 390×844. Confirm:

- the TIMELY-Agent PNG request returns 200, `complete` is true, and `naturalWidth` is greater than zero;
- the full diagram remains contained without cropping;
- the TIMELY preview is 240px high while PyPOTS, CSAI, and DEARI remain 180px high;
- card spacing remains balanced at desktop and mobile widths;
- the page has no horizontal overflow or failed project images.

- [ ] **Step 2: Confirm the detail-page boundary**

Confirm `timely-agent.html` still contains no hero image or `.timely-hero-visual` element.

- [ ] **Step 3: Review the scoped diff**

Run `git diff -- data/projects.json index.html style.css tests/test_site_contract.py` and confirm only the TIMELY record, allowlisted loader support, scoped CSS, and contract assertions changed. Run `git diff --quiet -- timely-agent.html images/timely-agent-overview.svg` and confirm it exits 0. Inspect the other four project records and confirm they are byte-for-byte unchanged in the JSON diff.

- [ ] **Step 4: Commit**

```bash
git add images/timely-agent.png data/projects.json index.html style.css tests/test_site_contract.py
git commit -m "style: use TIMELY architecture preview"
```
