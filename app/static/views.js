// Sidebar sahifalari: Bitimlar, Tovarlar, Ishtirokchilar, Ma'lumotlar manbasi, Sozlamalar.
// app.js dagi umumiy yordamchilardan foydalanadi: t, esc, fmtInt, fmtNum, fmtCompact, store, askFromCard, showToast.

Object.assign(translations.uz, {
  vDealsEyebrow:'BITIMLAR REYESTRI', vDealsTitle:'Bitimlar <em>reyestri.</em>', vDealsSub:'Barcha bitimlarni yil, tovar, viloyat va holat bo‘yicha filtrlang. Qatorni bosing — AI bitimni tushuntiradi.',
  vDealsSearch:'Bitim raqami, STIR, kompaniya yoki tovar…', vReset:'Tozalash', vAllYears:'Barcha yillar', vAllProducts:'Barcha tovarlar', vAllRegions:'Barcha viloyatlar', vAllStatuses:'Barcha holatlar',
  vColDeal:'№ / SANA', vColProduct:'TOVAR', vColRegion:'VILOYAT', vColVolume:'HAJM', vColAmount:'SUMMA', vColPrice:'NARX / BIRLIK', vColParties:'SOTUVCHI → XARIDOR', vColStatus:'HOLAT',
  vColCategory:'KATEGORIYA', vColDeals:'BITIMLAR', vColTurnover:'AYLANMA, SO‘M', vColShare:'ULUSH', vColTonnes:'HAJM, T', vColAvgPrice:'O‘RTACHA NARX', vColName:'NOMI', vColId:'STIR / KOD', vColActivity:'FAOLIYAT', vColSides:'SOTUVCHI / XARIDOR TOMONI', vColProducts:'TOVARLAR',
  vShown:(a, b, n) => `${a}–${b} / ${n} ta bitim`, vNothing:'Hech narsa topilmadi', vLoading:'Yuklanmoqda…', vAsk:'AI ✳', vPerUnit:'so‘m /',
  vProdEyebrow:'TOVARLAR TAHLILI', vProdTitle:'Tovarlar <em>kesimida.</em>', vProdSub:'230 xil yozuv 41 ta kanonik tovarga keltirilgan. Aylanma bekor qilingan bitimlarsiz hisoblanadi.',
  vPartEyebrow:'ISHTIROKCHILAR', vPartTitle:'Xaridorlar, sotuvchilar <em>va brokerlar.</em>', vPartSub:'Nom (kirill yoki lotin), STIR yoki broker kodi bo‘yicha qidiring. Qatorni bosing — AI tahlil qiladi.',
  vBuyers:'Xaridorlar', vSellers:'Sotuvchilar', vBrokers:'Brokerlar', vPartSearch:'Nomi, STIR yoki broker kodi…',
  vSrcEyebrow:'MA’LUMOTLAR MANBASI', vSrcTitle:'Dataset <em>va qoidalar.</em>', vSrcSub:'Agent javob beradigan ma’lumotlar, ularning tuzilishi va hisoblash qoidalari.',
  vSrcFiles:'FAYLLAR', vSrcRules:'HISOBLASH QOIDALARI', vSrcTables:'DUCKDB JADVALLARI', vSrcSynthTitle:'Sun’iy ma’lumotlar', vSrcSynth:'Barcha kompaniyalar, STIR, brokerlar, narxlar va dollar kursi o‘ylab topilgan. Format tovar-xomashyo birjasining ochiq reyestrini takrorlaydi.',
  vRows:'qator', vCols:'ustun',
  vFiles:[['deals_2022…2026.csv', 'Bitimlar: 500 000 ta, 2022-yil 3-yanvardan 2026-yil 30-oktabrgacha'], ['contracts.csv', 'Shartnoma kartochkalari: tovar, atributlar, valyuta, muddatlar'], ['participants.csv', 'Sotuvchi va xaridor kompaniyalar'], ['brokers.csv', 'Broker idoralari'], ['usd_rates.csv', 'Har kun uchun dollar kursi (so‘m / 1 USD)']],
  vRulesList:['Bekor qilingan (to‘lanmagan) bitimlar aylanma, hajm va narxga kirmaydi', 'O‘rtacha narx vaznli: summa ÷ hajm, bitta birlik va valyutada', 'Eksport bitimlari USD da; so‘mga bitim kunidagi kurs bo‘yicha o‘giriladi', 'Turli o‘lchov birliklari qo‘shilmaydi (benzin — tonna va litr)', 'Hajm = lotlar soni × lot hajmi; kg va tonna — tonnaga keltiriladi', 'Tovar nomlari normallashtirilgan: 230 xil yozuv → 41 ta tovar', 'Har bir raqam SQL so‘rov natijasidan olinadi, taxmin qilinmaydi'],
  vSetEyebrow:'SOZLAMALAR', vSetTitle:'Interfeys <em>sozlamalari.</em>', vSetSub:'Sozlamalar shu brauzerda saqlanadi.', vSetView:'JAVOB KO‘RINISHI', vSetLang:'Interfeys tili', vSetLangNote:'AI savol berilgan tilda javob beradi',
  vSetCharts:'Grafiklarni ko‘rsatish', vSetChartsNote:'Natija jadvalidan avtomatik grafik', vSetSql:'SQL so‘rovlarni ochiq ko‘rsatish', vSetSqlNote:'Har javob ostida SQL darhol ochiladi', vSetTable:'Natija jadvalini ochiq ko‘rsatish', vSetTableNote:'Jadval yig‘ilgan holda emas, ochiq chiqadi',
  vSetClearHistory:'So‘rovlar tarixini tozalash', vSetNewChat:'Yangi suhbat boshlash', vSetSystem:'TIZIM', vSetModel:'AI model', vSetModelNote:'Band bo‘lsa avtomatik zaxira modelga o‘tadi', vSetFallbacks:'Zaxira modellar', vSetData:'Ma’lumotlar sanasi', vSetBotNote:'Xuddi shu agent Telegram’da', vSaved:'Saqlandi',
  qDeal: id => `${id} raqamli bitim haqida batafsil ma’lumot ber`,
  qProduct: (p, y) => `${p} bo‘yicha ${y ? y + '-yilda' : '2022–2026-yillarda'} narx va savdo hajmi dinamikasini tahlil qil`,
  qCompany: (id, role) => `STIR ${id} kompaniyasi ${role === 'seller' ? 'sotuvchi' : 'xaridor'} sifatida qanday bitimlar tuzgan? Asosiy ko‘rsatkichlarini ber`,
  qBroker: id => `${id} kodli broker faoliyati: bitimlar soni, aylanma va asosiy tovarlar`,
});
Object.assign(translations.ru, {
  vDealsEyebrow:'РЕЕСТР СДЕЛОК', vDealsTitle:'Реестр <em>сделок.</em>', vDealsSub:'Фильтруйте сделки по году, товару, региону и статусу. Нажмите на строку — AI объяснит сделку.',
  vDealsSearch:'Номер сделки, ИНН, компания или товар…', vReset:'Сбросить', vAllYears:'Все годы', vAllProducts:'Все товары', vAllRegions:'Все регионы', vAllStatuses:'Все статусы',
  vColDeal:'№ / ДАТА', vColProduct:'ТОВАР', vColRegion:'РЕГИОН', vColVolume:'ОБЪЁМ', vColAmount:'СУММА', vColPrice:'ЦЕНА / ЕД.', vColParties:'ПРОДАВЕЦ → ПОКУПАТЕЛЬ', vColStatus:'СТАТУС',
  vColCategory:'КАТЕГОРИЯ', vColDeals:'СДЕЛКИ', vColTurnover:'ОБОРОТ, СУМ', vColShare:'ДОЛЯ', vColTonnes:'ОБЪЁМ, Т', vColAvgPrice:'СРЕДНЯЯ ЦЕНА', vColName:'НАИМЕНОВАНИЕ', vColId:'ИНН / КОД', vColActivity:'ДЕЯТЕЛЬНОСТЬ', vColSides:'СТОРОНА ПРОДАВЦА / ПОКУПАТЕЛЯ', vColProducts:'ТОВАРЫ',
  vShown:(a, b, n) => `${a}–${b} из ${n} сделок`, vNothing:'Ничего не найдено', vLoading:'Загрузка…', vAsk:'AI ✳', vPerUnit:'сум /',
  vProdEyebrow:'АНАЛИЗ ТОВАРОВ', vProdTitle:'В разрезе <em>товаров.</em>', vProdSub:'230 вариантов написания сведены к 41 каноническому товару. Оборот считается без аннулированных сделок.',
  vPartEyebrow:'УЧАСТНИКИ', vPartTitle:'Покупатели, продавцы <em>и брокеры.</em>', vPartSub:'Ищите по названию (кириллица или латиница), ИНН или коду брокера. Нажмите на строку — AI проанализирует.',
  vBuyers:'Покупатели', vSellers:'Продавцы', vBrokers:'Брокеры', vPartSearch:'Название, ИНН или код брокера…',
  vSrcEyebrow:'ИСТОЧНИКИ ДАННЫХ', vSrcTitle:'Датасет <em>и правила.</em>', vSrcSub:'Данные, на которые опирается агент, их структура и правила расчёта.',
  vSrcFiles:'ФАЙЛЫ', vSrcRules:'ПРАВИЛА РАСЧЁТА', vSrcTables:'ТАБЛИЦЫ DUCKDB', vSrcSynthTitle:'Синтетические данные', vSrcSynth:'Все компании, ИНН, брокеры, цены и курс доллара вымышлены. Формат повторяет публичный реестр товарно-сырьевой биржи.',
  vRows:'строк', vCols:'столбцов',
  vFiles:[['deals_2022…2026.csv', 'Сделки: 500 000, с 3 января 2022 по 30 октября 2026'], ['contracts.csv', 'Карточки контрактов: товар, атрибуты, валюта, сроки'], ['participants.csv', 'Компании-продавцы и покупатели'], ['brokers.csv', 'Брокерские конторы'], ['usd_rates.csv', 'Курс доллара на каждый день (сум за 1 USD)']],
  vRulesList:['Аннулированные (неоплаченные) сделки не входят в оборот, объём и цены', 'Средняя цена — взвешенная: сумма ÷ объём, в одной единице и валюте', 'Экспортные сделки в USD; в сумы — по курсу на дату сделки', 'Разные единицы измерения не складываются (бензин — тонны и литры)', 'Объём = лоты × размер лота; кг и тонны приводятся к тоннам', 'Названия товаров нормализованы: 230 вариантов → 41 товар', 'Каждое число берётся из результата SQL-запроса, без догадок'],
  vSetEyebrow:'НАСТРОЙКИ', vSetTitle:'Настройки <em>интерфейса.</em>', vSetSub:'Настройки сохраняются в этом браузере.', vSetView:'ВИД ОТВЕТА', vSetLang:'Язык интерфейса', vSetLangNote:'AI отвечает на языке вопроса',
  vSetCharts:'Показывать графики', vSetChartsNote:'Автоматический график по таблице результата', vSetSql:'Раскрывать SQL-запросы', vSetSqlNote:'SQL сразу открыт под каждым ответом', vSetTable:'Раскрывать таблицу результата', vSetTableNote:'Таблица показывается открытой',
  vSetClearHistory:'Очистить историю запросов', vSetNewChat:'Начать новый диалог', vSetSystem:'СИСТЕМА', vSetModel:'AI модель', vSetModelNote:'При перегрузке автоматически переключается на резервную', vSetFallbacks:'Резервные модели', vSetData:'Дата данных', vSetBotNote:'Тот же агент в Telegram', vSaved:'Сохранено',
  qDeal: id => `Расскажи подробно о сделке № ${id}`,
  qProduct: (p, y) => `Проанализируй динамику цен и объёма торгов по товару «${p}» ${y ? 'в ' + y + ' году' : 'за 2022–2026 годы'}`,
  qCompany: (id, role) => `Какие сделки заключала компания с ИНН ${id} как ${role === 'seller' ? 'продавец' : 'покупатель'}? Дай основные показатели`,
  qBroker: id => `Деятельность брокера ${id}: число сделок, оборот и основные товары`,
});

const ROUTES = {
  overview: 'overview', assistant: 'aiAnalyst', deals: 'deals', commodities: 'commodities',
  participants: 'participants', sources: 'dataSources', settings: 'settings',
};
const STATUS_UZ = {
  'Исполнен': 'Ijro etilgan', 'Исполнен(Частично)': 'Qisman ijro', 'Аннулирован(Не оплачен)': 'Bekor qilingan',
  'Оплачен': 'To‘langan', 'Заключен': 'Tuzilgan', 'Ждёт оплату': 'To‘lov kutilmoqda', 'Новый': 'Yangi', 'Не подписан': 'Imzolanmagan',
};
const UNIT_UZ = { 'тонна': 'tonna', 'килограмм': 'kg', 'литр': 'litr', 'штука': 'dona', 'куб.метр': 'm³', 'кв.метр': 'm²', 'метр': 'metr' };
const UNIT_RU = { 'тонна': 'т', 'килограмм': 'кг', 'литр': 'л', 'штука': 'шт', 'куб.метр': 'м³', 'кв.метр': 'м²', 'метр': 'м' };
const unitName = u => (currentLang === 'ru' ? UNIT_RU : UNIT_UZ)[u] || u;
const statusName = s => currentLang === 'ru' ? s : (STATUS_UZ[s] || s);
const productName = r => currentLang === 'ru' ? r.product : (r.product_uz || r.product);
const fmtDate = d => d ? d.split('-').reverse().join('.') : '—';
const statusClass = s => /Аннул/.test(s) ? 'st-bad' : /Частич/.test(s) ? 'st-warn' : /^Исполнен$/.test(s) ? 'st-ok' : 'st-mid';
const api = (path, params = {}) => {
  const qs = new URLSearchParams(Object.entries(params).filter(([, v]) => v !== '' && v !== null && v !== undefined));
  return fetch(`${path}${qs.toString() ? '?' + qs : ''}`).then(r => { if (!r.ok) throw new Error(r.status); return r.json(); });
};
const debounce = (fn, ms = 300) => { let h; return (...a) => { clearTimeout(h); h = setTimeout(() => fn(...a), ms); }; };
const loadingRow = cols => `<tr class="empty-row"><td colspan="${cols}">${esc(t('vLoading'))}</td></tr>`;
const emptyRow = cols => `<tr class="empty-row"><td colspan="${cols}">${esc(t('vNothing'))}</td></tr>`;

// ---------- Marshrutlash ----------
function currentRoute(){ const r = (location.hash.match(/^#\/(\w+)/) || [])[1]; return ROUTES[r] ? r : 'assistant'; }
function route(){
  const r = currentRoute();
  const dash = r === 'overview' || r === 'assistant';
  document.querySelectorAll('[data-view]').forEach(el => { el.hidden = dash ? el.dataset.view !== 'dashboard' : el.dataset.view !== r; });
  document.querySelectorAll('.nav-link[data-route]').forEach(a => a.classList.toggle('active', a.dataset.route === r));
  const crumb = document.getElementById('crumb');
  crumb.dataset.i18n = ROUTES[r]; crumb.textContent = t(ROUTES[r]);
  if (!location.hash) { /* ilk ochilish: aylantirmaymiz */ }
  else if (r === 'overview') window.scrollTo({ top: 0, behavior: 'smooth' });
  else if (r === 'assistant') document.getElementById('assistant').scrollIntoView({ behavior: 'smooth', block: 'start' });
  else window.scrollTo({ top: 0 });
  VIEWS[r]?.();
}

// ---------- Filtrlar (bir marta yuklanadi) ----------
let filterData = null;
async function filtersReady(){
  if (!filterData) filterData = await api('/api/v1/filters');
  return filterData;
}
function fillSelect(sel, first, items, value){
  const cur = sel.value;
  sel.innerHTML = `<option value="">${esc(first)}</option>` + items.map(([v, l]) => `<option value="${esc(v)}">${esc(l)}</option>`).join('');
  sel.value = value ?? cur;
}
function yearOptions(sel){ fillSelect(sel, t('vAllYears'), filterData.years.map(y => [y, y])); }

// ---------- Bitimlar ----------
const dealsState = { page: 1, size: 25 };
async function viewDeals(){
  await filtersReady();
  yearOptions(fYear);
  fillSelect(fProduct, t('vAllProducts'), filterData.products.map(p => [p.product, productName(p)]));
  fillSelect(fRegion, t('vAllRegions'), filterData.regions.map(r => [r.region_key, r.region]));
  fillSelect(fStatus, t('vAllStatuses'), filterData.statuses.map(s => [s.status, statusName(s.status)]));
  loadDeals();
}
let dealsSeq = 0, partSeq = 0;  // eskirgan (kech kelgan) javob yangisining ustiga yozilmasin
async function loadDeals(){
  const body = document.getElementById('dealsRows');
  const my = ++dealsSeq;
  body.innerHTML = loadingRow(8);
  let d;
  try {
    d = await api('/api/v1/deals', { year: fYear.value, product: fProduct.value, region: fRegion.value, status: fStatus.value, q: fQuery.value.trim(), page: dealsState.page, size: dealsState.size });
  } catch { if (my === dealsSeq) body.innerHTML = emptyRow(8); return; }
  if (my !== dealsSeq) return;
  body.innerHTML = d.rows.length ? d.rows.map(r => `
    <tr class="click-row" data-deal="${r.deal_id}">
      <td><strong>${r.deal_id}</strong><small>${fmtDate(r.deal_date)} · ${esc((r.deal_time || '').slice(0, 5))}</small></td>
      <td><span class="cell-main">${esc(productName(r))}</span><small>${esc(r.product_spec)}</small></td>
      <td>${esc(r.region)}</td>
      <td class="num">${fmtNum(r.volume)} ${esc(unitName(r.unit))}</td>
      <td class="num">${fmtCompact(r.amount)} ${r.currency === 'USD' ? 'USD' : (currentLang === 'ru' ? 'сум' : 'so‘m')}</td>
      <td class="num">${fmtNum(r.unit_price)}</td>
      <td><span class="cell-main">${esc(r.seller || r.seller_inn)}</span><small>→ ${esc(r.buyer || r.buyer_inn)}</small></td>
      <td><span class="status-pill ${statusClass(r.status)}">${esc(statusName(r.status))}</span></td>
    </tr>`).join('') : emptyRow(8);
  const a = d.total ? (d.page - 1) * d.size + 1 : 0, b = Math.min(d.page * d.size, d.total);
  document.getElementById('dealsInfo').textContent = t('vShown')(fmtInt(a), fmtInt(b), fmtInt(d.total));
  dealsPrev.disabled = d.page <= 1; dealsNext.disabled = b >= d.total;
  body.querySelectorAll('[data-deal]').forEach(tr => tr.onclick = () => askFromCard(t('qDeal')(tr.dataset.deal)));
}
const fYear = document.getElementById('fYear'), fProduct = document.getElementById('fProduct'), fRegion = document.getElementById('fRegion'),
      fStatus = document.getElementById('fStatus'), fQuery = document.getElementById('fQuery'),
      dealsPrev = document.getElementById('dealsPrev'), dealsNext = document.getElementById('dealsNext');
[fYear, fProduct, fRegion, fStatus].forEach(s => s.addEventListener('change', () => { dealsState.page = 1; loadDeals(); }));
fQuery.addEventListener('input', debounce(() => { dealsState.page = 1; loadDeals(); }, 400));
document.getElementById('fReset').onclick = () => { [fYear, fProduct, fRegion, fStatus].forEach(s => s.value = ''); fQuery.value = ''; dealsState.page = 1; loadDeals(); };
dealsPrev.onclick = () => { dealsState.page--; loadDeals(); };
dealsNext.onclick = () => { dealsState.page++; loadDeals(); };

// ---------- Tovarlar ----------
const pYear = document.getElementById('pYear');
async function viewProducts(){
  await filtersReady();
  yearOptions(pYear);
  const body = document.getElementById('productRows');
  body.innerHTML = loadingRow(8);
  let d;
  try { d = await api('/api/v1/products', { year: pYear.value }); } catch { body.innerHTML = emptyRow(8); return; }
  const total = d.rows.reduce((s, r) => s + (r.turnover_uzs || 0), 0) || 1;
  body.innerHTML = d.rows.map(r => {
    const share = (r.turnover_uzs || 0) / total * 100;
    const price = r.avg_price_uzs ? `${fmtNum(Math.round(r.avg_price_uzs))} <small class="inline">${esc(t('vPerUnit'))} ${esc(unitName(r.price_unit))}</small>` : `<small class="inline">${esc(r.units.split('/').map(unitName).join(' / '))}</small>`;
    return `<tr class="click-row" data-product="${esc(productName(r))}">
      <td><span class="cell-main">${esc(productName(r))}</span><small>${esc(currentLang === 'ru' ? r.product_uz : r.product)}</small></td>
      <td><span class="category-tag">${esc(r.category)}</span></td>
      <td class="num">${fmtInt(r.deals)}</td>
      <td class="num">${fmtCompact(r.turnover_uzs || 0)}</td>
      <td><span class="share-bar"><i style="width:${Math.max(1, share).toFixed(1)}%"></i></span><small class="inline">${share.toFixed(1)}%</small></td>
      <td class="num">${r.volume_tonnes ? fmtNum(Math.round(r.volume_tonnes)) : '—'}</td>
      <td class="num">${price}</td>
      <td><button type="button" class="ask-btn">${esc(t('vAsk'))}</button></td>
    </tr>`;
  }).join('') || emptyRow(8);
  body.querySelectorAll('[data-product]').forEach(tr => tr.onclick = () => askFromCard(t('qProduct')(tr.dataset.product, pYear.value)));
}
pYear.addEventListener('change', viewProducts);

// ---------- Ishtirokchilar ----------
let partRole = 'buyer';
const partYear = document.getElementById('partYear'), partQuery = document.getElementById('partQuery');
async function viewParticipants(){
  await filtersReady();
  yearOptions(partYear);
  loadParticipants();
}
async function loadParticipants(){
  const head = document.getElementById('partHead'), body = document.getElementById('partRows');
  const broker = partRole === 'broker';
  head.innerHTML = `<tr><th>#</th><th>${esc(t('vColName'))}</th><th>${esc(t('vColId'))}</th><th>${esc(t('vColRegion'))}</th><th>${esc(t(broker ? 'vColSides' : 'vColActivity'))}</th><th class="num">${esc(t('vColDeals'))}</th>${broker ? '' : `<th class="num">${esc(t('vColProducts'))}</th>`}<th class="num">${esc(t('vColTurnover'))}</th></tr>`;
  const cols = broker ? 7 : 8;
  const my = ++partSeq;
  body.innerHTML = loadingRow(cols);
  let d;
  try { d = await api('/api/v1/participants', { role: partRole, year: partYear.value, q: partQuery.value.trim(), limit: 50 }); } catch { if (my === partSeq) body.innerHTML = emptyRow(cols); return; }
  if (my !== partSeq) return;
  body.innerHTML = d.rows.map((r, i) => `<tr class="click-row" data-id="${esc(r.id)}">
      <td>${i + 1}</td>
      <td><span class="cell-main">${esc(r.name)}</span></td>
      <td><code>${esc(r.id)}</code></td>
      <td>${esc(r.region)}</td>
      <td>${broker ? `${fmtInt(r.seller_side)} / ${fmtInt(r.buyer_side)}` : esc(r.activity)}</td>
      <td class="num">${fmtInt(r.deals)}</td>
      ${broker ? '' : `<td class="num">${r.products}</td>`}
      <td class="num">${fmtCompact(r.turnover_uzs || 0)}</td>
    </tr>`).join('') || emptyRow(cols);
  body.querySelectorAll('[data-id]').forEach(tr => tr.onclick = () =>
    askFromCard(broker ? t('qBroker')(tr.dataset.id) : t('qCompany')(tr.dataset.id, partRole)));
}
document.querySelectorAll('#roleTabs [data-role]').forEach(b => b.onclick = () => {
  partRole = b.dataset.role;
  document.querySelectorAll('#roleTabs [data-role]').forEach(x => x.classList.toggle('active', x === b));
  loadParticipants();
});
partYear.addEventListener('change', loadParticipants);
partQuery.addEventListener('input', debounce(loadParticipants, 400));

// ---------- Ma'lumotlar manbasi ----------
let sourceData = null;
async function viewSources(){
  document.getElementById('srcFiles').innerHTML = t('vFiles').map(([f, d]) => `<div class="file-row"><code>${esc(f)}</code><span>${esc(d)}</span></div>`).join('');
  document.getElementById('srcRules').innerHTML = t('vRulesList').map(r => `<li>${esc(r)}</li>`).join('');
  const box = document.getElementById('srcTables');
  if (!sourceData) { box.textContent = t('vLoading'); try { sourceData = await api('/api/v1/sources'); } catch { box.textContent = '—'; return; } }
  box.innerHTML = sourceData.tables.map(tb => `<details class="answer-details table-details"><summary><code>${esc(tb.table)}</code> · ${fmtInt(tb.rows)} ${esc(t('vRows'))} · ${tb.columns.length} ${esc(t('vCols'))}</summary>
    <div class="col-chips">${tb.columns.map(c => `<span><b>${esc(c.column_name)}</b> ${esc(c.data_type.toLowerCase())}</span>`).join('')}</div></details>`).join('');
}

// ---------- Sozlamalar ----------
async function viewSettings(){
  const S = settings();
  document.querySelectorAll('[data-setting]').forEach(cb => { cb.checked = !!S[cb.dataset.setting]; });
  document.querySelectorAll('#setLang [data-lang]').forEach(b => b.classList.toggle('active', b.dataset.lang === currentLang));
  try {
    const h = await api('/api/health');
    document.getElementById('setModel').textContent = h.model;
    document.getElementById('setFallbacks').innerHTML = (h.models || []).filter(m => m !== h.model).map(m => `<code>${esc(m)}</code>`).join('');
  } catch {}
  document.getElementById('setData').textContent = document.getElementById('sidePeriod').textContent;
}
document.querySelectorAll('[data-setting]').forEach(cb => cb.addEventListener('change', () => {
  store.set('sq_settings', { ...settings(), [cb.dataset.setting]: cb.checked });
  showToast(t('vSaved'));
}));
document.querySelectorAll('#setLang [data-lang]').forEach(b => b.onclick = () => applyLanguage(b.dataset.lang));
document.getElementById('setClearHistory').onclick = () => document.getElementById('viewAll').click();
document.getElementById('setNewChat').onclick = () => { document.getElementById('clearChat').click(); location.hash = '#/assistant'; };

const VIEWS = { deals: viewDeals, commodities: viewProducts, participants: viewParticipants, sources: viewSources, settings: viewSettings };

window.addEventListener('hashchange', route);
document.addEventListener('langchange', () => { const r = currentRoute(); const c = document.getElementById('crumb'); c.textContent = t(ROUTES[r]); VIEWS[r]?.(); });
applyLanguage(currentLang);
route();
