package com.tripforge.tests;

import com.microsoft.playwright.Browser;
import com.microsoft.playwright.BrowserContext;
import com.microsoft.playwright.Page;
import com.microsoft.playwright.Playwright;
import com.selfhealing.healer.junit5.HealingExtension;
import com.selfhealing.healer.playwright.HealerBrowser;
import com.selfhealing.healer.playwright.SelfHealingPage;
import org.junit.jupiter.api.AfterAll;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.extension.ExtendWith;

/**
 * Browser lifecycle. Everything comes from the settings (src/test/resources/healer.properties, healer-ci.properties,
 * an uncommitted healer-local.properties, environment variables or -D): browser.name, browser.headless,
 * browser.slowmo, browser.viewport, browser.timeoutMs, browser.video, browser.trace, app.baseUrl.
 */
@ExtendWith(HealingExtension.class)
public abstract class BaseTest {

    protected static final String BASE_URL = HealerBrowser.baseUrl();

    private static Playwright playwright;
    private static Browser browser;

    protected BrowserContext context;
    protected Page page;
    protected SelfHealingPage healer;

    @BeforeAll
    static void launchBrowser() {
        playwright = Playwright.create();
        browser = HealerBrowser.launch(playwright);
    }

    @AfterAll
    static void closeBrowser() {
        if (playwright != null) playwright.close();
    }

    @BeforeEach
    void openPage() {
        context = HealerBrowser.newContext(browser);
        page = context.newPage();
        healer = SelfHealingPage.wrap(page);
    }

    @AfterEach
    void closePage() {
        HealerBrowser.close(context);   // keeps video and trace of failed tests (browser.video / browser.trace)
    }
}
