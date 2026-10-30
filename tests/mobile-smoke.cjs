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
