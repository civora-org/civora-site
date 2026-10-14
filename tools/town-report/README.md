# Town report ("Vaše mesto v číslach")

Generates one unlisted, static page per town from public CRZ data. Sales tooling for
civora-org/civora-platform#207. The pages are sent personally by the founder; nothing on
civora.sk links to them.

## Regenerate a page (one command per IČO)

```bash
python3 -I tools/town-report/town_report.py 00332933
```

This tops up the local CRZ cache, computes the stats, writes
`tools/town-report/data/<ico>.stats.json` and `r/<slug>/index.html`, and prints the slug.
The slug is minted once per IČO (80 random bits) and stored in `tools/town-report/slugs.json`,
so regenerating keeps the URL. Flags: `--no-sync` (use the cache as is), `--from-stats`
(re-render from the committed stats, no cache needed), `--months N`.

Python 3.9+, standard library only. Tests: `python3 -I -m unittest discover -s tools/town-report/tests`.

## Data

- Source: `datahub.ekosystem.slovensko.digital/api/data/crz/contracts/sync`, the same endpoint
  and fields the engine's `CrzImport::Client` uses. **The API has no per-IČO or per-date filter**
  (probed: `cin`, `contracting_authority_cin`, `ico`, `limit` are ignored; there is no list
  endpoint besides `sync`). The only way is to read the national feed from a start date, so
  `crawl.py` does it once for everybody: about 100 records a page, 60 requests a minute, roughly
  3 to 4 hours for 12 months. A new IČO then needs no new crawl, only a top-up of the newest pages.
- Cache: `~/.cache/civora-crz/` (or `$CIVORA_CRZ_CACHE`), outside the repository. It holds raw party
  names, so it is never committed. Resumable: kill and rerun, it continues from `cursor.txt`.
- Window: the last 12 complete calendar months before the data date.

## Privacy rules (enforced in `stats.py`, covered by tests)

- A counterparty is named only with a valid IČO and a legal-entity name marker (s. r. o., a. s.,
  obec, mesto, škola, ...). Sole traders (SZČO) are natural persons, so they and anyone without a
  marker are only counted in aggregates.
- Contract subjects are shown only next to a named legal entity, and are dropped when they look
  like they name a person.
- Committed `stats.json` files hold aggregates plus legal-entity names only.

## Unlisted pages

`r/<slug>/` with an unguessable slug, `<meta name="robots" content="noindex, nofollow, ...">`,
`Disallow: /r/` in `robots.txt`, not in `sitemap.xml`, not linked from `index.html`. The repository
is public, so this is "unlisted", not "private".

Hand-check notes live outside the repository (`VERIFY.md` in the planning scratch area).
