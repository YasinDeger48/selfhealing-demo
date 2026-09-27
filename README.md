# Self-Healing Demo

Demo material for the [Self-Healing Locator Framework](https://github.com/YasinDeger48/selfhealing-framework):
a multilingual demo shop and a UI test project that uses the framework like any other project would.

| Folder | What it is |
|---|---|
| [`demo-site/`](demo-site) | **ShopLab** — React (Vite) demo e-commerce site in 6 languages (EN default, DE, RU, JA, TR, AR), plus `mutate.py` to break locators on purpose |
| [`shoplab-tests/`](shoplab-tests) | Playwright + JUnit 5 tests for ShopLab, using the framework through its Maven dependencies |
| [`shoplab-selenium-tests/`](shoplab-selenium-tests) | The same framework with Selenium WebDriver (`healer-selenium`): login, search, cart, logout |
| [`tripforge-tests/`](tripforge-tests) | Tests for the public TripForge self-healing lab: every load changes all ids, so each step is healed from a cold start |
| [`tripforge-cucumber-tests/`](tripforge-cucumber-tests) | The TripForge lab with Cucumber (Gherkin scenarios), framework from Maven Central |
| [`tripforge-testng-tests/`](tripforge-testng-tests) | The TripForge lab with TestNG (incl. a data-driven test), framework from Maven Central |
| [`compatibility-matrix/`](compatibility-matrix) | One project per driver x test runner (+ parallel and older-version variants), each run passing and failing |
| [`tools/`](tools) | `healer_config.py`: the common `healer.properties` layout; `apply_config.py` brings every project into it |

**Settings in every project.** Each project manages the framework through `src/test/resources/healer.properties`
in the same commented layout - application (`app.baseUrl`), browser (`browser.name`, `browser.headless`,
`browser.slowmo`, `browser.viewport`, `browser.timeoutMs`, `browser.video`, `browser.trace`), healing
(`healer.enabled`, `healer.mode`, thresholds, popups, code fixes), Claude (`healer.llm.*`) and report
(`healer.report.*`). `healer-ci.properties` is the CI profile (`-Dhealer.profile=ci`), `healer-local.properties`
your own uncommitted overrides; environment variables and `-D` win over the files:
`mvn test -Dbrowser.headless=false -Dhealer.enabled=false`.

## Quick start

```bash
# 1) The framework comes from Maven Central (io.github.yasindeger48:healer-*) - nothing to install

# 2) Demo site - http://localhost:8080, user standard_user / secret123
cd demo-site && npm install && npm run dev          # keep running

# 3) Baseline run against the working site (records element fingerprints)
cd shoplab-tests && mvn test

# 4) Break the locators, run again: tests pass, every repair is reported as WARN
cd ../demo-site && python mutate.py --level extreme  # low | medium | high | extreme | removed
cd ../shoplab-tests && mvn test                      # report: target/healer-report/healing-report.html
```

Optional: set `ANTHROPIC_API_KEY` to enable the Claude stage (needed for the `extreme` level).
Watch it live: `mvn test -Dbrowser.headless=false -Dbrowser.slowmo=250 -Dhealer.visual=true`.

Requirements: Java 17+, Maven 3.9+, Node.js 18+, Python 3, Microsoft Edge (or `-Dbrowser.name=chromium`).
