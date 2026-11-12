#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate the static K&2P site in ko (root), en (/en/) and ja (/ja/).

    python3 _src/build.py

No dependencies beyond the Python 3 standard library. Copy lives in
_src/content.py; shared styles in assets/css/. Output HTML files are
committed so GitHub Pages can serve them without a build step.
"""
import html
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(__file__))
from content import ABOUT, COMMON, EXTRA, GUIDE, HOME, LANGS, LEGAL_DOCS, LEGAL_UI, LINE_URL, MP_BASE, SERVICES, SUPPORT_EMAIL  # noqa: E402
from sanitize import clean_html  # noqa: E402

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SITE = "https://kn2p.co.kr"
GA_ID = "G-DRZ7CXSHBG"
PAGES = ["index", "services", "guide", "about"]
LANG_DIR = {"ko": "", "en": "en/", "ja": "ja/"}
SHORT = {"ko": "KO", "en": "EN", "ja": "JA"}
MORIPAY = "https://moripay.com"


def esc(s):
    return html.escape(s, quote=True)


def page_url(lang, page):
    path = LANG_DIR[lang] + ("" if page == "index" else page + ".html")
    return f"{SITE}/{path}"


def up_of(lang, page="index"):
    """Relative prefix from a page back to the site root (pages may live in legal/)."""
    return "../" * ((1 if LANG_DIR[lang] else 0) + page.count("/"))


def rel(lang, target_lang, target, cur="index"):
    """Relative link from page `cur` in `lang` to page `target` in `target_lang`."""
    file = "index.html" if target == "index" else target + ".html"
    return up_of(lang, cur) + LANG_DIR[target_lang] + file


def load_legal():
    """{(slug, lang): document} for every legal document downloaded by fetch_legal.py."""
    docs = {}
    for slug in LEGAL_DOCS:
        for lang in LANGS:
            path = os.path.join(ROOT, "_src", "legal", f"{slug}.{lang}.json")
            if os.path.exists(path):
                with open(path, encoding="utf-8") as f:
                    docs[(slug, lang)] = json.load(f)
    return docs


LEGAL = load_legal()


ICONS = set()  # Material Symbols used on the site; the font request is subset to these


def icon(name):
    ICONS.add(name)
    return f'<span class="icon" aria-hidden="true">{name}</span>'


ORG = {
    "@type": "Organization",
    "@id": SITE + "/#organization",
    "name": "K&2P Co., Ltd.",
    "alternateName": ["케이앤투피", "주식회사 케이앤투피", "K&2P", "ケーアンドツーピー"],
    "url": SITE + "/",
    "logo": SITE + "/logo_horizontal_transparent.png",
    "telephone": "+82-2-498-3001",
    "taxID": "551-87-03073",
    "address": {
        "@type": "PostalAddress",
        "streetAddress": "25 Ttukseom-ro 1-gil, Halla Eco Valley 309",
        "addressLocality": "Seongdong-gu",
        "addressRegion": "Seoul",
        "addressCountry": "KR",
    },
    "brand": {"@type": "Brand", "name": "MoriPay", "url": MORIPAY},
    "sameAs": [MORIPAY],
}


WEBSITE = {
    "@type": "WebSite",
    "@id": SITE + "/#website",
    "url": SITE + "/",
    "name": "K&2P",
    "inLanguage": ["ko", "en", "ja"],
    "publisher": {"@id": SITE + "/#organization"},
}


def jsonld(lang, page, title, desc):
    graph = [ORG, WEBSITE, {
        "@type": "AboutPage" if page == "about" else "WebPage",
        "@id": page_url(lang, page) + "#webpage",
        "url": page_url(lang, page),
        "name": title,
        "description": desc,
        "inLanguage": lang,
        "isPartOf": {"@id": SITE + "/#website"},
        "about": {"@id": SITE + "/#organization"},
    }]
    data = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False)
    return f'<script type="application/ld+json">{data}</script>'


def head(lang, page, title, desc, langs=LANGS):
    c = COMMON[lang]
    up = up_of(lang, page)
    alternates = "\n".join(
        f'<link rel="alternate" hreflang="{l}" href="{page_url(l, page)}">' for l in langs
    )
    fonts = {
        "ko": "family=Noto+Sans+KR:wght@400;500;600;700;800",
        "en": "family=Noto+Sans+KR:wght@400;500;700",
        "ja": "family=Noto+Sans+JP:wght@400;500;600;700;800",
    }[lang]
    return f"""<!DOCTYPE html>
<html lang="{c['html_lang']}" data-astryx-theme="kn2p" data-theme="light">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
  gtag('config', '{GA_ID}');
</script>
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{page_url(lang, page)}">
{alternates}
<link rel="alternate" hreflang="x-default" href="{page_url('ko' if 'ko' in langs else langs[0], page)}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="K&amp;2P">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{page_url(lang, page)}">
<meta property="og:locale" content="{c['og_locale']}">
<meta property="og:image" content="{SITE}/assets/img/og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(desc)}">
<meta name="twitter:image" content="{SITE}/assets/img/og.png">
{jsonld(lang, page, title, desc)}
<meta name="theme-color" content="#f8fdff">
<link rel="icon" href="{up}assets/img/favicon.png" type="image/png">\n<link rel="apple-touch-icon" href="{up}assets/img/favicon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&amp;{fonts}&amp;display=swap">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@24,400,0,0&amp;icon_names=__ICON_NAMES__&amp;display=block">
<link rel="stylesheet" href="{up}assets/css/astryx-reset.css">
<link rel="stylesheet" href="{up}assets/css/astryx-tokens.css">
<link rel="stylesheet" href="{up}assets/css/kn2p-theme.css">
<link rel="stylesheet" href="{up}assets/css/site.css">
</head>
<body>
"""


def header(lang, page, langs=LANGS):
    c = COMMON[lang]
    up = up_of(lang, page)
    cur_page = ' aria-current="page"'
    cur_lang = ' aria-current="true"'
    nav = "".join(
        f'<a href="{rel(lang, lang, p, page)}"{cur_page if p == page else ""}>{esc(c["nav"][p])}</a>'
        for p in PAGES
    )
    switch = "".join(
        f'<a href="{rel(lang, l, page if l in langs else "index", page)}" hreflang="{l}" lang="{l}" title="{esc(COMMON[l]["lang_label"])}"'
        f'{cur_lang if l == lang else ""}>{SHORT[l]}</a>'
        for l in LANGS
    )
    return f"""<a class="skip-link" href="#main">{esc(c['skip'])}</a>
<header class="site-header">
  <div class="container">
    <a class="brand" href="{rel(lang, lang, 'index', page)}"><img src="{up}logo_horizontal_transparent.png" alt="K&amp;2P" width="94" height="30"></a>
    <nav class="nav" id="site-nav" aria-label="Main">{nav}<a class="nav-ext" href="{MP_BASE[lang]}" target="_blank" rel="noopener">{esc(c['cta_moripay'])} ↗</a></nav>
    <div class="header-actions">
      <div class="lang-switch" role="group" aria-label="Language">{switch}</div>
      <button class="menu-toggle" type="button" aria-controls="site-nav" aria-expanded="false" aria-label="{esc(c['menu'])}">{icon('menu')}</button>
    </div>
  </div>
</header>
<main id="main">
"""


def legal_links(lang, page="index"):
    """Footer links: microCMS documents rendered on this site, else their moripay.com fallback."""
    links = []
    for slug, doc in LEGAL_DOCS.items():
        if (slug, lang) in LEGAL:
            links.append(f'<a href="{rel(lang, lang, "legal/" + slug, page)}">{esc(doc["label"][lang])}</a>')
        elif doc["fallback"]:
            links.append(f'<a href="{MP_BASE[lang]}/legal/{doc["fallback"]}" target="_blank" rel="noopener">{esc(doc.get("fallback_label", doc["label"])[lang])}</a>')
    links += [f'<a href="{MP_BASE[lang]}/legal/{slug}" target="_blank" rel="noopener">{esc(label)}</a>' for slug, label in EXTRA[lang]["legal"]]
    return "".join(links)


def footer(lang, page="index"):
    c = COMMON[lang]
    up = up_of(lang, page)
    nav = "".join(f'<a href="{rel(lang, lang, p, page)}">{esc(c["nav"][p])}</a>' for p in PAGES)
    biz = "".join(f"<span>{esc(x)}</span>" for x in c["biz"])
    biz2 = "".join(f"<span>{esc(x)}</span>" for x in c["biz2"])
    x = EXTRA[lang]
    legal = legal_links(lang, page)
    return f"""</main>
<footer class="site-footer">
  <div class="container">
    <div class="top">
      <a class="logo-wrap" href="{rel(lang, lang, 'index', page)}"><img src="{up}logo_horizontal_transparent.png" alt="K&amp;2P" width="75" height="24"></a>
      <nav aria-label="Footer">{nav}<a href="{MP_BASE[lang]}" target="_blank" rel="noopener">{esc(c['footer_moripay'])} ↗</a></nav>
    </div>
    <nav class="legal" aria-label="Legal">{legal}</nav>
    <div class="biz"><div>{biz}</div><div>{biz2}<span>{esc(x['email_label'])}: <a href="mailto:{SUPPORT_EMAIL}">{SUPPORT_EMAIL}</a></span></div></div>
    <p class="copy">{esc(c['copyright'])}</p>
  </div>
</footer>
<script>
  (function () {{
    var b = document.querySelector('.menu-toggle'), n = document.getElementById('site-nav');
    if (!b || !n) return;
    b.addEventListener('click', function () {{
      var open = n.classList.toggle('open');
      b.setAttribute('aria-expanded', open ? 'true' : 'false');
    }});
  }})();
</script>
</body>
</html>
"""


def section_head(eyebrow, h2, p=None, center=False):
    cls = "section-head center" if center else "section-head"
    ptag = f"<p>{p}</p>" if p else ""
    return f'<div class="{cls}"><span class="eyebrow">{eyebrow}</span><h2>{h2}</h2>{ptag}</div>'


def checklist(items):
    return '<ul class="checklist">' + "".join(f"<li>{icon('check_circle')}<span>{i}</span></li>" for i in items) + "</ul>"


def feature_list(items):
    return '<ul class="feature-list">' + "".join(
        f'<li><span class="fi">{icon(ic)}</span><div><h3>{t}</h3><p>{d}</p></div></li>' for ic, t, d in items
    ) + "</ul>"


def brand_panel(up, sub, tiles, note=None):
    tiles_html = "".join(f'<div class="bp-tile">{icon(ic)}{t}</div>' for ic, t in tiles)
    note_html = f'<p class="bp-note">{note}</p>' if note else ""
    return f"""<div class="brand-panel">
  <div class="bp-top"><div><div class="bp-title">MoriPay</div><div class="bp-sub">{sub}</div></div><span class="pill">AVAILABLE IN KOREA</span></div>
  <div class="bp-card"><img src="{up}moripay_card.png" alt="MoriPay card" width="200" height="318"></div>
  <div class="bp-tiles">{tiles_html}</div>{note_html}
</div>"""


def cta_band(h2, p, buttons):
    btns = "".join(buttons)
    return f'<section class="section"><div class="container"><div class="cta-band"><div><h2>{h2}</h2><p>{p}</p></div><div class="actions">{btns}</div></div></div></section>'


def contact_section(lang):
    x = EXTRA[lang]
    return f"""<section class="section" id="contact">
  <div class="container">
    {section_head(x['contact_eyebrow'], x['contact_h2'], x['contact_p'], center=True)}
    <div class="grid grid-2 contact">
      <article class="card"><div class="card-icon">{icon('chat')}</div><h3>{x['line_t']}</h3><p>{x['line_d']}</p>
        <div class="hero-actions"><a class="btn btn-primary" href="{LINE_URL}" target="_blank" rel="noopener">{x['line_btn']} {icon('arrow_outward')}</a></div></article>
      <article class="card"><div class="card-icon">{icon('mail')}</div><h3>{x['mail_t']}</h3><p>{x['mail_d']}</p>
        <p class="mail"><a class="link" href="mailto:{SUPPORT_EMAIL}">{SUPPORT_EMAIL}</a></p>
        <div class="hero-actions"><a class="btn btn-secondary" href="{MP_BASE[lang]}/contact" target="_blank" rel="noopener">{x['mail_btn']} {icon('arrow_outward')}</a></div></article>
    </div>
  </div>
</section>"""


def btn_ext(lang, label, cls="btn-light"):
    return f'<a class="btn {cls}" href="{MP_BASE[lang]}" target="_blank" rel="noopener">{label} {icon("arrow_outward")}</a>'


# ───────────────────────────────────────────────── pages

def build_index(lang):
    t = HOME[lang]
    up = "../" if LANG_DIR[lang] else ""
    chips = "".join(
        f'<div class="chip chip-{i+1}">{icon(ic)}<div>{a}<small>{b}</small></div></div>'
        for i, (ic, a, b) in enumerate(t["chips"])
    )
    values = "".join(
        f'<article class="card"><div class="card-icon">{icon(ic)}</div><h3>{h}</h3><p>{p}</p></article>'
        for ic, h, p in t["values"]
    )
    badge = f'<span class="badge">{t["soon"]}</span>'
    eco = "".join(
        f'<article class="card{" soon" if soon else ""}">{badge if soon else ""}'
        f'<div class="card-icon">{icon(ic)}</div><h3>{h}</h3><p>{p}</p><span class="tag">{icon("schedule" if soon else "check")}{tag}</span></article>'
        for ic, h, p, tag, soon in t["eco"]
    )
    body = f"""
<section class="hero">
  <div class="container hero-grid">
    <div>
      <span class="eyebrow">{t['eyebrow']}</span>
      <h1>{t['h1']}</h1>
      <p class="lead">{t['lead']}</p>
      <div class="hero-actions">
        <a class="btn btn-primary" href="{rel(lang, lang, 'guide')}">{t['btn1']} {icon('arrow_forward')}</a>
        <a class="btn btn-secondary" href="{rel(lang, lang, 'about')}">{t['btn2']}</a>
      </div>
      <p class="app-note">{icon('translate')}{EXTRA[lang]['app_note']}</p>
    </div>
    <div class="hero-visual">
      <div class="card-stage">
        <img class="card-img" src="{up}moripay_card.png" alt="MoriPay card" width="320" height="508">
        {chips}
      </div>
    </div>
  </div>
</section>
<section class="section section-alt">
  <div class="container">
    {section_head(t['values_eyebrow'], t['values_h2'], t['values_p'], center=True)}
    <div class="grid grid-3">{values}</div>
  </div>
</section>
<section class="section">
  <div class="container split">
    <div>
      {section_head(t['flag_eyebrow'], t['flag_h2'], t['flag_p'])}
      {feature_list(t['flag_features'])}
    </div>
    {brand_panel(up, 'Inbound Traveler Wallet', t['panel_tiles'], t['panel_note'])}
  </div>
</section>
<section class="section section-alt">
  <div class="container">
    {section_head(t['eco_eyebrow'], t['eco_h2'], t['eco_p'], center=True)}
    <div class="grid grid-4">{eco}</div>
  </div>
</section>
{cta_band(t['cta_h2'], t['cta_p'], [btn_ext(lang, t['cta_btn1']), f'<a class="btn btn-ghost-light" href="{rel(lang, lang, "services")}">{t["cta_btn2"]}</a>'])}
"""
    return t, body


def build_services(lang):
    t = SERVICES[lang]
    up = "../" if LANG_DIR[lang] else ""
    eco = "".join(
        f'<article class="card"><div class="card-icon">{icon(ic)}</div><span class="tag tag-top">{tag}</span>'
        f'<h3 class="h3-tight">{h}</h3><p>{p}</p>{checklist(items)}</article>'
        for ic, tag, h, p, items in t["eco"]
    )
    body = f"""
<section class="page-hero">
  <div class="container">
    <span class="eyebrow">{t['eyebrow']}</span>
    <h1>{t['h1']}</h1>
    <p class="lead">{t['lead']}</p>
  </div>
</section>
<section class="section section-alt">
  <div class="container split reverse">
    <div>
      {section_head(t['mp_eyebrow'], t['mp_h2'], t['mp_p'])}
      {feature_list(t['mp_features'])}
    </div>
    {brand_panel(up, t['panel_sub'], t['panel_tiles'])}
  </div>
</section>
<section class="section">
  <div class="container">
    {section_head(t['eco_eyebrow'], t['eco_h2'], t['eco_p'], center=True)}
    <div class="grid grid-2">{eco}</div>
  </div>
</section>
{cta_band(f'<span class="cta-eyebrow">{t["cta_eyebrow"]}</span>' + t['cta_h2'], t['cta_p'], [f'<a class="btn btn-light" href="{rel(lang, lang, "guide")}">{t["cta_btn"]} {icon("arrow_forward")}</a>'])}
"""
    return t, body


def build_guide(lang):
    t = GUIDE[lang]
    steps = "".join(
        f'<article class="card step"><div><span class="num">0{i+1}</span><span class="when">{when}</span></div>'
        f'<h3>{h}</h3><p>{p}</p><span class="tag">{icon(ic)}{tag}</span></article>'
        for i, (when, h, p, ic, tag) in enumerate(t["steps"])
    )
    tips = "".join(
        f'<article class="card"><div class="card-icon">{icon(ic)}</div><h3>{h}</h3><p>{p}</p>{checklist(items)}</article>'
        for ic, h, p, items in t["tips"]
    )
    chev = icon("expand_more").replace('class="icon"', 'class="icon chev"')
    faq = "".join(
        f'<details{" open" if i == 0 else ""}><summary><span class="q">Q.</span><span>{q}</span>{chev}</summary><div class="a">{a}</div></details>'
        for i, (q, a) in enumerate(t["faq"])
    )
    body = f"""
<section class="page-hero">
  <div class="container">
    <span class="eyebrow">{t['eyebrow']}</span>
    <h1>{t['h1']}</h1>
    <p class="lead">{t['lead']}</p>
  </div>
</section>
<section class="section section-alt">
  <div class="container">
    {section_head(t['steps_eyebrow'], t['steps_h2'], t['steps_p'])}
    <div class="grid grid-4 steps">{steps}</div>
  </div>
</section>
<section class="section">
  <div class="container">
    {section_head(t['tips_eyebrow'], t['tips_h2'], t['tips_p'])}
    <div class="grid grid-3">{tips}</div>
  </div>
</section>
<section class="section section-alt" id="faq">
  <div class="container">
    {section_head(t['faq_eyebrow'], t['faq_h2'], t['faq_p'], center=True)}
    <div class="faq">{faq}</div>
  </div>
</section>
{contact_section(lang)}
{cta_band(t['cta_h2'], t['cta_p'], [btn_ext(lang, t['cta_btn1']), f'<a class="btn btn-ghost-light" href="{rel(lang, lang, "services")}">{t["cta_btn2"]}</a>'])}
"""
    return t, body


def build_about(lang):
    t = ABOUT[lang]
    up = "../" if LANG_DIR[lang] else ""
    cc = "".join(
        f'<article class="card"><div class="card-icon">{icon(ic)}</div><h3>{h}</h3><p>{p}</p></article>'
        for ic, h, p in t["cc"]
    )
    rows = "".join(f"<tr><th scope=\"row\">{k}</th><td>{v}</td></tr>" for k, v in t["info"])
    body = f"""
<section class="page-hero">
  <div class="container">
    <span class="eyebrow">{t['eyebrow']}</span>
    <h1>{t['h1']}</h1>
    <p class="lead">{t['lead']}</p>
  </div>
</section>
<section class="section section-alt">
  <div class="container">
    {section_head(t['mv_eyebrow'], t['mv_h2'])}
    <div class="mv">
      <article class="card"><span class="label">Mission</span><p>{t['mission']}</p></article>
      <article class="card"><span class="label">Vision</span><p>{t['vision']}</p></article>
    </div>
  </div>
</section>
<section class="section">
  <div class="container">
    {section_head(t['cc_eyebrow'], t['cc_h2'])}
    <div class="grid grid-2">{cc}</div>
  </div>
</section>
<section class="section section-alt">
  <div class="container split">
    <div>
      {section_head(t['pr_eyebrow'], t['pr_h2'], t['pr_p'])}
      {checklist(t['pr_list'])}
      <div class="hero-actions"><a class="btn btn-primary" href="{rel(lang, lang, 'services')}">{t['pr_btn']} {icon('arrow_forward')}</a></div>
    </div>
    {brand_panel(up, 'Your Travel Companion', HOME[lang]['panel_tiles'])}
  </div>
</section>
<section class="section">
  <div class="container">
    <span class="eyebrow">{t['ceo_eyebrow']}</span>
    <div class="ceo">
      <div class="avatar" aria-hidden="true">{t['ceo_initial']}</div>
      <div>
        <blockquote>{t['ceo_quote']}</blockquote>
        <p class="who"><strong>{t['ceo_name']}</strong> · {t['ceo_role']}</p>
      </div>
    </div>
  </div>
</section>
<section class="section section-alt">
  <div class="container">
    {section_head(t['info_eyebrow'], t['info_h2'])}
    <table class="info-table"><tbody>{rows}</tbody></table>
  </div>
</section>
{contact_section(lang)}
"""
    return t, body


# microCMS bodies repeat the document title as their first <h1>; the page header already shows it
LEADING_H1 = re.compile(r"^\s*<h1\b[^>]*>.*?</h1>", re.S | re.I)


def build_legal(lang, slug):
    d = LEGAL[(slug, lang)]
    ui = LEGAL_UI[lang]
    page = "legal/" + slug
    meta = []
    if d.get("version"):
        meta.append(f'{ui["version"]} {esc(d["version"])}')
    date = (d.get("revisedAt") or d.get("publishedAt") or "")[:10]
    if date:
        meta.append(f'{ui["updated"]} <time datetime="{date}">{date}</time>')
    others = "".join(
        f'<a href="{rel(lang, lang, "legal/" + s2, page)}">{esc(doc["label"][lang])}</a>'
        for s2, doc in LEGAL_DOCS.items() if s2 != slug and (s2, lang) in LEGAL
    )
    others_html = f'<nav class="legal-others" aria-label="{esc(ui["others"])}"><span>{esc(ui["others"])}</span>{others}</nav>' if others else ""
    body = f"""
<section class="page-hero page-hero-legal">
  <div class="container">
    <span class="eyebrow">{esc(ui['eyebrow'])}</span>
    <h1>{esc(d['title'].strip())}</h1>
    <p class="legal-meta">{' · '.join(meta)}</p>
  </div>
</section>
<section class="section section-legal">
  <div class="container">
    <article class="legal-body">{clean_html(LEADING_H1.sub("", d['body'], count=1))}</article>
    {others_html}
  </div>
</section>
"""
    title = f"{d['title'].strip()} | {'케이앤투피 K&2P' if lang == 'ko' else 'K&2P'}"
    return title, ui["desc"].format(title=d["title"].strip()), body


def legal_langs(slug):
    return [l for l in LANGS if (slug, l) in LEGAL]


BUILDERS = {"index": build_index, "services": build_services, "guide": build_guide, "about": build_about}


def write_extras():
    """Write robots.txt, sitemap.xml and llms.txt; return the 404 page HTML."""
    with open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")
    urls = []
    for lang in LANGS:
        for page in PAGES:
            alts = "".join(
                f'\n    <xhtml:link rel="alternate" hreflang="{l}" href="{page_url(l, page)}"/>' for l in LANGS
            ) + f'\n    <xhtml:link rel="alternate" hreflang="x-default" href="{page_url("ko", page)}"/>'
            urls.append(f"  <url>\n    <loc>{page_url(lang, page)}</loc>{alts}\n  </url>")
    for slug in LEGAL_DOCS:
        langs = legal_langs(slug)
        page = "legal/" + slug
        for lang in langs:
            alts = "".join(f'\n    <xhtml:link rel="alternate" hreflang="{l}" href="{page_url(l, page)}"/>' for l in langs)
            alts += f'\n    <xhtml:link rel="alternate" hreflang="x-default" href="{page_url("ko" if "ko" in langs else langs[0], page)}"/>'
            urls.append(f"  <url>\n    <loc>{page_url(lang, page)}</loc>{alts}\n  </url>")
    with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n'
                '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
                + "\n".join(urls) + "\n</urlset>\n")
    llms = [
        "# K&2P (케이앤투피)",
        "",
        "> K&2P Co., Ltd. is a Seoul-based travel tech company. It operates MoriPay, an all-in-one prepaid travel card",
        "> for international visitors to Korea: mobile top-up in foreign currency, payments at Shinhan Card merchants",
        "> nationwide, and EZL public transit, plus Korea eSIM, travel insurance and airport pickup in the app.",
        "",
        "## Pages",
    ]
    for lang, label in (("ko", "Korean"), ("en", "English"), ("ja", "Japanese")):
        for page in PAGES:
            title = BUILDERS[page](lang)[0]["title"]
            llms.append(f"- [{title}]({page_url(lang, page)}) ({label})")
    llms += ["", "## Related", f"- [MoriPay official site]({MORIPAY})", ""]
    with open(os.path.join(ROOT, "llms.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(llms))
    # 404 page (GitHub Pages serves /404.html); absolute asset paths so it works at any depth
    body404 = """
<section class="page-hero"><div class="container">
  <span class="eyebrow">404</span>
  <h1>페이지를 찾을 수 없습니다<br><span class="h1-sub">Page not found · ページが見つかりません</span></h1>
  <div class="hero-actions">
    <a class="btn btn-primary" href="/">홈으로</a>
    <a class="btn btn-secondary" href="/en/">English</a>
    <a class="btn btn-secondary" href="/ja/">日本語</a>
  </div>
</div></section>
"""
    doc = head("ko", "index", "404 | K&2P", "페이지를 찾을 수 없습니다.") + header("ko", "index") + body404 + footer("ko")
    doc = doc.replace('<link rel="canonical" href="https://kn2p.co.kr/">', '<meta name="robots" content="noindex">')
    doc = "\n".join(l for l in doc.split("\n") if 'hreflang=' not in l or 'lang-switch' in l)
    for a in ('href="assets/', 'src="assets/', 'href="logo_', 'src="logo_', 'href="index.html', 'href="services.html', 'href="guide.html', 'href="about.html', 'href="en/', 'href="ja/', 'href="legal/'):
        doc = doc.replace(a, a.replace('="', '="/'))
    return doc


def write(path, doc):
    with open(path, "w", encoding="utf-8") as f:
        f.write(doc.replace("__ICON_NAMES__", ",".join(sorted(ICONS))))


def main():
    docs = {}
    for lang in LANGS:
        outdir = os.path.join(ROOT, LANG_DIR[lang])
        os.makedirs(outdir, exist_ok=True)
        for page in PAGES:
            t, body = BUILDERS[page](lang)
            docs[os.path.join(outdir, page + ".html")] = head(lang, page, t["title"], t["desc"]) + header(lang, page) + body + footer(lang)
    for (slug, lang) in sorted(LEGAL):
        page = "legal/" + slug
        langs = legal_langs(slug)
        title, desc, body = build_legal(lang, slug)
        outdir = os.path.join(ROOT, LANG_DIR[lang], "legal")
        os.makedirs(outdir, exist_ok=True)
        docs[os.path.join(outdir, slug + ".html")] = head(lang, page, title, desc, langs) + header(lang, page, langs) + body + footer(lang, page)
    docs[os.path.join(ROOT, "404.html")] = write_extras()
    # icons are collected while rendering, so files are written only after every page is built
    for path, doc in docs.items():
        write(path, doc)
    print(f"built {len(docs) - 1 - len(LEGAL)} pages + {len(LEGAL)} legal pages + 404.html, robots.txt, sitemap.xml, llms.txt")


if __name__ == "__main__":
    main()
