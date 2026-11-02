# SEO implementation report — Instant Casino

Дата: 2026-11-02  
Репозиторий: https://github.com/ilyaivanov17/instant-casino  
Ветка: `seo/fix-indexing-hreflang-2026-11`  
Целевая ветка: `main`  
Pull Request: https://github.com/ilyaivanov17/instant-casino/pull/43  
Итоговый commit с отчётом: `a065975f106d406c4b4030709833358a5429e14e`

## Итог

В PR исправлена подтверждённая ошибка области видимости параметров Hugo, из-за которой `disableKinds = ['taxonomy','term']` не работал как корневая настройка. Из sitemap исключены пустые taxonomy-маршруты `/categories/` и `/tags/`, а также служебный раздел `/editorial/`; исходные записи настроек сохранены. Добавлены проверки sitemap и метаданных уже после генерации HTML. Уменьшен общий повторяющийся текст в шаблоне профилей слотов, исправлены две проверенные ошибки перевода.

**GitHub Actions для итогового PR-коммита завершился успешно.** Hugo Extended 0.169.0 собрал production output, проверки SEO и sitemap прошли, Playwright mobile smoke tests прошли, артефакт production-сборки был загружен.

PR оставлен открытым для review. Он не смержен в `main`; текущий production-сайт не обновлён этим PR до его принятия и последующего deployment. Результат сборки PR не означает, что Google уже проиндексировал страницы.

## 1. Выполненные этапы

| Этап | Статус | Выполненная работа и границы |
|---|---|---|
| 0. Аудит | Выполнен в пределах доступных данных | Изучены конфигурация Hugo, все шесть языковых деревьев, каталог игр, шаблоны SEO, скрипты QA, GitHub Actions и опубликованные production-маршруты. Создан `SEO-AUDIT-REPORT.md`. |
| 1. Техническая SEO-структура | Основная подтверждённая проблема исправлена | Исправлена TOML-область `disableKinds`; выключены taxonomy/term kinds. Служебный `/editorial/` исключён из output. Проверяются шесть sitemap, URL, canonical, robots, hreflang и x-default. |
| 2. Профили игровых автоматов | Частично выполнен | Проверены наличие 35 профилей × 6 языков (210 исходных страниц) и повторяемость общего шаблона. Общий блок сокращён с 30 988 до 2 470 символов. Исправлены польский и португальский тексты Starburst. Полная проверка фактов для каждого из 35 игр не выполнена: для неё нужны источники и проверка конкретной версии каждой игры. |
| 3. Экспертные статьи | Аудит и фиксация ограничений | Проверены документы прежнего editorial QA и выборочные содержательные страницы. Массовая перепись и подтверждение каждого факта не выполнялись: это создало бы риск выдумывания RTP, бонусных правил, платёжных сведений и юридических утверждений. |
| 4. Шесть языковых версий | Автоматическая структурная проверка выполнена; редакторская — частично | Проверены шесть локалей, 57 логических групп страниц без отсутствующих языковых файлов и 210 профилей слотов. Исправлены два конкретных дефекта польского/португальского Starburst. Автоматические тесты не подтверждают качество носительского перевода всех абзацев. |
| 5. Внутренняя перелинковка | Статическая проверка выполнена | Существующий `seo-audit.py` проверил relref-цели. Мобильные тесты подтвердили 35 ссылок на профили и успешные профильные маршруты в каждом из шести каталогов. Полный HTTP crawl всех production URL после deployment ещё нужен. |
| 6. Метаданные и schema | Автоматическая проверка основных SEO-метаданных выполнена | Для всех URL в сгенерированных sitemap проверены title, description, единственный canonical, robots, все шесть hreflang, self-reference и x-default. Playwright-проверка локализованных профилей проверила Article JSON-LD и автора. Отдельная внешняя валидация всех schema.org типов и Google Rich Results не проводилась. |
| 7. Производительность и Googlebot | Частично проверено | Проверена адаптивная работа существующего сайта в Chromium на 390 и 1440 px, загрузка изображений и отсутствие JS ошибок в smoke tests. Данных PageSpeed Insights, CrUX и Search Console нет; Core Web Vitals нельзя объявить измеренными. |
| 8. Финальная проверка и PR | Выполнен | Hugo production build, все доступные статические проверки, sitemap, rendered SEO, output safety, мобильные и браузерные тесты прошли в итоговом GitHub Actions run. PR #43 открыт в `main`. |

## 2. Исправления и файлы

Всего в PR изменено или добавлено 18 файлов:

1. `.github/workflows/hugo-production.yml` — добавлена проверка сгенерированных canonical/hreflang метаданных.
2. `hugo.toml` — корневые параметры Hugo перенесены выше `[minify]`; `disableKinds` теперь действительно находится на корневом уровне.
3. `layouts/partials/slot-profile-expert-analysis.html` — удалены длинные повторяющиеся универсальные объяснения; оставлена краткая локализованная сводка по данным каталога и указание проверять правила активной версии.
4. `scripts/check-sitemap.py` — проверяются ровно шесть локальных sitemap, уникальность HTTPS URL, язык child sitemap и отсутствие `categories`, `tags`, `editorial` в путях.
5. `scripts/check-rendered-seo.py` — новый аудит HTML, связанный с реальным sitemap output.
6. `scripts/check-all.sh` — новая rendered SEO-проверка включена в общий QA.
7. `scripts/build-production.sh` — после Hugo build выполняется проверка sitemap и metadata.
8. `tests/mobile-smoke.cjs` — проверка профиля приведена в соответствие с намеренно коротким общим шаблоном; сохраняются проверки имени игры, автора, metadata и Article JSON-LD.
9. `content/de/editorial/_index.md`
10. `content/en/editorial/_index.md`
11. `content/pl/editorial/_index.md`
12. `content/es/editorial/_index.md`
13. `content/pt/editorial/_index.md`
14. `content/ja/editorial/_index.md` — эти шесть файлов отключают вывод внутреннего раздела `/editorial/`; исходные `editorial/settings.md` сохранены и продолжают использоваться шаблонами.
15. `content/pl/slot-profiles/starburst.md` — исправлены польское описание и фразы о механике.
16. `content/pt/slot-profiles/starburst.md` — исправлены португальское описание и фразы о механике.
17. `SEO-AUDIT-REPORT.md` — технический аудит и исходные доказательства.
18. `SEO-IMPLEMENTATION-REPORT.md` — этот итоговый отчёт.

Полезные страницы, игровые карточки, авторские данные, изображения, URL, все шесть языковых каталогов и `/slot-profiles/` сохранены. Профильный список `/slot-profiles/` оставлен, потому что на production он реально содержит ссылки на 35 профилей. Неизвестные legacy URL автоматически не перенаправлялись.

## 3. Sitemap и индексируемые URL

### До исправлений — production crawl 2026-11-02

| Язык | URL в sitemap |
|---|---:|
| de | 61 |
| en | 61 |
| pl | 61 |
| es | 61 |
| pt | 61 |
| ja | 61 |
| **Всего** | **366** |

В этих списках находились `/categories/` и `/tags/` для каждой из шести локалей, а также служебный `/editorial/`.

### После исправлений — итоговый Hugo production build в GitHub Actions

| Язык | URL в sitemap |
|---|---:|
| de | 58 |
| en | 58 |
| pl | 58 |
| es | 58 |
| pt | 58 |
| ja | 58 |
| **Всего** | **348** |

Результат итогового CI:

- шесть child sitemap присутствуют в sitemap index;
- 58 URL в каждой локали;
- 348 уникальных HTTPS URL суммарно;
- отсутствуют taxonomy и служебные editorial-маршруты;
- каждый URL из sitemap соответствует сгенерированному HTML;
- canonical каждой страницы равен URL в sitemap;
- отсутствуют пустые/повторные canonical, случайный `noindex` на URL из sitemap и дубли hreflang;
- каждая страница содержит de/en/pl/es/pt/ja hreflang, включая самоссылочную альтернативу;
- `x-default` указывает на немецкий эквивалент;
- все hreflang-цели находятся в итоговом наборе sitemap.

**348 — количество уникальных URL, включённых в sitemap generated build, а не подтверждённое количество URL в индексе Google.** После merge и публикации нужно повторить production crawl: текущий live сайт не изменился автоматически от открытия PR.

## 4. Результаты автоматических проверок

Итоговый GitHub Actions run:

https://github.com/ilyaivanov17/instant-casino/actions/runs/41432576317

Версия Hugo: `0.169.0-1da10fc44701c566b1669cdb2d12638f155138bd+extended`.

| Проверка | Результат |
|---|---|
| `scripts/check-site.py` | PASS — 57 логических групп × 6 локалей |
| `scripts/check-slot-profiles.py` | PASS — 35 standalone профилей × 6 локалей = 210 страниц |
| `scripts/check-bonuses.py` | PASS — 3 бонусные записи проверены; статус верификации автоматически не предполагается |
| `scripts/seo-audit.py` | PASS — статический аудит; не заменяет проверку опубликованного сайта |
| `scripts/language-coverage.py` | PASS — 57 групп, отсутствующие языковые файлы: 0, точные дубли немецкого body: 0 |
| `scripts/check-locales.py` | PASS — кириллический текст в публичных исходниках не обнаружен |
| Hugo production build | PASS |
| `scripts/check-sitemap.py` | PASS — 6 child sitemap, 348 уникальных URL, по 58 на язык |
| `scripts/check-rendered-seo.py` | PASS — 348 HTML страниц проверены |
| `scripts/check-public-output.sh public` | PASS |
| Playwright mobile/browser smoke tests | PASS |
| Загрузка production artifact | PASS — `instant-casino-public`, 17 892 250 bytes |

В мобильных тестах на ширине 390 px каждый из шести каталогов вернул 35 карточек, 35/35 загруженных изображений, 35 ссылок на профили и 35 доступных профильных маршрутов. Также проверены поисковый интерфейс каталога, responsive header, бонусный калькулятор и отсутствие JavaScript ошибок на проверенных страницах. Для локализованных каталогов en/pl/es/pt/ja успешно проверены калькулятор, профиль Bonanza, canonical, hreflang, авторские metadata и Article schema.

### Исправленная регрессия теста

Первый PR run выявил несоответствие существующего Playwright-теста новому намеренному короткому шаблону: тест требовал более 1 800 символов общего expert-блока. Это требование поддерживало прежнее дублирование текста, поэтому проверка была исправлена на наличие краткой игры-специфичной справки и сохранность автора, keywords, Article JSON-LD и canonical. Повторный run прошёл; итоговый run также завершился успешно. Это была ошибка устаревшего тестового ожидания, а не проблема Hugo или переведённых страниц.

## 5. Коммиты

Все коммиты сделаны в feature-ветке, без force push и без изменения истории `main`.

1. [9231bf0](https://github.com/ilyaivanov17/instant-casino/commit/9231bf0dfbf83f33993eaddb6be212fe5b81f6b2) — audit report.
2. [78ef641](https://github.com/ilyaivanov17/instant-casino/commit/78ef6416efc3776b9fb93bfe3620aab025d2aa5a) — корректная область `disableKinds`.
3. [5ed5728](https://github.com/ilyaivanov17/instant-casino/commit/5ed57280519858d71254806c14748b0d5e961a35) — sitemap locale/taxonomy validation.
4. [5b9be51](https://github.com/ilyaivanov17/instant-casino/commit/5b9be511d7948cb5a92a665cadecf80f7a820716) — rendered SEO test.
5. [f7e360a](https://github.com/ilyaivanov17/instant-casino/commit/f7e360a5306ad288aab96aa7879bc50599ec138a) — сохранение действующего image path.
6. [ab8eba8](https://github.com/ilyaivanov17/instant-casino/commit/ab8eba8ecaf9e2713007331f29740b3effcb5b8a) — точная self-hreflang/x-default проверка.
7. [d06973e](https://github.com/ilyaivanov17/instant-casino/commit/d06973ecb69c48eebcba4c866e714a96652d59bc) — интеграция SEO-проверки в общий QA.
8. [f9e3f68](https://github.com/ilyaivanov17/instant-casino/commit/f9e3f68a45125324aeb35ce6245980dd7733f31e) — проверки в production build.
9. [9a4bc05](https://github.com/ilyaivanov17/instant-casino/commit/9a4bc058a6b9a1613d53e5f85ef2c2168a471e28) — GitHub Actions.
10. [a529996](https://github.com/ilyaivanov17/instant-casino/commit/a5299966c058ee36cd570722003bcd036b558cb3) — сокращение повторяющегося slot analysis.
11. [e5abd9a](https://github.com/ilyaivanov17/instant-casino/commit/e5abd9a56d796bd054d1cc293005a66ddae3de89) — польская локализация Starburst.
12. [39e82be](https://github.com/ilyaivanov17/instant-casino/commit/39e82bed24a7bdf88ce113ec14248290b93c90e5) — португальская локализация Starburst.
13. [e520b47](https://github.com/ilyaivanov17/instant-casino/commit/e520b47367dee4e7204b59f2502d34182d28cdd0) — исправление устаревшего ожидания mobile test.
14. [0efb6c5](https://github.com/ilyaivanov17/instant-casino/commit/0efb6c5f0fe50d62cac4ddadda6a33a4164d8273) — исключение внутреннего editorial section (de).
15. [36bb252](https://github.com/ilyaivanov17/instant-casino/commit/36bb2526927c24fb079c9cc835ef375a0e0df588) — editorial section (en).
16. [73b8f12](https://github.com/ilyaivanov17/instant-casino/commit/73b8f12de001f4774a4be522bb1de6e9b93c7da6) — editorial section (pl).
17. [6595aab](https://github.com/ilyaivanov17/instant-casino/commit/6595aabf2811ab3adf5d24cd64a72da5da3177c2) — editorial section (es).
18. [ae65abc](https://github.com/ilyaivanov17/instant-casino/commit/ae65abc73bdc8f0f7aaf8934c05be429f2b9ff33) — editorial section (pt).
19. [bcdfe6c](https://github.com/ilyaivanov17/instant-casino/commit/bcdfe6c10f48735f5a9867314a44c61af22c290f) — editorial section (ja).
20. [fb0b8f6](https://github.com/ilyaivanov17/instant-casino/commit/fb0b8f6517e7db44fdeaa0ea74f6702a4b8dc261) — запрет editorial route в sitemap QA.
21. [448bdd4](https://github.com/ilyaivanov17/instant-casino/commit/448bdd467c53263036c8786abfea2a9291b555c8) — обновление итогового аудита.
22. [a065975](https://github.com/ilyaivanov17/instant-casino/commit/a065975f106d406c4b4030709833358a5429e14e) — итоговый отчёт реализации.

## 6. Оставшиеся задачи и ограничения

1. **Фактические характеристики 35 игр.** Для каждой игры и каждой применимой версии нужно документировать первичный источник для RTP, волатильности, диапазона ставок, бонусных триггеров и выплат. Репозиторий содержит каталог игровых данных, но доступные исходники не предоставляют достаточную проверяемую цепочку источников для безопасной массовой корректировки всех значений.
2. **Полная содержательная уникальность 210 профилей.** Удалён длинный универсальный шаблон, но это не заменяет отдельное редакторское исследование всех 35 игр в каждой локали. Нужна проверка уникальной механики по названию игры и сверка с help/paytable фактической версии.
3. **Статьи и руководства.** Для всех 57 групп страниц нужна отдельная редакторская проверка полноты темы, первичных источников, актуальности и независимости текста. Статический QA подтверждает структуру и отсутствие пропущенных языковых файлов, но не доказывает экспертность статьи.
4. **Носительская языковая проверка.** Исправлены только два конкретных дефекта перевода Starburst. Полная языковая вычитка немецкого, английского, польского, испанского, португальского и японского текстов не заменяется автоматическим скриптом.
5. **Производительность.** Не было доступа к подтверждённым полевым данным CrUX/Search Console и полноценному PageSpeed/Lighthouse прогону. Core Web Vitals не объявляются измеренными.
6. **Полный live HTTP crawl.** В ходе аудита непосредственно проверены robots.txt, sitemap index/child sitemaps, главная, категории/теги, профильные и разделы-примеры. Проверка всех 348 URL по HTTP status и заголовкам после фактического deployment остаётся обязательным post-deploy шагом.
7. **Search Console.** Доступа к отчётам Indexing, Crawl Stats, URL Inspection и sitemap processing не было. Индексация Google не подтверждена.

## 7. Рекомендации после принятия PR

1. Принять PR и дождаться завершения обычного deployment pipeline.
2. После deployment повторно проверить `/robots.txt`, корневой sitemap index и все шесть языковых sitemap; ожидается 58 URL в каждой локали.
3. Выполнить HTTP crawl sitemap URL с фиксацией response code, canonical, robots header/meta и языкового набора hreflang. Проверить, что прежние `/categories/`, `/tags/` и `/editorial/` больше не отдаются как индексируемые страницы.
4. В Search Console проверить обработку sitemap, Page indexing, Duplicate/Google chose different canonical, Crawled/Discovered — currently not indexed и Crawl Stats. Не делать массовую отправку URL.
5. Поставить редакторскую верификацию RTP/игровых функций/платежей/бонусов и юридических утверждений в отдельный review workflow с первичным источником и датой проверки.
6. Отслеживать CWV по CrUX/PageSpeed и отдельно проверить мобильные LCP/INP/CLS на реальном production-трафике.

## 8. Статус PR и публикации

- PR: https://github.com/ilyaivanov17/instant-casino/pull/43
- Target: `main`
- Branch: `seo/fix-indexing-hreflang-2026-11`
- Итоговый проверенный commit: `a065975f106d406c4b4030709833358a5429e14e`
- Итоговый GitHub Actions run: https://github.com/ilyaivanov17/instant-casino/actions/runs/41432576317 — **success**
- PR открыт, не смержен.
- Production-деплой этим действием не выполнялся.
- Индексация Google не заявляется и должна подтверждаться только через Search Console.
