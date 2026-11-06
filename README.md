# Tropical Aire: website rebuild

A static, dependency-free site: plain HTML, one CSS file and one JS file. It's ready for Netlify (recommended) or any Apache host.

## Deploy (Netlify, ~5 minutes)
1. Drag this folder into app.netlify.com → "Add new site → Deploy manually" (or connect a Git repo).
2. Domain settings → add `tropical-aire.com` and turn on HTTPS. `_redirects` forces HTTPS and the non-www host, and 301-redirects every old WordPress URL.
3. Forms → enable form detection. Submissions from every page arrive as the **estimate** form. Add an email or Slack notification in Forms → Notifications. Netlify's Akismet spam filter is on by default, and the honeypot field plus a time-trap in `site.js` block bots.
4. In `assets/js/site.js`, set `ga4Id` to the real GA4 Measurement ID. Analytics only loads after a visitor clicks "Accept all" (Consent Mode v2). Call clicks are tracked as `call_click` and form leads as `generate_lead`. Mark both as Key Events in GA4.
5. Submit `https://tropical-aire.com/sitemap.xml` in Google Search Console.

## Before launch: confirm with the owner
- **Exit-intent offer**: `$50 OFF`, code `STAY50` (set in `content.py`/`build.py` and the footer terms). Swap for whatever offer the business will honour.
- **Same-day cut-off**: the sticky bar counts down to 2 PM (`sameDayCutoff` in `site.js`). Change it to match dispatch.
- **Warranty terms, licence number, years in business, review count**: these aren't on the current site. Adding them would strengthen the trust sections.
- **Legal pages** are solid templates, not legal advice. Have them reviewed.
- **Photos**: drop real job photos into `/assets/img/` (WebP, ≤200 KB, with descriptive alt text).

## Editing
Copy and services live in `src/content.py` and templates in `src/build.py`. Run `python3 src/build.py` after editing, after first changing `OUT` in build.py to this folder.

## Launch checklist status
| Item | Where |
|---|---|
| Privacy policy / Terms | `/privacy/`, `/terms/` (+ `/accessibility/`) |
| Secrets off the frontend | No keys in code; forms post to Netlify; GA ID is a public identifier |
| Force HTTPS | `_redirects`, `.htaccess`, HSTS in `_headers`, `upgrade-insecure-requests` |
| Cookie consent | Banner + "Cookie settings" footer link; GA blocked until consent |
| Meta titles/descriptions | Unique per page, plus canonical + JSON-LD (HVACBusiness, Service, FAQ, Breadcrumb) |
| Social preview | `/assets/img/og-image.jpg` (1200×630), OG + Twitter tags |
| Favicon | `favicon.ico`, PNG icons, apple-touch-icon, manifest |
| Sitemap + robots | `/sitemap.xml`, `/robots.txt` |
| Alt text | All `<img>` have alt; decorative SVGs are `aria-hidden` |
| Compressed images | WebP + 2x, self-hosted woff2 fonts, ~2 MB total site |
| Page speed | Lighthouse (mobile): Performance 96, Accessibility 100, Best Practices 100, SEO 100 |
| Colour contrast | All text ≥ 4.5:1 (WCAG AA) |
| Mobile friendly | Tested at 390px; no horizontal scroll; 44px+ touch targets |
| Custom 404 | `/404.html` |
| Broken links | 964 internal refs checked, 0 broken; old URLs 301'd; `netlify-plugin-checklinks` on deploy |
| Form validation | Inline, accessible errors (name, US phone, ZIP, email) |
| Spam protection | Honeypot + time-trap + Netlify Akismet |
| Analytics | GA4 with Consent Mode v2, call + lead events |
| One clear CTA | "Call (718) 766-0889" everywhere; the form is secondary |
