package com.shoplab.selenium.pages;

import com.selfhealing.healer.selenium.HealingElement;
import com.selfhealing.healer.selenium.SelfHealingDriver;
import org.openqa.selenium.By;

public class ProductsPage {

    private final SelfHealingDriver healer;
    private final HealingElement search;
    private final HealingElement categoryFilter;
    private final HealingElement resultCount;
    private final HealingElement cartBadge;
    private final HealingElement logoutButton;

    public ProductsPage(SelfHealingDriver healer) {
        this.healer = healer;
        this.search = healer.element("ProductsPage.search", By.id("product-search"));
        this.categoryFilter = healer.element("ProductsPage.categoryFilter", By.cssSelector("[data-testid='category-filter-select']"));
        this.resultCount = healer.element("ProductsPage.resultCount", By.cssSelector("[data-testid='product-result-count']"));
        this.cartBadge = healer.element("Header.cartBadge", By.id("cart-count"));
        this.logoutButton = healer.element("Header.logoutButton", By.xpath("//button[@data-testid='logout-button']"));
    }

    public void search(String term) {
        search.fill(term);
    }

    public void filterByCategory(String value) {
        categoryFilter.selectByValue(value);
    }

    public int resultCount() {
        return Integer.parseInt(resultCount.getText().trim().split(" ")[0]);
    }

    public void addToCart(int productId) {
        healer.element("ProductsPage.addToCart[" + productId + "]", By.id("add-to-cart-" + productId)).click();
    }

    public int cartCount() {
        return Integer.parseInt(cartBadge.getText().trim());
    }

    public void logout() {
        logoutButton.click();
    }
}
