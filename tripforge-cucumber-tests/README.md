# TripForge self-healing lab - Cucumber

Cucumber + Playwright + JUnit Platform tests for <https://trip-forge-lbuh.vercel.app/self-healing-lab>, using the
self-healing framework **straight from Maven Central** (`io.github.yasindeger48:healer-playwright`, `healer-cucumber`,
optional `healer-claude`). Nothing to build or install first.

- `features/booking.feature` - the scenarios in Gherkin
- `LabSteps` - step definitions; `pages/SelfHealingLabPage` - the page object (selectors from one page load, so
  every step is healed)
- `RunCucumberTest` - JUnit Platform suite with `com.selfhealing.healer.cucumber.HealingCucumberPlugin`

```bash
mvn test                                                          # headless
mvn test -Dbrowser.headless=false -Dhealer.visual=true -Dbrowser.slowmo=300       # watch it: healing drawn on the page
```

Report: `target/healer-report/healing-report.html` - each scenario is a test, the Gherkin steps are its steps.
