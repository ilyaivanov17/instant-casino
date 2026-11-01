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
      const link = card.querySelector('.slot-game-card-link');
      if (!link) return false;
      const segments = new URL(link.href).pathname.split('/').filter(Boolean);
      return segments.length >= 2 && segments[segments.length - 2] === 'slots';
    });
    const profileStatuses = await Promise.all(cards.map(async card => {
      const link = card.querySelector('.slot-game-card-link');
      try {
        const response = await fetch(link.href);
        return response.status;
      } catch (_) {
        return 0;
      }
    }));

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
      profileStatuses,
      tables: [...document.querySelectorAll('.table-scroll-container')].map(container => ({
        clientWidth: container.clientWidth,
        scrollWidth: container.scrollWidth,
        hasTable: Boolean(container.querySelector('table')),
        headers: container.querySelectorAll('th').length,
        cells: container.querySelectorAll('td').length,
        sample: container.querySelector('table')?.outerHTML.slice(0, 500) || ''
      })),
      columns: getComputedStyle(document.querySelector('.slots-catalog-grid') || document.body)
        .gridTemplateColumns.split(' ').filter(Boolean).length,
      cardLayout: (() => {
        const link = document.querySelector('.slot-game-card-link');
        const art = document.querySelector('.slot-game-card-art');
        const artRect = art?.getBoundingClientRect();
        const card = document.querySelector('.slot-game-card');
        return {
          direction: link ? getComputedStyle(link).flexDirection : 'missing',
          artRatio: artRect?.height ? artRect.width / artRect.height : 0,
          cardWidth: card?.getBoundingClientRect().width || 0
        };
      })()
    };
  });

  const galleryOk = expectedCards === null || (
    result.cards === expectedCards &&
    result.images.length === expectedCards &&
    result.images.every(image => image.alt.length > 0 && image.loaded) &&
    result.anchors.length === expectedCards &&
    result.anchors.every(Boolean) &&
    result.profileStatuses.length === expectedCards &&
    result.profileStatuses.every(status => status === 200)
  );
  const tableStructureOk = expectedCards === null || result.tables.length === 0;
  const ok = Boolean(response) &&
    response.status() === 200 &&
    result.title &&
    result.scrollWidth <= result.width + 1 &&
    errors.length === 0 &&
    galleryOk &&
    tableStructureOk;

  if (!ok) console.log(`  diagnostics ${path}: title=${Boolean(result.title)} pageOverflow=${result.scrollWidth > result.width + 1} galleryOk=${galleryOk} tableStructureOk=${tableStructureOk} profileRoutes=${result.profileStatuses.filter(status => status === 200).length}/${result.profileStatuses.length} tableHeaders=${Math.max(0, ...result.tables.map(table => table.headers))} tableCells=${Math.max(0, ...result.tables.map(table => table.cells))} tableSample=${JSON.stringify(result.tables[0]?.sample || '')} tableWrappers=${result.tables.length} tablesWithContent=${result.tables.filter(table => table.headers > 0 && table.cells > 0).length}`);
  console.log(`${ok ? 'OK' : 'FAIL'} ${path} status=${response?.status()} viewport=${result.width}/${result.scrollWidth} cards=${result.cards} images=${result.images.filter(image => image.loaded).length}/${result.images.length} profileLinks=${result.anchors.filter(Boolean).length}/${result.anchors.length} profileRoutes=${result.profileStatuses.filter(status => status === 200).length}/${result.profileStatuses.length} tables=${result.tables.length} tableScroll=${result.tables.filter(table => table.scrollWidth > table.clientWidth + 1).length} jsErrors=${errors.length}`);
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
    const check = await inspectPage(page, path, 35);
    if (!check.ok) failed = true;
    await page.close();
  }

  // Header direction behavior: verify the real on-screen position, not only its CSS class.
  async function readHeaderVisibility(page) {
    return page.locator('.lobby-header').evaluate(el => {
      const rect = el.getBoundingClientRect();
      const style = getComputedStyle(el);
      return {
        top: rect.top,
        bottom: rect.bottom,
        height: rect.height,
        visibility: style.visibility,
        display: style.display,
        visible: style.display !== 'none' && style.visibility !== 'hidden' &&
          rect.bottom > 0 && rect.top < window.innerHeight
      };
    });
  }
  async function scrollInSmallSteps(page, distance, step) {
    const count = Math.ceil(Math.abs(distance) / step);
    const direction = distance > 0 ? 1 : -1;
    for (let i = 0; i < count; i++) {
      await page.evaluate(delta => window.scrollBy(0, delta), direction * step);
      await page.evaluate(() => new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve))));
    }
  }

  const headerPage = await browser.newPage({ viewport: { width: 1280, height: 900 } });
  await headerPage.goto('http://127.0.0.1:4173/slots/', { waitUntil: 'networkidle' });
  await scrollInSmallSteps(headerPage, 650, 20);
  await headerPage.waitForTimeout(300);
  const desktopHidden = await readHeaderVisibility(headerPage);
  await scrollInSmallSteps(headerPage, -80, 3);
  await headerPage.waitForTimeout(300);
  const desktopRevealed = await readHeaderVisibility(headerPage);
  const desktopHeaderOk = !desktopHidden.visible && desktopRevealed.visible && desktopRevealed.top >= -2;
  console.log(`${desktopHeaderOk ? 'OK' : 'FAIL'} desktop header down/up hidden=${!desktopHidden.visible} revealed=${desktopRevealed.visible} top=${desktopRevealed.top.toFixed(1)}px`);
  if (!desktopHeaderOk) failed = true;
  await headerPage.close();

  // Mobile: several 3px upward deltas must accumulate and reveal the actual header.
  const mobileHeaderPage = await browser.newPage({
    viewport: { width: 390, height: 844 }, deviceScaleFactor: 1, isMobile: true, hasTouch: true
  });
  await mobileHeaderPage.goto('http://127.0.0.1:4173/slots/', { waitUntil: 'networkidle' });
  await scrollInSmallSteps(mobileHeaderPage, 520, 12);
  await mobileHeaderPage.waitForTimeout(300);
  const mobileHidden = await readHeaderVisibility(mobileHeaderPage);
  await scrollInSmallSteps(mobileHeaderPage, -60, 3);
  await mobileHeaderPage.waitForTimeout(300);
  const mobileRevealed = await readHeaderVisibility(mobileHeaderPage);
  const mobileHeaderOk = !mobileHidden.visible && mobileRevealed.visible && mobileRevealed.top >= -2;
  console.log(`${mobileHeaderOk ? 'OK' : 'FAIL'} mobile header small upward deltas hidden=${!mobileHidden.visible} revealed=${mobileRevealed.visible} top=${mobileRevealed.top.toFixed(1)}px`);
  if (!mobileHeaderOk) failed = true;

  const mobileMenuButton = mobileHeaderPage.locator('#mobile-menu-btn');
  if (await mobileMenuButton.count()) {
    await mobileMenuButton.click();
    const menuOpen = await mobileHeaderPage.locator('#mobile-menu').evaluate(el => !el.classList.contains('hidden'));
    const headerWithMenu = await readHeaderVisibility(mobileHeaderPage);
    const menuHeaderOk = menuOpen && headerWithMenu.visible;
    console.log(`${menuHeaderOk ? 'OK' : 'FAIL'} mobile header remains visible with menu open=${menuOpen} headerVisible=${headerWithMenu.visible}`);
    if (!menuHeaderOk) failed = true;
  } else {
    console.log('FAIL mobile menu button not found for header interaction test');
    failed = true;
  }
  await mobileHeaderPage.close();

  // Ordinary outbound sources must retain their real destinations, including when added dynamically.
  const outboundPage = await browser.newPage({ viewport: { width: 1280, height: 900 } });
  await outboundPage.goto('http://127.0.0.1:4173/slots/', { waitUntil: 'networkidle' });
  const outboundResult = await outboundPage.evaluate(async () => {
    const original = document.createElement('a');
    original.href = 'https://www.gluecksspiel-behoerde.de/source';
    original.target = '_blank';
    original.rel = 'noopener';
    original.textContent = 'official source';
    document.body.appendChild(original);
    await new Promise(resolve => setTimeout(resolve, 50));
    const externalHref = original.getAttribute('href');
    const externalTarget = original.getAttribute('target');
    const externalRel = original.getAttribute('rel');
    const internal = document.createElement('a');
    internal.href = '/en/slots/';
    document.body.appendChild(internal);
    const internalHref = internal.getAttribute('href');
    const mail = document.createElement('a');
    mail.href = 'mailto:info@example.org';
    document.body.appendChild(mail);
    const mailHref = mail.getAttribute('href');
    return { externalHref, externalTarget, externalRel, internalHref, mailHref };
  });
  const outboundOk = outboundResult.externalHref === 'https://www.gluecksspiel-behoerde.de/source' &&
    outboundResult.externalTarget === '_blank' &&
    outboundResult.externalRel === 'noopener' &&
    outboundResult.internalHref === '/en/slots/' &&
    outboundResult.mailHref === 'mailto:info@example.org';
  console.log(`${outboundOk ? 'OK' : 'FAIL'} outbound links external=${outboundResult.externalHref} target=${outboundResult.externalTarget} internal=${outboundResult.internalHref} mail=${outboundResult.mailHref}`);
  if (!outboundOk) failed = true;
  await outboundPage.close();

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
  // Search a phrase that appears in the game description, not the title/provider.
  await search.fill('Dual Reactions');
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
    crossLanguageMatches > 0 &&
    descriptionMatches === 1 && descriptionMatchTitle.trim() === 'Bonanza' &&
    longTextMatches === 0 && providerMatches > 0 && emptyStateVisible && restoredCount === 35;
  console.log(`${searchOk ? 'OK' : 'FAIL'} catalogue search title=${titleMatches} multiword=${multiWordMatches} typo=${typoMatches} crossLanguage=${crossLanguageMatches} description=${descriptionMatches} (${descriptionMatchTitle?.trim()}) longText=${longTextMatches} provider=${providerMatches} empty=${emptyStateVisible} reset=${restoredCount}/35`);
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
      iconWidth: panel.querySelector('.slot-search-icon').getBoundingClientRect().width,
      iconHeight: panel.querySelector('.slot-search-icon').getBoundingClientRect().height,
      visibleLabel: Boolean(panel.querySelector('.slot-search-label-title')?.textContent.trim())
    };
  });
  const mobileSearchOk = mobileSearchMetrics.panelRight <= 360 && mobileSearchMetrics.fieldWidth > 280 &&
    mobileSearchMetrics.fieldHeight >= 54 && mobileSearchMetrics.inputFontSize >= 16 && mobileSearchMetrics.iconWidth <= 24 && mobileSearchMetrics.iconHeight <= 24 && mobileSearchMetrics.visibleLabel;
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

  // Check the image-first three-column desktop layout on the German catalogue.
  const desktop = await browser.newPage({ viewport: { width: 1440, height: 1000 }, deviceScaleFactor: 1 });
  const desktopCheck = await inspectPage(desktop, '/slots/', 35);
  const desktopCardLayout = desktopCheck.result.cardLayout;
  const desktopCardOk = desktopCheck.result.columns === 3 &&
    desktopCardLayout.direction === 'column' &&
    desktopCardLayout.cardWidth >= 340 &&
    Math.abs(desktopCardLayout.artRatio - (16 / 9)) < 0.03;
  if (!desktopCheck.ok || !desktopCardOk) {
    console.log(`FAIL /slots/ desktop columns=${desktopCheck.result.columns} direction=${desktopCardLayout.direction} cardWidth=${desktopCardLayout.cardWidth.toFixed(1)} artRatio=${desktopCardLayout.artRatio.toFixed(3)} expected=3 columns, vertical cards, width>=340px, 16:9 artwork`);
    failed = true;
  }
  await desktop.close();

  // Verify the German bonus calculator inputs, calculation and post-result offer CTA.
  const calculatorPage = await browser.newPage({ viewport: { width: 1280, height: 900 } });
  await calculatorPage.goto('http://127.0.0.1:4173/slots/', { waitUntil: 'networkidle' });
  const calculator = calculatorPage.locator('[data-wager-form]');
  const calculatorExists = await calculator.count() === 1;
  if (!calculatorExists) {
    console.log('FAIL German bonus calculator is missing');
    failed = true;
  } else {
    await calculator.locator('[name="deposit"]').fill('100');
    await calculator.locator('[name="bonus"]').fill('100');
    await calculator.locator('[name="wager"]').fill('30');
    await calculator.locator('[name="basis"]').selectOption('deposit_bonus');
    await calculator.locator('[name="contribution"]').fill('20');
    await calculator.locator('button[type="submit"]').click();
    const resultText = await calculator.locator('[data-wager-result]').textContent();
    const ctaVisible = await calculator.locator('[data-wager-cta]').isVisible();
    const calculatorOk = resultText.includes('6.000,00') && resultText.includes('30.000,00') && ctaVisible;
    console.log(`${calculatorOk ? 'OK' : 'FAIL'} bonus calculator result and offer CTA: ${resultText.trim()}`);
    if (!calculatorOk) failed = true;
  }
  await calculatorPage.close();

  // Verify that the same localized offers, casino overview and calculator exist in every other language.
  const localizedCases = [
    { path: '/en/slots/', heading: 'Check bonus offers' },
    { path: '/pl/slots/', heading: 'Sprawdź oferty bonusowe' },
    { path: '/es/slots/', heading: 'Consultar ofertas de bonos' },
    { path: '/pt/slots/', heading: 'Consultar ofertas de bónus' },
    { path: '/ja/slots/', heading: 'ボーナスオファーを確認' }
  ];
  for (const item of localizedCases) {
    const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });
    await page.goto('http://127.0.0.1:4173' + item.path, { waitUntil: 'networkidle' });
    const hub = page.locator('[data-wager-calculator]');
    const hubExists = await hub.count() === 1;
    const headingVisible = await page.getByRole('heading', { name: item.heading }).count() === 1;
    const hubTableCount = await page.locator('table').count();
    const externalReviewLinks = await page.locator('a[href*="askgamblers.com"], a[href*="reddit.com"], a[href*="lcb.org"]').count();
    const bonanzaText = await page.locator('#bonanza').evaluate(el => {
      let node = el.nextElementSibling;
      while (node && node.tagName !== 'P') node = node.nextElementSibling;
      return node ? node.innerText : '';
    });
    const bonanzaWrongClaim = {
      '/en/slots/': /cluster-style wins/i,
      '/pl/slots/': /wygrane klastrowe/i,
      '/es/slots/': /premios por clústeres/i,
      '/pt/slots/': /vitórias por agrupamento/i,
      '/ja/slots/': /クラスター配当/
    }[item.path].test(bonanzaText);
    const cardAuthorCount = await page.locator('.slot-game-card-author').count();
    const hubOk = hubTableCount >= 1 && externalReviewLinks === 0 &&
      bonanzaText.includes('Megaways') && !bonanzaWrongClaim;
    const profilePath = item.path.replace('/slots/', '/slots/bonanza/');
    const profileResponse = await page.goto('http://127.0.0.1:4173' + profilePath, { waitUntil: 'networkidle' });
    const profileTableCount = await page.locator('table').count();
    const profileH1 = await page.locator('h1').first().textContent();
    const profileDescription = (await page.locator('article header p').first().textContent() || '').trim();
    const metaDescription = (await page.locator('meta[name="description"]').getAttribute('content') || '').trim();
    const canonical = await page.locator('link[rel="canonical"]').getAttribute('href');
    const hreflangCount = await page.locator('link[rel="alternate"][hreflang]').count();
    const expertSection = page.locator('[data-slot-expert-analysis]');
    const expertText = (await expertSection.innerText().catch(() => '')).trim();
    const authorText = (await page.locator('.editorial-meta').innerText().catch(() => '')).trim();
    const authorMeta = (await page.locator('meta[name="author"]').getAttribute('content') || '').trim();
    const keywordMeta = (await page.locator('meta[name="keywords"]').getAttribute('content') || '').trim();
    const articleSchemaText = await page.locator('script[type="application/ld+json"]').allTextContents();
    const articleSchema = articleSchemaText.map(value => { try { return JSON.parse(value); } catch { return null; } }).find(value => value && value['@type'] === 'Article');
    const profileSummaryOk = profileDescription.includes('Dual Reactions') && profileDescription === metaDescription;
    const editorialProfileOk = expertText.length > 1800 && /Bonanza/.test(expertText) &&
      authorText.includes('Jon Pill') && authorMeta === 'Jon Pill' && keywordMeta.includes('Bonanza') &&
      articleSchema?.author?.name === 'Jon Pill' && String(articleSchema?.author?.url || '').includes('/authors/jon-pill/');
    const profileOk = profileResponse?.status() === 200 && profileTableCount === 1 &&
      profileH1.includes('Bonanza') && canonical.includes('/slots/bonanza/') &&
      hreflangCount === 7 && profileSummaryOk && editorialProfileOk;
    const contentOk = hubOk && profileOk && cardAuthorCount === 35;
    if (!contentOk) console.log(`  author diagnostics ${item.path}: cards=${cardAuthorCount} expertLength=${expertText.length} byline=${JSON.stringify(authorText)} metaAuthor=${JSON.stringify(authorMeta)} keywords=${JSON.stringify(keywordMeta)}`);
    await page.goto('http://127.0.0.1:4173' + item.path, { waitUntil: 'networkidle' });
    let calculationOk = false;
    if (hubExists) {
      const form = hub.locator('[data-wager-form]');
      await form.locator('[name="deposit"]').fill('100');
      await form.locator('[name="bonus"]').fill('100');
      await form.locator('[name="wager"]').fill('30');
      await form.locator('[name="basis"]').selectOption('deposit_bonus');
      await form.locator('[name="contribution"]').fill('20');
      await form.locator('button[type="submit"]').click();
      const resultText = await form.locator('[data-wager-result]').textContent();
      const ctaVisible = await form.locator('[data-wager-cta]').isVisible();
      calculationOk = /6[.,\s]?000/.test(resultText) && /30[.,\s]?000/.test(resultText) && ctaVisible;
    }
    const localizedOk = hubExists && headingVisible && calculationOk && contentOk;
    console.log(`${localizedOk ? 'OK' : 'FAIL'} localized hub ${item.path} heading=${headingVisible} calculator=${hubExists} calculation=${calculationOk} hubTables=${hubTableCount} profileTables=${profileTableCount} canonical=${Boolean(canonical?.includes('/slots/bonanza/'))} hreflang=${hreflangCount} externalReviewLinks=${externalReviewLinks} content=${contentOk}`);
    if (!localizedOk) failed = true;
    await page.close();
  }

  await browser.close();
  if (failed) process.exit(1);
})().catch(error => { console.error(error); process.exit(1); });
