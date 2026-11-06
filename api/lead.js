// Vercel serverless function: receives the estimate form, filters spam, validates, and delivers the lead.
// All secrets come from Vercel Environment Variables. Nothing sensitive is ever sent to the browser.
//
//   LEAD_WEBHOOK_URL   optional  POST JSON to Zapier / Make / Slack / CRM
//   RESEND_API_KEY     optional  send an email via Resend (resend.com)
//   LEAD_TO_EMAIL      with Resend: where leads go, e.g. William@tropical-aire.com
//   LEAD_FROM_EMAIL    with Resend: verified sender, default "Tropical Aire Website <leads@tropical-aire.com>"
//
// Configure at least one destination, or the function returns 500 so a lead is never silently lost.

const hits = new Map(); // best-effort per-instance rate limit
const LIMIT = 5, WINDOW_MS = 10 * 60 * 1000;

const clean = (v, max = 200) => String(v == null ? '' : v).replace(/[\u0000-\u001f\u007f]/g, ' ').trim().slice(0, max);
const esc = (s) => s.replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));

function validate(b) {
  const errors = {};
  if (b.name.length < 2) errors.name = 'Please enter your name.';
  let d = b.phone.replace(/\D/g, '');
  if (d.length === 11 && d[0] === '1') d = d.slice(1);
  if (!/^[2-9]\d{2}[2-9]\d{6}$/.test(d)) errors.phone = 'Enter a valid 10-digit US phone number.';
  if (!/^\d{5}$/.test(b.zip)) errors.zip = 'Enter a 5-digit ZIP code.';
  if (b.email && !/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(b.email)) errors.email = 'Enter a valid email or leave it blank.';
  if (!b.service) errors.service = 'Choose what you need help with.';
  return { errors, phoneDigits: d };
}

module.exports = async function handler(req, res) {
  const wantsJson = String(req.headers.accept || '').includes('application/json');
  const reply = (ok, status = 200, extra = {}) => {
    if (wantsJson) return res.status(status).json({ ok, ...extra });
    res.statusCode = 303; // no-JS fallback: plain form post
    res.setHeader('Location', ok ? '/thank-you/' : '/?form=error#estimate');
    return res.end();
  };

  if (req.method !== 'POST') { res.setHeader('Allow', 'POST'); return res.status(405).json({ ok: false }); }

  let raw = req.body || {};
  if (typeof raw === 'string') raw = Object.fromEntries(new URLSearchParams(raw));

  // Spam traps. Bots get a fake success so they don't learn anything.
  if (clean(raw.company_website)) return reply(true);
  const ts = Number(raw._ts);
  const age = ts ? Date.now() - ts : null;
  if (age !== null && (age < 2500 || age > 24 * 3600 * 1000)) return reply(true);

  const ip = String(req.headers['x-forwarded-for'] || '').split(',')[0].trim() || 'unknown';
  const now = Date.now();
  const recent = (hits.get(ip) || []).filter((t) => now - t < WINDOW_MS);
  if (recent.length >= LIMIT) return reply(false, 429, { error: 'Too many requests. Please call (718) 766-0889.' });
  recent.push(now); hits.set(ip, recent);

  const b = {
    name: clean(raw.name, 100), phone: clean(raw.phone, 30), zip: clean(raw.zip, 5),
    email: clean(raw.email, 150), service: clean(raw.service, 80), page: clean(raw.page, 200),
  };
  const { errors, phoneDigits } = validate(b);
  if (Object.keys(errors).length) return reply(false, 422, { errors });

  const lead = {
    ...b,
    phone: `(${phoneDigits.slice(0, 3)}) ${phoneDigits.slice(3, 6)}-${phoneDigits.slice(6)}`,
    submittedAt: new Date().toISOString(),
    jsVerified: age !== null, // false = submitted without JavaScript (allowed, but worth a glance)
  };

  const tasks = [];
  if (process.env.LEAD_WEBHOOK_URL) {
    tasks.push(fetch(process.env.LEAD_WEBHOOK_URL, {
      method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(lead),
    }).then((r) => { if (!r.ok) throw new Error('webhook ' + r.status); }));
  }
  if (process.env.RESEND_API_KEY && process.env.LEAD_TO_EMAIL) {
    const rows = Object.entries(lead).map(([k, v]) => `<tr><td style="padding:4px 12px 4px 0"><b>${esc(k)}</b></td><td>${esc(String(v))}</td></tr>`).join('');
    tasks.push(fetch('https://api.resend.com/emails', {
      method: 'POST',
      headers: { Authorization: `Bearer ${process.env.RESEND_API_KEY}`, 'Content-Type': 'application/json' },
      body: JSON.stringify({
        from: process.env.LEAD_FROM_EMAIL || 'Tropical Aire Website <leads@tropical-aire.com>',
        to: process.env.LEAD_TO_EMAIL.split(',').map((s) => s.trim()),
        reply_to: lead.email || undefined,
        subject: `New lead: ${lead.service} — ${lead.name} (${lead.zip})`,
        html: `<h2>New estimate request</h2><table>${rows}</table><p>Call them back: <a href="tel:+1${phoneDigits}">${lead.phone}</a></p>`,
      }),
    }).then((r) => { if (!r.ok) throw new Error('resend ' + r.status); }));
  }

  if (!tasks.length) {
    console.error('Lead received but no destination configured (set LEAD_WEBHOOK_URL or RESEND_API_KEY + LEAD_TO_EMAIL):', lead);
    return reply(false, 500, { error: 'not_configured' });
  }
  const results = await Promise.allSettled(tasks);
  if (results.every((r) => r.status === 'rejected')) {
    console.error('Lead delivery failed', results, lead);
    return reply(false, 502, { error: 'delivery_failed' });
  }
  return reply(true);
};
