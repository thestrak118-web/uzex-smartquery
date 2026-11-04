import { test, expect, Page } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

// BASE_URL=http://127.0.0.1:8000 npx playwright test web/tests/uzex-smartquery.spec.ts
// AI javoblari: tayyor/keshdagi savollar yoki page.route bilan soxta javob — Gemini limiti sarflanmaydi.

const consoleErrors: string[] = [];

async function open(page: Page, hash = '') {
  consoleErrors.length = 0;
  page.on('console', (m) => { if (m.type() === 'error' && !/favicon/.test(m.text())) consoleErrors.push(m.text()); });
  page.on('pageerror', (e) => consoleErrors.push(e.message));
  await page.goto('/' + hash);
  await page.evaluate(() => localStorage.clear());
  await page.goto('/' + hash);
}

const fakeAnswer = (body: object, status = 200) => async (route: any) =>
  route.fulfill({ status, contentType: 'application/json', body: JSON.stringify(body) });

async function nav(page: Page, route: string) {
  const burger = page.locator('#mobileMenu');
  if (await burger.isVisible()) {           // telefonda sidebar yopiq — avval menyuni ochamiz
    await burger.click();
    await expect(page.locator('#sidebar')).toHaveClass(/open/);
  }
  await page.locator(`.nav-link[data-route="${route}"]`).click();
  await expect(page.locator('#sidebar')).not.toHaveClass(/open/);
}

async function lastAnswer(page: Page) {
  const bubble = page.locator('.assistant-message .answer-bubble').last();
  await expect(bubble).toBeVisible({ timeout: 15_000 });
  return bubble;
}

test.describe('Dashboard', () => {
  test('ko\'rsatkichlar bazadan yuklanadi va konsolda xato yo\'q', async ({ page }) => {
    await open(page);
    await expect(page).toHaveTitle(/UZEX SmartQuery/);
    await expect(page.locator('#statDeals')).toHaveText('500,000');
    await expect(page.locator('#statContracts')).toHaveText('6,616');
    await expect(page.locator('#statCompanies')).toHaveText('14,392');
    await expect(page.locator('#yearBars .bar-item')).toHaveCount(5);
    await expect(page.locator('#connStatus')).not.toHaveClass(/offline/);
    expect(consoleErrors).toEqual([]);
  });

  test('tayyor savol tugmasi darhol to\'g\'ri javob beradi', async ({ page }) => {
    await open(page);
    const t0 = Date.now();
    await page.getByRole('button', { name: '2025-yilda nechta bitim tuzilgan?' }).click();
    const bubble = await lastAnswer(page);
    expect(Date.now() - t0).toBeLessThan(5000);
    await expect(bubble).toContainText('115 763');
    await expect(bubble.locator('.answer-details summary').first()).toContainText('SQL');
    await expect(page.locator('#recentRows .recent-row')).toHaveCount(1);
  });

  test('til RU ga o\'tadi va qayta yuklanganda saqlanadi', async ({ page }) => {
    await open(page);
    await page.locator('.lang-btn[data-lang="ru"]').click();
    await expect(page.locator('#statDeals')).toBeVisible();
    await expect(page.locator('.page-heading h1').first()).toContainText('Точные ответы');
    await expect(page.locator('.suggestion-chip').first()).toContainText('Сколько сделок');
    await page.reload();
    await expect(page.locator('.page-heading h1').first()).toContainText('Точные ответы');
  });

  test('imkoniyat kartasi bosilganda savol yuboriladi', async ({ page }) => {
    await open(page);
    await page.locator('.capability-item').nth(2).click();
    await expect(page.locator('.user-message .message-bubble').last()).toContainText('eng yirik 5 ta xaridor');
    const bubble = await lastAnswer(page);
    await expect(bubble).toContainText('Zoket Invest');
  });

  test('grafik menyusi ko\'rsatkichni aylanmaga almashtiradi', async ({ page }) => {
    await open(page);
    await page.locator('.chart-menu').click();
    await page.locator('.chart-pop [data-metric="turnover"]').click();
    await expect(page.locator('#chartTotal')).toContainText('trln');
    await expect(page.locator('#yearBars .bar-value').first()).toContainText('trln');
    await page.locator('.chart-menu').click();
    await page.locator('.chart-pop [data-metric="cancel"]').click();
    await expect(page.locator('#chartTotal')).toContainText('%');
  });

  test('yil ustuni bosilganda o\'sha yil tahlili keladi', async ({ page }) => {
    await open(page);
    await page.locator('#yearBars .bar-item[data-year="2024"]').click();
    const bubble = await lastAnswer(page);
    await expect(bubble).toContainText('106 647');
  });

  test('AI band bo\'lsa tushunarli xato ko\'rsatiladi', async ({ page }) => {
    await open(page);
    await page.route('**/api/v1/ask', fakeAnswer({ answer: 'Gemini limiti vaqtincha tugadi', status: 'busy', language: 'uz' }, 503));
    await page.getByPlaceholder('Savolingizni kiriting...').fill('Erkin savol');
    await page.keyboard.press('Enter');
    await expect(page.locator('.error-bubble').last()).toContainText('limiti vaqtincha tugadi');
    await expect(page.locator('#recentRows')).toContainText('Limit');
    await expect(page.locator('.send-button')).toBeEnabled();
  });

  test('server javob bermasa sahifa qotib qolmaydi', async ({ page }) => {
    await open(page);
    await page.route('**/api/v1/ask', (r) => r.abort());
    await page.getByPlaceholder('Savolingizni kiriting...').fill('test');
    await page.keyboard.press('Enter');
    await expect(page.locator('.error-bubble').last()).toBeVisible();
    await expect(page.locator('.send-button')).toBeEnabled();
  });

  test('javobdagi HTML/skript bajarilmaydi (XSS)', async ({ page }) => {
    await open(page);
    let alerted = false;
    page.on('dialog', async (d) => { alerted = true; await d.dismiss(); });
    await page.route('**/api/v1/ask', fakeAnswer({
      answer: '<img src=x onerror=alert(1)> **qalin** <script>alert(2)</script>', status: 'ok', language: 'uz',
      source: { tables: ['deals'], filters: [{ text: '<b>x</b>', code: true }], sql: ['select 1 -- <script>alert(3)</script>'], model: 'm', steps: 1, seconds: 1 },
      visualization: { type: 'hbar', title: 'v', labels: ['<img src=y onerror=alert(4)>', 'b'], values: [2, 1] },
      table: { columns: ['<i>c</i>'], rows: [['<svg onload=alert(5)>'], ['x']], row_count: 2, truncated: false },
    }));
    await page.getByPlaceholder('Savolingizni kiriting...').fill('xss');
    await page.keyboard.press('Enter');
    const bubble = await lastAnswer(page);
    await expect(bubble.locator('b').first()).toHaveText('qalin');
    await expect(bubble.locator('img, script, svg[onload]')).toHaveCount(0);
    expect(alerted).toBe(false);
  });

  test('yangi suhbat tugmasi chatni tozalaydi', async ({ page }) => {
    await open(page);
    await page.getByRole('button', { name: '2025-yilda nechta bitim tuzilgan?' }).click();
    await lastAnswer(page);
    await page.locator('#clearChat').click();
    await expect(page.locator('.assistant-message .answer-bubble')).toHaveCount(0);
    await expect(page.locator('.suggestion-chip').first()).toBeVisible();
  });
});

test.describe('Sidebar sahifalari', () => {
  test('har bir bo\'lim o\'z sahifasini ochadi', async ({ page }) => {
    await open(page);
    for (const [route, title] of [['deals', 'Bitimlar'], ['commodities', 'Tovarlar'], ['participants', 'Ishtirokchilar'],
                                  ['sources', 'Ma’lumotlar manbasi'], ['settings', 'Sozlamalar']]) {
      await nav(page, route);
      await expect(page.locator('#crumb')).toHaveText(title);
      await expect(page.locator(`[data-view="${route}"]`)).toBeVisible();
      await expect(page.locator('#assistant')).toBeHidden();
    }
    await nav(page, 'overview');
    await expect(page.locator('#assistant')).toBeVisible();
    expect(consoleErrors).toEqual([]);
  });

  test('bitimlar: filtr, qidiruv va sahifalash ishlaydi', async ({ page }) => {
    await open(page, '#/deals');
    await expect(page.locator('#dealsInfo')).toContainText('500,000');
    await page.locator('#fYear').selectOption('2025');
    await page.locator('#fProduct').selectOption('Карбамид');
    await expect(page.locator('#dealsInfo')).toContainText('2,565');
    await page.locator('#dealsNext').click();
    await expect(page.locator('#dealsInfo')).toContainText('26–50');
    await page.locator('#fReset').click();
    await page.locator('#fQuery').fill('280092');
    await expect(page.locator('#dealsRows tr[data-deal]')).toHaveCount(1);
    await expect(page.locator('#dealsRows')).toContainText('Karbamid');
  });

  test('bitim qatori bosilganda AI shu bitimni tahlil qiladi', async ({ page }) => {
    await open(page, '#/deals');
    await page.route('**/api/v1/ask', fakeAnswer({ answer: 'Bitim tahlili', status: 'ok', language: 'uz' }));
    await page.locator('#fQuery').fill('280092');
    await expect(page.locator('#dealsRows tr[data-deal="280092"]')).toHaveCount(1);
    await page.locator('#dealsRows tr[data-deal="280092"]').click();
    await expect(page.locator('#crumb')).toHaveText('AI tahlilchi');
    await expect(page.locator('.user-message .message-bubble').last()).toContainText('280092');
  });

  test('tovarlar: 41 ta tovar va yil filtri', async ({ page }) => {
    await open(page, '#/commodities');
    await expect(page.locator('#productRows tr[data-product]')).toHaveCount(41);
    await expect(page.locator('#productRows tr').first()).toContainText('Paxta xomashyosi');
    await page.locator('#pYear').selectOption('2022');
    await expect(page.locator('#productRows tr').first()).toContainText('Paxta xomashyosi');
  });

  test('ishtirokchilar: rollar va qidiruv', async ({ page }) => {
    await open(page, '#/participants');
    await expect(page.locator('#partRows tr[data-id]')).toHaveCount(50);
    await page.locator('#roleTabs [data-role="broker"]').click();
    await expect(page.locator('#partHead')).toContainText('SOTUVCHI / XARIDOR TOMONI');
    await page.locator('#partQuery').fill('BK111');
    await expect(page.locator('#partRows tr[data-id]')).toHaveCount(1);
    await expect(page.locator('#partRows')).toContainText('Gucham');
  });

  test('sozlamalar saqlanadi va javob ko\'rinishiga ta\'sir qiladi', async ({ page }) => {
    await open(page, '#/settings');
    await expect(page.locator('#setModel')).not.toHaveText('—');
    await page.locator('[data-setting="openSql"]').check();
    await page.reload();
    await expect(page.locator('[data-setting="openSql"]')).toBeChecked();
    await nav(page, 'assistant');
    await page.getByRole('button', { name: '2025-yilda nechta bitim tuzilgan?' }).click();
    const bubble = await lastAnswer(page);
    await expect(bubble.locator('details.answer-details').first()).toHaveAttribute('open', '');
  });

  test('ma’lumotlar manbasi: 5 ta jadval', async ({ page }) => {
    await open(page, '#/sources');
    await expect(page.locator('#srcTables details')).toHaveCount(5);
    await expect(page.locator('#srcRules li')).toHaveCount(7);
  });
});

test.describe('Moslashuvchanlik va accessibility', () => {
  test.describe.configure({ timeout: 60_000 });  // axe parallel yuklamada sekinlashadi
  for (const route of ['', '#/deals', '#/commodities', '#/participants', '#/sources', '#/settings']) {
    test(`gorizontal siljish yo'q: ${route || 'dashboard'}`, async ({ page }) => {
      await open(page, route);
      await page.waitForLoadState('networkidle');
      const overflow = await page.evaluate(() => document.documentElement.scrollWidth - window.innerWidth);
      expect(overflow).toBeLessThanOrEqual(1);
    });
  }

  for (const route of ['', '#/deals', '#/commodities', '#/participants', '#/sources', '#/settings']) {
    test(`jiddiy accessibility xatolari yo'q: ${route || 'dashboard'}`, async ({ page }) => {
      await open(page, route);
      await page.waitForLoadState('networkidle');
      const r = await new AxeBuilder({ page }).withTags(['wcag2a', 'wcag2aa']).analyze();
      // color-contrast — dizayn palitrasi (alohida topilma sifatida hisobotda), qolgan jiddiylari 0 bo'lishi kerak
      const bad = r.violations.filter((v) => (v.impact === 'critical' || v.impact === 'serious') && v.id !== 'color-contrast');
      expect(bad, bad.map((v) => `${v.id} (${v.impact}): ${v.help} — ${v.nodes.length} ta`).join('\n')).toEqual([]);
    });
  }
});
