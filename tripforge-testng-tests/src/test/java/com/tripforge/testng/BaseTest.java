package com.tripforge.testng;

import com.microsoft.playwright.Browser;
import com.microsoft.playwright.BrowserContext;
import com.microsoft.playwright.Page;
import com.microsoft.playwright.Playwright;
import com.selfhealing.healer.playwright.HealerBrowser;
import com.selfhealing.healer.playwright.SelfHealingPage;
import org.testng.annotations.AfterClass;
import org.testng.annotations.AfterMethod;
import org.testng.annotations.BeforeClass;
import org.testng.annotations.BeforeMethod;

/**
 * Browser lifecycle. Everything comes from the settings (src/test/resources/healer.properties, environment variables
 * or -D): app.baseUrl, browser.name, browser.headless, browser.slowmo, browser.viewport, browser.timeoutMs.
 * No listener annotation: healer-testng registers itself.
 */
public abstract class BaseTest {

    protected static final String BASE_URL = HealerBrowser.baseUrl();

    private Playwright playwright;
    private Browser browser;
    protected BrowserContext context;
    protected Page page;
    protected SelfHealingPage healer;

    @BeforeClass(alwaysRun = true)
    public void launchBrowser() {
        playwright = Playwright.create();
        browser = HealerBrowser.launch(playwright);
    }

    @AfterClass(alwaysRun = true)
    public void closeBrowser() {
        if (playwright != null) playwright.close();
    }

    @BeforeMethod(alwaysRun = true)
    public void openPage() {
        context = HealerBrowser.newContext(browser);
        page = context.newPage();
        healer = SelfHealingPage.wrap(page);
    }

    @AfterMethod(alwaysRun = true)
    public void closePage() {
        HealerBrowser.close(context);
    }
}
