package matrix;

import com.selfhealing.healer.selenium.SelfHealingDriver;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.ui.WebDriverWait;

import java.time.Duration;

/** The TripForge self-healing lab: selectors recorded from one old page load - every step is healed. */
public class TripForgeLab {

    public static final String URL = System.getProperty("tripforge.url", "https://trip-forge-lbuh.vercel.app") + "/self-healing-lab";

    private final WebDriver driver;
    private final SelfHealingDriver healer;

    public TripForgeLab(WebDriver driver, SelfHealingDriver healer) {
        this.driver = driver;
        this.healer = healer;
    }

    public TripForgeLab open() {
        healer.navigate(URL);
        waitUntil(d -> !d.findElements(By.cssSelector("main input")).isEmpty());   // the single-page app has rendered
        for (WebElement accept : driver.findElements(By.cssSelector("[data-testid='cookie-accept']"))) {
            if (accept.isDisplayed()) {
                accept.click();
                break;
            }
        }
        return this;
    }

    public TripForgeLab findBooking(String reference, String surname) {
        healer.element("Lab.bookingReference", By.cssSelector("[data-testid='booking-reference-input-fe465c1e']")).fill(reference);
        healer.element("Lab.passengerSurname", By.id("passenger-surname-fe465c1e")).fill(surname);
        healer.element("Lab.findBookingButton", By.cssSelector("[data-testid='find-booking-button-fe465c1e']")).click();
        waitForText("BOOKING FOUND");
        return this;
    }

    public TripForgeLab confirmTraveller() {
        healer.element("Lab.travellerConfirmation", By.id("traveller-confirmation-fe465c1e")).check();
        healer.element("Lab.reviewJourneyButton", By.id("finalize-journey-fe465c1e")).click();
        waitForText("FINAL CHECK");
        return this;
    }

    public TripForgeLab completeVerification() {
        healer.element("Lab.completeVerificationButton", By.cssSelector("[data-testid='complete-verification-button-fe465c1e']")).click();
        waitForText("SELF-HEALING-COMPLETE");
        return this;
    }

    public String text() {
        return driver.findElement(By.tagName("main")).getText();
    }

    private void waitForText(String text) {
        waitUntil(d -> d.findElement(By.tagName("body")).getText().contains(text));
    }

    private void waitUntil(java.util.function.Function<WebDriver, Boolean> condition) {
        new WebDriverWait(driver, Duration.ofSeconds(15)).until(condition::apply);
    }
}
