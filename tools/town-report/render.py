"""Render the unlisted town report page from a stats dict (no data fetching here)."""
import html
from datetime import date

NB = " "   # non-breaking space
MONTHS_GEN = ["januára", "februára", "marca", "apríla", "mája", "júna", "júla", "augusta", "septembra", "októbra", "novembra", "decembra"]
MONTHS_NOM = ["január", "február", "marec", "apríl", "máj", "jún", "júl", "august", "september", "október", "november", "december"]
CSS = open(__file__.replace("render.py", "report.css"), encoding="utf-8").read()


def e(s):
    return html.escape(str(s), quote=True)


def num(n):
    return f"{int(round(n)):,}".replace(",", NB)


def plural(n, one, few, many):
    n = abs(int(n))
    return one if n == 1 else few if 2 <= n <= 4 else many


def eur(n):
    n = float(n)
    if n >= 1_000_000:
        return f"{n / 1_000_000:.1f}".replace(".", ",") + f"{NB}mil.{NB}€"
    return f"{num(n)}{NB}€"


def eur_full(n):
    return f"{num(n)}{NB}€"


def d_sk(iso):
    y, m, d = iso.split("-")
    return f"{int(d)}.{NB}{int(m)}.{NB}{y}"


def days(x):
    if x is None:
        return "–"
    s = str(int(x)) if float(x).is_integer() else str(x).replace(".", ",")
    unit = "dňa" if not float(x).is_integer() else plural(x, "deň", "dni", "dní")
    return f"{s}{NB}{unit}"


def period(w):
    a, b = date.fromisoformat(w["from"]), date.fromisoformat(w["to"])
    return f"{MONTHS_NOM[a.month - 1]} {a.year} až {MONTHS_NOM[b.month - 1]} {b.year}"


def render(s, slug, demo_href):
    c, a, dl, sup = s["contracts"], s["amount"], s["delay"], s["suppliers"]
    town = s["town"]
    data_date = date.fromisoformat(s["data_date"])
    data_sk = f"{data_date.day}.{NB}{data_date.month}.{NB}{data_date.year}"
    per = period(s["window"])
    total = c["total"]
    maxc = max(t["contracts"] for t in s["trend"]) or 1

    facts = [
        (num(total), f"{plural(total, 'zmluva alebo dodatok', 'zmluvy alebo dodatky', 'zmlúv a dodatkov')} s mestom",
         f"Z toho {num(c['main'])} {plural(c['main'], 'zmluva', 'zmluvy', 'zmlúv')} a {num(c['amendments'])} {plural(c['amendments'], 'dodatok', 'dodatky', 'dodatkov')}. "
         f"Dodatky počítame zvlášť, lebo zvyčajne menia podmienky a nie cenu."),
        (eur(a["value_eur"]), "podpísaná hodnota zmlúv so sumou",
         f"{num(a['with_amount'])} {plural(a['with_amount'], 'zmluva', 'zmluvy', 'zmlúv')} s uvedenou sumou, medián {eur_full(a['median_eur'])}. "
         "Je to hodnota z textu zmlúv, nie ročné výdavky mesta. Zahŕňa aj príjmy, úvery či viacročné zmluvy."
         if a["with_amount"] else "Žiadna zmluva v tomto období nemá v CRZ uvedenú sumu."),
        (f"{a['no_amount_pct']}{NB}%" if a["no_amount_pct"] is not None else "–", "zmlúv bez uvedenej sumy",
         f"{num(a['no_amount'])} z {num(c['main'])} zmlúv (bez dodatkov). CRZ zapisuje sumu 0 € aj tam, kde ide o rámcovú, bezodplatnú alebo nájomnú zmluvu, "
         "takže to nie je chyba, ale je to miesto, kde sa dá zlepšiť čitateľnosť."),
        (days(dl["median_days"]), "medián od podpisu po zverejnenie",
         f"{dl['within_7_pct']}{NB}% zmlúv je zverejnených do 7 dní, {dl['over_30_pct']}{NB}% po viac ako 30 dňoch." if dl["n"] else ""),
    ]
    facts_html = "".join(f'<div class="fact"><dt>{e(lbl)}</dt><dd class="big">{n}</dd><dd class="note">{e(note)}</dd></div>'
                         for n, lbl, note in facts)

    rows = []
    for t in s["trend"]:
        w = round(100 * t["contracts"] / maxc)
        val = f" · {eur(t['value_eur'])}" if t["value_eur"] else ""
        rows.append(f'<tr><th scope="row">{e(t["label"])} {t["year"]}</th>'
                    f'<td><span class="bar" style="width:{max(w, 1) if t["contracts"] else 0}%"></span>'
                    f'<span class="barlabel">{num(t["contracts"])}<span class="val">{val}</span></span></td></tr>')
    trend_html = "".join(rows)

    top_rows = []
    for i, t in enumerate(s["top_contracts"], 1):
        who = e(t["counterparty"]) if t["counterparty"] else "Iná strana (nezobrazujeme)"
        what = e(t["subject"]) if t["subject"] else e(t["category"][0].upper() + t["category"][1:])
        crz = f"https://www.crz.gov.sk/zmluva/{t['id']}/"
        top_rows.append(
            f'<tr><td class="rank">{i}</td><td class="what"><span class="subject">{what}</span>'
            f'<span class="who">{who} · {d_sk(t["signed_on"])}</span></td>'
            f'<td class="amt">{eur_full(t["amount_eur"])}</td>'
            f'<td class="crz"><a href="{crz}" rel="noreferrer noopener">CRZ<span class="sr"> – zmluva č. {t["id"]}</span></a></td></tr>')

    sup_rows = "".join(
        f'<tr><td class="what"><span class="subject">{e(x["name"])}</span><span class="who">IČO {e(x["ico"])}</span></td>'
        f'<td class="n">{num(x["contracts"])}</td><td class="amt">{eur_full(x["value_eur"])}</td></tr>' for x in sup["top"])
    sup_block = (f'<table class="data"><caption class="sr">Najväčší dodávatelia podľa hodnoty zmlúv</caption><thead><tr><th scope="col">Zmluvná strana</th><th scope="col" class="n">Zmlúv</th>'
                 f'<th scope="col" class="amt">Hodnota</th></tr></thead><tbody>{sup_rows}</tbody></table>') if sup["top"] else "<p>V tomto období nie je dostatok zmlúv s právnickými osobami.</p>"

    title = f"{town} v číslach"
    desc = f"Prehľad zmlúv mesta v Centrálnom registri zmlúv, {per}."
    dups = f" (odstránených {num(c['duplicates_removed'])})" if c.get("duplicates_removed") else ""
    return f"""<!doctype html>
<html lang="sk">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)} · Civora</title>
<meta name="description" content="{e(desc)}">
<meta name="robots" content="noindex, nofollow, noarchive, nosnippet, noimageindex">
<meta name="googlebot" content="noindex, nofollow">
<meta name="referrer" content="no-referrer">
<meta name="theme-color" content="#0b5cad">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="preload" href="/fonts/source-sans-3-latin-400.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/fonts/source-sans-3-latin-700.woff2" as="font" type="font/woff2" crossorigin>
<style>
{CSS}
</style>
</head>
<body>
<a class="skip" href="#obsah">Preskočiť na obsah</a>
<header class="top wrap">
  <a class="brand" href="https://civora.sk/" rel="noreferrer"><svg viewBox="0 0 28 28" aria-hidden="true" focusable="false"><rect width="28" height="28" rx="6" fill="#0b5cad"/><path d="M8 14.5l4 4 8-9" fill="none" stroke="#fff" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/></svg>Civora</a>
  <p class="meta">Pripravené pre mesto · údaje k {data_sk}</p>
</header>
<main id="obsah" class="wrap">
  <section class="intro">
    <h1>{e(town)} v&nbsp;číslach</h1>
    <p class="lead">Za {s['window']['months']} mesiacov ({e(per)}) bolo v&nbsp;Centrálnom registri zmlúv zverejnených {num(total)} {plural(total, 'zmluva alebo dodatok', 'zmluvy alebo dodatky', 'zmlúv a dodatkov')}, pri ktorých je {e(town)} zmluvnou stranou.
    Pripravili sme prehľad z&nbsp;verejných údajov, aby bolo vidieť, čo sa z&nbsp;nich dá jednoducho prečítať.</p>
  </section>

  <section aria-labelledby="h-cisla">
    <h2 id="h-cisla">Štyri čísla</h2>
    <dl class="facts">{facts_html}</dl>
  </section>

  <section aria-labelledby="h-mesiace">
    <h2 id="h-mesiace">Zmluvy po mesiacoch</h2>
    <p class="sub">Podľa dátumu podpisu. Dĺžka pruhu zodpovedá počtu zmlúv a dodatkov, vedľa je podpísaná hodnota zmlúv so sumou.</p>
    <table class="trend"><caption class="sr">Počet zmlúv a dodatkov podľa mesiaca podpisu</caption>
    <thead class="sr"><tr><th scope="col">Mesiac</th><th scope="col">Počet zmlúv a hodnota</th></tr></thead><tbody>{trend_html}</tbody></table>
  </section>

  <section aria-labelledby="h-top">
    <h2 id="h-top">Desať najväčších zmlúv podľa sumy</h2>
    <p class="sub">Bez dodatkov. Zmluvnú stranu uvádzame len pri právnických osobách. Každá zmluva odkazuje na originál v CRZ.</p>
    <table class="data"><caption class="sr">Desať zmlúv s najvyššou sumou</caption>
    <thead class="sr"><tr><th scope="col">Poradie</th><th scope="col">Predmet a zmluvná strana</th><th scope="col">Suma</th><th scope="col">Odkaz</th></tr></thead><tbody>{''.join(top_rows)}</tbody></table>
  </section>

  <section aria-labelledby="h-dod">
    <h2 id="h-dod">Najväčšie zmluvné strany</h2>
    <p class="sub">Dodávatelia, ale aj poskytovatelia dotácií a úverov. Zoradené podľa podpísanej hodnoty zmlúv, bez dodatkov. Uvádzame iba právnické osoby s IČO.
    {num(sup['aggregated_contracts'])} z&nbsp;{num(sup['main_contracts'])} zmlúv (fyzické osoby, živnostníci a strany bez IČO) zobrazujeme len súhrnne.</p>
    {sup_block}
  </section>

  <section class="next no-print" aria-labelledby="h-dalej">
    <h2 id="h-dalej">Čo s tým ďalej</h2>
    <p>Tieto čísla nehodnotia prácu úradu. Suma 0&nbsp;€ je pri rámcových, nájomných či bezodplatných zmluvách bežná a zverejnenie do niekoľkých dní je v&nbsp;poriadku. Zaujímavé sú otázky, na ktoré sa dá odpovedať rýchlo: ktoré zmluvy nemajú sumu a prečo, ako dlho trvá cesta od podpisu po zverejnenie, čo sa zverejnilo minulý mesiac.</p>
    <p>Civora Zmluvy drží celý postup (návrh, kontrolu, zverejnenie a prepojenie na CRZ) na jednom mieste, takže tieto odpovede sú po ruke.</p>
    <p><a class="btn" href="{e(demo_href)}">Takto by to vyzeralo u&nbsp;vás</a></p>
  </section>

  <section class="method" aria-labelledby="h-metoda">
    <h2 id="h-metoda">Ako sme to počítali</h2>
    <ul>
      <li><strong>Zdroj.</strong> Centrálny register zmlúv (crz.gov.sk) v&nbsp;podobe otvorených údajov na ekosystem.slovensko.digital. Údaje sú k&nbsp;{data_sk}.</li>
      <li><strong>Obdobie.</strong> Zmluvy podpísané od {d_sk(s['window']['from'])} do {d_sk(s['window']['to'])} (posledných {s['window']['months']} úplných mesiacov). Zmluva sa počíta, ak je {e(town)} (IČO {e(s['ico'])}) ktoroukoľvek stranou. Mestské firmy a rozpočtové organizácie majú vlastné IČO a nie sú zahrnuté.</li>
      <li><strong>Dvojité záznamy.</strong> CRZ vedie záznam od každej zverejňujúcej strany. Ak tú istú zmluvu zverejnili obe strany (rovnaká zmluvná strana, dátum podpisu a suma), počítame ju raz{dups}.</li>
      <li><strong>Dodatky</strong> poznáme podľa slova „dodatok“ v&nbsp;predmete zmluvy, lebo označenie druhu v&nbsp;zdroji nie je spoľahlivé. Môže ich byť o niečo viac či menej.</li>
      <li><strong>Suma.</strong> Berieme sumu zo zmluvy zapísanú v&nbsp;CRZ. CRZ nerozlišuje „nie je známa“, „bezodplatné“ a „0 €“, preto „bez sumy“ znamená, že suma je 0 € alebo chýba. Sumy sa nerozpočítavajú na roky a nie sú audit hospodárenia.</li>
      <li><strong>Zverejnenie.</strong> Rozdiel medzi dátumom podpisu a dátumom zverejnenia v&nbsp;CRZ, medián zo všetkých {num(dl['n'])} {plural(dl['n'], 'zmluvy', 'zmlúv', 'zmlúv')} so známym dátumom. Čerstvo podpísané zmluvy nemusia byť ešte zverejnené.</li>
      <li><strong>Mená.</strong> Zmluvné strany pomenúvame len vtedy, keď ide o právnickú osobu s IČO. Živnostníci sú fyzické osoby, preto sa spolu s ostatnými fyzickými osobami ukazujú len v&nbsp;súčtoch.</li>
    </ul>
  </section>
</main>
<footer class="wrap">
  <p class="attr">Zdroj údajov: Centrálny register zmlúv Slovenskej republiky, sprístupnený cez <a href="https://ekosystem.slovensko.digital/" rel="noreferrer noopener">ekosystem.slovensko.digital</a> pod licenciou <a href="https://creativecommons.org/licenses/by/4.0/deed.sk" rel="noreferrer noopener">CC BY 4.0</a>. Výpočty a spracovanie: Civora.</p>
  <p class="contact">Denys Kozlov · <a href="mailto:denys@civora.sk">denys@civora.sk</a> · <a href="tel:+421944926570">+421{NB}944{NB}926{NB}570</a></p>
</footer>
</body>
</html>
"""
