# Compatibility matrix

One small Maven project per **driver x test runner** combination, all using the framework from Maven
(`io.github.yasindeger48:healer-*`):

| | JUnit 5 | JUnit 4 | TestNG | Cucumber on JUnit Platform | Cucumber on TestNG | Cucumber on JUnit 4 |
|---|---|---|---|---|---|---|
| **Playwright** | `playwright-junit5` | `playwright-junit4` | `playwright-testng` | `playwright-cucumber-junit5` | `playwright-cucumber-testng` | `playwright-cucumber-junit4` |
| **Selenium** | `selenium-junit5` | `selenium-junit4` | `selenium-testng` | `selenium-cucumber-junit5` | `selenium-cucumber-testng` | `selenium-cucumber-junit4` |

Every project runs the same three tests (or scenarios) against two bundled pages - `v1.html` (original) and
`v2.html` (ids, names and classes renamed):

1. **healRenamedButton** - use the Save button on v1 (fingerprint recorded), open v2, click it again: healed, "Saved".
2. **plainLanguageStep** - `healer.find("Form.email", "the email field")` on v2: found by description.
3. **deliberateFailure** - passes normally, fails with `-Dmatrix.fail=true`.

Integrations used: `healer-junit5` (`playwright-junit5` without any annotation via extension auto-detection,
`selenium-junit5` with `@ExtendWith`), `healer-junit4` (`@Rule`), `healer-testng` (registers itself),
`healer-cucumber` (plugin) on all three Cucumber runners.

`run_all.py` runs each project twice and checks, from Surefire's output and the healer report:

- the build passes, Surefire ran the 3 tests, the report lists exactly those 3 tests (once each), a heal and a
  plain-language step were recorded and tied to their test;
- with `-Dmatrix.fail=true`: **the build fails**, and the report shows exactly one failed test, analysed as ASSERTION.

```bash
python generate.py 2.1.0     # (re)generate the projects for a healer version
python run_all.py            # all combinations -> RESULTS.md, results.json, <project>/run.log
python run_all.py selenium-testng playwright-junit4   # only some
```

Needs Java 17, Maven, and Microsoft Edge (Playwright uses the installed Edge; Selenium Manager fetches msedgedriver).
Findings and their fixes: [FINDINGS.md](FINDINGS.md).
