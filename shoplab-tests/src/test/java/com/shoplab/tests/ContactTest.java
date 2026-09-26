package com.shoplab.tests;

import com.shoplab.tests.pages.ContactPage;
import com.shoplab.tests.pages.Header;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertTrue;

class ContactTest extends BaseTest {

    @BeforeEach
    void login() {
        loginAsStandardUser();
        new Header(healer).goToContact();
    }

    @Test
    void emptyFormShowsErrors() {
        ContactPage contact = new ContactPage(healer);
        contact.submit();
        assertTrue(contact.errorText().contains("is required"));
    }

    @Test
    void sendMessage() {
        ContactPage contact = new ContactPage(healer);
        contact.fill("Ada Lovelace", "ada@test.com", "order", "I would like to know the status of my order.");
        contact.submit();
        assertTrue(contact.successText().contains("by phone"));
    }

    @Test
    void logout() {
        new Header(healer).logout();
        page.waitForURL("**/login");
    }
}
