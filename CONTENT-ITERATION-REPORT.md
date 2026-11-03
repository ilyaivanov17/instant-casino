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


## Content batch 4: Bonanza (Big Time Gaming)

Expanded all six localized pages:

- `content/de/slot-profiles/bonanza.md`
- `content/en/slot-profiles/bonanza.md`
- `content/pl/slot-profiles/bonanza.md`
- `content/es/slot-profiles/bonanza.md`
- `content/pt/slot-profiles/bonanza.md`
- `content/ja/slot-profiles/bonanza.md`

Source: [Big Time Gaming — Bonanza](https://beta.bigtimegaming.com/games/bonanza), checked 2026-11-02.

The source describes a 6×7 Megaways format with up to 117,649 ways, RTP 96.11%, hit frequency 37.94%, max payout 26,000× bet, and a listed stake range of €0.20–€20.00. It describes Dual Reactions as cascades from above and from the right. Four Scatters spell GOLD and unlock 12 Free Spins; each extra Scatter adds five. During Free Spins, each win triggers a reaction and increases the win multiplier by one. The page also lists Bonus Buy at 90× bet for 12 Free Spins.

The structured Volatility field on the provider page is blank. The profile does not turn that missing field into an independent low/medium/high rating. It distinguishes the provider's narrative phrase from a structured volatility value and asks readers to check the active casino build. Product settings may vary by operator/region. The six pages remain `editorial-review-pending`.

The source-backed page group replaces the older, unverified profile entries (including the former 96.1% RTP, “Medium” volatility and 0.1–50 EUR range). The catalog descriptions now include GOLD, the Free Spins award and Dual Reactions.

## Content batch 5: Sweet Bonanza (original title)

Expanded all six localized pages:

- `content/de/slot-profiles/sweet-bonanza.md`
- `content/en/slot-profiles/sweet-bonanza.md`
- `content/pl/slot-profiles/sweet-bonanza.md`
- `content/es/slot-profiles/sweet-bonanza.md`
- `content/pt/slot-profiles/sweet-bonanza.md`
- `content/ja/slot-profiles/sweet-bonanza.md`

Sources checked on 2026-11-02:

1. [Pragmatic Play — Sweet Bonanza product page](https://www.pragmaticplay.com/en/games/sweet-bonanza-slot/)
2. [Pragmatic Play — original Sweet Bonanza launch article](https://www.pragmaticplay.com/en/news/pragmatic-play-launches-sweet-bonanza/)

The current product page describes 8–12+ matching symbols anywhere on the grid, 4–6 Scatters triggering 10 Free Spins, multiplier symbols from 2× to 100× and addition of multiplier values at the end of the tumble sequence. It lists base-game and Scatter-related awards separately. The 2019 launch article describes the original game as 6×5 and explains that winning symbols disappear and are replaced by new symbols falling from above.

The profile distinguishes the original Sweet Bonanza from Sweet Bonanza 2500, Sweet Bonanza 1000 and Sweet Bonanza Super Scatter. No RTP or stake range is invented where the current product page does not publish one. A 2019 launch statement described the title as high-volatility, but the article notes that a current casino version's own help is the relevant place to check such a label. All six pages keep `editorial-review-pending`.

The localized Japanese profile has been expanded from a short stub; the former mixed-language fragments (including German `zufällige`) in Polish, Spanish, Portuguese and Japanese have been replaced with native-language copy. Catalogue descriptions now reflect the matching-symbol, Scatter and multiplier rules.


## Content batch 6: Fruit Party (original title)

Expanded all six localized profiles:

- `content/de/slot-profiles/fruit-party.md`
- `content/en/slot-profiles/fruit-party.md`
- `content/pl/slot-profiles/fruit-party.md`
- `content/es/slot-profiles/fruit-party.md`
- `content/pt/slot-profiles/fruit-party.md`
- `content/ja/slot-profiles/fruit-party.md`

Sources checked on 2026-11-02:

1. [Pragmatic Play — Fruit Party product page](https://www.pragmaticplay.com/en/games/fruit-party-slot/)
2. [Pragmatic Play — original Fruit Party launch article](https://www.pragmaticplay.com/en/news/pragmatic-play-gets-summer-started-with-fruit-party/)

The current product page describes a 7×7 cluster-pays game. In the base game, each symbol in a winning block can randomly carry 2×; symbol multipliers multiply together up to 256×. Three or more Scatters trigger 10 Free Spins. During the feature, winning symbols can carry 2× or 4× multipliers; additional groups of 3–7 Scatters can retrigger with 10–14 Free Spins. The launch article confirms the original 7×7 layout and tumble mechanic.

The prior RTP value of 96.47% and stake range of 0.2–100 EUR were removed from all six profiles because the current official product page consulted does not publish those settings. No substitute figures were invented. The article notes that the 2019 launch announcement described the original game as high-volatility, but directs readers to check the active version's own help for current configuration.

The profiles explicitly distinguish original Fruit Party from Fruit Party 2. The Japanese source page has been expanded from a short stub, and the Polish, Spanish and Portuguese pages have been rewritten to remove template-like language. The catalogue summaries now include cluster count, 2× multiplier behaviour, Scatter trigger and the 256× combined multiplier cap. Profile QA checks both official sources, content depth, absence of the old unsupported figures, and pending editorial status.


## Content batch 7: The Dog House (original title)

Expanded all six localized profiles:

- `content/de/slot-profiles/the-dog-house.md`
- `content/en/slot-profiles/the-dog-house.md`
- `content/pl/slot-profiles/the-dog-house.md`
- `content/es/slot-profiles/the-dog-house.md`
- `content/pt/slot-profiles/the-dog-house.md`
- `content/ja/slot-profiles/the-dog-house.md`

Sources checked on 2026-11-02:

1. [Pragmatic Play — The Dog House product page](https://www.pragmaticplay.com/en/games/the-dog-house-slot/): 5×3, 20 paylines, multiplier Wilds on reels 2, 3 and 4, Sticky Wilds during Free Spins.
2. [Pragmatic Play — original launch announcement](https://www.pragmaticplay.com/en/news/pragmatic-play-launches-the-dog-house/), dated 2019-05-09: three Bonus Paw symbols activate Free Spins, the number of spins is randomly allocated, and the launch announcement mentioned wins of up to 6,750× the original stake.

The page does not publish a current RTP, stake range or exact Wild multiplier values. None were invented. The 6,750× value is explicitly attributed to the 2019 launch announcement and is not presented as a typical result or guaranteed configuration. The profile distinguishes the original game from The Dog House Megaways, The Dog House Multihold, The Dog House Muttley Crew and The Dog House – Dog or Alive. All six pages retain `editorial-review-pending`.

The catalogue card now includes the 5×3 / 20-line layout, randomly allocated Free Spins from three Bonus Paws and multiplier Wilds on reels 2–4. Profile QA checks both provider URLs, minimum localized content depth, the four edition distinctions and the pending editorial state.

## Site-wide tools.cafe listing badge

Added the exact supplied badge markup to `layouts/partials/footer.html`, above the footer copyright/legal row. Since this partial is shared by the base layout, the badge appears across the site's public page routes and all six languages.

The URL, image source, target, rel value, alt text and dimensions are preserved exactly:
- `https://tools.cafe/p/instant-slot-reviews`
- `https://tools.cafe/b/light.svg`
- `target="_blank"`, `rel="noopener"`
- `alt="Listed on tools.cafe"`, `width="180"`, `height="54"`

`tests/mobile-smoke.cjs` now checks that the link and image exist in the footer on inspected routes and that target, rel, alt and dimensions match the supplied markup. The check runs for home, section and localized catalogue routes at mobile viewport widths as part of the regular Playwright smoke test.


## Final tools.cafe badge placement

The user later asked to retain the tools.cafe listing while keeping the footer uncluttered. The badge is now placed as a compact item in the bottom copyright/legal row of the shared footer, after the legal notice. It remains ordinarily visible and is not hidden behind imagery, opacity tricks or crawler-specific markup.

The supplied href, image source, target, rel, alt text and dimensions are retained. The Playwright smoke test checks that the badge exists on inspected home, section and localized catalogue routes, has its expected attributes, and is not hidden by CSS.


## Content batch 8: Fire in the Hole 3

Expanded the existing six localized profiles and aligned the six catalogue card summaries:

- `content/de/slot-profiles/fire-in-the-hole-3.md`
- `content/en/slot-profiles/fire-in-the-hole-3.md`
- `content/pl/slot-profiles/fire-in-the-hole-3.md`
- `content/es/slot-profiles/fire-in-the-hole-3.md`
- `content/pt/slot-profiles/fire-in-the-hole-3.md`
- `content/ja/slot-profiles/fire-in-the-hole-3.md`
- `data/slot_catalog.yaml`

The updated profiles now explain the 6-reel playfield beginning with three active rows and expanding to six, the maximum 46,656 ways in the full 6×6 layout, the triggers for Collapsing Mine, xBomb Wild, Wild Mining, xSplit, xHole, features buried in ice, and the Lucky Wagon Spins structure. They distinguish provider-published statistics (96.05% RTP, Extremely Volatile, maximum payout 70,000× base bet) from settings that can vary by operator integration.

### Source verification

Checked on 2026-11-03 against the official Nolimit City product/rules page:

1. [Nolimit City — Fire in the Hole 3](https://nolimitcity.com/games/fire-in-the-hole-3): product page and detailed feature rules, including RTP, volatility, maximum payout, reel expansion, xBomb, Wild Mining, xSplit, xHole, buried features and Lucky Wagon Spins.
2. [Nolimit City — Fire In The Hole 3: NOW LIVE!](https://nolimitcity.com/posts/fire-in-the-hole-3-now-live): launch announcement dated 3 June 2025, corroborating the core xMechanics and bonus feature structure.

No personal playtest, operator-specific settings or guaranteed outcome is claimed. The six profiles retain `editorial-review-pending`. The card summaries now reflect the three-active-row expansion and name xBomb, xSplit, xGod and Lucky Wagon Spins.

### Automated safeguards

The slot-profile validator now checks both official source links in all six Fire in the Hole 3 profiles, a minimum localized content depth, the presence of all seven named mechanics, and the pending editorial status. Existing catalogue validation continues to enforce unique localized card descriptions, SEO keyword coverage, author links and 45–180 character card summaries.



## Content batch 9: Dead or Alive 2

Reviewed and expanded all six localized profiles:

- `content/de/slot-profiles/dead-or-alive-2.md`
- `content/en/slot-profiles/dead-or-alive-2.md`
- `content/pl/slot-profiles/dead-or-alive-2.md`
- `content/es/slot-profiles/dead-or-alive-2.md`
- `content/pt/slot-profiles/dead-or-alive-2.md`
- `content/ja/slot-profiles/dead-or-alive-2.md`

Sources checked on 2026-11-03:

1. [NetEnt Game Sheet v1.2, dated 29 September 2020](https://cdn-sp.kertn.net/assets/cms/App_Data/20e8c524-e223-48de-9382-7401c87cd065/PDFs/GameRules/Netent/GamerulesEN/Dead_or_Alive_2_deadoralive2_not_mobile_Game_Sheet_default_en.pdf): five reels, three rows, nine fixed paylines; Scatter wins independent of paylines; the three Free Spins modes; Sticky Wild behaviour; High Noon x2/x3 multiplier combination; Train Heist meter and extra-spin rules. Pages 3–4 were visually checked.
2. [NetEnt launch announcement, 24 April 2019](https://news.cision.com/netent/r/netent-heads-back-to-the-wild-west-with-dead-or-alive-2---the-sequel-to-one-its-most-iconic-games,c2795155): original volatility wording and three separate Free Spins modes.
3. [Evolution product page](https://games.evolution.com/slots/dead-or-alive-2/): RTP 96.80%, High volatility classification, 2/3/4/5 Scatter instant prizes of 2x/4x/25x/2,500x, 12 initial Free Spins after the Scatter trigger, mode summaries and up to 100,000x potential in Train Heist.

The Evolution page and the NetEnt Game Sheet differ in how they describe the Old Saloon +5 Free Spins trigger. That discrepancy is explicitly disclosed in each localized profile rather than collapsed into a single universal rule. Evolution labels volatility "High", while NetEnt's 2019 launch announcement uses "extreme volatility"; both source labels are retained with attribution.

All six catalogue labels/descriptions now identify game mechanics rather than using image-scene wording. The Japanese profile receives additional Scatter payout, mode-choice, RTP/volatility and maximum-win explanations. Existing URLs, translation keys, imagery, Dominic Field byline assignment and `editorial-review-pending` status are preserved. Profile QA now checks primary sources, localized provider figures, mode coverage and Japanese content depth.
