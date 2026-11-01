#!/usr/bin/env python3
"""Validate the standalone localized slot-profile pages and catalogue links."""
from __future__ import annotations
from pathlib import Path
import re
import unicodedata
import yaml

ROOT = Path(__file__).resolve().parents[1]
LANGS = ("de", "en", "pl", "es", "pt", "ja")
PREFIX = {"de": "", "en": "/en", "pl": "/pl", "es": "/es", "pt": "/pt", "ja": "/ja"}

def slug_from_game_name(name: str) -> str:
    """Build a stable URL slug from the original game title."""
    normalized = unicodedata.normalize("NFKD", name)
    normalized = normalized.replace("'", "").replace("’", "")
    ascii_name = normalized.encode("ascii", "ignore").decode("ascii")
    return re.sub(r"[^a-z0-9]+", "-", ascii_name.lower()).strip("-")


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
    # Catalogue summaries are the source for the visible cards and slot-profile SEO metadata.
    # Keep every locale complete, concise and free of the known literal-translation templates.
    forbidden_phrases = {
        "pl": ("slot inspirowany motywem", "z funkcją:"),
        "pt": ("inspirado em o ", "inspirado em a "),
    }
    required_features = {
        "Bonanza": ("Dual Reactions", "117"),
        "Fire in the Hole 3": ("xGod", "Lucky Wagon Spins"),
        "Wanted Dead or a Wild": ("DuelReels", "VS"),
        "Temple Tumble": ("Megaways", "6×6"),
        "Bigger Bass Bonanza": ("Fisherman Wild",),
    }
    author_slugs = {
        "arthur-mustoe", "corey-levitan", "cristina-tudose", "dan-michalski",
        "dominic-field", "jon-pill", "marco-ibarra",
    }
    # Prevent accidental reuse of one card teaser for multiple games in any locale.
    seen_descriptions: dict[str, dict[str, str]] = {lang: {} for lang in LANGS}
    for game in games:
        game_name = str(game.get("name", "")).strip()
        localized = game.get("description", {}) or {}
        author = str(game.get("author", "")).strip()
        if author not in author_slugs:
            errors.append(f"{game_name}: missing or unknown confirmed author {author!r}")
        keywords = game.get("keywords", {}) or {}
        for lang in LANGS:
            localized_keywords = keywords.get(lang, [])
            if not isinstance(localized_keywords, list) or len(localized_keywords) < 5:
                errors.append(f"{game_name}/{lang}: expected at least five localized SEO keywords")
            if len({str(item).casefold() for item in localized_keywords}) != len(localized_keywords):
                errors.append(f"{game_name}/{lang}: duplicate SEO keywords")
            author_page = ROOT / "content" / lang / "authors" / f"{author}.md"
            if author and not author_page.exists():
                errors.append(f"{game_name}/{lang}: missing author profile {author_page.relative_to(ROOT)}")
        for lang in LANGS:
            summary = str(localized.get(lang, "")).strip()
            if not summary:
                errors.append(f"{game_name}: missing {lang} catalogue description")
                continue
            normalized_summary = re.sub(r"\s+", " ", summary).strip().casefold()
            previous_game = seen_descriptions[lang].get(normalized_summary)
            if previous_game:
                errors.append(f"{game_name}/{lang}: card description duplicates {previous_game}")
            else:
                seen_descriptions[lang][normalized_summary] = game_name
            if len(summary) < 45 or len(summary) > 180:
                errors.append(
                    f"{game_name}/{lang}: catalogue description length {len(summary)} is outside 45–180 characters"
                )
            lowered = summary.casefold()
            for phrase in forbidden_phrases.get(lang, ()):
                if phrase.casefold() in lowered:
                    errors.append(f"{game_name}/{lang}: contains a literal-translation template: {phrase!r}")
            for feature in required_features.get(game_name, ()):
                if feature.casefold() not in lowered:
                    errors.append(f"{game_name}/{lang}: missing checked feature term {feature!r}")
    for game in games:
        game_name = str(game.get("name", "")).strip()
        catalog_slug = str(game.get("anchor", "")).strip()
        slug = slug_from_game_name(game_name)
        if not game_name or not slug:
            errors.append(f"Catalogue game has no usable name: {game!r}")
            continue
        if catalog_slug != slug:
            errors.append(
                f"Game URL slug must be generated from its name: "
                f"{game_name!r} -> {slug!r}, but catalogue anchor is {catalog_slug!r}"
            )
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
            hub = hub_cache[lang]
            if f'id="{slug}"' not in hub:
                errors.append(f"content/{lang}/slots.md: missing legacy anchor {slug}")
            if f'relref "slot-profiles/{slug}"' not in hub:
                errors.append(f"content/{lang}/slots.md: missing link to profile {slug}")
    expert_partial = ROOT / "layouts" / "partials" / "slot-profile-expert-analysis.html"
    if not expert_partial.exists():
        errors.append("Missing localized expert-analysis partial")
    else:
        expert_text = expert_partial.read_text(encoding="utf-8")
        for lang in LANGS[:-1]:
            if f'eq $lang "{lang}"' not in expert_text:
                errors.append(f"Expert-analysis partial has no {lang} branch")
        if "{{ else }}" not in expert_text:
            errors.append("Expert-analysis partial has no Japanese fallback branch")
        if "data-slot-expert-analysis" not in expert_text:
            errors.append("Expert-analysis partial is missing its testable section marker")
    single_layout = (ROOT / "layouts" / "_default" / "single.html").read_text(encoding="utf-8")
    head_layout = (ROOT / "layouts" / "partials" / "head.html").read_text(encoding="utf-8")
    card_layout = (ROOT / "layouts" / "partials" / "slot-catalog.html").read_text(encoding="utf-8")
    if "slot-profile-expert-analysis.html" not in single_layout:
        errors.append("Single page layout does not render expert slot analyses")
    if 'name="keywords"' not in head_layout:
        errors.append("Head partial does not render localized SEO keywords")
    if "slot-game-card-author" not in card_layout:
        errors.append("Slot cards do not display author bylines")
    if errors:
        print("ERROR: standalone slot-profile checks failed:")
        print("\n".join(f" - {item}" for item in errors))
        return 1
    print(f"OK: {len(games)} standalone profiles x {len(LANGS)} locales = {len(games) * len(LANGS)} pages.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
