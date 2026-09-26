package com.shoplab.tests.pages;

import com.selfhealing.healer.playwright.HealingLocator;
import com.selfhealing.healer.playwright.SelfHealingPage;

public class CartPage {

    private final SelfHealingPage healer;
    private final HealingLocator couponInput;
    private final HealingLocator applyCoupon;
    private final HealingLocator couponMessage;
    private final HealingLocator total;
    private final HealingLocator firstName;
    private final HealingLocator lastName;
    private final HealingLocator address;
    private final HealingLocator city;
    private final HealingLocator postalCode;
    private final HealingLocator acceptTerms;
    private final HealingLocator placeOrder;
    private final HealingLocator checkoutError;
    private final HealingLocator orderSuccess;

    public CartPage(SelfHealingPage healer) {
        this.healer = healer;
        this.couponInput = healer.locator("CartPage.couponInput", "#coupon-code");
        this.applyCoupon = healer.locator("CartPage.applyCoupon", "[data-testid='apply-coupon-button']");
        this.couponMessage = healer.locator("CartPage.couponMessage", "[data-testid='coupon-message']");
        this.total = healer.locator("CartPage.total", "#summary-total");
        this.firstName = healer.locator("CartPage.firstName", "#first-name");
        this.lastName = healer.locator("CartPage.lastName", "[name='lastName']");
        this.address = healer.locator("CartPage.address", "[data-testid='checkout-address-input']");
        this.city = healer.locator("CartPage.city", "#city");
        this.postalCode = healer.locator("CartPage.postalCode", "[data-qa='postal-code']");
        this.acceptTerms = healer.locator("CartPage.acceptTerms", "#accept-terms");
        this.placeOrder = healer.locator("CartPage.placeOrder", "#place-order");
        this.checkoutError = healer.locator("CartPage.checkoutError", "[data-testid='checkout-error-message']");
        this.orderSuccess = healer.locator("CartPage.orderSuccess", "[data-testid='order-success-message']");
    }

    public int rowCount() {
        healer.page().locator("[data-qa='cart-item']").first().waitFor();
        return healer.page().locator("[data-qa='cart-item']").count();
    }

    public void applyCoupon(String code) {
        couponInput.fill(code);
        applyCoupon.click();
    }

    public String couponMessage() {
        return couponMessage.textContent().trim();
    }

    public String total() {
        return total.textContent().trim();
    }

    public void fillDelivery(String first, String last, String addr, String cityValue, String postal) {
        firstName.fill(first);
        lastName.fill(last);
        address.fill(addr);
        city.selectOption(cityValue);
        postalCode.fill(postal);
        acceptTerms.check();
    }

    public void placeOrder() {
        placeOrder.click();
    }

    public String checkoutError() {
        return checkoutError.textContent().trim();
    }

    public boolean orderPlaced() {
        orderSuccess.waitForVisible();
        return orderSuccess.isVisible();
    }
}
