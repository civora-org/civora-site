#!/usr/bin/env python3
"""Resumable crawl of the ekosystem.slovensko.digital CRZ sync feed.

The datahub has no per-IČO or per-date filter: the only list endpoint is
`/api/data/crz/contracts/sync?since=<updated-since>` (cursor-paginated, 100 rows
a page, ordered by update time, `Link: rel='next'` cursor). Everything the API
offers is followed here exactly as the engine's CrzImport::Client does, so one
crawl of the last ~12 months serves EVERY town (a new IČO needs no new crawl,
only a top-up of the newest pages).

Cache (outside the repository, it holds raw party names):
  $CIVORA_CRZ_CACHE or ~/.cache/civora-crz/
    contracts.jsonl   compact records, append-only (later line wins per id)
    cursor.txt        the next URL to fetch, verbatim from the Link header
    meta.json         since / last_changed_at / pages / records / synced_at

Limits: 60 requests/min -> >= 1.1 s between requests; 429 sleeps 65 s; 5xx and
network errors back off. Only counts are logged, never payloads.
"""
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone

BASE = "https://datahub.ekosystem.slovensko.digital/api/data/crz/contracts/sync"
PAUSE = 1.1
UA = "civora-town-report/1.0 (contact: denys@civora.sk)"


def cache_dir():
    d = os.environ.get("CIVORA_CRZ_CACHE") or os.path.expanduser("~/.cache/civora-crz")
    os.makedirs(d, exist_ok=True)
    return d


def compact(r):
    """The subset of the payload the report needs."""
    return {
        "id": r.get("id"),
        "subject": r.get("subject"),
        "signed_on": r.get("signed_on"),
        "published_at": r.get("published_at"),
        "changed_at": r.get("changed_at"),
        "amount": r.get("contract_price_amount"),
        "total_amount": r.get("contract_price_total_amount"),
        "ca_name": r.get("contracting_authority_name"),
        "ca_cin": r.get("contracting_authority_cin"),
        "ca_cin_raw": r.get("contracting_authority_cin_raw"),
        "sup_name": r.get("supplier_name"),
        "sup_cin": r.get("supplier_cin"),
        "sup_cin_raw": r.get("supplier_cin_raw"),
        "kind_id": r.get("kind_id"),
        "contract_identifier": r.get("contract_identifier"),
    }


def fetch(url):
    attempt = 0
    while True:
        attempt += 1
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=90) as resp:
                return json.load(resp), resp.headers.get("Link")
        except urllib.error.HTTPError as e:
            wait = 65 if e.code == 429 else min(5 * attempt, 60)
            print(f"HTTP {e.code}; sleep {wait}s (attempt {attempt})", file=sys.stderr, flush=True)
            if e.code == 404 or attempt > 12:
                raise
            time.sleep(wait)
        except Exception as e:  # transport errors, bad JSON
            wait = min(5 * attempt, 60)
            print(f"{type(e).__name__}; sleep {wait}s (attempt {attempt})", file=sys.stderr, flush=True)
            if attempt > 12:
                raise
            time.sleep(wait)


def next_link(link):
    m = re.search(r"<([^>]+)>\s*;\s*rel=[\"']?next[\"']?", link or "", re.I)
    return m.group(1) if m else None


def sync(since, max_seconds=None, quiet=False):
    """Crawl (or resume) until the feed is exhausted or max_seconds elapse.
    Returns True when the feed was exhausted (cache is current)."""
    d = cache_dir()
    data_path, cursor_path, meta_path = (os.path.join(d, n) for n in ("contracts.jsonl", "cursor.txt", "meta.json"))
    meta = json.load(open(meta_path)) if os.path.exists(meta_path) else {"since": since, "pages": 0, "records": 0}
    if os.path.exists(cursor_path):
        url = open(cursor_path).read().strip()
        since = meta.get("since", since)
        print("resuming from saved cursor", file=sys.stderr, flush=True)
    else:
        url = BASE + "?" + urllib.parse.urlencode({"since": since})
        meta["since"] = since
    deadline = time.time() + max_seconds if max_seconds else None
    exhausted = False
    with open(data_path, "a") as out:
        while True:
            if deadline and time.time() > deadline:
                break
            records, link = fetch(url)
            for r in records:
                out.write(json.dumps(compact(r), ensure_ascii=False) + "\n")
            out.flush()
            meta["pages"] += 1
            meta["records"] += len(records)
            if records:
                meta["last_changed_at"] = records[-1].get("changed_at") or meta.get("last_changed_at")
            nxt = next_link(link)
            if not records or not nxt:
                exhausted = True
                meta["synced_at"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
                json.dump(meta, open(meta_path, "w"))
                break
            url = nxt
            tmp = cursor_path + ".tmp"
            open(tmp, "w").write(url)
            os.replace(tmp, cursor_path)  # atomic: a kill never leaves a half cursor
            json.dump(meta, open(meta_path, "w"))
            if meta["pages"] % 25 == 0 and not quiet:
                print(f"pages={meta['pages']} records={meta['records']} last_changed={meta.get('last_changed_at')}", file=sys.stderr, flush=True)
            time.sleep(PAUSE)
    return exhausted


if __name__ == "__main__":
    since = sys.argv[1] if len(sys.argv) > 1 else "2025-10-01T00:00:00Z"
    done = sync(since, float(os.environ["MAX_SECONDS"]) if os.environ.get("MAX_SECONDS") else None)
    print("CURRENT" if done else "PARTIAL (rerun to resume)", file=sys.stderr)
