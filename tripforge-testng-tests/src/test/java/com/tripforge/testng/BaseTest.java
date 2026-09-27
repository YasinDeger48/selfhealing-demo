package com.tripforge.testng;

import com.microsoft.playwright.Browser;
import com.microsoft.playwright.BrowserContext;
import com.microsoft.playwright.BrowserType;
import com.microsoft.playwright.Page;
import com.microsoft.playwright.Playwright;
import com.selfhealing.healer.playwright.SelfHealingPage;
import org.testng.annotations.AfterClass;
import org.testng.annotations.AfterMethod;
import org.testng.annotations.BeforeClass;
import org.testng.annotations.BeforeMethod;

/**
 * Browser lifecycle. System properties: {@code headless} (default true), {@code slowmo} (ms, default 0),
 * {@code browser.channel} (default msedge; "chromium" for Playwright's bundled browser).
 * No listener annotation: healer-testng registers itself.
 */
public abstract class BaseTest {

    protected static final String BASE_URL = System.getProperty("tripforge.baseUrl", "https://trip-forge-lbuh.vercel.app");

    private Playwright playwright;
    private Browser browser;
    protected BrowserContext context;
    protected Page page;
    protected SelfHealingPage healer;

    @BeforeClass(alwaysRun = true)
    public void launchBrowser() {
        playwright = Playwright.create();
        BrowserType.LaunchOptions o = new BrowserType.LaunchOptions()
                .setHeadless(Boolean.parseBoolean(System.getProperty("headless", "true")))
                .setSlowMo(Double.parseDouble(System.getProperty("slowmo", "0")));
        String channel = System.getProperty("browser.channel", "msedge");
        if (!"chromium".equals(channel)) o.setChannel(channel);
        browser = playwright.chromium().launch(o);
    }

    @AfterClass(alwaysRun = true)
    public void closeBrowser() {
        if (playwright != null) playwright.close();
    }

    @BeforeMethod(alwaysRun = true)
    public void openPage() {
        context = browser.newContext(new Browser.NewContextOptions().setViewportSize(1280, 900));
        page = context.newPage();
        page.setDefaultTimeout(15_000);
        healer = SelfHealingPage.wrap(page);
    }

    @AfterMethod(alwaysRun = true)
    public void closePage() {
        context.close();
    }
}
