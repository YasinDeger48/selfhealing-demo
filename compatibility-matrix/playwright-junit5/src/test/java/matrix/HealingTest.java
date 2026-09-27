package matrix;

/** playwright + junit5: the same tests in every combination. */
@org.junit.jupiter.api.extension.ExtendWith(com.selfhealing.healer.playwright.HealingExtension.class)
public class HealingTest {

    static com.microsoft.playwright.Playwright playwright;
    static com.microsoft.playwright.Browser browser;
    com.microsoft.playwright.Page page;
    com.selfhealing.healer.playwright.SelfHealingPage healer;

    @org.junit.jupiter.api.BeforeEach
    public void open() {
        if (browser == null) {
            playwright = com.microsoft.playwright.Playwright.create();
            browser = playwright.chromium().launch(new com.microsoft.playwright.BrowserType.LaunchOptions()
                    .setHeadless(true).setChannel(System.getProperty("browser.channel", "msedge")));
        }
        page = browser.newPage();
        healer = com.selfhealing.healer.playwright.SelfHealingPage.wrap(page);
    }

    @org.junit.jupiter.api.AfterEach
    public void close() {
        page.close();
    }

    @org.junit.jupiter.api.Test
    public void healRenamedButton() {
        page.navigate(Fixtures.url("v1.html"));
        healer.locator("Form.save", "#save").click();
        page.navigate(Fixtures.url("v2.html"));
        healer.locator("Form.save", "#save").click();
        Fixtures.check("Saved".equals(page.locator("#out").textContent()), "Saved expected after the healed click");
    }

    @org.junit.jupiter.api.Test
    public void plainLanguageStep() {
        page.navigate(Fixtures.url("v2.html"));
        healer.find("Form.email", "the email field").fill("jane@example.com");
        Fixtures.check("jane@example.com".equals(page.locator("#mail").inputValue()), "the email field was filled");
    }

    @org.junit.jupiter.api.Test
    public void deliberateFailure() {
        page.navigate(Fixtures.url("v1.html"));
        Fixtures.failWhenAsked();
    }
}
