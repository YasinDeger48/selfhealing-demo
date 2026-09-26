package com.shoplab.tests.pages;

import com.selfhealing.healer.playwright.HealingLocator;
import com.selfhealing.healer.playwright.SelfHealingPage;

public class Header {

    private final HealingLocator cartBadge;
    private final HealingLocator cartLink;
    private final HealingLocator contactLink;
    private final HealingLocator logoutButton;

    public Header(SelfHealingPage healer) {
        this.cartBadge = healer.locator("Header.cartBadge", "#cart-count");
        this.cartLink = healer.locator("Header.cartLink", "[data-testid='nav-cart-link']");
        this.contactLink = healer.locator("Header.contactLink", "#nav-contact");
        this.logoutButton = healer.locator("Header.logoutButton", "button[data-testid='logout-button']");
    }

    public int cartCount() {
        return Integer.parseInt(cartBadge.textContent().trim());
    }

    public void goToCart() {
        cartLink.click();
    }

    public void goToContact() {
        contactLink.click();
    }

    public void logout() {
        logoutButton.click();
    }
}
