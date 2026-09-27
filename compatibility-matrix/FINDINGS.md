# Findings

## 2.2.1: settings-driven browsers, more tests, the real sites

Every project now takes its browser from `healer.properties` (`HealerBrowser` / `HealerDriver`) and runs ten tests:
the five on bundled pages (two heals, a plain-language step, a removed button that must not be healed, a
deliberate failure) and five on the real sites (TripForge on Vercel, ShopLab broken with `mutate.py --level high`).

| # | Combination | Problem | Cause | Fix (2.2.1) |
|---|---|---|---|---|
| 1 | Playwright + TestNG / JUnit 4 | The video and trace of a failed test were never kept (`browser.video/trace=failures`). | TestNG runs @AfterMethod after the test ended (no current test any more); JUnit 4 runs @After before the rule sees the failure. | The outcome comes from the test that just ran on the thread; when it is not known yet, the files are kept until the test ends and dropped if it passed. |
| 2 | Playwright 1.45 | Every test failed when `browser.video` was on and Playwright's ffmpeg was missing. | 1.45 only looks for ffmpeg when the first page opens, the fallback was rejected by Playwright, and closing the broken context dropped the connection. | ffmpeg is checked with a probe page before the test, the fallback context is valid, the broken one is left to the browser. |
| 3 | Any, without `.healer/` (cold start) on the changed ShopLab | Login fields and buttons were not healed; best matches were a div, a form, a paragraph. | Only the old id was known, compared with the new id only. | The step's action (`fill` needs a field ...) and the old name's control word (`...-button`) rule out other kinds; the old name is looked for in all names, the label and the button text. 4 of 5 ShopLab elements heal without history; the cart badge (`cart-count` -> `basket-count`, inside the "Cart" link) is ambiguous and correctly refused - the recorded baseline or Claude solves it. |
| 4 | Any | A heal refused by a guard read like a threshold problem ("scored 0.82 (min 0.60)"). | The reason did not say which guard. | "... but it is the element of locator 'X'" / "... needs an element that is editable". |
| 6 | Selenium + Cucumber on JUnit 4 (once) | A scenario failed: "Cannot write .healer/healed-locators.json" (AccessDeniedException). | The project folder is in OneDrive; a scanner / sync held the file while it was replaced. | Retried, and kept in memory if it stays locked - the test goes on. |
| 5 | Selenium | `healer.visual=true` drew nothing. | The overlay existed for Playwright only. | Selenium overlay (same drawing, through JavaScript). |

Notes (test setup, not framework):
- Selenium projects share one browser between tests - the ShopLab helper logs out (clears storage and cookies) first.
- Wait for a single-page app to render before the first step when the probe time is short (`healer.probeTimeoutMs`).
- Parallel Cucumber on TestNG runs 10 scenarios at once by default (`testng.dataProviderThreadCount`), JUnit 5 may
  grow its pool beyond `parallelism` (`...fixed.max-pool-size`) - too many browsers against a real site time out.

## 2.2.0: parallel runs and older library versions

Eight more projects (see [README.md](README.md)): parallel JUnit 5, TestNG and Cucumber runs, Playwright 1.45 and
Selenium 4.21. All pass both runs - no framework change was needed. Heals, plain-language steps and failures stay tied
to the right test when tests run on several threads and share element keys.

Notes for users:

- **Parallel tests need their own browser per thread.** TestNG `parallel=methods` runs the methods of one instance on
  several threads, so instance fields (`page`, `driver`) are shared - keep them in a `ThreadLocal`
  (the matrix projects show how).
- **TestNG parallel with Surefire 3.6:** Surefire runs TestNG on the JUnit Platform (testng-engine); set
  `testng.parallel=methods` and `testng.threadCount=3` in `src/test/resources/junit-platform.properties` - the
  `<parallel>` setting of Surefire's own TestNG provider does not apply.
- **Surefire only runs classes named `*Test`, `Test*`, `*Tests`, `*TestCase`** - a class named `HealingTest2` is
  silently skipped (this was a mistake in the first version of the parallel projects, not a framework bug).

## 2.1.0

Found by running the matrix with healer 2.0.1 (Maven Surefire 3.5.3, then 3.6.0), fixed in **healer 2.1.0**.
After the fixes all 12 combinations pass both runs (see [RESULTS.md](RESULTS.md)).

| # | Combination | Problem | Cause | Fix (2.1.0) |
|---|---|---|---|---|
| 1 | Cucumber on TestNG | Every scenario was listed twice in the report: as the scenario and as TestNG's `runScenario[...]` (without steps); a failing scenario counted as two failed tests. | Cucumber's TestNG runner runs each scenario as a TestNG test, so the TestNG listener and the Cucumber plugin both recorded it. | The TestNG listener leaves tests of Cucumber's TestNG runner to the Cucumber plugin when the plugin is active. |
| 2 | JUnit 4 (Playwright and Selenium) | Healing worked, but no report, no test attribution, no failure analysis. | There was no JUnit 4 integration. | New module **`healer-junit4`**: `@Rule public HealingRule healing = new HealingRule();` The report is written when the JVM ends (JUnit 4 has no end-of-run hook for rules) or with `HealingRule.finishRun()`. |
| 3 | TestNG with Surefire 3.6.0 | Tests appeared in the report without steps or heals, although the heals happened. | Surefire 3.6.0 runs TestNG on the JUnit Platform and starts TestNG twice (discovery, then execution). TestNG reports "execution finished" after discovery, the healer wrote the report then and ignored the second, real finish. | The report is written again whenever tests, steps or heals were added since the last report. All integrations share one run (`HealingRun.shared`), so one JVM writes one report. |
| 4 | Cucumber on the JUnit Platform with Surefire 3.5.3 | Surefire counted 0 tests - **a failing scenario did not fail the build**. Not caused by the healer (the same without its plugin). | Surefire 3.5.3 does not report Cucumber scenarios of a JUnit Platform `@Suite` (JUnit Platform 1.14). | Surefire **3.6.0** everywhere (framework, examples, matrix) and documented as the minimum. The healer now prints `[healer] N test(s) FAILED` at the end of every run, whatever the build result says. |

## Found earlier (fixed in 2.0.1)

| Combination | Problem | Fix |
|---|---|---|
| TestNG (any driver) | No TestNG test ran at all, build green: the adapters brought the JUnit API, so Surefire picked its JUnit provider. | The JUnit API is an optional dependency of the adapters. |
| all | Values typed into fields whose name merely contained "pass"/"pin" (e.g. `passengerSurname`) were masked. | Secret names are matched by whole words (password, pwd, pin, token, parola, sifre ...). |
| Cucumber | A broken setup (missing constructor, wrong glue) was analysed as UNKNOWN. | Setup errors are TEST_CODE. |

## Notes for users (not bugs)

- **Cucumber constructor injection** (`public Steps(World world)`) needs `cucumber-picocontainer`; without it Cucumber
  fails with "does not have a public zero-argument constructor".
- **Cucumber on the JUnit Platform:** select features with `@SelectPackages("features")`; Cucumber warns that
  `@SelectClasspathResource` should not be used for a package.
- **JUnit 4 screenshots:** rules wrap `@After`, so a failure is analysed after the browser was closed there - the
  analysis has no screenshot unless the browser is closed later (e.g. in `@AfterClass`).
- **One report per JVM:** with several integrations in one project (e.g. JUnit 5 tests and a Cucumber suite) all tests
  go into the same report.
