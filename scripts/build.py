#!/usr/bin/env python3
"""The Argo Registry — site builder.

Reads  ledger/ledger.json  (the master ledger, the single source of truth)
and    templates/registry.html
and writes  docs/registry/index.html  (the published registry page).

The ledger is the book. This script only typesets it.
Corrections are new ledger entries — never silent edits. Every change to the
ledger is a git commit: timestamped, attributed, and preserved forever. That
history is the audit trail.
"""
import json, html, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
ledger = json.loads((ROOT / "ledger" / "ledger.json").read_text(encoding="utf-8"))
tpl = (ROOT / "templates" / "registry.html").read_text(encoding="utf-8")

meta = ledger["meta"]

def esc(s):
    return html.escape(s, quote=False)

# --- badge (mockup mode shows the specimen badge; live mode shows nothing) ---
noindex = (
    '\n<meta name="robots" content="noindex">'
    if meta.get("mode") == "mockup" else ""
)

badge = (
    f'<div class="mockbadge">{esc(meta["badge"])}</div>'
    if meta.get("badge") else ""
)

# --- series cards ---
series_cards = "\n".join(
    f'    <div class="covcard"><div class="t">{esc(c["title"])}</div>\n'
    f'      <div class="d">{esc(c["body"])}</div></div>'
    for c in ledger["series_cards"]
)

# --- census rows ---
census_rows = "\n".join(
    f'    <tr><td>{esc(r["series"])}</td>'
    f'<td class="num">{esc(r.get("opens","—"))}</td>'
    f'<td class="num">{esc(r["issued"])}</td>'
    f'<td class="num">{esc(r["reserved"])}</td>'
    f'<td class="num">{esc(r["retired"])}</td>'
    f'<td class="num">{esc(r["demo"])}</td>'
    f'<td class="num">{esc(r["ceiling"])}</td></tr>'
    for r in ledger["census"]
)

# --- authorization cards ---
auth_cards = "\n".join(
    f'    <div class="covcard"><div class="t">{esc(a["title"])}</div>\n'
    f'      <div class="d" style="font-size:16px;color:var(--gold-pale)">{esc(a["body"])}</div></div>'
    for a in ledger["authorizations"]
)

out = (
    tpl.replace("%NOINDEX%", noindex)
       .replace("%BADGE%", badge)
       .replace("%LOOKUP_HINT%", meta["lookup_hint"])
       .replace("%SERIES_CARDS%", series_cards)
       .replace("%CENSUS_ROWS%", census_rows)
       .replace("%CENSUS_NOTE%", esc(meta["census_note"]))
       .replace("%AUTH_CARDS%", auth_cards)
       .replace("%FOOTER_NOTE%", esc(meta["footer_note"]))
       .replace("%REC_JSON%", json.dumps(ledger["stones"], ensure_ascii=False))
)

for marker in ("%NOINDEX%", "%BADGE%", "%LOOKUP_HINT%", "%SERIES_CARDS%", "%CENSUS_ROWS%",
               "%CENSUS_NOTE%", "%AUTH_CARDS%", "%FOOTER_NOTE%", "%REC_JSON%"):
    if marker in out:
        sys.exit(f"build failed: unresolved marker {marker}")

(ROOT / "docs" / "registry").mkdir(parents=True, exist_ok=True)
(ROOT / "docs" / "registry" / "index.html").write_text(out, encoding="utf-8")
print("built docs/registry/index.html from ledger (mode: %s, as of %s)" % (meta.get("mode"), meta.get("as_of")))
