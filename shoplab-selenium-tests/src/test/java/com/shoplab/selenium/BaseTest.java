package com.shoplab.selenium;

import com.selfhealing.healer.selenium.SeleniumHealingExtension;
import com.selfhealing.healer.selenium.SelfHealingDriver;
import com.shoplab.selenium.pages.LoginPage;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.extension.ExtendWith;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;
import org.openqa.selenium.edge.EdgeDriver;
import org.openqa.selenium.edge.EdgeOptions;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;

import java.time.Duration;

/**
 * Browser lifecycle for the Selenium tests. System properties: {@code shoplab.baseUrl} (default http://localhost:8080),
 * {@code browser} (edge | chrome, default edge), {@code headless} (default true).
 * Selenium Manager downloads the matching driver automatically.
 */
@ExtendWith(SeleniumHealingExtension.class)
public abstract class BaseTest {

    protected static final String BASE_URL = System.getProperty("shoplab.baseUrl", "http://localhost:8080");

    protected WebDriver driver;
    protected SelfHealingDriver healer;

    @BeforeEach
    void openBrowser() {
        boolean headless = Boolean.parseBoolean(System.getProperty("headless", "true"));
        if ("chrome".equals(System.getProperty("browser", "edge"))) {
            ChromeOptions o = new ChromeOptions().addArguments("--window-size=1280,900");
            if (headless) o.addArguments("--headless=new");
            driver = new ChromeDriver(o);
        } else {
            EdgeOptions o = new EdgeOptions().addArguments("--window-size=1280,900");
            if (headless) o.addArguments("--headless=new");
            driver = new EdgeDriver(o);
        }
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
