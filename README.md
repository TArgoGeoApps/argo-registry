# The Argo Registry

The public book of a closed series. This repository is the registry's complete
machinery: the master ledger, the site builder, and the published page.

**Status: pre-launch.** The ledger holds specimen data and the site is marked
DESIGN MOCKUP. Nothing is public until GitHub Pages is switched on.

---

## How it works

```
ledger/ledger.json          THE MASTER LEDGER — the single source of truth.
                            Every serial, status, census count, series, and
                            authorization. Edit this file and nothing else.

templates/registry.html     The registry page design. Rarely changes.

scripts/build.py            The typesetter. Reads the ledger, writes the
                            registry page.

docs/index.html             THE FRONT DOOR — the minimal house page. Emblem,
                            motto, and two pointers: the registry and the
                            authorized jeweler. Edited by hand, rarely.

docs/registry/index.html    THE REGISTRY — generated from the ledger,
                            never hand-edited.
```

One site, two pages. Every domain the house owns points here; one domain is
canonical (the one printed on certificates) and the others redirect to it.
The site deliberately sells nothing — buying happens at the authorized
jeweler; verifying happens in the registry.

Change the ledger → commit → the build runs automatically → `docs/index.html`
updates. Every change is a git commit: timestamped, attributed, permanent.
**That history is the audit trail the CPA examines.**

## The rules of the book

1. **One keyholder writes.** Only the house commits to this repository.
2. **Corrections are new entries, never silent edits.** If a record was wrong,
   the correcting commit says so in its message. History is never rewritten.
3. **The jeweler reports; the house records.** Authorized jewelers submit
   events (a sale, a setting, a transfer verification) through the agreed
   channel. They do not have access to this repository.
4. **The CPA reads everything** — the ledger, the site, and the full commit
   history — and attests annually.
5. **The design of the cut appears nowhere in this repository, ever.**
   No angles, no proportions, no scan files, no geometry. The registry
   records standing, not design.

## Going live (launch day checklist)

1. Replace specimen data in `ledger/ledger.json` with the first true records
   (the demonstration stone's actual report numbers; the real ceilings).
2. Set `"mode": "live"` in the ledger's `meta` (removes the mockup badge and
   the registry page's noindex tag), and delete the `noindex` meta line from
   `docs/index.html` (marked with a PRE-LAUNCH comment)
   and update `census_note`, `footer_note`, and `lookup_hint` to live wording.
3. Commit. Confirm the build updated `docs/index.html`.
4. Make the repository **public** (Settings → General → Danger Zone), or keep
   it private and deploy `docs/` via Cloudflare Pages instead.
5. Switch on **GitHub Pages**: Settings → Pages → Deploy from a branch →
   `main` / `docs`.
6. Point the domains (the house owns three):
   - **argodiamond.com** — canonical. Add a file `docs/CNAME` containing
     `argodiamond.com`, commit, then at the registrar set GitHub Pages DNS
     (four A records for the apex: 185.199.108.153 / .109. / .110. / .111.,
     plus a CNAME `www` → `<username>.github.io`). HTTPS is automatic.
   - **argoregistry.com** — registrar "domain forwarding" →
     `https://argodiamond.com/registry` (301 permanent). This is the URL
     printed on certificates.
   - **theargostar.com** — registrar forwarding → `https://argodiamond.com`
     (301 permanent). Matches the Instagram handle.
   All three: WHOIS privacy on, AUTO-RENEW LOCKED, credentials sealed in the
   vault with the hard-copy records.
7. Verify the live site, then record the go-live date in the ledger.

## Local build

```
python3 scripts/build.py
```

No dependencies beyond Python 3.
