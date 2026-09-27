package matrix;

/** selenium + junit5: the same tests in every combination. */
@org.junit.jupiter.api.extension.ExtendWith(com.selfhealing.healer.junit5.HealingExtension.class)
public class HealingAgainTest {

    static final ThreadLocal<org.openqa.selenium.WebDriver> DRIVER = ThreadLocal.withInitial(() -> {
        org.openqa.selenium.WebDriver driver = new org.openqa.selenium.edge.EdgeDriver(
                new org.openqa.selenium.edge.EdgeOptions().addArguments("--headless=new"));
        Runtime.getRuntime().addShutdownHook(new Thread(driver::quit));
        return driver;
    });
    static final ThreadLocal<com.selfhealing.healer.selenium.SelfHealingDriver> HEALER = new ThreadLocal<>();

    @org.junit.jupiter.api.BeforeEach
    public void open() {
        System.out.println("[matrix-thread] " + Thread.currentThread().getName());
        HEALER.set(com.selfhealing.healer.selenium.SelfHealingDriver.wrap(DRIVER.get()));
    }

    @org.junit.jupiter.api.AfterEach
    public void close() {
    }

    @org.junit.jupiter.api.Test
    public void healRenamedButton() {
        DRIVER.get().get(Fixtures.url("v1.html"));
        HEALER.get().element("Form.save", org.openqa.selenium.By.id("save")).click();
        DRIVER.get().get(Fixtures.url("v2.html"));
        HEALER.get().element("Form.save", org.openqa.selenium.By.id("save")).click();
        Fixtures.check("Saved".equals(DRIVER.get().findElement(org.openqa.selenium.By.id("out")).getText()), "Saved expected after the healed click");
    }

    @org.junit.jupiter.api.Test
    public void plainLanguageStep() {
        DRIVER.get().get(Fixtures.url("v2.html"));
        HEALER.get().find("Form.email", "the email field").fill("jane@example.com");
        Fixtures.check("jane@example.com".equals(DRIVER.get().findElement(org.openqa.selenium.By.id("mail")).getDomProperty("value")),
                "the email field was filled");
    }

    @org.junit.jupiter.api.Test
    public void deliberateFailure() {
        DRIVER.get().get(Fixtures.url("v1.html"));
        Fixtures.failWhenAsked();
    }
}
