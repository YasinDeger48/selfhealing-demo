package com.tripforge.testng;

import com.tripforge.testng.pages.SelfHealingLabPage;
import org.testng.annotations.DataProvider;
import org.testng.annotations.Test;

import static org.testng.Assert.assertTrue;

/** Every page load generates new ids: each test is healed, and passes with WARN entries in the report. */
public class SelfHealingLabTest extends BaseTest {

    private static final String REFERENCE = "TFH-2026";
    private static final String SURNAME = "IPEK";

    @Test(description = "Booking lookup shows the itinerary")
    public void lookupShowsItinerary() {
        SelfHealingLabPage lab = new SelfHealingLabPage(page, healer).open(BASE_URL).findBooking(REFERENCE, SURNAME);
        String text = lab.mainText();
        assertTrue(text.contains("TF-222"), "flight number expected");
        assertTrue(text.contains("Istanbul") && text.contains("Madrid"), "route Istanbul -> Madrid expected");
    }

    @Test(description = "Full verification reaches SELF-HEALING-COMPLETE")
    public void fullVerificationCompletes() {
        SelfHealingLabPage lab = new SelfHealingLabPage(page, healer).open(BASE_URL);
        lab.findBooking(REFERENCE, SURNAME).confirmTraveller().completeVerification();
        assertTrue(lab.mainText().contains("SELF-HEALING-COMPLETE"), "business outcome expected");
    }

    @DataProvider(name = "loads")
    public Object[][] loads() {
        return new Object[][] {{1}, {2}, {3}};
    }

    /** Data-driven: every invocation is a fresh page load with a new locator set, and its own test in the report. */
    @Test(dataProvider = "loads", description = "A fresh page load, a new locator set")
    public void everyLoadIsHealed(int load) {
        SelfHealingLabPage lab = new SelfHealingLabPage(page, healer).open(BASE_URL);
        lab.findBooking(REFERENCE, SURNAME);
        assertTrue(lab.mainText().contains("TF-222"), "load " + load + ": itinerary expected");
    }
}
