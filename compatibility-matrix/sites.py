"""Real-site scenarios for every matrix project (imported by generate.py).

TripForge (https://trip-forge-lbuh.vercel.app/self-healing-lab): every page load generates new ids, test ids, names
and classes - the selectors below are from ONE old load, so every step is healed from a cold start. Decoys on the page
must not be picked.
ShopLab (../demo-site, http://localhost:8080): the same keys and selectors as ../shoplab-tests and
../shoplab-selenium-tests, whose recorded fingerprints run_all.py puts into the store - "recorded yesterday" - before
it breaks the site with mutate.py --level high.
Override the addresses with -Dtripforge.url=... / -Dshoplab.url=... ; -Dmatrix.skipSites=true skips these scenarios.
"""

# test method -> Cucumber scenario
TESTS = {
    "tripForgeLookup": "TripForge - booking lookup shows the itinerary",
    "tripForgeVerification": "TripForge - full verification completes",
    "shopLabWrongPassword": "ShopLab - a wrong password shows an error",
    "shopLabSearchAndFilter": "ShopLab - search and filter",
    "shopLabAddToCart": "ShopLab - adding to the cart updates the badge",
}

# (when, then) per driver - "page, healer" / "driver, healer" are swapped for the thread-local versions when parallel
_G = "        if (!Fixtures.sites()) return;\n"
BODIES = {
    "playwright": {
        "tripForgeLookup": (_G + """        new TripForgeLab(page, healer).open().findBooking("TFH-2026", "IPEK");
""", _G + """        Fixtures.check(Fixtures.containsAll(new TripForgeLab(page, healer).text(), "TF-222", "Istanbul", "Madrid"),
                "itinerary TF-222 Istanbul -> Madrid expected");
"""),
        "tripForgeVerification": (_G + """        new TripForgeLab(page, healer).open().findBooking("TFH-2026", "IPEK").confirmTraveller().completeVerification();
""", _G + """        Fixtures.check(new TripForgeLab(page, healer).text().contains("SELF-HEALING-COMPLETE"), "business outcome expected");
"""),
        "shopLabWrongPassword": (_G + """        new ShopLab(page, healer).openLogin().login("standard_user", "wrong-password");
""", _G + """        Fixtures.check(new ShopLab(page, healer).errorText().contains("Invalid username or password"), "error message expected");
"""),
        "shopLabSearchAndFilter": (_G + """        new ShopLab(page, healer).loginAsStandardUser().search("watch");
""", _G + """        Fixtures.check(new ShopLab(page, healer).resultCount() == 1, "one watch expected");
        new ShopLab(page, healer).search("").filterByCategory("sports");
        Fixtures.check(new ShopLab(page, healer).resultCount() == 2, "two sports products expected");
"""),
        "shopLabAddToCart": (_G + """        new ShopLab(page, healer).loginAsStandardUser().addToCart(8).addToCart(2);
""", _G + """        Fixtures.check(new ShopLab(page, healer).cartCount() == 2, "two items in the cart badge expected");
"""),
    },
    "selenium": {
        "tripForgeLookup": (_G + """        new TripForgeLab(driver, healer).open().findBooking("TFH-2026", "IPEK");
""", _G + """        Fixtures.check(Fixtures.containsAll(new TripForgeLab(driver, healer).text(), "TF-222", "Istanbul", "Madrid"),
                "itinerary TF-222 Istanbul -> Madrid expected");
"""),
        "tripForgeVerification": (_G + """        new TripForgeLab(driver, healer).open().findBooking("TFH-2026", "IPEK").confirmTraveller().completeVerification();
""", _G + """        Fixtures.check(new TripForgeLab(driver, healer).text().contains("SELF-HEALING-COMPLETE"), "business outcome expected");
"""),
        "shopLabWrongPassword": (_G + """        new ShopLab(driver, healer).openLogin().login("standard_user", "wrong-password");
""", _G + """        Fixtures.check(new ShopLab(driver, healer).errorText().contains("Invalid username or password"), "error message expected");
"""),
        "shopLabSearchAndFilter": (_G + """        new ShopLab(driver, healer).loginAsStandardUser().search("watch");
""", _G + """        Fixtures.check(new ShopLab(driver, healer).resultCount() == 1, "one watch expected");
        new ShopLab(driver, healer).search("").filterByCategory("sports");
        Fixtures.check(new ShopLab(driver, healer).resultCount() == 2, "two sports products expected");
"""),
        "shopLabAddToCart": (_G + """        new ShopLab(driver, healer).loginAsStandardUser().addToCart(1).addToCart(5);
""", _G + """        Fixtures.check(new ShopLab(driver, healer).cartCount() == 2, "two items in the cart badge expected");
"""),
    },
}

FEATURE = """
  Scenario: TripForge - booking lookup shows the itinerary
    When I look up the TripForge booking
    Then the itinerary is shown

  Scenario: TripForge - full verification completes
    When I complete the TripForge verification
    Then the verification is complete

  Scenario: ShopLab - a wrong password shows an error
    When I log in to ShopLab with a wrong password
    Then ShopLab shows a login error

  Scenario: ShopLab - search and filter
    When I log in to ShopLab and search for a watch
    Then the search and the category filter narrow the products

  Scenario: ShopLab - adding to the cart updates the badge
    When I log in to ShopLab and add two products to the cart
    Then the cart badge shows two items
"""

STEPS = [  # (annotation, method, test, part)
    ('@When("I look up the TripForge booking")', "lookUpBooking", "tripForgeLookup", 0),
    ('@Then("the itinerary is shown")', "itineraryShown", "tripForgeLookup", 1),
    ('@When("I complete the TripForge verification")', "completeVerification", "tripForgeVerification", 0),
    ('@Then("the verification is complete")', "verificationComplete", "tripForgeVerification", 1),
    ('@When("I log in to ShopLab with a wrong password")', "wrongPassword", "shopLabWrongPassword", 0),
    ('@Then("ShopLab shows a login error")', "loginError", "shopLabWrongPassword", 1),
    ('@When("I log in to ShopLab and search for a watch")', "searchWatch", "shopLabSearchAndFilter", 0),
    ('@Then("the search and the category filter narrow the products")', "narrowed", "shopLabSearchAndFilter", 1),
    ('@When("I log in to ShopLab and add two products to the cart")', "addTwo", "shopLabAddToCart", 0),
    ('@Then("the cart badge shows two items")', "badgeShowsTwo", "shopLabAddToCart", 1),
]

JAVA = {
    "playwright": {
        "TripForgeLab.java": """package matrix;

import com.microsoft.playwright.Locator;
import com.microsoft.playwright.Page;
import com.microsoft.playwright.options.LoadState;
import com.selfhealing.healer.playwright.SelfHealingPage;

/** The TripForge self-healing lab: selectors recorded from one old page load - every step is healed. */
public class TripForgeLab {

    public static final String URL = System.getProperty("tripforge.url", "https://trip-forge-lbuh.vercel.app") + "/self-healing-lab";

    private final Page page;
    private final SelfHealingPage healer;

    public TripForgeLab(Page page, SelfHealingPage healer) {
        this.page = page;
        this.healer = healer;
    }

    public TripForgeLab open() {
        healer.navigate(URL);
        page.waitForLoadState(LoadState.NETWORKIDLE);
        Locator accept = page.locator("[data-testid='cookie-accept']");   // not part of the experiment: stable test id
        if (accept.count() > 0 && accept.isVisible()) accept.click();
        return this;
    }

    public TripForgeLab findBooking(String reference, String surname) {
        healer.locator("Lab.bookingReference", "[data-testid='booking-reference-input-fe465c1e']").fill(reference);
        healer.locator("Lab.passengerSurname", "#passenger-surname-fe465c1e").fill(surname);
        healer.locator("Lab.findBookingButton", "[data-testid='find-booking-button-fe465c1e']").click();
        page.getByText("BOOKING FOUND").waitFor();
        return this;
    }

    public TripForgeLab confirmTraveller() {
        healer.locator("Lab.travellerConfirmation", "#traveller-confirmation-fe465c1e").check();
        healer.locator("Lab.reviewJourneyButton", "#finalize-journey-fe465c1e").click();
        page.getByText("FINAL CHECK").waitFor();
        return this;
    }

    public TripForgeLab completeVerification() {
        healer.locator("Lab.completeVerificationButton", "[data-testid='complete-verification-button-fe465c1e']").click();
        page.getByText("SELF-HEALING-COMPLETE").waitFor();
        return this;
    }

    public String text() {
        return page.locator("main").innerText();
    }
}
""",
        "ShopLab.java": """package matrix;

import com.microsoft.playwright.Page;
import com.selfhealing.healer.playwright.SelfHealingPage;

/** ShopLab demo shop: the keys and selectors of ../shoplab-tests (their recorded fingerprints are used). */
public class ShopLab {

    public static final String URL = System.getProperty("shoplab.url", "http://localhost:8080");

    private final Page page;
    private final SelfHealingPage healer;

    public ShopLab(Page page, SelfHealingPage healer) {
        this.page = page;
        this.healer = healer;
    }

    public ShopLab openLogin() {
        healer.navigate(URL + "/login");
        page.waitForSelector("form input");   // the single-page app has rendered the form
        return this;
    }

    public ShopLab login(String user, String password) {
        healer.locator("LoginPage.username", "#login-username").fill(user);
        healer.locator("LoginPage.password", "input[name='password']").fill(password);
        healer.locator("LoginPage.loginButton", "[data-testid='login-submit-button']").click();
        return this;
    }

    public ShopLab loginAsStandardUser() {
        openLogin().login("standard_user", "secret123");
        page.waitForURL("**/products");
        return this;
    }

    public String errorText() {
        return healer.locator("LoginPage.errorMessage", "[data-testid='login-error-message']").textContent().trim();
    }

    public ShopLab search(String term) {
        healer.locator("ProductsPage.search", "#product-search").fill(term);
        return this;
    }

    public ShopLab filterByCategory(String category) {
        healer.locator("ProductsPage.categoryFilter", "[data-testid='category-filter-select']").selectOption(category);
        return this;
    }

    public int resultCount() {
        return Integer.parseInt(healer.locator("ProductsPage.resultCount", "[data-testid='product-result-count']").textContent().trim().split(" ")[0]);
    }

    public ShopLab addToCart(int productId) {
        healer.locator("ProductsPage.addToCart[" + productId + "]", "#add-to-cart-" + productId).click();
        return this;
    }

    public int cartCount() {
        return Integer.parseInt(healer.locator("Header.cartBadge", "#cart-count").textContent().trim());
    }
}
""",
    },
    "selenium": {
        "TripForgeLab.java": """package matrix;

import com.selfhealing.healer.selenium.SelfHealingDriver;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.ui.WebDriverWait;

import java.time.Duration;

/** The TripForge self-healing lab: selectors recorded from one old page load - every step is healed. */
public class TripForgeLab {

    public static final String URL = System.getProperty("tripforge.url", "https://trip-forge-lbuh.vercel.app") + "/self-healing-lab";

    private final WebDriver driver;
    private final SelfHealingDriver healer;

    public TripForgeLab(WebDriver driver, SelfHealingDriver healer) {
        this.driver = driver;
        this.healer = healer;
    }

    public TripForgeLab open() {
        healer.navigate(URL);
        waitUntil(d -> !d.findElements(By.cssSelector("main input")).isEmpty());   // the single-page app has rendered
        for (WebElement accept : driver.findElements(By.cssSelector("[data-testid='cookie-accept']"))) {
            if (accept.isDisplayed()) {
                accept.click();
                break;
            }
        }
        return this;
    }

    public TripForgeLab findBooking(String reference, String surname) {
        healer.element("Lab.bookingReference", By.cssSelector("[data-testid='booking-reference-input-fe465c1e']")).fill(reference);
        healer.element("Lab.passengerSurname", By.id("passenger-surname-fe465c1e")).fill(surname);
        healer.element("Lab.findBookingButton", By.cssSelector("[data-testid='find-booking-button-fe465c1e']")).click();
        waitForText("BOOKING FOUND");
        return this;
    }

    public TripForgeLab confirmTraveller() {
        healer.element("Lab.travellerConfirmation", By.id("traveller-confirmation-fe465c1e")).check();
        healer.element("Lab.reviewJourneyButton", By.id("finalize-journey-fe465c1e")).click();
        waitForText("FINAL CHECK");
        return this;
    }

    public TripForgeLab completeVerification() {
        healer.element("Lab.completeVerificationButton", By.cssSelector("[data-testid='complete-verification-button-fe465c1e']")).click();
        waitForText("SELF-HEALING-COMPLETE");
        return this;
    }

    public String text() {
        return driver.findElement(By.tagName("main")).getText();
    }

    private void waitForText(String text) {
        waitUntil(d -> d.findElement(By.tagName("body")).getText().contains(text));
    }

    private void waitUntil(java.util.function.Function<WebDriver, Boolean> condition) {
        new WebDriverWait(driver, Duration.ofSeconds(15)).until(condition::apply);
    }
}
""",
        "ShopLab.java": """package matrix;

import com.selfhealing.healer.selenium.SelfHealingDriver;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;

import java.time.Duration;

/** ShopLab demo shop: the keys and selectors of ../shoplab-selenium-tests (their recorded fingerprints are used). */
public class ShopLab {

    public static final String URL = System.getProperty("shoplab.url", "http://localhost:8080");

    private final WebDriver driver;
    private final SelfHealingDriver healer;

    public ShopLab(WebDriver driver, SelfHealingDriver healer) {
        this.driver = driver;
        this.healer = healer;
    }

    public ShopLab openLogin() {
        // one browser for all tests: start logged out with an empty cart (the shop keeps both in the browser)
        healer.navigate(URL + "/login");
        ((org.openqa.selenium.JavascriptExecutor) driver).executeScript("window.localStorage.clear(); window.sessionStorage.clear();");
        driver.manage().deleteAllCookies();
        healer.navigate(URL + "/login");
        // the single-page app has rendered the form
        new WebDriverWait(driver, Duration.ofSeconds(10)).until(d -> !d.findElements(By.cssSelector("form input")).isEmpty());
        return this;
    }

    public ShopLab login(String user, String password) {
        healer.element("LoginPage.username", By.id("login-username")).fill(user);
        healer.element("LoginPage.password", By.name("password")).fill(password);
        healer.element("LoginPage.loginButton", By.cssSelector("[data-testid='login-submit-button']")).click();
        return this;
    }

    public ShopLab loginAsStandardUser() {
        openLogin().login("standard_user", "secret123");
        new WebDriverWait(driver, Duration.ofSeconds(10)).until(ExpectedConditions.urlContains("/products"));
        return this;
    }

    public String errorText() {
        return healer.element("LoginPage.errorMessage", By.cssSelector("[data-testid='login-error-message']")).getText().trim();
    }

    public ShopLab search(String term) {
        healer.element("ProductsPage.search", By.id("product-search")).fill(term);
        return this;
    }

    public ShopLab filterByCategory(String category) {
        healer.element("ProductsPage.categoryFilter", By.cssSelector("[data-testid='category-filter-select']")).selectByValue(category);
        return this;
    }

    public int resultCount() {
        return Integer.parseInt(healer.element("ProductsPage.resultCount", By.cssSelector("[data-testid='product-result-count']"))
                .getText().trim().split(" ")[0]);
    }

    public ShopLab addToCart(int productId) {
        healer.element("ProductsPage.addToCart[" + productId + "]", By.id("add-to-cart-" + productId)).click();
        return this;
    }

    public int cartCount() {
        return Integer.parseInt(healer.element("Header.cartBadge", By.id("cart-count")).getText().trim());
    }
}
""",
    },
}
