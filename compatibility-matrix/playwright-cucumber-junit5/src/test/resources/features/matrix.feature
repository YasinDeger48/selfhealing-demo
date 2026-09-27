Feature: Matrix
  Scenario: Heal a renamed button
    When I save on the original page and again on the changed page
    Then the page says Saved

  Scenario: Heal a renamed field
    When I type my name on the original page and again on the changed page
    Then the changed name field has the value

  Scenario: Plain-language step
    When I fill the email field by its description
    Then the email field has the value

  Scenario: A removed button is not healed
    When I cancel on the original page and open a page without the Cancel button
    Then no other button is used instead

  Scenario: Deliberate failure
    When I save on the original page and again on the changed page
    Then it fails when asked

  Scenario: TripForge - booking lookup shows the itinerary
    When I look up the TripForge booking
    Then the itinerary is shown

  Scenario: TripForge - full verification completes
    When I complete the TripForge verification
    Then the verification is complete

  Scenario: ShopLab - a wrong password shows an error
    When I log in to ShopLab with a wrong password
    Then ShopLab shows a login error

  Scenario: ShopLab - search and filter
    When I log in to ShopLab and search for a watch
    Then the search and the category filter narrow the products

  Scenario: ShopLab - adding to the cart updates the badge
    When I log in to ShopLab and add two products to the cart
    Then the cart badge shows two items
