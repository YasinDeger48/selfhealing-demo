package matrix;

/** playwright + junit5: the same tests in every combination. The browser comes from healer.properties. */
public class HealingAgainTest {

    // every thread its own browser, context, page and healer (TestNG shares one instance between threads)
    static final ThreadLocal<com.microsoft.playwright.Browser> BROWSER = ThreadLocal.withInitial(() -> {
        com.microsoft.playwright.Playwright playwright = com.microsoft.playwright.Playwright.create();
        Runtime.getRuntime().addShutdownHook(new Thread(playwright::close));
        return com.selfhealing.healer.playwright.HealerBrowser.launch(playwright);
    });
    static final ThreadLocal<com.microsoft.playwright.BrowserContext> CONTEXT = new ThreadLocal<>();
    static final ThreadLocal<com.microsoft.playwright.Page> PAGE = new ThreadLocal<>();
    static final ThreadLocal<com.selfhealing.healer.playwright.SelfHealingPage> HEALER = new ThreadLocal<>();

    @org.junit.jupiter.api.BeforeEach
    public void open() {
        System.out.println("[matrix-thread] " + Thread.currentThread().getName());
        CONTEXT.set(com.selfhealing.healer.playwright.HealerBrowser.newContext(BROWSER.get()));
        PAGE.set(CONTEXT.get().newPage());
        HEALER.set(com.selfhealing.healer.playwright.SelfHealingPage.wrap(PAGE.get()));
    }

    @org.junit.jupiter.api.AfterEach
    public void close() {
        com.selfhealing.healer.playwright.HealerBrowser.close(CONTEXT.get());
    }

    @org.junit.jupiter.api.Test
    public void healRenamedButton() {
        PAGE.get().navigate(Fixtures.url("v1.html"));
        HEALER.get().locator("Form.save", "#save").click();
        PAGE.get().navigate(Fixtures.url("v2.html"));
        HEALER.get().locator("Form.save", "#save").click();
        Fixtures.check("Saved".equals(PAGE.get().locator("#out").textContent()), "Saved expected after the healed click");
    }

    @org.junit.jupiter.api.Test
    public void healRenamedField() {
        PAGE.get().navigate(Fixtures.url("v1.html"));
        HEALER.get().locator("Form.nameField", "#name").fill("Jane");
        PAGE.get().navigate(Fixtures.url("v2.html"));
        HEALER.get().locator("Form.nameField", "#name").fill("Jane Doe");
        Fixtures.check("Jane Doe".equals(PAGE.get().locator("#full-name").inputValue()), "the healed name field was filled");
    }

    @org.junit.jupiter.api.Test
    public void plainLanguageStep() {
        PAGE.get().navigate(Fixtures.url("v2.html"));
        HEALER.get().find("Form.email", "the email field").fill("jane@example.com");
        Fixtures.check("jane@example.com".equals(PAGE.get().locator("#mail").inputValue()), "the email field was filled");
    }

    @org.junit.jupiter.api.Test
    public void removedButtonNotHealed() {
        PAGE.get().navigate(Fixtures.url("v1.html"));
        HEALER.get().locator("Form.cancel", "#cancel").click();
        PAGE.get().navigate(Fixtures.url("v3.html"));
        Fixtures.expectFailure(() -> HEALER.get().locator("Form.cancel", "#cancel").click(), "a removed button must not be healed to another one");
        Fixtures.check(PAGE.get().locator("#out").textContent().isEmpty(), "no other button was clicked");
    }

    @org.junit.jupiter.api.Test
    public void tripForgeLookup() {
        if (!Fixtures.sites()) return;
        new TripForgeLab(PAGE.get(), HEALER.get()).open().findBooking("TFH-2026", "IPEK");
        if (!Fixtures.sites()) return;
        Fixtures.check(Fixtures.containsAll(new TripForgeLab(PAGE.get(), HEALER.get()).text(), "TF-222", "Istanbul", "Madrid"),
                "itinerary TF-222 Istanbul -> Madrid expected");
    }

    @org.junit.jupiter.api.Test
    public void tripForgeVerification() {
        if (!Fixtures.sites()) return;
        new TripForgeLab(PAGE.get(), HEALER.get()).open().findBooking("TFH-2026", "IPEK").confirmTraveller().completeVerification();
        if (!Fixtures.sites()) return;
        Fixtures.check(new TripForgeLab(PAGE.get(), HEALER.get()).text().contains("SELF-HEALING-COMPLETE"), "business outcome expected");
    }

    @org.junit.jupiter.api.Test
    public void shopLabWrongPassword() {
        if (!Fixtures.sites()) return;
        new ShopLab(PAGE.get(), HEALER.get()).openLogin().login("standard_user", "wrong-password");
        if (!Fixtures.sites()) return;
        Fixtures.check(new ShopLab(PAGE.get(), HEALER.get()).errorText().contains("Invalid username or password"), "error message expected");
    }

    @org.junit.jupiter.api.Test
    public void shopLabSearchAndFilter() {
        if (!Fixtures.sites()) return;
        new ShopLab(PAGE.get(), HEALER.get()).loginAsStandardUser().search("watch");
        if (!Fixtures.sites()) return;
        Fixtures.check(new ShopLab(PAGE.get(), HEALER.get()).resultCount() == 1, "one watch expected");
        new ShopLab(PAGE.get(), HEALER.get()).search("").filterByCategory("sports");
        Fixtures.check(new ShopLab(PAGE.get(), HEALER.get()).resultCount() == 2, "two sports products expected");
    }

    @org.junit.jupiter.api.Test
    public void shopLabAddToCart() {
        if (!Fixtures.sites()) return;
        new ShopLab(PAGE.get(), HEALER.get()).loginAsStandardUser().addToCart(8).addToCart(2);
        if (!Fixtures.sites()) return;
        Fixtures.check(new ShopLab(PAGE.get(), HEALER.get()).cartCount() == 2, "two items in the cart badge expected");
    }

    @org.junit.jupiter.api.Test
    public void deliberateFailure() {
        PAGE.get().navigate(Fixtures.url("v1.html"));
        Fixtures.failWhenAsked();
    }
}
