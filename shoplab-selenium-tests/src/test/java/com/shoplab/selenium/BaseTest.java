package com.shoplab.selenium;

import com.selfhealing.healer.junit5.HealingExtension;
import com.selfhealing.healer.selenium.HealerDriver;
import com.selfhealing.healer.selenium.SelfHealingDriver;
import com.shoplab.selenium.pages.LoginPage;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.extension.ExtendWith;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;

import java.time.Duration;

/**
 * Browser lifecycle for the Selenium tests. Everything comes from the settings (src/test/resources/healer.properties,
 * environment variables or -D): app.baseUrl, browser.name (edge | chrome | firefox | safari), browser.headless,
 * browser.viewport, browser.timeoutMs. Selenium Manager downloads the matching driver automatically.
 */
@ExtendWith(HealingExtension.class)
public abstract class BaseTest {

    protected static final String BASE_URL = HealerDriver.baseUrl();

    protected WebDriver driver;
    protected SelfHealingDriver healer;

    @BeforeEach
    void openBrowser() {
        driver = HealerDriver.create();
        healer = SelfHealingDriver.wrap(driver);
    }

    @AfterEach
    void closeBrowser() {
        if (driver != null) driver.quit();
    }

    protected void loginAsStandardUser() {
        new LoginPage(healer).open(BASE_URL).loginAs("standard_user", "secret123");
        new WebDriverWait(driver, Duration.ofSeconds(10)).until(ExpectedConditions.urlContains("/products"));
    }
}
