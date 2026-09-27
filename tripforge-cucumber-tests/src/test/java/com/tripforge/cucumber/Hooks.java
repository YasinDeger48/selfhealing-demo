package com.tripforge.cucumber;

import com.microsoft.playwright.Browser;
import com.microsoft.playwright.BrowserContext;
import com.microsoft.playwright.BrowserType;
import com.microsoft.playwright.Page;
import com.microsoft.playwright.Playwright;
import com.selfhealing.healer.playwright.SelfHealingPage;
import io.cucumber.java.After;
import io.cucumber.java.AfterAll;
import io.cucumber.java.Before;

/**
 * Browser lifecycle. System properties: {@code headless} (default true), {@code slowmo} (ms, default 0),
 * {@code browser.channel} (default msedge; "chromium" for Playwright's bundled browser).
 */
public class Hooks {

    public static final String BASE_URL = System.getProperty("tripforge.baseUrl", "https://trip-forge-lbuh.vercel.app");

    private static Playwright playwright;
    private static Browser browser;

    private final World world;

    public Hooks(World world) {
        this.world = world;
    }

    @Before
    public void openBrowser() {
        if (browser == null) {
            playwright = Playwright.create();
            BrowserType.LaunchOptions o = new BrowserType.LaunchOptions()
                    .setHeadless(Boolean.parseBoolean(System.getProperty("headless", "true")))
                    .setSlowMo(Double.parseDouble(System.getProperty("slowmo", "0")));
            String channel = System.getProperty("browser.channel", "msedge");
            if (!"chromium".equals(channel)) o.setChannel(channel);
            browser = playwright.chromium().launch(o);
        }
        BrowserContext context = browser.newContext(new Browser.NewContextOptions().setViewportSize(1280, 900));
        Page page = context.newPage();
        page.setDefaultTimeout(15_000);
        world.page = page;
        world.healer = SelfHealingPage.wrap(page);
    }

    @After
    public void closeBrowser() {
        world.page.context().close();
    }

    @AfterAll
    public static void quit() {
        if (playwright != null) playwright.close();
    }
}
