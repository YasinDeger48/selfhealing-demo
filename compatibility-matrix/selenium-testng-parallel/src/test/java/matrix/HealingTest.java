package matrix;

/** selenium + testng: the same tests in every combination. The browser comes from healer.properties. */
public class HealingTest {

    // every thread its own browser and healer (TestNG shares one instance between threads)
    static final ThreadLocal<org.openqa.selenium.WebDriver> DRIVER = ThreadLocal.withInitial(() -> {
        org.openqa.selenium.WebDriver driver = com.selfhealing.healer.selenium.HealerDriver.create();
        Runtime.getRuntime().addShutdownHook(new Thread(driver::quit));
        return driver;
    });
    static final ThreadLocal<com.selfhealing.healer.selenium.SelfHealingDriver> HEALER = new ThreadLocal<>();

    @org.testng.annotations.BeforeMethod
    public void open() {
        System.out.println("[matrix-thread] " + Thread.currentThread().getName());
        HEALER.set(com.selfhealing.healer.selenium.SelfHealingDriver.wrap(DRIVER.get()));
    }

    @org.testng.annotations.AfterMethod
    public void close() {
    }

    @org.testng.annotations.Test
    public void healRenamedButton() {
        DRIVER.get().get(Fixtures.url("v1.html"));
        HEALER.get().element("Form.save", org.openqa.selenium.By.id("save")).click();
        DRIVER.get().get(Fixtures.url("v2.html"));
        HEALER.get().element("Form.save", org.openqa.selenium.By.id("save")).click();
        Fixtures.check("Saved".equals(DRIVER.get().findElement(org.openqa.selenium.By.id("out")).getText()), "Saved expected after the healed click");
    }

    @org.testng.annotations.Test
    public void healRenamedField() {
        DRIVER.get().get(Fixtures.url("v1.html"));
        HEALER.get().element("Form.nameField", org.openqa.selenium.By.id("name")).fill("Jane");
        DRIVER.get().get(Fixtures.url("v2.html"));
        HEALER.get().element("Form.nameField", org.openqa.selenium.By.id("name")).fill("Jane Doe");
        Fixtures.check("Jane Doe".equals(DRIVER.get().findElement(org.openqa.selenium.By.id("full-name")).getDomProperty("value")),
                "the healed name field was filled");
    }

    @org.testng.annotations.Test
    public void plainLanguageStep() {
        DRIVER.get().get(Fixtures.url("v2.html"));
        HEALER.get().find("Form.email", "the email field").fill("jane@example.com");
        Fixtures.check("jane@example.com".equals(DRIVER.get().findElement(org.openqa.selenium.By.id("mail")).getDomProperty("value")),
                "the email field was filled");
    }

    @org.testng.annotations.Test
    public void removedButtonNotHealed() {
        DRIVER.get().get(Fixtures.url("v1.html"));
        HEALER.get().element("Form.cancel", org.openqa.selenium.By.id("cancel")).click();
        DRIVER.get().get(Fixtures.url("v3.html"));
        Fixtures.expectFailure(() -> HEALER.get().element("Form.cancel", org.openqa.selenium.By.id("cancel")).click(),
                "a removed button must not be healed to another one");
        Fixtures.check(DRIVER.get().findElement(org.openqa.selenium.By.id("out")).getText().isEmpty(), "no other button was clicked");
    }

    @org.testng.annotations.Test
    public void tripForgeLookup() {
        if (!Fixtures.sites()) return;
        new TripForgeLab(DRIVER.get(), HEALER.get()).open().findBooking("TFH-2026", "IPEK");
        if (!Fixtures.sites()) return;
        Fixtures.check(Fixtures.containsAll(new TripForgeLab(DRIVER.get(), HEALER.get()).text(), "TF-222", "Istanbul", "Madrid"),
                "itinerary TF-222 Istanbul -> Madrid expected");
    }

    @org.testng.annotations.Test
    public void tripForgeVerification() {
        if (!Fixtures.sites()) return;
        new TripForgeLab(DRIVER.get(), HEALER.get()).open().findBooking("TFH-2026", "IPEK").confirmTraveller().completeVerification();
        if (!Fixtures.sites()) return;
        Fixtures.check(new TripForgeLab(DRIVER.get(), HEALER.get()).text().contains("SELF-HEALING-COMPLETE"), "business outcome expected");
    }

    @org.testng.annotations.Test
    public void shopLabWrongPassword() {
        if (!Fixtures.sites()) return;
        new ShopLab(DRIVER.get(), HEALER.get()).openLogin().login("standard_user", "wrong-password");
        if (!Fixtures.sites()) return;
        Fixtures.check(new ShopLab(DRIVER.get(), HEALER.get()).errorText().contains("Invalid username or password"), "error message expected");
    }

    @org.testng.annotations.Test
    public void shopLabSearchAndFilter() {
        if (!Fixtures.sites()) return;
        new ShopLab(DRIVER.get(), HEALER.get()).loginAsStandardUser().search("watch");
        if (!Fixtures.sites()) return;
        Fixtures.check(new ShopLab(DRIVER.get(), HEALER.get()).resultCount() == 1, "one watch expected");
        new ShopLab(DRIVER.get(), HEALER.get()).search("").filterByCategory("sports");
        Fixtures.check(new ShopLab(DRIVER.get(), HEALER.get()).resultCount() == 2, "two sports products expected");
    }

    @org.testng.annotations.Test
    public void shopLabAddToCart() {
        if (!Fixtures.sites()) return;
        new ShopLab(DRIVER.get(), HEALER.get()).loginAsStandardUser().addToCart(1).addToCart(5);
        if (!Fixtures.sites()) return;
        Fixtures.check(new ShopLab(DRIVER.get(), HEALER.get()).cartCount() == 2, "two items in the cart badge expected");
    }

    @org.testng.annotations.Test
    public void deliberateFailure() {
        DRIVER.get().get(Fixtures.url("v1.html"));
        Fixtures.failWhenAsked();
    }
}
