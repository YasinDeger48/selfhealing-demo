package matrix;

import io.cucumber.java.After;
import io.cucumber.java.Before;
import io.cucumber.java.en.Then;
import io.cucumber.java.en.When;

/** playwright + cucumber-testng: glue for features/*.feature. The browser comes from healer.properties. */
public class Steps {

    static com.microsoft.playwright.Playwright playwright;
    static com.microsoft.playwright.Browser browser;
    com.microsoft.playwright.BrowserContext context;
    com.microsoft.playwright.Page page;
    com.selfhealing.healer.playwright.SelfHealingPage healer;

    @Before
    public void open() {
        if (browser == null) {
            playwright = com.microsoft.playwright.Playwright.create();
            browser = com.selfhealing.healer.playwright.HealerBrowser.launch(playwright);   // browser.name, browser.headless, browser.slowmo
        }
        context = com.selfhealing.healer.playwright.HealerBrowser.newContext(browser);        // browser.viewport, timeoutMs, video, trace
        page = context.newPage();
        healer = com.selfhealing.healer.playwright.SelfHealingPage.wrap(page);
    }

    @After
    public void close() {
        com.selfhealing.healer.playwright.HealerBrowser.close(context);                       // keeps video / trace of a failed test
    }

    @When("I save on the original page and again on the changed page")
    public void save() {
        page.navigate(Fixtures.url("v1.html"));
        healer.locator("Form.save", "#save").click();
        page.navigate(Fixtures.url("v2.html"));
        healer.locator("Form.save", "#save").click();
    }

    @Then("the page says Saved")
    public void saved() {
        Fixtures.check("Saved".equals(page.locator("#out").textContent()), "Saved expected after the healed click");
    }

    @When("I type my name on the original page and again on the changed page")
    public void type() {
        page.navigate(Fixtures.url("v1.html"));
        healer.locator("Form.nameField", "#name").fill("Jane");
        page.navigate(Fixtures.url("v2.html"));
        healer.locator("Form.nameField", "#name").fill("Jane Doe");
    }

    @Then("the changed name field has the value")
    public void typed() {
        Fixtures.check("Jane Doe".equals(page.locator("#full-name").inputValue()), "the healed name field was filled");
    }

    @When("I fill the email field by its description")
    public void fill() {
        page.navigate(Fixtures.url("v2.html"));
        healer.find("Form.email", "the email field").fill("jane@example.com");
    }

    @Then("the email field has the value")
    public void filled() {
        Fixtures.check("jane@example.com".equals(page.locator("#mail").inputValue()), "the email field was filled");
    }

    @When("I cancel on the original page and open a page without the Cancel button")
    public void cancel() {
        page.navigate(Fixtures.url("v1.html"));
        healer.locator("Form.cancel", "#cancel").click();
        page.navigate(Fixtures.url("v3.html"));
    }

    @Then("no other button is used instead")
    public void notReplaced() {
        Fixtures.expectFailure(() -> healer.locator("Form.cancel", "#cancel").click(), "a removed button must not be healed to another one");
        Fixtures.check(page.locator("#out").textContent().isEmpty(), "no other button was clicked");
    }

    @When("I look up the TripForge booking")
    public void lookUpBooking() {
        if (!Fixtures.sites()) return;
        new TripForgeLab(page, healer).open().findBooking("TFH-2026", "IPEK");
    }

    @Then("the itinerary is shown")
    public void itineraryShown() {
        if (!Fixtures.sites()) return;
        Fixtures.check(Fixtures.containsAll(new TripForgeLab(page, healer).text(), "TF-222", "Istanbul", "Madrid"),
                "itinerary TF-222 Istanbul -> Madrid expected");
    }

    @When("I complete the TripForge verification")
    public void completeVerification() {
        if (!Fixtures.sites()) return;
        new TripForgeLab(page, healer).open().findBooking("TFH-2026", "IPEK").confirmTraveller().completeVerification();
    }

    @Then("the verification is complete")
    public void verificationComplete() {
        if (!Fixtures.sites()) return;
        Fixtures.check(new TripForgeLab(page, healer).text().contains("SELF-HEALING-COMPLETE"), "business outcome expected");
    }

    @When("I log in to ShopLab with a wrong password")
    public void wrongPassword() {
        if (!Fixtures.sites()) return;
        new ShopLab(page, healer).openLogin().login("standard_user", "wrong-password");
    }

    @Then("ShopLab shows a login error")
    public void loginError() {
        if (!Fixtures.sites()) return;
        Fixtures.check(new ShopLab(page, healer).errorText().contains("Invalid username or password"), "error message expected");
    }

    @When("I log in to ShopLab and search for a watch")
    public void searchWatch() {
        if (!Fixtures.sites()) return;
        new ShopLab(page, healer).loginAsStandardUser().search("watch");
    }

    @Then("the search and the category filter narrow the products")
    public void narrowed() {
        if (!Fixtures.sites()) return;
        Fixtures.check(new ShopLab(page, healer).resultCount() == 1, "one watch expected");
        new ShopLab(page, healer).search("").filterByCategory("sports");
        Fixtures.check(new ShopLab(page, healer).resultCount() == 2, "two sports products expected");
    }

    @When("I log in to ShopLab and add two products to the cart")
    public void addTwo() {
        if (!Fixtures.sites()) return;
        new ShopLab(page, healer).loginAsStandardUser().addToCart(8).addToCart(2);
    }

    @Then("the cart badge shows two items")
    public void badgeShowsTwo() {
        if (!Fixtures.sites()) return;
        Fixtures.check(new ShopLab(page, healer).cartCount() == 2, "two items in the cart badge expected");
    }

    @Then("it fails when asked")
    public void failWhenAsked() {
        Fixtures.failWhenAsked();
    }
}
