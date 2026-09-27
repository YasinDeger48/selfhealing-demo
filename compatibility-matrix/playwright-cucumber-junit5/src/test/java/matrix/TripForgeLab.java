package matrix;

import com.microsoft.playwright.Locator;
import com.microsoft.playwright.Page;
import com.microsoft.playwright.options.LoadState;
import com.selfhealing.healer.playwright.SelfHealingPage;

/** The TripForge self-healing lab: selectors recorded from one old page load - every step is healed. */
public class TripForgeLab {

    public static final String URL = System.getProperty("tripforge.url", "https://trip-forge-lbuh.vercel.app") + "/self-healing-lab";

    private final Page page;
    private final SelfHealingPage healer;

    public TripForgeLab(Page page, SelfHealingPage healer) {
        this.page = page;
        this.healer = healer;
    }

    public TripForgeLab open() {
        healer.navigate(URL);
        page.waitForLoadState(LoadState.NETWORKIDLE);
        Locator accept = page.locator("[data-testid='cookie-accept']");   // not part of the experiment: stable test id
        if (accept.count() > 0 && accept.isVisible()) accept.click();
        return this;
    }

    public TripForgeLab findBooking(String reference, String surname) {
        healer.locator("Lab.bookingReference", "[data-testid='booking-reference-input-fe465c1e']").fill(reference);
        healer.locator("Lab.passengerSurname", "#passenger-surname-fe465c1e").fill(surname);
        healer.locator("Lab.findBookingButton", "[data-testid='find-booking-button-fe465c1e']").click();
        page.getByText("BOOKING FOUND").waitFor();
        return this;
    }

    public TripForgeLab confirmTraveller() {
        healer.locator("Lab.travellerConfirmation", "#traveller-confirmation-fe465c1e").check();
        healer.locator("Lab.reviewJourneyButton", "#finalize-journey-fe465c1e").click();
        page.getByText("FINAL CHECK").waitFor();
        return this;
    }

    public TripForgeLab completeVerification() {
        healer.locator("Lab.completeVerificationButton", "[data-testid='complete-verification-button-fe465c1e']").click();
        page.getByText("SELF-HEALING-COMPLETE").waitFor();
        return this;
    }

    public String text() {
        return page.locator("main").innerText();
    }
}
