package linkedin;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.microsoft.playwright.Browser;
import com.microsoft.playwright.BrowserType;
import com.microsoft.playwright.Page;
import com.microsoft.playwright.Playwright;

import java.nio.file.Path;

/** Turns the slides written by ../build.py (graphics/out/render.json) into PNG pictures and the carousel PDFs. */
public class Render {

    public static void main(String[] args) throws Exception {
        JsonNode jobs = new ObjectMapper().readTree(Path.of("../graphics/out/render.json").toFile());
        try (Playwright playwright = Playwright.create()) {
            Browser browser = playwright.chromium().launch(new BrowserType.LaunchOptions().setChannel("msedge").setHeadless(true));
            Page page = browser.newContext(new Browser.NewContextOptions().setViewportSize(1080, 1350)).newPage();
            for (JsonNode job : jobs) {
                page.navigate(Path.of(job.get("html").asText()).toUri().toString());
                page.waitForLoadState();
                page.evaluate("() => document.fonts.ready");
                if (job.has("png")) {
                    page.screenshot(new Page.ScreenshotOptions().setPath(Path.of(job.get("png").asText())));
                    System.out.println("png " + job.get("png").asText());
                } else {
                    page.pdf(new Page.PdfOptions().setPath(Path.of(job.get("pdf").asText()))
                            .setWidth("1080px").setHeight("1350px").setPrintBackground(true).setPreferCSSPageSize(true));
                    System.out.println("pdf " + job.get("pdf").asText());
                }
            }
        }
    }
}
