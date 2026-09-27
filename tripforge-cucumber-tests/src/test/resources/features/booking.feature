Feature: Booking verification in the self-healing lab
  Every page load of the lab generates new ids, test ids, names and classes and renames labels.
  The page object uses selectors recorded from one load, so every step is healed.

  Background:
    Given the self-healing lab is open

  Scenario: Booking lookup shows the itinerary
    When I look up booking "TFH-2026" for passenger "IPEK"
    Then the itinerary shows flight "TF-222" from "Istanbul" to "Madrid"

  Scenario: Full verification reaches the business outcome
    When I look up booking "TFH-2026" for passenger "IPEK"
    And I confirm the traveller details
    And I complete the verification
    Then the lab reports "SELF-HEALING-COMPLETE"
