package com.shoplab.tests.pages;

import com.selfhealing.healer.playwright.HealingLocator;
import com.selfhealing.healer.playwright.SelfHealingPage;

public class ProductsPage {

    private final SelfHealingPage healer;
    private final HealingLocator search;
    private final HealingLocator categoryFilter;
    private final HealingLocator sort;
    private final HealingLocator resultCount;

    public ProductsPage(SelfHealingPage healer) {
        this.healer = healer;
        this.search = healer.locator("ProductsPage.search", "#product-search");
        this.categoryFilter = healer.locator("ProductsPage.categoryFilter", "[data-testid='category-filter-select']");
        this.sort = healer.locator("ProductsPage.sort", "#sort-select");
        this.resultCount = healer.locator("ProductsPage.resultCount", "[data-testid='product-result-count']");
    }

    public void search(String term) {
        search.fill(term);
    }

    public void filterByCategory(String category) {
        categoryFilter.selectOption(category);
    }

    public void sortBy(String option) {
        sort.selectOption(option);
    }

    public int resultCount() {
        return Integer.parseInt(resultCount.textContent().trim().split(" ")[0]);
    }

    public void addToCart(int productId) {
        healer.locator("ProductsPage.addToCart[" + productId + "]", "#add-to-cart-" + productId).click();
    }

    public void openProduct(int productId) {
        healer.locator("ProductsPage.viewProduct[" + productId + "]", "[data-testid='view-product-" + productId + "']").click();
    }

    public String firstProductName() {
        return healer.page().locator("[data-qa='product-title']").first().textContent();
    }
}
