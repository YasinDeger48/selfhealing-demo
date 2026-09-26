package com.shoplab.selenium;

import com.shoplab.selenium.pages.LoginPage;
import com.shoplab.selenium.pages.ProductsPage;
import org.junit.jupiter.api.Test;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;

import java.time.Duration;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

class ShopTest extends BaseTest {

    @Test
    void invalidPasswordShowsError() {
        LoginPage login = new LoginPage(healer).open(BASE_URL);
        login.loginAs("standard_user", "wrong-password");
        assertTrue(login.errorText().contains("Invalid username or password"), "error message expected");
    }

    @Test
    void searchAndFilter() {
        loginAsStandardUser();
        ProductsPage products = new ProductsPage(healer);
        products.search("watch");
        assertEquals(1, products.resultCount());
        products.search("");
        products.filterByCategory("sports");
        assertEquals(2, products.resultCount());
    }

    @Test
    void addToCartUpdatesBadge() {
        loginAsStandardUser();
        ProductsPage products = new ProductsPage(healer);
        products.addToCart(1);
        products.addToCart(5);
        assertEquals(2, products.cartCount());
    }

    @Test
    void logoutReturnsToLogin() {
        loginAsStandardUser();
        new ProductsPage(healer).logout();
        new WebDriverWait(driver, Duration.ofSeconds(10)).until(ExpectedConditions.urlContains("/login"));
    }
}
