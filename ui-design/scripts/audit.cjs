// Measurements for visual review: horizontal overflow, font sizes, small text, density, borders.
// Use to compare variants or explain a felt problem; these are not targets.
// Usage: node audit.cjs <file.html|url> [width=1440]
// Exit 1 only on horizontal overflow. Dev-time only.
const { execSync } = require('child_process');
const path = require('path');
function loadPlaywright() {
  try { return require('playwright'); } catch (_) {}
  const hit = execSync("find ~/.npm/_npx -path '*node_modules/playwright/package.json' 2>/dev/null | head -1", { shell: '/bin/bash' }).toString().trim();
  if (!hit) { console.error('Playwright not found. Run once online: npx playwright@latest install chromium'); process.exit(1); }
  return require(path.dirname(hit));
}
(async () => {
  const target = process.argv[2], width = Number(process.argv[3] || 1440);
  if (!target) { console.error('usage: node audit.cjs <file.html|url> [width]'); process.exit(2); }
  const url = /^(https?|file):/.test(target) ? target : 'file://' + path.resolve(target);
  const { chromium } = loadPlaywright();
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width, height: 900 } });
  await page.goto(url); await page.waitForTimeout(500);
  const r = await page.evaluate(() => {
    const W = document.documentElement.clientWidth, H = innerHeight;
    const all = [...document.querySelectorAll('body *')].filter(e => e.getClientRects().length);
    const vis = e => getComputedStyle(e).visibility !== 'hidden' && getComputedStyle(e).display !== 'none';
    const hasText = e => [...e.childNodes].some(n => n.nodeType === 3 && n.textContent.trim());
    const texts = all.filter(e => hasText(e) && vis(e));
    const sizes = {}; let tiny = 0;
    for (const e of texts) { const s = parseFloat(getComputedStyle(e).fontSize); sizes[s] = (sizes[s] || 0) + 1; if (s < 11) tiny++; }
    const bordered = all.filter(e => ['Top', 'Right', 'Bottom', 'Left'].some(k => parseFloat(getComputedStyle(e)['border' + k + 'Width']) > 0)).length;
    // saturated colored marks above the fold — informational only (did not separate calm from heavy in calibration)
    const sat = c => { const m = c.match(/[\d.]+/g); if (!m) return 0; const [r, g, b, a = 1] = m.map(Number); if (a < 0.08) return 0; return (Math.max(r, g, b) - Math.min(r, g, b)) / 255; };
    const colorful = all.filter(e => { const b = e.getBoundingClientRect(); if (b.top > H) return false; const cs = getComputedStyle(e); return (hasText(e) && sat(cs.color) > 0.35) || sat(cs.backgroundColor) > 0.35; }).length;
    const off = [];
    for (const el of all) {
      const box = el.getBoundingClientRect();
      if (box.right <= W + 1) continue;
      let scrolled = false;
      for (let a = el.parentElement; a; a = a.parentElement) if (getComputedStyle(a).overflowX !== 'visible') { scrolled = true; break; }
      if (!scrolled) off.push(`${el.tagName.toLowerCase()}.${String(el.getAttribute('class') || '').trim().replace(/\s+/g, '.')} right=${Math.round(box.right)}`);
    }
    return { viewport: W, scrollWidth: document.documentElement.scrollWidth, pageHeight: document.documentElement.scrollHeight,
             textElements: texts.length, distinctFontSizes: Object.keys(sizes).length, fontSizes: sizes, tinyTextUnder11px: tiny,
             borderedElements: bordered, colorfulAboveFold: colorful, overflow: off.slice(0, 15) };
  });
  // Numbers are for comparing variants or confirming a felt problem — not targets.
  const notes = [];
  if (r.scrollWidth > r.viewport) notes.push('FAIL horizontal overflow — see "overflow"');
  if (r.tinyTextUnder11px > 0) notes.push(`NOTE ${r.tinyTextUnder11px} text elements under 11px — will they be comfortable to read in real use?`);
  console.log(JSON.stringify(r, null, 1)); if (notes.length) console.log(notes.join('\n'));
  await browser.close();
  process.exit(r.scrollWidth > r.viewport ? 1 : 0);
})();
