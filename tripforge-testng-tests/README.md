# TripForge self-healing lab - TestNG

TestNG + Playwright tests for <https://trip-forge-lbuh.vercel.app/self-healing-lab>, using the self-healing framework
**straight from Maven Central** (`io.github.yasindeger48:healer-playwright`, `healer-testng`, optional `healer-claude`).
The TestNG listener registers itself through `META-INF/services` - there is no `@Listeners` annotation in the code.

- `SelfHealingLabTest` - lookup, full verification, and a data-driven test (`@DataProvider`): every invocation is its
  own test in the report
- `pages/SelfHealingLabPage` - selectors recorded from one page load, so every step is healed

```bash
mvn test                                                          # headless
mvn test -Dheadless=false -Dhealer.visual=true -Dslowmo=300       # watch it: healing drawn on the page
```

Report: `target/healer-report/healing-report.html`.
