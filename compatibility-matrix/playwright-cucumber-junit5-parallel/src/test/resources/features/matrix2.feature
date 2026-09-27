Feature: Matrix 2
  Scenario: Heal a renamed button 2
    When I save on the original page and again on the changed page
    Then the page says Saved

  Scenario: Plain-language step 2
    When I fill the email field by its description
    Then the email field has the value

  Scenario: Deliberate failure 2
    When I save on the original page and again on the changed page
    Then it fails when asked
