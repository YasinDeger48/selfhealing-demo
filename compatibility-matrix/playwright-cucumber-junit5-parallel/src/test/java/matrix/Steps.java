package matrix;

import io.cucumber.java.After;
import io.cucumber.java.Before;
import io.cucumber.java.en.Then;
import io.cucumber.java.en.When;

/** playwright + cucumber-junit5: glue for features/*.feature. The browser comes from healer.properties. */
public class Steps {

    // every thread its own browser, context, page and healer (TestNG shares one instance between threads)
    static final ThreadLocal<com.microsoft.playwright.Browser> BROWSER = ThreadLocal.withInitial(() -> {
        com.microsoft.playwright.Playwright playwright = com.microsoft.playwright.Playwright.create();
        Runtime.getRuntime().addShutdownHook(new Thread(playwright::close));
        return com.selfhealing.healer.playwright.HealerBrowser.launch(playwright);
    });
    static final ThreadLocal<com.microsoft.playwright.BrowserContext> CONTEXT = new ThreadLocal<>();
    static final ThreadLocal<com.microsoft.playwright.Page> PAGE = new ThreadLocal<>();
    static final ThreadLocal<com.selfhealing.healer.playwright.SelfHealingPage> HEALER = new ThreadLocal<>();

    @Before
    public void open() {
        System.out.println("[matrix-thread] " + Thread.currentThread().getName());
        CONTEXT.set(com.selfhealing.healer.playwright.HealerBrowser.newContext(BROWSER.get()));
        PAGE.set(CONTEXT.get().newPage());
        HEALER.set(com.selfhealing.healer.playwright.SelfHealingPage.wrap(PAGE.get()));
    }

    @After
    public void close() {
        com.selfhealing.healer.playwright.HealerBrowser.close(CONTEXT.get());
    }

    @When("I save on the original page and again on the changed page")
    public void save() {
        PAGE.get().navigate(Fixtures.url("v1.html"));
        HEALER.get().locator("Form.save", "#save").click();
        PAGE.get().navigate(Fixtures.url("v2.html"));
        HEALER.get().locator("Form.save", "#save").click();
    }

    @Then("the page says Saved")
    public void saved() {
        Fixtures.check("Saved".equals(PAGE.get().locator("#out").textContent()), "Saved expected after the healed click");
    }

    @When("I type my name on the original page and again on the changed page")
    public void type() {
        PAGE.get().navigate(Fixtures.url("v1.html"));
        HEALER.get().locator("Form.nameField", "#name").fill("Jane");
        PAGE.get().navigate(Fixtures.url("v2.html"));
        HEALER.get().locator("Form.nameField", "#name").fill("Jane Doe");
    }

    @Then("the changed name field has the value")
    public void typed() {
        Fixtures.check("Jane Doe".equals(PAGE.get().locator("#full-name").inputValue()), "the healed name field was filled");
    }

    @When("I fill the email field by its description")
    public void fill() {
        PAGE.get().navigate(Fixtures.url("v2.html"));
        HEALER.get().find("Form.email", "the email field").fill("jane@example.com");
    }

    @Then("the email field has the value")
    public void filled() {
        Fixtures.check("jane@example.com".equals(PAGE.get().locator("#mail").inputValue()), "the email field was filled");
    }

    @When("I cancel on the original page and open a page without the Cancel button")
    public void cancel() {
        PAGE.get().navigate(Fixtures.url("v1.html"));
        HEALER.get().locator("Form.cancel", "#cancel").click();
        PAGE.get().navigate(Fixtures.url("v3.html"));
    }

    @Then("no other button is used instead")
    public void notReplaced() {
        Fixtures.expectFailure(() -> HEALER.get().locator("Form.cancel", "#cancel").click(), "a removed button must not be healed to another one");
        Fixtures.check(PAGE.get().locator("#out").textContent().isEmpty(), "no other button was clicked");
    }

    @When("I look up the TripForge booking")
    public void lookUpBooking() {
        if (!Fixtures.sites()) return;
        new TripForgeLab(PAGE.get(), HEALER.get()).open().findBooking("TFH-2026", "IPEK");
    }

    @Then("the itinerary is shown")
    public void itineraryShown() {
        if (!Fixtures.sites()) return;
        Fixtures.check(Fixtures.containsAll(new TripForgeLab(PAGE.get(), HEALER.get()).text(), "TF-222", "Istanbul", "Madrid"),
                "itinerary TF-222 Istanbul -> Madrid expected");
    }

    @When("I complete the TripForge verification")
    public void completeVerification() {
        if (!Fixtures.sites()) return;
        new TripForgeLab(PAGE.get(), HEALER.get()).open().findBooking("TFH-2026", "IPEK").confirmTraveller().completeVerification();
    }

    @Then("the verification is complete")
    public void verificationComplete() {
        if (!Fixtures.sites()) return;
        Fixtures.check(new TripForgeLab(PAGE.get(), HEALER.get()).text().contains("SELF-HEALING-COMPLETE"), "business outcome expected");
    }

    @When("I log in to ShopLab with a wrong password")
    public void wrongPassword() {
        if (!Fixtures.sites()) return;
        new ShopLab(PAGE.get(), HEALER.get()).openLogin().login("standard_user", "wrong-password");
    }

    @Then("ShopLab shows a login error")
    public void loginError() {
        if (!Fixtures.sites()) return;
        Fixtures.check(new ShopLab(PAGE.get(), HEALER.get()).errorText().contains("Invalid username or password"), "error message expected");
    }

    @When("I log in to ShopLab and search for a watch")
    public void searchWatch() {
        if (!Fixtures.sites()) return;
        new ShopLab(PAGE.get(), HEALER.get()).loginAsStandardUser().search("watch");
    }

    @Then("the search and the category filter narrow the products")
    public void narrowed() {
        if (!Fixtures.sites()) return;
        Fixtures.check(new ShopLab(PAGE.get(), HEALER.get()).resultCount() == 1, "one watch expected");
        new ShopLab(PAGE.get(), HEALER.get()).search("").filterByCategory("sports");
        Fixtures.check(new ShopLab(PAGE.get(), HEALER.get()).resultCount() == 2, "two sports products expected");
    }

    @When("I log in to ShopLab and add two products to the cart")
    public void addTwo() {
        if (!Fixtures.sites()) return;
        new ShopLab(PAGE.get(), HEALER.get()).loginAsStandardUser().addToCart(8).addToCart(2);
    }

    @Then("the cart badge shows two items")
    public void badgeShowsTwo() {
        if (!Fixtures.sites()) return;
        Fixtures.check(new ShopLab(PAGE.get(), HEALER.get()).cartCount() == 2, "two items in the cart badge expected");
    }

    @Then("it fails when asked")
    public void failWhenAsked() {
        Fixtures.failWhenAsked();
    }
}
