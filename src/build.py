#!/usr/bin/env python3
"""Static site generator for the Tropical Aire rebuild. Output: /home/claude/site"""
import json, os, html, datetime
from content import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
TODAY = datetime.date.today().isoformat()
E = html.escape

I = {  # 24x24 stroke icons
 "phone": '<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z"/>',
 "snow": '<path d="M12 2v20M4.9 7l14.2 10M4.9 17 19.1 7M9 4l3 2 3-2M9 20l3-2 3 2M3.5 10.5 5 7.6 3 5.2M20.5 13.5 19 16.4l2 2.4M3.5 13.5 5 16.4l-2 2.4M20.5 10.5 19 7.6l2-2.4"/>',
 "flame": '<path d="M8.5 14.5A2.5 2.5 0 0 0 11 12c0-1.4-.5-2-1-3-1.1-2.1-.2-4 2-6 .5 2.5 2 4.9 4 6.5 2 1.6 3 3.5 3 5.5a7 7 0 1 1-14 0c0-1.2.4-2.3 1-3.2.3 1.5 1.4 2.7 2.5 2.7z"/>',
 "sun": '<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M6.3 17.7l-1.4 1.4M19.1 4.9l-1.4 1.4"/>',
 "wrench": '<path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.8-3.8a6 6 0 0 1-7.9 7.9l-6.9 6.9a2.1 2.1 0 0 1-3-3l6.9-6.9a6 6 0 0 1 7.9-7.9l-3.8 3.8z"/>',
 "gauge": '<path d="m12 14 4-4"/><path d="M3.3 19a10 10 0 1 1 17.4 0"/>',
 "home": '<path d="m3 10 9-7 9 7v10a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><path d="M9 22V12h6v10"/>',
 "wind": '<path d="M17.7 7.7A2.5 2.5 0 1 1 19.5 12H2M9.6 4.6A2 2 0 1 1 11 8H2M12.6 19.4A2 2 0 1 0 14 16H2"/>',
 "drop": '<path d="M12 22a7 7 0 0 0 7-7c0-2-1-3.9-3-5.5s-3.5-4-4-6.5c-.5 2.5-2 4.9-4 6.5S5 13 5 15a7 7 0 0 0 7 7z"/>',
 "building": '<rect x="4" y="2" width="16" height="20" rx="2"/><path d="M9 22v-4h6v4M8 6h.01M16 6h.01M12 6h.01M12 10h.01M12 14h.01M16 10h.01M16 14h.01M8 10h.01M8 14h.01"/>',
 "tool": '<path d="M2 20h20M4 20V10l8-6 8 6v10M9 20v-6h6v6"/><path d="M4 10h16"/>',
 "leaf": '<path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.5 19 2c1 2 2 4.2 2 8 0 5.5-4.8 10-10 10z"/><path d="M2 21c0-3 1.9-5.4 5.2-6.1 2.5-.5 4.8-2 5.8-3.9"/>',
 "bolt": '<path d="M13 2 3 14h9l-1 8 10-12h-9z"/>',
 "truck": '<path d="M10 17h4V5H2v12h3M20 17h2v-3.3a1 1 0 0 0-.2-.6l-3.5-4.4a1 1 0 0 0-.8-.4H14v8.7"/><circle cx="7.5" cy="17.5" r="2.5"/><circle cx="17.5" cy="17.5" r="2.5"/>',
 "dollar": '<path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/>',
 "shield": '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="m9 12 2 2 4-4"/>',
 "award": '<circle cx="12" cy="8" r="6"/><path d="M15.5 12.9 17 22l-5-3-5 3 1.5-9.1"/>',
 "clipboard": '<rect x="8" y="2" width="8" height="4" rx="1"/><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2M9 14l2 2 4-4"/>',
 "card": '<rect x="2" y="5" width="20" height="14" rx="2"/><path d="M2 10h20M6 15h4"/>',
 "check": '<path d="M20 6 9 17l-5-5"/>',
 "checkc": '<circle cx="12" cy="12" r="10"/><path d="m9 12 2 2 4-4"/>',
 "alert": '<circle cx="12" cy="12" r="10"/><path d="M12 8v4M12 16h.01"/>',
 "clock": '<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>',
 "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
 "chev": '<path d="m6 9 6 6 6-6"/>',
 "pin": '<path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0z"/><circle cx="12" cy="10" r="3"/>',
 "mail": '<rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-10 6L2 7"/>',
 "x": '<path d="M18 6 6 18M6 6l12 12"/>',
 "fb": '<path d="M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3z"/>',
 "ig": '<rect x="2" y="2" width="20" height="20" rx="5"/><circle cx="12" cy="12" r="4"/><path d="M17.5 6.5h.01"/>',
}
def ico(n, cls=""):
    c = f' class="{cls}"' if cls else ""
    return f'<svg{c} viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">{I[n]}</svg>'
STAR = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="m12 2 3.1 6.3 6.9 1-5 4.9 1.2 6.8L12 17.8 5.8 21l1.2-6.8-5-4.9 6.9-1z"/></svg>'
STARS = f'<span class="stars" role="img" aria-label="5 out of 5 stars">{STAR*5}</span>'

# Decorative split-hex line motif (echoes the logo; aria-hidden)
HEX = '''<svg viewBox="0 0 200 174" fill="none" stroke="#fff" stroke-width="3" aria-hidden="true" focusable="false"><path d="M50 2h45v170H50L2 87z"/><path d="M105 2h45l48 85-48 85h-45z"/><path d="M80 87H30M70 70l10 17-10 17M55 62l8 8M55 112l8-8M45 87l-8-8M45 87l-8 8M80 40v94"/><path d="M118 87h60M118 87l40-30M118 87l40 30M118 87l20-50M118 87l20 50"/></svg>'''

PAGES = []  # (path, priority)

def call_btn(loc, cls="btn btn-call pulse", label=None, big=False, aria=None):
    lab = label or f'Call <span class="num">{PHONE}</span>'
    size = " btn-lg" if big else ""
    al = f' aria-label="{aria}"' if aria else ""
    return f'<a class="{cls}{size}" href="tel:{TEL}" data-loc="{loc}"{al}>{ico("phone","ico-phone")}<span>{lab}</span></a>'

def head(title, desc, path, schema=None, noindex=False, og_img="/assets/img/og-image.jpg"):
    url = DOMAIN + path
    sch = "".join(f'<script type="application/ld+json">{json.dumps(s, separators=(",",":"))}</script>' for s in (schema or []))
    robots = '<meta name="robots" content="noindex, follow">' if noindex else '<meta name="robots" content="index, follow, max-image-preview:large">'
    return f'''<!doctype html>
<html lang="en-US">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta http-equiv="Content-Security-Policy" content="upgrade-insecure-requests">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
{robots}
<link rel="canonical" href="{url}">
<meta name="theme-color" content="#0B1F3F">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Tropical Aire Mechanical &amp; Sheetmetal">
<meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{E(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{DOMAIN}{og_img}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Tropical Aire: NYC heating &amp; cooling. Call {PHONE}">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{E(title)}">
<meta name="twitter:description" content="{E(desc)}">
<meta name="twitter:image" content="{DOMAIN}{og_img}">
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" type="image/png" sizes="32x32" href="/assets/img/icon-32.png">
<link rel="apple-touch-icon" href="/assets/img/icon-180.png">
<link rel="manifest" href="/site.webmanifest">
<link rel="preload" href="/assets/fonts/lexend.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/assets/fonts/inter.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" as="image" href="/assets/img/logo.webp" type="image/webp">
<link rel="stylesheet" href="/assets/css/site.css">
<script>document.documentElement.classList.add('js')</script>
{sch}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<div class="scroll-progress" aria-hidden="true"></div>
'''

def svc_url(s): return f"/services/{s['slug']}/"

def header():
    cols = {"cool": "Cooling", "heat": "Heating & Hot Water", "other": "Commercial & Air"}
    mega = ""
    for k, lab in cols.items():
        items = "".join(f'<li><a href="{svc_url(s)}">{E(s["name"])}</a></li>' for s in SERVICES if s["cat"] == k)
        mega += f'<div><h4>{lab}</h4><ul>{items}</ul></div>'
    return f'''<div class="topbar"><div class="wrap">
<span data-open-status><span class="dot" aria-hidden="true"></span>Mon–Fri 7:00am–4:30pm</span>
<span class="hide-sm">Serving Queens, Brooklyn, Manhattan, the Bronx &amp; Long Island</span>
<a href="tel:{TEL}" data-loc="topbar">{PHONE}</a>
</div></div>
<header class="site-header">
<div class="wrap">
<a class="brand" href="/" aria-label="Tropical Aire home"><picture><source srcset="/assets/img/logo.webp 1x, /assets/img/logo@2x.webp 2x" type="image/webp"><img src="/assets/img/logo.png" width="600" height="156" alt="Tropical Aire Mechanical and Sheetmetal logo"></picture></a>
<nav class="nav" aria-label="Main">
<ul>
<li class="has-mega"><button class="nl" type="button" aria-expanded="false" aria-controls="mega-services">Services {ico("chev","chev")}</button>
<div class="mega" id="mega-services">{mega}</div></li>
<li><a class="nl" href="/#rebates">Rebates</a></li>
<li><a class="nl" href="/#financing">Financing</a></li>
<li><a class="nl" href="/#reviews">Reviews</a></li>
<li><a class="nl" href="/#areas">Service Areas</a></li>
</ul>
<div class="header-call">{call_btn("header", "btn btn-call", f'<span class="label">Call </span><span class="num">{PHONE}</span>', aria=f"Call {PHONE}")}</div>
<button class="menu-toggle" type="button" aria-expanded="false" aria-label="Open menu"><span></span></button>
</nav>
</div>
</header>
'''

SERVICE_OPTS = ["AC Repair","AC Installation / Replacement","AC Maintenance","Heating / Furnace Repair","Furnace Installation / Replacement","Furnace Maintenance","Ductless Mini-Split / Heat Pump","Water Heater","Commercial HVAC","Ductwork / Aeroseal","Indoor Air Quality","Something else"]

def lead_form(preselect=None, fid="hero"):
    opts = "".join(f'<option{" selected" if o == preselect else ""}>{E(o)}</option>' for o in SERVICE_OPTS)
    return f'''<div class="form-card" id="estimate">
<h2>Get a free estimate</h2>
<p class="fine">Takes about 30 seconds. We call back fast during business hours.</p>
<form name="estimate" method="POST" action="/api/lead" data-lead novalidate>
<input type="hidden" name="_ts" value="">
<input type="hidden" name="page" value="">
<p class="hp" aria-hidden="true"><label>Leave this empty <input name="company_website" tabindex="-1" autocomplete="off"></label></p>
<div class="form-grid">
<div class="field"><label for="{fid}-name">Name</label><input id="{fid}-name" name="name" autocomplete="name" required aria-describedby="{fid}-name-e"><div class="err" id="{fid}-name-e" aria-live="polite"></div></div>
<div class="field"><label for="{fid}-phone">Phone</label><input id="{fid}-phone" name="phone" type="tel" inputmode="tel" autocomplete="tel" required placeholder="(718) 555-0123" aria-describedby="{fid}-phone-e"><div class="err" id="{fid}-phone-e" aria-live="polite"></div></div>
<div class="field"><label for="{fid}-zip">ZIP code</label><input id="{fid}-zip" name="zip" inputmode="numeric" autocomplete="postal-code" maxlength="5" required aria-describedby="{fid}-zip-e"><div class="err" id="{fid}-zip-e" aria-live="polite"></div></div>
<div class="field"><label for="{fid}-service">I need help with</label><select id="{fid}-service" name="service" required aria-describedby="{fid}-service-e"><option value="">Choose one…</option>{opts}</select><div class="err" id="{fid}-service-e" aria-live="polite"></div></div>
<div class="field full"><label for="{fid}-email">Email <span style="font-weight:400;color:#4A5A75">(optional)</span></label><input id="{fid}-email" name="email" type="email" autocomplete="email" aria-describedby="{fid}-email-e"><div class="err" id="{fid}-email-e" aria-live="polite"></div></div>
</div>
<button class="btn btn-submit" type="submit">Request my free estimate</button>
<div class="form-status" role="status" aria-live="polite"></div>
<p class="privacy-note">By submitting, you agree we may contact you about your request by phone, text or email. No spam, ever. See our <a href="/privacy/">Privacy Policy</a>.</p>
</form>
<p class="form-alt">Faster: talk to a real person</p>
{call_btn("form", "btn btn-call")}
</div>'''

def hero_home():
    return f'''<section class="hero" data-mode="cool" aria-labelledby="h1">
<div class="hex-motif">{HEX}</div>
<div class="wrap hero-grid">
<div>
<div class="mode-switch rise" role="group" aria-label="What do you need?">
<span class="knob" aria-hidden="true"></span>
<button type="button" data-set="cool" aria-pressed="true">{ico("snow")}Cooling</button>
<button type="button" data-set="heat" aria-pressed="false">{ico("flame")}Heating</button>
</div>
<h1 id="h1" class="rise d1">NYC's 5-Star HVAC Team. <span class="swap"><span class="c accent">Cool Comfort, Today.</span><span class="h accent">Warm Again, Today.</span></span></h1>
<p class="lead rise d2">Same-day heating and cooling repair, installation and maintenance for homes and businesses across Queens, Brooklyn, Manhattan, the Bronx and Long Island. Honest pricing, no pushy sales.</p>
<div class="hero-ctas rise d3">
<div>{call_btn("hero", big=True)}<span class="sub">Free estimates · Upfront quotes · Real local techs</span></div>
</div>
<ul class="trust-row rise d4">
<li>{STARS} 5-star rated on Google &amp; Facebook</li>
<li>{ico("shield")} Licensed &amp; insured</li>
<li>{ico("dollar")} Rebates up to $10,000</li>
</ul>
</div>
<div class="rise d2">{lead_form()}</div>
</div>
</section>'''

PROOF = f'''<div class="proof-strip"><div class="wrap">
<span class="chip">{ico("award")} Authorized Daikin &amp; Amana Dealer</span>
<span class="chip">{ico("wind")} Aeroseal Certified Professional</span>
<span class="chip">{ico("leaf")} Supporting NYC's Clean Heat Program</span>
<span class="chip">{ico("building")} Residential &amp; Commercial</span>
</div></div>'''

def svc_card(s, i=0):
    heat = " heat" if s["cat"] == "heat" else ""
    return f'''<a class="card{heat} rv d{i%4+1}" href="{svc_url(s)}"><span class="ico">{ico(s["icon"])}</span><h3>{E(s["name"])}</h3><p>{E(s["short"])}</p><span class="more">Learn more {ico("arrow")}</span></a>'''

def services_grid():
    out = ""
    for k, lab in [("cool","Cooling"),("heat","Heating &amp; Hot Water"),("other","Commercial, Ductwork &amp; Air Quality")]:
        cls = " heat" if k == "heat" else ""
        cards = "".join(svc_card(s, i) for i, s in enumerate([x for x in SERVICES if x["cat"] == k]))
        out += f'<h3 class="cat-title{cls}"><span class="bar" aria-hidden="true"></span>{lab}</h3><div class="grid-4">{cards}</div>'
    return out

PROMISE = f'''<section class="section promise" id="why-us" aria-labelledby="why-h">
<div class="wrap">
<div class="section-head rv"><span class="eyebrow" style="color:#7CC7F2">The Tropical Aire Promise</span>
<h2 id="why-h">Show up on time. Do the job right. Treat every property like our own.</h2>
<p class="lead">This is how we've earned a 5-star reputation in NYC, one honest service call at a time.</p></div>
<div class="promise-grid">
<div class="promise-item rv d1">{ico("dollar")}<h3>Repair cost credited to a new system</h3><p>If your unit can't be saved, we explain your options and apply your repair visit cost toward the new install. You never pay twice.</p></div>
<div class="promise-item rv d2">{ico("clipboard")}<h3>Upfront quotes. Zero upsells.</h3><p>You get a clear price before any work starts, with no surprises and no high-pressure sales.</p></div>
<div class="promise-item rv d3">{ico("truck")}<h3>Fixed on the first visit</h3><p>Our fully stocked vans mean most issues are fixed the same day.</p></div>
<div class="promise-item rv d1">{ico("shield")}<h3>Backed by our service warranty</h3><p>Repairs are covered by our service warranty, carried out by licensed and insured technicians.</p></div>
<div class="promise-item rv d2">{ico("bolt")}<h3>Same-day or next-day</h3><p>Fast response in most boroughs, including emergency repair, with no waiting and no worry.</p></div>
<div class="promise-item rv d3">{ico("home")}<h3>Respectful, clean techs</h3><p>We protect your floors, explain everything clearly and leave the space spotless.</p></div>
</div>
</div></section>'''

def steps_block(title="What happens when you call"):
    return f'''<section class="section" aria-labelledby="steps-h"><div class="wrap">
<div class="section-head center rv" style="text-align:center"><span class="eyebrow">Simple, honest process</span><h2 id="steps-h">{title}</h2></div>
<div class="steps"><span class="fill" aria-hidden="true"></span>
<div class="step"><h3>Quick diagnosis</h3><p>We assess the issue on-site and explain the cause in plain English.</p></div>
<div class="step"><h3>Upfront estimate</h3><p>You get a clear quote with no upsells, and you approve it before we start.</p></div>
<div class="step"><h3>On-the-spot fix</h3><p>Fully stocked vans mean most issues are fixed the same day.</p></div>
<div class="step"><h3>Full system check</h3><p>We confirm everything is performing properly before we leave.</p></div>
</div>
<p class="center" style="text-align:center;margin-top:40px">{call_btn("steps")}</p>
</div></section>'''

def reviews_block():
    cards = "".join(f'''<figure class="review rv d{i+1}">{STARS}<blockquote>“{E(t)}”</blockquote><footer><span class="av" aria-hidden="true">{n[0]}</span><span><strong>{n}</strong>Google review</span></footer></figure>''' for i, (n, t) in enumerate(REVIEWS))
    return f'''<section class="section alt" id="reviews" aria-labelledby="rev-h"><div class="wrap">
<div class="section-head rv"><span class="eyebrow">5-star rated on Google &amp; Facebook</span><h2 id="rev-h">New Yorkers trust us with their comfort</h2></div>
<div class="reviews">{cards}</div>
</div></section>'''

REBATE = f'''<section class="section" id="rebates" aria-labelledby="reb-h"><div class="wrap">
<div class="rebate rv">
<div><span class="eyebrow" style="color:#FFC93C">Con Edison Clean Heat Program</span>
<h2 id="reb-h">Upgrade to a heat pump and get money back</h2>
<p>NYC's Clean Heat incentives can cover a big share of a heat pump or ductless upgrade. We check your eligibility, size the system and handle the rebate paperwork for you.</p>
{call_btn("rebate")}</div>
<div class="big"><small>Rebates up to</small><span data-count="10000" data-pre="$">$10,000</span></div>
</div></div></section>'''

FINANCING = f'''<section class="section alt" id="financing" aria-labelledby="fin-h"><div class="wrap split">
<div class="rv"><span class="eyebrow">Flexible financing</span><h2 id="fin-h">Comfort now. Easy payments later.</h2>
<p class="lead">Quick application, fast approval. Find the right financing option for your new AC, furnace, heat pump or water heater.</p>
{call_btn("financing")}</div>
<div class="callout rv d2"><h3>Free estimates on every install</h3>
<ul class="check-list">
<li>{ico("checkc")} Free in-home consultation and estimate</li>
<li>{ico("checkc")} Honest recommendations with no pressure</li>
<li>{ico("checkc")} Rebates and financing combined for the lowest cost</li>
<li>{ico("checkc")} Authorized Daikin &amp; Amana dealer, with more brands available</li>
</ul></div>
</div></section>'''

def areas_block():
    pills = "".join(f'<span class="pill">{ico("pin") if False else ""}{a}</span>' for a in AREAS)
    return f'''<section class="section" id="areas" aria-labelledby="area-h"><div class="wrap">
<div class="section-head rv"><span class="eyebrow">Local NYC technicians you can count on</span><h2 id="area-h">Proudly serving the five boroughs &amp; Long Island</h2>
<p class="lead">Based at 152-32 Rockaway Blvd in Jamaica, Queens, and on the road across NYC every weekday.</p></div>
</div>
<div class="marquee" aria-label="Service areas"><div class="marquee-track">{pills}{pills.replace('class="pill"','class="pill" aria-hidden="true"')}</div></div>
</section>'''

def faq_block(faqs):
    items = "".join(f'<details class="rv"><summary>{E(q)}</summary><div class="ans"><p>{E(a)}</p></div></details>' for q, a in faqs)
    return f'''<section class="section alt" aria-labelledby="faq-h"><div class="wrap">
<div class="section-head center rv" style="text-align:center"><span class="eyebrow">FAQ</span><h2 id="faq-h">Questions, answered</h2></div>
<div class="faq">{items}</div></div></section>'''

def final_cta(h="Don't sweat it. Don't freeze. Just call.", p="Talk to a real local technician. Free estimates, upfront pricing and same-day service in most boroughs."):
    return f'''<section class="section final-cta" aria-labelledby="cta-h"><div class="hex-bg">{HEX}</div><div class="wrap" style="position:relative">
<h2 id="cta-h" class="rv">{h}</h2><p class="rv d1">{p}</p>
<div class="rv d2">{call_btn("final-cta", big=True)}</div></div></section>'''

def footer():
    svc = "".join(f'<li><a href="{svc_url(s)}">{E(s["name"])}</a></li>' for s in SERVICES[:6])
    svc2 = "".join(f'<li><a href="{svc_url(s)}">{E(s["name"])}</a></li>' for s in SERVICES[6:])
    return f'''<footer class="site-footer">
<div class="wrap">
<div class="foot-grid">
<div class="foot-brand"><picture><source srcset="/assets/img/logo-white.webp 1x, /assets/img/logo-white@2x.webp 2x" type="image/webp"><img src="/assets/img/logo-white.png" width="600" height="156" alt="Tropical Aire Mechanical and Sheetmetal logo" loading="lazy"></picture>
<p>Top-rated heating, cooling and sheet metal for NYC homes and businesses. Honest pricing, no pressure, and comfort every time.</p>
<div class="socials"><a href="https://www.facebook.com/p/Tropical-Aire-LLC-61576816213095/" aria-label="Tropical Aire on Facebook (opens in new tab)" rel="noopener" target="_blank">{ico("fb")}</a><a href="https://share.google/99wc0b7RLgry2ci7D" aria-label="Tropical Aire reviews on Google (opens in new tab)" rel="noopener" target="_blank">{STAR}</a></div></div>
<div><h3>Services</h3><ul>{svc}</ul></div>
<div><h3>More services</h3><ul>{svc2}<li><a href="/services/">All services</a></li></ul></div>
<div><h3>Contact</h3><ul>
<li><a href="tel:{TEL}" data-loc="footer"><strong>{PHONE}</strong></a></li>
<li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
<li>{ADDR}</li>
<li>Mon–Fri: 7:00am – 4:30pm</li>
<li><a href="https://clienthub.getjobber.com/client_hubs/9861464c-e2c2-43b8-87b7-5f9cd1b39380/login/new?source=share_login" rel="noopener" target="_blank">Client login</a></li>
</ul></div>
</div>
<div class="foot-bottom">
<span>© <span data-year>2026</span> Tropical Aire Mechanical &amp; Sheetmetal. All rights reserved.</span>
<ul><li><a href="/privacy/">Privacy Policy</a></li><li><a href="/terms/">Terms &amp; Conditions</a></li><li><a href="/accessibility/">Accessibility</a></li><li><a href="/sitemap.xml">Sitemap</a></li><li><button type="button" data-cookie-settings>Cookie settings</button></li></ul>
</div>
</div>
</footer>'''

def chrome_end():
    return f'''<div class="urgency-bar" role="region" aria-label="Call now">
<div class="wrap">
<div class="msg"><span class="flame" aria-hidden="true">{ico("bolt")}</span><div><strong data-urgency-title>Same-day service available in most boroughs</strong><span data-urgency-sub>Call before 2 PM for a same-day slot. Fully stocked vans fix most issues on the first visit.</span></div></div>
{call_btn("sticky-bar", label='Call Now <span class="num hide-xs">· ' + PHONE + '</span>')}
</div></div>

<div class="modal" id="exit-offer" role="dialog" aria-modal="true" aria-labelledby="exit-h" hidden>
<div class="modal-box">
<button class="modal-close" type="button" data-close aria-label="Close offer">{ico("x")}</button>
<div class="modal-top">
<span class="kicker">Wait! Before you go</span>
<div class="amount" aria-hidden="true">{OFFER} OFF</div>
<h2 id="exit-h" style="color:#fff;font-size:1.35rem;margin:0 0 4px">Your first service call, {OFFER} cheaper</h2>
<p>For first-time customers who book today. Mention the code when you call.</p>
</div>
<div class="modal-body">
<div class="code"><span>Your code: <b>{OFFER_CODE}</b></span><button type="button" data-copy="{OFFER_CODE}">Copy code</button></div>
{call_btn("exit-offer", "btn btn-call pulse btn-block", f'Call &amp; claim {OFFER} off')}
<p class="terms">One per household. Cannot be combined with other offers. Valid on repair or service visits.</p>
<button class="nothanks" type="button" data-close>No thanks, I'll pay full price</button>
</div>
</div>
</div>

<div class="cookie" id="cookie" role="dialog" aria-live="polite" aria-labelledby="cookie-h" hidden>
<h2 id="cookie-h">We value your privacy</h2>
<p>We use essential cookies to run this site and, with your permission, analytics cookies to understand how it's used. Read our <a href="/privacy/#cookies">Privacy Policy</a>.</p>
<div class="row"><button class="btn accept" type="button" data-consent="accept">Accept all</button><button class="btn btn-ghost" type="button" data-consent="reject">Essential only</button></div>
</div>
<script src="/assets/js/site.js" defer></script>
</body>
</html>
'''

BUSINESS = {
 "@context":"https://schema.org","@type":"HVACBusiness","@id":DOMAIN+"/#business",
 "name":"Tropical Aire Mechanical & Sheetmetal","url":DOMAIN+"/","telephone":"+1-718-766-0889","email":EMAIL,
 "image":DOMAIN+"/assets/img/og-image.jpg","logo":DOMAIN+"/assets/img/logo-hires-transparent.png",
 "address":{"@type":"PostalAddress","streetAddress":"152-32 Rockaway Blvd","addressLocality":"Jamaica","addressRegion":"NY","postalCode":"11434","addressCountry":"US"},
 "openingHoursSpecification":[{"@type":"OpeningHoursSpecification","dayOfWeek":["Monday","Tuesday","Wednesday","Thursday","Friday"],"opens":"07:00","closes":"16:30"}],
 "areaServed":[{"@type":"Place","name":a} for a in AREAS],
 "priceRange":"$$",
 "sameAs":["https://www.facebook.com/p/Tropical-Aire-LLC-61576816213095/","https://share.google/99wc0b7RLgry2ci7D"],
 "geo":{"@type":"GeoCoordinates","latitude":40.6716269,"longitude":-73.785126},
}

def write(path, content, priority="0.8", index=True):
    full = os.path.join(OUT, path.strip("/"), "index.html") if not path.endswith(".html") else os.path.join(OUT, path.strip("/"))
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, "w").write(content)
    if index: PAGES.append((path, priority))

# ---------------- Home ----------------
home = head("Tropical Aire | 5-Star HVAC Repair & Installation in NYC & Long Island",
            "Same-day AC, heating & water heater service for NYC homes & businesses. Free estimates, upfront pricing, rebates up to $10,000. Call (718) 766-0889.",
            "/", [BUSINESS]) + header() + '<main id="main">' + hero_home() + PROOF + f'''
<section class="section" id="services" aria-labelledby="svc-h"><div class="wrap">
<div class="section-head rv"><span class="eyebrow">Everything heating, cooling &amp; sheet metal</span><h2 id="svc-h">One trusted team for every system in your building</h2>
<p class="lead">Residential and commercial. Repair, replacement and maintenance. Pick your service, or just call and we'll point you the right way.</p></div>
{services_grid()}
</div></section>''' + PROMISE + steps_block() + REBATE + reviews_block() + FINANCING + areas_block() + faq_block([
 ("How fast can you get to me?","We offer same-day or next-day service in most boroughs. Call before 2 PM for the best chance of a same-day slot."),
 ("Are estimates free?","Yes. Consultations and estimates are free, and you approve a clear, upfront price before any work starts."),
 ("What if my system can't be repaired?","We'll explain your options honestly, and if you choose a replacement, your repair visit cost is applied toward the new install."),
 ("Do you help with Con Edison rebates?","Yes. We support NYC's Clean Heat program and help eligible customers claim rebates up to $10,000 on heat pump and ductless upgrades."),
 ("Do you work on commercial properties?","Yes. We handle rooftop units, system design and build-outs, custom ductwork and sheet metal, and commercial repair."),
 ("What are your hours?","Monday to Friday, 7:00am to 4:30pm. Submit the form any time and we'll call you back first thing."),
]) + final_cta() + '</main>' + footer() + chrome_end()
write("/", home, "1.0")

# ---------------- Service pages ----------------
def related(s):
    rel = [x for x in SERVICES if x["cat"] == s["cat"] and x["slug"] != s["slug"]][:3]
    if len(rel) < 3: rel += [x for x in SERVICES if x not in rel and x["slug"] != s["slug"]][:3-len(rel)]
    return "".join(svc_card(x, i) for i, x in enumerate(rel))

PRESELECT = {"ac-repair":"AC Repair","ac-installation-replacement":"AC Installation / Replacement","ac-maintenance":"AC Maintenance",
 "furnace-repair":"Heating / Furnace Repair","furnace-installation-replacement":"Furnace Installation / Replacement","furnace-maintenance":"Furnace Maintenance",
 "ductless-mini-splits-heat-pumps":"Ductless Mini-Split / Heat Pump","water-heaters":"Water Heater","commercial-hvac":"Commercial HVAC",
 "ductwork-sheet-metal":"Ductwork / Aeroseal","indoor-air-quality":"Indoor Air Quality"}

for s in SERVICES:
    url = svc_url(s)
    mode = "heat" if s["cat"] == "heat" else "cool"
    schema = [
      {"@context":"https://schema.org","@type":"Service","name":s["name"],"serviceType":s["name"],"provider":{"@id":DOMAIN+"/#business"},"areaServed":AREAS,"url":DOMAIN+url,"description":s["desc"]},
      {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in s["faq"]]},
      {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Home","item":DOMAIN+"/"},{"@type":"ListItem","position":2,"name":"Services","item":DOMAIN+"/services/"},{"@type":"ListItem","position":3,"name":s["name"],"item":DOMAIN+url}]},
      BUSINESS]
    signs = "".join(f'<li class="rv">{ico("alert")}<span>{E(x)}</span></li>' for x in s["signs"])
    why = "".join(f'<div class="card rv d{i+1}"><span class="ico">{ico(ic)}</span><h3>{E(t)}</h3><p>{E(d)}</p></div>' for i,(ic,t,d) in enumerate(s["why"]))
    heatcls = ' heat' if s['cat']=='heat' else ''
    page = head(s["title"], s["desc"], url, schema) + header() + f'''<main id="main">
<section class="hero" data-mode="{mode}" aria-labelledby="h1">
<div class="hex-motif">{HEX}</div>
<div class="wrap hero-grid">
<div>
<nav class="crumbs rise" aria-label="Breadcrumb"><a href="/">Home</a><span aria-hidden="true">/</span><a href="/services/">Services</a><span aria-hidden="true">/</span><span aria-current="page" style="margin:0;opacity:1">{E(s["name"])}</span></nav>
<h1 id="h1" class="rise d1">{E(s["h1a"])} <span class="accent">{E(s["h1b"])}</span></h1>
<p class="lead rise d2">{E(s["lead"])}</p>
<div class="hero-ctas rise d3"><div>{call_btn("hero", big=True)}<span class="sub">Free estimates · Upfront quotes · Licensed &amp; insured</span></div></div>
<ul class="trust-row rise d4"><li>{STARS} 5-star rated</li><li>{ico("clock")} Same-day / next-day</li><li>{ico("shield")} Service warranty</li></ul>
</div>
<div class="rise d2">{lead_form(PRESELECT[s["slug"]])}</div>
</div></section>
{PROOF}
<section class="section" aria-labelledby="signs-h"><div class="wrap split">
<div class="rv"><span class="eyebrow">Know the signs</span><h2 id="signs-h">When to call for {E(s["name"].lower())}</h2>
<p class="lead">Spotting a problem early usually means a smaller, cheaper fix. If any of these sound familiar, give us a call.</p>
{call_btn("signs")}</div>
<ul class="check-list">{signs}</ul>
</div></section>
<section class="section alt" aria-labelledby="why-h"><div class="wrap">
<div class="section-head rv"><span class="eyebrow">Why NYC chooses Tropical Aire</span><h2 id="why-h">Honest work you can count on</h2></div>
<div class="grid-4">{why.replace('class="card', 'class="card' + heatcls)}</div>
</div></section>
{steps_block()}
{reviews_block()}
<section class="section" aria-labelledby="money-h"><div class="wrap"><div class="rebate rv">
<div><span class="eyebrow" style="color:#FFC93C">Save more</span><h2 id="money-h">Rebates, financing &amp; your repair cost credited</h2>
<p>Ask about Con Edison Clean Heat rebates up to $10,000 and flexible financing. If a repair turns into a replacement, we apply your repair visit cost toward the new system.</p>{call_btn("savings")}</div>
<div class="big"><small>Rebates up to</small><span data-count="10000" data-pre="$">$10,000</span></div>
</div></div></section>
{faq_block(s["faq"])}
<section class="section" aria-labelledby="rel-h"><div class="wrap"><div class="section-head rv"><span class="eyebrow">Related services</span><h2 id="rel-h">You might also need</h2></div><div class="grid-3">{related(s)}</div></div></section>
{final_cta()}
</main>''' + footer() + chrome_end()
    write(url, page, "0.9")

# ---------------- Services hub ----------------
hub = head("HVAC Services in NYC & Long Island | Tropical Aire", "Heating, cooling, ductless, water heaters, commercial HVAC, ductwork & indoor air quality across NYC & Long Island. Free estimates. Call (718) 766-0889.", "/services/", [BUSINESS]) + header() + f'''<main id="main">
<section class="hero" data-mode="cool" aria-labelledby="h1"><div class="hex-motif">{HEX}</div><div class="wrap hero-grid">
<div><nav class="crumbs rise" aria-label="Breadcrumb"><a href="/">Home</a><span aria-hidden="true">/</span><span aria-current="page" style="margin:0;opacity:1">Services</span></nav>
<h1 id="h1" class="rise d1">Every HVAC service. <span class="accent">One honest team.</span></h1>
<p class="lead rise d2">Cooling, heating, hot water, ductless, commercial and sheet metal for homes and businesses across NYC and Long Island.</p>
<div class="hero-ctas rise d3"><div>{call_btn("hero", big=True)}<span class="sub">Free estimates · Same-day in most boroughs</span></div></div></div>
<div class="rise d2">{lead_form()}</div></div></section>
{PROOF}
<section class="section"><div class="wrap">{services_grid()}</div></section>
{final_cta()}</main>''' + footer() + chrome_end()
write("/services/", hub, "0.8")

# ---------------- Legal ----------------
LEGAL_UPDATED = "2026-11-06"  # bump when the legal text changes
def legal(path, title, desc, h1, body, updated=LEGAL_UPDATED):
    return head(title, desc, path) + header() + f'''<main id="main" class="legal">
<section class="hero" data-mode="cool" style="padding:56px 0"><div class="wrap"><nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a><span aria-hidden="true">/</span><span aria-current="page" style="margin:0;opacity:1">{h1}</span></nav><h1 style="margin:0">{h1}</h1><p class="lead" style="margin-top:12px">Last updated: {datetime.date.fromisoformat(updated).strftime("%B %-d, %Y")}</p></div></section>
<section class="section"><div class="wrap"><div class="prose">{body}</div></div></section>
</main>''' + footer() + chrome_end()

PRIV = f'''<p>Tropical Aire Mechanical &amp; Sheetmetal ("Tropical Aire", "we", "us") respects your privacy. This policy explains what we collect when you visit <strong>tropical-aire.com</strong> or contact us, how we use it, and your choices.</p>
<h2>Information we collect</h2>
<ul><li><strong>Information you give us:</strong> your name, phone number, ZIP code, email address and details of the service you need, when you submit a form, call, text or email us.</li>
<li><strong>Information collected automatically:</strong> with your consent, analytics data such as pages viewed, device and browser type, approximate location (city level) and how you arrived at our site.</li>
<li><strong>Call information:</strong> if you click a phone link, we may record (with consent) that the click happened, but not the content of your call.</li></ul>
<h2>How we use your information</h2>
<ul><li>To respond to your request, schedule service and provide estimates.</li><li>To send appointment confirmations, reminders and service follow-ups.</li><li>To improve our website and services.</li><li>To comply with legal obligations.</li></ul>
<p>We do <strong>not</strong> sell or rent your personal information. We do not share your mobile number or SMS opt-in with third parties for their marketing.</p>
<h2>Calls, texts and emails</h2>
<p>When you submit a form, you agree we may contact you about your request by phone, text or email. Message and data rates may apply. Reply STOP to opt out of texts, or ask us at any time to stop contacting you.</p>
<h2 id="cookies">Cookies and analytics</h2>
<p>We use essential cookies and local storage to make the site work, for example to remember your cookie choice. With your consent, we use Google Analytics 4 to understand site usage. Analytics stays off until you click "Accept all" in our cookie banner. You can change your choice at any time using the "Cookie settings" link in the footer.</p>
<h2>Service providers</h2>
<p>We use trusted providers to host our website and process form submissions (Vercel), deliver lead notifications to our team, measure site usage (Google Analytics, only with consent) and manage scheduling and customer accounts (Jobber). They may process your data only on our behalf.</p>
<h2>Data retention and security</h2>
<p>We keep your information only as long as needed for the purposes above or as required by law, and protect it with reasonable administrative, technical and physical safeguards. Our site is served only over encrypted HTTPS.</p>
<h2>Your rights</h2>
<p>You can ask us to access, correct or delete your personal information, or to stop contacting you. Depending on where you live, you may have additional rights under applicable privacy laws. Email <a href="mailto:{EMAIL}">{EMAIL}</a> or call <a href="tel:{TEL}">{PHONE}</a>.</p>
<h2>Children</h2><p>Our site is not directed to children under 13, and we do not knowingly collect their information.</p>
<h2>Changes</h2><p>We may update this policy and will post the new version on this page with a new "last updated" date.</p>
<h2>Contact</h2><p>Tropical Aire Mechanical &amp; Sheetmetal, {ADDR} · <a href="tel:{TEL}">{PHONE}</a> · <a href="mailto:{EMAIL}">{EMAIL}</a></p>'''
write("/privacy/", legal("/privacy/", "Privacy Policy | Tropical Aire", "How Tropical Aire collects, uses and protects your personal information, plus your cookie and contact choices.", "Privacy Policy", PRIV), "0.3")

TERMS = f'''<p>These Terms &amp; Conditions govern your use of <strong>tropical-aire.com</strong>. By using this site, you agree to them.</p>
<h2>Website information</h2><p>Content on this site is for general information. Service availability, response times, rebates and financing depend on your location, equipment, eligibility and scheduling, and are not guaranteed until confirmed by Tropical Aire.</p>
<h2>Estimates and pricing</h2><p>Estimates are free and provided after assessment. Final pricing is confirmed in writing (or verbally by your technician) and approved by you before work begins.</p>
<h2>Promotions</h2><p>Online offers, including any discount code shown on this site, are limited to one per household, apply to new customers unless stated otherwise, cannot be combined with other offers, have no cash value, and may be changed or withdrawn at any time. The code must be mentioned when booking.</p>
<h2>Rebates and financing</h2><p>Rebates (including Con Edison Clean Heat incentives) are issued by third parties and subject to their eligibility rules and funding. Financing is subject to credit approval by the lender. We help with applications but do not guarantee approval or amounts.</p>
<h2>Warranties</h2><p>Repairs are backed by our service warranty, and equipment carries the manufacturer's warranty. Specific warranty terms are provided with your invoice or installation agreement.</p>
<h2>Scheduling and cancellations</h2><p>Please give us as much notice as possible if you need to reschedule. Arrival windows are estimates and may be affected by traffic, weather and emergencies.</p>
<h2>Acceptable use</h2><p>You agree not to misuse this site, submit false information, attempt to interfere with its operation, or send spam through our forms.</p>
<h2>Intellectual property</h2><p>The Tropical Aire name, logo and site content belong to Tropical Aire Mechanical &amp; Sheetmetal and may not be used without permission.</p>
<h2>Third-party links</h2><p>Links to third-party sites (for example, client login or financing partners) are provided for convenience, and we are not responsible for their content or policies.</p>
<h2>Limitation of liability</h2><p>To the fullest extent permitted by law, Tropical Aire is not liable for indirect or consequential damages arising from use of this website. Nothing here limits liability that cannot be limited by law.</p>
<h2>Governing law</h2><p>These terms are governed by the laws of the State of New York.</p>
<h2>Contact</h2><p>{ADDR} · <a href="tel:{TEL}">{PHONE}</a> · <a href="mailto:{EMAIL}">{EMAIL}</a></p>'''
write("/terms/", legal("/terms/", "Terms & Conditions | Tropical Aire", "Terms and conditions for using the Tropical Aire website, online offers, estimates, rebates and financing.", "Terms &amp; Conditions", TERMS), "0.3")

ACC = f'''<p>Tropical Aire is committed to making our website usable by everyone. We aim to meet the Web Content Accessibility Guidelines (WCAG) 2.2 Level AA.</p>
<h2>What we've done</h2><ul><li>Text and buttons meet WCAG AA colour-contrast ratios.</li><li>Everything can be used with a keyboard, with visible focus indicators and a skip-to-content link.</li><li>Images have descriptive alt text, and decorative graphics are hidden from screen readers.</li><li>Form fields have labels and clear, announced error messages.</li><li>Animations are turned off if your device is set to reduce motion.</li></ul>
<h2>Need help?</h2><p>If anything on this site is hard to use, call <a href="tel:{TEL}">{PHONE}</a> or email <a href="mailto:{EMAIL}">{EMAIL}</a> and we'll help you directly and fix the issue.</p>'''
write("/accessibility/", legal("/accessibility/", "Accessibility Statement | Tropical Aire", "Tropical Aire's commitment to an accessible website, and how to get help.", "Accessibility Statement", ACC), "0.2")

# ---------------- Thank you (noindex) ----------------
ty = head("Thank You | Tropical Aire", "Thanks for contacting Tropical Aire. We'll be in touch shortly.", "/thank-you/", noindex=True) + header() + f'''<main id="main"><section class="notfound"><div class="wrap">
<div class="thermo" style="color:#1D5AAB">{ico("checkc")}</div>
<h1>Thanks! Your request is in.</h1><p class="lead">A member of our team will call you back shortly during business hours (Mon–Fri, 7:00am–4:30pm). Need us sooner?</p>
<p>{call_btn("thank-you", big=True)}</p><p><a href="/">Back to home</a></p></div></section></main>''' + footer() + chrome_end()
write("/thank-you/", ty, index=False)

# ---------------- 404 ----------------
nf = head("Page Not Found | Tropical Aire", "Sorry, that page doesn't exist. Find heating and cooling help from Tropical Aire.", "/404.html", noindex=True) + header() + f'''<main id="main"><section class="notfound"><div class="wrap">
<div class="code" aria-hidden="true">404</div>
<h1>This page has gone cold.</h1>
<p class="lead">The link may be broken or the page may have moved. Here's where to find heat, cool air and help fast:</p>
<p style="display:flex;gap:12px;justify-content:center;flex-wrap:wrap">{call_btn("404", big=True)}</p>
<p style="display:flex;gap:10px 18px;justify-content:center;flex-wrap:wrap;margin-top:18px"><a href="/">Home</a><a href="/services/">All services</a><a href="/services/ac-repair/">AC repair</a><a href="/services/furnace-repair/">Furnace repair</a><a href="/#reviews">Reviews</a></p>
</div></section></main>''' + footer() + chrome_end()
write("/404.html", nf, index=False)

# ---------------- sitemap / robots / manifest ----------------
urls = "".join(f"<url><loc>{DOMAIN}{p}</loc><lastmod>{TODAY}</lastmod><priority>{pr}</priority></url>\n" for p, pr in PAGES)
open(f"{OUT}/sitemap.xml","w").write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n')
open(f"{OUT}/robots.txt","w").write(f"User-agent: *\nAllow: /\nDisallow: /thank-you/\n\nSitemap: {DOMAIN}/sitemap.xml\n")
open(f"{OUT}/site.webmanifest","w").write(json.dumps({"name":"Tropical Aire","short_name":"Tropical Aire","icons":[{"src":"/assets/img/icon-192.png","sizes":"192x192","type":"image/png"},{"src":"/assets/img/icon-512.png","sizes":"512x512","type":"image/png"}],"theme_color":"#0B1F3F","background_color":"#ffffff","display":"standalone","start_url":"/"}, indent=1))
print(len(PAGES), "indexed pages")
