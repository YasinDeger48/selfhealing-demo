# Self-Healing Demo

Demo material for the [Self-Healing Locator Framework](https://github.com/YasinDeger48/selfhealing-framework):
a multilingual demo shop and a UI test project that uses the framework like any other project would.

| Folder | What it is |
|---|---|
| [`demo-site/`](demo-site) | **ShopLab** — React (Vite) demo e-commerce site in 6 languages (EN default, DE, RU, JA, TR, AR), plus `mutate.py` to break locators on purpose |
| [`shoplab-tests/`](shoplab-tests) | Playwright + JUnit 5 tests for ShopLab, using the framework through its Maven dependencies |
| [`shoplab-selenium-tests/`](shoplab-selenium-tests) | The same framework with Selenium WebDriver (`healer-selenium`): login, search, cart, logout |
| [`tripforge-tests/`](tripforge-tests) | Tests for the public TripForge self-healing lab: every load changes all ids, so each step is healed from a cold start |

## Quick start

```bash
# 1) Framework (until it is published to a Maven repository)
git clone https://github.com/YasinDeger48/selfhealing-framework.git
cd selfhealing-framework && mvn install && cd ..

# 2) Demo site - http://localhost:8080, user standard_user / secret123
cd demo-site && npm install && npm run dev          # keep running

# 3) Baseline run against the working site (records element fingerprints)
cd shoplab-tests && mvn test

# 4) Break the locators, run again: tests pass, every repair is reported as WARN
cd ../demo-site && python mutate.py --level extreme  # low | medium | high | extreme | removed
cd ../shoplab-tests && mvn test                      # report: target/healer-report/healing-report.html
```

Optional: set `ANTHROPIC_API_KEY` to enable the Claude stage (needed for the `extreme` level).
Watch it live: `mvn test -Dheadless=false -Dslowmo=250 -Dhealer.visual=true`.

Requirements: Java 17+, Maven 3.9+, Node.js 18+, Python 3, Microsoft Edge (or `-Dbrowser.channel=chromium`).
