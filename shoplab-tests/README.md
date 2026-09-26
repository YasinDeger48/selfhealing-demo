# ShopLab Tests — self-healing demo

UI tests for the ShopLab demo site (`../demo-site`), written with Playwright + JUnit 5 and the
self-healing framework (`../healing-framework`), which this project uses only as Maven dependencies.

## Setup (once)

```bash
cd ../healing-framework && mvn install        # install the framework into the local Maven repo
cd ../demo-site && npm install
```

Optional, for the Claude stage: set the `ANTHROPIC_API_KEY` environment variable.

## Demo

```bash
# 1) Start the site (separate terminal) - http://localhost:8080, user standard_user / secret123
cd ../demo-site && npm run dev

# 2) Baseline: run against the working site, fingerprints are recorded in .healer/
mvn test

# 3) Break the locators and run again - tests pass, heals are reported as WARN
cd ../demo-site && python mutate.py --level extreme    # low | medium | high | extreme
cd ../shoplab-tests && mvn test

# 4) Watch it happen: headed browser + healing overlay
mvn test -Dheadless=false -Dslowmo=250 -Dhealer.visual=true -Dhealer.visual.pauseMs=1500

# 5) Restore the site
cd ../demo-site && python mutate.py --reset
```

- Report: `target/healer-report/healing-report.html` (+ `.pdf`, `.json`).
- To see every healing step again instead of cache hits, delete `.healer/healed-locators.json`
  (keep `fingerprints.json`).
- Negative test: `python mutate.py --level removed` deletes four elements (one is a look-alike trap:
  only product 8 loses its add-to-cart button). Expected: 4 tests FAIL with "could not be healed" -
  nothing may be healed onto a wrong element.
- Mutation levels: `low` / `medium` / `high` are healed by the free local heuristic;
  `extreme` renames four elements to synonyms (Password → Passphrase, Apply → Redeem,
  Place Order → Buy Now ...) and needs Claude.

## Parallel

`mvn test -DforkCount=2 -DreuseForks=true` runs the test classes in two JVMs; the pom passes the same
`healer.runId` to both, so `target/healer-report` contains one merged report.

## Settings

`src/test/resources/healer.properties` — `healer.language=en` (console trace and the report's default
language; also `de`, `ru`, `ja`, `tr`, `ar`). The report itself has a language menu. System properties: `shoplab.baseUrl`
(default `http://localhost:8080`), `browser.channel` (default `msedge`), `headless`, `slowmo`.
