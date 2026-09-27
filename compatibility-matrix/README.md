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

Every project runs the same three tests (or scenarios) against two bundled pages - `v1.html` (original) and
`v2.html` (ids, names and classes renamed):

1. **healRenamedButton** - use the Save button on v1 (fingerprint recorded), open v2, click it again: healed, "Saved".
2. **plainLanguageStep** - `healer.find("Form.email", "the email field")` on v2: found by description.
3. **deliberateFailure** - passes normally, fails with `-Dmatrix.fail=true`.

Integrations used: `healer-junit5` (`playwright-junit5` without any annotation via extension auto-detection,
`selenium-junit5` with `@ExtendWith`), `healer-junit4` (`@Rule`), `healer-testng` (registers itself),
`healer-cucumber` (plugin) on all three Cucumber runners.

`run_all.py` runs each project twice and checks, from Surefire's output and the healer report:

- the build passes, Surefire ran the tests, the report lists exactly those tests (once each), a heal and a
  plain-language step were recorded and tied to their test; parallel projects really ran on several threads;
- with `-Dmatrix.fail=true`: **the build fails**, and the report shows exactly the deliberately failed test(s),
  analysed as ASSERTION.

The expected numbers per project are in its `matrix.json` (written by `generate.py`).

```bash
python generate.py 2.2.0     # (re)generate the projects for a healer version
python run_all.py            # all combinations -> RESULTS.md, results.json, <project>/run.log
python run_all.py selenium-testng playwright-junit4   # only some
```

Needs Java 17, Maven, and Microsoft Edge (Playwright uses the installed Edge; Selenium Manager fetches msedgedriver).
Findings and their fixes: [FINDINGS.md](FINDINGS.md).
