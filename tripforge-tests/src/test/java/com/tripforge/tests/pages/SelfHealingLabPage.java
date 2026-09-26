package com.tripforge.tests.pages;

import com.microsoft.playwright.Locator;
import com.microsoft.playwright.Page;
import com.microsoft.playwright.options.LoadState;
import com.selfhealing.healer.playwright.HealingLocator;
import com.selfhealing.healer.playwright.SelfHealingPage;

/**
 * The TripForge "Self-Healing Lab": every page load generates new ids, test ids, names and classes
 * (a random 8-character suffix), renames labels and reorders the fields.
 *
 * <p>The selectors below were recorded from ONE load (suffix {@code fe465c1e}) - exactly like a test
 * written yesterday against a build that has since changed. They never match again, so every step is
 * healed: the framework derives a fingerprint from the selector, finds the element, and learns its real
 * fingerprint for the next runs. Decoys on the page ("Example reservation", "Find example booking",
 * "Approve journey details", "Go back") must not be picked.
 */
public class SelfHealingLabPage {

    public static final String PATH = "/self-healing-lab";

    private final Page page;
    private final SelfHealingPage healer;

    // Selector styles are mixed on purpose: data-testid, #id and name attributes.
    private final HealingLocator bookingReference;
    private final HealingLocator surname;
    private final HealingLocator findBooking;
    private final HealingLocator travellerConfirmation;
    private final HealingLocator reviewJourney;
    private final HealingLocator completeVerification;

    public SelfHealingLabPage(Page page, SelfHealingPage healer) {
        this.page = page;
        this.healer = healer;
        this.bookingReference = healer.locator("Lab.bookingReference", "[data-testid='booking-reference-input-fe465c1e']");
        this.surname = healer.locator("Lab.passengerSurname", "#passenger-surname-fe465c1e");
        this.findBooking = healer.locator("Lab.findBookingButton", "[data-testid='find-booking-button-fe465c1e']");
        this.travellerConfirmation = healer.locator("Lab.travellerConfirmation", "#traveller-confirmation-fe465c1e");
        this.reviewJourney = healer.locator("Lab.reviewJourneyButton", "#finalize-journey-fe465c1e");
        this.completeVerification = healer.locator("Lab.completeVerificationButton", "[data-testid='complete-verification-button-fe465c1e']");
    }

    /** Opens the lab (a fresh set of locators every time) and accepts the cookie notice. */
    public SelfHealingLabPage open(String baseUrl) {
        healer.navigate(baseUrl + PATH);
        page.waitForLoadState(LoadState.NETWORKIDLE);
        // The cookie notice is not part of the experiment: its test id is stable.
        Locator accept = page.locator("[data-testid='cookie-accept']");
        if (accept.count() > 0 && accept.isVisible()) accept.click();
        return this;
    }

    public SelfHealingLabPage findBooking(String reference, String lastName) {
        bookingReference.fill(reference);
        surname.fill(lastName);
        findBooking.click();
        page.getByText("BOOKING FOUND").waitFor();
        return this;
    }

    public SelfHealingLabPage confirmTraveller() {
        travellerConfirmation.check();
        reviewJourney.click();
        page.getByText("FINAL CHECK").waitFor();
        return this;
    }

    public void completeVerification() {
        completeVerification.click();
        page.getByText("SELF-HEALING-COMPLETE").waitFor();
    }

    public String mainText() {
        return page.locator("main").innerText();
    }
}
