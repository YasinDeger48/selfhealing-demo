package matrix;

import io.cucumber.java.After;
import io.cucumber.java.Before;
import io.cucumber.java.en.Then;
import io.cucumber.java.en.When;

/** selenium + cucumber-junit5: glue for features/matrix.feature. */
public class Steps {

    static org.openqa.selenium.WebDriver driver;
    com.selfhealing.healer.selenium.SelfHealingDriver healer;

    @Before
    public void open() {
        if (driver == null) {
            driver = new org.openqa.selenium.edge.EdgeDriver(new org.openqa.selenium.edge.EdgeOptions().addArguments("--headless=new"));
            Runtime.getRuntime().addShutdownHook(new Thread(driver::quit));
        }
        healer = com.selfhealing.healer.selenium.SelfHealingDriver.wrap(driver);
    }

    @After
    public void close() {
    }

    @When("I save on the original page and again on the changed page")
    public void save() {
        driver.get(Fixtures.url("v1.html"));
        healer.element("Form.save", org.openqa.selenium.By.id("save")).click();
        driver.get(Fixtures.url("v2.html"));
        healer.element("Form.save", org.openqa.selenium.By.id("save")).click();
    }

    @Then("the page says Saved")
    public void saved() {
        Fixtures.check("Saved".equals(driver.findElement(org.openqa.selenium.By.id("out")).getText()), "Saved expected after the healed click");
    }

    @When("I fill the email field by its description")
    public void fill() {
        driver.get(Fixtures.url("v2.html"));
        healer.find("Form.email", "the email field").fill("jane@example.com");
    }

    @Then("the email field has the value")
    public void filled() {
        Fixtures.check("jane@example.com".equals(driver.findElement(org.openqa.selenium.By.id("mail")).getDomProperty("value")),
                "the email field was filled");
    }

    @Then("it fails when asked")
    public void failWhenAsked() {
        Fixtures.failWhenAsked();
    }
}
