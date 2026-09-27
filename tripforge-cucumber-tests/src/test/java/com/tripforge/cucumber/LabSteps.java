package com.tripforge.cucumber;

import com.tripforge.cucumber.pages.SelfHealingLabPage;
import io.cucumber.java.en.Given;
import io.cucumber.java.en.Then;
import io.cucumber.java.en.When;

import static org.junit.jupiter.api.Assertions.assertTrue;

public class LabSteps {

    private final World world;
    private SelfHealingLabPage lab;

    public LabSteps(World world) {
        this.world = world;
    }

    @Given("the self-healing lab is open")
    public void labIsOpen() {
        lab = new SelfHealingLabPage(world.page, world.healer).open(Hooks.BASE_URL);
    }

    @When("I look up booking {string} for passenger {string}")
    public void lookUp(String reference, String surname) {
        lab.findBooking(reference, surname);
    }

    @When("I confirm the traveller details")
    public void confirmTraveller() {
        lab.confirmTraveller();
    }

    @When("I complete the verification")
    public void completeVerification() {
        lab.completeVerification();
    }

    @Then("the itinerary shows flight {string} from {string} to {string}")
    public void itinerary(String flight, String from, String to) {
        String text = lab.mainText();
        assertTrue(text.contains(flight), "flight " + flight + " expected");
        assertTrue(text.contains(from) && text.contains(to), "route " + from + " -> " + to + " expected");
    }

    @Then("the lab reports {string}")
    public void labReports(String outcome) {
        assertTrue(lab.mainText().contains(outcome), outcome + " expected");
    }
}
