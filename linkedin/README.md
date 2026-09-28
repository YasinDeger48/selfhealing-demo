# LinkedIn kit - self-healing locator framework

Everything for introducing the framework on LinkedIn, in Turkish and English. Every screenshot and the video come
from real runs of the framework (nothing mocked), every number from its own measurements (framework README
"Measured accuracy", `compatibility-matrix/RESULTS.md`).

## Contents

| Path | What | Use it for |
|---|---|---|
| `posts-tr.md`, `posts-en.md` | Launch post, video post, 3 series posts, first comment with links, "Featured" text | Copy into LinkedIn |
| `carousel/self-healing-tr.pdf`, `-en.pdf` | 10-slide carousel, 1080 x 1350 | Launch post: **Add a document**, upload the PDF, give it a title |
| `images/tr/`, `images/en/` | The 10 slides as PNG (1080 x 1350) | Single-picture posts (series), comments, profile banner ideas |
| `video/healing-demo-1280x800.webm` | 58 s: the test runs against the broken ShopLab, the overlay draws every healing step | Video post (convert to MP4 first, see below) |
| `images/step1-candidates-scored.png` | Frame of the video: candidates scored (orange) | Extra picture, comments |
| `images/step2-healed-login.png`, `step3-healed-search.png` | Frames: element healed (green) | Extra pictures |
| `images/overlay-*.png` | Overlay panel after the heals (login, products) | Extra pictures |
| `images/report-summary.png`, `report-expanded-top.png` | The real HTML report of the 12 ShopLab tests on the broken site (17 heals, $0) | "The report" post, comments |
| `source/report/` | That report itself (HTML, PDF, JSON, `locator-fixes.patch`) | Link / attach if someone asks |
| `source/` | How all of this is produced (below) | Regenerating after changes |

## Posting plan (suggestion)

| When | Post | Media |
|---|---|---|
| Day 1, Tue-Thu 08:00-10:00 | 1. Launch | Carousel PDF |
| Day 1, right after posting | First comment with the links | - |
| Day 3-4 | 2. Video | MP4 |
| Week 2 | 3. "A wrong heal is worse than a failed test" | `images/<lang>/06-guards.png` |
| Week 2-3 | 4. Cost | `images/<lang>/07-benchmark.png` |
| Week 3 | 5. Compatibility | `images/<lang>/09-compatibility.png` |

- One language per post. Posting both: Turkish from the profile, English a few days later (or the other way round) -
  not the same day.
- Answer comments during the first hour; that is what LinkedIn weighs most.
- Personalise the first lines of the launch post ("I have been that someone...") - it has to be your story.
- Tag nobody who did not agree to it. Pin the launch post to the profile (Featured) with the text in `posts-*.md`.

## Video: WebM -> MP4

LinkedIn wants MP4. The Playwright ffmpeg on this machine can only write WebM, so convert once:

- **Clipchamp** (built into Windows 11): open it, drag `healing-demo-1280x800.webm` in, put it on the timeline,
  **Export -> 1080p**. Optionally add a title card and captions ("old selector not found", "candidates scored",
  "healed - test goes on").
- Or with a full ffmpeg: `ffmpeg -i healing-demo-1280x800.webm -c:v libx264 -pix_fmt yuv420p -crf 20 healing-demo.mp4`

Upload the MP4 as a native video (not a link) and add captions - most people watch without sound.

## Alt texts (accessibility - "Alt text" field when uploading)

| Picture | Alt text (EN) | Alt metni (TR) |
|---|---|---|
| 01-cover | Title "Your locator broke. Your test didn't." above a screenshot of a login form whose username field is framed in green and labelled HEALED, next to a panel listing the scored candidates. | "Locator bozuldu. Test bozulmadı." başlığı; altında kullanıcı adı alanı yeşil çerçeveli ve HEALED etiketli bir login formu ile puanlanan adayları listeleyen panel. |
| 04-live | Login form with three candidates framed in dashed orange boxes and their scores 0.82, 0.34 and 0.30. | Kesikli turuncu kutularla çerçevelenmiş üç aday ve skorları: 0.82, 0.34, 0.30. |
| 05-healed | Product search field framed in green, labelled HEALED (local 0.69); the panel shows the old selector #product-search and the new one. | Yeşil çerçeveli ürün arama alanı, HEALED (local 0.69) etiketi; panelde eski selector #product-search ve yenisi. |
| 06-guards | Two figures: 0 wrong elements picked, 100% of deleted elements correctly refused, and a log line of a refused heal. | İki rakam: 0 yanlış element, silinen elementlerin %100'ü doğru şekilde reddedildi; altında reddedilen bir heal'in log satırı. |
| 07-benchmark | Table: accuracy per breakage level, local only and with Claude Haiku; wrong elements 0 in both. | Tablo: bozulma seviyesine göre doğruluk, sadece yerel ve Claude Haiku ile; iki durumda da yanlış element 0. |
| 08-report | The HTML report: 12 tests, 17 heals, $0; for each healed element the old and new selector, source line and code fix. | HTML rapor: 12 test, 17 heal, $0; her element için eski ve yeni selector, kaynak satırı ve kod düzeltmesi. |
| 09-compatibility | Grid of 6 test runners by Playwright and Selenium, all OK, plus parallel runs, versions, Java 17/21/25, Linux and Windows, Maven and Gradle. | 6 test runner × Playwright ve Selenium tablosu, hepsi OK; ayrıca paralel koşu, sürümler, Java 17/21/25, Linux ve Windows, Maven ve Gradle. |

## Before posting - check

- [ ] The links in the first comment open (both GitHub repositories are public, Maven Central shows the version).
- [ ] The version in the posts (`2.2.0`) is the one on Maven Central - if 2.2.1 is published by then, update it in
      `posts-*.md` and `source/build.py` (START_CODE) and rebuild.
- [ ] Nothing in the pictures you would not show (they contain only the demo site and the framework).

## Regenerating

Everything is produced from the real framework - change something, run it again:

```bash
# 1. screenshots + video: ShopLab running (cd ../demo-site && npm run dev), broken on purpose
python ../demo-site/mutate.py --level high
cd source/capture && mvn -q compile exec:java        # -> images/overlay-*.png, video/*.webm, images/report-*.png
cd ../../.. && python demo-site/mutate.py --reset

# 2. video frames used on the slides (images/step*.png): pick frames from the video, e.g.
#    ffmpeg -i video/healing-demo-1280x800.webm -r 1 frames/f%03d.png   (then copy the ones you like)
#    then crop them for the slides: python source/crops.py   (-> images/crops/, boxes in the script)

# 3. slides: HTML -> PNG + PDF
cd linkedin/source && python build.py
cd capture && mvn -q exec:java -Dexec.mainClass=linkedin.Render
```

The real report in `source/report/` comes from `shoplab-tests` run against the broken site with
`-Dhealer.llm.enabled=false` and the heal cache (`.healer/healed-locators.json`) removed, so every heal is live.
