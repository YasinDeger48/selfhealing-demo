package matrix;

import io.cucumber.java.After;
import io.cucumber.java.Before;
import io.cucumber.java.en.Then;
import io.cucumber.java.en.When;

/** selenium + cucumber-testng: glue for features/*.feature. The browser comes from healer.properties. */
public class Steps {

    static org.openqa.selenium.WebDriver driver;
    com.selfhealing.healer.selenium.SelfHealingDriver healer;

    @Before
    public void open() {
        if (driver == null) {
            driver = com.selfhealing.healer.selenium.HealerDriver.create();   // browser.name, browser.headless, browser.viewport, browser.timeoutMs
            Runtime.getRuntime().addShutdownHook(new Thread(driver::quit));
        }
        healer = com.selfhealing.healer.selenium.SelfHealingDriver.wrap(driver);
    }

    @After
    public void close() {
    }

    @When("I save on the original page and again on the changed page")
    public void save() {
        driver.get(Fixtures.url("v1.html"));
        healer.element("Form.save", org.openqa.selenium.By.id("save")).click();
        driver.get(Fixtures.url("v2.html"));
        healer.element("Form.save", org.openqa.selenium.By.id("save")).click();
    }

    @Then("the page says Saved")
    public void saved() {
        Fixtures.check("Saved".equals(driver.findElement(org.openqa.selenium.By.id("out")).getText()), "Saved expected after the healed click");
    }

    @When("I type my name on the original page and again on the changed page")
    public void type() {
        driver.get(Fixtures.url("v1.html"));
        healer.element("Form.nameField", org.openqa.selenium.By.id("name")).fill("Jane");
        driver.get(Fixtures.url("v2.html"));
        healer.element("Form.nameField", org.openqa.selenium.By.id("name")).fill("Jane Doe");
    }

    @Then("the changed name field has the value")
    public void typed() {
        Fixtures.check("Jane Doe".equals(driver.findElement(org.openqa.selenium.By.id("full-name")).getDomProperty("value")),
                "the healed name field was filled");
    }

    @When("I fill the email field by its description")
    public void fill() {
        driver.get(Fixtures.url("v2.html"));
        healer.find("Form.email", "the email field").fill("jane@example.com");
    }

    @Then("the email field has the value")
    public void filled() {
        Fixtures.check("jane@example.com".equals(driver.findElement(org.openqa.selenium.By.id("mail")).getDomProperty("value")),
                "the email field was filled");
    }

    @When("I cancel on the original page and open a page without the Cancel button")
    public void cancel() {
        driver.get(Fixtures.url("v1.html"));
        healer.element("Form.cancel", org.openqa.selenium.By.id("cancel")).click();
        driver.get(Fixtures.url("v3.html"));
    }

    @Then("no other button is used instead")
    public void notReplaced() {
        Fixtures.expectFailure(() -> healer.element("Form.cancel", org.openqa.selenium.By.id("cancel")).click(),
                "a removed button must not be healed to another one");
        Fixtures.check(driver.findElement(org.openqa.selenium.By.id("out")).getText().isEmpty(), "no other button was clicked");
    }

    @When("I look up the TripForge booking")
    public void lookUpBooking() {
        if (!Fixtures.sites()) return;
        new TripForgeLab(driver, healer).open().findBooking("TFH-2026", "IPEK");
    }

    @Then("the itinerary is shown")
    public void itineraryShown() {
        if (!Fixtures.sites()) return;
        Fixtures.check(Fixtures.containsAll(new TripForgeLab(driver, healer).text(), "TF-222", "Istanbul", "Madrid"),
                "itinerary TF-222 Istanbul -> Madrid expected");
    }

    @When("I complete the TripForge verification")
    public void completeVerification() {
        if (!Fixtures.sites()) return;
        new TripForgeLab(driver, healer).open().findBooking("TFH-2026", "IPEK").confirmTraveller().completeVerification();
    }

    @Then("the verification is complete")
    public void verificationComplete() {
        if (!Fixtures.sites()) return;
        Fixtures.check(new TripForgeLab(driver, healer).text().contains("SELF-HEALING-COMPLETE"), "business outcome expected");
    }

    @When("I log in to ShopLab with a wrong password")
    public void wrongPassword() {
        if (!Fixtures.sites()) return;
        new ShopLab(driver, healer).openLogin().login("standard_user", "wrong-password");
    }

    @Then("ShopLab shows a login error")
    public void loginError() {
        if (!Fixtures.sites()) return;
        Fixtures.check(new ShopLab(driver, healer).errorText().contains("Invalid username or password"), "error message expected");
    }

    @When("I log in to ShopLab and search for a watch")
    public void searchWatch() {
        if (!Fixtures.sites()) return;
        new ShopLab(driver, healer).loginAsStandardUser().search("watch");
    }

    @Then("the search and the category filter narrow the products")
    public void narrowed() {
        if (!Fixtures.sites()) return;
        Fixtures.check(new ShopLab(driver, healer).resultCount() == 1, "one watch expected");
        new ShopLab(driver, healer).search("").filterByCategory("sports");
        Fixtures.check(new ShopLab(driver, healer).resultCount() == 2, "two sports products expected");
    }

    @When("I log in to ShopLab and add two products to the cart")
    public void addTwo() {
        if (!Fixtures.sites()) return;
        new ShopLab(driver, healer).loginAsStandardUser().addToCart(1).addToCart(5);
    }

    @Then("the cart badge shows two items")
    public void badgeShowsTwo() {
        if (!Fixtures.sites()) return;
        Fixtures.check(new ShopLab(driver, healer).cartCount() == 2, "two items in the cart badge expected");
    }

    @Then("it fails when asked")
    public void failWhenAsked() {
        Fixtures.failWhenAsked();
    }
}
