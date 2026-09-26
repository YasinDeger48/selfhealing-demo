package com.shoplab.tests;

import com.shoplab.tests.pages.Header;
import com.shoplab.tests.pages.ProductsPage;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;

class ProductsTest extends BaseTest {

    @BeforeEach
    void login() {
        loginAsStandardUser();
    }

    @Test
    void searchAndFilter() {
        ProductsPage products = new ProductsPage(healer);
        products.search("watch");
        assertEquals(1, products.resultCount());
        products.search("");
        products.filterByCategory("sports");
        assertEquals(2, products.resultCount());
    }

    @Test
    void sortByPrice() {
        ProductsPage products = new ProductsPage(healer);
        products.sortBy("price-asc");
        assertEquals("Coffee Mug", products.firstProductName());
    }

    @Test
    void addToCartUpdatesBadge() {
        ProductsPage products = new ProductsPage(healer);
        products.addToCart(8);
        products.addToCart(2);
        assertEquals(2, new Header(healer).cartCount());
    }
}
