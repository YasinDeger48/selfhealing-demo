package matrix;

/** playwright + junit5: the same tests in every combination. */
public class HealingAgainTest {

    static final ThreadLocal<com.microsoft.playwright.Browser> BROWSER = ThreadLocal.withInitial(() -> {
        com.microsoft.playwright.Playwright playwright = com.microsoft.playwright.Playwright.create();
        Runtime.getRuntime().addShutdownHook(new Thread(playwright::close));
        return playwright.chromium().launch(new com.microsoft.playwright.BrowserType.LaunchOptions()
                .setHeadless(true).setChannel(System.getProperty("browser.channel", "msedge")));
    });
    static final ThreadLocal<com.microsoft.playwright.Page> PAGE = new ThreadLocal<>();
    static final ThreadLocal<com.selfhealing.healer.playwright.SelfHealingPage> HEALER = new ThreadLocal<>();

    @org.junit.jupiter.api.BeforeEach
    public void open() {
        System.out.println("[matrix-thread] " + Thread.currentThread().getName());
        PAGE.set(BROWSER.get().newPage());
        HEALER.set(com.selfhealing.healer.playwright.SelfHealingPage.wrap(PAGE.get()));
    }

    @org.junit.jupiter.api.AfterEach
    public void close() {
        PAGE.get().close();
    }

    @org.junit.jupiter.api.Test
    public void healRenamedButton() {
        PAGE.get().navigate(Fixtures.url("v1.html"));
        HEALER.get().locator("Form.save", "#save").click();
        PAGE.get().navigate(Fixtures.url("v2.html"));
        HEALER.get().locator("Form.save", "#save").click();
        Fixtures.check("Saved".equals(PAGE.get().locator("#out").textContent()), "Saved expected after the healed click");
    }

    @org.junit.jupiter.api.Test
    public void plainLanguageStep() {
        PAGE.get().navigate(Fixtures.url("v2.html"));
        HEALER.get().find("Form.email", "the email field").fill("jane@example.com");
        Fixtures.check("jane@example.com".equals(PAGE.get().locator("#mail").inputValue()), "the email field was filled");
    }

    @org.junit.jupiter.api.Test
    public void deliberateFailure() {
        PAGE.get().navigate(Fixtures.url("v1.html"));
        Fixtures.failWhenAsked();
    }
}
