# Content expansion log — Dead or Alive 2

Date: 2026-11-02  
Page: `/slots/dead-or-alive-2/`  
Locales: de, en, pl, es, pt, ja.

## What changed

The six localized profile pages now explain the original game's three free-spins modes instead of describing them as one generic bonus:

- Five reels, three rows and nine fixed paylines.
- Wild substitution rules and Scatter wins independent of paylines.
- Old Saloon: all free-spin wins are doubled; Sticky Wilds remain; one or more Sticky Wilds on each reel can award five extra spins.
- High Noon Saloon: two Wilds on one reel form an x2 Multiplier Wild, three form an x3 Multiplier Wild; multiple multiplier Wilds can combine (NetEnt's example: x2 × x3 = x6).
- Train Heist: every Wild increases a meter from x1 and awards an extra spin; reaching x16 adds five spins, while later Wilds continue to add spins.
- The importance of checking which bonus mode is active before evaluating a result.

The NetEnt Game Sheet cited is version 1.2 dated 29 September 2020 and describes a specific game variant. It is not treated as universal current operator configuration. One operator help page lists twelve initial free spins for each mode in its own implementation; the page explicitly tells readers to confirm this in the version they have opened. RTP, stakes and other default values from the old game sheet were not copied into the profile.

Existing URLs, translation keys, author metadata, CTA, related links and catalogue navigation are preserved. Localized catalogue descriptions were synchronized and an existing German alt-text grammar error was corrected. `lastmod` reflects the content change; review status remains `editorial-review-pending`.

## Sources

1. NetEnt, [Dead or Alive 2 Game Sheet, version 1.2 dated 29 September 2020](https://cdn-sp.kertn.net/assets/cms/App_Data/20e8c524-e223-48de-9382-7401c87cd065/PDFs/GameRules/Netent/GamerulesEN/Dead_or_Alive_2_deadoralive2_not_mobile_Game_Sheet_default_en.pdf). It documents the reel/grid/line layout, Wild and Scatter rules, and the three distinct bonus mechanisms.
2. NetEnt, [Dead or Alive 2 announcement dated 24 April 2019](https://www.netent.com/en/wp-content/uploads/sites/2/2019/04/netent-netent-heads-back-to-the-wild-west-with-dead-or-alive-2-the-sequel-to-one-its-most-iconic-games-190424.pdf).
3. Danske Spil, [Dead or Alive 2 operator help](https://help.danskespil.dk/en/casino-help/slots/netentdeadoralive2). Used only for the operator-specific note about twelve initial free spins per mode; it is not presented as a universal NetEnt setting.

## QA

GitHub Actions runs the existing content and slot-profile checks, Hugo production build, sitemap and rendered metadata validation, public-output safety check, and Playwright mobile/browser smoke tests.
