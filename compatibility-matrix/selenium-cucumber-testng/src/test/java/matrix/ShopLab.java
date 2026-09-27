package matrix;

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
