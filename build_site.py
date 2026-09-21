# -*- coding: utf-8 -*-
"""Assemble the static site in docs/ from the canonical pitch/ and plan/ sources.

pitch/ and plan/ stay the editable originals; docs/ is generated and disposable.
Serves HTML plus images only - PDFs stay local and are never published.
Adds a noindex meta to every document so the deploy stays out of search results.
"""
import os, re, shutil, datetime

DOCS = [
    ("aashas-pitch.html",   "pitch/aashas-pitch.html",
     "Aashas", "Content &amp; Growth Proposal", "Proposal with full costing", "wine"),
    ("aashas-plan.html",    "plan/aashas-plan.html",
     "Aashas", "Content &amp; Brand Growth Plan", "Growth plan, 15 sections", "wine"),
    ("mommade-pitch.html",  "pitch/mommade-pitch.html",
     "Mom Made", "Content &amp; Growth Proposal", "Proposal with full costing", "wood"),
    ("mommade-plan.html",   "plan/mommade-plan.html",
     "Mom Made", "Content &amp; Brand Growth Plan", "Growth plan, 17 sections", "wood"),
]
ASSET_DIRS = [("pitch/a_assets", "a_assets"), ("pitch/m_assets", "m_assets"),
              ("plan/assets", "assets")]
NOINDEX = '<meta name="robots" content="noindex, nofollow">'

def main():
    if os.path.isdir("docs"):
        shutil.rmtree("docs")
    os.makedirs("docs", exist_ok=True)

    for src, dst in ASSET_DIRS:
        if os.path.isdir(src):
            shutil.copytree(src, f"docs/{dst}")

    for name, html, brand, kind, blurb, tone in DOCS:
        s = open(html, encoding="utf-8").read()
        if NOINDEX not in s:
            s = re.sub(r"(</title>)", r"\1\n" + NOINDEX, s, count=1)
        open(f"docs/{name}", "w", encoding="utf-8").write(s)

    open("docs/.nojekyll", "w").close()
    open("docs/robots.txt", "w").write("User-agent: *\nDisallow: /\n")

    cards = ""
    for name, _h, brand, kind, blurb, tone in DOCS:
        cards += f"""
    <article class="card {tone}">
      <p class="brand">{brand}</p>
      <h2><a href="{name}">{kind}</a></h2>
      <p class="blurb">{blurb}</p>
      <p class="links"><a href="{name}">Open document</a></p>
    </article>"""

    today = datetime.date.today().strftime("%d %B %Y")
    open("docs/index.html", "w", encoding="utf-8").write(f"""<!doctype html>
<html lang="en"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Client Documents</title>
{NOINDEX}
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;500;600;700&display=swap">
<style>
:root{{--ink:#1B1A19;--paper:#FBFAF8;--quiet:#6E6963;--line:#DFDAD2;
  --wine:#6E1A20;--wood:#2A1D14;
  --sans:"Archivo",-apple-system,"Segoe UI",Helvetica,Arial,sans-serif}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--paper);color:var(--ink);font-family:var(--sans);
  font-size:16px;line-height:1.6}}
.wrap{{max-width:780px;margin:0 auto;padding-inline:clamp(20px,5vw,40px)}}
header{{background:var(--ink);color:var(--paper)}}
header .wrap{{padding-block:clamp(40px,7vw,68px)}}
h1{{font-size:clamp(1.8rem,4vw,2.6rem);line-height:1.1;margin:0 0 10px;font-weight:600;
  letter-spacing:-.015em}}
header p{{margin:0;color:#B8B2AA;font-size:.9rem}}
main .wrap{{padding-block:clamp(32px,5vw,52px);display:grid;gap:18px}}
.card{{border:1px solid var(--line);border-left:4px solid var(--line);border-radius:3px;
  padding:20px 22px;background:#fff}}
.card.wine{{border-left-color:var(--wine)}}
.card.wood{{border-left-color:var(--wood)}}
.brand{{margin:0;font-size:.64rem;font-weight:700;letter-spacing:.19em;text-transform:uppercase;
  color:var(--quiet)}}
.card h2{{margin:6px 0 4px;font-size:1.16rem;font-weight:600;letter-spacing:-.005em}}
.card h2 a{{color:inherit;text-decoration:none}}
.card h2 a:hover{{text-decoration:underline}}
.blurb{{margin:0 0 12px;font-size:.88rem;color:var(--quiet)}}
.links{{margin:0;display:flex;flex-wrap:wrap;gap:8px 18px;font-size:.85rem}}
.links a{{color:var(--wine);font-weight:600;text-decoration:none}}
.card.wood .links a{{color:var(--wood)}}
.links a:hover{{text-decoration:underline}}
a:focus-visible{{outline:2px solid var(--wine);outline-offset:3px}}
.note{{margin-top:14px;padding:15px 18px;border-left:3px solid #C9A227;
  background:#FBF6E6;font-size:.85rem;line-height:1.55;color:#5A5348}}
footer .wrap{{padding-block:26px;border-top:1px solid var(--line);font-size:.78rem;
  color:var(--quiet)}}
@media (prefers-reduced-motion:reduce){{*{{animation:none!important;transition:none!important}}}}
</style></head><body>
<header><div class="wrap">
  <h1>Client Documents</h1>
  <p>Proposals and growth plans &middot; Updated {today}</p>
</div></header>
<main><div class="wrap">{cards}
  <p class="note"><strong>Confidential.</strong> These documents contain commercial terms,
  rate cards and client business data. This site is excluded from search engines, but anyone
  holding the link can read it. Share the link deliberately.</p>
</div></main>
<footer><div class="wrap">Storzey Content Studio &middot; Hyderabad</div></footer>
</body></html>
""")

    total = sum(os.path.getsize(os.path.join(r, f))
                for r, _d, fs in os.walk("docs") for f in fs)
    files = sum(len(fs) for _r, _d, fs in os.walk("docs"))
    print(f"docs/ built: {files} files, {total/1e6:.2f} MB")

if __name__ == "__main__":
    main()
