package com.shoplab.tests.pages;

import com.selfhealing.healer.playwright.HealingLocator;
import com.selfhealing.healer.playwright.SelfHealingPage;

public class ProductDetailPage {

    private final SelfHealingPage healer;
    private final HealingLocator name;
    private final HealingLocator sizeSelect;
    private final HealingLocator sizeError;
    private final HealingLocator quantityIncrease;
    private final HealingLocator addToCart;

    public ProductDetailPage(SelfHealingPage healer) {
        this.healer = healer;
        this.name = healer.locator("ProductDetailPage.name", "[data-testid='product-detail-name']");
        this.sizeSelect = healer.locator("ProductDetailPage.sizeSelect", "[data-testid='size-select']");
        this.sizeError = healer.locator("ProductDetailPage.sizeError", "#size-error");
        this.quantityIncrease = healer.locator("ProductDetailPage.quantityIncrease", "[aria-label='Increase quantity']");
        this.addToCart = healer.locator("ProductDetailPage.addToCart", "button:has-text('Add to Cart')");
    }

    public String productName() {
        return name.textContent().trim();
    }

    public void selectColor(String colorKey) {
        healer.locator("ProductDetailPage.color[" + colorKey + "]", "[data-testid='color-option-" + colorKey + "']").click();
    }

    public void selectSize(String size) {
        sizeSelect.selectOption(size);
    }

    public void increaseQuantity() {
        quantityIncrease.click();
    }

    public void addToCart() {
        addToCart.click();
    }

    public boolean sizeErrorVisible() {
        return sizeError.getAttribute("class").contains("visible");
    }
}
