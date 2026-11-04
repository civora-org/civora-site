#!/usr/bin/env python3
"""One command per IČO: top up the CRZ cache, compute the stats, write the page.

    python3 -I tools/town-report/town_report.py 00332933

Writes (repository root = two levels above this file):
    tools/town-report/data/<ico>.stats.json   aggregates only, no personal names
    r/<slug>/index.html                       the unlisted page (slug minted once,
                                              kept in tools/town-report/slugs.json)

Options:
    --no-sync     use the cache as it is (fast; for rebuilding)
    --from-stats  re-render from the committed stats.json, no cache needed
    --months N    window length in complete months (default 12)
    --demo-href   target of the closing "Takto by to vyzeralo u vás" link
"""
import argparse
import json
import os
import re
import secrets
import sys
from datetime import date, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import crawl, render, stats  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(HERE))
SLUGS = os.path.join(HERE, "slugs.json")
DEMO = "mailto:denys@civora.sk?subject=Ukážka%20Civora%20Zmluvy%20pre%20{town}"


def slug_for(ico):
    slugs = json.load(open(SLUGS)) if os.path.exists(SLUGS) else {}
    if ico not in slugs:
        slugs[ico] = secrets.token_hex(10)  # 80 bits, unguessable; minted once, then stable
        json.dump(slugs, open(SLUGS, "w"), indent=2, sort_keys=True)
        open(SLUGS, "a").write("\n")
    return slugs[ico]


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("ico")
    ap.add_argument("--no-sync", action="store_true")
    ap.add_argument("--from-stats", action="store_true")
    ap.add_argument("--months", type=int, default=12)
    ap.add_argument("--demo-href")
    a = ap.parse_args(argv)
    ico = re.sub(r"\s+", "", a.ico).zfill(8)
    if not re.fullmatch(r"\d{8}", ico):
        sys.exit("IČO must be 8 digits")
    stats_path = os.path.join(HERE, "data", f"{ico}.stats.json")

    if a.from_stats:
        s = json.load(open(stats_path))
    else:
        if not a.no_sync:
            start, _ = stats.window(date.today(), a.months)
            if not crawl.sync(f"{start.isoformat()}T00:00:00Z"):
                sys.exit("Crawl not finished (feed is slow, 60 req/min). Rerun the same command to resume.")
        rows, meta = stats.load_cache()
        s = stats.compute(ico, rows, meta, a.months)
        os.makedirs(os.path.dirname(stats_path), exist_ok=True)
        json.dump(s, open(stats_path, "w"), ensure_ascii=False, indent=2)
        open(stats_path, "a").write("\n")

    slug = slug_for(ico)
    demo = (a.demo_href or DEMO).format(town=s["town"].replace(" ", "%20"))
    out = os.path.join(ROOT, "r", slug, "index.html")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, "w", encoding="utf-8").write(render.render(s, slug, demo))
    print(f"{s['town']} ({ico}): {s['contracts']['total']} contracts -> /r/{slug}/")


if __name__ == "__main__":
    main()
