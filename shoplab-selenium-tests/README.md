# ShopLab tests with Selenium

The ShopLab example with Selenium WebDriver instead of Playwright: page objects use ordinary `By` locators
(`By.id`, `By.name`, `By.cssSelector`, `By.xpath`) through `SelfHealingDriver.element(key, by)`.

```bash
# demo site on :8080 (see ../demo-site); the framework comes from Maven Central
mvn test                                   # headless Edge
mvn test -Dbrowser=chrome -Dheadless=false # visible Chrome
```

Selenium Manager downloads the matching browser driver automatically.

Try healing: `python ../demo-site/mutate.py --level high`, run `mvn test` again, then open
`target/healer-report/healing-report.html`. `target/healer-report/locator-fixes.patch` rewrites the broken locators,
e.g. `By.id("login-username")` -> `By.cssSelector("[data-testid='username-input']")`.
Restore the site with `python ../demo-site/mutate.py --reset`.
