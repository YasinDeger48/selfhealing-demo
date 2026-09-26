package com.tripforge.tests;

import com.tripforge.tests.pages.SelfHealingLabPage;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertTrue;

/**
 * Three scenarios against https://trip-forge-lbuh.vercel.app/self-healing-lab. Every test passes with
 * WARN entries in the report: each healed locator is something a person should review.
 */
class SelfHealingLabTest extends BaseTest {

    private static final String REFERENCE = "TFH-2026";
    private static final String SURNAME = "IPEK";

    @Test
    @DisplayName("1. Booking lookup shows the itinerary")
    void lookupShowsItinerary() {
        SelfHealingLabPage lab = new SelfHealingLabPage(page, healer).open(BASE_URL).findBooking(REFERENCE, SURNAME);
        String text = lab.mainText();
        assertTrue(text.contains("TF-222"), "flight number expected");
        assertTrue(text.contains("Istanbul") && text.contains("Madrid"), "route Istanbul -> Madrid expected");
    }

    @Test
    @DisplayName("2. Full verification reaches SELF-HEALING-COMPLETE")
    void fullVerificationCompletes() {
        SelfHealingLabPage lab = new SelfHealingLabPage(page, healer).open(BASE_URL);
        lab.findBooking(REFERENCE, SURNAME).confirmTraveller().completeVerification();
        assertTrue(lab.mainText().contains("SELF-HEALING-COMPLETE"), "business outcome expected");
    }

    @Test
    @DisplayName("3. Three reloads, three different locator sets")
    void survivesRepeatedReloads() {
        for (int load = 1; load <= 3; load++) {
            SelfHealingLabPage lab = new SelfHealingLabPage(page, healer).open(BASE_URL);
            lab.findBooking(REFERENCE, SURNAME).confirmTraveller().completeVerification();
            assertTrue(lab.mainText().contains("SELF-HEALING-COMPLETE"), "load " + load + " should complete");
        }
    }
}
