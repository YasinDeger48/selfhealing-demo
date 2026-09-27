package matrix;

/** playwright + junit5: the same tests in every combination. The browser comes from healer.properties. */
public class HealingTest {

    static com.microsoft.playwright.Playwright playwright;
    static com.microsoft.playwright.Browser browser;
    com.microsoft.playwright.BrowserContext context;
    com.microsoft.playwright.Page page;
    com.selfhealing.healer.playwright.SelfHealingPage healer;

    @org.junit.jupiter.api.BeforeEach
    public void open() {
        if (browser == null) {
            playwright = com.microsoft.playwright.Playwright.create();
            browser = com.selfhealing.healer.playwright.HealerBrowser.launch(playwright);   // browser.name, browser.headless, browser.slowmo
        }
        context = com.selfhealing.healer.playwright.HealerBrowser.newContext(browser);        // browser.viewport, timeoutMs, video, trace
        page = context.newPage();
        healer = com.selfhealing.healer.playwright.SelfHealingPage.wrap(page);
    }

    @org.junit.jupiter.api.AfterEach
    public void close() {
        com.selfhealing.healer.playwright.HealerBrowser.close(context);                       // keeps video / trace of a failed test
    }

    @org.junit.jupiter.api.Test
    public void healRenamedButton() {
        page.navigate(Fixtures.url("v1.html"));
        healer.locator("Form.save", "#save").click();
        page.navigate(Fixtures.url("v2.html"));
        healer.locator("Form.save", "#save").click();
        Fixtures.check("Saved".equals(page.locator("#out").textContent()), "Saved expected after the healed click");
    }

    @org.junit.jupiter.api.Test
    public void healRenamedField() {
        page.navigate(Fixtures.url("v1.html"));
        healer.locator("Form.nameField", "#name").fill("Jane");
        page.navigate(Fixtures.url("v2.html"));
        healer.locator("Form.nameField", "#name").fill("Jane Doe");
        Fixtures.check("Jane Doe".equals(page.locator("#full-name").inputValue()), "the healed name field was filled");
    }

    @org.junit.jupiter.api.Test
    public void plainLanguageStep() {
        page.navigate(Fixtures.url("v2.html"));
        healer.find("Form.email", "the email field").fill("jane@example.com");
        Fixtures.check("jane@example.com".equals(page.locator("#mail").inputValue()), "the email field was filled");
    }

    @org.junit.jupiter.api.Test
    public void removedButtonNotHealed() {
        page.navigate(Fixtures.url("v1.html"));
        healer.locator("Form.cancel", "#cancel").click();
        page.navigate(Fixtures.url("v3.html"));
        Fixtures.expectFailure(() -> healer.locator("Form.cancel", "#cancel").click(), "a removed button must not be healed to another one");
        Fixtures.check(page.locator("#out").textContent().isEmpty(), "no other button was clicked");
    }

    @org.junit.jupiter.api.Test
    public void tripForgeLookup() {
        if (!Fixtures.sites()) return;
        new TripForgeLab(page, healer).open().findBooking("TFH-2026", "IPEK");
        if (!Fixtures.sites()) return;
        Fixtures.check(Fixtures.containsAll(new TripForgeLab(page, healer).text(), "TF-222", "Istanbul", "Madrid"),
                "itinerary TF-222 Istanbul -> Madrid expected");
    }

    @org.junit.jupiter.api.Test
    public void tripForgeVerification() {
        if (!Fixtures.sites()) return;
        new TripForgeLab(page, healer).open().findBooking("TFH-2026", "IPEK").confirmTraveller().completeVerification();
        if (!Fixtures.sites()) return;
        Fixtures.check(new TripForgeLab(page, healer).text().contains("SELF-HEALING-COMPLETE"), "business outcome expected");
    }

    @org.junit.jupiter.api.Test
    public void shopLabWrongPassword() {
        if (!Fixtures.sites()) return;
        new ShopLab(page, healer).openLogin().login("standard_user", "wrong-password");
        if (!Fixtures.sites()) return;
        Fixtures.check(new ShopLab(page, healer).errorText().contains("Invalid username or password"), "error message expected");
    }

    @org.junit.jupiter.api.Test
    public void shopLabSearchAndFilter() {
        if (!Fixtures.sites()) return;
        new ShopLab(page, healer).loginAsStandardUser().search("watch");
        if (!Fixtures.sites()) return;
        Fixtures.check(new ShopLab(page, healer).resultCount() == 1, "one watch expected");
        new ShopLab(page, healer).search("").filterByCategory("sports");
        Fixtures.check(new ShopLab(page, healer).resultCount() == 2, "two sports products expected");
    }

    @org.junit.jupiter.api.Test
    public void shopLabAddToCart() {
        if (!Fixtures.sites()) return;
        new ShopLab(page, healer).loginAsStandardUser().addToCart(8).addToCart(2);
        if (!Fixtures.sites()) return;
        Fixtures.check(new ShopLab(page, healer).cartCount() == 2, "two items in the cart badge expected");
    }

    @org.junit.jupiter.api.Test
    public void deliberateFailure() {
        page.navigate(Fixtures.url("v1.html"));
        Fixtures.failWhenAsked();
    }
}
