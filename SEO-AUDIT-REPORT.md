# SEO audit report — instant.slot-reviews.com

Audit date: 2026-11-02  
Repository: [ilyaivanov17/instant-casino](https://github.com/ilyaivanov17/instant-casino)  
Audited ref: `main` at `e91247e061373c604f665773e175534cef64b6ed`  
Production origin: https://instant.slot-reviews.com/

## Scope and method

The audit covered the Hugo configuration, the recursive Git tree (560 tracked files), all six locale trees, Hugo layouts and SEO partials, the slot catalogue, release scripts, GitHub Actions, and deployed production routes. Production HTML, head metadata, robots.txt, the sitemap index and all six language sitemap endpoints were fetched directly. Representative German, English and Japanese slot pages and the German slot-guide page were inspected.

The repository has 348 Markdown files under the six language content trees, 35 entries in `data/slot_catalog.yaml`, and corresponding standalone profile sources in six locales (210 profile source files). There is an existing collection of static QA scripts and a GitHub Actions Hugo production workflow.

This is a source and production crawl audit, not Google Search Console verification. No Search Console property data, URL Inspection results, crawl statistics or index coverage reports were available.

## Findings

### P0 — Hugo root configuration is accidentally scoped under [minify]

**Evidence:** In `hugo.toml`, the root-level configuration settings `buildDrafts`, `buildFuture`, `buildExpired`, `canonifyURLs`, `enableGitInfo` and `disableKinds` occur after the TOML table header `[minify]` and before the next table header. TOML therefore parses these keys as members of `minify`, not as top-level Hugo settings. The setting intended to disable taxonomy and term output is not active at the root level.

**Production confirmation:** `/categories/` and `/tags/` both return rendered pages with HTTP-successful fetches, self-canonical URLs, `index,follow`, and generic metadata. Both appear in every language sitemap. They contain no useful taxonomy terms or category/tag navigation and are thin listing stubs. The production sitemap endpoints report 61 URLs each (366 URL entries across six sitemaps).

**Resolution:** Move all root-level Hugo keys above `[minify]`, leaving only `minifyOutput` in the minify table. Retain the configured six languages and all content. Add a build-time sitemap assertion that taxonomy/term URLs never reappear.

**Expected effect:** Remove the two unintended taxonomy endpoints per locale; no useful article, profile, or section page is deleted. Expected sitemap count after the fix is 59 URLs per locale (354 total), subject to the production build output and CI confirmation.

### P1 — Repeated generic expert-analysis block on all slot pages

**Evidence:** `layouts/partials/slot-profile-expert-analysis.html` is a 30,988-character partial with six language branches. Each branch repeats the same broad explanations of RTP, volatility, game rules, bonus triggers, paytables, mobile usability, FAQs and gambling risk, with only game name, provider, summary and feature label interpolated. The partial is invoked for every page whose `translationKey` starts with `slot-profile-`. That produces a substantial common text block across 210 localized pages and obscures the individual material written in each profile.

**Resolution:** Shorten the shared block to a concise, localized data summary and version-verification note, while leaving each existing game profile, feature table, game-specific mechanic text, images and navigation intact. Do not add facts or RTP values.

**Remaining editorial work:** A short template cannot substitute for title-by-title fact checking. Each provider, mechanic, RTP configuration, volatility label and stake range must still be verified against the actual game version and a documented source before presenting it as a current fact.

### P1 — Translation defects exist in profile content

**Evidence:** The Polish Starburst profile contains the unnatural phrase “Slot inspirowany motywem kosmos i kolorowe klejnoty”; the Portuguese equivalent contains “Um slot inspirado em o espaço”. The English, Japanese and German versions have more natural phrasing. The slot catalogue maintains six localized descriptions and keywords, but source metadata/body copy is not consistently aligned.

**Resolution:** Correct these two localized Starburst descriptions in the profile source. Other locale QA remains a broader native-speaker editorial task; automated coverage cannot certify translation quality.

### P1 — Editorial verification remains incomplete despite indexable status

**Evidence:** Many public content pages, including slot profiles and slot guides, carry `article_review_status: editorial-review-pending`. The editorial review registry (`data/site/reviews.yaml`) has `status: pending_source_verification` and an empty `sources` array. The source registry has owner-confirmed status, but several operational data entries have no primary URL or verification date. The rendered slot profile's factual attributes are partly drawn from the catalogue.

**Resolution:** Keep the public site crawlable; do not apply a global `noindex`. Do not invent review scores, testimonials, RTP values, sources, author testing or author approval. Treat source verification and content approval as explicit remaining publication-quality tasks.

### P1 — Sitemap and section-route hygiene needs continued attention

**Evidence:** The six-language sitemap index is correctly present and each language sitemap reports 61 URLs. Besides taxonomy stubs, the sitemap includes `/editorial/`, a rendered section page whose body is an internal “Site settings” listing, and `/slot-profiles/`, which is a navigable directory of the 35 profile pages. The latter has user value and should not be removed automatically; the editorial settings section is low-value and should be excluded deliberately after confirming the Hugo section behavior.

**Resolution:** This change removes the proven taxonomy stubs. The `/editorial/` section route is recorded for follow-up; do not remove or rename the underlying localized settings records because templates read them through `site.GetPage`.

### P2 — Multilingual canonical and hreflang

**Production result:** Sampled German, English and Japanese Starburst pages each have one self-referential canonical. Their `hreflang` sets include de, en, pl, es, pt, ja, and x-default; x-default points to the German profile URL. The current template emits the current page as one of the entries via `.AllTranslations`. No change is needed to this behavior. The homepage and sampled profile metadata have localized title and description values.

### P2 — robots.txt and tracking paths

**Production result:** Production `/robots.txt` allows `/`, disallows `/go/`, and references the sitemap index. The tracking/redirect routes have separate noindex response-header policy in `static/_headers`. Do not submit or index tracking URLs.

### P2 — Structured data and metadata

**Source review:** `head.html` emits localized title, description, canonical, robots, Open Graph, Twitter metadata, alternate-language links and JSON-LD. Review and aggregate ratings are gated on verification fields; `data/site/reviews.yaml` currently has no evidence records, so no rating should be fabricated. A complete JSON-LD validator/Google rich-results test has not been run.

### P2 — Performance, mobile and HTTP

The source includes responsive CSS, image dimensions, lazy loading for below-the-fold imagery, high fetch priority for the homepage hero, and a Playwright mobile smoke suite. No Lighthouse/PageSpeed/Core Web Vitals lab or field data was available in this audit. Browser automation and full response-header checks remain CI/deployment validation items. A production fetch of the sampled legacy path `/de/slot-profiles/starburst/` returned 404; the canonical profile route is `/slots/starburst/` for German and `/en/slots/starburst/`, `/ja/slots/starburst/` for translated pages. No redirect should be created for an unconfirmed legacy path.

## Baseline sitemap counts

| Locale | Sitemap URL | URLs before remediation |
|---|---|---:|
| German (de) | `/de/sitemap.xml` | 61 |
| English (en) | `/en/sitemap.xml` | 61 |
| Polish (pl) | `/pl/sitemap.xml` | 61 |
| Spanish (es) | `/es/sitemap.xml` | 61 |
| Portuguese (pt) | `/pt/sitemap.xml` | 61 |
| Japanese (ja) | `/ja/sitemap.xml` | 61 |
| **Total** | **6 child sitemaps** | **366** |

The 366 entries are unique locale-specific URLs in the live sitemap set as observed. Twelve entries are the two thin taxonomy routes repeated across six locales. The planned post-fix count is 59 per locale and 354 total; the build-time checks must confirm the actual generated result.

## Prioritized remediation plan

1. Correct the TOML table scope so `disableKinds = ['taxonomy','term']` is truly top-level.
2. Add generated-output tests for sitemap contents, canonical links, localized hreflang, x-default, robots and URL uniqueness.
3. Reduce the long repeated expert-analysis template; preserve the existing standalone profiles and all six language trees.
4. Correct demonstrated Polish and Portuguese wording and continue the 210-page native-speaker/source audit as a separate editorial task.
5. Review `/editorial/` section output and legacy route handling; retain useful directory and profile pages.
6. Run production Hugo build, existing static checks, sitemap validation, browser/mobile CI, and production smoke checks. Use Search Console only when authorized access is available.

## Explicit limitations

- Google indexing is not confirmed. No Search Console access or inspection data was provided.
- Live RTP, volatility, stake range, payout limits, bonus terms, legal availability and payment details cannot be certified from the current repository alone.
- Translation fluency for every paragraph cannot be certified by automated checks.
- Core Web Vitals and real-device network performance require PageSpeed/CrUX or a browser measurement environment.
- Production origin response status/headers were directly confirmed only for sampled routes; this is not a 366-URL HTTP crawl.
