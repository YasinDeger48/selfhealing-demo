package com.shoplab.tests;

import com.microsoft.playwright.Browser;
import com.microsoft.playwright.BrowserContext;
import com.microsoft.playwright.BrowserType;
import com.microsoft.playwright.Page;
import com.microsoft.playwright.Playwright;
import com.shoplab.tests.pages.LoginPage;
import com.selfhealing.healer.playwright.HealingExtension;
import com.selfhealing.healer.playwright.SelfHealingPage;
import org.junit.jupiter.api.AfterAll;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.extension.ExtendWith;

/**
 * Browser lifecycle for the ShopLab tests. System properties:
 * {@code shoplab.baseUrl} (default http://localhost:8080), {@code browser.channel} (default msedge,
 * use "chromium" for Playwright's bundled browser), {@code headless} (default true),
 * {@code slowmo} (ms between browser actions, default 0 - use ~300 to watch a headed run).
 */
@ExtendWith(HealingExtension.class)
public abstract class BaseTest {

    protected static final String BASE_URL = System.getProperty("shoplab.baseUrl", "http://localhost:8080");

    private static Playwright playwright;
    private static Browser browser;

    protected BrowserContext context;
    protected Page page;
    protected SelfHealingPage healer;

    @BeforeAll
    static void launchBrowser() {
        playwright = Playwright.create();
        BrowserType.LaunchOptions options = new BrowserType.LaunchOptions()
                .setHeadless(Boolean.parseBoolean(System.getProperty("headless", "true")))
                .setSlowMo(Double.parseDouble(System.getProperty("slowmo", "0")));
        String channel = System.getProperty("browser.channel", "msedge");
        if (!"chromium".equals(channel)) options.setChannel(channel);
        browser = playwright.chromium().launch(options);
    }

    @AfterAll
    static void closeBrowser() {
        if (playwright != null) playwright.close();
    }

    @BeforeEach
    void openPage() {
        context = browser.newContext(new Browser.NewContextOptions().setViewportSize(1280, 900));
        page = context.newPage();
        healer = SelfHealingPage.wrap(page);
    }

    @AfterEach
    void closePage() {
        context.close();
    }

    protected void loginAsStandardUser() {
        new LoginPage(healer).open(BASE_URL).loginAs("standard_user", "secret123");
        page.waitForURL("**/products");
    }
}
