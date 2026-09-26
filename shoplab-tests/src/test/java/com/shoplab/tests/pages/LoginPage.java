package com.shoplab.tests.pages;

import com.selfhealing.healer.playwright.HealingLocator;
import com.selfhealing.healer.playwright.SelfHealingPage;

public class LoginPage {

    private final SelfHealingPage healer;
    private final HealingLocator username;
    private final HealingLocator password;
    private final HealingLocator loginButton;
    private final HealingLocator errorMessage;

    public LoginPage(SelfHealingPage healer) {
        this.healer = healer;
        this.username = healer.locator("LoginPage.username", "#login-username");
        this.password = healer.locator("LoginPage.password", "input[name='password']");
        this.loginButton = healer.locator("LoginPage.loginButton", "[data-testid='login-submit-button']");
        this.errorMessage = healer.locator("LoginPage.errorMessage", "[data-testid='login-error-message']");
    }

    public LoginPage open(String baseUrl) {
        healer.navigate(baseUrl + "/login");
        return this;
    }

    public void loginAs(String user, String pass) {
        username.fill(user);
        password.fill(pass);
        loginButton.click();
    }

    public String errorText() {
        return errorMessage.textContent().trim();
    }
}
