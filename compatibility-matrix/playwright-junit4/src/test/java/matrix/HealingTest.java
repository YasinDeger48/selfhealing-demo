package matrix;

/** playwright + junit4: the same tests in every combination. */
public class HealingTest {

    @org.junit.Rule
    public com.selfhealing.healer.junit4.HealingRule healing = new com.selfhealing.healer.junit4.HealingRule();

    static com.microsoft.playwright.Playwright playwright;
    static com.microsoft.playwright.Browser browser;
    com.microsoft.playwright.Page page;
    com.selfhealing.healer.playwright.SelfHealingPage healer;

    @org.junit.Before
    public void open() {
        if (browser == null) {
            playwright = com.microsoft.playwright.Playwright.create();
            browser = playwright.chromium().launch(new com.microsoft.playwright.BrowserType.LaunchOptions()
                    .setHeadless(true).setChannel(System.getProperty("browser.channel", "msedge")));
        }
        page = browser.newPage();
        healer = com.selfhealing.healer.playwright.SelfHealingPage.wrap(page);
    }

    @org.junit.After
    public void close() {
        page.close();
    }

    @org.junit.Test
    public void healRenamedButton() {
        page.navigate(Fixtures.url("v1.html"));
        healer.locator("Form.save", "#save").click();
        page.navigate(Fixtures.url("v2.html"));
        healer.locator("Form.save", "#save").click();
        Fixtures.check("Saved".equals(page.locator("#out").textContent()), "Saved expected after the healed click");
    }

    @org.junit.Test
    public void plainLanguageStep() {
        page.navigate(Fixtures.url("v2.html"));
        healer.find("Form.email", "the email field").fill("jane@example.com");
        Fixtures.check("jane@example.com".equals(page.locator("#mail").inputValue()), "the email field was filled");
    }

    @org.junit.Test
    public void deliberateFailure() {
        page.navigate(Fixtures.url("v1.html"));
        Fixtures.failWhenAsked();
    }
}
