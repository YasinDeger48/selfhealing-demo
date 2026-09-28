"""Builds the LinkedIn carousel (PDF) and the single pictures (PNG) in English and Turkish.

    python build.py                                                  (slides as HTML)
    cd capture && mvn -q compile exec:java -Dexec.mainClass=linkedin.Render   (-> ../images/<lang>/*.png, ../carousel/*.pdf)

Every number on the slides comes from the framework's own measurements (README "Measured accuracy", the
compatibility matrix RESULTS.md) and every screenshot from a real run (capture/).
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LINKEDIN = os.path.dirname(HERE)
OUT = os.path.join(HERE, "graphics", "out")
REPO = "github.com/YasinDeger48/selfhealing-framework"


def img(name):
    return "../../../../images/" + name   # from graphics/out/<lang>/


TEXT = {
    "en": {
        "footer": "Self-healing locators for Playwright &amp; Selenium",
        "cover": ("Open source · Java", "Your locator broke.<br><span class='green'>Your test didn't.</span>",
                  "A self-healing layer for Playwright and Selenium tests: when the markup changes, it finds the element "
                  "again, keeps the test running and tells you exactly what to fix."),
        "problem": ("The problem", "A renamed id should not cost you a red build.",
                    "A release renames <code>#login-username</code> to <code>#user-name</code>. Nothing is broken for "
                    "the user - but every test that touches the login fails, and someone spends the morning updating "
                    "page objects.",
                    ["Red builds after harmless UI changes", "Hours of page-object maintenance after every release",
                     "No idea which locators are about to break next"]),
        "how": ("How it heals", "Six steps, most of them free", [
            ("Remember", "The first green run stores a fingerprint of every element: tag, ids, text, label, position."),
            ("Detect", "A selector finds nothing - the healer takes over instead of failing the test."),
            ("Match locally", "Every element on the page is scored against the fingerprint. Free, milliseconds."),
            ("Guard", "Never another list item, the opposite button, a field for a button, or another locator's element."),
            ("Ask Claude - optional", "Only when the local match is not sure: about $0.002 per heal."),
            ("Report", "The test passes with a WARN - and a ready-made code fix for the page object.")]),
        "live": ("Live, on a broken demo shop", "26 candidates.<br>One clear winner.",
                 "The overlay shows what the healer sees: the old selector is gone, the candidates are scored."),
        "healed": ("Healed", "Milliseconds. <span class='green'>$0.</span>",
                   "<code>#product-search</code> &rarr; <code>[data-testid=\"search-box\"]</code>, local heuristic, "
                   "confidence 0.69 - the test just goes on."),
        "guards": ("Safety first", "A wrong heal is worse than a failed test.",
                   "When an element is really gone, the healer says so instead of guessing.",
                   "wrong elements picked", "of deleted elements correctly refused"),
        "bench": ("Measured, not claimed", "Accuracy on a broken shop",
                  ["Level", "Local only ($0)", "+ Claude Haiku"],
                  "ShopLab demo: 4 pages, 86 elements. Claude cost for all 373 broken elements: $0.13.",
                  ["ids renamed", "+ names, texts", "+ moved, re-tagged", "all ids removed", "deleted - must not heal"]),
        "report": ("Every heal is a to-do, not a secret", "The report tells you what to fix",
                   "Old &rarr; new selector, source line, confidence, cost - and the code fix, as a patch or applied."),
        "fits": ("Fits your stack", "Tested in 20 combinations",
                 "Every combination runs the same ten tests - twice: once green, once with a deliberate failure.",
                 ["Parallel runs", "Playwright 1.45 - 1.63", "Selenium 4.21 - 4.49", "Java 17 / 21 / 25",
                  "Linux &amp; Windows", "Maven &amp; Gradle"]),
        "start": ("Get started", "One dependency.<br>One settings file.", "Free, open source, on Maven Central."),
    },
    "tr": {
        "footer": "Playwright ve Selenium için kendini onaran locator'lar",
        "cover": ("Açık kaynak · Java", "Locator bozuldu.<br><span class='green'>Test bozulmadı.</span>",
                  "Playwright ve Selenium testleri için self-healing katmanı: sayfa yapısı değişince elementi yeniden "
                  "bulur, testi devam ettirir ve neyi düzeltmen gerektiğini tam olarak söyler."),
        "problem": ("Problem", "Bir id'nin adı değişti diye build kırmızı olmamalı.",
                    "Yeni sürümde <code>#login-username</code>, <code>#user-name</code> oldu. Kullanıcı için hiçbir "
                    "şey bozulmadı - ama login'e dokunan her test düştü ve biri sabahını page object güncelleyerek "
                    "geçirdi.",
                    ["Zararsız arayüz değişikliklerinden sonra kırmızı build'ler",
                     "Her sürümden sonra saatlerce page object bakımı", "Hangi locator'ın sıradaki kırılacağı belirsiz"]),
        "how": ("Nasıl onarıyor", "Altı adım, çoğu ücretsiz", [
            ("Hatırla", "İlk yeşil koşu her elementin parmak izini saklar: tag, id'ler, metin, label, konum."),
            ("Fark et", "Selector hiçbir şey bulamaz - healer testi düşürmek yerine devreye girer."),
            ("Yerelde eşleştir", "Sayfadaki her element parmak iziyle puanlanır. Ücretsiz, milisaniyeler."),
            ("Koru", "Asla listedeki başka bir kayıt, zıt buton, buton yerine alan ya da başka locator'ın elementi."),
            ("Claude'a sor - isteğe bağlı", "Sadece yerel eşleşme emin değilse: heal başına yaklaşık $0.002."),
            ("Raporla", "Test WARN ile geçer - page object için hazır kod düzeltmesiyle.")]),
        "live": ("Canlı, bozulmuş bir demo mağazada", "26 aday.<br>Tek net kazanan.",
                 "Overlay healer'ın gördüğünü gösteriyor: eski selector yok, adaylar puanlanıyor."),
        "healed": ("Onarıldı", "Milisaniyeler. <span class='green'>$0.</span>",
                   "<code>#product-search</code> &rarr; <code>[data-testid=\"search-box\"]</code>, yerel heuristic, "
                   "güven 0.69 - test kaldığı yerden devam ediyor."),
        "guards": ("Önce güvenlik", "Yanlış heal, düşen testten daha kötüdür.",
                   "Element gerçekten kaldırıldıysa healer tahmin yürütmez, bunu söyler.",
                   "yanlış element seçildi", "silinen elementin doğru şekilde reddedilme oranı"),
        "bench": ("İddia değil, ölçüm", "Bozulmuş bir mağazada doğruluk",
                  ["Seviye", "Sadece yerel ($0)", "+ Claude Haiku"],
                  "ShopLab demo: 4 sayfa, 86 element. Bozulan 373 elementin tamamı için Claude maliyeti: $0.13.",
                  ["id'ler değişti", "+ name, metinler", "+ taşındı, tag değişti", "tüm id'ler silindi",
                   "silindi - heal edilmemeli"]),
        "report": ("Her heal bir yapılacak iş, sır değil", "Rapor neyi düzelteceğini söylüyor",
                   "Eski &rarr; yeni selector, kaynak satırı, güven, maliyet - ve kod düzeltmesi: patch olarak ya da doğrudan uygulanmış."),
        "fits": ("Stack'ine uyar", "20 kombinasyonda test edildi",
                 "Her kombinasyon aynı on testi iki kez koşar: bir kez yeşil, bir kez bilerek hatalı.",
                 ["Paralel koşu", "Playwright 1.45 - 1.63", "Selenium 4.21 - 4.49", "Java 17 / 21 / 25",
                  "Linux ve Windows", "Maven ve Gradle"]),
        "start": ("Başla", "Tek bağımlılık.<br>Tek ayar dosyası.", "Ücretsiz, açık kaynak, Maven Central'da."),
    },
}

BENCH = [("low", "100%", "100%"), ("medium", "97.7%", "100%"), ("high", "87.2%", "98.8%"),
         ("extreme", "22.1%", "97.7%"), ("removed", "100%", "100%")]
RUNNERS = ["JUnit 5", "JUnit 4", "TestNG", "Cucumber<br><small>JUnit 5</small>", "Cucumber<br><small>TestNG</small>",
           "Cucumber<br><small>JUnit 4</small>"]

START_CODE = """<span class="c">&lt;!-- pom.xml --&gt;</span>
&lt;dependency&gt;
  &lt;groupId&gt;<span class="v">io.github.yasindeger48</span>&lt;/groupId&gt;
  <span class="c">&lt;!-- or healer-selenium --&gt;</span>
  &lt;artifactId&gt;<span class="v">healer-playwright</span>&lt;/artifactId&gt;
  &lt;version&gt;<span class="v">2.2.0</span>&lt;/version&gt;
&lt;/dependency&gt;

<span class="c"># src/test/resources/healer.properties</span>
<span class="k">browser.name</span>=<span class="v">msedge</span>
<span class="k">browser.headless</span>=<span class="v">true</span>
<span class="k">healer.mode</span>=<span class="v">auto</span>            <span class="c"># auto | suggest | off</span>
<span class="k">healer.llm.enabled</span>=<span class="v">false</span>     <span class="c"># Claude, optional</span>
<span class="k">healer.report.open</span>=<span class="v">onWarn</span>"""


def slides(lang):
    t = TEXT[lang]
    foot = lambda n: f"<div class='footer'><span>{t['footer']}</span><span>{n}/10</span></div>"
    out = []
    k, h, lead = t["cover"]
    chips = "".join(f"<span class='chip'>{c}</span>" for c in
                    ["Playwright", "Selenium", "JUnit 5 / 4", "TestNG", "Cucumber", "Maven Central"])
    out.append(("cover", f"""<section class="slide dark"><div class="kicker">{k}</div><h1>{h}</h1>
<p class="lead">{lead}</p><div class="chips">{chips}</div>
<div class="shot" style="margin-top:48px"><img src="{img('crops/cover.png')}"></div>{foot(1)}</section>"""))
    k, h, lead, pains = t["problem"]
    items = "".join(f"<div class='card' style='font-size:32px;font-weight:650;display:flex;gap:20px;align-items:center'>"
                    f"<span class='red' style='font-size:40px'>&#10007;</span>{p}</div>" for p in pains)
    out.append(("problem", f"""<section class="slide light"><div class="kicker">{k}</div><h2>{h}</h2>
<p class="lead">{lead}</p><div class="steps" style="margin-top:48px">{items}</div>
<pre style="margin-top:auto;margin-bottom:40px;font-size:24px"><span class="c">&lt;!-- release 2.0 --&gt;</span>
<span style="color:#fca5a5">- &lt;input id="login-username" name="username"&gt;</span>
<span class="v">+ &lt;input id="user-name" data-testid="username-input"&gt;</span>

<span style="color:#fca5a5">&#10007; NoSuchElementException: #login-username</span></pre>{foot(2)}</section>"""))
    k, h, steps = t["how"]
    rows = "".join(f"<div class='step'><div class='num' style='flex-basis:76px;height:76px;font-size:36px;{'background:var(--green)' if i == 5 else ''}'>{i + 1}</div>"
                   f"<div><h3 style='font-size:40px'>{a}</h3><p style='font-size:30px'>{b}</p></div></div>" for i, (a, b) in enumerate(steps))
    out.append(("how-it-works", f"""<section class="slide light"><div class="kicker">{k}</div><h2>{h}</h2>
<div class="steps" style="gap:34px;margin-top:56px">{rows}</div>{foot(3)}</section>"""))
    k, h, lead = t["live"]
    out.append(("live", f"""<section class="slide dark"><div class="kicker">{k}</div><h2>{h}</h2><p class="lead">{lead}</p>
<div class="shot"><img src="{img('crops/candidates.png')}"></div>{foot(4)}</section>"""))
    k, h, lead = t["healed"]
    out.append(("healed", f"""<section class="slide dark"><div class="kicker">{k}</div><h2>{h}</h2><p class="lead">{lead}</p>
<div class="shot"><img src="{img('crops/healed-search.png')}"></div>{foot(5)}</section>"""))
    k, h, lead, wrong, refused = t["guards"]
    out.append(("guards", f"""<section class="slide light"><div class="kicker">{k}</div><h2>{h}</h2><p class="lead">{lead}</p>
<div style="display:flex;gap:28px;margin-top:70px">
 <div class="card" style="flex:1;text-align:center;padding:50px 20px"><div class="big green">0</div><p class="lead" style="margin-top:14px">{wrong}</p></div>
 <div class="card" style="flex:1;text-align:center;padding:50px 20px"><div class="big green">100%</div><p class="lead" style="margin-top:14px">{refused}</p></div>
</div>
<div class="shot" style="margin-top:60px;box-shadow:0 12px 34px rgba(0,0,0,.12)"><pre style="border-radius:0;font-size:23px">[FAIL] Form.cancel: '#cancel' could not be healed
  best match: button "Save", score 0.53 &lt; 0.60</pre></div>{foot(6)}</section>"""))
    k, h, head, note, labels = t["bench"]
    trs = "".join(f"<tr><td><b>{lvl}</b><br><span style='font-size:22px;color:var(--muted)'>{lab}</span></td>"
                  f"<td class='n'>{a}</td><td class='n green'>{b}</td></tr>" for (lvl, a, b), lab in zip(BENCH, labels))
    out.append(("benchmark", f"""<section class="slide light"><div class="kicker">{k}</div><h2>{h}</h2>
<div class="card" style="margin-top:50px;padding:20px 30px"><table><tr><th>{head[0]}</th><th class='n'>{head[1]}</th><th class='n'>{head[2]}</th></tr>{trs}
<tr><td><b class='red'>wrong element</b></td><td class='n green'>0</td><td class='n green'>0</td></tr></table></div>
<p class="lead" style="font-size:26px">{note}</p>{foot(7)}</section>"""))
    k, h, lead = t["report"]
    out.append(("report", f"""<section class="slide light"><div class="kicker">{k}</div><h2>{h}</h2><p class="lead">{lead}</p>
<div class="shot" style="box-shadow:0 20px 50px rgba(22,33,62,.25)"><img src="{img('crops/report.png')}"></div>{foot(8)}</section>"""))
    k, h, lead, extras = t["fits"]
    cells = "".join(f"<div class='cell' style='background:#e7ebff;color:#2b3f8f'>{d}</div>" for d in ["", "Playwright", "Selenium"])
    for r in RUNNERS:
        cells += f"<div class='cell' style='background:#fff;color:var(--ink)'>{r}</div>" + "<div class='cell'>&#10003; OK</div>" * 2
    chips = "".join(f"<span class='chip'>{c}</span>" for c in extras)
    out.append(("compatibility", f"""<section class="slide light"><div class="kicker">{k}</div><h2>{h}</h2><p class="lead">{lead}</p>
<div class="grid" style="grid-template-columns:1.3fr 1fr 1fr;margin-top:40px">{cells}</div>
<div class="chips" style="margin-top:30px">{chips}</div>{foot(9)}</section>"""))
    k, h, lead = t["start"]
    code = START_CODE if lang == "en" else START_CODE.replace("or healer-selenium", "ya da healer-selenium")         .replace("Claude, optional", "Claude, isteğe bağlı")
    out.append(("get-started", f"""<section class="slide dark"><div class="kicker">{k}</div><h2>{h}</h2><p class="lead">{lead}</p>
<pre style="margin-top:44px">{code}</pre>
<p class="lead" style="margin-top:auto;font-size:32px;color:#fff"><b>{REPO}</b></p>{foot(10)}</section>"""))
    return out


PAGE = """<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><title>Self-healing locators</title>
<link rel="stylesheet" href="../../style.css"><style>@page {{ size: 1080px 1350px; margin: 0 }} code {{ font-variant-ligatures: none; font-family: var(--mono); font-size: .9em; background: rgba(76,110,245,.12); padding: 2px 8px; border-radius: 8px }}</style>
</head><body>{body}</body></html>"""


def main():
    """Writes the slides as HTML and render.json - what capture/ (linkedin.Render, Playwright) turns into PNG and PDF."""
    jobs = []
    for lang in TEXT:
        d = os.path.join(OUT, lang)
        os.makedirs(d, exist_ok=True)
        images = os.path.join(LINKEDIN, "images", lang)
        os.makedirs(images, exist_ok=True)
        all_slides = slides(lang)
        for i, (name, html) in enumerate(all_slides, 1):
            f = os.path.join(d, f"{i:02d}-{name}.html")
            open(f, "w", encoding="utf-8").write(PAGE.format(lang=lang, body=html))
            jobs.append({"html": f, "png": os.path.join(images, f"{i:02d}-{name}.png")})
        deck = os.path.join(d, "carousel.html")
        open(deck, "w", encoding="utf-8").write(PAGE.format(lang=lang, body="\n".join(h for _, h in all_slides)))
        os.makedirs(os.path.join(LINKEDIN, "carousel"), exist_ok=True)
        jobs.append({"html": deck, "pdf": os.path.join(LINKEDIN, "carousel", f"self-healing-{lang}.pdf")})
        print("built", lang, len(all_slides), "slides")
    import json
    json.dump(jobs, open(os.path.join(HERE, "graphics", "out", "render.json"), "w", encoding="utf-8"), indent=1)


if __name__ == "__main__":
    sys.exit(main())
