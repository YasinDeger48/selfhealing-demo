package com.tripforge.cucumber;

import com.microsoft.playwright.Browser;
import com.microsoft.playwright.BrowserContext;
import com.microsoft.playwright.Page;
import com.microsoft.playwright.Playwright;
import com.selfhealing.healer.playwright.HealerBrowser;
import com.selfhealing.healer.playwright.SelfHealingPage;
import io.cucumber.java.After;
import io.cucumber.java.AfterAll;
import io.cucumber.java.Before;

/**
 * Browser lifecycle. Everything comes from the settings (src/test/resources/healer.properties, environment variables
 * or -D): app.baseUrl, browser.name, browser.headless, browser.slowmo, browser.viewport, browser.timeoutMs.
 */
public class Hooks {

    public static final String BASE_URL = HealerBrowser.baseUrl();

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
            browser = HealerBrowser.launch(playwright);
        }
        BrowserContext context = HealerBrowser.newContext(browser);
        Page page = context.newPage();
        world.page = page;
        world.healer = SelfHealingPage.wrap(page);
    }

    @After
    public void closeBrowser() {
        HealerBrowser.close(world.page.context());
    }

    @AfterAll
    public static void quit() {
        if (playwright != null) playwright.close();
    }
}
