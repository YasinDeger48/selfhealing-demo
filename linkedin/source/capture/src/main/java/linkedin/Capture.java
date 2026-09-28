package linkedin;

import com.microsoft.playwright.Browser;
import com.microsoft.playwright.BrowserContext;
import com.microsoft.playwright.BrowserType;
import com.microsoft.playwright.Page;
import com.microsoft.playwright.Playwright;
import com.selfhealing.healer.playwright.SelfHealingPage;

import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.StandardCopyOption;

/**
 * Screenshots and a demo video of the real framework healing the (broken) ShopLab site with the overlay on,
 * and pictures of the real report in ../report. Nothing here is mocked: the heals are the framework's own.
 */
public class Capture {

    public static void main(String[] args) throws Exception {
        Path linkedin = Path.of("../..").toAbsolutePath().normalize();
        Path images = linkedin.resolve("images");
        Path video = linkedin.resolve("video");
        Files.createDirectories(images);
        Files.createDirectories(video);
        String shop = System.getProperty("shoplab.url", "http://localhost:8080");

        // the settings a project would put into healer.properties
        System.setProperty("healer.visual", "true");
        System.setProperty("healer.visual.pauseMs", "1400");
        System.setProperty("healer.storeDir", "target/capture-store");
        System.setProperty("healer.reportDir", "target/capture-report");
        System.setProperty("healer.llm.enabled", "false");
        System.setProperty("healer.verbose", "false");
        System.setProperty("healer.report.open", "never");
        System.setProperty("healer.report.pdf", "false");
        // the fingerprints ShopLab's tests recorded on the original site ("yesterday")
        Path store = Path.of("target/capture-store");
        Files.createDirectories(store);
        Files.copy(linkedin.resolve("../shoplab-tests/.healer/fingerprints.json"), store.resolve("fingerprints.json"),
                StandardCopyOption.REPLACE_EXISTING);
        Files.deleteIfExists(store.resolve("healed-locators.json"));

        try (Playwright playwright = Playwright.create()) {
            Browser browser = playwright.chromium().launch(new BrowserType.LaunchOptions().setChannel("msedge").setHeadless(true));

            // 1. the healing, recorded with the overlay drawing every step
            BrowserContext context = browser.newContext(new Browser.NewContextOptions()
                    .setViewportSize(1280, 800).setRecordVideoDir(video.resolve("raw")).setRecordVideoSize(1280, 800));
            Page page = context.newPage();
            SelfHealingPage healer = SelfHealingPage.wrap(page);
            healer.navigate(shop + "/login");
            page.waitForSelector("form input");
            page.waitForTimeout(800);
            healer.locator("LoginPage.username", "#login-username").fill("standard_user");
            page.screenshot(new Page.ScreenshotOptions().setPath(images.resolve("overlay-login-1280x800.png")));
            healer.locator("LoginPage.password", "input[name='password']").fill("secret123");
            healer.locator("LoginPage.loginButton", "[data-testid='login-submit-button']").click();
            page.waitForURL("**/products");
            page.waitForTimeout(800);
            healer.locator("ProductsPage.search", "#product-search").fill("watch");
            page.waitForTimeout(600);
            healer.locator("ProductsPage.search", "#product-search").fill("");
            healer.locator("ProductsPage.addToCart[8]", "#add-to-cart-8").click();
            page.screenshot(new Page.ScreenshotOptions().setPath(images.resolve("overlay-products-1280x800.png")));
            page.waitForTimeout(1500);
            Path raw = page.video().path();
            context.close();
            Files.move(raw, video.resolve("healing-demo-1280x800.webm"), StandardCopyOption.REPLACE_EXISTING);

            // 2. the real report of the ShopLab test run (12 tests, broken site, local heals only)
            BrowserContext rc = browser.newContext(new Browser.NewContextOptions().setViewportSize(1400, 900).setDeviceScaleFactor(2));
            Page report = rc.newPage();
            report.navigate(linkedin.resolve("source/report/healing-report.html").toUri().toString());
            report.screenshot(new Page.ScreenshotOptions().setPath(images.resolve("report-summary.png"))
                    .setClip(0, 0, 1400, 330));
            report.getByText("Expand all").first().click();
            report.waitForTimeout(500);
            report.screenshot(new Page.ScreenshotOptions().setPath(images.resolve("report-expanded-top.png"))
                    .setClip(0, 0, 1400, 1600));
            report.screenshot(new Page.ScreenshotOptions().setPath(linkedin.resolve("source/report-expanded-full.png")).setFullPage(true));
            rc.close();
        }
        System.out.println("captured into " + linkedin);
    }
}
