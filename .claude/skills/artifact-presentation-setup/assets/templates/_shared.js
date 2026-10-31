/* Shared helpers: DOM builder, theme toggle, chrome, approval decisions (db capability with local fallback). */
const DATA = JSON.parse(document.getElementById('data').textContent);

function h(tag, attrs, ...kids) {
  const e = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs || {})) {
    if (v == null || v === false) continue;
    if (k === 'class') e.className = v;
    else if (k.startsWith('on') && typeof v === 'function') e.addEventListener(k.slice(2), v);
    else e.setAttribute(k, v === true ? '' : v);
  }
  for (const kid of kids.flat(Infinity)) {
    if (kid == null || kid === false) continue;
    e.append(kid.nodeType ? kid : document.createTextNode(String(kid)));
  }
  return e;
}
const $ = (sel, root) => (root || document).querySelector(sel);
const esc = (s) => String(s == null ? '' : s);

function toast(msg) {
  const t = h('div', { class: 'toast', role: 'status' }, msg);
  document.body.append(t);
  setTimeout(() => t.remove(), 1800);
}

async function copyText(text, okMsg) {
  try { await navigator.clipboard.writeText(text); toast(okMsg || 'Copied'); }
  catch (e) {
    const ta = h('textarea', { 'aria-label': 'Copy this text', style: 'position:fixed;inset:20% 10% auto;height:50%;z-index:50;width:80%' }, text);
    document.body.append(ta); ta.select();
    toast('Select and copy the text shown');
    ta.addEventListener('blur', () => ta.remove());
  }
}

/* theme: 'system' by default, toggle writes data-theme */
function themeButton() {
  const root = document.documentElement;
  try { const t = localStorage.getItem('theme'); if (t) root.dataset.theme = t; } catch (e) {}
  return h('button', {
    class: 'btn sm', type: 'button', 'aria-label': 'Switch light or dark theme',
    onclick: () => {
      const dark = root.dataset.theme ? root.dataset.theme === 'dark' : matchMedia('(prefers-color-scheme: dark)').matches;
      root.dataset.theme = dark ? 'light' : 'dark';
      try { localStorage.setItem('theme', root.dataset.theme); } catch (e) {}
    },
  }, 'Light / Dark');
}

function chrome(title, sub, extra) {
  return h('header', { class: 'top' },
    h('div', { class: 'wrap top-in' },
      h('div', { class: 'grow' },
        h('div', { class: 'eyebrow' }, DATA.project || ''),
        h('h1', null, title),
        sub ? h('div', { class: 'sub' }, sub) : null),
      extra, themeButton()));
}

const STATUS_TONE = {
  approved: 'good', published: 'good', scheduled: 'info', measured: 'info',
  review: 'warn', revision: 'warn', revise: 'warn', draft: 'warn',
  rejected: 'bad', reject: 'bad',
};
function badge(text) {
  const key = String(text || '').toLowerCase().replace(/\s+/g, '_');
  return h('span', { class: 'badge ' + (STATUS_TONE[key] || '') }, text);
}

/* ---- decisions ---- */
const Decisions = (() => {
  let map = {}, subs = [], mode = 'local', db = null;
  const LS = 'decisions:' + (DATA.project || '') + ':' + document.title;
  const key = (id) => String(id).replace(/[^A-Za-z0-9_-]/g, '_');
  const emit = () => subs.forEach((f) => f(map, mode));
  const saveLocal = () => { try { localStorage.setItem(LS, JSON.stringify(map)); } catch (e) {} };
  async function init() {
    try { map = JSON.parse(localStorage.getItem(LS) || '{}'); } catch (e) { map = {}; }
    emit();
    try {
      if (!window.claude || !window.claude.use) return;
      db = await window.claude.use('db');
      if (!db) return;
      mode = 'shared';
      db.collection('decisions').onSnapshot(
        (snap) => { const m = {}; snap.docs.forEach((d) => { m[d.id] = d.data(); }); map = m; emit(); },
        () => { mode = 'local'; db = null; emit(); });
    } catch (e) { db = null; mode = 'local'; emit(); }
  }
  async function set(id, rec) {
    const k = key(id);
    const next = Object.assign({}, map[k] || {}, rec, { item: String(id), at: new Date().toISOString() });
    map[k] = next; emit();
    if (db) {
      try { await db.doc('decisions/' + k).set(next); return; }
      catch (e) { mode = 'local'; db = null; }
    }
    saveLocal(); emit();
  }
  return {
    init, set,
    get: (id) => map[key(id)],
    all: () => map,
    mode: () => mode,
    onChange: (f) => { subs.push(f); f(map, mode); return () => { subs = subs.filter((s) => s !== f); }; },
    summary(items, title) {
      const lines = ['Decisions for: ' + title];
      for (const it of items) {
        const d = map[key(it.id)];
        lines.push('- ' + it.id + ' (' + (it.title || '') + '): ' + (d && d.decision ? d.decision : 'pending') + (d && d.comment ? ' | ' + d.comment : ''));
      }
      return lines.join('\n');
    },
  };
})();

const DECISION_LABELS = { approve: 'Approve', revise: 'Request changes', reject: 'Reject' };

function decisionWidget(item, opts) {
  const o = opts || {};
  const id = 'c-' + String(item.id).replace(/[^A-Za-z0-9_-]/g, '_');
  const buttons = Object.keys(DECISION_LABELS).map((k) =>
    h('button', { class: 'opt ' + k, type: 'button', 'aria-pressed': 'false', 'data-k': k,
      onclick: () => Decisions.set(item.id, { decision: k, comment: ta.value.trim() }) }, DECISION_LABELS[k]));
  const ta = h('textarea', { id, placeholder: o.placeholder || 'Optional note: what should change, or why it works', 'aria-label': 'Comment for ' + (item.title || item.id),
    onchange: () => { const d = Decisions.get(item.id); Decisions.set(item.id, { decision: d ? d.decision : undefined, comment: ta.value.trim() }); } });
  const el = h('div', { class: 'decide' }, h('div', { class: 'opts' }, buttons), ta);
  let off = () => {};
  off = Decisions.onChange((map) => {
    if (el.isConnected === false && el.dataset.seen) { off(); return; }
    if (el.isConnected) el.dataset.seen = '1';
    const d = Decisions.get(item.id) || {};
    buttons.forEach((b) => b.setAttribute('aria-pressed', String(d.decision === b.dataset.k)));
    if (d.comment != null && document.activeElement !== ta) ta.value = d.comment;
  });
  return el;
}

function progressBar(items) {
  const bar = h('i'); const label = h('span', { class: 'muted' });
  const wrap = h('div', { class: 'row', style: 'flex:1 1 220px' }, h('div', { class: 'progress' }, bar), label);
  Decisions.onChange(() => {
    const n = items.filter((it) => { const d = Decisions.get(it.id); return d && d.decision; }).length;
    bar.style.width = (items.length ? (100 * n / items.length) : 0) + '%';
    label.textContent = n + ' of ' + items.length + ' decided';
  });
  return wrap;
}

function saveStatus() {
  const s = h('span', { class: 'muted', style: 'font-size:12px' });
  Decisions.onChange((m, mode) => {
    s.textContent = mode === 'shared' ? 'Decisions are saved to this page. Tell Claude when you are done.' : 'Decisions are kept in this browser only. Use Copy summary and paste it to Claude.';
  });
  return s;
}

function renderTabs(defs, mount, startId) {
  const bar = h('div', { class: 'tabs', role: 'tablist' });
  const panel = h('div', { role: 'tabpanel', class: 'stack', style: 'margin-top:16px' });
  const btns = {};
  function show(id) {
    for (const [k, b] of Object.entries(btns)) b.setAttribute('aria-selected', String(k === id));
    panel.replaceChildren(defs.find((d) => d.id === id).render());
  }
  if (!defs.some((d) => d.id === startId)) startId = defs[0].id;
  defs.forEach((d) => {
    btns[d.id] = h('button', { class: 'tab', role: 'tab', type: 'button', onclick: () => show(d.id) }, d.label);
    bar.append(btns[d.id]);
  });
  mount.append(bar, panel);
  show(startId || defs[0].id);
}
