/* Tropical Aire — site behaviour. No secrets live here: the GA4 Measurement ID is a public identifier,
   and form submissions go to the /api/lead serverless function, where delivery keys live in Vercel env vars. */
(function () {
  'use strict';
  var CONFIG = {
    ga4Id: 'G-XXXXXXXXXX',          // TODO: replace with the real GA4 Measurement ID
    tz: 'America/New_York',
    openHour: 7, closeHour: 16.5,    // Mon–Fri 7:00am–4:30pm
    sameDayCutoff: 14,               // "call before 2 PM for same-day" — confirm with dispatch
    exitDelayMs: 4000                // don't fire exit offer in the first few seconds
  };
  var doc = document.documentElement;
  var store = {
    get: function (k, s) { try { return (s ? sessionStorage : localStorage).getItem(k); } catch (e) { return null; } },
    set: function (k, v, s) { try { (s ? sessionStorage : localStorage).setItem(k, v); } catch (e) {} }
  };
  var reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  function $(s, c) { return (c || document).querySelector(s); }
  function $$(s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); }

  /* ---------- Header, progress, menu ---------- */
  var header = $('.site-header'), prog = $('.scroll-progress');
  function onScroll() {
    var y = window.scrollY || 0;
    if (header) header.classList.toggle('scrolled', y > 10);
    if (prog) { var h = doc.scrollHeight - innerHeight; prog.style.transform = 'scaleX(' + (h > 0 ? Math.min(1, y / h) : 0) + ')'; }
  }
  addEventListener('scroll', onScroll, { passive: true }); onScroll();

  var toggle = $('.menu-toggle');
  if (toggle) toggle.addEventListener('click', function () {
    var open = doc.classList.toggle('menu-open');
    toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
  });
  $$('.has-mega > button').forEach(function (b) {
    b.addEventListener('click', function () {
      var li = b.parentNode, open = !li.classList.contains('open');
      li.classList.toggle('open', open); b.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') {
      doc.classList.remove('menu-open'); if (toggle) toggle.setAttribute('aria-expanded', 'false');
      $$('.has-mega.open').forEach(function (li) { li.classList.remove('open'); li.firstElementChild.setAttribute('aria-expanded', 'false'); });
    }
  });

  /* ---------- Reveal on scroll + count-up ---------- */
  if ('IntersectionObserver' in window && !reduce) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (en) {
        if (!en.isIntersecting) return;
        en.target.classList.add('in'); io.unobserve(en.target);
        if (en.target.hasAttribute('data-count')) countUp(en.target);
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.12 });
    $$('.rv, .steps, [data-count]').forEach(function (el) { io.observe(el); });
  } else { $$('.rv, .steps').forEach(function (el) { el.classList.add('in'); }); }
  function countUp(el) {
    var to = +el.getAttribute('data-count'), pre = el.getAttribute('data-pre') || '', suf = el.getAttribute('data-suf') || '', t0 = null;
    function f(t) { if (!t0) t0 = t; var p = Math.min(1, (t - t0) / 1400), v = Math.round(to * (1 - Math.pow(1 - p, 3)));
      el.textContent = pre + v.toLocaleString('en-US') + suf; if (p < 1) requestAnimationFrame(f); }
    requestAnimationFrame(f);
  }

  /* ---------- Hero cooling/heating switch ---------- */
  var hero = $('.hero[data-mode]');
  $$('.mode-switch button').forEach(function (b) {
    b.addEventListener('click', function () {
      var m = b.getAttribute('data-set');
      hero.setAttribute('data-mode', m);
      $$('.mode-switch button').forEach(function (x) { x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); });
      var sel = $('.hero select[name="service"]');
      if (sel && !sel.dataset.touched) sel.value = m === 'heat' ? 'Heating / Furnace Repair' : 'AC Repair';
    });
  });
  $$('select[name="service"]').forEach(function (s) { s.addEventListener('change', function () { s.dataset.touched = '1'; }); });

  /* ---------- Open / closed status + honest same-day urgency ---------- */
  function nyNow() {
    try {
      var p = new Intl.DateTimeFormat('en-US', { timeZone: CONFIG.tz, weekday: 'short', hour: 'numeric', minute: 'numeric', hour12: false }).formatToParts(new Date());
      var o = {}; p.forEach(function (x) { o[x.type] = x.value; });
      return { day: o.weekday, h: (+o.hour % 24) + (+o.minute) / 60 };
    } catch (e) { var d = new Date(); return { day: 'Mon', h: d.getHours() + d.getMinutes() / 60 }; }
  }
  function status() {
    var n = nyNow(), weekday = ['Sat', 'Sun'].indexOf(n.day) === -1;
    var open = weekday && n.h >= CONFIG.openHour && n.h < CONFIG.closeHour;
    $$('[data-open-status]').forEach(function (el) {
      el.innerHTML = open ? '<span class="dot" aria-hidden="true"></span>Open now · techs on the road' : '<span class="dot off" aria-hidden="true"></span>Closed now · call to be first on tomorrow’s schedule';
    });
    var t = $('[data-urgency-title]'), s = $('[data-urgency-sub]');
    if (!t) return;
    if (open && n.h < CONFIG.sameDayCutoff) {
      var left = CONFIG.sameDayCutoff - n.h, hh = Math.floor(left), mm = Math.round((left - hh) * 60);
      t.textContent = 'Same-day service: call within ' + (hh ? hh + 'h ' : '') + mm + 'm';
      s.textContent = 'Calls before 2 PM get same-day slots in most boroughs. Fully stocked vans fix most issues on the first visit.';
    } else if (open) {
      t.textContent = 'Today’s same-day slots are closing. Call to lock in tomorrow';
      s.textContent = 'Call now and we’ll put you on the first route out tomorrow morning.';
    } else {
      t.textContent = 'Beat the morning rush. Be first on tomorrow’s schedule';
      s.textContent = 'Phones open at 7:00 AM Mon–Fri. Leave a message or a request and we’ll call you first.';
    }
  }
  status(); setInterval(status, 60000);

  /* ---------- Modal (exit-intent offer) ---------- */
  var modal = $('#exit-offer'), lastFocus = null;
  function openModal() {
    if (!modal || store.get('ta_exit_seen', true) || doc.classList.contains('menu-open')) return;
    store.set('ta_exit_seen', '1', true);
    lastFocus = document.activeElement;
    modal.hidden = false; requestAnimationFrame(function () { modal.classList.add('show'); });
    var f = $('.btn-call', modal); if (f) f.focus();
    track('exit_offer_shown');
  }
  function closeModal() {
    if (!modal) return; modal.classList.remove('show');
    setTimeout(function () { modal.hidden = true; }, 320);
    if (lastFocus && lastFocus.focus) lastFocus.focus();
  }
  if (modal) {
    $$('[data-close]', modal).forEach(function (b) { b.addEventListener('click', closeModal); });
    modal.addEventListener('click', function (e) { if (e.target === modal) closeModal(); });
    modal.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') closeModal();
      if (e.key === 'Tab') {
        var f = $$('a[href],button:not([disabled]),input:not([type=hidden]):not([tabindex="-1"])', modal).filter(function (x) { return x.offsetParent; });
        if (!f.length) return; var a = f[0], z = f[f.length - 1];
        if (e.shiftKey && document.activeElement === a) { e.preventDefault(); z.focus(); }
        else if (!e.shiftKey && document.activeElement === z) { e.preventDefault(); a.focus(); }
      }
    });
    var copy = $('[data-copy]', modal);
    if (copy) copy.addEventListener('click', function () {
      var c = copy.getAttribute('data-copy');
      try { navigator.clipboard.writeText(c); copy.textContent = 'Copied!'; } catch (e) { copy.textContent = c; }
    });
    var armed = false; setTimeout(function () { armed = true; }, CONFIG.exitDelayMs);
    // Desktop: cursor heads for the tab bar / close button
    document.addEventListener('mouseout', function (e) {
      if (!armed || e.relatedTarget || e.toElement) return;
      if (e.clientY <= 8) openModal();
    });
    document.addEventListener('mousemove', function (e) { if (armed && e.clientY < 6 && e.movementY < 0) openModal(); }, { passive: true });
    // Touch devices: a fast flick back up after reading a good chunk of the page
    if (matchMedia('(hover: none)').matches) {
      var lastY = scrollY, lastT = Date.now(), maxDepth = 0;
      addEventListener('scroll', function () {
        var y = scrollY, t = Date.now(), h = doc.scrollHeight - innerHeight;
        maxDepth = Math.max(maxDepth, h > 0 ? y / h : 0);
        if (armed && maxDepth > 0.35 && (lastY - y) / Math.max(1, t - lastT) > 2.2 && y > 200) openModal();
        lastY = y; lastT = t;
      }, { passive: true });
    }
  }

  /* ---------- Cookie consent + analytics (GA4 with Consent Mode v2) ---------- */
  window.dataLayer = window.dataLayer || [];
  function gtag() { window.dataLayer.push(arguments); }
  window.gtag = window.gtag || gtag;
  gtag('consent', 'default', { analytics_storage: 'denied', ad_storage: 'denied', ad_user_data: 'denied', ad_personalization: 'denied', wait_for_update: 500 });
  var gaLoaded = false;
  function loadGA() {
    if (gaLoaded || !/^G-[A-Z0-9]{6,}$/.test(CONFIG.ga4Id) || CONFIG.ga4Id.indexOf('XXXX') > -1) return;
    gaLoaded = true;
    var s = document.createElement('script'); s.async = true; s.src = 'https://www.googletagmanager.com/gtag/js?id=' + CONFIG.ga4Id;
    document.head.appendChild(s); gtag('js', new Date()); gtag('config', CONFIG.ga4Id, { anonymize_ip: true });
  }
  function track(name, params) { if (store.get('ta_consent') === 'granted') gtag('event', name, params || {}); }
  var cookie = $('#cookie');
  function setConsent(v) {
    store.set('ta_consent', v);
    gtag('consent', 'update', { analytics_storage: v === 'granted' ? 'granted' : 'denied' });
    if (v === 'granted') loadGA();
    if (cookie) { cookie.classList.remove('show'); setTimeout(function () { cookie.hidden = true; }, 360); }
  }
  if (cookie) {
    $('[data-consent="accept"]', cookie).addEventListener('click', function () { setConsent('granted'); });
    $('[data-consent="reject"]', cookie).addEventListener('click', function () { setConsent('denied'); });
    var c = store.get('ta_consent');
    if (c === 'granted') { gtag('consent', 'update', { analytics_storage: 'granted' }); loadGA(); }
    else if (!c) setTimeout(function () { cookie.hidden = false; requestAnimationFrame(function () { cookie.classList.add('show'); }); }, 1200);
    $$('[data-cookie-settings]').forEach(function (b) { b.addEventListener('click', function () { cookie.hidden = false; requestAnimationFrame(function () { cookie.classList.add('show'); }); }); });
  }

  // Track every call click (the one conversion that matters)
  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('a[href^="tel:"]');
    if (a) track('call_click', { location: a.getAttribute('data-loc') || 'unknown' });
  });

  /* ---------- Forms: validation, spam protection, submit ---------- */
  var rules = {
    name: function (v) { return v.trim().length >= 2 || 'Please enter your name.'; },
    phone: function (v) { var d = v.replace(/\D/g, ''); if (d.length === 11 && d[0] === '1') d = d.slice(1); return /^[2-9]\d{2}[2-9]\d{6}$/.test(d) || 'Enter a valid 10-digit US phone number.'; },
    zip: function (v) { return /^\d{5}$/.test(v.trim()) || 'Enter a 5-digit ZIP code.'; },
    email: function (v) { return !v.trim() || /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v.trim()) || 'Enter a valid email or leave it blank.'; },
    service: function (v) { return !!v || 'Choose what you need help with.'; }
  };
  function check(input) {
    var r = rules[input.name]; if (!r) return true;
    var res = r(input.value), field = input.closest('.field'), ok = res === true;
    if (field) { field.classList.toggle('invalid', !ok); var e = $('.err', field); if (e) e.textContent = ok ? '' : res; }
    input.setAttribute('aria-invalid', ok ? 'false' : 'true');
    return ok;
  }
  $$('form[data-lead]').forEach(function (form) {
    var started = Date.now();
    var ts = form.querySelector('input[name="_ts"]'); if (ts) ts.value = String(started);
    var pg = form.querySelector('input[name="page"]'); if (pg) pg.value = location.pathname;
    $$('input,select', form).forEach(function (i) {
      i.addEventListener('blur', function () { if (i.value) check(i); });
      i.addEventListener('input', function () { if (i.closest('.field.invalid')) check(i); });
    });
    var phone = form.querySelector('input[name="phone"]');
    if (phone) phone.addEventListener('input', function () {
      var d = phone.value.replace(/\D/g, '').slice(0, 10), o = d;
      if (d.length > 6) o = '(' + d.slice(0, 3) + ') ' + d.slice(3, 6) + '-' + d.slice(6);
      else if (d.length > 3) o = '(' + d.slice(0, 3) + ') ' + d.slice(3);
      phone.value = o;
    });
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var ok = true, first = null;
      $$('input,select', form).forEach(function (i) { if (!check(i)) { ok = false; first = first || i; } });
      var st = $('.form-status', form);
      if (!ok) { if (st) { st.className = 'form-status bad'; st.textContent = 'Please fix the highlighted fields.'; } first.focus(); return; }
      // Spam traps: honeypot filled, or submitted faster than a human could
      var hp = form.querySelector('.hp input');
      if ((hp && hp.value) || Date.now() - started < 2500) { location.href = '/thank-you/'; return; }
      var btn = $('button[type=submit]', form); if (btn) { btn.disabled = true; btn.dataset.t = btn.textContent; btn.textContent = 'Sending…'; }
      var body = new URLSearchParams(new FormData(form)).toString();
      fetch('/api/lead', { method: 'POST', headers: { 'Content-Type': 'application/x-www-form-urlencoded', 'Accept': 'application/json' }, body: body })
        .then(function (r) { if (!r.ok) throw new Error(r.status); track('generate_lead', { form: form.getAttribute('name') }); location.href = '/thank-you/'; })
        .catch(function () {
          if (btn) { btn.disabled = false; btn.textContent = btn.dataset.t; }
          if (st) { st.className = 'form-status bad'; st.innerHTML = 'Something went wrong sending that. Please call <a href="tel:+17187660889">(718) 766-0889</a>.'; }
        });
    });
  });

  var y = $('[data-year]'); if (y) y.textContent = new Date().getFullYear();
})();
