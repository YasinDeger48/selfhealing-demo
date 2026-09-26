package com.shoplab.tests.pages;

import com.selfhealing.healer.playwright.HealingLocator;
import com.selfhealing.healer.playwright.SelfHealingPage;

public class ContactPage {

    private final HealingLocator fullName;
    private final HealingLocator email;
    private final HealingLocator subject;
    private final HealingLocator phonePreference;
    private final HealingLocator message;
    private final HealingLocator submit;
    private final HealingLocator successMessage;
    private final HealingLocator errorMessage;

    public ContactPage(SelfHealingPage healer) {
        this.fullName = healer.locator("ContactPage.fullName", "#contact-name");
        this.email = healer.locator("ContactPage.email", "#contact-email");
        this.subject = healer.locator("ContactPage.subject", "[data-testid='contact-subject-select']");
        this.phonePreference = healer.locator("ContactPage.phonePreference", "#pref-phone");
        this.message = healer.locator("ContactPage.message", "textarea[name='message']");
        this.submit = healer.locator("ContactPage.submit", "button[data-qa='send-message']");
        this.successMessage = healer.locator("ContactPage.successMessage", "[data-testid='contact-success-message']");
        this.errorMessage = healer.locator("ContactPage.errorMessage", "[data-testid='contact-error-message']");
    }

    public void fill(String name, String mail, String subjectValue, String text) {
        fullName.fill(name);
        email.fill(mail);
        subject.selectOption(subjectValue);
        phonePreference.check();
        message.fill(text);
    }

    public void submit() {
        submit.click();
    }

    public String successText() {
        return successMessage.textContent().trim();
    }

    public String errorText() {
        return errorMessage.textContent().trim();
    }
}
