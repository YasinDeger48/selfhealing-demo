package com.shoplab.tests;

import com.shoplab.tests.pages.LoginPage;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertTrue;

class LoginTest extends BaseTest {

    @Test
    void invalidPasswordShowsError() {
        LoginPage login = new LoginPage(healer).open(BASE_URL);
        login.loginAs("standard_user", "wrong-password");
        assertTrue(login.errorText().contains("Invalid username or password"), "error message expected");
    }

    @Test
    void validLoginOpensProducts() {
        new LoginPage(healer).open(BASE_URL).loginAs("standard_user", "secret123");
        page.waitForURL("**/products");
    }
}
