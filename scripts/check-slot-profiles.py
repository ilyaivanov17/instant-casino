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
        "Fruit Party": ("7×7", "256"),
        "Dead or Alive 2": ("Old Saloon", "High Noon Saloon", "Train Heist"),
        "Legacy of Dead": ("Tomb", "Wild", "Scatter"),
        "Wolf Gold": ("Money Respin", "Scatter"),
        "Money Train 4": ("Money Cart", "Arms Dealer", "Unlocker", "Upgrader"),
    }
    author_slugs = {
        "arthur-mustoe", "corey-levitan", "cristina-tudose", "dan-michalski",
        "dominic-field", "jon-pill", "marco-ibarra",
    }
    # Expert card copy is separate from the short mechanic labels and must exist in every locale.
    expert_insight_terms = {
        "5 Lions Megaways": {
            "de": ("117.649", "sieben"),
            "en": ("117,649", "seven"),
            "pl": ("117 649", "siedem"),
            "es": ("117.649", "siete"),
            "pt": ("117 649", "sete"),
            "ja": ("117,649", "7種類"),
        },
        "Le Bandit": {
            "de": ("Golden Squares", "Rainbow", "fünf FS"),
            "en": ("Golden Squares", "Rainbow", "five-FS"),
            "pl": ("Golden Squares", "Rainbow", "5 symbolami FS"),
            "es": ("Golden Squares", "Rainbow", "5 símbolos FS"),
            "pt": ("Golden Squares", "Rainbow", "5 símbolos FS"),
            "ja": ("Golden Squares", "Rainbow", "FSが5個"),
        },
    }
    # Prevent accidental reuse of one card teaser for multiple games in any locale.
    seen_descriptions: dict[str, dict[str, str]] = {lang: {} for lang in LANGS}
    for game in games:
        game_name = str(game.get("name", "")).strip()
        localized = game.get("description", {}) or {}
        expert_insight = game.get("expert_insight", {}) or {}
        author = str(game.get("author", "")).strip()
        if game_name in expert_insight_terms:
            localized_labels = game.get("label", {}) or {}
            for lang in LANGS:
                insight = str(expert_insight.get(lang, "")).strip()
                label = str(localized_labels.get(lang, "")).strip()
                if len(insight) < 70 or len(insight) > 260:
                    errors.append(f"{game_name}/{lang}: expert insight length must be 70–260 characters")
                if not insight:
                    errors.append(f"{game_name}/{lang}: missing expert insight")
                if insight.casefold() == label.casefold():
                    errors.append(f"{game_name}/{lang}: expert insight duplicates the feature label")
                for term in expert_insight_terms[game_name][lang]:
                    if term.casefold() not in insight.casefold():
                        errors.append(f"{game_name}/{lang}: expert insight is missing {term!r}")
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
            if slug == "buffalo-king-megaways":
                required_sources = (
                    "https://www.pragmaticplay.com/en/games/buffalo-king-megaways/",
                    "https://www.pragmaticplay.com/en/news/pragmatic-play-revamps-a-classic-in-buffalo-king-megaways/",
                    "https://thescorebethelp.zendesk.com/hc/en-us/articles/13873576906509-Buffalo-King-Megaways",
                )
                for source_url in required_sources:
                    if source_url not in body:
                        errors.append(f"{path.relative_to(ROOT)}: missing Buffalo King Megaways rules source {source_url}")
                minimum_length = 4200 if lang == "ja" else 6000
                if len(body) < minimum_length:
                    errors.append(f"{path.relative_to(ROOT)}: Buffalo King Megaways profile is too short ({len(body)} < {minimum_length})")
                localized_mechanics = {
                    "de": ("5×", "20×", "100×", "multipliziert"),
                    "en": ("5x", "20x", "100x", "multiplied together"),
                    "pl": ("5×", "20×", "100×", "mnożone"),
                    "es": ("5x", "20x", "100x", "multiplican"),
                    "pt": ("5x", "20x", "100x", "multiplicados"),
                    "ja": ("12回", "17回", "22回", "5倍", "20倍", "100倍", "乗算"),
                }
                for term in localized_mechanics[lang]:
                    if term not in body:
                        errors.append(f"{path.relative_to(ROOT)}: missing localized Buffalo King Megaways mechanic {term!r}")
                if meta.get("article_review_status") != "editorial-review-pending":
                    errors.append(f"{path.relative_to(ROOT)}: keep the profile pending until editorial sign-off")
            if slug == "starburst":
                required_sources = (
                    "https://netent.com/games/starburst",
                    "https://games.evolution.com/slots/starburst/",
                )
                for source_url in required_sources:
                    if source_url not in body:
                        errors.append(f"{path.relative_to(ROOT)}: missing primary source link {source_url}")
                if len(body) < 2400:
                    errors.append(f"{path.relative_to(ROOT)}: Starburst profile is missing its detailed localized sections")
                if meta.get("article_review_status") != "editorial-review-pending":
                    errors.append(f"{path.relative_to(ROOT)}: keep the profile pending until editorial sign-off")
            if slug == "book-of-dead":
                required_sources = (
                    "https://www.playngo.com/post/book-of-dead-walkthrough",
                    "https://www.playngo.com/post/a-complete-guide-on-how-to-play-book-of-dead",
                )
                for source_url in required_sources:
                    if source_url not in body:
                        errors.append(f"{path.relative_to(ROOT)}: missing primary source link {source_url}")
                if len(body) < 2400:
                    errors.append(f"{path.relative_to(ROOT)}: Book of Dead profile is missing its localized mechanics sections")
                for unsupported_value in ("96.21", "0.1–50 EUR"):
                    if unsupported_value in body:
                        errors.append(f"{path.relative_to(ROOT)}: unsupported/unverified Book of Dead value remains: {unsupported_value}")
                if meta.get("article_review_status") != "editorial-review-pending":
                    errors.append(f"{path.relative_to(ROOT)}: keep the profile pending until editorial sign-off")
            if slug == "bigger-bass-bonanza":
                required_sources = (
                    "https://www.pragmaticplay.com/en/games/bigger-bass-bonanza/",
                    "https://www.pragmaticplay.com/de/spiele/bigger-bass-bonanza/",
                )
                for source_url in required_sources:
                    if source_url not in body:
                        errors.append(f"{path.relative_to(ROOT)}: missing primary source link {source_url}")
                if len(body) < 2400:
                    errors.append(f"{path.relative_to(ROOT)}: Bigger Bass Bonanza profile is missing its localized mechanics sections")
                for unsupported_value in ("96.71", "0.2–125 EUR"):
                    if unsupported_value in body:
                        errors.append(f"{path.relative_to(ROOT)}: unsupported/unverified Bigger Bass Bonanza value remains: {unsupported_value}")
                if meta.get("article_review_status") != "editorial-review-pending":
                    errors.append(f"{path.relative_to(ROOT)}: keep the profile pending until editorial sign-off")
            if slug == "bonanza":
                source_url = "https://beta.bigtimegaming.com/games/bonanza"
                if source_url not in body:
                    errors.append(f"{path.relative_to(ROOT)}: missing official Big Time Gaming source link")
                if len(body) < 2400:
                    errors.append(f"{path.relative_to(ROOT)}: Bonanza profile is missing its localized mechanics sections")
                for unsupported_value in ("96.1 %", "0.1–50 EUR", "| Medium |"):
                    if unsupported_value in body:
                        errors.append(f"{path.relative_to(ROOT)}: stale Bonanza profile value remains: {unsupported_value}")
                if meta.get("article_review_status") != "editorial-review-pending":
                    errors.append(f"{path.relative_to(ROOT)}: keep the profile pending until editorial sign-off")
            if slug == "sweet-bonanza":
                required_sources = (
                    "https://www.pragmaticplay.com/en/games/sweet-bonanza-slot/",
                    "https://www.pragmaticplay.com/en/news/pragmatic-play-launches-sweet-bonanza/",
                )
                for source_url in required_sources:
                    if source_url not in body:
                        errors.append(f"{path.relative_to(ROOT)}: missing primary source link {source_url}")
                if len(body) < 2400:
                    errors.append(f"{path.relative_to(ROOT)}: Sweet Bonanza profile is missing its localized mechanics sections")
                if "zufällige" in body:
                    errors.append(f"{path.relative_to(ROOT)}: untranslated German template fragment remains")
                if meta.get("article_review_status") != "editorial-review-pending":
                    errors.append(f"{path.relative_to(ROOT)}: keep the profile pending until editorial sign-off")
            if slug == "fruit-party":
                required_sources = (
                    "https://www.pragmaticplay.com/en/games/fruit-party-slot/",
                    "https://www.pragmaticplay.com/en/news/pragmatic-play-gets-summer-started-with-fruit-party/",
                )
                for source_url in required_sources:
                    if source_url not in body:
                        errors.append(f"{path.relative_to(ROOT)}: missing primary source link {source_url}")
                if len(body) < 2400:
                    errors.append(f"{path.relative_to(ROOT)}: Fruit Party profile is missing its localized mechanics sections")
                for unsupported_value in ("96.47", "0.2–100 EUR"):
                    if unsupported_value in body:
                        errors.append(f"{path.relative_to(ROOT)}: unsupported/unverified Fruit Party value remains: {unsupported_value}")
                if meta.get("article_review_status") != "editorial-review-pending":
                    errors.append(f"{path.relative_to(ROOT)}: keep the profile pending until editorial sign-off")
            if slug == "the-dog-house":
                required_sources = (
                    "https://www.pragmaticplay.com/en/games/the-dog-house-slot/",
                    "https://www.pragmaticplay.com/en/news/pragmatic-play-launches-the-dog-house/",
                )
                for source_url in required_sources:
                    if source_url not in body:
                        errors.append(f"{path.relative_to(ROOT)}: missing primary source link {source_url}")
                if len(body) < 2400:
                    errors.append(f"{path.relative_to(ROOT)}: The Dog House profile is missing its localized mechanics sections")
                for other_edition in ("The Dog House Megaways", "The Dog House Multihold", "The Dog House Muttley Crew", "The Dog House – Dog or Alive"):
                    if other_edition not in body:
                        errors.append(f"{path.relative_to(ROOT)}: missing distinction from related edition {other_edition}")
                if meta.get("article_review_status") != "editorial-review-pending":
                    errors.append(f"{path.relative_to(ROOT)}: keep the profile pending until editorial sign-off")
            if slug == "fire-in-the-hole-3":
                required_sources = (
                    "https://nolimitcity.com/games/fire-in-the-hole-3",
                    "https://nolimitcity.com/posts/fire-in-the-hole-3-now-live",
                )
                for source_url in required_sources:
                    if source_url not in body:
                        errors.append(f"{path.relative_to(ROOT)}: missing official Nolimit City source link {source_url}")
                if len(body) < 2400:
                    errors.append(f"{path.relative_to(ROOT)}: Fire in the Hole 3 profile is missing detailed localized mechanics sections")
                for mechanic in ("Collapsing Mine", "xBomb", "Wild Mining", "xSplit", "xHole", "Lucky Wagon Spins", "xGod"):
                    if mechanic not in body:
                        errors.append(f"{path.relative_to(ROOT)}: missing checked Fire in the Hole 3 mechanic {mechanic!r}")
                if meta.get("article_review_status") != "editorial-review-pending":
                    errors.append(f"{path.relative_to(ROOT)}: keep the profile pending until editorial sign-off")
            if slug == "dead-or-alive-2":
                required_sources = (
                    "https://cdn-sp.kertn.net/assets/cms/App_Data/20e8c524-e223-48de-9382-7401c87cd065/PDFs/GameRules/Netent/GamerulesEN/Dead_or_Alive_2_deadoralive2_not_mobile_Game_Sheet_default_en.pdf",
                    "https://news.cision.com/netent/r/netent-heads-back-to-the-wild-west-with-dead-or-alive-2---the-sequel-to-one-its-most-iconic-games,c2795155",
                    "https://games.evolution.com/slots/dead-or-alive-2/",
                )
                for source_url in required_sources:
                    if source_url not in body:
                        errors.append(f"{path.relative_to(ROOT)}: missing Dead or Alive 2 primary source {source_url}")
                minimum_lengths = {"de": 6800, "en": 6800, "pl": 6800, "es": 6800, "pt": 6800, "ja": 4700}
                minimum_length = minimum_lengths[lang]
                if len(body) < minimum_length:
                    errors.append(f"{path.relative_to(ROOT)}: Dead or Alive 2 profile is too short ({len(body)} < {minimum_length})")
                for feature in ("Old Saloon", "High Noon Saloon", "Train Heist"):
                    if feature not in body:
                        errors.append(f"{path.relative_to(ROOT)}: missing Free Spins mode {feature}")
                localized_values = {
                    "de": ("96,80", "100.000", "2.500"),
                    "en": ("96.80", "100,000", "2,500"),
                    "pl": ("96,80", "100 000", "2500"),
                    "es": ("96,80", "100.000", "2.500"),
                    "pt": ("96,80", "100.000", "2.500"),
                    "ja": ("96.80", "100,000", "2,500"),
                }
                for marker in localized_values[lang]:
                    if marker not in body:
                        errors.append(f"{path.relative_to(ROOT)}: missing localized Dead or Alive 2 value {marker!r}")
                if meta.get("article_review_status") != "editorial-review-pending":
                    errors.append(f"{path.relative_to(ROOT)}: keep the profile pending until editorial sign-off")

            if slug == "legacy-of-dead":
                required_sources = (
                    "https://www.playngo.com/games/legacy-of-dead",
                    "https://cms.rationalcdn.com/v3/assets/blteecf9626d9a38b03/blt898cf269cdcf0f68/6669ae43664d450e1620e1a6/Legacy_of_Dead.pdf",
                )
                for source_url in required_sources:
                    if source_url not in body:
                        errors.append(f"{path.relative_to(ROOT)}: missing primary source link {source_url}")
                if len(body) < 1700:
                    errors.append(f"{path.relative_to(ROOT)}: Legacy of Dead profile is missing its localized mechanics sections")
                required_terms = {
                    "de": ("8 Freispiele", "Special Expanding Symbol", "250,000 coins", "500,000 USD"),
                    "en": ("8 Free Spins", "Special Expanding Symbol", "250,000 coins", "500,000 USD"),
                    "pl": ("8 początkowych darmowych spinów", "Special Expanding Symbol", "250,000 coins", "500,000 USD"),
                    "es": ("8 giros gratis", "Special Expanding Symbol", "250,000 coins", "500,000 USD"),
                    "pt": ("8 rodadas grátis", "Special Expanding Symbol", "250,000 coins", "500,000 USD"),
                    "ja": ("8回", "Special Expanding Symbol", "250,000 coins", "500,000 USD"),
                }
                for term in required_terms[lang]:
                    if term not in body:
                        errors.append(f"{path.relative_to(ROOT)}: missing localized/source-specific term {term!r}")
                if "96.58" in body:
                    errors.append(f"{path.relative_to(ROOT)}: unsupported RTP figure remains in Legacy of Dead profile")
                if meta.get("article_review_status") != "editorial-review-pending":
                    errors.append(f"{path.relative_to(ROOT)}: keep the profile pending until editorial sign-off")

    # Keep the two newly expanded profiles tied to their primary provider sources and verified feature descriptions.
    source_backed_profiles = {
        "wolf-gold": (
            ("https://www.pragmaticplay.com/en/games/wolf-gold-slot/",),
            1800,
            {
                "de": ("Money Respin", "Mega-Jackpot", "1.000×", "15 Positionen"),
                "en": ("Money Respin", "Mega Jackpot", "1,000×", "15 positions"),
                "pl": ("Money Respin", "Mega Jackpot", "1000×", "15 pozycji"),
                "es": ("Money Respin", "Mega Jackpot", "1.000×", "15 posiciones"),
                "pt": ("Money Respin", "Mega Jackpot", "1.000×", "15 posições"),
                "ja": ("Money Respin", "Mega Jackpot", "1,000倍", "15マス"),
            },
        ),
        "money-train-4": (
            (
                "https://www.relax-gaming.com/products/casino/moneytrain4",
                "https://www.relax-gaming.com/news/2023/09/relax-gamings-legendary-bandits-depart-the-station-for-their-last-stand-in-money-train-4",
            ),
            1800,
            {
                "de": ("Money Cart", "Arms Dealer", "Unlocker", "Upgrader", "Reset", "150.000×"),
                "en": ("Money Cart", "Arms Dealer", "Unlocker", "Upgrader", "Reset", "150,000×"),
                "pl": ("Money Cart", "Arms Dealer", "Unlocker", "Upgrader", "Reset", "150 000×"),
                "es": ("Money Cart", "Arms Dealer", "Unlocker", "Upgrader", "Reset", "150.000×"),
                "pt": ("Money Cart", "Arms Dealer", "Unlocker", "Upgrader", "Reset", "150.000×"),
                "ja": ("Money Cart", "Arms Dealer", "Unlocker", "Upgrader", "Reset", "150,000倍"),
            },
        ),
        "mega-moolah": (
            (
                "https://www.gamesglobal.com/Products",
                "https://www.megamoolah.com/news/what-are-the-key-symbols-i-need-to-know-on-the-mega-moolah-slot-539",
                "https://www.meccagames.com/games/mega-moolah",
            ),
            1900,
            {
                "de": ("Fünf Walzen", "25 Gewinnlinien", "15 Freispiele", "verdreifacht", "Mini, Minor, Major und Mega"),
                "en": ("Five reels", "25 paylines", "15 Free Spins", "tripled", "Mini, Minor, Major and Mega"),
                "pl": ("Pięć bębnów", "25 liniami", "15 spinów", "potrajane", "Mini, Minor, Major i Mega"),
                "es": ("Cinco rodillos", "25 líneas", "15 giros", "triplican", "Mini, Minor, Major y Mega"),
                "pt": ("Cinco rolos", "25 linhas", "15 rodadas", "triplicados", "Mini, Minor, Major e Mega"),
                "ja": ("5リール", "25ペイライン", "15回", "3倍", "Mini、Minor、Major、Mega"),
            },
        ),
        "immortal-romance": (
            (
                "https://help.danskespil.dk/en/casino-help/slots/mgsimmortalromancehtml",
                "https://www.meccagames.com/games/immortal-romance",
                "https://www.gamesglobal.com/Media/games_global_and_stormcraft_studios_reveal_the_highly_anticipated_release_of_Immortal_Romance_II",
            ),
            1900,
            {
                "de": ("243 Gewinnwege", "Wild Desire", "Chamber of Spins", "Amber", "Troy", "Michael", "Sarah", "5×", "6×"),
                "en": ("243 ways", "Wild Desire", "Chamber of Spins", "Amber", "Troy", "Michael", "Sarah", "5×", "6×"),
                "pl": ("243 stale aktywne sposoby", "Wild Desire", "Chamber of Spins", "Amber", "Troy", "Michael", "Sarah", "5×", "6×"),
                "es": ("243 formas", "Wild Desire", "Chamber of Spins", "Amber", "Troy", "Michael", "Sarah", "5×", "6×"),
                "pt": ("243 formas", "Wild Desire", "Chamber of Spins", "Amber", "Troy", "Michael", "Sarah", "5×", "6×"),
                "ja": ("243通り", "Wild Desire", "Chamber of Spins", "Amber", "Troy", "Michael", "Sarah", "5倍", "6倍"),
            },
        ),
    }
    for profile_slug, (required_sources, minimum_length, localized_terms) in source_backed_profiles.items():
        for lang in LANGS:
            path = ROOT / "content" / lang / "slot-profiles" / f"{profile_slug}.md"
            if not path.exists():
                errors.append(f"Missing source-backed profile {lang}/{profile_slug}")
                continue
            try:
                meta, body = read_page(path)
            except Exception as exc:
                errors.append(str(exc))
                continue
            for source_url in required_sources:
                if source_url not in body:
                    errors.append(f"{path.relative_to(ROOT)}: missing official source {source_url}")
            if len(body) < minimum_length:
                errors.append(f"{path.relative_to(ROOT)}: source-backed profile is too short ({len(body)} < {minimum_length})")
            for term in localized_terms[lang]:
                if term not in body:
                    errors.append(f"{path.relative_to(ROOT)}: missing checked feature/value {term!r}")
            if meta.get("article_review_status") != "editorial-review-pending":
                errors.append(f"{path.relative_to(ROOT)}: keep the profile pending until editorial sign-off")

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
    if "expert_insight" not in card_layout or "slot-game-card-insight--expert" not in card_layout:
        errors.append("Slot catalogue cards do not render localized expert insights")
    if "expert_insight" not in expert_text or "slot-expert-analysis--expert" not in expert_text:
        errors.append("Slot profile pages do not render source-based expert insight cards")
    if errors:
        print("ERROR: standalone slot-profile checks failed:")
        print("\n".join(f" - {item}" for item in errors))
        return 1
    print(f"OK: {len(games)} standalone profiles x {len(LANGS)} locales = {len(games) * len(LANGS)} pages.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
