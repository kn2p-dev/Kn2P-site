#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate the static K&2P site in ko (root), en (/en/) and ja (/ja/).

    python3 _src/build.py

No dependencies beyond the Python 3 standard library. Copy lives in
_src/content.py; shared styles in assets/css/. Output HTML files are
committed so GitHub Pages can serve them without a build step.
"""
import html
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from content import ABOUT, COMMON, GUIDE, HOME, LANGS, SERVICES  # noqa: E402

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


def rel(lang, target_lang, page):
    """Relative link from a page in `lang` to `page` in `target_lang`."""
    up = "../" if LANG_DIR[lang] else ""
    file = "index.html" if page == "index" else page + ".html"
    return up + LANG_DIR[target_lang] + file


def icon(name):
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


def jsonld(lang, page, title, desc):
    import json
    graph = [ORG]
    if page == "index":
        graph.append({
            "@type": "WebSite",
            "@id": SITE + "/#website",
            "url": SITE + "/",
            "name": "K&2P",
            "inLanguage": ["ko", "en", "ja"],
            "publisher": {"@id": SITE + "/#organization"},
        })
    graph.append({
        "@type": "AboutPage" if page == "about" else "WebPage",
        "@id": page_url(lang, page) + "#webpage",
        "url": page_url(lang, page),
        "name": title,
        "description": desc,
        "inLanguage": lang,
        "isPartOf": {"@id": SITE + "/#website"},
        "about": {"@id": SITE + "/#organization"},
    })
    data = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False)
    return f'<script type="application/ld+json">{data}</script>'


def head(lang, page, title, desc):
    c = COMMON[lang]
    up = "../" if LANG_DIR[lang] else ""
    alternates = "\n".join(
        f'<link rel="alternate" hreflang="{l}" href="{page_url(l, page)}">' for l in LANGS
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
<link rel="alternate" hreflang="x-default" href="{page_url('ko', page)}">
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
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@24,400,0,0&amp;display=block">
<link rel="stylesheet" href="{up}assets/css/astryx-reset.css">
<link rel="stylesheet" href="{up}assets/css/astryx-tokens.css">
<link rel="stylesheet" href="{up}assets/css/kn2p-theme.css">
<link rel="stylesheet" href="{up}assets/css/site.css">
</head>
<body>
"""


def header(lang, page):
    c = COMMON[lang]
    up = "../" if LANG_DIR[lang] else ""
    nav = "".join(
        f'<a href="{rel(lang, lang, p)}"{" aria-current=\"page\"" if p == page else ""}>{esc(c["nav"][p])}</a>'
        for p in PAGES
    )
    switch = "".join(
        f'<a href="{rel(lang, l, page)}" hreflang="{l}" lang="{l}" title="{esc(COMMON[l]["lang_label"])}"'
        f'{" aria-current=\"true\"" if l == lang else ""}>{SHORT[l]}</a>'
        for l in LANGS
    )
    return f"""<a class="skip-link" href="#main">{esc(c['skip'])}</a>
<header class="site-header">
  <div class="container">
    <a class="brand" href="{rel(lang, lang, 'index')}"><img src="{up}logo_horizontal_transparent.png" alt="K&amp;2P" width="94" height="30"></a>
    <nav class="nav" id="site-nav" aria-label="Main">{nav}<a class="nav-ext" href="{MORIPAY}" target="_blank" rel="noopener">{esc(c['cta_moripay'])} ↗</a></nav>
    <div class="header-actions">
      <div class="lang-switch" role="group" aria-label="Language">{switch}</div>
      <a class="btn btn-primary btn-sm btn-cta" href="{MORIPAY}" target="_blank" rel="noopener">{esc(c['cta_moripay'])} {icon('arrow_outward')}</a>
      <button class="menu-toggle" type="button" aria-controls="site-nav" aria-expanded="false" aria-label="{esc(c['menu'])}">{icon('menu')}</button>
    </div>
  </div>
</header>
<main id="main">
"""


def footer(lang):
    c = COMMON[lang]
    up = "../" if LANG_DIR[lang] else ""
    nav = "".join(f'<a href="{rel(lang, lang, p)}">{esc(c["nav"][p])}</a>' for p in PAGES)
    biz = "".join(f"<span>{esc(x)}</span>" for x in c["biz"])
    biz2 = "".join(f"<span>{esc(x)}</span>" for x in c["biz2"])
    return f"""</main>
<footer class="site-footer">
  <div class="container">
    <div class="top">
      <a class="logo-wrap" href="{rel(lang, lang, 'index')}"><img src="{up}logo_horizontal_transparent.png" alt="K&amp;2P" width="75" height="24"></a>
      <nav aria-label="Footer">{nav}<a href="{MORIPAY}" target="_blank" rel="noopener">{esc(c['footer_moripay'])} ↗</a></nav>
    </div>
    <div class="biz"><div>{biz}</div><div>{biz2}</div></div>
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


def btn_ext(label, cls="btn-light"):
    return f'<a class="btn {cls}" href="{MORIPAY}" target="_blank" rel="noopener">{label} {icon("arrow_outward")}</a>'


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
    eco = "".join(
        f'<article class="card{" soon" if soon else ""}">{f"<span class=badge>{t["soon"]}</span>" if soon else ""}'
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
{cta_band(t['cta_h2'], t['cta_p'], [btn_ext(t['cta_btn1']), f'<a class="btn btn-ghost-light" href="{rel(lang, lang, "services")}">{t["cta_btn2"]}</a>'])}
"""
    return t, body


def build_services(lang):
    t = SERVICES[lang]
    up = "../" if LANG_DIR[lang] else ""
    eco = "".join(
        f'<article class="card"><div class="card-icon">{icon(ic)}</div><span class="tag" style="margin-top:20px">{tag}</span>'
        f'<h3 style="margin-top:6px">{h}</h3><p>{p}</p>{checklist(items)}</article>'
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
{cta_band(f'<span style="display:block;font-size:.8125rem;letter-spacing:.08em;text-transform:uppercase;opacity:.8;margin-bottom:10px">{t["cta_eyebrow"]}</span>' + t['cta_h2'], t['cta_p'], [f'<a class="btn btn-light" href="{rel(lang, lang, "guide")}">{t["cta_btn"]} {icon("arrow_forward")}</a>'])}
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
    faq = "".join(
        f'<details{" open" if i == 0 else ""}><summary><span class="q">Q.</span><span>{q}</span>{icon("expand_more").replace("class=\"icon\"", "class=\"icon chev\"")}</summary><div class="a">{a}</div></details>'
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
{cta_band(t['cta_h2'], t['cta_p'], [btn_ext(t['cta_btn1']), f'<a class="btn btn-ghost-light" href="{rel(lang, lang, "services")}">{t["cta_btn2"]}</a>'])}
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
    <div class="ceo" style="margin-top:16px">
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
"""
    return t, body


BUILDERS = {"index": build_index, "services": build_services, "guide": build_guide, "about": build_about}



def write_extras():
    with open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")
    urls = []
    for lang in LANGS:
        for page in PAGES:
            alts = "".join(
                f'\n    <xhtml:link rel="alternate" hreflang="{l}" href="{page_url(l, page)}"/>' for l in LANGS
            ) + f'\n    <xhtml:link rel="alternate" hreflang="x-default" href="{page_url("ko", page)}"/>'
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
  <h1>페이지를 찾을 수 없습니다<br><span style="font-size:.5em;font-weight:600;color:var(--color-text-secondary)">Page not found · ページが見つかりません</span></h1>
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
    for a in ('href="assets/', 'src="assets/', 'href="logo_', 'src="logo_', 'href="index.html', 'href="services.html', 'href="guide.html', 'href="about.html', 'href="en/', 'href="ja/'):
        doc = doc.replace(a, a.replace('="', '="/'))
    with open(os.path.join(ROOT, "404.html"), "w", encoding="utf-8") as f:
        f.write(doc)


def main():
    count = 0
    for lang in LANGS:
        outdir = os.path.join(ROOT, LANG_DIR[lang])
        os.makedirs(outdir, exist_ok=True)
        for page in PAGES:
            t, body = BUILDERS[page](lang)
            doc = head(lang, page, t["title"], t["desc"]) + header(lang, page) + body + footer(lang)
            with open(os.path.join(outdir, page + ".html"), "w", encoding="utf-8") as f:
                f.write(doc)
            count += 1
    write_extras()
    print(f"built {count} pages + robots.txt, sitemap.xml, llms.txt, 404.html")


if __name__ == "__main__":
    main()
