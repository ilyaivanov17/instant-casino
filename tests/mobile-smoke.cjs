const { chromium } = require('playwright');

const slotRoutes = [
  '/slots/',
  '/en/slots/',
  '/pl/slots/',
  '/es/slots/',
  '/pt/slots/',
  '/ja/slots/'
];

async function inspectPage(page, path, expectedCards = null) {
  const errors = [];
  page.on('pageerror', error => errors.push(error.message));
  const response = await page.goto(`http://127.0.0.1:4173${path}`, { waitUntil: 'networkidle' });
  const result = await page.evaluate(async () => {
    const cards = [...document.querySelectorAll('.slot-game-card')];
    const images = cards.map(card => card.querySelector('img')).filter(Boolean);

    await Promise.all(images.map(async image => {
      image.loading = 'eager';
      try { await image.decode(); } catch (_) { /* reported below */ }
    }));

    const anchors = cards.map(card => {
      const link = card.querySelector('a[href*="#"]');
      if (!link) return false;
      const target = new URL(link.href).hash;
      return Boolean(target && document.getElementById(decodeURIComponent(target.slice(1))));
    });

    return {
      width: document.documentElement.clientWidth,
      scrollWidth: document.documentElement.scrollWidth,
      title: document.title,
      cards: cards.length,
      images: images.map(image => ({
        alt: image.alt.trim(),
        loaded: image.complete && image.naturalWidth > 0
      })),
      anchors,
      columns: getComputedStyle(document.querySelector('.slots-catalog-grid') || document.body)
        .gridTemplateColumns.split(' ').filter(Boolean).length
    };
  });

  const galleryOk = expectedCards === null || (
    result.cards === expectedCards &&
    result.images.length === expectedCards &&
    result.images.every(image => image.alt.length > 0 && image.loaded) &&
    result.anchors.length === expectedCards &&
    result.anchors.every(Boolean)
  );
  const ok = Boolean(response) &&
    response.status() === 200 &&
    result.title &&
    result.scrollWidth <= result.width + 1 &&
    errors.length === 0 &&
    galleryOk;

  console.log(`${ok ? 'OK' : 'FAIL'} ${path} status=${response?.status()} viewport=${result.width}/${result.scrollWidth} cards=${result.cards} images=${result.images.filter(image => image.loaded).length}/${result.images.length} links=${result.anchors.filter(Boolean).length}/${result.anchors.length} jsErrors=${errors.length}`);
  return { ok, result };
}

(async () => {
  const browser = await chromium.launch({ headless: true });
  let failed = false;

  for (const path of ['/', '/es/', '/pt/', '/pl/', '/ja/', '/bonuses/']) {
    const page = await browser.newPage({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 1 });
    const check = await inspectPage(page, path);
    if (!check.ok) failed = true;
    await page.close();
  }

  for (const path of slotRoutes) {
    const page = await browser.newPage({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 1 });
    const check = await inspectPage(page, path, 30);
    if (!check.ok) failed = true;
    await page.close();
  }

  // Exercise catalogue search against real catalogue entries and reset behaviour.
  const searchPage = await browser.newPage({ viewport: { width: 1280, height: 900 }, deviceScaleFactor: 1 });
  await searchPage.goto('http://127.0.0.1:4173/en/slots/', { waitUntil: 'networkidle' });
  const search = searchPage.locator('#slot-catalog-search');
  await search.fill('Bigger Bass Bonanza');
  const titleMatches = await searchPage.locator('.slot-game-card:visible').count();
  const firstTitle = await searchPage.locator('.slot-game-card:visible h3').first().textContent();
  await search.fill('Bigger Bass');
  const multiWordMatches = await searchPage.locator('.slot-game-card:visible').count();
  await search.fill('Biger Bass Bonanza');
  const typoMatches = await searchPage.locator('.slot-game-card:visible').count();
  const typoFirstTitle = await searchPage.locator('.slot-game-card:visible h3').first().textContent();
  // Search metadata written in another locale.
  await search.fill('frutas de colores');
  const crossLanguageMatches = await searchPage.locator('.slot-game-card:visible').count();
  const crossLanguageTitle = await searchPage.locator('.slot-game-card:visible h3').first().textContent();
  // Search a phrase that appears in the game description, not the title/provider.
  await search.fill('gold mining theme');
  const descriptionMatches = await searchPage.locator('.slot-game-card:visible').count();
  const descriptionMatchTitle = await searchPage.locator('.slot-game-card:visible h3').first().textContent();
  // Longer editorial/profile text must not be searchable.
  await search.fill('variable number of symbol positions');
  const longTextMatches = await searchPage.locator('.slot-game-card:visible').count();
  await search.fill('Pragmatic Play');
  const providerMatches = await searchPage.locator('.slot-game-card:visible').count();
  await search.fill('no-such-game-123');
  const emptyStateVisible = await searchPage.locator('#slot-catalog-empty').isVisible();
  await searchPage.locator('#slot-catalog-clear').click();
  const restoredCount = await searchPage.locator('.slot-game-card:visible').count();
  const searchOk = titleMatches === 1 && firstTitle.trim() === 'Bigger Bass Bonanza' &&
    multiWordMatches === 1 && typoMatches === 1 && typoFirstTitle.trim() === 'Bigger Bass Bonanza' &&
    crossLanguageMatches > 0 && crossLanguageTitle.trim() === 'Fruit Party' &&
    descriptionMatches === 1 && descriptionMatchTitle.trim() === 'Bonanza' &&
    longTextMatches === 0 && providerMatches > 0 && emptyStateVisible && restoredCount === 30;
  console.log(`${searchOk ? 'OK' : 'FAIL'} catalogue search title=${titleMatches} multiword=${multiWordMatches} typo=${typoMatches} crossLanguage=${crossLanguageMatches} description=${descriptionMatches} (${descriptionMatchTitle?.trim()}) longText=${longTextMatches} provider=${providerMatches} empty=${emptyStateVisible} reset=${restoredCount}/30`);
  if (!searchOk) failed = true;
  await searchPage.close();

  // Check the redesigned search control at narrow mobile and desktop widths.
  const mobileSearchPage = await browser.newPage({ viewport: { width: 360, height: 780 }, deviceScaleFactor: 1, isMobile: true, hasTouch: true });
  await mobileSearchPage.goto('http://127.0.0.1:4173/slots/', { waitUntil: 'networkidle' });
  const mobileSearchMetrics = await mobileSearchPage.locator('.slot-search-panel').evaluate(panel => {
    const field = panel.querySelector('.slot-search-field');
    const input = panel.querySelector('#slot-catalog-search');
    const panelRect = panel.getBoundingClientRect();
    const fieldRect = field.getBoundingClientRect();
    return {
      panelWidth: panelRect.width,
      panelRight: panelRect.right,
      fieldWidth: fieldRect.width,
      fieldHeight: fieldRect.height,
      inputFontSize: parseFloat(getComputedStyle(input).fontSize),
      visibleLabel: Boolean(panel.querySelector('.slot-search-label-title')?.textContent.trim())
    };
  });
  const mobileSearchOk = mobileSearchMetrics.panelRight <= 360 && mobileSearchMetrics.fieldWidth > 280 &&
    mobileSearchMetrics.fieldHeight >= 54 && mobileSearchMetrics.inputFontSize >= 16 && mobileSearchMetrics.visibleLabel;
  console.log(`${mobileSearchOk ? 'OK' : 'FAIL'} mobile search panel width=${mobileSearchMetrics.panelWidth.toFixed(1)} field=${mobileSearchMetrics.fieldWidth.toFixed(1)}x${mobileSearchMetrics.fieldHeight.toFixed(1)} font=${mobileSearchMetrics.inputFontSize}px`);
  if (!mobileSearchOk) failed = true;
  await mobileSearchPage.close();

  const desktopSearchPage = await browser.newPage({ viewport: { width: 1440, height: 900 }, deviceScaleFactor: 1 });
  await desktopSearchPage.goto('http://127.0.0.1:4173/slots/', { waitUntil: 'networkidle' });
  const desktopSearchMetrics = await desktopSearchPage.locator('.slot-search-panel').evaluate(panel => {
    const rect = panel.getBoundingClientRect();
    const field = panel.querySelector('.slot-search-field').getBoundingClientRect();
    return { panelWidth: rect.width, fieldWidth: field.width, fieldHeight: field.height };
  });
  const desktopSearchOk = desktopSearchMetrics.panelWidth >= 500 && desktopSearchMetrics.fieldWidth >= 450 && desktopSearchMetrics.fieldHeight >= 58;
  console.log(`${desktopSearchOk ? 'OK' : 'FAIL'} desktop search panel width=${desktopSearchMetrics.panelWidth.toFixed(1)} field=${desktopSearchMetrics.fieldWidth.toFixed(1)}x${desktopSearchMetrics.fieldHeight.toFixed(1)}`);
  if (!desktopSearchOk) failed = true;
  await desktopSearchPage.close();

  // Check the intended four-column desktop layout on the German catalogue.
  const desktop = await browser.newPage({ viewport: { width: 1440, height: 1000 }, deviceScaleFactor: 1 });
  const desktopCheck = await inspectPage(desktop, '/slots/', 30);
  if (!desktopCheck.ok || desktopCheck.result.columns !== 4) {
    console.log(`FAIL /slots/ desktop columns=${desktopCheck.result.columns}, expected=4`);
    failed = true;
  }
  await desktop.close();

  await browser.close();
  if (failed) process.exit(1);
})().catch(error => { console.error(error); process.exit(1); });
