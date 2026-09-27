# Findings

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
