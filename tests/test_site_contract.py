import json
import re
import unittest
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
BANNED_PUBLIC_TERMS = (
    "METHOD",
    "FastOMOP",
    "OMCP",
    "CRES",
    "12,000",
    "9,587",
    "53,070",
    "0.655",
    "0.535",
)


class VisibleTextParser(HTMLParser):
    EXCLUDED_ELEMENTS = {"script", "style", "template"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self._excluded_depth = 0
        self.text = []

    def handle_starttag(self, tag, attrs):
        if tag.lower() in self.EXCLUDED_ELEMENTS:
            self._excluded_depth += 1

    def handle_startendtag(self, tag, attrs):
        pass

    def handle_endtag(self, tag):
        if tag.lower() in self.EXCLUDED_ELEMENTS and self._excluded_depth:
            self._excluded_depth -= 1

    def handle_data(self, data):
        if not self._excluded_depth:
            self.text.append(data)


class AssetParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.assets = []

    def handle_starttag(self, tag, attrs):
        for name, value in attrs:
            if name.lower() in {"href", "src"} and value:
                self.assets.append(value)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)


class HTMLContractParser(HTMLParser):
    HEADING_TAGS = {f"h{level}" for level in range(1, 7)}
    HIDDEN_ELEMENTS = {"script", "style", "template"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.attributes = []
        self.ids = set()
        self.section_ids = set()
        self.headings = []
        self.links = []
        self.anchors = []
        self.meta_refresh = []
        self.canonical = []
        self.titles = []
        self.scripts = []
        self._hidden_elements = []
        self._heading_tag = None
        self._heading_text = []
        self._anchor_href = None
        self._anchor_text = []
        self._title_text = None
        self._collecting_script = False
        self._script_text = []

    def handle_starttag(self, tag, attrs):
        tag = tag.lower()
        attributes = {
            name.lower(): value for name, value in attrs if value is not None
        }

        active_markup = not self._hidden_elements
        if tag in self.HIDDEN_ELEMENTS:
            if tag == "script" and active_markup:
                self._collecting_script = True
                self._script_text = []
            self._hidden_elements.append(tag)
            return
        if not active_markup:
            return

        self.attributes.append((tag, attributes))

        if "id" in attributes:
            self.ids.add(attributes["id"])
            if tag == "section":
                self.section_ids.add(attributes["id"])
        if tag == "a" and "href" in attributes:
            self.links.append(attributes["href"])
            self._anchor_href = attributes["href"]
            self._anchor_text = []
        if (
            tag == "meta"
            and attributes.get("http-equiv", "").casefold() == "refresh"
            and "content" in attributes
        ):
            self.meta_refresh.append(attributes["content"])
        if tag == "link" and "canonical" in attributes.get("rel", "").casefold().split():
            if "href" in attributes:
                self.canonical.append(attributes["href"])
        if tag == "title":
            self._title_text = []
        if tag in self.HEADING_TAGS and self._heading_tag is None:
            self._heading_tag = tag
            self._heading_text = []

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        self.handle_endtag(tag)

    def handle_endtag(self, tag):
        tag = tag.lower()
        if tag in self.HIDDEN_ELEMENTS:
            if tag == "script" and self._collecting_script:
                self.scripts.append("".join(self._script_text))
                self._script_text = []
                self._collecting_script = False
            if self._hidden_elements and self._hidden_elements[-1] == tag:
                self._hidden_elements.pop()
            return
        if self._hidden_elements:
            return

        if tag == self._heading_tag:
            self.headings.append(" ".join(" ".join(self._heading_text).split()))
            self._heading_tag = None
            self._heading_text = []
        if tag == "a" and self._anchor_href is not None:
            text = " ".join(" ".join(self._anchor_text).split())
            self.anchors.append((self._anchor_href, text))
            self._anchor_href = None
            self._anchor_text = []
        if tag == "title" and self._title_text is not None:
            self.titles.append(" ".join(" ".join(self._title_text).split()))
            self._title_text = None

    def handle_data(self, data):
        if self._collecting_script:
            self._script_text.append(data)
            return
        if self._hidden_elements:
            return
        if self._heading_tag is not None:
            self._heading_text.append(data)
        if self._anchor_href is not None:
            self._anchor_text.append(data)
        if self._title_text is not None:
            self._title_text.append(data)


def read(relative_path):
    return (ROOT / relative_path).read_text(encoding="utf-8")


def read_json(relative_path):
    return json.loads(read(relative_path))


def visible_text(html):
    parser = VisibleTextParser()
    parser.feed(html)
    parser.close()
    return " ".join(" ".join(parser.text).split())


def parse_html(html):
    parser = HTMLContractParser()
    parser.feed(html)
    parser.close()
    return parser


def contains_banned_term(text, term):
    text = str(text)
    if term.isalpha():
        pattern = rf"(?<!\w){re.escape(term)}(?!\w)"
        return re.search(pattern, text, flags=re.IGNORECASE) is not None
    return term.casefold() in text.casefold()


def json_strings(value):
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for child in value.values():
            yield from json_strings(child)
    elif isinstance(value, list):
        for child in value:
            yield from json_strings(child)


def refresh_destination(content):
    match = re.fullmatch(
        r"\s*0\s*;\s*url\s*=\s*(?P<destination>.*?)\s*",
        content,
        flags=re.IGNORECASE,
    )
    return match.group("destination") if match else None


def strip_comments(source, line_comments):
    result = []
    index = 0
    quote = None

    while index < len(source):
        character = source[index]
        following = source[index + 1] if index + 1 < len(source) else ""

        if quote is not None:
            result.append(character)
            if character == "\\" and following:
                result.append(following)
                index += 2
                continue
            if character == quote:
                quote = None
            index += 1
            continue

        if character in {'"', "'", "`"}:
            quote = character
            result.append(character)
            index += 1
            continue
        if character == "/" and following == "*":
            index += 2
            while index < len(source) - 1 and source[index : index + 2] != "*/":
                if source[index] in "\r\n":
                    result.append(source[index])
                index += 1
            index = min(index + 2, len(source))
            continue
        if line_comments and character == "/" and following == "/":
            index += 2
            while index < len(source) and source[index] not in "\r\n":
                index += 1
            continue

        result.append(character)
        index += 1

    return "".join(result)


def javascript_without_comments(source):
    return strip_comments(source, line_comments=True)


def css_rule_openings(source):
    source = strip_comments(source, line_comments=False)
    openings = []
    segment_start = 0
    quote = None
    index = 0

    while index < len(source):
        character = source[index]
        following = source[index + 1] if index + 1 < len(source) else ""
        if quote is not None:
            if character == "\\" and following:
                index += 2
                continue
            if character == quote:
                quote = None
            index += 1
            continue
        if character in {'"', "'"}:
            quote = character
        elif character == "{":
            opening = source[segment_start:index].strip()
            if opening:
                openings.append(opening)
            segment_start = index + 1
        elif character in "};":
            segment_start = index + 1
        index += 1

    return openings


class PublicSiteContractTests(unittest.TestCase):
    def assert_file_exists(self, relative_path):
        path = ROOT / relative_path
        self.assertTrue(path.is_file(), f"Required public file is missing: {relative_path}")

    def assert_no_banned_terms(self, text, source):
        for term in BANNED_PUBLIC_TERMS:
            with self.subTest(source=source, banned_term=term):
                self.assertFalse(
                    contains_banned_term(text, term),
                    f"Public copy in {source} contains banned term {term!r}",
                )

    def test_visible_projects_lead_with_timely_agent_and_hide_method(self):
        projects = read_json("data/projects.json")
        visible_projects = [
            project for project in projects if not project.get("hidden", False)
        ]
        timely_projects = [
            project for project in projects if project.get("title") == "TIMELY-Agent"
        ]

        self.assertEqual(len(timely_projects), 1, "Define exactly one TIMELY-Agent record")
        self.assertTrue(visible_projects, "At least one project must be publicly visible")
        self.assertEqual(visible_projects[0].get("title"), "TIMELY-Agent")
        self.assertEqual(visible_projects[0].get("link"), "timely-agent.html")

        method_projects = [project for project in projects if project.get("title") == "METHOD"]
        self.assertEqual(len(method_projects), 1, "Retain exactly one historical METHOD record")
        self.assertIs(method_projects[0].get("hidden"), True)

    def test_public_copy_contains_no_banned_terms(self):
        self.assert_no_banned_terms(
            "methodological methodologies",
            "token-boundary regression probe",
        )
        public_pages = (
            "index.html",
            "timely-agent.html",
            "method.html",
            "docs.html",
            "people/zina.html",
        )
        for page in public_pages:
            self.assert_file_exists(page)

        projects = read_json("data/projects.json")
        team = read_json("data/team.json")
        copy_parts = [visible_text(read(page)) for page in public_pages]
        copy_parts.extend(json_strings(team))
        for project in projects:
            if not project.get("hidden", False):
                copy_parts.extend(json_strings(project))

        self.assert_no_banned_terms(" ".join(copy_parts), "public site copy")

    def test_timely_page_has_required_sections_and_resource_note(self):
        self.assert_file_exists("timely-agent.html")
        html = read("timely-agent.html")
        parser = parse_html(html)

        for section_id in ("overview", "framework", "privacy", "foundations", "contact"):
            with self.subTest(section_id=section_id):
                self.assertIn(
                    section_id,
                    parser.section_ids,
                    f"timely-agent.html must contain id={section_id!r}",
                )

        page_text = visible_text(html)
        for heading in parser.headings:
            with self.subTest(heading=heading):
                self.assertIsNone(
                    re.search(r"\b(?:status|roadmap)\b", heading, flags=re.IGNORECASE),
                    "timely-agent.html must not publish a Status or Roadmap heading",
                )
        resource_note = (
            "Publications and project resources will be linked here when available."
        )
        self.assertTrue(
            resource_note in page_text,
            "timely-agent.html must contain the exact approved resource note",
        )

        navigation_groups = [
            attributes
            for tag, attributes in parser.attributes
            if tag == "div"
            and "nav-right-group" in attributes.get("class", "").split()
        ]
        self.assertEqual(len(navigation_groups), 1)
        with self.subTest(accessibility_hook="navigation id"):
            self.assertEqual(navigation_groups[0].get("id"), "primary-navigation")

        mobile_toggles = [
            attributes
            for tag, attributes in parser.attributes
            if tag == "button" and attributes.get("id") == "mobile-menu-toggle"
        ]
        self.assertEqual(len(mobile_toggles), 1)
        with self.subTest(accessibility_hook="toggle aria-controls"):
            self.assertEqual(
                mobile_toggles[0].get("aria-controls"), "primary-navigation"
            )

        privacy_boundaries = [
            attributes
            for tag, attributes in parser.attributes
            if tag == "div"
            and "privacy-boundary" in attributes.get("class", "").split()
        ]
        self.assertEqual(len(privacy_boundaries), 1)
        with self.subTest(accessibility_hook="privacy group role"):
            self.assertEqual(privacy_boundaries[0].get("role"), "group")
        with self.subTest(accessibility_hook="privacy group label"):
            self.assertTrue(privacy_boundaries[0].get("aria-label", "").strip())

    def test_timely_svg_is_sanitized_and_uses_approved_labels(self):
        svg_path = "images/timely-agent-overview.svg"
        self.assert_file_exists(svg_path)
        try:
            root = ET.parse(ROOT / svg_path).getroot()
        except ET.ParseError as error:
            self.fail(f"{svg_path} must be valid XML: {error}")

        root_name = root.tag.rsplit("}", 1)[-1].casefold()
        self.assertEqual(root_name, "svg", f"{svg_path} must have an SVG root element")
        rendered_text = " ".join(
            " ".join(" ".join(element.itertext()).split())
            for element in root.iter()
            if element.tag.rsplit("}", 1)[-1].casefold() == "text"
        )
        actual_text = " ".join(root.itertext())
        attribute_text = " ".join(
            attribute
            for element in root.iter()
            for attribute in element.attrib.values()
        )

        for label in (
            "Clinical knowledge",
            "Governed retrieval",
            "Reasoning episodes",
            "Tasks and audit",
        ):
            with self.subTest(label=label):
                self.assertTrue(
                    label in rendered_text,
                    f"{svg_path} rendered text must contain label {label!r}",
                )
        self.assert_no_banned_terms(f"{actual_text} {attribute_text}", svg_path)

    def test_legacy_pages_are_exact_redirects(self):
        redirects = {
            "method.html": "timely-agent.html",
            "docs.html": "index.html",
            "people/zina.html": "../index.html",
        }

        for source, destination in redirects.items():
            with self.subTest(source=source, destination=destination):
                html = read(source)
                parser = parse_html(html)
                self.assertEqual(
                    len(parser.meta_refresh),
                    1,
                    f"{source} must contain exactly one active meta refresh",
                )
                self.assertEqual(
                    refresh_destination(parser.meta_refresh[0]),
                    destination,
                    f"{source} meta refresh must point exactly to {destination}",
                )
                self.assertEqual(
                    len(parser.canonical),
                    1,
                    f"{source} must contain exactly one active canonical link",
                )
                self.assertEqual(
                    parser.canonical[0],
                    destination,
                    f"{source} canonical link must point exactly to {destination}",
                )
                self.assertEqual(
                    parser.titles,
                    ["Project moved | MAI Research Group"],
                    f"{source} must use the exact legacy redirect title",
                )
                self.assertTrue(
                    any(href == destination and text for href, text in parser.anchors),
                    f"{source} must contain a fallback link to {destination}",
                )

    def test_index_filters_hidden_projects_and_has_fallback_copy(self):
        inactive_markup = parse_html(
            "<!-- <h2 id='overview'>Status</h2>"
            "<meta http-equiv='refresh' content='0;url=bad'>"
            "<link rel='canonical' href='bad'><a href='bad'>Bad</a> -->"
            "<template><section id='projects'><h2>Status</h2>"
            "<meta http-equiv='refresh' content='0;url=bad'>"
            "<link rel='canonical' href='bad'><a href='bad'>Bad</a>"
            "</section></template>"
        )
        self.assertEqual(inactive_markup.ids, set())
        self.assertEqual(inactive_markup.section_ids, set())
        self.assertEqual(inactive_markup.headings, [])
        self.assertEqual(inactive_markup.meta_refresh, [])
        self.assertEqual(inactive_markup.canonical, [])
        self.assertEqual(inactive_markup.links, [])
        self.assertEqual(inactive_markup.anchors, [])

        stripped_probe = javascript_without_comments(
            "render();// .filter(project => !project.hidden)\ncontinueRender();"
        )
        self.assertNotIn(".filter(project => !project.hidden)", stripped_probe)

        html = read("index.html")
        parser = parse_html(html)
        scripts = " ".join(javascript_without_comments(script) for script in parser.scripts)
        project_scripts = [
            script for script in parser.scripts if "function loadProjects" in script
        ]
        self.assertEqual(len(project_scripts), 1)
        project_script = project_scripts[0]

        navigation_groups = [
            attributes
            for tag, attributes in parser.attributes
            if tag == "div"
            and "nav-right-group" in attributes.get("class", "").split()
        ]
        self.assertEqual(len(navigation_groups), 1)
        with self.subTest(accessibility_hook="navigation id"):
            self.assertEqual(navigation_groups[0].get("id"), "primary-navigation")

        mobile_toggles = [
            attributes
            for tag, attributes in parser.attributes
            if tag == "button" and attributes.get("id") == "mobile-menu-toggle"
        ]
        self.assertEqual(len(mobile_toggles), 1)
        with self.subTest(accessibility_hook="toggle aria-controls"):
            self.assertEqual(
                mobile_toggles[0].get("aria-controls"), "primary-navigation"
            )

        institution_links = {
            attributes.get("href"): attributes
            for tag, attributes in parser.attributes
            if tag == "a"
            and attributes.get("href")
            in {
                "https://www.kcl.ac.uk/bhi",
                "https://www.kcl.ac.uk/",
                "https://phidatalab.org/about-us/",
            }
        }
        for institution_url in (
            "https://www.kcl.ac.uk/bhi",
            "https://www.kcl.ac.uk/",
            "https://phidatalab.org/about-us/",
        ):
            with self.subTest(institution_url=institution_url):
                self.assertIn(institution_url, institution_links)
                self.assertEqual(institution_links[institution_url].get("target"), "_blank")
                self.assertEqual(
                    institution_links[institution_url].get("rel"),
                    "noopener noreferrer",
                )

        filter_pattern = (
            r"\.filter\s*\(\s*\(?\s*project\s*\)?\s*=>"
            r"\s*!\s*project\.hidden\s*\)"
        )
        with self.subTest(project_contract="hidden filter"):
            self.assertIsNotNone(
                re.search(filter_pattern, scripts, flags=re.DOTALL),
                "index.html must actively filter hidden projects",
            )
        with self.subTest(project_contract="HTTP status check"):
            self.assertRegex(project_script, r"if\s*\(\s*!\s*response\.ok\s*\)")
        with self.subTest(project_contract="external link helper"):
            self.assertIn(
                "function externalLinkAttributes(url = '') { return "
                "/^https?:\\/\\//i.test(url) ? "
                "' target=\"_blank\" rel=\"noopener noreferrer\"' : ''; }",
                project_script,
            )
            self.assertIn(
                "${externalLinkAttributes(project.title_link)}", project_script
            )
            self.assertIn("${externalLinkAttributes(project.link)}", project_script)
        fallback_markup = (
            '<p class="load-error" role="status">Unable to load projects right now. '
            "Please try again later.</p>"
        )
        with self.subTest(project_contract="exact fallback markup"):
            self.assertIn(fallback_markup, project_script)
            self.assertRegex(project_script, r"catch\s*\([^)]*\)\s*\{")
            self.assertRegex(project_script, r"console\.error\s*\(")
            self.assertLess(
                project_script.index("document.getElementById('projects-list')"),
                project_script.index("try"),
                "Obtain the project container before entering the fetch/render try block",
            )
        self.assertIn(
            "https://www.kcl.ac.uk/",
            parser.links,
            "The King's College London URL must be an actual href, not commented copy",
        )

    def test_internal_assets_exist(self):
        for page in ("index.html", "timely-agent.html"):
            with self.subTest(page=page):
                self.assert_file_exists(page)
                parser = AssetParser()
                parser.feed(read(page))
                parser.close()

                for asset in parser.assets:
                    parsed = urlsplit(asset)
                    if asset.startswith("#") or parsed.scheme or parsed.netloc or not parsed.path:
                        continue
                    decoded_path = unquote(parsed.path)
                    asset_path = (
                        ROOT / decoded_path.lstrip("/")
                        if decoded_path.startswith("/")
                        else ROOT / Path(page).parent / decoded_path
                    ).resolve()
                    with self.subTest(page=page, asset=asset):
                        try:
                            asset_path.relative_to(ROOT.resolve())
                        except ValueError:
                            self.fail(
                                f"Internal asset referenced by {page} escapes ROOT: {asset}"
                            )
                        self.assertTrue(
                            asset_path.is_file(),
                            f"Internal asset referenced by {page} is missing: {asset}",
                        )

    def test_css_includes_timely_and_mobile_navigation_rules(self):
        decoy_openings = css_rule_openings(
            '/* @media (max-width: 768px) { .timely-workflow-grid {} } */'
            '.decoy { content: "body.mobile-nav-open .nav-right-group { }"; }'
        )
        self.assertFalse(
            any("timely-workflow-grid" in opening for opening in decoy_openings)
        )
        self.assertFalse(
            any("mobile-nav-open" in opening for opening in decoy_openings)
        )

        css = strip_comments(read("style.css"), line_comments=False)
        openings = css_rule_openings(css)
        required_patterns = (
            r"^@media\b[^{}]*\(\s*max-width\s*:\s*768px\s*\)$",
            r"(?:^|,)\s*\.timely-workflow-grid\b",
            r"(?:^|,)\s*body\.mobile-nav-open\s+\.nav-right-group\b",
        )
        for pattern in required_patterns:
            with self.subTest(pattern=pattern):
                self.assertTrue(
                    any(re.search(pattern, opening) for opening in openings),
                    f"style.css must contain rule opening matching {pattern!r}",
                )

        contact_button_rule = re.search(
            r"\.timely-contact\s+\.project-link\s*\{(?P<body>[^{}]*)\}",
            css,
            flags=re.DOTALL,
        )
        with self.subTest(css_rule="TIMELY contact button"):
            self.assertIsNotNone(
                contact_button_rule,
                "TIMELY contact button must have an uncommented scoped CSS rule",
            )
        if contact_button_rule is not None:
            contact_button_body = contact_button_rule.group("body")
            self.assertRegex(
                contact_button_body,
                r"background-color\s*:\s*var\(\s*--primary-color\s*\)",
            )
            self.assertRegex(
                contact_button_body,
                r"color\s*:\s*var\(\s*--hero-text\s*\)",
            )

        script = javascript_without_comments(read("script.js"))
        behavior_patterns = (
            r"firstNavLink\.focus\s*\(\s*\)",
            r"addEventListener\s*\(\s*['\"]keydown['\"]",
            r"\.key\s*===\s*['\"]Escape['\"]",
            r"mobileMenuToggle\.focus\s*\(\s*\)",
            r"function\s+handleViewportResize\s*\(",
            r"addEventListener\s*\(\s*['\"]resize['\"]\s*,\s*handleViewportResize",
            r"handleViewportResize[\s\S]*?innerWidth\s*>\s*768[\s\S]*?setMobileMenuState\s*\(\s*false\s*\)",
        )
        for pattern in behavior_patterns:
            with self.subTest(script_pattern=pattern):
                self.assertIsNotNone(
                    re.search(pattern, script),
                    f"script.js must contain active behavior matching {pattern!r}",
                )


if __name__ == "__main__":
    unittest.main()
