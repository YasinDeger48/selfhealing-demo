package com.shoplab.selenium.pages;

import com.selfhealing.healer.selenium.HealingElement;
import com.selfhealing.healer.selenium.SelfHealingDriver;
import org.openqa.selenium.By;

public class LoginPage {

    private final SelfHealingDriver healer;
    private final HealingElement username;
    private final HealingElement password;
    private final HealingElement loginButton;
    private final HealingElement errorMessage;

    public LoginPage(SelfHealingDriver healer) {
        this.healer = healer;
        this.username = healer.element("LoginPage.username", By.id("login-username"));
        this.password = healer.element("LoginPage.password", By.name("password"));
        this.loginButton = healer.element("LoginPage.loginButton", By.cssSelector("[data-testid='login-submit-button']"));
        this.errorMessage = healer.element("LoginPage.errorMessage", By.cssSelector("[data-testid='login-error-message']"));
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
        return errorMessage.getText().trim();
    }
}
