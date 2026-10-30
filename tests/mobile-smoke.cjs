const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({ headless: true });
  let failed = false;
  for (const path of ['/', '/es/', '/pt/', '/pl/', '/ja/', '/bonuses/', '/slots/']) {
    const page = await browser.newPage({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 1 });
    const errors = [];
    page.on('pageerror', error => errors.push(error.message));
    const response = await page.goto(`http://127.0.0.1:4173${path}`, { waitUntil: 'networkidle' });
    const result = await page.evaluate(async () => {
      const slotImages = [...document.querySelectorAll('.slot-game-card img')];
      await Promise.all(slotImages.map(async image => {
        image.loading = 'eager';
        try { await image.decode(); } catch (_) { /* reported below */ }
      }));
      return {
        width: document.documentElement.clientWidth,
        scrollWidth: document.documentElement.scrollWidth,
        title: document.title,
        slotCards: document.querySelectorAll('.slot-game-card').length,
        slotImages: slotImages.map(image => ({
          alt: image.alt.trim(),
          loaded: image.complete && image.naturalWidth > 0
        }))
      };
    });
    const isSlotsPage = path === '/slots/';
    const slotGalleryOk = !isSlotsPage || (
      result.slotCards === 5 &&
      result.slotImages.length === 5 &&
      result.slotImages.every(image => image.alt.length > 0 && image.loaded)
    );
    const ok = response &&
      response.status() === 200 &&
      result.title &&
      result.scrollWidth <= result.width + 1 &&
      errors.length === 0 &&
      slotGalleryOk;
    console.log(`${ok ? 'OK' : 'FAIL'} ${path} status=${response?.status()} viewport=${result.width}/${result.scrollWidth} title=${Boolean(result.title)} slotCards=${result.slotCards} jsErrors=${errors.length}`);
    if (!ok) failed = true;
    await page.close();
  }
  await browser.close();
  if (failed) process.exit(1);
})().catch(error => { console.error(error); process.exit(1); });
