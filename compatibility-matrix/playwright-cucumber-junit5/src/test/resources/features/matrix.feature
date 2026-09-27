Feature: Matrix
  Scenario: Heal a renamed button
    When I save on the original page and again on the changed page
    Then the page says Saved

  Scenario: Plain-language step
    When I fill the email field by its description
    Then the email field has the value

  Scenario: Deliberate failure
    When I save on the original page and again on the changed page
    Then it fails when asked
