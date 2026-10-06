"""Static site builder for the Sustainable Olympiad website.

Usage:   cd sustainable-olympiad/_build && python3 build.py
Output:  the .html pages, assets/js/config.js, assets/data/search-index.json,
         images (make_images.py) and PDFs/.ics (make_pdfs.py, needs reportlab).

The folder starts with an underscore, so GitHub Pages (Jekyll) does not publish it.
"""
import html
import json
import os
import re
from datetime import date

import make_images
import make_paper_pdfs
import make_pdfs
from content import (CATEGORIES, DIVISIONS, DOWNLOADS, EVENT, FAQ, GALLERY, GUIDELINES,
                     HISTORY, JUDGING, NEWS, RULES, SCHOOLS, SPONSORS, STATS, TIMELINE, TIPS)
from icons import icon
from papers import PAPERS, part_b_marks, total_marks

# ---------------------------------------------------------------------------
# Site settings: edit these, then run build.py
# ---------------------------------------------------------------------------
SITE = {
    "url": "https://jaorrrr.github.io/sustainable-olympiad/",
    "contact_email": "info@sustainableolympiad.org",
    # Paste a form-handling endpoint (e.g. https://formspree.io/f/xxxxxx) to have
    # forms submitted directly. When empty, forms open the visitor's email app
    # with the completed message addressed to contact_email.
    "form_endpoint": "",
    "address": ["Sustainable Olympiad Secretariat", "Rua da Ribeira Verde 21", "1200-000 Lisbon, Portugal"],
    "social": [
        ("Instagram", "https://www.instagram.com/sustainableolympiad", "instagram"),
        ("X (Twitter)", "https://x.com/sustainolympiad", "x"),
        ("LinkedIn", "https://www.linkedin.com/company/sustainable-olympiad", "linkedin"),
        ("YouTube", "https://www.youtube.com/@sustainableolympiad", "youtube"),
        ("Facebook", "https://www.facebook.com/sustainableolympiad", "facebook"),
    ],
}

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NAV = [("index", "Home"), ("about", "About"), ("challenges", "Challenges"), ("schedule", "Schedule"),
       ("rules", "Rules"), ("past-papers", "Past Papers"), ("partners", "Partners"), ("news", "News"), ("faq", "FAQ"),
       ("contact", "Contact")]
e = html.escape


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def fmt_date(d, year=True):
    d = date.fromisoformat(d)
    return d.strftime("%-d %B %Y" if year else "%-d %B")


def date_range(t):
    return make_pdfs.fmt_range(t)


def time_el(t):
    """<time> element(s) for a timeline item."""
    if not t.get("end"):
        return f'<time datetime="{t["start"]}">{fmt_date(t["start"])}</time>'
    return f'<time datetime="{t["start"]}">{date_range(t)}</time>'


def b2strong(s):
    return s.replace("<b>", "<strong>").replace("</b>", "</strong>")


def file_size(name):
    kb = os.path.getsize(os.path.join(ROOT, "assets", "docs", name)) / 1024
    return f"{max(1, round(kb))} KB"


def banner(title, lead, crumb=None, parent=None):
    crumb = crumb or title
    mid = f'<li><a href="{parent[0]}">{e(parent[1])}</a></li>' if parent else ""
    return f"""
<div class="page-banner">
  <div class="container">
    <nav aria-label="Breadcrumb" class="breadcrumb">
      <ol><li><a href="index.html">Home</a></li>{mid}<li><a href="#main" aria-current="page">{e(crumb)}</a></li></ol>
    </nav>
    <h1>{title}</h1>
    <p class="lead">{lead}</p>
  </div>
</div>"""


def section(id_, title, body, cls="", intro=""):
    intro = f'<p class="section-intro">{intro}</p>' if intro else ""
    return f"""
<section class="section {cls}" aria-labelledby="{id_}">
  <div class="container">
    <h2 id="{id_}">{title}</h2>{intro}
    {body}
  </div>
</section>"""


def btn(href, label, kind="primary", ico=None, extra=""):
    i = icon(ico) if ico else ""
    return f'<a class="btn btn-{kind}" href="{href}"{extra}>{label}{i}</a>'


def field(id_, label, type_="text", required=True, autocomplete=None, hint=None,
          attrs="", name=None, error=None, options=None, rows=None):
    """Accessible form field with label, hint and error container."""
    name = name or id_
    req = ' <span class="req">(required)</span>' if required else ' <span class="opt">(optional)</span>'
    described = []
    hint_html = ""
    if hint:
        hint_html = f'<p class="hint" id="{id_}-hint">{hint}</p>'
        described.append(f"{id_}-hint")
    described.append(f"{id_}-error")
    common = (f'id="{id_}" name="{name}" aria-describedby="{" ".join(described)}"'
              + (" required" if required else "")
              + (f' autocomplete="{autocomplete}"' if autocomplete else "")
              + (f' data-error-required="{e(error)}"' if error else "")
              + (" " + attrs if attrs else ""))
    if type_ == "select":
        opts = '<option value="">Select an option</option>' + "".join(
            f'<option value="{e(v)}">{e(t)}</option>' for v, t in options)
        control = f"<select {common}>{opts}</select>"
    elif type_ == "textarea":
        control = f'<textarea {common} rows="{rows or 5}"></textarea>'
    elif type_ == "checkbox":
        return f"""
<div class="field field-check">
  <input type="checkbox" {common} value="yes">
  <label for="{id_}">{label}{req}</label>
  {hint_html}<p class="field-error" id="{id_}-error"></p>
</div>"""
    else:
        control = f'<input type="{type_}" {common}>'
    return f"""
<div class="field">
  <label for="{id_}">{label}{req}</label>
  {hint_html}<p class="field-error" id="{id_}-error"></p>
  {control}
</div>"""


def error_summary(prefix):
    return f"""
<div class="error-summary" id="{prefix}-errors" role="alert" tabindex="-1" hidden>
  <h2 class="h3" id="{prefix}-errors-title">There is a problem with your submission</h2>
  <ul></ul>
</div>"""


def success_panel(prefix, title, text):
    return f"""
<div class="form-success" id="{prefix}-success" tabindex="-1" hidden>
  {icon("check")}
  <div><h2 class="h3">{title}</h2><p data-success-text>{text}</p></div>
</div>"""


def form_attrs(kind, subject):
    return (f'class="so-form" data-form="{kind}" data-subject="{e(subject)}" '
            f'action="mailto:{SITE["contact_email"]}?subject={e(subject)}" method="post" enctype="text/plain"')


# ---------------------------------------------------------------------------
# Layout
# ---------------------------------------------------------------------------
def head(page, title, description):
    full = title if page == "index" else f"{title} | Sustainable Olympiad"
    url = SITE["url"] + ("" if page == "index" else f"{page}.html")
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(full)}</title>
<meta name="description" content="{e(description)}">
<meta name="theme-color" content="#0a6b3d">
<link rel="canonical" href="{url}">
<link rel="icon" href="assets/img/favicon-64.png" type="image/png" sizes="64x64">
<link rel="apple-touch-icon" href="assets/img/apple-touch-icon.png">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Sustainable Olympiad">
<meta property="og:title" content="{e(full)}">
<meta property="og:description" content="{e(description)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE['url']}assets/img/logo.png">
<meta property="og:image:alt" content="Sustainable Olympiad logo">
<meta name="twitter:card" content="summary">
<script src="assets/js/a11y-init.js"></script>
<link rel="stylesheet" href="assets/css/main.css">
</head>"""


LOGO = ('<picture><source srcset="assets/img/logo-mark.webp" type="image/webp">'
        '<img class="brand-mark" src="assets/img/logo-mark.png" alt="" width="48" height="48"></picture>')


def header(page):
    items = []
    nav_key = "past-papers" if page.startswith("paper-") else page
    for key, label in NAV:
        cur = ' aria-current="page"' if key == nav_key else ""
        items.append(f'<li><a href="{key}.html"{cur}>{label}</a></li>')
    items.append('<li class="nav-register"><a class="btn btn-primary" href="register.html"'
                 + (' aria-current="page"' if page == "register" else "") + '>Register Now</a></li>')
    return f"""
<body data-page="{page}">
<a class="skip-link" href="#main">Skip to main content</a>
<div class="utility-bar">
  <div class="container utility-inner">
    <form class="site-search" role="search" aria-label="Site" action="search.html" method="get">
      <label for="site-search-q" class="visually-hidden">Search the site</label>
      <input type="search" id="site-search-q" name="q" placeholder="Search the site" autocomplete="off">
      <button type="submit" class="icon-btn">{icon("search")}<span class="visually-hidden">Search</span></button>
    </form>
    <button type="button" class="a11y-toggle" aria-expanded="false" aria-controls="a11y-panel">
      {icon("a11y")}<span>Accessibility</span>
    </button>
  </div>
</div>
<section id="a11y-panel" class="a11y-panel" aria-labelledby="a11y-panel-title" hidden>
  <div class="container">
    <h2 class="h3" id="a11y-panel-title">Accessibility options</h2>
    <div class="a11y-controls" role="group" aria-labelledby="a11y-panel-title">
      <div class="a11y-group" role="group" aria-labelledby="a11y-size-label">
        <span id="a11y-size-label" class="a11y-label">{icon("text")} Text size</span>
        <div class="a11y-buttons">
          <button type="button" data-a11y="font-down" aria-label="Decrease text size">A&minus;</button>
          <button type="button" data-a11y="font-reset" aria-label="Reset text size">A</button>
          <button type="button" data-a11y="font-up" aria-label="Increase text size">A+</button>
        </div>
        <output class="a11y-status" id="a11y-font-status" aria-live="polite">100%</output>
      </div>
      <button type="button" class="a11y-switch" data-a11y="dark" aria-pressed="false">{icon("moon")}<span>Dark mode</span></button>
      <button type="button" class="a11y-switch" data-a11y="contrast" aria-pressed="false">{icon("contrast")}<span>High contrast</span></button>
      <button type="button" class="a11y-switch" data-a11y="spacing" aria-pressed="false">{icon("spacing")}<span>Text spacing</span></button>
      <button type="button" class="a11y-switch" data-a11y="links" aria-pressed="false">{icon("link")}<span>Highlight links</span></button>
      <button type="button" class="a11y-reset" data-a11y="reset">Reset all</button>
    </div>
    <p class="a11y-note">Your choices are saved on this device. <a href="accessibility.html">Read our accessibility statement</a>.</p>
  </div>
</section>
<header class="site-header">
  <div class="container header-inner">
    <a class="brand" href="index.html"{' aria-current="page"' if page == "index" else ""}>
      {LOGO}<span class="brand-text">Sustainable <span>Olympiad</span></span>
    </a>
    <button type="button" class="nav-toggle" aria-expanded="false" aria-controls="primary-nav">
      <span class="nav-toggle-open">{icon("menu")}</span><span class="nav-toggle-close">{icon("close")}</span>
      <span class="nav-toggle-label">Menu</span>
    </button>
    <nav id="primary-nav" class="primary-nav" aria-label="Main">
      <ul>{"".join(items)}</ul>
    </nav>
  </div>
</header>
<main id="main" tabindex="-1">"""


def footer():
    explore = "".join(f'<li><a href="{k}.html">{l}</a></li>' for k, l in NAV[1:])
    explore += '<li><a href="register.html">Register</a></li>'
    downloads = "".join(
        f'<li><a href="assets/docs/{f}" download>{t} <span class="meta">(PDF, {file_size(f)})</span></a></li>'
        for _, t, f, _, _ in DOWNLOADS)
    social = "".join(
        f'<li><a href="{u}" rel="noopener" target="_blank">{icon(i)}<span class="visually-hidden">'
        f'{n} (opens in a new tab)</span></a></li>' for n, u, i in SITE["social"])
    return f"""
</main>
<footer class="site-footer">
  <div class="container footer-grid">
    <section class="footer-about" aria-labelledby="footer-about-title">
      <h2 id="footer-about-title" class="visually-hidden">About the Sustainable Olympiad</h2>
      <a class="brand brand-footer" href="index.html">{LOGO}<span class="brand-text">Sustainable <span>Olympiad</span></span></a>
      <p>An international competition that empowers students to design real solutions for a sustainable future.</p>
      <h3 class="footer-small-title">Follow us</h3>
      <ul class="social-list">{social}</ul>
    </section>
    <nav aria-labelledby="footer-explore-title">
      <h2 id="footer-explore-title" class="footer-title">Explore</h2>
      <ul class="footer-links">{explore}</ul>
    </nav>
    <section aria-labelledby="footer-res-title">
      <h2 id="footer-res-title" class="footer-title">Resources</h2>
      <ul class="footer-links">{downloads}
        <li><a href="assets/docs/{make_pdfs.ICS_NAME}" download>Event calendar <span class="meta">(.ics)</span></a></li>
        <li><a href="past-papers.html">Past papers and solutions</a></li>
      </ul>
    </section>
    <section aria-labelledby="newsletter-title" class="footer-newsletter">
      <h2 id="newsletter-title" class="footer-title">Newsletter</h2>
      <p>Monthly updates, deadlines and project ideas. No spam, and you can unsubscribe at any time.</p>
      <form {form_attrs("newsletter", "Newsletter subscription")} novalidate>
        <div class="field">
          <label for="newsletter-email">Email address</label>
          <p class="field-error" id="newsletter-email-error"></p>
          <div class="inline-field">
            <input type="email" id="newsletter-email" name="email" autocomplete="email" required
              aria-describedby="newsletter-email-error" data-error-required="Enter your email address to subscribe">
            <button type="submit" class="btn btn-light">Subscribe</button>
          </div>
        </div>
        <p class="form-status" role="status" aria-live="polite"></p>
      </form>
    </section>
  </div>
  <div class="footer-bottom">
    <div class="container footer-bottom-inner">
      <p>&copy; 2026 Sustainable Olympiad. All rights reserved.</p>
      <ul>
        <li><a href="accessibility.html">Accessibility statement</a></li>
        <li><a href="contact.html#privacy">Privacy</a></li>
        <li><a href="#main">Back to top</a></li>
      </ul>
    </div>
  </div>
</footer>"""


def scripts(extra=()):
    tags = ['<script src="assets/js/config.js"></script>', '<script src="assets/js/main.js" defer></script>']
    tags += [f'<script src="assets/js/{s}" defer></script>' for s in extra]
    return "\n".join(tags) + "\n</body>\n</html>\n"


# ---------------------------------------------------------------------------
# Reusable blocks
# ---------------------------------------------------------------------------
def countdown(heading_id="countdown-title", tag="h2"):
    units = "".join(
        f'<div class="cd-unit"><span class="cd-num" data-unit="{u}">--</span><span class="cd-label">{u}</span></div>'
        for u in ("days", "hours", "minutes", "seconds"))
    return f"""
<section class="countdown" aria-labelledby="{heading_id}">
  <{tag} id="{heading_id}" class="countdown-title">Countdown to the Global Finals</{tag}>
  <p class="countdown-date">{icon("calendar")}<time datetime="{EVENT['finals_iso']}">{EVENT['finals_label']}</time></p>
  <div class="cd-grid" role="timer" aria-live="off" aria-atomic="true" data-countdown="{EVENT['finals_iso']}">{units}</div>
  <p class="cd-done" hidden>The Global Finals have started. Follow the live stream on our social channels.</p>
  <button type="button" class="link-btn cd-toggle" data-countdown-toggle hidden>Pause countdown</button>
</section>"""


def category_cards(link_prefix="challenges.html#"):
    cards = []
    for c in CATEGORIES:
        cards.append(f"""
<li class="card card-category">
  <span class="card-icon">{icon(c['icon'])}</span>
  <h3><a class="card-link" href="{link_prefix}{c['id']}">{c['name']}</a></h3>
  <p>{c['summary']}</p>
</li>""")
    return f'<ul class="grid grid-3 card-list" role="list">{"".join(cards)}</ul>'


def downloads_block(show_html_link=True):
    items = []
    for key, title, f, desc, html_link in DOWNLOADS:
        alt = (f'<a href="{html_link}">Read on this page<span class="visually-hidden">: {title}</span></a>'
               if show_html_link else "")
        items.append(f"""
<li class="card download-card">
  <span class="card-icon">{icon("file")}</span>
  <div>
    <h3>{title}</h3>
    <p>{desc}</p>
    <p class="download-actions">
      <a class="btn btn-secondary btn-sm" href="assets/docs/{f}" download>{icon("download")}Download<span class="visually-hidden"> {title}</span> <span class="meta">(PDF, {file_size(f)})</span></a>
      {alt}
    </p>
  </div>
</li>""")
    return f'<ul class="grid grid-3 card-list" role="list">{"".join(items)}</ul>'


def partner_logos(compact=False):
    out = []
    for tier, items in SPONSORS.items():
        if compact and tier == "Community Partners":
            continue
        for name, key, _ in items:
            out.append(f'<li><img src="assets/img/partners/{key}.svg" alt="{e(name)}" width="200" height="56"></li>')
    return f'<ul class="logo-strip" role="list">{"".join(out)}</ul>'


def news_card(n, full=False, heading="h3"):
    body = "".join(f"<p>{p}</p>" for p in (n["body"] if full else n["body"][:1]))
    share = ""
    if full:
        url = SITE["url"] + "news.html#" + n["id"]
        from urllib.parse import quote
        u, t = quote(url, safe=""), quote(n["title"], safe="")
        share = f"""
  <div class="share" role="group" aria-label="Share: {e(n['title'])}">
    <span class="share-label">Share</span>
    <a href="https://x.com/intent/post?url={u}&amp;text={t}" target="_blank" rel="noopener">{icon("x")}<span class="visually-hidden">Share on X (opens in a new tab)</span></a>
    <a href="https://www.linkedin.com/sharing/share-offsite/?url={u}" target="_blank" rel="noopener">{icon("linkedin")}<span class="visually-hidden">Share on LinkedIn (opens in a new tab)</span></a>
    <a href="https://www.facebook.com/sharer/sharer.php?u={u}" target="_blank" rel="noopener">{icon("facebook")}<span class="visually-hidden">Share on Facebook (opens in a new tab)</span></a>
    <a href="mailto:?subject={t}&amp;body={u}">{icon("mail")}<span class="visually-hidden">Share by email</span></a>
    <button type="button" class="copy-link" data-copy="{url}" hidden>{icon("link")}<span class="visually-hidden">Copy link to this article</span></button>
  </div>"""
    title = (f'<a class="card-link" href="news.html#{n["id"]}">{n["title"]}</a>' if not full else n["title"])
    id_attr = f' id="{n["id"]}" tabindex="-1"' if full else ""
    return f"""
<article class="card news-card" data-tag="{e(n['tag'])}"{id_attr} aria-labelledby="{n['id']}-title{'' if full else '-teaser'}">
  <p class="news-meta"><span class="tag">{n['tag']}</span> <time datetime="{n['date']}">{fmt_date(n['date'])}</time></p>
  <{heading} id="{n['id']}-title{'' if full else '-teaser'}">{title}</{heading}>
  {body}{share}
</article>"""


# ---------------------------------------------------------------------------
# Pages
# ---------------------------------------------------------------------------
def page_index():
    stats = "".join(f'<li><span class="stat-num">{n}</span><span class="stat-label">{l}</span></li>' for n, l in STATS)
    key = [t for t in TIMELINE if t["id"] in ("registration-deadline", "round-1", "round-2", "finals")]
    dates = "".join(f"""
<li class="key-date" data-start="{t['start']}" data-end="{t.get('end', t['start'])}">
  <span class="key-date-when">{time_el(t)}</span>
  <span class="key-date-what">{t['title']}</span>
</li>""" for t in key)
    latest = "".join(news_card(n) for n in NEWS[:3])
    hero = f"""
<section class="hero" aria-labelledby="hero-title">
  <div class="hero-bg" aria-hidden="true">
    <svg viewBox="0 0 1200 600" preserveAspectRatio="xMidYMid slice" focusable="false">
      <circle cx="1040" cy="120" r="220" fill="rgba(255,255,255,.06)"/>
      <circle cx="120" cy="560" r="260" fill="rgba(255,255,255,.05)"/>
      <path d="M0 520 Q300 440 600 500 T1200 470 V600 H0Z" fill="rgba(124,194,66,.25)"/>
      <path d="M0 560 Q320 500 640 550 T1200 530 V600 H0Z" fill="rgba(255,255,255,.08)"/>
    </svg>
  </div>
  <div class="container hero-inner">
    <div class="hero-text">
      <p class="eyebrow">{EVENT['edition_number']} edition &middot; {EVENT['finals_dates']} &middot; {EVENT['venue']}</p>
      <h1 id="hero-title">Sustainable Olympiad <span class="hero-year">{EVENT['edition']}</span></h1>
      <p class="hero-tagline">{EVENT['tagline']}</p>
      <p class="hero-lead">The international competition where student teams compete to design real solutions
        for energy, waste, water, climate and nature. Free to enter for students aged 12 to 25.</p>
      <div class="hero-actions">
        {btn("register.html", "Register Now", "accent", "arrow")}
        {btn("challenges.html", "Explore the challenges", "ghost")}
      </div>
      <p class="hero-note">{icon("clock")}<span>Registration closes on <time datetime="{EVENT['registration_deadline_iso']}">{EVENT['registration_deadline']}</time>.</span></p>
    </div>
    <div class="hero-side">{countdown()}</div>
  </div>
</section>"""
    why = f"""
<ul class="grid grid-3 card-list" role="list">
  <li class="card feature"><span class="card-icon">{icon("globe")}</span><h3>Solve real problems</h3>
    <p>Work on challenges that matter in your own school and community, and measure the difference you make.</p></li>
  <li class="card feature"><span class="card-icon">{icon("users")}</span><h3>Learn from experts</h3>
    <p>Get feedback from scientists, engineers and entrepreneurs, and connect with students in more than 60 countries.</p></li>
  <li class="card feature"><span class="card-icon">{icon("trophy")}</span><h3>Win grants and recognition</h3>
    <p>Medals in every category, certificates for all teams, and grants of up to &euro;5,000 to bring winning ideas to life.</p></li>
</ul>"""
    steps = """
<ol class="steps" role="list">
  <li><h3>Register your team</h3><p>Form a team of 2–5 students with a mentor and choose a challenge.</p></li>
  <li><h3>Round 1: Knowledge Challenge</h3><p>Take a 90-minute online quiz on sustainability science from your school.</p></li>
  <li><h3>Round 2: Project Challenge</h3><p>Spend ten days building, testing and documenting a real solution.</p></li>
  <li><h3>Global Finals</h3><p>Present your project to an international jury in Lisbon, in Brazil or online.</p></li>
</ol>"""
    body = hero + f"""
<section class="stats-band" aria-labelledby="stats-title">
  <div class="container">
    <h2 id="stats-title" class="visually-hidden">The Olympiad in numbers</h2>
    <ul class="stats" role="list">{stats}</ul>
  </div>
</section>""" + section("why-title", "Why take part?", why,
                        intro="Teams learn by doing, and leave with skills, friendships and projects that keep making an impact.") \
        + section("challenges-title", "Six challenges, one planet", category_cards()
                  + f'<p class="section-cta">{btn("challenges.html", "See all challenges and briefs", "secondary", "arrow")}</p>',
                  cls="section-tint", intro=f"Every team chooses one category. Each comes with a practical brief for {EVENT['edition']}.") \
        + section("how-title", "How it works", steps) \
        + section("dates-title", "Key dates", f"""
<ul class="key-dates" role="list">{dates}</ul>
<p class="section-cta">{btn("schedule.html", "View the full schedule", "secondary", "arrow")}
  <a class="btn btn-ghost-dark" href="assets/docs/{make_pdfs.ICS_NAME}" download>{icon("calendar")}Add dates to your calendar</a></p>""",
                  cls="section-tint") \
        + section("news-title", "Latest news", f'<div class="grid grid-3">{latest}</div>'
                  + f'<p class="section-cta">{btn("news.html", "All news and photos", "secondary", "arrow")}</p>') \
        + section("resources-title", "Free resources", downloads_block()
                  + f'<p class="section-cta">{btn("past-papers.html", "Practise with past papers", "secondary", "arrow")}</p>',
                  cls="section-tint",
                  intro="Everything you need to prepare, in PDF format. The same content is available as web pages.") \
        + section("partners-title", "Supported by", partner_logos(True)
                  + f'<p class="section-cta"><a href="partners.html">Meet all our partners and participating schools</a></p>') \
        + f"""
<section class="cta-band" aria-labelledby="cta-title">
  <div class="container cta-inner">
    <div>
      <h2 id="cta-title">Ready to make a difference?</h2>
      <p>Registration is free and takes about ten minutes. Gather your team and join students from around the world.</p>
    </div>
    {btn("register.html", "Register Now", "accent", "arrow")}
  </div>
</section>"""
    return body


def page_about():
    goals = [
        ("leaf", "Inspire action", "Turn concern about the environment into practical, measurable projects."),
        ("book", "Build skills", "Develop scientific thinking, creativity, teamwork and communication."),
        ("users", "Connect communities", "Link students, schools, researchers and businesses across borders."),
        ("globe", "Include everyone", "Keep participation free, accessible and open to every school."),
    ]
    goals_html = "".join(f'<li class="card feature"><span class="card-icon">{icon(i)}</span><h3>{t}</h3><p>{d}</p></li>'
                         for i, t, d in goals)
    history = "".join(f'<li><span class="history-year">{y}</span><div><h3>{t}</h3><p>{d}</p></div></li>'
                      for y, t, d in HISTORY)
    stats = "".join(f'<li><span class="stat-num">{n}</span><span class="stat-label">{l}</span></li>' for n, l in STATS)
    return banner("About the Olympiad",
                  "Since 2020, the Sustainable Olympiad has brought students together to compete, collaborate and innovate for a healthier planet.",
                  "About") + section("mission", "Our mission", """
<div class="two-col">
  <div class="prose">
    <p class="big">We believe the people who will live longest with the consequences of today's environmental choices
      deserve the tools, knowledge and platform to shape them.</p>
    <p>The Sustainable Olympiad is a non-profit, international competition for students aged 12 to 25.
      Teams investigate an environmental problem in their own community, design a solution, test it and share
      what they learn, guided by mentors and assessed by experts.</p>
    <p>Unlike traditional olympiads, success is not only about knowing the right answer. It is about
      making a measurable difference and inspiring others to follow.</p>
  </div>
  <aside class="card quote-card" aria-label="Student quote">
    <blockquote><p>&ldquo;We started with a question about our cafeteria bins. We finished with a product that a local
      cooperative now makes every week.&rdquo;</p></blockquote>
    <p class="quote-by">Planet Award winning team, 2025</p>
  </aside>
</div>""") + section("goals", "Our goals", f'<ul class="grid grid-4 card-list" role="list">{goals_html}</ul>',
                     cls="section-tint") + section("values", "Our values", """
<ul class="values-list" role="list">
  <li><strong>Evidence over opinion.</strong> We value honest data, including results that did not go to plan.</li>
  <li><strong>Collaboration over competition.</strong> Teams compete, but every project and every lesson is shared openly.</li>
  <li><strong>Access for all.</strong> No fees, low-cost materials, travel support and full accessibility.</li>
  <li><strong>Practise what we teach.</strong> Our Finals are low-waste, mostly plant-based and carbon-accounted.</li>
</ul>""") + section("history", "Our history", f'<ol class="history" role="list">{history}</ol>', cls="section-tint",
                    intro="From an online experiment during school closures to a global community.") \
        + f"""
<section class="stats-band" aria-labelledby="impact-title">
  <div class="container">
    <h2 id="impact-title" class="stats-heading">Our impact so far</h2>
    <ul class="stats" role="list">{stats}</ul>
  </div>
</section>""" + section("organisers", "Who organises the Olympiad", """
<div class="prose">
  <p>The Olympiad is run by an independent non-profit association of educators and scientists, supported by volunteers
    from universities and partner organisations. An advisory board of teachers, students and accessibility specialists
    reviews the rules and challenges every year.</p>
  <p>Judges are recruited openly and declare any conflicts of interest. Our accounts are published every year after the Finals.</p>
</div>""") + cta_band()


def cta_band(title=f"Join the {EVENT['edition']} Olympiad",
             text=f"Registration is free and open until {EVENT['registration_deadline']}."):
    return f"""
<section class="cta-band" aria-labelledby="cta-title">
  <div class="container cta-inner">
    <div><h2 id="cta-title">{title}</h2><p>{text}</p></div>
    {btn("register.html", "Register Now", "accent", "arrow")}
  </div>
</section>"""


def page_challenges():
    toc = "".join(f'<li><a href="#{c["id"]}">{c["name"]}</a></li>' for c in CATEGORIES)
    divisions = "".join(f"<tr><th scope=\"row\">{d}</th><td>{a}</td></tr>" for d, a in DIVISIONS)
    judging = "".join(f'<tr><th scope="row">{a}</th><td>{b}</td><td>{c}</td></tr>' for a, b, c in JUDGING)
    cats = []
    for i, c in enumerate(CATEGORIES):
        ex = "".join(f"<li>{x}</li>" for x in c["examples"])
        new = ' <span class="tag tag-new">New</span>' if c["id"] == "water-oceans" else ""
        cats.append(f"""
<article class="category" aria-labelledby="{c['id']}">
  <div class="category-head">
    <span class="card-icon card-icon-lg">{icon(c['icon'])}</span>
    <div><h3 id="{c['id']}" tabindex="-1">{c['name']}{new}</h3><p class="category-summary">{c['summary']}</p></div>
  </div>
  <div class="category-body">
    <p>{c['description']}</p>
    <div class="brief"><h4>{EVENT['edition']} challenge brief</h4><p>{c['brief']}</p></div>
    <div class="two-col two-col-tight">
      <div><h4>Example projects</h4><ul>{ex}</ul></div>
      <div><h4>Useful skills</h4><p>{c['skills']}</p>
        <p>{btn(f"register.html?category={c['id']}", f"Register for this challenge<span class='visually-hidden'>: {c['name']}</span>", "secondary btn-sm")}</p></div>
    </div>
  </div>
</article>""")
    return banner("Challenges & Categories",
                  "Six competition areas, each with a real-world brief. Choose the one where your team can make the biggest difference.",
                  "Challenges") + f"""
<section class="section" aria-labelledby="categories-title">
  <div class="container layout-sidebar">
    <nav class="toc" aria-labelledby="toc-title">
      <h2 id="toc-title" class="h4">On this page</h2>
      <ul>{toc}<li><a href="#divisions">Divisions</a></li><li><a href="#judging">Judging criteria</a></li></ul>
    </nav>
    <div>
      <h2 id="categories-title">The six categories</h2>
      <p class="section-intro">Every category is open to all three divisions. Briefs are deliberately open, so you can adapt them to your local context.</p>
      {"".join(cats)}
    </div>
  </div>
</section>""" + section("divisions", "Divisions", f"""
<div class="table-wrap" role="region" aria-labelledby="divisions-caption" tabindex="0">
<table>
  <caption id="divisions-caption">Age divisions for the {EVENT['edition']} Olympiad</caption>
  <thead><tr><th scope="col">Division</th><th scope="col">Who can enter</th></tr></thead>
  <tbody>{divisions}</tbody>
</table></div>
<p>A team competes in the division of its oldest member. Each team has 2–5 students and one adult mentor.</p>""",
                          cls="section-tint") + section("judging", "Judging criteria", f"""
<div class="table-wrap" role="region" aria-labelledby="judging-caption" tabindex="0">
<table>
  <caption id="judging-caption">How Round 2 projects and finalists are scored</caption>
  <thead><tr><th scope="col">Criterion</th><th scope="col">Weight</th><th scope="col">What judges look for</th></tr></thead>
  <tbody>{judging}</tbody>
</table></div>
<p>Read the full judging process in the <a href="rules.html#judging">Rules &amp; Guidelines</a>.</p>""") + cta_band()


def page_schedule():
    items = []
    for t in TIMELINE:
        items.append(f"""
<li class="tl-item" data-start="{t['start']}" data-end="{t.get('end', t['start'])}" id="{t['id']}">
  <div class="tl-marker" aria-hidden="true"></div>
  <div class="tl-card card">
    <p class="tl-when">{icon("calendar")}{time_el(t)} <span class="tag">{t['kind']}</span> <span class="tl-status"></span></p>
    <h3>{t['title']}</h3>
    <p>{t['desc']}</p>
  </div>
</li>""")
    return banner("Schedule & Timeline",
                  f"Key dates for the {EVENT['edition']} edition, from registration to the Awards Ceremony. All times are Brasília time (BRT, UTC−3).",
                  "Schedule") + f"""
<section class="section" aria-labelledby="timeline-title">
  <div class="container layout-sidebar layout-sidebar-right">
    <div>
      <h2 id="timeline-title">Timeline {EVENT['edition']}</h2>
      <p class="section-intro">Status labels update automatically based on today's date.</p>
      <ol class="timeline" role="list">{"".join(items)}</ol>
    </div>
    <aside class="sidebar-stack" aria-label="Schedule tools">
      <div class="card countdown-card">{countdown("schedule-countdown-title", "h2")}</div>
      <div class="card">
        <h2 class="h4">Never miss a deadline</h2>
        <p>Add every milestone to Google Calendar, Outlook or Apple Calendar.</p>
        <p><a class="btn btn-secondary btn-sm" href="assets/docs/{make_pdfs.ICS_NAME}" download>{icon("calendar")}Download calendar <span class="meta">(.ics)</span></a></p>
      </div>
    </aside>
  </div>
</section>""" + section("finals-programme", "Global Finals programme", """
<div class="table-wrap" role="region" aria-labelledby="finals-caption" tabindex="0">
<table>
  <caption id="finals-caption">Draft programme, 28–30 October 2026 (Brasília time)</caption>
  <thead><tr><th scope="col">Day</th><th scope="col">Morning</th><th scope="col">Afternoon</th><th scope="col">Evening</th></tr></thead>
  <tbody>
    <tr><th scope="row">Wednesday 28 October</th><td>Opening session and keynote</td><td>Finalist presentations: Junior division</td><td>Welcome dinner</td></tr>
    <tr><th scope="row">Thursday 29 October</th><td>Finalist presentations: Senior and University divisions</td><td>Workshops and field visits</td><td>Project fair, open to the public</td></tr>
    <tr><th scope="row">Friday 30 October</th><td>Jury deliberations and youth climate forum</td><td>Awards Ceremony, streamed live</td><td>Closing celebration</td></tr>
  </tbody>
</table></div>
<p>The venues in Lisbon (Portugal) and Brazil are linked live, so every session is shared by both audiences. Online finalists present by video call in the same sessions. Times are Brasília time (12:00 in Lisbon when it is 09:00 in Brasília). All sessions are captioned and interpreted into International Sign.</p>""",
                              cls="section-tint") + cta_band()


def page_rules():
    toc = "".join(f'<li><a href="#{i}">{h}</a></li>' for i, h, _, _ in RULES)
    rules = []
    for i, h, paras, items in RULES:
        ps = "".join(f"<p>{b2strong(p)}</p>" for p in paras)
        li = "".join(f"<li>{b2strong(x)}</li>" for x in items)
        rules.append(f'<section class="rule" aria-labelledby="{i}"><h3 id="{i}" tabindex="-1">{h}</h3>{ps}<ul>{li}</ul></section>')
    guide = "".join(f'<li class="card"><h3>{h}</h3><ul>{"".join(f"<li>{x}</li>" for x in items)}</ul></li>'
                    for h, items in GUIDELINES)
    tips = "".join(f'<li class="card"><h3>{h}</h3><ul>{"".join(f"<li>{x}</li>" for x in items)}</ul></li>'
                   for h, items in TIPS)
    return banner("Rules & Guidelines",
                  "Everything teams and mentors need to compete fairly, safely and confidently. The rules below match the official PDF rulebook.",
                  "Rules") + section("downloads", "Downloads", downloads_block(False)
                  + f'<p class="section-cta">Preparing for Round 1? {btn("past-papers.html", "Past papers with worked solutions", "secondary", "arrow")}</p>') + f"""
<section class="section section-tint" aria-labelledby="rules">
  <div class="container layout-sidebar">
    <nav class="toc" aria-labelledby="rules-toc-title">
      <h2 id="rules-toc-title" class="h4">Rulebook contents</h2>
      <ol>{toc}</ol>
    </nav>
    <div class="prose rules">
      <h2 id="rules">Official rules {EVENT['edition']}</h2>
      {"".join(rules)}
    </div>
  </div>
</section>""" + section("guidelines", "Participant guidelines", f'<ul class="grid grid-2 card-list" role="list">{guide}</ul>',
                        intro="Practical advice for every stage of the competition.") \
        + section("tips", "Sustainability tips", f'<ul class="grid grid-3 card-list" role="list">{tips}</ul>',
                  cls="section-tint", intro="Small everyday actions for students, schools and families.")


def page_partners():
    tiers = []
    for tier, items in SPONSORS.items():
        cards = "".join(f"""
<li class="card partner-card">
  <img src="assets/img/partners/{key}.svg" alt="{e(name)} logo" width="240" height="56" loading="lazy">
  <p>{desc}</p>
</li>""" for name, key, desc in items)
        tid = re.sub(r"[^a-z]+", "-", tier.lower()).strip("-")
        tiers.append(f'<h3 id="{tid}">{tier}</h3><ul class="grid grid-3 card-list" role="list">{cards}</ul>')
    countries = sorted({s[2] for s in SCHOOLS})
    options = "".join(f'<option value="{e(c)}">{e(c)}</option>' for c in countries)
    schools = "".join(f"""
<li class="school" data-country="{e(country)}" data-name="{e(name.lower())} {e(city.lower())}">
  <span class="school-name">{e(name)}</span>
  <span class="school-meta">{icon("pin")}{e(city)}, {e(country)} &middot; {e(kind)}</span>
</li>""" for name, city, country, lat, lng, kind in sorted(SCHOOLS, key=lambda s: (s[2], s[0])))
    data = json.dumps([{"name": n, "city": c, "country": co, "lat": la, "lng": ln, "type": k}
                       for n, c, co, la, ln, k in SCHOOLS])
    return banner("Sponsors & Partners",
                  "The Olympiad is free for every student thanks to organisations that share our commitment to education and sustainability.",
                  "Partners") + section("sponsors", "Our partners", "".join(tiers)) + section("become-partner", "Become a partner", f"""
<div class="two-col">
  <div class="prose">
    <p>Partnering with the Sustainable Olympiad connects your organisation with thousands of motivated young innovators,
      their teachers and their communities.</p>
    <ul>
      <li>Sponsor a category award or student grant</li>
      <li>Offer mentoring, workshops or field visits</li>
      <li>Provide equipment and starter kits</li>
      <li>Host a regional event or join the jury</li>
    </ul>
  </div>
  <div class="card">
    <h3>Let&rsquo;s talk</h3>
    <p>Our partnership team will share our impact report and options for 2027.</p>
    <p>{btn("contact.html?subject=partnership", "Contact the partnership team", "primary", "arrow")}</p>
  </div>
</div>""", cls="section-tint") + f"""
<section class="section" aria-labelledby="schools">
  <div class="container">
    <h2 id="schools">Participating schools and institutions</h2>
    <p class="section-intro">A selection of schools, colleges and universities registered for {EVENT['edition']}. Search or filter the list, or view them on a map.</p>
    <form class="filters" role="search" aria-label="Filter schools" data-school-filter>
      <div class="field">
        <label for="school-q">Search by name or city</label>
        <input type="search" id="school-q" name="q" autocomplete="off">
      </div>
      <div class="field">
        <label for="school-country">Country</label>
        <select id="school-country" name="country"><option value="">All countries</option>{options}</select>
      </div>
      <div class="filters-actions">
        <button type="button" class="btn btn-secondary btn-sm" data-map-toggle aria-expanded="false" aria-controls="school-map-wrap" hidden>{icon("pin")}<span>Show map</span></button>
      </div>
    </form>
    <p class="filter-status" role="status" aria-live="polite" id="school-status">Showing all {len(SCHOOLS)} institutions.</p>
    <div id="school-map-wrap" class="map-wrap" hidden>
      <p class="hint" id="school-map-hint">Map data &copy; OpenStreetMap contributors. Use the list above for the same information; map markers can be reached with the Tab key.</p>
      <div id="school-map" class="map" role="region" aria-label="Map of participating institutions" aria-describedby="school-map-hint"></div>
    </div>
    <ul class="school-list" role="list" id="school-list">{schools}</ul>
    <script type="application/json" id="school-data">{data}</script>
  </div>
</section>"""


def page_news():
    tags = sorted({n["tag"] for n in NEWS})
    filters = '<button type="button" aria-pressed="true" data-filter="">All</button>' + "".join(
        f'<button type="button" aria-pressed="false" data-filter="{e(t)}">{t}</button>' for t in tags)
    news = "".join(news_card(n, full=True) for n in NEWS)
    gallery = "".join(f"""
<li>
  <figure class="gallery-item">
    <a href="assets/img/gallery/{k}.svg" data-lightbox data-caption="{e(cap)}">
      <img src="assets/img/gallery/{k}.svg" alt="{e(alt)}" width="800" height="500" loading="lazy">
      <span class="visually-hidden"> (enlarge photo)</span>
    </a>
    <figcaption>{cap}</figcaption>
  </figure>
</li>""" for k, alt, cap in GALLERY)
    return banner("News & Gallery", f"Updates on the {EVENT['edition']} Olympiad and highlights from past editions.", "News & Gallery") + f"""
<section class="section" aria-labelledby="news">
  <div class="container">
    <h2 id="news">Latest news</h2>
    <div class="filter-buttons" role="group" aria-label="Filter news by topic">{filters}</div>
    <p class="filter-status" role="status" aria-live="polite" id="news-status"></p>
    <div class="grid grid-2 news-grid">{news}</div>
  </div>
</section>
<section class="section section-tint" aria-labelledby="gallery">
  <div class="container">
    <h2 id="gallery">Gallery: past editions</h2>
    <p class="section-intro">Select an image to enlarge it. Use the arrow keys to move between images and Escape to close.</p>
    <ul class="gallery" role="list">{gallery}</ul>
  </div>
</section>
<dialog class="lightbox" aria-labelledby="lightbox-caption">
  <div class="lightbox-inner">
    <button type="button" class="lightbox-close icon-btn" data-lb="close">{icon("close")}<span class="visually-hidden">Close</span></button>
    <img src="" alt="" width="800" height="500">
    <p id="lightbox-caption" class="lightbox-caption"></p>
    <div class="lightbox-nav">
      <button type="button" class="btn btn-secondary btn-sm" data-lb="prev">Previous</button>
      <span class="lightbox-count" aria-live="polite"></span>
      <button type="button" class="btn btn-secondary btn-sm" data-lb="next">Next</button>
    </div>
  </div>
</dialog>"""


def page_faq():
    groups = []
    for gi, (g, qs) in enumerate(FAQ):
        gid = re.sub(r"[^a-z]+", "-", g.lower()).strip("-")
        items = "".join(f"""
<details class="faq-item">
  <summary><span>{q}</span></summary>
  <div class="faq-answer"><p>{a}</p></div>
</details>""" for q, a in qs)
        groups.append(f'<section class="faq-group" aria-labelledby="faq-{gid}"><h2 id="faq-{gid}">{g}</h2>{items}</section>')
    return banner("Frequently Asked Questions", "Quick answers about taking part. Can&rsquo;t find what you need? Contact us.", "FAQ") + f"""
<section class="section" aria-label="Questions and answers">
  <div class="container narrow">
    <form class="filters filters-single" role="search" aria-label="Filter questions" onsubmit="return false">
      <div class="field">
        <label for="faq-q">Filter questions</label>
        <p class="hint" id="faq-q-hint">Type a word such as &ldquo;team&rdquo;, &ldquo;cost&rdquo; or &ldquo;travel&rdquo;.</p>
        <input type="search" id="faq-q" aria-describedby="faq-q-hint" autocomplete="off" data-faq-filter>
      </div>
    </form>
    <p class="filter-status" role="status" aria-live="polite" id="faq-status"></p>
    <p class="faq-tools"><button type="button" class="link-btn" data-faq-expand hidden>Expand all answers</button></p>
    {"".join(groups)}
    <div class="card callout">
      <h2 class="h3">Still have a question?</h2>
      <p>Our team usually replies within two working days.</p>
      <p>{btn("contact.html", "Contact us", "primary", "arrow")}</p>
    </div>
  </div>
</section>"""


def page_contact():
    subjects = [("general", "General question"), ("registration", "Registration and teams"),
                ("partnership", "Partnership and sponsorship"), ("media", "Media and press"),
                ("accessibility", "Accessibility support"), ("other", "Something else")]
    social = "".join(f'<li><a href="{u}" target="_blank" rel="noopener">{icon(i)}{n}<span class="visually-hidden"> (opens in a new tab)</span></a></li>'
                     for n, u, i in SITE["social"])
    addr = "<br>".join(SITE["address"])
    return banner("Contact Us", "Questions about the competition, partnerships or accessibility? We&rsquo;re here to help.", "Contact") + f"""
<section class="section" aria-labelledby="contact-form-title">
  <div class="container layout-sidebar layout-sidebar-right">
    <div>
      <h2 id="contact-form-title">Send us a message</h2>
      <p>All fields marked <span class="req">(required)</span> must be completed.</p>
      {error_summary("contact")}
      {success_panel("contact", "Thank you, your message is ready", "We usually reply within two working days.")}
      <form {form_attrs("contact", "Website contact form")} novalidate aria-labelledby="contact-form-title">
        {field("contact-name", "Full name", autocomplete="name", error="Enter your full name", name="name")}
        {field("contact-email", "Email address", "email", autocomplete="email", error="Enter your email address", name="email",
               hint="We will only use this to reply to you.")}
        {field("contact-org", "School or organisation", required=False, autocomplete="organization", name="organisation")}
        {field("contact-subject", "Subject", "select", options=subjects, error="Choose a subject", name="subject")}
        {field("contact-message", "Message", "textarea", error="Enter your message", name="message", rows=6,
               attrs='minlength="10" maxlength="2000" data-error-minlength="Your message must be at least 10 characters"',
               hint="Up to 2,000 characters.")}
        {field("contact-consent", 'I agree that my details will be used to answer my enquiry, as described in the <a href="#privacy">privacy notice</a>.',
               "checkbox", error="Confirm that we can use your details to reply", name="consent")}
        <button type="submit" class="btn btn-primary">Send message{icon("arrow")}</button>
        <p class="form-status" role="status" aria-live="polite"></p>
      </form>
    </div>
    <aside class="sidebar-stack" aria-labelledby="contact-details-title">
      <div class="card">
        <h2 id="contact-details-title" class="h3">Contact details</h2>
        <ul class="contact-list">
          <li>{icon("mail")}<a href="mailto:{SITE['contact_email']}">{SITE['contact_email']}</a></li>
          <li>{icon("pin")}<address>{addr}</address></li>
          <li>{icon("clock")}<span>Monday to Friday, 09:00–17:00 (Lisbon time)</span></li>
        </ul>
      </div>
      <div class="card">
        <h2 class="h3">Follow us</h2>
        <ul class="social-text-list">{social}</ul>
      </div>
      <div class="card">
        <h2 class="h3">Quick answers</h2>
        <p>Many questions are answered in our <a href="faq.html">FAQ</a>.</p>
      </div>
    </aside>
  </div>
</section>""" + section("privacy", "Privacy notice", """
<div class="prose">
  <p>We collect only the information you choose to send us through our forms: your name, contact details and message,
    or your team's registration details. We use it solely to run the Sustainable Olympiad and to reply to you.</p>
  <ul>
    <li>We never sell or share your data for marketing.</li>
    <li>Registration data is deleted 12 months after the end of each edition.</li>
    <li>Newsletter subscribers can unsubscribe at any time using the link in every email.</li>
    <li>This website does not use tracking or advertising cookies. Your accessibility preferences are stored only in your own browser.</li>
  </ul>
  <p>To access, correct or delete your data, contact us using the details above.</p>
</div>""", cls="section-tint")


def page_register():
    cats = [(c["id"], c["name"]) for c in CATEGORIES]
    divs = [(d, f"{d} ({a})") for d, a in DIVISIONS]
    members = []
    for n in range(2, 6):
        req = n == 2
        hidden = "" if n <= 2 else ' data-optional-member hidden'
        members.append(f"""
<fieldset class="member"{hidden} id="member-{n}">
  <legend>Team member {n}{' <span class="req">(required)</span>' if req else ' <span class="opt">(optional)</span>'}</legend>
  <div class="field-row">
    {field(f"member{n}-name", "Full name", required=req, error=f"Enter the name of team member {n}", name=f"member{n}_name")}
    {field(f"member{n}-email", "Email address", "email", required=False, name=f"member{n}_email")}
  </div>
</fieldset>""")
    return banner("Register Your Team",
                  f"Registration for the {EVENT['edition']} Olympiad is free and open until {EVENT['registration_deadline']}. It takes about ten minutes.",
                  "Register") + f"""
<section class="section" aria-labelledby="register-title">
  <div class="container layout-sidebar layout-sidebar-right">
    <div>
      <h2 id="register-title">Team registration form</h2>
      <p>All fields marked <span class="req">(required)</span> must be completed. The team captain should fill in this form.</p>
      {error_summary("register")}
      {success_panel("register", "Registration ready to send", "Thank you for registering. We will confirm your place by email within three working days.")}
      <form {form_attrs("register", f"Team registration {EVENT['edition']}")} novalidate aria-labelledby="register-title">
        <fieldset>
          <legend>1. Your team</legend>
          {field("team-name", "Team name", error="Enter a team name", name="team_name", attrs='maxlength="60"',
                 hint="Up to 60 characters. This will appear on certificates.")}
          <div class="field-row">
            {field("team-category", "Challenge category", "select", options=cats, error="Choose a challenge category", name="category")}
            {field("team-division", "Division", "select", options=divs, error="Choose a division", name="division",
                   hint="Based on the age of your oldest team member.")}
          </div>
          {field("team-school", "School, college or university", autocomplete="organization", error="Enter the name of your school or institution", name="institution")}
          <div class="field-row">
            {field("team-city", "City", autocomplete="address-level2", error="Enter your city", name="city")}
            {field("team-country", "Country", autocomplete="country-name", error="Enter your country", name="country")}
          </div>
        </fieldset>
        <fieldset>
          <legend>2. Team captain</legend>
          <div class="field-row">
            {field("captain-name", "Full name", autocomplete="name", error="Enter the team captain's full name", name="captain_name")}
            {field("captain-email", "Email address", "email", autocomplete="email", error="Enter the team captain's email address", name="captain_email",
                   hint="We will send the confirmation here.")}
          </div>
        </fieldset>
        <fieldset>
          <legend>3. Team members</legend>
          <p class="hint">Teams have 2 to 5 students, including the captain.</p>
          {"".join(members)}
          <p><button type="button" class="btn btn-ghost-dark btn-sm" data-add-member hidden>{icon("plus")}Add another team member</button></p>
          <p class="form-status" role="status" aria-live="polite" data-member-status></p>
        </fieldset>
        <fieldset>
          <legend>4. Mentor</legend>
          <p class="hint">A teacher, lecturer or other responsible adult aged 21 or over.</p>
          <div class="field-row">
            {field("mentor-name", "Mentor's full name", error="Enter your mentor's full name", name="mentor_name")}
            {field("mentor-email", "Mentor's email address", "email", error="Enter your mentor's email address", name="mentor_email")}
          </div>
          {field("mentor-role", "Mentor's role", required=False, name="mentor_role", hint="For example, Biology teacher.")}
        </fieldset>
        <fieldset>
          <legend>5. Support and preferences</legend>
          {field("access-needs", "Accessibility or support needs", "textarea", required=False, name="access_needs", rows=3,
                 hint="Tell us about any adjustments that would help your team take part, such as extra time or captioning.")}
          {field("heard", "How did you hear about us?", "select", required=False, name="heard",
                 options=[("teacher", "From a teacher"), ("social", "Social media"), ("friend", "A friend"), ("previous", "We took part before"), ("other", "Other")])}
        </fieldset>
        <fieldset>
          <legend>6. Confirmation</legend>
          {field("agree-rules", 'We have read and agree to the <a href="rules.html" target="_blank">official rules<span class="visually-hidden"> (opens in a new tab)</span></a>.',
                 "checkbox", error="Confirm that your team agrees to the rules", name="agree_rules")}
          {field("agree-consent", "Our mentor confirms that parental or guardian consent has been obtained for every team member under 18.",
                 "checkbox", error="Confirm that guardian consent has been obtained", name="guardian_consent")}
          {field("agree-news", "Send us the monthly newsletter.", "checkbox", required=False, name="newsletter")}
        </fieldset>
        <button type="submit" class="btn btn-primary btn-lg">Submit registration{icon("arrow")}</button>
        <p class="form-status" role="status" aria-live="polite"></p>
      </form>
    </div>
    <aside class="sidebar-stack" aria-labelledby="checklist-title">
      <div class="card">
        <h2 id="checklist-title" class="h3">Before you start</h2>
        <ul class="checklist">
          <li>{icon("check")}<span>Names of 2–5 team members</span></li>
          <li>{icon("check")}<span>Your mentor&rsquo;s name and email address</span></li>
          <li>{icon("check")}<span>Your chosen <a href="challenges.html">challenge category</a></span></li>
          <li>{icon("check")}<span>Guardian consent for members under 18</span></li>
        </ul>
      </div>
      <div class="card">
        <h2 class="h3">Key deadlines</h2>
        <p><strong>Round 1:</strong> <time datetime="2026-10-10">10 October 2026</time></p>
        <p><strong>Registration closes:</strong> <time datetime="{EVENT['registration_deadline_iso']}">{EVENT['registration_deadline']}</time></p>
      </div>
      <div class="card">
        <h2 class="h3">Need help?</h2>
        <p>Read the <a href="faq.html">FAQ</a> or <a href="contact.html?subject=registration">contact us</a>.</p>
      </div>
    </aside>
  </div>
</section>"""


def page_search():
    return banner("Search", "Find pages, rules, dates and answers across the website.", "Search") + """
<section class="section" aria-labelledby="results-title">
  <div class="container narrow">
    <form class="search-page-form" role="search" aria-label="Search page" action="search.html" method="get" data-search-form>
      <label for="search-page-q">Search the site</label>
      <div class="inline-field">
        <input type="search" id="search-page-q" name="q" autocomplete="off">
        <button type="submit" class="btn btn-primary">Search</button>
      </div>
    </form>
    <h2 id="results-title" class="h3">Results</h2>
    <p id="search-status" role="status" aria-live="polite">Enter a word or phrase to search.</p>
    <ol class="search-results" id="search-results" role="list"></ol>
    <noscript><p>Search needs JavaScript. You can browse all pages from the main menu.</p></noscript>
  </div>
</section>"""


def page_accessibility():
    return banner("Accessibility Statement",
                  "We want everyone to be able to use this website and take part in the Olympiad.", "Accessibility") + section(
        "commitment", "Our commitment", """
<div class="prose">
  <p>This website is designed to conform to the <a href="https://www.w3.org/TR/WCAG21/">Web Content Accessibility Guidelines (WCAG) 2.1</a>
    at level AA. Accessibility is part of how we design, write and test every page.</p>
</div>""") + section("features", "Accessibility features", """
<div class="prose">
  <ul>
    <li>A &ldquo;Skip to main content&rdquo; link and clear page landmarks for screen readers.</li>
    <li>Full keyboard support, with a clearly visible focus indicator.</li>
    <li>Text and controls that meet WCAG AA colour contrast in every theme.</li>
    <li>An accessibility toolbar with text size, dark mode, high contrast, text spacing and link highlighting.</li>
    <li>Layouts that reflow at 400% zoom and on small screens without horizontal scrolling.</li>
    <li>Respect for your system&rsquo;s reduced-motion and dark mode settings.</li>
    <li>Forms with visible labels, clear instructions and error messages that are announced to screen readers.</li>
    <li>Text alternatives for all meaningful images, with decorative images hidden from assistive technology.</li>
  </ul>
</div>""", cls="section-tint") + section("toolbar-help", "Using the accessibility toolbar", """
<div class="prose">
  <p>Select <strong>Accessibility</strong> at the top of any page to open the toolbar. Your choices are remembered on this device.</p>
  <ul>
    <li><strong>Text size:</strong> enlarge text up to 200%. Browser zoom (Ctrl or Cmd and +) also works.</li>
    <li><strong>Dark mode:</strong> light text on a dark background.</li>
    <li><strong>High contrast:</strong> maximum contrast with yellow highlights.</li>
    <li><strong>Text spacing:</strong> more space between lines, words and letters.</li>
    <li><strong>Highlight links:</strong> makes every link stand out clearly.</li>
  </ul>
</div>""") + section("limitations", "Known limitations", """
<div class="prose">
  <ul>
    <li>The downloadable PDFs are not yet fully tagged for screen readers. The same content is available as web pages:
      the rulebook, guidelines and tips on the <a href="rules.html">Rules &amp; Guidelines</a> page, and every past paper
      as an online practice page via <a href="past-papers.html">Past Papers</a>.</li>
    <li>The optional schools map uses a third-party map service. The same information is always available in the list on the
      <a href="partners.html#schools">Partners</a> page.</li>
  </ul>
</div>""", cls="section-tint") + section("feedback", "Feedback and contact", """
<div class="prose">
  <p>If you have difficulty using any part of this website, or you need information in a different format,
    please <a href="contact.html?subject=accessibility">contact us</a>. We aim to respond within two working days.</p>
  <p>This statement was last reviewed on 1 October 2026.</p>
</div>""")


# ---------------------------------------------------------------------------
# Past papers
# ---------------------------------------------------------------------------
def paper_files(p):
    paper, sol = make_paper_pdfs.file_names(p)
    return f"past-papers/{paper}", f"past-papers/{sol}"


def paper_label(p):
    return f"{p['year']} {p['division']} paper"


def page_past_papers():
    years = sorted({p["year"] for p in PAPERS}, reverse=True)
    groups = []
    for y in years:
        cards = []
        for p in [x for x in PAPERS if x["year"] == y]:
            paper, sol = paper_files(p)
            n_q = len(p["part_a"]) + len(p["part_b"])
            cards.append(f"""
<article class="card paper-card" aria-labelledby="pp-{p['id']}">
  <p class="paper-kicker"><span class="tag">{p['division']}</span> Ages {p['ages']}</p>
  <h3 id="pp-{p['id']}">{p['year']} {p['division']} Division</h3>
  <p class="paper-sub">Round 1: Online Knowledge Challenge</p>
  <ul class="paper-meta" role="list">
    <li>{icon("clock")}{p['duration']} minutes</li>
    <li>{icon("trophy")}{total_marks(p)} marks</li>
    <li>{icon("file")}{n_q} questions</li>
  </ul>
  <p class="paper-topics"><strong>Topics:</strong> {", ".join(p['topics'])}.</p>
  <div class="paper-actions">
    {btn(f"paper-{p['id']}.html", f"Practise online<span class='visually-hidden'>: {paper_label(p)}</span>", "primary btn-sm", "arrow")}
    <a class="btn btn-secondary btn-sm" href="assets/docs/{paper}" download>{icon("download")}Question paper<span class="visually-hidden">, {paper_label(p)},</span> <span class="meta">(PDF, {file_size(paper)})</span></a>
    <a class="btn btn-ghost-dark btn-sm" href="assets/docs/{sol}" download>{icon("download")}Solutions<span class="visually-hidden">, {paper_label(p)},</span> <span class="meta">(PDF, {file_size(sol)})</span></a>
  </div>
</article>""")
        groups.append(section(f"edition-{y}", f"{y} edition", f'<div class="grid grid-2">{"".join(cards)}</div>',
                              cls="section-tint" if y != years[0] else ""))
    zip_name = "past-papers/sustainable-olympiad-past-papers.zip"
    return banner("Past Papers",
                  "Real Round 1 papers from previous editions, with mark schemes and fully worked solutions. "
                  "Practise online or download them to print.", "Past Papers") + f"""
<section class="section" aria-labelledby="about-papers">
  <div class="container two-col">
    <div class="prose">
      <h2 id="about-papers">Prepare like a finalist</h2>
      <p>Round 1 is a 90-minute Knowledge Challenge taken by each team at their own school. Part A has ten
        multiple-choice questions. Part B has multi-step problems that test whether you can apply science and
        mathematics to real sustainability decisions.</p>
      <p>These papers are set at olympiad level. Senior papers in particular are meant to stretch the strongest
        students: <strong>a score of around 50% is a strong result</strong>, and the top teams usually score above 75%.</p>
      <h3>How to use them</h3>
      <ol>
        <li>Download the question paper, or use the online version, and set a 90-minute timer.</li>
        <li>Work as a team, with a scientific calculator and the data sheet only.</li>
        <li>Mark your work with the mark scheme. Method marks count as much as final answers.</li>
        <li>Study the worked solutions for every question you missed, then try a different paper.</li>
      </ol>
    </div>
    <aside class="card" aria-labelledby="download-all-title">
      <span class="card-icon">{icon("download")}</span>
      <h2 id="download-all-title" class="h3">Download everything</h2>
      <p>All {len(PAPERS)} question papers and mark schemes in one file.</p>
      <p><a class="btn btn-primary" href="assets/docs/{zip_name}" download>{icon("download")}All past papers <span class="meta">(ZIP, {file_size(zip_name)})</span></a></p>
      <p class="hint">The online versions are fully accessible to screen readers. The PDFs are designed for printing.</p>
    </aside>
  </div>
</section>""" + "".join(groups) + cta_band("Ready for the real thing?", f"Register your team for the {EVENT['edition']} Olympiad before {EVENT['registration_deadline']}.")


def page_paper(p):
    pid = p["id"]
    paper, sol = paper_files(p)
    data = "".join(f"<li>{d}</li>" for d in p["data"])
    qa = []
    for i, q in enumerate(p["part_a"], 1):
        qid = f"a{i}"
        opts = "".join(f"""
      <div class="option">
        <input type="radio" name="{qid}" id="{qid}-{L}" value="{L}">
        <label for="{qid}-{L}"><span class="opt-letter" aria-hidden="true">{L}</span><span class="opt-text"><span class="visually-hidden">{L}: </span>{o}</span></label>
      </div>""" for L, o in zip("ABCD", q["options"]))
        qa.append(f"""
<article class="exam-q" id="{qid}" aria-labelledby="{qid}-title" data-answer="{q['answer']}">
  <h3 id="{qid}-title">Question A{i} <span class="q-marks">2 marks</span></h3>
  <p class="q-text">{q['q']}</p>
  <fieldset class="options">
    <legend class="visually-hidden">Answer options for question A{i}</legend>{opts}
  </fieldset>
  <div class="q-actions" hidden>
    <button type="button" class="btn btn-secondary btn-sm" data-check>Check answer<span class="visually-hidden"> to question A{i}</span></button>
    <p class="q-feedback" role="status" aria-live="polite"></p>
  </div>
  <details class="solution">
    <summary>Worked solution<span class="visually-hidden"> for question A{i}</span></summary>
    <div class="solution-body"><p><strong>Answer: {q['answer']}.</strong> {q['solution']}</p></div>
  </details>
</article>""")
    qb = []
    for i, q in enumerate(p["part_b"], 1):
        qm = sum(x["marks"] for x in q["parts"])
        parts = "".join(f"""
    <li>
      <div class="part-q"><span class="part-letter" aria-hidden="true">({'abcdefg'[j]})</span>
        <p><span class="visually-hidden">Part {'abcdefg'[j]}: </span>{part['text']} <span class="q-marks">{part['marks']} mark{'s' if part['marks'] > 1 else ''}</span></p></div>
      <details class="solution">
        <summary>Worked solution<span class="visually-hidden"> for question B{i} part {'abcdefg'[j]}</span></summary>
        <div class="solution-body"><p>{part['solution']}</p><p class="scheme"><strong>Marking:</strong> {part['scheme']}</p></div>
      </details>
    </li>""" for j, part in enumerate(q["parts"]))
        qb.append(f"""
<article class="exam-q exam-q-long" id="b{i}" aria-labelledby="b{i}-title">
  <h3 id="b{i}-title">Question B{i}: {q['title']} <span class="q-marks">{qm} marks</span></h3>
  <p class="q-text">{q['stem']}</p>
  <ol class="parts" role="list">{parts}</ol>
</article>""")
    others = "".join(f'<li><a href="paper-{x["id"]}.html">{x["year"]} {x["division"]} Division</a></li>'
                     for x in PAPERS if x["id"] != pid)
    return banner(f"{p['year']} {p['division']} Division: Round 1",
                  f"The Online Knowledge Challenge from the {p['year']} edition, for students aged {p['ages']}. "
                  f"{p['duration']} minutes, {total_marks(p)} marks.",
                  f"{p['year']} {p['division']}", ("past-papers.html", "Past Papers")) + f"""
<section class="section" aria-labelledby="paper-intro">
  <div class="container layout-sidebar layout-sidebar-right">
    <div>
      <h2 id="paper-intro">Before you start</h2>
      <ul class="paper-meta paper-meta-lg" role="list">
        <li>{icon("clock")}{p['duration']} minutes</li>
        <li>{icon("trophy")}{total_marks(p)} marks</li>
        <li>{icon("file")}Part A: {len(p['part_a'])} multiple-choice questions ({2 * len(p['part_a'])} marks)</li>
        <li>{icon("file")}Part B: {len(p['part_b'])} structured problems ({part_b_marks(p)} marks)</li>
      </ul>
      <p>Set a timer and work as a team. You may use a scientific calculator and the data sheet. For Part A, choose an answer
        and check it. For Part B, write your working on paper, then compare it with the worked solution and mark scheme.</p>
      <p class="paper-tools"><button type="button" class="link-btn" data-toggle-solutions hidden>Show all worked solutions</button></p>
      <div class="card data-sheet">
        <h2 id="data-sheet" class="h3">Data sheet</h2>
        <ul>{data}</ul>
      </div>
    </div>
    <aside class="sidebar-stack" aria-labelledby="paper-downloads-title">
      <div class="card">
        <h2 id="paper-downloads-title" class="h3">Download</h2>
        <p><a class="btn btn-secondary btn-sm" href="assets/docs/{paper}" download>{icon("download")}Question paper <span class="meta">(PDF, {file_size(paper)})</span></a></p>
        <p><a class="btn btn-ghost-dark btn-sm" href="assets/docs/{sol}" download>{icon("download")}Mark scheme <span class="meta">(PDF, {file_size(sol)})</span></a></p>
      </div>
      <nav class="card" aria-labelledby="other-papers-title">
        <h2 id="other-papers-title" class="h3">Other papers</h2>
        <ul>{others}</ul>
        <p><a href="past-papers.html">All past papers</a></p>
      </nav>
    </aside>
  </div>
</section>
<section class="section section-tint" aria-labelledby="part-a">
  <div class="container narrow" data-quiz>
    <h2 id="part-a">Part A: Multiple choice <span class="q-marks">{2 * len(p['part_a'])} marks</span></h2>
    <p class="section-intro">Each question is worth 2 marks. Choose one answer.</p>
    {"".join(qa)}
    <div class="card quiz-score" hidden>
      <h3 id="score-title">Your Part A score</h3>
      <p>Check every answer at once to see your score.</p>
      <p class="quiz-buttons"><button type="button" class="btn btn-primary" data-check-all>Check all Part A answers</button>
        <button type="button" class="btn btn-ghost-dark" data-reset>Start again</button></p>
      <p class="quiz-result" role="status" aria-live="polite"></p>
    </div>
  </div>
</section>
<section class="section" aria-labelledby="part-b">
  <div class="container narrow">
    <h2 id="part-b">Part B: Structured problems <span class="q-marks">{part_b_marks(p)} marks</span></h2>
    <p class="section-intro">Show all your working. Method marks are awarded even if the final answer is wrong.</p>
    {"".join(qb)}
    <p class="end-paper">End of paper. <a href="past-papers.html">Try another past paper</a>.</p>
  </div>
</section>"""


PAGES = [
    ("index", "Sustainable Olympiad 2026 | Young minds. Real solutions. One planet.",
     "The Sustainable Olympiad is a free international competition where student teams design real solutions for energy, waste, water, climate and nature. Register for 2026.",
     page_index, []),
    ("about", "About", "The mission, goals and history of the Sustainable Olympiad, an international sustainability competition for students since 2020.", page_about, []),
    ("challenges", "Challenges & Categories", "Six competition categories: renewable energy, waste reduction, sustainable design, climate solutions, water & oceans, and biodiversity & food.", page_challenges, []),
    ("schedule", "Schedule & Timeline", "Key dates for the Sustainable Olympiad 2026: registration deadline, competition rounds, Global Finals and Awards Ceremony.", page_schedule, []),
    ("rules", "Rules & Guidelines", "Official rules, participant guidelines and sustainability tips for the Sustainable Olympiad 2026, with PDF downloads.", page_rules, []),
    ("partners", "Sponsors & Partners", "The sponsors, partners, schools and institutions that make the Sustainable Olympiad possible.", page_partners, ["schools.js"]),
    ("news", "News & Gallery", "News, announcements and photos from the Sustainable Olympiad.", page_news, []),
    ("faq", "FAQ", "Frequently asked questions about registering for and competing in the Sustainable Olympiad.", page_faq, []),
    ("contact", "Contact", "Contact the Sustainable Olympiad team about registration, partnerships, media or accessibility.", page_contact, []),
    ("register", "Register", "Register your team for the Sustainable Olympiad 2026. Free for students aged 12 to 25.", page_register, []),
    ("search", "Search", "Search the Sustainable Olympiad website.", page_search, ["search.js"]),
    ("accessibility", "Accessibility Statement", "How the Sustainable Olympiad website meets WCAG 2.1 AA and how to use the accessibility toolbar.", page_accessibility, []),
    ("past-papers", "Past Papers", "Round 1 past papers from previous Sustainable Olympiad editions, with mark schemes and worked solutions. Practise online or download PDFs.", page_past_papers, []),
] + [
    (f"paper-{p['id']}", f"{p['year']} {p['division']} Division: Round 1 Past Paper",
     f"Practise the {p['year']} Sustainable Olympiad Round 1 paper for the {p['division']} division (ages {p['ages']}), with answers and worked solutions.",
     (lambda p=p: page_paper(p)), [])
    for p in PAPERS
]


# ---------------------------------------------------------------------------
# Search index
# ---------------------------------------------------------------------------
def strip(s):
    s = re.sub(r"<(script|style|svg|dialog)\b.*?</\1>", " ", s, flags=re.S)
    s = re.sub(r"<[^>]+>", " ", s)
    return re.sub(r"\s+", " ", html.unescape(s)).strip()


def index_page(page, title, main_html):
    entries = []
    parts = re.split(r'(<h[23][^>]*\bid="[^"]+"[^>]*>.*?</h[23]>)', main_html, flags=re.S)
    current = (page + ".html", title.split(" | ")[0])
    buf = parts[0]
    for p in parts[1:]:
        m = re.match(r'<h[23][^>]*\bid="([^"]+)"[^>]*>(.*?)</h[23]>', p, flags=re.S)
        if m:
            if strip(buf):
                entries.append({"url": current[0], "title": current[1], "page": title.split(" | ")[0], "text": strip(buf)[:1200]})
            current = (f"{page}.html#{m.group(1)}", strip(m.group(2)))
            buf = ""
        else:
            buf += p
    if strip(buf):
        entries.append({"url": current[0], "title": current[1], "page": title.split(" | ")[0], "text": strip(buf)[:1200]})
    return entries


def write_config():
    cfg = {"contactEmail": SITE["contact_email"], "formEndpoint": SITE["form_endpoint"]}
    with open(os.path.join(ROOT, "assets", "js", "config.js"), "w") as f:
        f.write("/* Generated by _build/build.py. Edit SITE in build.py, not this file. */\n"
                f"window.SO_CONFIG = {json.dumps(cfg, indent=2)};\n")


def main():
    make_images.main()
    make_pdfs.main()
    make_paper_pdfs.main()
    write_config()
    index = []
    for page, title, desc, fn, extra in PAGES:
        main_html = fn()
        doc = head(page, title, desc) + header(page) + main_html + footer() + "\n" + scripts(extra)
        with open(os.path.join(ROOT, f"{page}.html"), "w") as f:
            f.write(doc)
        if page != "search":
            index += index_page(page, title, main_html)
    os.makedirs(os.path.join(ROOT, "assets", "data"), exist_ok=True)
    with open(os.path.join(ROOT, "assets", "data", "search-index.json"), "w") as f:
        json.dump(index, f, ensure_ascii=False, separators=(",", ":"))
    print(f"Built {len(PAGES)} pages, {len(index)} search entries.")


if __name__ == "__main__":
    main()
