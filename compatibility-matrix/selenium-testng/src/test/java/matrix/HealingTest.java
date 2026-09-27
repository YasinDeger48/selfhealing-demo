package matrix;

/** selenium + testng: the same tests in every combination. */
public class HealingTest {

    static org.openqa.selenium.WebDriver driver;
    com.selfhealing.healer.selenium.SelfHealingDriver healer;

    @org.testng.annotations.BeforeMethod
    public void open() {
        if (driver == null) {
            driver = new org.openqa.selenium.edge.EdgeDriver(new org.openqa.selenium.edge.EdgeOptions().addArguments("--headless=new"));
            Runtime.getRuntime().addShutdownHook(new Thread(driver::quit));
        }
        healer = com.selfhealing.healer.selenium.SelfHealingDriver.wrap(driver);
    }

    @org.testng.annotations.AfterMethod
    public void close() {
    }

    @org.testng.annotations.Test
    public void healRenamedButton() {
        driver.get(Fixtures.url("v1.html"));
        healer.element("Form.save", org.openqa.selenium.By.id("save")).click();
        driver.get(Fixtures.url("v2.html"));
        healer.element("Form.save", org.openqa.selenium.By.id("save")).click();
        Fixtures.check("Saved".equals(driver.findElement(org.openqa.selenium.By.id("out")).getText()), "Saved expected after the healed click");
    }

    @org.testng.annotations.Test
    public void plainLanguageStep() {
        driver.get(Fixtures.url("v2.html"));
        healer.find("Form.email", "the email field").fill("jane@example.com");
        Fixtures.check("jane@example.com".equals(driver.findElement(org.openqa.selenium.By.id("mail")).getDomProperty("value")),
                "the email field was filled");
    }

    @org.testng.annotations.Test
    public void deliberateFailure() {
        driver.get(Fixtures.url("v1.html"));
        Fixtures.failWhenAsked();
    }
}
