"""Generates one Maven project per driver x test-runner combination (see README.md).

Every project runs the same two tests against two bundled pages (v1 = original, v2 = ids and classes renamed):
  1. healRenamedButton - use the Save button on v1 (fingerprint), open v2, click it again -> healed, "Saved"
  2. plainLanguageStep  - healer.find("Form.email", "the email field") on v2 -> found by description
  3. deliberateFailure  - passes, but fails with -Dmatrix.fail=true: proves a failing test fails the build
Variants on top of driver x runner:
  *-parallel   the tests run in parallel threads (two test classes / two features sharing the same element keys)
  *-pw1.45 ... an older Playwright / Selenium than the framework is built with (supported-range check)
Run: python generate.py [healer-version]   then   python run_all.py
"""
import json, os, shutil, sys

HERE = os.path.dirname(os.path.abspath(__file__))
HEALER = sys.argv[1] if len(sys.argv) > 1 else "2.0.1"
CUCUMBER = "7.34.9"
DRIVERS = ["playwright", "selenium"]
RUNNERS = ["junit5", "junit4", "testng", "cucumber-junit5", "cucumber-testng", "cucumber-junit4"]
# (name, driver, runner, options): parallel = two classes/features in parallel threads; pin = older library versions
EXTRA = [
    ("playwright-junit5-parallel", "playwright", "junit5", {"parallel": True}),
    ("playwright-testng-parallel", "playwright", "testng", {"parallel": True}),
    ("playwright-cucumber-junit5-parallel", "playwright", "cucumber-junit5", {"parallel": True}),
    ("playwright-cucumber-testng-parallel", "playwright", "cucumber-testng", {"parallel": True}),
    ("selenium-junit5-parallel", "selenium", "junit5", {"parallel": True}),
    ("selenium-testng-parallel", "selenium", "testng", {"parallel": True}),
    ("playwright-junit5-pw1.45", "playwright", "junit5", {"pin": {"playwright": "1.45.0"}}),
    ("selenium-junit5-se4.21", "selenium", "junit5", {"pin": {"selenium": "4.21.0"}}),
]

V1 = """<!doctype html><html><head><meta charset="utf-8"><title>Contact</title></head><body>
<form onsubmit="return false">
  <label for="email">Email</label><input id="email" name="email" type="email">
  <button type="button" id="save" data-testid="save-btn" class="btn primary"
          onclick="document.getElementById('out').textContent='Saved'">Save</button>
  <button type="button" id="cancel" class="btn">Cancel</button>
</form><p id="out"></p></body></html>
"""
V2 = V1.replace('id="email" name="email"', 'id="mail" name="contact-mail"') \
       .replace('for="email"', 'for="mail"') \
       .replace('id="save" data-testid="save-btn" class="btn primary"', 'id="store" data-testid="store-btn" class="button primary-action"')

PROPS = """healer.language=en
healer.mode=auto
healer.probeTimeoutMs=800
healer.storeDir=target/healer-store
healer.reportDir=target/healer-report
healer.screenshots=false
healer.report.pdf=false
healer.verbose=false
healer.llm.enabled=false
"""


def w(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, "w", encoding="utf-8", newline="\n").write(text)


def deps(driver, runner):
    d = [("io.github.yasindeger48", "healer-" + driver, "${healer.version}")]
    if runner in ("testng", "cucumber-testng"):
        d.append(("io.github.yasindeger48", "healer-testng", "${healer.version}"))
    if runner.startswith("cucumber"):
        d.append(("io.github.yasindeger48", "healer-cucumber", "${healer.version}"))
        d += [("io.cucumber", "cucumber-java", CUCUMBER), ("io.cucumber", "cucumber-picocontainer", CUCUMBER)]
    if runner == "junit5":
        d.append(("io.github.yasindeger48", "healer-junit5", "${healer.version}"))
        d.append(("org.junit.jupiter", "junit-jupiter", "5.14.4"))
    if runner == "cucumber-junit5":
        d += [("io.cucumber", "cucumber-junit-platform-engine", CUCUMBER), ("org.junit.platform", "junit-platform-suite", "1.14.4"),
              ("org.junit.jupiter", "junit-jupiter-api", "5.14.4")]
    if runner in ("junit4", "cucumber-junit4"):
        d.append(("junit", "junit", "4.13.2"))
    if runner == "junit4":
        d.append(("io.github.yasindeger48", "healer-junit4", "${healer.version}"))
    if runner == "cucumber-junit4":
        d.append(("io.cucumber", "cucumber-junit", CUCUMBER))
    if runner in ("testng", "cucumber-testng"):
        d.append(("org.testng", "testng", "7.12.0"))
    if runner == "cucumber-testng":
        d.append(("io.cucumber", "cucumber-testng", CUCUMBER))
    d.append(("org.slf4j", "slf4j-simple", "2.0.20"))
    return d


def managed(pin):
    parts = []
    if "playwright" in pin:
        parts.append(f"""      <dependency>
        <groupId>com.microsoft.playwright</groupId>
        <artifactId>playwright</artifactId>
        <version>{pin['playwright']}</version>
      </dependency>
""")
    if "selenium" in pin:
        parts.append(f"""      <dependency>
        <groupId>org.seleniumhq.selenium</groupId>
        <artifactId>selenium-bom</artifactId>
        <version>{pin['selenium']}</version>
        <type>pom</type>
        <scope>import</scope>
      </dependency>
""")
    if not parts:
        return ""
    return "  <dependencyManagement>\n    <dependencies>\n" + "".join(parts) + "    </dependencies>\n  </dependencyManagement>\n\n"


def pom(name, driver, runner, pin=None):
    body = "".join(f"""    <dependency>
      <groupId>{g}</groupId>
      <artifactId>{a}</artifactId>
      <version>{v}</version>
      <scope>test</scope>
    </dependency>
""" for g, a, v in deps(driver, runner))
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<!-- Compatibility check: {name}. Generated by ../generate.py - edit the generator, not this file. -->
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
  <modelVersion>4.0.0</modelVersion>
  <groupId>com.example.matrix</groupId>
  <artifactId>{name}</artifactId>
  <version>1.0.0</version>

  <properties>
    <maven.compiler.release>17</maven.compiler.release>
    <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    <healer.version>{HEALER}</healer.version>
  </properties>

{managed(pin or {})}  <dependencies>
{body}  </dependencies>

  <build>
    <plugins>
      <plugin>
        <groupId>org.apache.maven.plugins</groupId>
        <artifactId>maven-compiler-plugin</artifactId>
        <version>3.14.0</version>
      </plugin>
      <plugin>
        <groupId>org.apache.maven.plugins</groupId>
        <artifactId>maven-surefire-plugin</artifactId>
        <version>3.6.0</version>
        <configuration>
          <argLine>-Dfile.encoding=UTF-8</argLine>
          <environmentVariables>
            <PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD>1</PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD>
          </environmentVariables>
        </configuration>
      </plugin>
    </plugins>
  </build>
</project>
"""


# ---- driver-specific building blocks --------------------------------------------------------------

def setup(driver):
    """(fields, open, close, heal-body, find-body) as Java snippets."""
    if driver == "playwright":
        return ("""    static com.microsoft.playwright.Playwright playwright;
    static com.microsoft.playwright.Browser browser;
    com.microsoft.playwright.Page page;
    com.selfhealing.healer.playwright.SelfHealingPage healer;
""", """        if (browser == null) {
            playwright = com.microsoft.playwright.Playwright.create();
            browser = playwright.chromium().launch(new com.microsoft.playwright.BrowserType.LaunchOptions()
                    .setHeadless(true).setChannel(System.getProperty("browser.channel", "msedge")));
        }
        page = browser.newPage();
        healer = com.selfhealing.healer.playwright.SelfHealingPage.wrap(page);
""", """        page.close();
""", """        page.navigate(Fixtures.url("v1.html"));
        healer.locator("Form.save", "#save").click();
        page.navigate(Fixtures.url("v2.html"));
        healer.locator("Form.save", "#save").click();
        Fixtures.check("Saved".equals(page.locator("#out").textContent()), "Saved expected after the healed click");
""", """        page.navigate(Fixtures.url("v2.html"));
        healer.find("Form.email", "the email field").fill("jane@example.com");
        Fixtures.check("jane@example.com".equals(page.locator("#mail").inputValue()), "the email field was filled");
""")
    return ("""    static org.openqa.selenium.WebDriver driver;
    com.selfhealing.healer.selenium.SelfHealingDriver healer;
""", """        if (driver == null) {
            driver = new org.openqa.selenium.edge.EdgeDriver(new org.openqa.selenium.edge.EdgeOptions().addArguments("--headless=new"));
            Runtime.getRuntime().addShutdownHook(new Thread(driver::quit));
        }
        healer = com.selfhealing.healer.selenium.SelfHealingDriver.wrap(driver);
""", "", """        driver.get(Fixtures.url("v1.html"));
        healer.element("Form.save", org.openqa.selenium.By.id("save")).click();
        driver.get(Fixtures.url("v2.html"));
        healer.element("Form.save", org.openqa.selenium.By.id("save")).click();
        Fixtures.check("Saved".equals(driver.findElement(org.openqa.selenium.By.id("out")).getText()), "Saved expected after the healed click");
""", """        driver.get(Fixtures.url("v2.html"));
        healer.find("Form.email", "the email field").fill("jane@example.com");
        Fixtures.check("jane@example.com".equals(driver.findElement(org.openqa.selenium.By.id("mail")).getDomProperty("value")),
                "the email field was filled");
""")


def setup_parallel(driver):
    """Like setup(), but every thread has its own browser, page and healer (TestNG shares one instance between threads)."""
    _, _, _, heal, find = setup(driver)
    who = '        System.out.println("[matrix-thread] " + Thread.currentThread().getName());\n'
    if driver == "playwright":
        swap = lambda code: code.replace("page.", "PAGE.get().").replace("healer.", "HEALER.get().")
        return ("""    static final ThreadLocal<com.microsoft.playwright.Browser> BROWSER = ThreadLocal.withInitial(() -> {
        com.microsoft.playwright.Playwright playwright = com.microsoft.playwright.Playwright.create();
        Runtime.getRuntime().addShutdownHook(new Thread(playwright::close));
        return playwright.chromium().launch(new com.microsoft.playwright.BrowserType.LaunchOptions()
                .setHeadless(true).setChannel(System.getProperty("browser.channel", "msedge")));
    });
    static final ThreadLocal<com.microsoft.playwright.Page> PAGE = new ThreadLocal<>();
    static final ThreadLocal<com.selfhealing.healer.playwright.SelfHealingPage> HEALER = new ThreadLocal<>();
""", who + """        PAGE.set(BROWSER.get().newPage());
        HEALER.set(com.selfhealing.healer.playwright.SelfHealingPage.wrap(PAGE.get()));
""", """        PAGE.get().close();
""", swap(heal), swap(find))
    swap = lambda code: code.replace("driver.", "DRIVER.get().").replace("healer.", "HEALER.get().")
    return ("""    static final ThreadLocal<org.openqa.selenium.WebDriver> DRIVER = ThreadLocal.withInitial(() -> {
        org.openqa.selenium.WebDriver driver = new org.openqa.selenium.edge.EdgeDriver(
                new org.openqa.selenium.edge.EdgeOptions().addArguments("--headless=new"));
        Runtime.getRuntime().addShutdownHook(new Thread(driver::quit));
        return driver;
    });
    static final ThreadLocal<com.selfhealing.healer.selenium.SelfHealingDriver> HEALER = new ThreadLocal<>();
""", who + """        HEALER.set(com.selfhealing.healer.selenium.SelfHealingDriver.wrap(DRIVER.get()));
""", "", swap(heal), swap(find))


FIXTURES = """package matrix;

/** Bundled test pages and a framework-neutral assertion (works under every runner). */
public final class Fixtures {
    private Fixtures() {
    }

    public static String url(String page) {
        try {
            return Fixtures.class.getResource("/pages/" + page).toURI().toString();
        } catch (java.net.URISyntaxException e) {
            throw new IllegalStateException(e);
        }
    }

    public static void check(boolean ok, String message) {
        if (!ok) throw new AssertionError(message);
    }

    /** Fails only when the run is started with -Dmatrix.fail=true. */
    public static void failWhenAsked() {
        check(!Boolean.getBoolean("matrix.fail"), "deliberate failure (-Dmatrix.fail=true)");
    }
}
"""


def plain_test(driver, runner, parallel=False, cls="HealingTest"):
    fields, open_, close, heal, find = (setup_parallel if parallel else setup)(driver)
    open_page = heal.split("\n")[0] + "\n"   # the page is open, so a failure gets a screenshot
    if runner == "junit5":
        # Playwright: no annotation at all (extension auto-detection); Selenium: the usual @ExtendWith
        head = "" if driver == "playwright" else "@org.junit.jupiter.api.extension.ExtendWith(com.selfhealing.healer.junit5.HealingExtension.class)\n"
        before, after, test = "@org.junit.jupiter.api.BeforeEach", "@org.junit.jupiter.api.AfterEach", "@org.junit.jupiter.api.Test"
    elif runner == "junit4":
        head, before, after, test = "", "@org.junit.Before", "@org.junit.After", "@org.junit.Test"
    else:
        head, before, after, test = "", "@org.testng.annotations.BeforeMethod", "@org.testng.annotations.AfterMethod", "@org.testng.annotations.Test"
    rule = "    @org.junit.Rule\n    public com.selfhealing.healer.junit4.HealingRule healing = new com.selfhealing.healer.junit4.HealingRule();\n\n" \
        if runner == "junit4" else ""
    return f"""package matrix;

/** {driver} + {runner}: the same tests in every combination. */
{head}public class {cls} {{

{rule}{fields}
    {before}
    public void open() {{
{open_}    }}

    {after}
    public void close() {{
{close}    }}

    {test}
    public void healRenamedButton() {{
{heal}    }}

    {test}
    public void plainLanguageStep() {{
{find}    }}

    {test}
    public void deliberateFailure() {{
{open_page}        Fixtures.failWhenAsked();
    }}
}}
"""


FEATURE = """Feature: Matrix
  Scenario: Heal a renamed button
    When I save on the original page and again on the changed page
    Then the page says Saved

  Scenario: Plain-language step
    When I fill the email field by its description
    Then the email field has the value

  Scenario: Deliberate failure
    When I save on the original page and again on the changed page
    Then it fails when asked
"""


PARALLEL_JUNIT = """
@org.junit.platform.suite.api.ConfigurationParameter(key = "cucumber.execution.parallel.enabled", value = "true")
@org.junit.platform.suite.api.ConfigurationParameter(key = "cucumber.execution.parallel.config.strategy", value = "fixed")
@org.junit.platform.suite.api.ConfigurationParameter(key = "cucumber.execution.parallel.config.fixed.parallelism", value = "3")"""
PARALLEL_TESTNG = """

    @Override
    @org.testng.annotations.DataProvider(parallel = true)
    public Object[][] scenarios() {
        return super.scenarios();
    }"""

JUNIT5_PARALLEL = """junit.jupiter.execution.parallel.enabled=true
junit.jupiter.execution.parallel.mode.default=concurrent
junit.jupiter.execution.parallel.mode.classes.default=concurrent
junit.jupiter.execution.parallel.config.strategy=fixed
junit.jupiter.execution.parallel.config.fixed.parallelism=3
"""
TESTNG_PARALLEL = """testng.parallel=methods
testng.threadCount=3
"""


def cucumber(driver, runner, parallel=False):
    fields, open_, close, heal, find = (setup_parallel if parallel else setup)(driver)
    heal_when, heal_then = heal.rsplit("        Fixtures.check", 1)
    find_when, find_then = find.rsplit("        Fixtures.check", 1)
    steps = f"""package matrix;

import io.cucumber.java.After;
import io.cucumber.java.Before;
import io.cucumber.java.en.Then;
import io.cucumber.java.en.When;

/** {driver} + {runner}: glue for features/matrix.feature. */
public class Steps {{

{fields}
    @Before
    public void open() {{
{open_}    }}

    @After
    public void close() {{
{close}    }}

    @When("I save on the original page and again on the changed page")
    public void save() {{
{heal_when}    }}

    @Then("the page says Saved")
    public void saved() {{
        Fixtures.check{heal_then}    }}

    @When("I fill the email field by its description")
    public void fill() {{
{find_when}    }}

    @Then("the email field has the value")
    public void filled() {{
        Fixtures.check{find_then}    }}

    @Then("it fails when asked")
    public void failWhenAsked() {{
        Fixtures.failWhenAsked();
    }}
}}
"""
    plugin = "com.selfhealing.healer.cucumber.HealingCucumberPlugin"
    if runner == "cucumber-junit5":
        run = f"""package matrix;

@org.junit.platform.suite.api.Suite
@org.junit.platform.suite.api.IncludeEngines("cucumber")
@org.junit.platform.suite.api.SelectPackages("features")
@org.junit.platform.suite.api.ConfigurationParameter(key = "cucumber.glue", value = "matrix")
@org.junit.platform.suite.api.ConfigurationParameter(key = "cucumber.plugin", value = "{plugin}"){PARALLEL_JUNIT if parallel else ""}
public class RunCucumberTest {{
}}
"""
    elif runner == "cucumber-testng":
        run = f"""package matrix;

@io.cucumber.testng.CucumberOptions(features = "classpath:features", glue = "matrix", plugin = "{plugin}")
public class RunCucumberTest extends io.cucumber.testng.AbstractTestNGCucumberTests {{{PARALLEL_TESTNG if parallel else ""}
}}
"""
    else:
        run = f"""package matrix;

@org.junit.runner.RunWith(io.cucumber.junit.Cucumber.class)
@io.cucumber.junit.CucumberOptions(features = "classpath:features", glue = "matrix", plugin = "{plugin}")
public class RunCucumberTest {{
}}
"""
    return steps, run


def generate(name, driver, runner, opts=None):
    opts = opts or {}
    parallel = opts.get("parallel", False)
    d = os.path.join(HERE, name)
    # refresh in place (the folder itself may be held open by OneDrive or an IDE)
    for sub in ("src", "target"):
        shutil.rmtree(os.path.join(d, sub), ignore_errors=True)
    w(os.path.join(d, "pom.xml"), pom(name, driver, runner, opts.get("pin")))
    src = os.path.join(d, "src", "test", "java", "matrix")
    res = os.path.join(d, "src", "test", "resources")
    w(os.path.join(src, "Fixtures.java"), FIXTURES)
    w(os.path.join(res, "pages", "v1.html"), V1)
    w(os.path.join(res, "pages", "v2.html"), V2)
    w(os.path.join(res, "healer.properties"), PROPS)
    w(os.path.join(res, "simplelogger.properties"), "org.slf4j.simpleLogger.defaultLogLevel=warn\n")
    copies = 2 if parallel else 1
    if runner.startswith("cucumber"):
        steps, run = cucumber(driver, runner, parallel)
        w(os.path.join(src, "Steps.java"), steps)
        w(os.path.join(src, "RunCucumberTest.java"), run)
        w(os.path.join(res, "features", "matrix.feature"), FEATURE)
        if parallel:   # a second feature with the same steps (and element keys), scenario names kept apart
            second = FEATURE.replace("Feature: Matrix", "Feature: Matrix 2")
            for title in ("Heal a renamed button", "Plain-language step", "Deliberate failure"):
                second = second.replace("Scenario: " + title, "Scenario: " + title + " 2")
            w(os.path.join(res, "features", "matrix2.feature"), second)
    else:
        for i in range(copies):
            cls = ("HealingTest", "HealingAgainTest")[i]   # both match Surefire's default *Test pattern
            w(os.path.join(src, cls + ".java"), plain_test(driver, runner, parallel, cls))
    platform = ""
    if runner == "junit5" and driver == "playwright":
        platform += "junit.jupiter.extensions.autodetection.enabled=true\n"
    if parallel and runner == "junit5":
        platform += JUNIT5_PARALLEL
    if parallel and runner == "testng":
        platform += TESTNG_PARALLEL
    if platform:
        w(os.path.join(res, "junit-platform.properties"), platform)
    # what run_all.py expects from this project
    w(os.path.join(d, "matrix.json"), json.dumps({"tests": 3 * copies, "failures": copies, "parallel": parallel}) + "\n")
    mvn = os.path.join(d, ".mvn")
    os.makedirs(mvn, exist_ok=True)
    src_mvn = os.path.join(os.path.dirname(HERE), "tripforge-tests", ".mvn")
    for f in ("maven.config", "settings.xml", "jvm.config"):
        shutil.copy(os.path.join(src_mvn, f), os.path.join(mvn, f))
    print("generated", name)


def main():
    for driver in DRIVERS:
        for runner in RUNNERS:
            generate(f"{driver}-{runner}", driver, runner)
    for name, driver, runner, opts in EXTRA:
        generate(name, driver, runner, opts)


if __name__ == "__main__":
    main()
