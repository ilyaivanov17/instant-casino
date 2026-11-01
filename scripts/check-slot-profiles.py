#!/usr/bin/env python3
"""Validate the standalone localized slot-profile pages and catalogue links."""
from __future__ import annotations
from pathlib import Path
import re
import yaml

ROOT = Path(__file__).resolve().parents[1]
LANGS = ("de", "en", "pl", "es", "pt", "ja")
PREFIX = {"de": "", "en": "/en", "pl": "/pl", "es": "/es", "pt": "/pt", "ja": "/ja"}

def read_page(path: Path):
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n?(.*)$", text, re.S)
    if not match:
        raise ValueError(f"{path}: missing YAML front matter")
    metadata = yaml.safe_load(match.group(1)) or {}
    return metadata, match.group(2)

def main():
    catalog_path = ROOT / "data" / "slot_catalog.yaml"
    catalog = yaml.safe_load(catalog_path.read_text(encoding="utf-8")) or {}
    games = catalog.get("games", [])
    errors = []
    if len(games) != 35:
        errors.append(f"Expected 35 catalogue entries, found {len(games)}")
    hub_cache = {lang: (ROOT / "content" / lang / "slots.md").read_text(encoding="utf-8") for lang in LANGS}
    for game in games:
        slug = str(game.get("anchor", "")).strip()
        if not slug:
            errors.append(f"Catalogue game has no anchor: {game.get('name')}")
            continue
        for lang in LANGS:
            path = ROOT / "content" / lang / "slot-profiles" / f"{slug}.md"
            if not path.exists():
                errors.append(f"Missing profile {lang}/{slug}")
                continue
            try:
                meta, body = read_page(path)
            except Exception as exc:
                errors.append(str(exc))
                continue
            expected_url = f"{PREFIX[lang]}/slots/{slug}/"
            expected_key = f"slot-profile-{slug}"
            for key in ("title", "description", "seo_title", "type", "translationKey", "url"):
                if not meta.get(key):
                    errors.append(f"{path.relative_to(ROOT)}: missing {key}")
            if meta.get("type") != "slots":
                errors.append(f"{path.relative_to(ROOT)}: expected type=slots")
            if meta.get("url") != expected_url:
                errors.append(f"{path.relative_to(ROOT)}: URL {meta.get('url')} != {expected_url}")
            if meta.get("translationKey") != expected_key:
                errors.append(f"{path.relative_to(ROOT)}: translationKey mismatch")
            if len(str(meta.get("seo_title", ""))) > 75:
                errors.append(f"{path.relative_to(ROOT)}: seo_title exceeds 75 characters")
            if len(str(meta.get("description", ""))) > 180:
                errors.append(f"{path.relative_to(ROOT)}: description exceeds 180 characters")
            lines = [line.strip() for line in body.splitlines()]
            has_table = any(line.startswith("|") for line in lines) and any("-" in line and set(line) <= set("|-: ") for line in lines)
            if not has_table:
                errors.append(f"{path.relative_to(ROOT)}: profile table is missing")
            if 'relref "slots"' not in body:
                errors.append(f"{path.relative_to(ROOT)}: missing return link to catalogue")
            if not re.search(r"https?://", body):
                errors.append(f"{path.relative_to(ROOT)}: no source or outbound reference found")
            hub = hub_cache[lang]
            if f'id="{slug}"' not in hub:
                errors.append(f"content/{lang}/slots.md: missing legacy anchor {slug}")
            if f'relref "slot-profiles/{slug}"' not in hub:
                errors.append(f"content/{lang}/slots.md: missing link to profile {slug}")
    if errors:
        print("ERROR: standalone slot-profile checks failed:")
        print("\n".join(f" - {item}" for item in errors))
        return 1
    print(f"OK: {len(games)} standalone profiles x {len(LANGS)} locales = {len(games) * len(LANGS)} pages.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
