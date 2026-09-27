# Compatibility matrix

One small Maven project per **driver x test runner** combination, all using the framework from Maven
(`io.github.yasindeger48:healer-*`):

| | JUnit 5 | JUnit 4 | TestNG | Cucumber on JUnit Platform | Cucumber on TestNG | Cucumber on JUnit 4 |
|---|---|---|---|---|---|---|
| **Playwright** | `playwright-junit5` | `playwright-junit4` | `playwright-testng` | `playwright-cucumber-junit5` | `playwright-cucumber-testng` | `playwright-cucumber-junit4` |
| **Selenium** | `selenium-junit5` | `selenium-junit4` | `selenium-testng` | `selenium-cucumber-junit5` | `selenium-cucumber-testng` | `selenium-cucumber-junit4` |

Variants on top of that:

| Project | What it checks |
|---|---|
| `playwright-junit5-parallel`, `selenium-junit5-parallel` | JUnit 5 parallel execution (3 threads), two test classes sharing the element keys |
| `playwright-testng-parallel`, `selenium-testng-parallel` | TestNG `parallel=methods` (3 threads), two test classes |
| `playwright-cucumber-junit5-parallel` | Cucumber parallel scenarios on the JUnit Platform, two features |
| `playwright-cucumber-testng-parallel` | Cucumber on TestNG with a parallel `@DataProvider`, two features |
| `playwright-junit5-pw1.45` | Playwright 1.45.0 instead of the version the framework is built with |
| `selenium-junit5-se4.21` | Selenium 4.21.0 (BOM) instead of the version the framework is built with |

Every project runs the same five tests (or scenarios) against three bundled pages - `v1.html` (original),
`v2.html` (ids, names and classes renamed) and `v3.html` (v2 without the Cancel button):

1. **healRenamedButton** - click Save on v1 (fingerprint recorded), open v2, click it again: healed, "Saved".
2. **healRenamedField** - type into the Name field on v1, again on v2 (id and name changed): healed.
3. **plainLanguageStep** - `healer.find("Form.email", "the email field")` on v2: found by its description.
4. **removedButtonNotHealed** - click Cancel on v1, open v3: the healer must **not** pick another button
   (false-positive protection) - the step fails and nothing else is clicked.
5. **deliberateFailure** - passes normally, fails with `-Dmatrix.fail=true`.

And the scenarios of the example projects, on the real sites ([`sites.py`](sites.py)):

| Test | Site | What it proves |
|---|---|---|
| **tripForgeLookup** | TripForge on Vercel | Booking lookup shows the itinerary - every id, test id and name changes on every page load, so each step is healed from a cold start (decoys must not be picked) |
| **tripForgeVerification** | TripForge on Vercel | Lookup, traveller confirmation, final check: `SELF-HEALING-COMPLETE` |
| **shopLabWrongPassword** | ShopLab demo site | A wrong password shows the error message |
| **shopLabSearchAndFilter** | ShopLab demo site | Search and category filter narrow the products |
| **shopLabAddToCart** | ShopLab demo site | Two products in the cart: the badge shows 2 |

The ShopLab scenarios use the keys and selectors of `../shoplab-tests` / `../shoplab-selenium-tests`; each project
starts from the fingerprints those projects recorded on the original site, and `run_all.py` breaks the site with
`mutate.py --level high` for the run (restored afterwards) - the situation after a release that changed the markup.

**Settings, not code.** The tests contain no browser setup: `HealerBrowser` / `HealerDriver` open the browser from
`src/test/resources/healer.properties` - the same commented layout as every project in this repository
(`../tools/healer_config.py`): application, browser (`browser.name`, `browser.headless`, `browser.slowmo`,
`browser.viewport`, `browser.timeoutMs`, `browser.video`, `browser.trace`), healing (`healer.enabled`,
`healer.mode`, thresholds ...), Claude, report. Change any of them in the file or for one run:

```bash
mvn test -Dbrowser.headless=false -Dbrowser.slowmo=300      # watch it
mvn test -Dbrowser.name=chromium                             # Playwright's own Chromium instead of Edge
mvn test -Dhealer.mode=suggest                               # report replacements, fail instead of healing
BROWSER_HEADLESS=false mvn test                              # the same through an environment variable
```

Integrations used: `healer-junit5` (`playwright-junit5` without any annotation via extension auto-detection,
`selenium-junit5` with `@ExtendWith`), `healer-junit4` (`@Rule`), `healer-testng` (registers itself),
`healer-cucumber` (plugin) on all three Cucumber runners.

`run_all.py` runs each project twice and checks, from Surefire's output and the healer report:

- the build passes, Surefire ran the tests, the report lists exactly those tests (once each), both heals and the
  plain-language step were recorded and tied to their test, the removed Cancel button was **not** healed onto another
  element; parallel projects really ran on several threads;
- with `-Dmatrix.fail=true`: **the build fails**, the report shows exactly the deliberately failed test(s), analysed as
  ASSERTION, and (Playwright) their video and trace are kept and linked (`browser.video/trace=failures`).

The expected numbers per project are in its `matrix.json` (written by `generate.py`).

```bash
python generate.py 2.2.0     # (re)generate the projects for a healer version
python run_all.py            # all combinations -> RESULTS.md, results.json, <project>/run.log
python run_all.py selenium-testng playwright-junit4   # only some
```

Needs Java 17, Maven, Microsoft Edge (Playwright uses the installed Edge; Selenium Manager fetches msedgedriver),
internet access (TripForge) and the ShopLab demo site running: `cd ../demo-site && npm run dev` (`run_all.py` stops
with a message when it is not). Addresses: `-Dtripforge.url=...`, `-Dshoplab.url=...` (or `SHOPLAB_URL` for
`run_all.py`); `-Dmatrix.skipSites=true` runs only the bundled pages. The failing run skips the real sites.
Findings and their fixes: [FINDINGS.md](FINDINGS.md).
