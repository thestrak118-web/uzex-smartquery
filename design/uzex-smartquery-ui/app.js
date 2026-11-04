const translations = {
  uz: {
    workspace:'ISH MAYDONI', overview:'Umumiy ko‘rinish', aiAnalyst:'AI tahlilchi', deals:'Bitimlar', commodities:'Tovarlar', participants:'Ishtirokchilar', system:'TIZIM', dataSources:'Ma’lumotlar manbasi', settings:'Sozlamalar', datasetReady:'Dataset tayyor', dealsLoaded:'bitim yozuvi yuklangan', demoWorkspace:'Demo workspace', dataConnected:'Ma’lumotlar ulangan', exchangeIntelligence:'BIRJA INTELLEKTI', pageTitle:'Savollaringizga <em>aniq javoblar.</em>', pageSubtitle:'UZEX bitimlari bo‘yicha ma’lumotlarni tahlil qiling. Savol bering — tekshirilgan natijani oling.', dataSnapshot:'MA’LUMOTLAR HOLATI', snapshotNote:'Datasetning oxirgi sanasi', totalDeals:'Jami bitimlar', fiveYearsData:'2022–2026 yillar ma’lumoti', contracts:'Shartnomalar', contractCards:'shartnoma kartochkasi', companies:'Ishtirokchilar', participantRecords:'kompaniya yozuvi', brokers:'Brokerlar', brokerFirms:'brokerlik tashkiloti', assistantTitle:'UZEX AI yordamchi', assistantReady:'Savollaringizni kutyapti', demoMode:'DEMO REJIMI', newConversation:'YANGI SUHBAT', now:'hozir', welcomeText:'Assalomu alaykum! Men UZEX birja bitimlari bo‘yicha AI tahlilchiman. Savolingizni o‘zbek yoki rus tilida yozing — ma’lumotlar doirasida javob beraman.', groundedNote:'Javoblar faqat datasetdagi ma’lumotlarga tayanishi kerak.', tryAsking:'QUYIDAGILARDAN BIRINI SO‘RANG', suggestion1:'2025-yilda nechta bitim tuzilgan?', suggestion2:'Yillar bo‘yicha bitimlarni taqqosla', suggestion3:'Dataset tarkibini tushuntir', messagePlaceholder:'Savolingizni kiriting...', sendHint:'yuborish', languageHint:'UZ / RU', send:'Yuborish', demoDisclaimer:'Demo rejimi: javoblar namuna sifatida ko‘rsatiladi. Haqiqiy AI backend hali ulanmagan.', datasetOverview:'DATASET TAHLILI', dealsByYear:'Yillar bo‘yicha bitimlar', allDeals:'jami bitim', dealCount:'Bitimlar soni', partialYear:'* 2026 — 30-oktabrgacha', agentCapabilities:'AGENT IMKONIYATLARI', whatCanDo:'Nimalarni tahlil qiladi?', cap1Title:'Bitimlar statistikasi', cap1Desc:'Sana, miqdor va savdo hajmi', cap2Title:'Tovarlar tahlili', cap2Desc:'Mahsulotlar va narx dinamikasi', cap3Title:'Ishtirokchilar', cap3Desc:'Sotuvchi, xaridor va brokerlar', cap4Title:'Shartnoma holati', cap4Desc:'To‘lov va yetkazib berish', trustTitle:'Manbaga asoslangan javob', trustText:'Agent mavjud bo‘lmagan ma’lumotni taxmin qilmasligi va javob uchun ishlatilgan filtrlarni ko‘rsatishi kerak.', activity:'FAOLIYAT', recentQueries:'So‘nggi so‘rovlar', viewAll:'Barchasini ko‘rish', question:'SAVOL', category:'KATEGORIYA', language:'TIL', tableStatus:'HOLAT', time:'VAQT', footerNote:'Hackathon prototipi · Sun’iy dataset asosida', noAnswer:'Bu demo uchun tayyor namunaviy javob mavjud emas. To‘liq javob olish uchun AI backend va SQL query engine ulanishi kerak.', answer2025:'2025-yil uchun datasetda 115 763 ta bitim qayd etilgan.', answerTrend:'Datasetdagi yillik bitimlar soni: 2022 — 84 299; 2023 — 93 985; 2024 — 106 647; 2025 — 115 763; 2026 — 99 306. 2026-yil ma’lumotlari 30-oktabrgacha.', answerDataset:'Dataset 2022–2026-yillarni qamrab oladi: 500 000 ta bitim, 6 616 ta shartnoma kartochkasi, 14 392 ta ishtirokchi va 120 ta broker. Barcha yozuvlar sun’iy (synthetic) ma’lumotlardir.', answerSource:'Manba: foydalanuvchi taqdim etgan dataset README fayli. Hisoblash ko‘rsatkichi: bitimlar soni; sana oralig‘i: datasetda berilgan yil.', notConnected:'Demo rejimi: hozircha faqat oldindan tayyorlangan namunaviy savollarga javob beriladi.', querySent:'So‘rov demo rejimida bajarildi.'
  },
  ru: {
    workspace:'РАБОЧАЯ ОБЛАСТЬ', overview:'Обзор', aiAnalyst:'AI аналитик', deals:'Сделки', commodities:'Товары', participants:'Участники', system:'СИСТЕМА', dataSources:'Источники данных', settings:'Настройки', datasetReady:'Датасет готов', dealsLoaded:'записей сделок загружено', demoWorkspace:'Демо-пространство', dataConnected:'Данные подключены', exchangeIntelligence:'БИРЖЕВАЯ АНАЛИТИКА', pageTitle:'Точные ответы <em>на ваши вопросы.</em>', pageSubtitle:'Анализируйте данные биржевых сделок UZEX. Задайте вопрос — получите проверенный результат.', dataSnapshot:'СОСТОЯНИЕ ДАННЫХ', snapshotNote:'Последняя дата датасета', totalDeals:'Всего сделок', fiveYearsData:'Данные за 2022–2026 годы', contracts:'Контракты', contractCards:'карточек контрактов', companies:'Участники', participantRecords:'записей компаний', brokers:'Брокеры', brokerFirms:'брокерских организаций', assistantTitle:'UZEX AI помощник', assistantReady:'Готов к вашим вопросам', demoMode:'ДЕМО-РЕЖИМ', newConversation:'НОВЫЙ ДИАЛОГ', now:'сейчас', welcomeText:'Здравствуйте! Я AI-аналитик биржевых сделок UZEX. Задайте вопрос на узбекском или русском языке — я отвечу в рамках доступных данных.', groundedNote:'Ответы должны основываться только на данных датасета.', tryAsking:'ПОПРОБУЙТЕ СПРОСИТЬ', suggestion1:'Сколько сделок заключено в 2025 году?', suggestion2:'Сравни количество сделок по годам', suggestion3:'Объясни состав датасета', messagePlaceholder:'Введите ваш вопрос...', sendHint:'отправить', languageHint:'UZ / RU', send:'Отправить', demoDisclaimer:'Демо-режим: ответы показаны в качестве примера. Реальный AI backend пока не подключён.', datasetOverview:'АНАЛИЗ ДАТАСЕТА', dealsByYear:'Сделки по годам', allDeals:'всего сделок', dealCount:'Количество сделок', partialYear:'* 2026 — по 30 октября', agentCapabilities:'ВОЗМОЖНОСТИ АГЕНТА', whatCanDo:'Что анализирует?', cap1Title:'Статистика сделок', cap1Desc:'Дата, количество и объём торгов', cap2Title:'Анализ товаров', cap2Desc:'Продукты и динамика цен', cap3Title:'Участники', cap3Desc:'Продавцы, покупатели и брокеры', cap4Title:'Статус контрактов', cap4Desc:'Оплата и поставка', trustTitle:'Ответы на основе источников', trustText:'Агент не должен выдумывать отсутствующие данные и должен показывать фильтры, использованные для ответа.', activity:'АКТИВНОСТЬ', recentQueries:'Последние запросы', viewAll:'Посмотреть все', question:'ВОПРОС', category:'КАТЕГОРИЯ', language:'ЯЗЫК', tableStatus:'СТАТУС', time:'ВРЕМЯ', footerNote:'Прототип хакатона · На синтетическом датасете', noAnswer:'Для этого вопроса нет готового демонстрационного ответа. Для полноценной работы необходимо подключить AI backend и SQL query engine.', answer2025:'В датасете за 2025 год зарегистрировано 115 763 сделки.', answerTrend:'Количество сделок по годам: 2022 — 84 299; 2023 — 93 985; 2024 — 106 647; 2025 — 115 763; 2026 — 99 306. Данные за 2026 год представлены по 30 октября.', answerDataset:'Датасет охватывает 2022–2026 годы: 500 000 сделок, 6 616 карточек контрактов, 14 392 участника и 120 брокеров. Все записи являются синтетическими (искусственными) данными.', answerSource:'Источник: README-файл предоставленного датасета. Метрика: количество сделок; период: соответствующий год в датасете.', notConnected:'Демо-режим: пока доступны только заранее подготовленные примеры вопросов.', querySent:'Запрос обработан в демо-режиме.'
  }
};

let currentLang = 'uz';
const chatArea = document.getElementById('chatArea');
const input = document.getElementById('messageInput');
const form = document.getElementById('chatForm');
const recentRows = document.getElementById('recentRows');
const toast = document.getElementById('toast');

function t(key){ return translations[currentLang][key] || translations.uz[key] || key; }
function applyLanguage(lang){
  currentLang = lang;
  document.documentElement.lang = lang;
  document.querySelectorAll('[data-i18n]').forEach(el => {
    const value = t(el.dataset.i18n);
    if (value.includes('<em>')) el.innerHTML = value; else el.textContent = value;
  });
  document.querySelectorAll('[data-i18n-placeholder]').forEach(el => el.placeholder = t(el.dataset.i18nPlaceholder));
  document.querySelectorAll('.lang-btn').forEach(btn => btn.classList.toggle('active', btn.dataset.lang === lang));
  document.querySelectorAll('.suggestion-chip').forEach((btn, i) => {
    const keys = ['suggestion1','suggestion2','suggestion3'];
    btn.querySelector('span:last-child').textContent = t(keys[i]);
    btn.dataset.query = lang === 'uz' ? [
      '2025-yilda nechta bitim tuzilgan?', 'Yillar bo‘yicha bitimlar sonini taqqosla.', 'Datasetda qanday ma’lumotlar mavjud?'
    ][i] : [
      'Сколько сделок заключено в 2025 году?', 'Сравни количество сделок по годам.', 'Какие данные доступны в датасете?'
    ][i];
  });
}

document.querySelectorAll('.lang-btn').forEach(btn => btn.addEventListener('click', () => applyLanguage(btn.dataset.lang)));

document.querySelectorAll('.suggestion-chip').forEach(btn => btn.addEventListener('click', () => {
  input.value = btn.dataset.query;
  input.focus();
  sendQuestion(btn.dataset.query);
}));

function addMessage(kind, text, extra = {}){
  const wrap = document.createElement('div');
  wrap.className = `message ${kind === 'user' ? 'user-message' : 'assistant-message'}`;
  const avatar = document.createElement('div');
  avatar.className = 'message-avatar';
  avatar.textContent = kind === 'user' ? 'SA' : '✳';
  const body = document.createElement('div');
  body.className = 'message-body';
  const author = document.createElement('div');
  author.className = 'message-author';
  author.innerHTML = kind === 'user' ? 'Siz <span>• hozir</span>' : 'UZEX AI <span>• hozir</span>';
  const bubble = document.createElement('div');
  bubble.className = 'message-bubble' + (extra.answer ? ' answer-bubble' : '');
  if (extra.answer === '2025') {
    const p = document.createElement('p'); p.className='answer-summary'; p.textContent = t('answer2025'); bubble.appendChild(p);
    const result = document.createElement('div'); result.className='answer-result'; result.innerHTML='<strong>115,763</strong><span>bitim · 2025-yil</span>'; bubble.appendChild(result);
    const meta = document.createElement('p'); meta.className='answer-meta'; meta.textContent=t('answerSource'); bubble.appendChild(meta);
  } else {
    const p = document.createElement('p'); p.textContent = text; bubble.appendChild(p);
    if (extra.answer === 'trend' || extra.answer === 'dataset') {
      const meta = document.createElement('p'); meta.className='answer-meta'; meta.textContent=t('answerSource'); bubble.appendChild(meta);
    }
  }
  body.append(author,bubble); wrap.append(avatar,body); chatArea.appendChild(wrap); chatArea.scrollTop=chatArea.scrollHeight;
}

function classifyQuestion(q){
  const s = q.toLowerCase();
  if ((s.includes('2025') || s.includes('2025')) && (s.includes('nechta') || s.includes('количество') || s.includes('сколько') || s.includes('bitim') || s.includes('сделк'))) return '2025';
  if ((s.includes('yil') || s.includes('год')) && (s.includes('taqqos') || s.includes('dinamik') || s.includes('сравн') || s.includes('динамик') || s.includes('bitim') || s.includes('сделк'))) return 'trend';
  if (s.includes('dataset') || s.includes('ma’lumot') || s.includes('malumot') || s.includes('датасет') || s.includes('данн')) return 'dataset';
  return 'unknown';
}

function addRecent(question, category){
  const tr = document.createElement('tr');
  const safeQ = document.createElement('td'); const qspan = document.createElement('span'); qspan.className='table-question'; qspan.textContent=question; safeQ.appendChild(qspan);
  const cat = document.createElement('td'); const tag = document.createElement('span'); tag.className='category-tag'; tag.textContent=category; cat.appendChild(tag);
  const lang = document.createElement('td'); lang.textContent=currentLang.toUpperCase();
  const status = document.createElement('td'); status.innerHTML='<span class="success-status"><i></i>Demo</span>';
  const time = document.createElement('td'); time.textContent=new Date().toLocaleTimeString([], {hour:'2-digit',minute:'2-digit'});
  tr.append(safeQ,cat,lang,status,time); recentRows.prepend(tr);
  while(recentRows.children.length>5) recentRows.removeChild(recentRows.lastElementChild);
}

function showToast(message){ toast.textContent=message; toast.classList.add('show'); clearTimeout(showToast.timer); showToast.timer=setTimeout(()=>toast.classList.remove('show'),2600); }
function sendQuestion(question){
  const q = (question || '').trim(); if(!q) return;
  document.getElementById('suggestionsBlock').style.display='none';
  addMessage('user', q);
  const type = classifyQuestion(q);
  setTimeout(()=>{
    if(type==='2025') addMessage('assistant', t('answer2025'), {answer:'2025'});
    else if(type==='trend') addMessage('assistant', t('answerTrend'), {answer:'trend'});
    else if(type==='dataset') addMessage('assistant', t('answerDataset'), {answer:'dataset'});
    else addMessage('assistant', t('noAnswer')+' '+t('notConnected'));
    const category = type==='2025' ? 'Statistika' : type==='trend' ? 'Trend tahlili' : type==='dataset' ? 'Ma’lumotlar' : 'Umumiy';
    addRecent(q, category); showToast(t('querySent'));
  }, 350);
}

form.addEventListener('submit', e=>{e.preventDefault(); const q=input.value; if(!q.trim()) return; sendQuestion(q); input.value=''; input.style.height='auto';});
input.addEventListener('keydown', e=>{if(e.key==='Enter'&&!e.shiftKey){e.preventDefault();form.requestSubmit();}});
input.addEventListener('input',()=>{input.style.height='auto';input.style.height=Math.min(input.scrollHeight,100)+'px';});
document.getElementById('clearChat').addEventListener('click',()=>{
  chatArea.innerHTML='';
  const divider=document.createElement('div'); divider.className='date-divider'; divider.innerHTML=`<span>${t('newConversation')}</span>`;
  chatArea.appendChild(divider);
  const welcome=document.createElement('div'); welcome.className='message assistant-message'; welcome.innerHTML=`<div class="message-avatar">✳</div><div class="message-body"><div class="message-author">UZEX AI <span>• ${t('now')}</span></div><div class="message-bubble welcome-bubble"><p>${t('welcomeText')}</p><div class="welcome-note"><span>✦</span><span>${t('groundedNote')}</span></div></div></div>`;
  chatArea.appendChild(welcome); document.getElementById('suggestionsBlock').style.display='block';
});
document.getElementById('viewAll').addEventListener('click',()=>showToast(currentLang==='uz'?'Demo rejimida so‘rovlar tarixi shu oynada ko‘rsatiladi.':'В демо-режиме история запросов отображается в этом окне.'));
document.getElementById('mobileMenu').addEventListener('click',()=>document.getElementById('sidebar').classList.toggle('open'));
document.querySelectorAll('.nav-link').forEach(link=>link.addEventListener('click',()=>{if(window.innerWidth<=760)document.getElementById('sidebar').classList.remove('open');}));

applyLanguage('uz');
