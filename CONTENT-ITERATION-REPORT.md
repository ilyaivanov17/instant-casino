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


## Content batch 10: Legacy of Dead

Expanded the existing profile group in German, English, Polish, Spanish, Portuguese and Japanese:

- `content/de/slot-profiles/legacy-of-dead.md`
- `content/en/slot-profiles/legacy-of-dead.md`
- `content/pl/slot-profiles/legacy-of-dead.md`
- `content/es/slot-profiles/legacy-of-dead.md`
- `content/pt/slot-profiles/legacy-of-dead.md`
- `content/ja/slot-profiles/legacy-of-dead.md`

Updated the six catalogue card labels and descriptions in `data/slot_catalog.yaml` so they describe the Tomb Wild/Scatter role, Free Spins and the cumulative Expanding Symbol feature rather than the artwork alone.

### Source verification

Checked on 2026-11-03 against:

1. [Play'n GO — Legacy of Dead](https://www.playngo.com/games/legacy-of-dead): the provider page gives the release date as 2 January 2020; explains that three or more Tomb Scatters trigger Free Spins; describes the Tomb as a Wild and the randomly selected Special Expanding Symbol; and says Tomb Scatters can retrigger during Free Spins.
2. [Legacy of Dead Game Help PDF](https://cms.rationalcdn.com/v3/assets/blteecf9626d9a38b03/blt898cf269cdcf0f68/6669ae43664d450e1620e1a6/Legacy_of_Dead.pdf): the document is linked to a specific PA/USD game-help endpoint and lists five reels, up to ten selectable lines, eight initial Free Spins, eight additional spins on a Scatter retrigger, and one additional randomly selected Special Expanding Symbol per retrigger. It also specifies that Special Expanding Symbol wins in Free Spins may contain gaps.

The Game Help PDF is configuration-specific; its 8-spin award is not generalized to all markets or operators. The provider page describes potential winnings up to 250,000 coins, while that PA/USD help sheet lists a maximum win of 500,000 USD. Since those figures use different units and contexts, the profiles do not convert them into a single universal multiplier or state a universal maximum win. Neither consulted primary source gives a universally applicable current RTP or volatility class, so no such value is added.

The pages preserve existing URLs, translation keys, image paths, Dominic Field attribution and `editorial-review-pending` status. The edits are source-based editorial copy and do not claim a personal playtest or final human approval.

The profile validator now checks the two source links, minimum localized depth, source-specific Free Spins details, disclosure of the differing payout units, absence of the unsupported 96.58% RTP figure and pending editorial status.



## Content batch 11: Wolf Gold

Expanded the existing Wolf Gold profile in all six locales and aligned the catalogue summaries:

- `content/{de,en,pl,es,pt,ja}/slot-profiles/wolf-gold.md`
- `data/slot_catalog.yaml`

Official source checked on 2026-11-03:

1. [Pragmatic Play — Wolf Gold](https://www.pragmaticplay.com/en/games/wolf-gold-slot/): three Scatter symbols trigger five Free Spins; reels 2–4 combine into one giant symbol; three more Scatters award three additional spins with no stated overall retrigger limit. Six or more Money Symbols trigger Money Respin with three respins; new Money Symbols reset the counter to three; all visible values are collected at the end. Filling all 15 positions awards the 1,000× Mega Jackpot. Money Respin can also be triggered during Free Spins.

The six localized profiles distinguish the Free Spins route from Money Respin, explain the 15-position completion condition, and avoid adding unsupported RTP or stake-range values. The provider's 100× Money Symbol value and jackpot descriptions are attributed to its product page; no extra jackpot tiers or operator settings are inferred. Existing URLs, artwork, author attribution and `editorial-review-pending` status are preserved.

## Content batch 12: Money Train 4

Expanded the existing Money Train 4 profile in all six locales and updated the catalogue descriptions:

- `content/{de,en,pl,es,pt,ja}/slot-profiles/money-train-4.md`
- `data/slot_catalog.yaml`

Official Relax Gaming sources checked on 2026-11-03:

1. [Relax Gaming — Money Train 4 product page](https://www.relax-gaming.com/products/casino/moneytrain4): identifies the game as a Scatter Pays video slot, lists 20+ features and a provider-published maximum win of 150,000×, and describes Arms Dealer, Upgrader, Unlocker and Reset.
2. [Relax Gaming — Money Train 4 launch announcement, 20 September 2023](https://www.relax-gaming.com/news/2023/09/relax-gamings-legendary-bandits-depart-the-station-for-their-last-stand-in-money-train-4): describes the base-game Respin feature, sticky symbols and possible multipliers, the separate Money Cart Bonus Round with three spins and 20 possible special symbols, and the Arms Dealer, Unlocker and Upgrader roles. It also notes that direct bonus access is market-dependent and starts with one guaranteed persistent symbol where available.

The rewrite corrects the earlier broad Hold-and-Respin description by distinguishing the Scatter Pays game, base-game Respin and separate Money Cart bonus. The 150,000× figure is clearly attributed as a provider-published cap, not a typical outcome. No universal RTP or stake range is invented. Existing URLs, artwork, Jon Pill attribution and `editorial-review-pending` status are preserved.

Both batches include source checks in `scripts/check-slot-profiles.py`; the validator now enforces the provider source references, localized mechanics, profile depth and pending editorial status.


## Content batch 13: Mega Moolah (classic version)

Expanded all six localized profiles and aligned the catalogue card and six slot-hub summaries:

- `content/{de,en,pl,es,pt,ja}/slot-profiles/mega-moolah.md`
- `data/slot_catalog.yaml`
- `content/{de,en,pl,es,pt,ja}/slots.md`

Sources checked on 2026-11-03:

1. [Games Global — Products](https://www.gamesglobal.com/Products): current product portfolio and progressive jackpot network.
2. [Mega Moolah — What are the key symbols I need to know on the Mega Moolah slot?](https://www.megamoolah.com/news/what-are-the-key-symbols-i-need-to-know-on-the-mega-moolah-slot-539): Lion Wild, Monkey Scatter, 15 Free Spins and 3× feature description.
3. [Mecca Games — Mega Moolah](https://www.meccagames.com/games/mega-moolah): classic five-reel, 25-payline game rules, Lion Wild, Monkey Scatter, retriggers and randomly activated four-tier jackpot wheel.

The six profiles distinguish the classic 5-reel/25-payline Mega Moolah from later branded variants, separate Free Spins from the progressive jackpot wheel, and name the Mini, Minor, Major and Mega tiers. No fixed jackpot cash amounts, universal RTP or universal stake range are added. Existing URLs, artwork, author attribution and `editorial-review-pending` status are preserved.

## Content batch 14: Immortal Romance (original version)

Expanded all six localized profiles and aligned the catalogue card and six slot-hub summaries:

- `content/{de,en,pl,es,pt,ja}/slot-profiles/immortal-romance.md`
- `data/slot_catalog.yaml`
- `content/{de,en,pl,es,pt,ja}/slots.md`

Sources checked on 2026-11-03:

1. [Danske Spil — Immortal Romance game help](https://help.danskespil.dk/en/casino-help/slots/mgsimmortalromancehtml): original Microgaming rules for 243 ways, Wild multiplier, random Wild Desire and the four Chamber of Spins modes.
2. [Mecca Games — Immortal Romance](https://www.meccagames.com/games/immortal-romance): detailed mode rules, spin awards, unlock sequence, Vampire Bats, Rolling Reels and Wild Vine.
3. [Games Global — Immortal Romance II announcement](https://www.gamesglobal.com/Media/games_global_and_stormcraft_studios_reveal_the_highly_anticipated_release_of_Immortal_Romance_II): used to distinguish the original from its sequel.

The profiles explicitly identify the original game, not Immortal Romance II, Remastered or Immortal Romance Mega Moolah. They separate base-game Wild Desire from the Scatter-triggered Chamber of Spins, explain Amber/Troy/Michael/Sarah individually, and avoid a universal RTP or stake-range claim because operator help pages show different configurations. Existing URLs, artwork, Corey Levitan attribution and `editorial-review-pending` status are preserved.

The slot-profile validator now checks the exact source records, localized mechanics, profile depth and pending editorial status for both batches.

## Expert card batch 1: 5 Lions Megaways and Le Bandit

Introduced a separate localized `expert_insight` field for the catalogue cards of 5 Lions Megaways and Le Bandit, in German, English, Polish, Spanish, Portuguese and Japanese.

The new card copy is an interpretation of the mechanics rather than a repeat of the feature label:

- **5 Lions Megaways:** clarifies that 117,649 is the ceiling of the variable 7×6 layout, not a fixed count on every spin; highlights the seven Free Spins configurations and the trade-off between spin counts and Wild-multiplier ranges.
- **Le Bandit:** explains that Super Cascades preserve winning positions as Golden Squares, which Rainbow activates later; distinguishes the five-FS mode by its persistent highlighted squares and guaranteed Rainbow on each spin.

Sources checked on 2026-11-03:

1. [Pragmatic Play — 5 Lions Megaways](https://www.pragmaticplay.com/en/games/5-lions-megaways/): three or more bonus symbols trigger the feature; seven Free Spins options combine up to 25 spins with Wild multipliers up to 40×.
2. [Pragmatic Play — 5 Lions Megaways launch announcement, 24 June 2021](https://www.pragmaticplay.com/en/news/pragmatic-play-recharges-asian-adventure-in-5-lions-megaways/): 7×6 layout, up to 117,649 ways, Tumbles, Gold Lion Wild and Yin-Yang Scatter.
3. [Hacksaw Gaming — Le Bandit](https://www.hacksawgaming.com/games/le-bandit): Super Cascades, Golden Squares and Rainbow activation, coin and special-symbol sequence, and the three bonus modes.

The catalogue cards and their corresponding game-profile pages now render the same localized expert takeaway. Other catalogue entries retain the existing editorial-insight fallback until their own source-backed analysis is prepared. The card label field remains unchanged. Existing game URLs, images, author attribution and `editorial-review-pending` status are preserved; no claim of a personal playtest or human editorial sign-off is made.

Automated validation now checks that both expert insight fields exist in all six locales, contain the expected game-specific mechanics, stay within the approved card-length range and render in both catalogue and profile templates.

## Expert card batch 2: Money Train 3, Money Train 4, Fruit Party 2 and Gates of Olympus

Added localized expert takeaways to the four catalogue entries and matching profile pages, in German, English, Polish, Spanish, Portuguese and Japanese.

- **Money Train 3:** separates the jobs of Shapeshifter, Absorber and Tommy Gun, and distinguishes the three-symbol Money Cart trigger from the no-win Respin trigger.
- **Money Train 4:** separates Scatter Pays, base-game Respins and Money Cart; clarifies the different roles of Arms Dealer, Unlocker, Upgrader and Reset.
- **Fruit Party 2:** prevents a common comparison error by distinguishing the additive 256× base-game Wild multiplier across winning clusters from the up-to-729× value of an individual Wild during Free Spins.
- **Gates of Olympus:** explains pays-anywhere wins (8–30 matching symbols), Tumbles and the running Free Spins multiplier; the accumulated multiplier increases when a multiplier symbol lands on a winning spin.

Primary sources are linked in the corresponding existing English profile and were used as the source record for the localized takeaway:

1. [Relax Gaming — Money Train 3 announcement, 22 September 2022](https://www.relax-gaming.com/news/2022/09/relax-gamings-biggest-slot-release-of-the-year-money-train-3-arrives-at-the-station)
2. [Relax Gaming — Money Train 4 product page](https://www.relax-gaming.com/products/casino/moneytrain4) and [launch announcement, 20 September 2023](https://www.relax-gaming.com/news/2023/09/relax-gamings-legendary-bandits-depart-the-station-for-their-last-stand-in-money-train-4)
3. [Pragmatic Play — Fruit Party 2 announcement, 5 August 2021](https://www.pragmaticplay.com/en/news/pragmatic-play-back-with-juicier-wins-than-ever-in-fruit-party-2/)
4. [Pragmatic Play — Gates of Olympus product page](https://www.pragmaticplay.com/en/games/gates-of-olympus/) and [original game announcement, 24 February 2021](https://www.pragmaticplay.com/en/news/pragmatic-play-aims-for-the-heavens-in-gates-of-olympus/)

No additional RTP, volatility, stake or personal-playtest claims were introduced. Existing URLs, artwork, authorship and `editorial-review-pending` status are preserved.

## Expert card coverage status

Six of the 25 catalogue games now have source-based, localized expert takeaways: 5 Lions Megaways, Le Bandit, Money Train 3, Money Train 4, Fruit Party 2 and Gates of Olympus.

The remaining cards retain the previous catalogue-label fallback until a source-backed game-specific insight is prepared. Short or stub profiles such as Wanted Dead or a Wild and Thunderstruck II are deliberately not given speculative expert copy; they need a fuller source verification pass first.

## Expert card batch 3: Starburst, The Dog House and Legacy of Dead

Added expert takeaways for three established profiles, across German, English, Polish, Spanish, Portuguese and Japanese.

- **Starburst:** clarifies that the ten paylines are evaluated in both directions rather than doubled into twenty separate lines; the Expanding Wild fills a reel and triggers a Respin without guaranteeing a win.
- **The Dog House:** highlights that multiplier Wilds are on reels 2–4, three Bonus Paws trigger a randomly allocated number of Free Spins, and Sticky Wilds remain in place during the bonus.
- **Legacy of Dead:** explains the Tomb's dual Wild/Scatter role and the three-symbol Free Spins trigger; carefully labels the randomly selected Special Expanding Symbol and any spin counts as configuration-specific to the reviewed rules PDF.

Sources already recorded in the corresponding source-based profiles:

1. [NetEnt — Starburst](https://netent.com/games/starburst) and [Evolution Games — Starburst](https://games.evolution.com/slots/starburst/).
2. [Pragmatic Play — The Dog House](https://www.pragmaticplay.com/en/games/the-dog-house-slot/) and [original launch announcement](https://www.pragmaticplay.com/en/news/pragmatic-play-launches-the-dog-house/).
3. [Play'n GO — Legacy of Dead](https://www.playngo.com/games/legacy-of-dead) and [the specific PA/USD rules PDF](https://cms.rationalcdn.com/v3/assets/blteecf9626d9a38b03/blt898cf269cdcf0f68/6669ae43664d450e1620e1a6/Legacy_of_Dead.pdf).

The card copy does not generalize the reviewed PDF's spin counts to every operator version and does not introduce unsupported volatility, universal RTP or stake claims. Existing URL, artwork, author attribution and pending editorial status are preserved.

## Expert card batch 4: Immortal Romance, Sweet Bonanza, Wolf Gold, Mega Moolah and Gonzo's Quest

Added five more localized expert takeaways in all six configured languages.

- **Immortal Romance:** separates random base-game Wild Desire from the Scatter-triggered Chamber of Spins and notes that the Amber/Troy/Michael/Sarah modes unlock through the 1/5/10/15 entry progression.
- **Sweet Bonanza:** clarifies that 8–12+ matching symbols can win anywhere on the 6×5 grid and that Free Spins multipliers from 2× to 100× are summed at the end of the full tumble sequence.
- **Wolf Gold:** distinguishes the 3-Scatter/5-Free-Spins giant-symbol route from the six-Money-Symbol Money Respin route, including the respin reset and 15-position completion condition.
- **Mega Moolah:** separates the Lion Wild's 2× line-win effect and 15 Free Spins with 3× wins from the independent progressive jackpot wheel and its four tiers.
- **Gonzo's Quest:** explains that Avalanche chains belong to one paid spin, the base multiplier grows to x5 and resets when the chain ends, while Free Falls use a higher multiplier scale up to x15.

Sources are linked from the corresponding existing English profiles:

1. [Danske Spil — Immortal Romance game help](https://help.danskespil.dk/en/casino-help/slots/mgsimmortalromancehtml), [Mecca Games — Immortal Romance](https://www.meccagames.com/games/immortal-romance).
2. [Pragmatic Play — Sweet Bonanza product page](https://www.pragmaticplay.com/en/games/sweet-bonanza-slot/) and [launch article](https://www.pragmaticplay.com/en/news/pragmatic-play-launches-sweet-bonanza/).
3. [Pragmatic Play — Wolf Gold](https://www.pragmaticplay.com/en/games/wolf-gold-slot/).
4. [Games Global — progressive jackpot portfolio](https://www.gamesglobal.com/Products), [Mega Moolah feature guide](https://www.megamoolah.com/news/what-are-the-key-symbols-i-need-to-know-on-the-mega-moolah-slot-539), and [Mecca Games — classic rules](https://www.meccagames.com/games/mega-moolah).
5. [NetEnt — Gonzo's Quest](https://netent.com/games/gonzos-quest) and [Danske Spil — Gonzo's Quest game help](https://help.danskespil.dk/en/casino-help/slots/netentgonzosquesthtml).

No universal RTP, volatility or stake claims are added to the expert cards. Operator-specific rules remain identified as version-dependent in the associated profiles.

## Expert card batch 5: Reactoonz, Wild West Gold, Starlight Princess, Mega Fortune, Twin Spin, Sugar Rush and Wanted Dead or a Wild

Added source-based expert insights for seven more games in all six locales.

- **Reactoonz:** cluster wins of five or more on a 7×7 grid charge Gargantoon; Quantum Leap then releases a chain of up to five features.
- **Wild West Gold:** distinguishes 2×/3×/5× multiplier Wilds on reels 2–4, the three-Sunset-Scatter trigger and Sticky Wilds / additional spins during the bonus.
- **Starlight Princess:** separates pays-anywhere wins (8–30 matching symbols) from multiplier evaluation; multipliers are summed at tumble end and winning bonus multipliers build a running total. A conflicting displayed initial-spin count is intentionally omitted.
- **Mega Fortune:** distinguishes the x5 Wild effect on eligible line wins from the separate three-wheel progressive jackpot game triggered by three Bonus symbols on an active line.
- **Twin Spin:** explains that each spin starts with at least two adjacent linked reels, which can expand to three, four or five, while wins use 243 ways rather than fixed paylines.
- **Sugar Rush:** explains how winning positions are marked, same-spin hits build a multiplier from 2× up to 128×, and marks/multipliers persist through the Free Spins round.
- **Wanted Dead or a Wild:** explains VS-triggered DuelReels and distinguishes the sticky-Wild Great Train Robbery from the collection-and-Showdown sequence in Dead Man's Hand.

Sources used and recorded in the source list:

1. [Play'n GO — Reactoonz](https://www.playngo.com/games/reactoonz).
2. [Pragmatic Play — Wild West Gold product page](https://www.pragmaticplay.com/en/games/wild-west-gold-slot/) and [launch article, 26 March 2020](https://www.pragmaticplay.com/en/news/pragmatic-play-rides-into-town-with-wild-west-gold/).
3. [Pragmatic Play — Starlight Princess product page](https://www.pragmaticplay.com/en/games/starlight-princess/) and [launch article, 23 September 2021](https://www.pragmaticplay.com/en/news/pragmatic-play-delivers-regal-adventure-in-starlight-princess/).
4. [NetEnt — Mega Fortune](https://netent.com/games/mega-fortune).
5. [NetEnt — Twin Spin](https://netent.com/games/twin-spin) and [Danske Spil game help](https://help.danskespil.dk/en/casino-help/slots/netenttwinspinhtml).
6. [Pragmatic Play — original Sugar Rush](https://www.pragmaticplay.com/en/games/sugar-rush/).
7. [Hacksaw Gaming — Wanted Dead or a Wild](https://www.hacksawgaming.com/games/wanted-dead-or-a-wild).

The insight deliberately does not carry operator-specific RTP/stake figures into the cards. Existing URLs, art, authorship and pending editorial review are preserved.

## Expert card batch 6: Thunderstruck II

Completed the final catalogue entry with localized expert insight in all six languages.

The card explains the Great Hall of Spins progression: Valkyrie is available on the first entry, Loki unlocks after five activations, Odin after ten and Thor after fifteen. It emphasizes that each chamber changes the bonus mechanic, not only the number of spins: x5 wins, Wild Magic, Wild Ravens and Rolling Reels.

Sources checked:

1. [Mecca Games — Thunderstruck II game rules](https://www.meccagames.com/games/thunderstruck-ii): 243 ways, Wild and Scatter rules, Wild Storm, Great Hall of Spins, chamber unlocks and each mode's feature.
2. [Danske Spil — Thunderstruck II game help](https://help.danskespil.dk/en/casino-help/slots/mgsthunderstruck2html): confirms the five-reel/243-ways structure and gives detailed rules for Valkyrie, Loki, Odin and Thor.

The profile remains editorial-review-pending. Version-specific bet configuration and the operator-specific RTP are not generalized into the expert card.
