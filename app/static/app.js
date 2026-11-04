const translations = {
  uz: {
    workspace:'ISH MAYDONI', overview:'Umumiy ko‘rinish', aiAnalyst:'AI tahlilchi', deals:'Bitimlar', commodities:'Tovarlar', participants:'Ishtirokchilar', system:'TIZIM', dataSources:'Ma’lumotlar manbasi', settings:'Sozlamalar', datasetReady:'Dataset tayyor', dealsLoaded:'bitim yozuvi yuklangan', demoWorkspace:'Demo workspace', dataConnected:'Ma’lumotlar ulangan', dataOffline:'Server bilan aloqa yo‘q', exchangeIntelligence:'BIRJA INTELLEKTI', pageTitle:'Savollaringizga <em>aniq javoblar.</em>', pageSubtitle:'UZEX bitimlari bo‘yicha ma’lumotlarni tahlil qiling. Savol bering — tekshirilgan natijani oling.', dataSnapshot:'MA’LUMOTLAR HOLATI', snapshotNote:'Datasetning oxirgi sanasi', totalDeals:'Jami bitimlar', fiveYearsData:'2022–2026 yillar ma’lumoti', contracts:'Shartnomalar', contractCards:'shartnoma kartochkasi', companies:'Ishtirokchilar', participantRecords:'kompaniya yozuvi', brokers:'Brokerlar', brokerFirms:'brokerlik tashkiloti', assistantTitle:'UZEX AI yordamchi', assistantReady:'Savollaringizni kutyapti', assistantBusy:'Ma’lumotlarni tahlil qilyapti…', liveMode:'JONLI REJIM', newConversation:'YANGI SUHBAT', now:'hozir', you:'Siz', welcomeText:'Assalomu alaykum! Men UZEX birja bitimlari bo‘yicha AI tahlilchiman. Savolingizni o‘zbek yoki rus tilida yozing — ma’lumotlar doirasida javob beraman.', groundedNote:'Javoblar faqat datasetdagi ma’lumotlarga tayanadi — har bir raqam SQL so‘rov natijasidan olinadi.', tryAsking:'QUYIDAGILARDAN BIRINI SO‘RANG', suggestion1:'2025-yilda nechta bitim tuzilgan?', suggestion2:'Yillar bo‘yicha bitimlarni taqqosla', suggestion3:'Dataset tarkibini tushuntir', suggestion4:'2025-yilda eng ko‘p savdo qilingan 5 ta tovar', messagePlaceholder:'Savolingizni kiriting...', sendHint:'yuborish', languageHint:'UZ / RU', send:'Yuborish', liveDisclaimer:'Javoblar DuckDB bazasida bajarilgan SQL natijalariga asoslanadi. Dataset sun’iy (synthetic) ma’lumotlardan iborat.', datasetOverview:'DATASET TAHLILI', dealsByYear:'Yillar bo‘yicha bitimlar', allDeals:'jami bitim', dealCount:'Bitimlar soni', partialYear:'* 2026 — 30-oktabrgacha', agentCapabilities:'AGENT IMKONIYATLARI', whatCanDo:'Nimalarni tahlil qiladi?', cap1Title:'Bitimlar statistikasi', cap1Desc:'Sana, miqdor va savdo hajmi', cap2Title:'Tovarlar tahlili', cap2Desc:'Mahsulotlar va narx dinamikasi', cap3Title:'Ishtirokchilar', cap3Desc:'Sotuvchi, xaridor va brokerlar', cap4Title:'Shartnoma holati', cap4Desc:'To‘lov va yetkazib berish', trustTitle:'Manbaga asoslangan javob', trustText:'Agent mavjud bo‘lmagan ma’lumotni taxmin qilmaydi: har bir javob ostida ishlatilgan SQL, filtrlar va natija jadvali ko‘rsatiladi.', activity:'FAOLIYAT', recentQueries:'So‘nggi so‘rovlar', viewAll:'Tarixni tozalash', question:'SAVOL', category:'KATEGORIYA', language:'TIL', tableStatus:'HOLAT', time:'VAQT', footerNote:'Hackathon prototipi · Sun’iy dataset asosida', noRecent:'Hali so‘rov berilmadi — birinchi savolingizni yozing.',
    sourceLabel:'Manba', cached:'keshdan', metricDeals:'Bitimlar soni', metricTurnover:'Aylanma, so‘m', metricCancel:'Bekor qilinganlar, %', allTurnover:'jami aylanma, so‘m', avgCancel:'o‘rtacha bekor qilish ulushi', askAboutChart:'AI’dan tahlil so‘rash', profileNote:'Demo workspace · ma’lumotlar sun’iy', clickToAsk:'Bosing — AI tahlil qiladi', filtersLabel:'Filtrlar', sqlLabel:'SQL so‘rovlar', tableLabel:'Natija jadvali', rowsLabel:'qator', secLabel:'s', stepsLabel:'qadam', chartLabel:'Grafik',
    statusOk:'OK', statusNoData:'Ma’lumot yo‘q', statusError:'Xato', statusBusy:'Limit',
    answerReady:'Javob tayyor', errorToast:'So‘rov bajarilmadi', copied:'Nusxa olindi', historyCleared:'Tarix tozalandi', settingsSoon:'Sozlamalar keyingi versiyada',
    helpText:'Savolni o‘zbek (lotin/kirill) yoki rus tilida yozing. Masalan: «2024-yilda karbamid o‘rtacha narxi», «STIR 921912462 qancha sotgan?»',
    askCommodities:'2025-yilda qaysi tovarlar bo‘yicha savdo aylanmasi eng yuqori bo‘lgan?', askParticipants:'2025-yilda eng yirik 5 ta xaridor kim?',
    cat:{price:'Narx tahlili', broker:'Brokerlar', party:'Ishtirokchilar', export:'Eksport', status:'Shartnoma holati', trend:'Trend tahlili', product:'Tovarlar', stat:'Statistika'},
  },
  ru: {
    workspace:'РАБОЧАЯ ОБЛАСТЬ', overview:'Обзор', aiAnalyst:'AI аналитик', deals:'Сделки', commodities:'Товары', participants:'Участники', system:'СИСТЕМА', dataSources:'Источники данных', settings:'Настройки', datasetReady:'Датасет готов', dealsLoaded:'записей сделок загружено', demoWorkspace:'Демо-пространство', dataConnected:'Данные подключены', dataOffline:'Нет связи с сервером', exchangeIntelligence:'БИРЖЕВАЯ АНАЛИТИКА', pageTitle:'Точные ответы <em>на ваши вопросы.</em>', pageSubtitle:'Анализируйте данные биржевых сделок UZEX. Задайте вопрос — получите проверенный результат.', dataSnapshot:'СОСТОЯНИЕ ДАННЫХ', snapshotNote:'Последняя дата датасета', totalDeals:'Всего сделок', fiveYearsData:'Данные за 2022–2026 годы', contracts:'Контракты', contractCards:'карточек контрактов', companies:'Участники', participantRecords:'записей компаний', brokers:'Брокеры', brokerFirms:'брокерских организаций', assistantTitle:'UZEX AI помощник', assistantReady:'Готов к вашим вопросам', assistantBusy:'Анализирую данные…', liveMode:'РАБОЧИЙ РЕЖИМ', newConversation:'НОВЫЙ ДИАЛОГ', now:'сейчас', you:'Вы', welcomeText:'Здравствуйте! Я AI-аналитик биржевых сделок UZEX. Задайте вопрос на узбекском или русском языке — я отвечу в рамках доступных данных.', groundedNote:'Ответы основаны только на данных датасета — каждое число берётся из результата SQL-запроса.', tryAsking:'ПОПРОБУЙТЕ СПРОСИТЬ', suggestion1:'Сколько сделок заключено в 2025 году?', suggestion2:'Сравни количество сделок по годам', suggestion3:'Объясни состав датасета', suggestion4:'Топ-5 товаров по объёму торгов в 2025 году', messagePlaceholder:'Введите ваш вопрос...', sendHint:'отправить', languageHint:'UZ / RU', send:'Отправить', liveDisclaimer:'Ответы основаны на результатах SQL-запросов к базе DuckDB. Датасет состоит из синтетических данных.', datasetOverview:'АНАЛИЗ ДАТАСЕТА', dealsByYear:'Сделки по годам', allDeals:'всего сделок', dealCount:'Количество сделок', partialYear:'* 2026 — по 30 октября', agentCapabilities:'ВОЗМОЖНОСТИ АГЕНТА', whatCanDo:'Что анализирует?', cap1Title:'Статистика сделок', cap1Desc:'Дата, количество и объём торгов', cap2Title:'Анализ товаров', cap2Desc:'Продукты и динамика цен', cap3Title:'Участники', cap3Desc:'Продавцы, покупатели и брокеры', cap4Title:'Статус контрактов', cap4Desc:'Оплата и поставка', trustTitle:'Ответы на основе источников', trustText:'Агент не выдумывает отсутствующие данные: под каждым ответом показаны SQL, фильтры и таблица результата.', activity:'АКТИВНОСТЬ', recentQueries:'Последние запросы', viewAll:'Очистить историю', question:'ВОПРОС', category:'КАТЕГОРИЯ', language:'ЯЗЫК', tableStatus:'СТАТУС', time:'ВРЕМЯ', footerNote:'Прототип хакатона · На синтетическом датасете', noRecent:'Запросов пока нет — задайте первый вопрос.',
    sourceLabel:'Источник', cached:'из кэша', metricDeals:'Количество сделок', metricTurnover:'Оборот, сум', metricCancel:'Аннулировано, %', allTurnover:'общий оборот, сум', avgCancel:'средняя доля аннулирования', askAboutChart:'Спросить анализ у AI', profileNote:'Демо-пространство · данные синтетические', clickToAsk:'Нажмите — AI проанализирует', filtersLabel:'Фильтры', sqlLabel:'SQL-запросы', tableLabel:'Таблица результата', rowsLabel:'строк', secLabel:'с', stepsLabel:'шагов', chartLabel:'График',
    statusOk:'OK', statusNoData:'Нет данных', statusError:'Ошибка', statusBusy:'Лимит',
    answerReady:'Ответ готов', errorToast:'Запрос не выполнен', copied:'Скопировано', historyCleared:'История очищена', settingsSoon:'Настройки в следующей версии',
    helpText:'Пишите вопрос на русском или узбекском. Например: «Средняя цена карбамида в 2024 году», «Сколько продала компания с ИНН 921912462?»',
    askCommodities:'По каким товарам оборот торгов в 2025 году был максимальным?', askParticipants:'Кто 5 крупнейших покупателей в 2025 году?',
    cat:{price:'Анализ цен', broker:'Брокеры', party:'Участники', export:'Экспорт', status:'Статус контрактов', trend:'Тренды', product:'Товары', stat:'Статистика'},
  }
};
const SUGGESTION_QUERIES = {
  uz: ['2025-yilda nechta bitim tuzilgan?', 'Yillar bo‘yicha bitimlar sonini taqqosla.', 'Datasetda qanday ma’lumotlar mavjud?', '2025-yilda eng ko‘p savdo qilingan 5 ta tovar qaysi?'],
  ru: ['Сколько сделок заключено в 2025 году?', 'Сравни количество сделок по годам.', 'Какие данные доступны в датасете?', 'Топ-5 товаров по объёму торгов в 2025 году'],
};

const CARD_QUERIES = {
  uz: {
    cap: ['2025-yilda oylar bo‘yicha bitimlar soni va savdo aylanmasi qanday bo‘lgan?',
          '2024-yilda karbamidning 1 tonnasi oylar bo‘yicha o‘rtacha qanchadan sotilgan?',
          '2025-yilda savdo summasi bo‘yicha eng yirik 5 ta xaridor kim?',
          '2026-yilda bitimlar holati bo‘yicha qanday taqsimlangan (ijro etilgan, bekor qilingan, qisman va h.k.)?'],
    metric: ['Yillar bo‘yicha bitimlar soni va savdo aylanmasini taqqosla.',
             'Shartnomalar tovar kategoriyalari bo‘yicha qanday taqsimlangan?',
             'Bitimlar soni bo‘yicha eng faol 5 ta xaridor kim?',
             'Bitimlar soni bo‘yicha top-5 broker (xaridor tomonida) kim?'],
    year: y => `${y}-yil bo‘yicha asosiy ko‘rsatkichlar: bitimlar soni, aylanma, bekor qilinganlar ulushi va eng ko‘p sotilgan tovar.`,
    chart: m => ({deals: 'Yillar bo‘yicha bitimlar soni qanday o‘zgargan va o‘sish sur’ati qancha?', turnover: 'Yillar bo‘yicha savdo aylanmasi so‘mda qanday o‘zgargan?', cancel: 'Yillar bo‘yicha bekor qilingan bitimlar ulushi qanday o‘zgargan?'})[m],
  },
  ru: {
    cap: ['Каким было количество сделок и оборот по месяцам в 2025 году?',
          'Какова средняя цена тонны карбамида по месяцам в 2024 году?',
          'Кто 5 крупнейших покупателей по сумме сделок в 2025 году?',
          'Как распределились сделки 2026 года по статусам (исполнены, аннулированы, частично и т.д.)?'],
    metric: ['Сравни количество сделок и оборот по годам.',
             'Как контракты распределены по категориям товаров?',
             'Кто 5 самых активных покупателей по числу сделок?',
             'Топ-5 брокеров покупателя по числу сделок.'],
    year: y => `Основные показатели за ${y} год: число сделок, оборот, доля аннулированных и самый продаваемый товар.`,
    chart: m => ({deals: 'Как менялось количество сделок по годам и каковы темпы роста?', turnover: 'Как менялся оборот торгов в сумах по годам?', cancel: 'Как менялась доля аннулированных сделок по годам?'})[m],
  },
};
let yearStats = null;
let yearMetric = 'deals';
let currentLang = 'uz';
let conversationId = null;
let busy = false;
const chatArea = document.getElementById('chatArea');
const input = document.getElementById('messageInput');
const form = document.getElementById('chatForm');
const recentRows = document.getElementById('recentRows');
const toast = document.getElementById('toast');
const sendButton = form.querySelector('.send-button');

const store = {
  get(k, d) { try { const v = localStorage.getItem(k); return v === null ? d : JSON.parse(v); } catch { return d; } },
  set(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch {} },
};

function t(key){ return translations[currentLang][key] ?? translations.uz[key] ?? key; }
function esc(s){ return String(s ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c])); }
function timeNow(){ return new Date().toLocaleTimeString('ru-RU', {hour:'2-digit', minute:'2-digit'}); }
const fmtInt = n => Number(n).toLocaleString('en-US');
const DEFAULT_SETTINGS = { charts: true, openSql: false, openTable: false };
function settings(){ return { ...DEFAULT_SETTINGS, ...store.get('sq_settings', {}) }; }

function fmtNum(v){
  if (typeof v !== 'number') return v === null || v === undefined ? '—' : esc(v);
  return v.toLocaleString('ru-RU', {maximumFractionDigits: 2}).replace(/ /g, ' ');
}
function fmtCompact(v){
  if (typeof v !== 'number') return esc(v);
  const units = currentLang === 'ru' ? ['', 'тыс', 'млн', 'млрд', 'трлн'] : ['', 'ming', 'mln', 'mlrd', 'trln'];
  let i = 0, x = Math.abs(v);
  while (x >= 1000 && i < units.length - 1) { x /= 1000; i++; }
  const s = (v < 0 ? -x : x).toLocaleString('ru-RU', {maximumFractionDigits: x < 10 && i ? 1 : 0}).replace(/ /g, ' ');
  return i ? `${s} ${units[i]}` : fmtNum(v);
}
const RAW_COL = /(^|_)(year|month|day|id|inn|code|yil|oy|stir)$/i;
function fmtCell(v, col){ return typeof v === 'number' && RAW_COL.test(col) ? String(v) : fmtNum(v); }
function prettyCol(c){ return esc(String(c).replace(/_/g, ' ')); }

// --- Javob matni: sodda Markdown -> HTML ---
function inline(s){
  return esc(s).replace(/\*\*(.+?)\*\*/g, '<b>$1</b>').replace(/`([^`]+)`/g, '<code>$1</code>')
    .replace(/(^|[^*\w])\*([^*\n]+)\*(?!\w)/g, '$1<i>$2</i>');
}
function md(text){
  const out = []; let list = null;
  for (const raw of String(text).split('\n')) {
    const line = raw.trimEnd();
    const ul = line.match(/^\s*[-•*]\s+(.*)/), ol = line.match(/^\s*\d+[.)]\s+(.*)/);
    if (ul || ol) {
      const tag = ul ? 'ul' : 'ol';
      if (list !== tag) { if (list) out.push(`</${list}>`); out.push(`<${tag}>`); list = tag; }
      out.push(`<li>${inline((ul || ol)[1])}</li>`);
      continue;
    }
    if (list) { out.push(`</${list}>`); list = null; }
    if (line.trim()) out.push(`<p>${inline(line)}</p>`);
  }
  if (list) out.push(`</${list}>`);
  return out.join('');
}

// --- Grafiklar ---
function chartHtml(viz){
  if (!viz || !viz.values || !viz.values.length) return '';
  const vals = viz.values.map(v => typeof v === 'number' ? v : 0);
  const max = Math.max(...vals.map(Math.abs), 1);
  const title = `<div class="answer-chart-title"><span class="legend-square"></span>${prettyCol(viz.title)}</div>`;
  if (viz.type === 'hbar') {
    const rows = viz.labels.map((l, i) => `
      <div class="hbar-row" title="${esc(l)}: ${fmtNum(viz.values[i])}">
        <span class="hbar-label">${esc(l)}</span>
        <span class="hbar-track"><i style="width:${Math.max(2, Math.abs(vals[i]) / max * 100).toFixed(1)}%"></i></span>
        <span class="hbar-value">${fmtCompact(viz.values[i])}</span>
      </div>`).join('');
    return `<div class="answer-chart">${title}<div class="hbar-list">${rows}</div></div>`;
  }
  if (viz.type === 'line') {
    const W = 520, H = 150, P = 6, n = vals.length;
    const min = Math.min(...vals, 0);
    const x = i => P + i * (W - 2 * P) / (n - 1), y = v => H - P - (v - min) / ((max - min) || 1) * (H - 2 * P);
    const pts = vals.map((v, i) => `${x(i).toFixed(1)},${y(v).toFixed(1)}`).join(' ');
    const dots = vals.map((v, i) => `<circle cx="${x(i).toFixed(1)}" cy="${y(v).toFixed(1)}" r="2.6"><title>${esc(viz.labels[i])}: ${fmtNum(viz.values[i])}</title></circle>`).join('');
    const step = Math.ceil(n / 6);
    const ticks = viz.labels.map((l, i) => i % step === 0 || i === n - 1 ? `<span style="left:${(x(i) / W * 100).toFixed(1)}%">${esc(l)}</span>` : '').join('');
    return `<div class="answer-chart">${title}
      <svg class="line-chart" viewBox="0 0 ${W} ${H}" preserveAspectRatio="none" role="img">
        <polygon points="${P},${H - P} ${pts} ${W - P},${H - P}" class="line-area"/>
        <polyline points="${pts}" class="line-path"/>${dots}
      </svg><div class="line-ticks">${ticks}</div>
      <div class="line-range"><span>min ${fmtCompact(Math.min(...vals))}</span><span>max ${fmtCompact(Math.max(...vals))}</span></div></div>`;
  }
  const bars = viz.labels.map((l, i) => `
    <div class="bar-item${vals[i] === Math.max(...vals) ? ' highlighted' : ''}">
      <div class="bar-value">${fmtCompact(viz.values[i])}</div>
      <div class="bar" style="--bar-height:${Math.max(3, Math.abs(vals[i]) / max * 92).toFixed(1)}%"></div><span>${esc(l)}</span>
    </div>`).join('');
  return `<div class="answer-chart">${title}<div class="bar-chart answer-bars"><div class="chart-bars">${bars}</div></div></div>`;
}

function tableHtml(tbl){
  if (!tbl || !tbl.columns || !tbl.columns.length || !tbl.rows.length) return '';
  const head = tbl.columns.map(c => `<th>${prettyCol(c)}</th>`).join('');
  const body = tbl.rows.map(r => '<tr>' + r.map((v, i) => `<td class="${typeof v === 'number' ? 'num' : ''}">${fmtCell(v, tbl.columns[i])}</td>`).join('') + '</tr>').join('');
  return `<div class="result-table"><table><thead><tr>${head}</tr></thead><tbody>${body}</tbody></table></div>`;
}

// --- Xabarlar ---
function messageEl(kind){
  const wrap = document.createElement('div');
  wrap.className = `message ${kind === 'user' ? 'user-message' : 'assistant-message'}`;
  wrap.innerHTML = `<div class="message-avatar">${kind === 'user' ? 'SA' : '✳'}</div>
    <div class="message-body"><div class="message-author">${kind === 'user' ? esc(t('you')) : 'UZEX AI'} <span>• ${esc(t('now'))} · ${timeNow()}</span></div>
    <div class="message-bubble"></div></div>`;
  chatArea.appendChild(wrap);
  chatArea.scrollTop = chatArea.scrollHeight;
  return wrap.querySelector('.message-bubble');
}

function renderAnswer(bubble, data){
  bubble.classList.add('answer-bubble');
  if (data.status === 'error' || data.status === 'busy') bubble.classList.add('error-bubble');
  let html = md(data.answer || '');
  const tbl = data.table;
  const firstBold = (data.answer || '').match(/\*\*(.+?)\*\*/);
  if (data.status === 'ok' && tbl && tbl.rows && tbl.rows.length === 1 && firstBold && firstBold[1].length <= 40)
    html = `<div class="answer-result"><strong>${esc(firstBold[1])}</strong></div>` + html;
  const S = settings();
  if (data.visualization && S.charts) html += chartHtml(data.visualization);
  const src = data.source;
  if (src) {
    const meta = [src.tables && src.tables.length ? `${t('sourceLabel')}: ${src.tables.join(', ')}` : '',
                  `${src.sql.length} SQL`, `${src.steps} ${t('stepsLabel')}`, src.seconds ? `${src.seconds} ${t('secLabel')}` : `⚡ ${t('cached')}`, src.model].filter(Boolean);
    html += `<div class="answer-meta">${meta.map(esc).join(' · ')}</div>`;
    if (src.filters && src.filters.length)
      html += `<div class="answer-filters"><span>${esc(t('filtersLabel'))}:</span>${src.filters.map(f => typeof f === 'string' || f.code ? `<code>${esc(f.text ?? f)}</code>` : `<span class="filter-chip">${esc(f.text)}</span>`).join('')}</div>`;
    html += `<details class="answer-details"${S.openSql ? ' open' : ''}><summary>${esc(t('sqlLabel'))} (${src.sql.length})</summary>${src.sql.map(s => `<pre class="sql-block">${esc(s.trim())}</pre>`).join('')}<button type="button" class="text-button copy-sql">⧉ SQL</button></details>`;
  }
  if (tbl && tbl.rows && tbl.rows.length > 1)
    html += `<details class="answer-details"${S.openTable ? ' open' : ''}><summary>${esc(t('tableLabel'))} · ${tbl.rows.length}${tbl.truncated ? '+' : ''} ${esc(t('rowsLabel'))}</summary>${tableHtml(tbl)}</details>`;
  bubble.innerHTML = html;
  const copy = bubble.querySelector('.copy-sql');
  if (copy) copy.onclick = () => { navigator.clipboard?.writeText(src.sql.join(';\n\n')).then(() => showToast(t('copied'))).catch(() => {}); };
}

function welcome(){
  chatArea.innerHTML = `<div class="date-divider"><span>${esc(t('newConversation'))}</span></div>
    <div class="message assistant-message"><div class="message-avatar">✳</div><div class="message-body">
      <div class="message-author">UZEX AI <span>• ${esc(t('now'))}</span></div>
      <div class="message-bubble welcome-bubble"><p>${esc(t('welcomeText'))}</p>
      <div class="welcome-note"><span>✦</span><span>${esc(t('groundedNote'))}</span></div></div></div></div>`;
  chatArea.appendChild(suggestionsBlock);
  suggestionsBlock.style.display = 'block';
}

// --- So'nggi so'rovlar ---
function categorize(q){
  const s = q.toLowerCase();
  if (/narx|цен|стоим|qimmat|arzon/.test(s)) return 'price';
  if (/broker|брокер/.test(s)) return 'broker';
  if (/eksport|экспорт|dollar|доллар|usd/.test(s)) return 'export';
  if (/xaridor|sotuvchi|kompaniya|stir|покупат|продав|компан|инн|участник|ishtirokchi/.test(s)) return 'party';
  if (/bekor|аннул|to‘lov|to'lov|оплат|yetkaz|постав|holat|статус|qisman|частич/.test(s)) return 'status';
  if (/tovar|товар|mahsulot|продукт|paxta|хлоп|karbamid|карбамид|sement|цемент|benzin|бензин/.test(s)) return 'product';
  if (/yillar|oylar|dinamika|taqqos|trend|по годам|по месяц|динамик|сравн/.test(s)) return 'trend';
  return 'stat';
}
let recent = store.get('sq_recent', []);
function renderRecent(){
  if (!recent.length) {
    recentRows.innerHTML = `<tr class="empty-row"><td colspan="5">${esc(t('noRecent'))}</td></tr>`;
    return;
  }
  const label = { ok: t('statusOk'), no_data: t('statusNoData'), error: t('statusError'), busy: t('statusBusy') };
  recentRows.innerHTML = recent.map((r, i) => `<tr data-i="${i}" class="recent-row">
    <td><span class="table-question">${esc(r.q)}</span></td>
    <td><span class="category-tag">${esc(t('cat')[r.cat] || r.cat)}</span></td>
    <td>${esc(r.lang.toUpperCase())}</td>
    <td><span class="success-status ${r.status === 'ok' ? '' : 'status-' + r.status}"><i></i>${esc(label[r.status] || r.status)}${r.sec !== undefined ? ` · ${r.sec} ${esc(t('secLabel'))}` : ''}</span></td>
    <td>${esc(r.time)}</td></tr>`).join('');
  recentRows.querySelectorAll('.recent-row').forEach(tr => tr.onclick = () => {
    input.value = recent[+tr.dataset.i].q; input.focus(); document.getElementById('assistant').scrollIntoView({behavior: 'smooth'});
  });
}
function addRecent(q, lang, status, sec){
  recent.unshift({ q, cat: categorize(q), lang, status, sec, time: timeNow() });
  recent = recent.slice(0, 8);
  store.set('sq_recent', recent);
  renderRecent();
}

// --- Yuborish ---
async function sendQuestion(question){
  const q = (question || '').trim();
  if (!q || busy) return;
  busy = true; sendButton.disabled = true;
  suggestionsBlock.style.display = 'none';
  messageEl('user').textContent = q;
  const bubble = messageEl('assistant');
  bubble.innerHTML = '<span class="typing-dots"><i></i><i></i><i></i></span>';
  setAssistantState(true);
  const t0 = performance.now();
  let data;
  try {
    const r = await fetch('/api/v1/ask', { method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ question: q, language: currentLang, conversation_id: conversationId }) });
    data = await r.json().catch(() => ({ answer: `HTTP ${r.status}`, status: 'error' }));
  } catch (e) {
    data = { answer: t('dataOffline'), status: 'error' };
    setConnection(false);
  }
  if (data.conversation_id) conversationId = data.conversation_id;
  renderAnswer(bubble, data);
  chatArea.scrollTop = chatArea.scrollHeight;
  const sec = data.source ? data.source.seconds : +((performance.now() - t0) / 1000).toFixed(1);
  addRecent(q, data.language || currentLang, data.status || 'error', sec);
  showToast(data.status === 'ok' || data.status === 'no_data' ? t('answerReady') : t('errorToast'));
  setAssistantState(false);
  busy = false; sendButton.disabled = false;
  input.focus();
}

function setAssistantState(working){
  const el = document.getElementById('assistantState');
  el.dataset.i18n = working ? 'assistantBusy' : 'assistantReady';
  el.textContent = t(el.dataset.i18n);
}
function setConnection(ok){
  const el = document.getElementById('connStatus');
  el.classList.toggle('offline', !ok);
  const label = el.querySelector('span:last-child');
  label.dataset.i18n = ok ? 'dataConnected' : 'dataOffline';
  label.textContent = t(label.dataset.i18n);
}

// --- Til ---
function applyLanguage(lang){
  currentLang = lang;
  store.set('sq_lang', lang);
  document.documentElement.lang = lang;
  document.querySelectorAll('[data-i18n]').forEach(el => {
    const value = t(el.dataset.i18n);
    if (typeof value !== 'string') return;
    if (value.includes('<em>')) el.innerHTML = value; else el.textContent = value;
  });
  document.querySelectorAll('[data-i18n-placeholder]').forEach(el => el.placeholder = t(el.dataset.i18nPlaceholder));
  document.querySelectorAll('.lang-btn').forEach(btn => btn.classList.toggle('active', btn.dataset.lang === lang));
  document.querySelectorAll('.suggestion-chip').forEach((btn, i) => { btn.dataset.query = SUGGESTION_QUERIES[lang][i]; });
  document.querySelectorAll('.capability-item, .metric-card').forEach(el => { el.title = t('clickToAsk'); });
  renderRecent();
  renderYears();
  document.dispatchEvent(new Event('langchange'));
}

// --- Dashboard: bazadan jonli statistika ---
function niceTop(max){
  const p = Math.pow(10, Math.floor(Math.log10(max || 1)));
  for (const k of [1, 1.2, 1.5, 2, 2.5, 3, 4, 5, 6, 8, 10]) if (k * p >= max) return k * p;
  return 10 * p;
}
function axisLabel(v){
  if (yearMetric === 'cancel') return v ? v.toFixed(v < 10 ? 1 : 0) + '%' : '0';
  if (v >= 1e12) return (v / 1e12).toFixed(v % 1e12 ? 1 : 0) + (currentLang === 'ru' ? 'трлн' : 'trln');
  if (v >= 1e9) return Math.round(v / 1e9) + (currentLang === 'ru' ? 'млрд' : 'mlrd');
  return v ? Math.round(v / 1000) + 'k' : '0';
}
function metricValue(y){ return yearMetric === 'turnover' ? y.turnover_uzs : yearMetric === 'cancel' ? y.cancelled_pct : y.deals; }
function barLabel(v){
  if (yearMetric === 'cancel') return v.toFixed(1) + '%';
  if (yearMetric === 'turnover') return (v / 1e12).toFixed(1) + (currentLang === 'ru' ? ' трлн' : ' trln');
  return (v / 1000).toFixed(1) + 'k';
}
function renderYears(){
  if (!yearStats) return;
  const vals = yearStats.map(metricValue);
  const top = niceTop(Math.max(...vals));
  document.getElementById('yearAxis').innerHTML = [4, 3, 2, 1, 0].map(k => `<span>${axisLabel(top * k / 4)}</span>`).join('');
  const bestV = Math.max(...vals);
  const bars = yearStats.map((y, i) => {
    const cls = y.partial && yearMetric !== 'cancel' ? ' partial' : vals[i] === bestV ? ' highlighted' : '';
    return `<button type="button" class="bar-item${cls}" data-year="${y.year}" title="${esc(t('clickToAsk'))}"><div class="bar-value">${barLabel(vals[i])}</div><div class="bar" style="--bar-height:${(vals[i] / top * 100).toFixed(2)}%"></div><span>${y.year}${y.partial ? '*' : ''}</span></button>`;
  }).join('');
  const box = document.getElementById('yearBars');
  box.innerHTML = '<div class="chart-grid-lines"><i></i><i></i><i></i><i></i><i></i></div>' + bars;
  box.querySelectorAll('.bar-item').forEach(b => b.onclick = () => askFromCard(CARD_QUERIES[currentLang].year(b.dataset.year)));
  const total = document.getElementById('chartTotal'), totalLabel = total.nextElementSibling;
  if (yearMetric === 'turnover') {
    total.textContent = fmtCompact(vals.reduce((a, b) => a + b, 0)); totalLabel.dataset.i18n = 'allTurnover';
  } else if (yearMetric === 'cancel') {
    const all = yearStats.reduce((a, y) => a + y.deals, 0), canc = yearStats.reduce((a, y) => a + y.deals * y.cancelled_pct / 100, 0);
    total.textContent = (canc / all * 100).toFixed(1) + '%'; totalLabel.dataset.i18n = 'avgCancel';
  } else {
    total.textContent = fmtInt(yearStats.reduce((a, y) => a + y.deals, 0)); totalLabel.dataset.i18n = 'allDeals';
  }
  totalLabel.textContent = t(totalLabel.dataset.i18n);
  const legend = document.querySelector('.chart-legend > span > span');
  legend.dataset.i18n = {deals: 'dealCount', turnover: 'metricTurnover', cancel: 'metricCancel'}[yearMetric];
  legend.textContent = t(legend.dataset.i18n);
  document.querySelectorAll('.chart-pop [data-metric]').forEach(b => b.classList.toggle('active', b.dataset.metric === yearMetric));
}
async function loadStats(){
  try {
    const r = await fetch('/api/v1/stats');
    if (!r.ok) throw new Error(r.status);
    const s = await r.json();
    setConnection(true);
    for (const [id, v] of [['statDeals', s.deals], ['sideDeals', s.deals], ['chartTotal', s.deals], ['statContracts', s.contracts], ['statCompanies', s.companies], ['statBrokers', s.brokers]])
      document.getElementById(id).textContent = fmtInt(v);
    const d = s.last_date.split('-').reverse().join('.');
    document.getElementById('lastDate').textContent = d;
    document.getElementById('sidePeriod').textContent = `${s.first_date.slice(0, 4)} — ${d}`;
    const lastMonthEnd = !/-12-31$/.test(s.last_date);
    yearStats = s.by_year.map((y, i, a) => ({ ...y, partial: i === a.length - 1 && lastMonthEnd }));
    renderYears();
    document.getElementById('modeBadge').title = s.model;
  } catch (e) {
    setConnection(false);
  }
}

// --- Hodisalar ---
const suggestionsBlock = document.getElementById('suggestionsBlock');
document.querySelectorAll('.lang-btn').forEach(btn => btn.addEventListener('click', () => applyLanguage(btn.dataset.lang)));
document.querySelectorAll('.suggestion-chip').forEach(btn => btn.addEventListener('click', () => sendQuestion(btn.dataset.query)));
form.addEventListener('submit', e => { e.preventDefault(); const q = input.value; if (!q.trim() || busy) return; input.value = ''; input.style.height = 'auto'; sendQuestion(q); });
input.addEventListener('keydown', e => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); form.requestSubmit(); } });
input.addEventListener('input', () => { input.style.height = 'auto'; input.style.height = Math.min(input.scrollHeight, 100) + 'px'; });
document.getElementById('clearChat').addEventListener('click', () => {
  if (conversationId) fetch('/api/reset', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ conversation_id: conversationId }) }).catch(() => {});
  conversationId = null;
  welcome();
});
document.getElementById('viewAll').addEventListener('click', () => { recent = []; store.set('sq_recent', recent); renderRecent(); showToast(t('historyCleared')); });
document.getElementById('helpButton').addEventListener('click', () => showToast(t('helpText'), 6000));
document.getElementById('mobileMenu').addEventListener('click', () => document.getElementById('sidebar').classList.toggle('open'));
document.querySelectorAll('.nav-link').forEach(link => link.addEventListener('click', () => {
  if (window.innerWidth <= 760) document.getElementById('sidebar').classList.remove('open');
}));

function askFromCard(q){
  if (location.hash !== '#/assistant') location.hash = '#/assistant';
  setTimeout(() => document.getElementById('assistant').scrollIntoView({behavior: 'smooth', block: 'start'}), 50);
  if (busy) { input.value = q; showToast(t('assistantBusy')); return; }
  sendQuestion(q);
}
document.querySelectorAll('.capability-item').forEach((el, i) => {
  el.setAttribute('role', 'button'); el.tabIndex = 0; el.title = t('clickToAsk');
  const go = () => askFromCard(CARD_QUERIES[currentLang].cap[i]);
  el.addEventListener('click', go);
  el.addEventListener('keydown', e => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); go(); } });
});
document.querySelectorAll('.metric-card').forEach((el, i) => {
  el.setAttribute('role', 'button'); el.tabIndex = 0; el.title = t('clickToAsk');
  const go = () => askFromCard(CARD_QUERIES[currentLang].metric[i]);
  el.addEventListener('click', go);
  el.addEventListener('keydown', e => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); go(); } });
});
// Grafik menyusi (•••)
const chartMenu = document.querySelector('.chart-menu');
const chartPop = document.createElement('div');
chartPop.className = 'chart-pop';
chartPop.hidden = true;
chartMenu.parentElement.style.position = 'relative';
chartMenu.parentElement.appendChild(chartPop);
function renderChartPop(){
  chartPop.innerHTML = ['deals', 'turnover', 'cancel'].map(m => `<button type="button" data-metric="${m}" class="${m === yearMetric ? 'active' : ''}">${esc(t({deals: 'metricDeals', turnover: 'metricTurnover', cancel: 'metricCancel'}[m]))}</button>`).join('')
    + `<hr><button type="button" data-ask-chart>✳ ${esc(t('askAboutChart'))}</button>`;
  chartPop.querySelectorAll('[data-metric]').forEach(b => b.onclick = () => { yearMetric = b.dataset.metric; renderYears(); chartPop.hidden = true; });
  chartPop.querySelector('[data-ask-chart]').onclick = () => { chartPop.hidden = true; askFromCard(CARD_QUERIES[currentLang].chart(yearMetric)); };
}
chartMenu.setAttribute('role', 'button'); chartMenu.tabIndex = 0;
chartMenu.addEventListener('click', e => { e.stopPropagation(); renderChartPop(); chartPop.hidden = !chartPop.hidden; });
document.addEventListener('click', e => { if (!chartPop.contains(e.target)) chartPop.hidden = true; });
document.querySelector('.dots-button').addEventListener('click', () => showToast(t('profileNote')));

function showToast(message, ms = 2600){ toast.textContent = message; toast.classList.add('show'); clearTimeout(showToast.timer); showToast.timer = setTimeout(() => toast.classList.remove('show'), ms); }

applyLanguage(store.get('sq_lang', 'uz'));
loadStats();
