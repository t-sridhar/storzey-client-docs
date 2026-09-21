# Client documents

Static site hosting proposals and growth plans for Storzey Content Studio clients.

## Layout

| Path | What it is |
| --- | --- |
| `docs/` | The published site: HTML and images only. GitHub Pages serves this folder. **Generated — do not edit.** |
| `pitch/` | Source for the two proposals (HTML + images; local PDFs are untracked) |
| `plan/` | Source for the two growth plans (HTML + images; local PDFs are untracked) |
| `build_site.py` | Assembles `docs/` from `pitch/` and `plan/` |
| `CREDITS.md` | Image sources and licences |

## Rebuilding

Edit the files in `pitch/` or `plan/`, then:

```bash
python3 build_site.py     # refreshes docs/
```

PDFs are deliberately not published or tracked. Regenerate one locally after
editing its HTML (WSL + Windows Chrome):

```bash
cd plan
"/mnt/c/Program Files/Google/Chrome/Application/chrome.exe" \
  --headless=new --no-pdf-header-footer --virtual-time-budget=15000 \
  --print-to-pdf="$(wslpath -w "$PWD/aashas-plan.pdf")" \
  "file:///$(wslpath -w "$PWD/aashas-plan.html")"
```

## Confidentiality

These documents carry commercial terms, rate cards and client business data.
`docs/robots.txt` and a `noindex` meta on every page keep the site out of search
engines, but **anyone with the link can read it.** The source `.docx` files, the
studio's own business plan and the client's original deck are excluded via
`.gitignore` and must not be committed.
