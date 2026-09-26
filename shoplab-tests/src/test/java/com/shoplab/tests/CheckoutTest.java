package com.shoplab.tests;

import com.shoplab.tests.pages.CartPage;
import com.shoplab.tests.pages.Header;
import com.shoplab.tests.pages.ProductsPage;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

class CheckoutTest extends BaseTest {

    @BeforeEach
    void loginAndFillCart() {
        loginAsStandardUser();
        ProductsPage products = new ProductsPage(healer);
        products.addToCart(1);
        products.addToCart(5);
        new Header(healer).goToCart();
    }

    @Test
    void couponReducesTotal() {
        CartPage cart = new CartPage(healer);
        assertEquals(2, cart.rowCount());
        String before = cart.total();
        cart.applyCoupon("SAVE10");
        assertTrue(cart.couponMessage().contains("10% off"));
        assertTrue(!before.equals(cart.total()), "total should change after coupon");
    }

    @Test
    void checkoutValidationAndOrder() {
        CartPage cart = new CartPage(healer);
        cart.placeOrder();
        assertTrue(cart.checkoutError().contains("First name is required"));
        cart.fillDelivery("Ada", "Lovelace", "Test sokak 1", "istanbul", "34000");
        cart.placeOrder();
        assertTrue(cart.orderPlaced());
    }
}
