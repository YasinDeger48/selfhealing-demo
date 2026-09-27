package matrix;

/** selenium + testng: the same tests in every combination. The browser comes from healer.properties. */
public class HealingTest {

    static org.openqa.selenium.WebDriver driver;
    com.selfhealing.healer.selenium.SelfHealingDriver healer;

    @org.testng.annotations.BeforeMethod
    public void open() {
        if (driver == null) {
            driver = com.selfhealing.healer.selenium.HealerDriver.create();   // browser.name, browser.headless, browser.viewport, browser.timeoutMs
            Runtime.getRuntime().addShutdownHook(new Thread(driver::quit));
        }
        healer = com.selfhealing.healer.selenium.SelfHealingDriver.wrap(driver);
    }

    @org.testng.annotations.AfterMethod
    public void close() {
    }

    @org.testng.annotations.Test
    public void healRenamedButton() {
        driver.get(Fixtures.url("v1.html"));
        healer.element("Form.save", org.openqa.selenium.By.id("save")).click();
        driver.get(Fixtures.url("v2.html"));
        healer.element("Form.save", org.openqa.selenium.By.id("save")).click();
        Fixtures.check("Saved".equals(driver.findElement(org.openqa.selenium.By.id("out")).getText()), "Saved expected after the healed click");
    }

    @org.testng.annotations.Test
    public void healRenamedField() {
        driver.get(Fixtures.url("v1.html"));
        healer.element("Form.nameField", org.openqa.selenium.By.id("name")).fill("Jane");
        driver.get(Fixtures.url("v2.html"));
        healer.element("Form.nameField", org.openqa.selenium.By.id("name")).fill("Jane Doe");
        Fixtures.check("Jane Doe".equals(driver.findElement(org.openqa.selenium.By.id("full-name")).getDomProperty("value")),
                "the healed name field was filled");
    }

    @org.testng.annotations.Test
    public void plainLanguageStep() {
        driver.get(Fixtures.url("v2.html"));
        healer.find("Form.email", "the email field").fill("jane@example.com");
        Fixtures.check("jane@example.com".equals(driver.findElement(org.openqa.selenium.By.id("mail")).getDomProperty("value")),
                "the email field was filled");
    }

    @org.testng.annotations.Test
    public void removedButtonNotHealed() {
        driver.get(Fixtures.url("v1.html"));
        healer.element("Form.cancel", org.openqa.selenium.By.id("cancel")).click();
        driver.get(Fixtures.url("v3.html"));
        Fixtures.expectFailure(() -> healer.element("Form.cancel", org.openqa.selenium.By.id("cancel")).click(),
                "a removed button must not be healed to another one");
        Fixtures.check(driver.findElement(org.openqa.selenium.By.id("out")).getText().isEmpty(), "no other button was clicked");
    }

    @org.testng.annotations.Test
    public void tripForgeLookup() {
        if (!Fixtures.sites()) return;
        new TripForgeLab(driver, healer).open().findBooking("TFH-2026", "IPEK");
        if (!Fixtures.sites()) return;
        Fixtures.check(Fixtures.containsAll(new TripForgeLab(driver, healer).text(), "TF-222", "Istanbul", "Madrid"),
                "itinerary TF-222 Istanbul -> Madrid expected");
    }

    @org.testng.annotations.Test
    public void tripForgeVerification() {
        if (!Fixtures.sites()) return;
        new TripForgeLab(driver, healer).open().findBooking("TFH-2026", "IPEK").confirmTraveller().completeVerification();
        if (!Fixtures.sites()) return;
        Fixtures.check(new TripForgeLab(driver, healer).text().contains("SELF-HEALING-COMPLETE"), "business outcome expected");
    }

    @org.testng.annotations.Test
    public void shopLabWrongPassword() {
        if (!Fixtures.sites()) return;
        new ShopLab(driver, healer).openLogin().login("standard_user", "wrong-password");
        if (!Fixtures.sites()) return;
        Fixtures.check(new ShopLab(driver, healer).errorText().contains("Invalid username or password"), "error message expected");
    }

    @org.testng.annotations.Test
    public void shopLabSearchAndFilter() {
        if (!Fixtures.sites()) return;
        new ShopLab(driver, healer).loginAsStandardUser().search("watch");
        if (!Fixtures.sites()) return;
        Fixtures.check(new ShopLab(driver, healer).resultCount() == 1, "one watch expected");
        new ShopLab(driver, healer).search("").filterByCategory("sports");
        Fixtures.check(new ShopLab(driver, healer).resultCount() == 2, "two sports products expected");
    }

    @org.testng.annotations.Test
    public void shopLabAddToCart() {
        if (!Fixtures.sites()) return;
        new ShopLab(driver, healer).loginAsStandardUser().addToCart(1).addToCart(5);
        if (!Fixtures.sites()) return;
        Fixtures.check(new ShopLab(driver, healer).cartCount() == 2, "two items in the cart badge expected");
    }

    @org.testng.annotations.Test
    public void deliberateFailure() {
        driver.get(Fixtures.url("v1.html"));
        Fixtures.failWhenAsked();
    }
}
