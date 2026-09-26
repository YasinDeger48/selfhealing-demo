package com.shoplab.tests;

import com.shoplab.tests.pages.Header;
import com.shoplab.tests.pages.ProductDetailPage;
import com.shoplab.tests.pages.ProductsPage;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

class ProductDetailTest extends BaseTest {

    @BeforeEach
    void login() {
        loginAsStandardUser();
    }

    @Test
    void sizeIsRequired() {
        new ProductsPage(healer).openProduct(4);
        ProductDetailPage detail = new ProductDetailPage(healer);
        assertEquals("Running Shoes", detail.productName());
        detail.addToCart();
        assertTrue(detail.sizeErrorVisible(), "size error expected");
    }

    @Test
    void addWithVariantAndQuantity() {
        new ProductsPage(healer).openProduct(4);
        ProductDetailPage detail = new ProductDetailPage(healer);
        detail.selectColor("blue");
        detail.selectSize("M");
        detail.increaseQuantity();
        detail.addToCart();
        assertEquals(2, new Header(healer).cartCount());
    }
}
