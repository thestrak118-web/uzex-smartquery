import { test, expect, Page } from '@playwright/test';
import * as fs from 'fs';

// Dizayn QA: skrinshot matritsasi + avtomatik vizual tekshiruvlar.
// BASE_URL=http://127.0.0.1:8000 npx playwright test web/tests/uzex-dizayn.spec.ts --project=chromium
const OUT = 'hisobotlar/uzex/dizayn';
fs.mkdirSync(OUT, { recursive: true });

const VIEWPORTS = [
  { name: '1920', width: 1920, height: 1080 },
  { name: '1366', width: 1366, height: 768 },
  { name: '1024', width: 1024, height: 768 },
  { name: '768', width: 768, height: 1024 },
  { name: '390', width: 390, height: 844 },
];
const ROUTES = ['', '#/deals', '#/commodities', '#/participants', '#/sources', '#/settings'];
const routeName = (r: string) => r.replace('#/', '') || 'dashboard';

async function audit(page: Page, vw: number) {
  return page.evaluate((vw) => {
    const vis = (el: Element) => {
      const s = getComputedStyle(el); const r = el.getBoundingClientRect();
      return s.display !== 'none' && s.visibility !== 'hidden' && r.width > 0 && r.height > 0 && !el.closest('[hidden]');
    };
    const name = (el: Element) => (el.id ? '#' + el.id : el.tagName.toLowerCase() + (el.className && typeof el.className === 'string' ? '.' + el.className.split(' ')[0] : '')) + ` «${(el.textContent || '').trim().slice(0, 30)}»`;
    const out: Record<string, string[]> = { tinyFont: [], clipped: [], offscreen: [], smallTap: [], wrongFont: [] };
    for (const el of Array.from(document.querySelectorAll('body *'))) {
      if (!vis(el)) continue;
      const s = getComputedStyle(el);
      const hasText = Array.from(el.childNodes).some((n) => n.nodeType === 3 && n.textContent!.trim());
      if (hasText && parseFloat(s.fontSize) < 9) out.tinyFont.push(`${name(el)} ${s.fontSize}`);
      if (hasText && !/DM Sans|Manrope|monospace|Menlo|SFMono/i.test(s.fontFamily)) out.wrongFont.push(`${name(el)} ${s.fontFamily.slice(0, 30)}`);
      // matn sig'madi: kesilgan (ellipsis'siz) yoki konteynerdan chiqqan
      if (hasText && el.scrollWidth > el.clientWidth + 2 && s.overflowX === 'hidden' && s.textOverflow !== 'ellipsis' && el.clientWidth > 0)
        out.clipped.push(`${name(el)} ${el.scrollWidth}>${el.clientWidth}`);
      const r = el.getBoundingClientRect();
      if (r.right > vw + 1 && !el.closest('.table-wrap, .result-table, .sql-block, .tbl, .sidebar:not(.open), .toast')) out.offscreen.push(`${name(el)} right=${Math.round(r.right)}`);
      if (vw <= 420 && el.matches('button, a, select, input, [role="button"]') && (r.height < 32 || r.width < 32))
        out.smallTap.push(`${name(el)} ${Math.round(r.width)}×${Math.round(r.height)}`);
    }
    for (const k of Object.keys(out)) out[k] = Array.from(new Set(out[k]));
    return out;
  }, vw);
}

const report: any = {};
test.afterAll(() => fs.writeFileSync(`${OUT}/audit.json`, JSON.stringify(report, null, 1)));

for (const vp of VIEWPORTS) {
  for (const lang of ['uz', 'ru']) {
    test(`dizayn ${vp.name} ${lang}`, async ({ page }) => {
      test.setTimeout(120_000);
      await page.setViewportSize({ width: vp.width, height: vp.height });
      await page.goto('/');
      await page.evaluate((l) => { localStorage.clear(); localStorage.setItem('sq_lang', JSON.stringify(l)); }, lang);
      for (const r of ROUTES) {
        await page.goto('/' + r);
        await page.waitForLoadState('networkidle');
        await page.evaluate(() => document.fonts.ready);
        if (lang === 'uz' || ['390', '1366'].includes(vp.name))
          await page.screenshot({ path: `${OUT}/${vp.name}-${lang}-${routeName(r)}.png`, fullPage: true });
        report[`${vp.name}-${lang}-${routeName(r)}`] = await audit(page, vp.width);
      }
      // holatlar: javob (tayyor savol), grafik menyusi, mobil menyu
      await page.goto('/');
      await page.waitForLoadState('networkidle');
      await page.locator('.suggestion-chip').nth(1).click();
      await expect(page.locator('.answer-bubble').last()).toBeVisible();
      await page.locator('.answer-bubble details').last().evaluate((d: any) => (d.open = true));
      await page.locator('#assistant').scrollIntoViewIfNeeded();
      await page.screenshot({ path: `${OUT}/${vp.name}-${lang}-javob.png` });
      report[`${vp.name}-${lang}-javob`] = await audit(page, vp.width);
      if (vp.width <= 760) {
        await page.locator('#mobileMenu').click();
        await page.screenshot({ path: `${OUT}/${vp.name}-${lang}-menyu.png` });
      } else {
        await page.locator('.chart-menu').click();
        await page.screenshot({ path: `${OUT}/${vp.name}-${lang}-grafik-menyu.png` });
      }
      const fontsOk = await page.evaluate(() => ['DM Sans', 'Manrope'].map((f) => document.fonts.check(`12px "${f}"`)));
      report[`${vp.name}-${lang}-fonts`] = fontsOk;
    });
  }
}
