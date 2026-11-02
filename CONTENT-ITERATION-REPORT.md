# Content iteration report — batch 1: Starburst

Date: 2026-11-02  
Branch: `seo/fix-indexing-hreflang-2026-11`  
Pull request: https://github.com/ilyaivanov17/instant-casino/pull/43

## Scope

Expanded the existing Starburst profile as one localized page group rather than creating a duplicate URL. Updated the six locale files:

- `content/de/slot-profiles/starburst.md`
- `content/en/slot-profiles/starburst.md`
- `content/pl/slot-profiles/starburst.md`
- `content/es/slot-profiles/starburst.md`
- `content/pt/slot-profiles/starburst.md`
- `content/ja/slot-profiles/starburst.md`

Also updated the Starburst entry in `data/slot_catalog.yaml`, so the six catalogue cards reflect the same checked mechanics as the profile.

## What changed

Each locale now includes a structured fact table, an explanation of the two-way line evaluation, the expanding Wild and Respin sequence, interpretation notes for RTP/hit frequency/maximum payout, a version-check checklist and direct links to the official provider sources. The card description is aligned with the long-form profile. The existing translation key, URL, image, author metadata and internal navigation were preserved.

The pages do not claim that a personal playtest was performed. `article_review_status: editorial-review-pending` is intentionally retained pending editorial sign-off.

## Source verification

Checked on 2026-11-02:

1. [NetEnt — Starburst](https://netent.com/games/starburst): the current product page lists release date 23 January 2012, 96.08% RTP, 23.00% hit frequency, 800× max payout, a 5×3 grid, a 10-line maximum, a €0.10–€100.00 bet range, and describes the expanding Wild and Respin feature. The current page does not state a volatility category.
2. [Evolution Games — Starburst](https://games.evolution.com/slots/starburst/): describes the five-reel/three-row game, ten paylines and the “Win Both Ways” evaluation. Its current page lists RTP as 96.09%.

The provider pages therefore differ by 0.01 percentage point in the displayed RTP (96.08% versus 96.09%). The page records this discrepancy and tells readers to use the information/help panel in the active casino version. No unsupported volatility label, maximum chain length, bonus trigger count or alternate-game feature was added.

## Automated safeguards added

`scripts/check-slot-profiles.py` now checks that all six Starburst profiles retain both primary-source links, contain the expanded localized content sections, and remain pending editorial approval. Existing validation continues to check all 35 profiles across six locales, catalogue descriptions, localized keywords, URL mapping and internal catalogue links.

## Not covered in this iteration

This batch covers Starburst only. It does not certify facts for the other 34 games, complete native-speaker proofreading across all site pages, establish the active configuration at every casino operator, or replace Search Console / post-deployment HTTP monitoring.


## Content batch 2: Book of Dead

Expanded the existing six-language page group:

- `content/de/slot-profiles/book-of-dead.md`
- `content/en/slot-profiles/book-of-dead.md`
- `content/pl/slot-profiles/book-of-dead.md`
- `content/es/slot-profiles/book-of-dead.md`
- `content/pt/slot-profiles/book-of-dead.md`
- `content/ja/slot-profiles/book-of-dead.md`

The six profile pages and the catalogue teaser in `data/slot_catalog.yaml` now describe the same checked feature flow: the Tomb symbol's Wild/Scatter roles, three Tombs triggering ten Free Spins, the random selection of a Special Expanding Symbol, its conditional expansion across all three reel positions, the possibility of non-adjacent expanded symbols forming a win, and the award of ten additional spins when three Tombs retrigger the feature.

### Source verification

Checked on 2026-11-02 against:

1. [Play'n GO — How to play Rich Wilde and the Book of Dead walkthrough](https://www.playngo.com/post/book-of-dead-walkthrough): three Tombs trigger ten Free Spins; a symbol is selected at random before the feature; it can expand only when it creates additional prizes on active paylines; three more Tombs during Free Spins award ten additional spins.
2. [Play'n GO — A complete guide on how to play Book of Dead](https://www.playngo.com/post/a-complete-guide-on-how-to-play-book-of-dead): five reels, three rows, up to ten selectable paylines, and the Tomb's Wild/Scatter role.

The prior German profile listed 96.21% RTP, high volatility and a 0.1–50 EUR stake range. The two official Play'n GO articles used here do not verify those values for a specific current casino configuration. Those figures were therefore removed from all six localized profiles; readers are directed to the help panel of the game version actually loaded. No substitute values were invented.

The Polish and Portuguese profiles no longer contain the English template fragment that appeared in their previous editorial copy. The Japanese version now has the same substantive mechanics explanation and source references as the other locales. All six pages remain `editorial-review-pending`; this pass is source-backed editing, not an assertion of a personal playtest or final human editorial approval.

The profile QA now checks the two official Play'n GO source links, the expanded localized content, absence of the unsupported RTP/stake figure, and the pending-review status.


## Content batch 3: Bigger Bass Bonanza

Expanded all six localized profiles:

- `content/de/slot-profiles/bigger-bass-bonanza.md`
- `content/en/slot-profiles/bigger-bass-bonanza.md`
- `content/pl/slot-profiles/bigger-bass-bonanza.md`
- `content/es/slot-profiles/bigger-bass-bonanza.md`
- `content/pt/slot-profiles/bigger-bass-bonanza.md`
- `content/ja/slot-profiles/bigger-bass-bonanza.md`

Updated the catalogue teaser in `data/slot_catalog.yaml` to match the full profile.

### Source verification

Checked on 2026-11-02 against the official Pragmatic Play pages:

1. [Bigger Bass Bonanza — English](https://www.pragmaticplay.com/en/games/bigger-bass-bonanza/)
2. [Bigger Bass Bonanza — German](https://www.pragmaticplay.com/de/spiele/bigger-bass-bonanza/)

The new profiles describe the 4×5 format, 3/4/5 Scatter triggers awarding 10/15/20 Free Spins, Fisherman Wild collecting all visible Money Symbols, Money Symbol values up to 4,000× bet in the bonus, every fourth Wild retriggering 10 additional Free Spins, and the 2× / 3× / 10× multiplier progression.

The 4,000× value is explicitly described as a Money Symbol value, not as the overall maximum game payout. RTP, volatility and stake range were removed from all six pages because they are not listed on the official product pages consulted; no replacement values were invented. The text distinguishes Bigger Bass Bonanza from Bigger Bass Bonanza 1000 and Big Bass Football Bonanza to avoid mixing features from related titles.

Each locale retains `editorial-review-pending`; the source-backed rewrite does not claim a personal playtest or final human sign-off. The six catalogue descriptions now reflect the verified bonus loop and remain within the existing 45–180-character requirement. Profile QA checks the two official sources, localized content length, absence of the old unsupported RTP/stake values and pending-review status.
