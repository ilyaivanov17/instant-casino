#!/usr/bin/env python3
"""Validate rendered HTML metadata against Hugo's generated multilingual sitemap."""
from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse
import sys
import tomllib
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
LANGS = ("de", "en", "pl", "es", "pt", "ja")
SM_NS = "http://www.sitemaps.org/schemas/sitemap/0.9"


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


class HeadParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.in_head = False
        self.in_title = False
        self.title_parts: list[str] = []
        self.canonicals: list[str] = []
        self.descriptions: list[str] = []
        self.robots: list[str] = []
        self.alternates: list[tuple[str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = {key.lower(): (value or "") for key, value in attrs}
        if tag == "head":
            self.in_head = True
        elif self.in_head and tag == "title":
            self.in_title = True
        elif self.in_head and tag == "meta":
            if values.get("name", "").casefold() == "description":
                self.descriptions.append(values.get("content", "").strip())
            elif values.get("name", "").casefold() == "robots":
                self.robots.append(values.get("content", "").strip())
        elif self.in_head and tag == "link":
            rel = set(values.get("rel", "").casefold().split())
            if "canonical" in rel:
                self.canonicals.append(values.get("href", "").strip())
            if "alternate" in rel and values.get("hreflang"):
                self.alternates.append((values["hreflang"].casefold(), values.get("href", "").strip()))

    def handle_endtag(self, tag: str) -> None:
        if tag == "title" and self.in_head:
            self.in_title = False
        elif tag == "head":
            self.in_head = False

    def handle_data(self, data: str) -> None:
        if self.in_head and self.in_title:
            self.title_parts.append(data)

    @property
    def title(self) -> str:
        return " ".join(" ".join(self.title_parts).split())


def sitemap_urls() -> tuple[list[str], dict[str, int]]:
    config = tomllib.loads((ROOT / "hugo.toml").read_text(encoding="utf-8"))
    base = urlparse(config.get("baseURL", ""))
    root_map = PUBLIC / "sitemap.xml"
    if not root_map.is_file():
        fail("public/sitemap.xml is missing; build Hugo first.")
    index = ET.parse(root_map).getroot()
    if index.tag != f"{{{SM_NS}}}sitemapindex":
        fail("public/sitemap.xml is not a sitemap index.")
    children = [
        (node.findtext(f"{{{SM_NS}}}loc") or "").strip()
        for node in index.findall(f"{{{SM_NS}}}sitemap")
    ]
    if len(children) != len(LANGS):
        fail(f"Expected {len(LANGS)} language sitemaps, found {len(children)}.")
    all_urls: list[str] = []
    counts: dict[str, int] = {}
    for lang in LANGS:
        child = next((u for u in children if urlparse(u).path.strip("/").split("/")[-2:] == [lang, "sitemap.xml"]), None)
        if not child:
            fail(f"Missing child sitemap for locale {lang}.")
        path_parts = urlparse(child).path.strip("/").split("/")
        local = PUBLIC.joinpath(*path_parts)
        if not local.is_file():
            fail(f"Child sitemap file is missing: {local.relative_to(ROOT)}")
        sitemap = ET.parse(local).getroot()
        if sitemap.tag != f"{{{SM_NS}}}urlset":
            fail(f"Child sitemap is not a urlset: {child}")
        count = 0
        for node in sitemap.findall(f"{{{SM_NS}}}url"):
            url = (node.findtext(f"{{{SM_NS}}}loc") or "").strip()
            if not url:
                fail(f"Empty URL in {child}")
            parsed = urlparse(url)
            if parsed.scheme != "https" or parsed.netloc.casefold() != base.netloc.casefold():
                fail(f"Off-domain or non-HTTPS sitemap URL: {url}")
            all_urls.append(url)
            count += 1
        counts[lang] = count
    if len(set(all_urls)) != len(all_urls):
        fail("Duplicate canonical URL appears across language sitemaps.")
    return all_urls, counts


def main() -> int:
    urls, counts = sitemap_urls()
    url_set = set(urls)
    errors: list[str] = []
    for url in urls:
        parsed = urlparse(url)
        path = parsed.path.strip("/")
        html_path = PUBLIC / path / "index.html" if path else PUBLIC / "index.html"
        if not html_path.is_file():
            errors.append(f"Sitemap URL has no rendered HTML file: {url}")
            continue
        parser = HeadParser()
        try:
            parser.feed(html_path.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError) as exc:
            errors.append(f"Could not read {html_path.relative_to(ROOT)}: {exc}")
            continue

        label = html_path.relative_to(PUBLIC).as_posix()
        if not parser.title:
            errors.append(f"{label}: missing <title>")
        if len(parser.canonicals) != 1:
            errors.append(f"{label}: expected exactly one canonical link, found {len(parser.canonicals)}")
        elif parser.canonicals[0] != url:
            errors.append(f"{label}: canonical {parser.canonicals[0]!r} does not match sitemap URL {url!r}")
        if len(parser.descriptions) != 1 or not parser.descriptions[0]:
            errors.append(f"{label}: expected one non-empty meta description")
        if len(parser.robots) != 1:
            errors.append(f"{label}: expected exactly one meta robots directive")
        elif "noindex" in parser.robots[0].casefold():
            errors.append(f"{label}: sitemap page unexpectedly carries noindex")
        alternates: dict[str, str] = {}
        for language, target in parser.alternates:
            if language in alternates:
                errors.append(f"{label}: duplicate hreflang={language}")
            alternates[language] = target
        missing = set(LANGS) - set(alternates)
        if missing:
            errors.append(f"{label}: missing hreflang values {sorted(missing)}")
        if alternates.get("x-default") is None:
            errors.append(f"{label}: missing x-default hreflang")
        if url not in [alternates.get(language, "") for language in LANGS]:
            errors.append(f"{label}: no self-referential hreflang entry")
        if alternates.get("x-default") != alternates.get("de"):
            errors.append(f"{label}: x-default must point to the German equivalent")
        for language, target in alternates.items():
            if target not in url_set:
                errors.append(f"{label}: hreflang={language} points outside the sitemap set: {target}")

    if errors:
        print("ERROR: rendered SEO validation failed:", file=sys.stderr)
        print("\n".join(f" - {item}" for item in errors), file=sys.stderr)
        return 1
    print("Rendered SEO checks passed: canonical, title, description, robots, six self-consistent hreflang targets and x-default.")
    print("Sitemap page counts: " + ", ".join(f"{lang}={counts[lang]}" for lang in LANGS))
    print(f"Validated {len(urls)} unique sitemap URLs against rendered HTML.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
