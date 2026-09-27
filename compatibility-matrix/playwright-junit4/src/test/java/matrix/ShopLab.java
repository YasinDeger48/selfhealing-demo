package matrix;

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
