# Tropical Aire: website rebuild

A static, dependency-free site (plain HTML, one CSS file, one JS file) plus a single Vercel serverless function for the estimate form.

## Deploy on Vercel
1. vercel.com → **Add New → Project** → import `thehiveee/tropical-aire`. Framework preset: **Other**. Leave the build command empty and the output directory as `.` (`vercel.json` already sets both).
2. **Settings → Environment Variables**: set at least one lead destination, or the form returns an error (on purpose, so no lead is ever silently lost).
   - `RESEND_API_KEY` + `LEAD_TO_EMAIL` (e.g. `William@tropical-aire.com`), plus optionally `LEAD_FROM_EMAIL`. Verify the sending domain in Resend first.
   - and/or `LEAD_WEBHOOK_URL`: a Zapier, Make, Slack or CRM webhook. It receives the lead as JSON.
   Redeploy after adding them.
3. **Settings → Domains**: add `tropical-aire.com` and `www.tropical-aire.com`. Vercel issues SSL and forces HTTPS automatically. `vercel.json` 301s www to the apex domain and every old WordPress URL to its new page, and adds HSTS plus security headers.
4. In `assets/js/site.js`, set `ga4Id` to the real GA4 Measurement ID. Analytics loads only after a visitor clicks "Accept all" (Consent Mode v2). Call clicks are sent as `call_click` and leads as `generate_lead`. Mark both as Key Events in GA4.
5. Submit `https://tropical-aire.com/sitemap.xml` in Google Search Console.

Every push to `main` redeploys automatically. Pull requests get preview URLs.

## How the form works
`/api/lead` (`api/lead.js`) applies a honeypot field, a time-trap and a per-IP rate limit. It validates name, US phone, ZIP and email on the server too, then delivers the lead to email and/or the webhook. API keys exist only in Vercel's environment variables, never in the browser. Without JavaScript the form still works: it posts to the function and lands on `/thank-you/`.

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
| Secrets off the frontend | Keys live only in Vercel env vars, used by `api/lead.js`; the GA ID is a public identifier |
| Force HTTPS | Vercel auto-HTTPS + HSTS header in `vercel.json` + `upgrade-insecure-requests` |
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
| Broken links | 964 internal refs checked, 0 broken; old URLs 301'd in `vercel.json`; checked on every push by GitHub Actions |
| Form validation | Inline, accessible errors in the browser, re-validated on the server |
| Spam protection | Honeypot + time-trap + per-IP rate limit (client and server) |
| Analytics | GA4 with Consent Mode v2, call + lead events |
| One clear CTA | "Call (718) 766-0889" everywhere; the form is secondary |
