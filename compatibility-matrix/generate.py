"""Generates one Maven project per driver x test-runner combination (see README.md).

Every project runs the same tests against three bundled pages (v1 = original, v2 = ids, names and classes renamed,
v3 = v2 without the Cancel button):
  1. healRenamedButton      - click Save on v1 (fingerprint), open v2, click it again -> healed, "Saved"
  2. healRenamedField       - type into the Name field on v1, again on v2 (id and name changed) -> healed
  3. plainLanguageStep      - healer.find("Form.email", "the email field") on v2 -> found by its description
  4. removedButtonNotHealed - click Cancel on v1, open v3: the healer must NOT pick another button (false positive)
  5. deliberateFailure      - passes, but fails with -Dmatrix.fail=true: the build fails, the failure is analysed,
                              and the Playwright video and trace of the failed test are kept
plus the real-site scenarios of sites.py - TripForge on Vercel (every id changes on every load) and the ShopLab demo
site (broken on purpose by run_all.py): 2 TripForge and 3 ShopLab tests.
Browser, headless, healing, report ... come from src/test/resources/healer.properties (tools/healer_config.py) -
the tests contain no browser setup of their own (HealerBrowser / HealerDriver).
Variants on top of driver x runner:
  *-parallel   the tests run in parallel threads (two test classes / two features sharing the same element keys)
  *-pw1.45 ... an older Playwright / Selenium than the framework is built with (supported-range check)
Run: python generate.py [healer-version]   then   python run_all.py
"""
import json, os, shutil, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "tools"))
import healer_config  # noqa: E402

sys.path.insert(0, HERE)
import sites  # noqa: E402

HEALER = sys.argv[1] if len(sys.argv) > 1 else "2.2.0"
ROOT = os.path.dirname(HERE)
BASELINE = {"playwright": os.path.join(ROOT, "shoplab-tests", ".healer", "fingerprints.json"),
            "selenium": os.path.join(ROOT, "shoplab-selenium-tests", ".healer", "fingerprints.json")}
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
# test method -> Cucumber scenario (run_all.py checks the report against these names)
TESTS = {
    "healRenamedButton": "Heal a renamed button",
    "healRenamedField": "Heal a renamed field",
    "plainLanguageStep": "Plain-language step",
    "removedButtonNotHealed": "A removed button is not healed",
    "deliberateFailure": "Deliberate failure",
    **sites.TESTS,
}

V1 = """<!doctype html><html><head><meta charset="utf-8"><title>Contact</title></head><body>
<form onsubmit="return false">
  <label for="name">Name</label><input id="name" name="name" type="text">
  <label for="email">Email</label><input id="email" name="email" type="email">
  <button type="button" id="save" data-testid="save-btn" class="btn primary"
          onclick="document.getElementById('out').textContent='Saved'">Save</button>
  <button type="button" id="cancel" class="btn" onclick="document.getElementById('out').textContent='Cancelled'">Cancel</button>
</form><p id="out"></p></body></html>
"""
V2 = V1.replace('id="email" name="email"', 'id="mail" name="contact-mail"') \
       .replace('for="name">Name</label><input id="name" name="name"', 'for="full-name">Name</label><input id="full-name" name="fullname"') \
       .replace('for="email"', 'for="mail"') \
       .replace('id="save" data-testid="save-btn" class="btn primary"', 'id="store" data-testid="store-btn" class="button primary-action"')
V3 = V2.replace("""  <button type="button" id="cancel" class="btn" onclick="document.getElementById('out').textContent='Cancelled'">Cancel</button>
""", "")
assert V3 != V2


def props(driver):
    """Every setting a project manages, in the common layout; values chosen for fast, quiet matrix runs."""
    values = {
        "browser.name": "msedge" if driver == "playwright" else "edge",
        "browser.timeoutMs": "10000",
        "browser.video": "failures",
        "browser.trace": "failures",
        "healer.probeTimeoutMs": "800",
        "healer.fix": "off",
        "healer.report.pdf": "false",
        "healer.report.screenshots": "failures",
        "healer.verbose": "false",
    }
    return healer_config.render(values, driver, f"Compatibility matrix - {driver}. Generated by ../generate.py")


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

PW = "com.microsoft.playwright."
SE = "org.openqa.selenium."
HP = "com.selfhealing.healer.playwright."
HS = "com.selfhealing.healer.selenium."

# each test as (when, then): Cucumber uses them as two steps, the plain tests one after the other
BODIES = {
    "playwright": {
        "open": """        page.navigate(Fixtures.url("v1.html"));
""",
        "healRenamedButton": ("""        page.navigate(Fixtures.url("v1.html"));
        healer.locator("Form.save", "#save").click();
        page.navigate(Fixtures.url("v2.html"));
        healer.locator("Form.save", "#save").click();
""", """        Fixtures.check("Saved".equals(page.locator("#out").textContent()), "Saved expected after the healed click");
"""),
        "healRenamedField": ("""        page.navigate(Fixtures.url("v1.html"));
        healer.locator("Form.nameField", "#name").fill("Jane");
        page.navigate(Fixtures.url("v2.html"));
        healer.locator("Form.nameField", "#name").fill("Jane Doe");
""", """        Fixtures.check("Jane Doe".equals(page.locator("#full-name").inputValue()), "the healed name field was filled");
"""),
        "plainLanguageStep": ("""        page.navigate(Fixtures.url("v2.html"));
        healer.find("Form.email", "the email field").fill("jane@example.com");
""", """        Fixtures.check("jane@example.com".equals(page.locator("#mail").inputValue()), "the email field was filled");
"""),
        "removedButtonNotHealed": ("""        page.navigate(Fixtures.url("v1.html"));
        healer.locator("Form.cancel", "#cancel").click();
        page.navigate(Fixtures.url("v3.html"));
""", """        Fixtures.expectFailure(() -> healer.locator("Form.cancel", "#cancel").click(), "a removed button must not be healed to another one");
        Fixtures.check(page.locator("#out").textContent().isEmpty(), "no other button was clicked");
"""),
    },
    "selenium": {
        "open": """        driver.get(Fixtures.url("v1.html"));
""",
        "healRenamedButton": ("""        driver.get(Fixtures.url("v1.html"));
        healer.element("Form.save", org.openqa.selenium.By.id("save")).click();
        driver.get(Fixtures.url("v2.html"));
        healer.element("Form.save", org.openqa.selenium.By.id("save")).click();
""", """        Fixtures.check("Saved".equals(driver.findElement(org.openqa.selenium.By.id("out")).getText()), "Saved expected after the healed click");
"""),
        "healRenamedField": ("""        driver.get(Fixtures.url("v1.html"));
        healer.element("Form.nameField", org.openqa.selenium.By.id("name")).fill("Jane");
        driver.get(Fixtures.url("v2.html"));
        healer.element("Form.nameField", org.openqa.selenium.By.id("name")).fill("Jane Doe");
""", """        Fixtures.check("Jane Doe".equals(driver.findElement(org.openqa.selenium.By.id("full-name")).getDomProperty("value")),
                "the healed name field was filled");
"""),
        "plainLanguageStep": ("""        driver.get(Fixtures.url("v2.html"));
        healer.find("Form.email", "the email field").fill("jane@example.com");
""", """        Fixtures.check("jane@example.com".equals(driver.findElement(org.openqa.selenium.By.id("mail")).getDomProperty("value")),
                "the email field was filled");
"""),
        "removedButtonNotHealed": ("""        driver.get(Fixtures.url("v1.html"));
        healer.element("Form.cancel", org.openqa.selenium.By.id("cancel")).click();
        driver.get(Fixtures.url("v3.html"));
""", """        Fixtures.expectFailure(() -> healer.element("Form.cancel", org.openqa.selenium.By.id("cancel")).click(),
                "a removed button must not be healed to another one");
        Fixtures.check(driver.findElement(org.openqa.selenium.By.id("out")).getText().isEmpty(), "no other button was clicked");
"""),
    },
}


for _driver, _bodies in sites.BODIES.items():
    BODIES[_driver].update(_bodies)


def lifecycle(driver, parallel):
    """(fields, open, close) - the browser comes from the settings (HealerBrowser / HealerDriver)."""
    if driver == "playwright" and not parallel:
        return (f"""    static {PW}Playwright playwright;
    static {PW}Browser browser;
    {PW}BrowserContext context;
    {PW}Page page;
    {HP}SelfHealingPage healer;
""", f"""        if (browser == null) {{
            playwright = {PW}Playwright.create();
            browser = {HP}HealerBrowser.launch(playwright);   // browser.name, browser.headless, browser.slowmo
        }}
        context = {HP}HealerBrowser.newContext(browser);        // browser.viewport, timeoutMs, video, trace
        page = context.newPage();
        healer = {HP}SelfHealingPage.wrap(page);
""", f"""        {HP}HealerBrowser.close(context);                       // keeps video / trace of a failed test
""")
    if driver == "selenium" and not parallel:
        return (f"""    static {SE}WebDriver driver;
    {HS}SelfHealingDriver healer;
""", f"""        if (driver == null) {{
            driver = {HS}HealerDriver.create();   // browser.name, browser.headless, browser.viewport, browser.timeoutMs
            Runtime.getRuntime().addShutdownHook(new Thread(driver::quit));
        }}
        healer = {HS}SelfHealingDriver.wrap(driver);
""", "")
    who = '        System.out.println("[matrix-thread] " + Thread.currentThread().getName());\n'
    if driver == "playwright":
        return (f"""    // every thread its own browser, context, page and healer (TestNG shares one instance between threads)
    static final ThreadLocal<{PW}Browser> BROWSER = ThreadLocal.withInitial(() -> {{
        {PW}Playwright playwright = {PW}Playwright.create();
        Runtime.getRuntime().addShutdownHook(new Thread(playwright::close));
        return {HP}HealerBrowser.launch(playwright);
    }});
    static final ThreadLocal<{PW}BrowserContext> CONTEXT = new ThreadLocal<>();
    static final ThreadLocal<{PW}Page> PAGE = new ThreadLocal<>();
    static final ThreadLocal<{HP}SelfHealingPage> HEALER = new ThreadLocal<>();
""", who + f"""        CONTEXT.set({HP}HealerBrowser.newContext(BROWSER.get()));
        PAGE.set(CONTEXT.get().newPage());
        HEALER.set({HP}SelfHealingPage.wrap(PAGE.get()));
""", f"""        {HP}HealerBrowser.close(CONTEXT.get());
""")
    return (f"""    // every thread its own browser and healer (TestNG shares one instance between threads)
    static final ThreadLocal<{SE}WebDriver> DRIVER = ThreadLocal.withInitial(() -> {{
        {SE}WebDriver driver = {HS}HealerDriver.create();
        Runtime.getRuntime().addShutdownHook(new Thread(driver::quit));
        return driver;
    }});
    static final ThreadLocal<{HS}SelfHealingDriver> HEALER = new ThreadLocal<>();
""", who + f"""        HEALER.set({HS}SelfHealingDriver.wrap(DRIVER.get()));
""", "")


def bodies(driver, parallel):
    b = BODIES[driver]
    if not parallel:
        return b
    if driver == "playwright":
        swap = lambda code: code.replace("page.", "PAGE.get().").replace("healer.", "HEALER.get().") \
            .replace("(page, healer)", "(PAGE.get(), HEALER.get())")
    else:
        swap = lambda code: code.replace("driver.", "DRIVER.get().").replace("healer.", "HEALER.get().") \
            .replace("(driver, healer)", "(DRIVER.get(), HEALER.get())")
    return {k: (swap(v) if isinstance(v, str) else (swap(v[0]), swap(v[1]))) for k, v in b.items()}


FIXTURES = """package matrix;

/** Bundled test pages and framework-neutral assertions (work under every runner). */
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

    /** The action must fail - e.g. a removed element must not be "healed" to another one. */
    public static void expectFailure(Runnable action, String message) {
        try {
            action.run();
        } catch (RuntimeException expected) {
            return;
        }
        throw new AssertionError(message);
    }

    public static boolean containsAll(String text, String... parts) {
        for (String p : parts) {
            if (!text.contains(p)) return false;
        }
        return true;
    }

    /** The TripForge / ShopLab scenarios run unless -Dmatrix.skipSites=true. */
    public static boolean sites() {
        return !Boolean.getBoolean("matrix.skipSites");
    }

    /** Fails only when the run is started with -Dmatrix.fail=true. */
    public static void failWhenAsked() {
        check(!Boolean.getBoolean("matrix.fail"), "deliberate failure (-Dmatrix.fail=true)");
    }
}
"""


def plain_test(driver, runner, parallel=False, cls="HealingTest"):
    fields, open_, close = lifecycle(driver, parallel)
    b = bodies(driver, parallel)
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
    methods = "".join(f"""
    {test}
    public void {name}() {{
{b[name][0]}{b[name][1]}    }}
""" for name in TESTS if name != "deliberateFailure")
    return f"""package matrix;

/** {driver} + {runner}: the same tests in every combination. The browser comes from healer.properties. */
{head}public class {cls} {{

{rule}{fields}
    {before}
    public void open() {{
{open_}    }}

    {after}
    public void close() {{
{close}    }}
{methods}
    {test}
    public void deliberateFailure() {{
{b["open"]}        Fixtures.failWhenAsked();
    }}
}}
"""


FEATURE = """Feature: Matrix
  Scenario: Heal a renamed button
    When I save on the original page and again on the changed page
    Then the page says Saved

  Scenario: Heal a renamed field
    When I type my name on the original page and again on the changed page
    Then the changed name field has the value

  Scenario: Plain-language step
    When I fill the email field by its description
    Then the email field has the value

  Scenario: A removed button is not healed
    When I cancel on the original page and open a page without the Cancel button
    Then no other button is used instead

  Scenario: Deliberate failure
    When I save on the original page and again on the changed page
    Then it fails when asked
""" + sites.FEATURE

STEPS = [  # (annotation, method, test, part)
    ('@When("I save on the original page and again on the changed page")', "save", "healRenamedButton", 0),
    ('@Then("the page says Saved")', "saved", "healRenamedButton", 1),
    ('@When("I type my name on the original page and again on the changed page")', "type", "healRenamedField", 0),
    ('@Then("the changed name field has the value")', "typed", "healRenamedField", 1),
    ('@When("I fill the email field by its description")', "fill", "plainLanguageStep", 0),
    ('@Then("the email field has the value")', "filled", "plainLanguageStep", 1),
    ('@When("I cancel on the original page and open a page without the Cancel button")', "cancel", "removedButtonNotHealed", 0),
    ('@Then("no other button is used instead")', "notReplaced", "removedButtonNotHealed", 1),
] + sites.STEPS

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
junit.jupiter.execution.parallel.config.fixed.max-pool-size=3
"""
TESTNG_PARALLEL = """testng.parallel=methods
testng.threadCount=3
"""
# Cucumber's parallel @DataProvider would run 10 scenarios (10 browsers) at once by default
CUCUMBER_TESTNG_PARALLEL = """testng.dataProviderThreadCount=3
"""


def cucumber(driver, runner, parallel=False):
    fields, open_, close = lifecycle(driver, parallel)
    b = bodies(driver, parallel)
    steps_code = "".join(f"""
    {ann}
    public void {method}() {{
{b[test][part]}    }}
""" for ann, method, test, part in STEPS)
    steps = f"""package matrix;

import io.cucumber.java.After;
import io.cucumber.java.Before;
import io.cucumber.java.en.Then;
import io.cucumber.java.en.When;

/** {driver} + {runner}: glue for features/*.feature. The browser comes from healer.properties. */
public class Steps {{

{fields}
    @Before
    public void open() {{
{open_}    }}

    @After
    public void close() {{
{close}    }}
{steps_code}
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
    for file, java in sites.JAVA[driver].items():
        w(os.path.join(src, file), java)
    for page, html in (("v1.html", V1), ("v2.html", V2), ("v3.html", V3)):
        w(os.path.join(res, "pages", page), html)
    w(os.path.join(res, "healer.properties"), props(driver))
    # like every real project: the fingerprints recorded on the original ShopLab site, committed in .healer/
    shutil.rmtree(os.path.join(d, ".healer"), ignore_errors=True)
    os.makedirs(os.path.join(d, ".healer"))
    shutil.copy(BASELINE[driver], os.path.join(d, ".healer", "fingerprints.json"))
    w(os.path.join(res, "simplelogger.properties"), "org.slf4j.simpleLogger.defaultLogLevel=warn\n")
    copies = 2 if parallel else 1
    if runner.startswith("cucumber"):
        steps, run = cucumber(driver, runner, parallel)
        w(os.path.join(src, "Steps.java"), steps)
        w(os.path.join(src, "RunCucumberTest.java"), run)
        w(os.path.join(res, "features", "matrix.feature"), FEATURE)
        if parallel:   # a second feature with the same steps (and element keys), scenario names kept apart
            second = FEATURE.replace("Feature: Matrix", "Feature: Matrix 2")
            for title in TESTS.values():
                second = second.replace("Scenario: " + title + "\n", "Scenario: " + title + " 2\n")
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
    if parallel and runner == "cucumber-testng":
        platform += CUCUMBER_TESTNG_PARALLEL
    if platform:
        w(os.path.join(res, "junit-platform.properties"), platform)
    # what run_all.py expects from this project
    w(os.path.join(d, "matrix.json"), json.dumps({
        "tests": len(TESTS) * copies, "failures": copies, "heals": 2 * copies, "parallel": parallel,
        "names": list(TESTS) + list(TESTS.values()), "video": driver == "playwright", "driver": driver}) + "\n")
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
