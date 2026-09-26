package com.tripforge.tests;

import com.microsoft.playwright.Browser;
import com.microsoft.playwright.BrowserContext;
import com.microsoft.playwright.BrowserType;
import com.microsoft.playwright.Page;
import com.microsoft.playwright.Playwright;
import com.selfhealing.healer.playwright.HealingExtension;
import com.selfhealing.healer.playwright.SelfHealingPage;
import org.junit.jupiter.api.AfterAll;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.extension.ExtendWith;

/**
 * Browser lifecycle for the TripForge lab tests. System properties:
 * {@code tripforge.baseUrl} (default https://trip-forge-lbuh.vercel.app), {@code browser.channel}
 * (default msedge, "chromium" for Playwright's bundled browser), {@code headless} (default true),
 * {@code slowmo} (ms between browser actions, default 0 - use ~300 to watch a headed run).
 */
@ExtendWith(HealingExtension.class)
public abstract class BaseTest {

    protected static final String BASE_URL = System.getProperty("tripforge.baseUrl", "https://trip-forge-lbuh.vercel.app");

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
        page.setDefaultTimeout(15_000);
        healer = SelfHealingPage.wrap(page);
    }

    @AfterEach
    void closePage() {
        context.close();
    }
}
