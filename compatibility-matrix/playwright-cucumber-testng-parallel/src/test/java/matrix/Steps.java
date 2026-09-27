package matrix;

import io.cucumber.java.After;
import io.cucumber.java.Before;
import io.cucumber.java.en.Then;
import io.cucumber.java.en.When;

/** playwright + cucumber-testng: glue for features/matrix.feature. */
public class Steps {

    static final ThreadLocal<com.microsoft.playwright.Browser> BROWSER = ThreadLocal.withInitial(() -> {
        com.microsoft.playwright.Playwright playwright = com.microsoft.playwright.Playwright.create();
        Runtime.getRuntime().addShutdownHook(new Thread(playwright::close));
        return playwright.chromium().launch(new com.microsoft.playwright.BrowserType.LaunchOptions()
                .setHeadless(true).setChannel(System.getProperty("browser.channel", "msedge")));
    });
    static final ThreadLocal<com.microsoft.playwright.Page> PAGE = new ThreadLocal<>();
    static final ThreadLocal<com.selfhealing.healer.playwright.SelfHealingPage> HEALER = new ThreadLocal<>();

    @Before
    public void open() {
        System.out.println("[matrix-thread] " + Thread.currentThread().getName());
        PAGE.set(BROWSER.get().newPage());
        HEALER.set(com.selfhealing.healer.playwright.SelfHealingPage.wrap(PAGE.get()));
    }

    @After
    public void close() {
        PAGE.get().close();
    }

    @When("I save on the original page and again on the changed page")
    public void save() {
        PAGE.get().navigate(Fixtures.url("v1.html"));
        HEALER.get().locator("Form.save", "#save").click();
        PAGE.get().navigate(Fixtures.url("v2.html"));
        HEALER.get().locator("Form.save", "#save").click();
    }

    @Then("the page says Saved")
    public void saved() {
        Fixtures.check("Saved".equals(PAGE.get().locator("#out").textContent()), "Saved expected after the healed click");
    }

    @When("I fill the email field by its description")
    public void fill() {
        PAGE.get().navigate(Fixtures.url("v2.html"));
        HEALER.get().find("Form.email", "the email field").fill("jane@example.com");
    }

    @Then("the email field has the value")
    public void filled() {
        Fixtures.check("jane@example.com".equals(PAGE.get().locator("#mail").inputValue()), "the email field was filled");
    }

    @Then("it fails when asked")
    public void failWhenAsked() {
        Fixtures.failWhenAsked();
    }
}
