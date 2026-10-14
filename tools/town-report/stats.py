"""Aggregate one town's CRZ contracts from the local cache into a stats dict.

Privacy rules enforced here, not in the template:
  * a counterparty is NAMED only when it has a valid 8-digit IČO AND its name
    carries a legal-entity marker. Sole traders (SZČO) are natural persons, so
    "Ján Novák - SERVIS" is not named even though it has an IČO;
  * rows whose counterparty is not named never show their subject (subjects of
    contracts with private persons can contain names and addresses);
  * everything not named is only counted, in aggregate.
"""
import json
import math
import os
import re
import statistics
import unicodedata
from collections import Counter, defaultdict
from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo

import crawl

TZ = ZoneInfo("Europe/Bratislava")
MONTHS_SK = ["január", "február", "marec", "apríl", "máj", "jún", "júl", "august", "september", "október", "november", "december"]


def norm(s):
    s = unicodedata.normalize("NFKD", (s or "").lower())
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", s).strip()


def ico_of(cin, raw):
    """8-digit IČO or None (the API returns the number; `raw` is the source text)."""
    if isinstance(cin, int) and 0 < cin < 10**8:
        return "%08d" % cin
    digits = re.sub(r"\s+", "", str(raw or ""))
    return digits.zfill(8) if digits.isdigit() and 0 < len(digits) <= 8 else None


# --- legal entity vs natural person -----------------------------------------
STRONG = re.compile(r"\bs\. ?r\. ?o\b|spol\. ?s r|\ba\. ?s\b|\bk\. ?s\b|\bv\. ?o\. ?s\b|\bs\. ?p\b|\bo\. ?z\b|\bn\. ?o\b|\bn\. ?f\b|"
                    r"akciov|druzstvo|\bse\b$|\bs\.r\.o", re.I)
INSTITUTION = re.compile(r"\b(obec|mesto|mestsk\w+|ministerstvo|urad|sprava|agentura|fond|skola|skolsk\w+|gymnazium|univerzita|"
                         r"nemocnica|poliklinika|kraj|zdruzenie|spolok|zvaz|centrum|institut|komora|nadacia|cirkev|farnost|"
                         r"republika|statny|statna|slovensk\w+|riaditelstvo|inspektorat|zbor|organizacia|podnik|"
                         r"arcidiecez\w*|arcibiskupstvo|biskupstvo|diecez\w*|banka|poistovna|dobrovolny|hasicsky|vodarne|energetika|distribucia|telekom|posta)\b")
TITLE = r"(?:Ing\.|Mgr\.|MUDr\.|JUDr\.|PhDr\.|PaedDr\.|RNDr\.|Bc\.|Dr\.|doc\.|prof\.)"
PERSON_SHAPE = re.compile(rf"^(?:{TITLE}\s+)*[A-ZÁÄČĎÉÍĹĽŇÓÔŔŠŤÚÝŽ][a-záäčďéíĺľňóôŕšťúýž'-]+(?:\s+[A-ZÁÄČĎÉÍĹĽŇÓÔŔŠŤÚÝŽ][a-záäčďéíĺľňóôŕšťúýž'-]+){{1,2}}(?:\s*[,-].*)?$")


def is_legal_entity(name, ico):
    """True only for a named party that has an IČO and looks like an organisation."""
    if not ico or not name:
        return False
    n = norm(name)
    if STRONG.search(n):
        return True
    if INSTITUTION.search(n):
        # an institution word buried after a person-shaped prefix ("Ján Novák - Centrum")
        # is a sole trader's trade name, not an organisation
        first = INSTITUTION.search(n).start()
        if first > 0 and PERSON_SHAPE.match(name.strip()):
            return False
        return True
    return False


# --- subject handling --------------------------------------------------------
AMENDMENT = re.compile(r"\bdodat", re.I)
CATEGORIES = [("dodatok k zmluve", r"\bdodat"), ("rámcová dohoda", r"ramcov"),
              ("nájom", r"najom|najm[eu]|najomn|prenajm|prenajom|hrobov|pohrebisk"),
              ("kúpa alebo predaj", r"kupn|predaj|kupa\b"), ("darovanie alebo bezodplatné užívanie", r"darovac|bezodplat|bezplatn|vypozick"),
              ("vecné bremeno", r"vecn\w* brem"), ("dotácia alebo príspevok", r"dotaci|prispevok|prispevku|grant"),
              ("zmluva o dielo", r"o dielo|stavebn|rekonstruk"), ("úver alebo financovanie", r"uver|financn|leasing"),
              ("služby alebo dodávka", r"sluzb|servis|dodavk|dodani|poskytovani|poskytnuti")]


def category(subject):
    s = norm(subject)
    for label, rx in CATEGORIES:
        if re.search(rx, s):
            return label
    return "zmluva (iný predmet)"


PERSONISH_SUBJECT = re.compile(rf"{TITLE}\s+[A-ZÁÄČĎÉÍĹĽŇÓÔŔŠŤÚÝŽ][a-záäčďéíĺľňóôŕšťúýž]+|\b[A-ZÁÄČĎÉÍĹĽŇÓÔŔŠŤÚÝŽ][a-záäčďéíĺľňóôŕšťúýž]+\s+[A-ZÁÄČĎÉÍĹĽŇÓÔŔŠŤÚÝŽ][a-záäčďéíĺľňóôŕšťúýž]+(?:ová|ova|ská|cká)\b|nar\.|rod\.|r\.č\.|rodné číslo", re.U)


def safe_subject(subject, limit=110):
    """The contract subject, shortened; None when it looks like it names a person."""
    s = re.sub(r"\s+", " ", (subject or "")).strip()
    if not s or PERSONISH_SUBJECT.search(s):
        return None
    return s if len(s) <= limit else s[: limit - 1].rsplit(" ", 1)[0] + "…"


def amount(r):
    try:
        return float(r["amount"])
    except (TypeError, ValueError):
        return None


def pub_date(r):
    try:
        return datetime.fromisoformat(r["published_at"].replace("Z", "+00:00")).astimezone(TZ).date()
    except Exception:
        return None


def window(synced_on, months=12):
    """The last `months` COMPLETE calendar months before the data date."""
    end = synced_on.replace(day=1) - timedelta(days=1)
    y, m = end.year, end.month - (months - 1)
    while m < 1:
        m += 12
        y -= 1
    return date(y, m, 1), end


def load_cache():
    d = crawl.cache_dir()
    rows = {}
    with open(os.path.join(d, "contracts.jsonl")) as f:
        for line in f:
            r = json.loads(line)
            rows[r["id"]] = r  # later line wins
    meta = json.load(open(os.path.join(d, "meta.json")))
    return rows, meta


def dedupe(rows):
    """CRZ holds one record per publishing party, so a contract both sides published appears twice
    (same counterparty, signing date and amount). Count it once; keep the lowest id.
    Zero-amount contracts need the same subject text too, otherwise unrelated ones would merge."""
    seen, kept = {}, []
    for r in sorted(rows, key=lambda r: r["id"]):
        a = amount(r) or 0
        who = r["_other"][1] or norm(r["_other"][0])
        if not r["_other"][1] and (not who or re.match(r"(fyzick|nezverej|bez |anonym)", who)):
            kept.append(r)  # redacted party ("fyzická osoba"): unrelated people look identical, never merge
            continue
        key = (who, r["signed_on"], a) if a > 0 else (who, r["signed_on"], 0, norm(r["subject"]))
        if key in seen:
            continue
        seen[key] = True
        kept.append(r)
    return kept, len(rows) - len(kept)


def compute(ico, rows, meta, months=12):
    synced_on = datetime.fromisoformat(meta["synced_at"]).astimezone(TZ).date() if meta.get("synced_at") else date.today()
    start, end = window(synced_on, months)
    mine, names = [], Counter()
    for r in rows.values():
        ca, sup = ico_of(r["ca_cin"], r["ca_cin_raw"]), ico_of(r["sup_cin"], r["sup_cin_raw"])
        if ico not in (ca, sup):
            continue
        if not r["signed_on"] or not (start.isoformat() <= r["signed_on"] <= end.isoformat()):
            continue
        other = (r["sup_name"], sup) if ca == ico else (r["ca_name"], ca)
        other = (re.sub(r"\s+", " ", other[0] or "").strip(), other[1])
        names[(r["ca_name"] if ca == ico else r["sup_name"]).strip()] += 1
        mine.append(dict(r, _other=other))
    mine, duplicates = dedupe(mine)
    if not mine:
        raise SystemExit(f"No contracts for IČO {ico} in {start}..{end}: wrong IČO or cache not synced.")

    amend = [r for r in mine if AMENDMENT.search(norm(r["subject"]))]
    main = [r for r in mine if not AMENDMENT.search(norm(r["subject"]))]
    amt = {id(r): amount(r) for r in main}
    with_amt = [r for r in main if (amt[id(r)] or 0) > 0]
    no_amt = len(main) - len(with_amt)
    value = sum(amt[id(r)] for r in with_amt)

    # monthly trend (all contracts, amendments included)
    per_month = Counter(r["signed_on"][:7] for r in mine)
    val_month = defaultdict(float)
    for r in with_amt:
        val_month[r["signed_on"][:7]] += amt[id(r)]
    trend, y, m = [], start.year, start.month
    for _ in range(months):
        k = f"{y}-{m:02d}"
        trend.append({"month": k, "label": MONTHS_SK[m - 1], "year": y, "contracts": per_month.get(k, 0), "value_eur": round(val_month.get(k, 0))})
        m += 1
        if m > 12:
            m, y = 1, y + 1

    # publication delay (signing -> publication in CRZ), whole contracts incl. amendments
    delays = []
    for r in mine:
        p = pub_date(r)
        if p:
            delays.append((p - date.fromisoformat(r["signed_on"])).days)
    delay = {"n": len(delays), "median_days": statistics.median(delays) if delays else None,
             "within_7_pct": round(100 * sum(0 <= d <= 7 for d in delays) / len(delays)) if delays else None,
             "over_30_pct": round(100 * sum(d > 30 for d in delays) / len(delays)) if delays else None}

    # top 10 by signed value (non-amendments); counterparty named only if a legal entity
    top = []
    for r in sorted(with_amt, key=lambda r: -amt[id(r)])[:10]:
        nm, oi = r["_other"]
        named = is_legal_entity(nm, oi)
        subj = safe_subject(r["subject"]) if named else None
        top.append({"id": r["id"], "signed_on": r["signed_on"], "amount_eur": round(amt[id(r)]),
                    "counterparty": nm if named else None, "counterparty_ico": oi if named else None,
                    "subject": subj, "category": category(r["subject"])})

    # largest counterparties: named legal entities with an IČO (a lender or grant giver counts too)
    by_sup, hidden_n, shown_n = {}, 0, 0
    for r in main:
        nm, oi = r["_other"]
        if is_legal_entity(nm, oi):
            shown_n += 1
            x = by_sup.setdefault(oi, {"name": nm, "ico": oi, "contracts": 0, "value_eur": 0.0})
            x["contracts"] += 1
            x["value_eur"] += amt[id(r)] or 0
        else:
            hidden_n += 1
    suppliers = sorted(by_sup.values(), key=lambda x: (-x["value_eur"], -x["contracts"]))[:5]
    for x in suppliers:
        x["value_eur"] = round(x["value_eur"])

    return {
        "ico": ico, "town": names.most_common(1)[0][0].strip(),
        "window": {"from": start.isoformat(), "to": end.isoformat(), "months": months},
        "data_date": synced_on.isoformat(),
        "contracts": {"total": len(mine), "amendments": len(amend), "main": len(main), "duplicates_removed": duplicates},
        "amount": {"with_amount": len(with_amt), "value_eur": round(value), "no_amount": no_amt,
                   "no_amount_pct": round(100 * no_amt / len(main)) if main else None,
                   "median_eur": round(statistics.median([amt[id(r)] for r in with_amt])) if with_amt else None},
        "delay": delay, "trend": trend, "top_contracts": top,
        "suppliers": {"top": suppliers, "main_contracts": len(main), "named_contracts": shown_n, "aggregated_contracts": hidden_n},
    }
