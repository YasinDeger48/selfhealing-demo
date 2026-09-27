"""One layout for src/test/resources/healer.properties in every project of this repository.

render(values, driver, title) writes all settings a test project normally manages - application, browser, healing,
Claude, report - with a short explanation each. `values` overrides the defaults; settings not in the layout are kept
in a "project-specific" section at the end, so nothing a project set is lost.
Used by compatibility-matrix/generate.py and tools/apply_config.py (the example projects).
"""
import re

HEADER = """# {title}
#
# Settings of the self-healing framework (io.github.yasindeger48:healer-*). Where values come from, later wins:
#   1. this file
#   2. healer-<profile>.properties   (-Dhealer.profile=ci  or  HEALER_PROFILE=ci)
#   3. healer-local.properties       (your own overrides - not committed)
#   4. environment variables          HEALER_MODE=off, BROWSER_HEADLESS=false, APP_BASEURL=...
#   5. -D on the command line         mvn test -Dbrowser.headless=false -Dhealer.enabled=false
# Values may reference ${{env:NAME:-default}} or ${{sys:name}}; a trailing "# comment" is ignored.
"""

# (section, [(key, default, explanation, drivers)]) - drivers: "both" | "playwright"
LAYOUT = [
    ("Application", [
        ("app.baseUrl", "", "Address of the application under test - HealerBrowser.url(\"/login\") / HealerDriver.url(...)", "both"),
    ]),
    ("Browser", [
        ("browser.name", "msedge", None, "both"),
        ("browser.headless", "true", "true = no window; false = watch the run", "both"),
        ("browser.slowmo", "0", "Milliseconds between browser actions - e.g. 300 to follow a run with your eyes", "playwright"),
        ("browser.viewport", "1280x900", "Window / viewport size", "both"),
        ("browser.timeoutMs", "15000", "Default timeout of actions (Playwright) / page loads (Selenium), ms", "both"),
        ("browser.video", "off", "off | failures | all - video of the test, linked in the report", "playwright"),
        ("browser.trace", "off", "off | failures | all - Playwright trace (npx playwright show-trace file.zip)", "playwright"),
    ]),
    ("Healing", [
        ("healer.enabled", "true", "false = healer switched off completely: plain locators, no report, no analysis", "both"),
        ("healer.mode", "auto", "auto = heal and continue (WARN) | suggest = report the replacement, fail the step | off = no healing", "both"),
        ("healer.probeTimeoutMs", "3000", "How long the original selector may take before it counts as broken (SPA render delay), ms", "both"),
        ("healer.minConfidence", "0.60", "Matches scoring below this are rejected", "both"),
        ("healer.minMargin", "0.08", "The best match must beat the runner-up by this much (no guessing between look-alikes)", "both"),
        ("healer.failOnHeal", "false", "true = a healed test fails instead of passing with WARN (strict CI)", "both"),
        ("healer.popups", "auto", "auto = close cookie banners / overlays covering an element | off", "both"),
        ("healer.fix", "patch", "Code fixes for healed locators: patch (locator-fixes.patch) | apply (edit the sources) | off", "both"),
        ("healer.storeDir", ".healer", "Learned fingerprints and heals - commit this folder to share them", "both"),
    ]),
    ("AI stage (Claude) - needs the healer-claude dependency", [
        ("healer.llm.enabled", "false", "true = ask Claude when the local matching is not sure (about $0.002 per heal)", "both"),
        ("#healer.llm.apiKey", "${env:ANTHROPIC_API_KEY}", "API key - default: the ANTHROPIC_API_KEY environment variable. Never write the key itself here", "both"),
        ("healer.llm.model", "claude-haiku-4-5", "First model asked", "both"),
        ("healer.llm.escalateTo", "claude-opus-5", "Asked when the first model is not sure (empty = never)", "both"),
        ("#healer.llm.maxCostPerRun", "1.00", "USD budget per run - Claude is skipped after it (no limit when not set)", "both"),
        ("healer.llm.maxCallsPerRun", "50", "Claude calls per run at most", "both"),
    ]),
    ("Report", [
        ("healer.language", "en", "en | de | ru | ja | tr | ar - console, report and Claude's explanations", "both"),
        ("healer.reportDir", "target/healer-report", "Where the report is written", "both"),
        ("healer.report.open", "never", "Open the HTML report after the run: never | always | onFailure | onWarn (never on CI)", "both"),
        ("healer.report.pdf", "auto", "Also write a PDF: auto (not on CI) | true | false", "both"),
        ("healer.report.screenshots", "all", "all | failures | none", "both"),
        ("healer.report.history", "false", "true = keep every run's report in history/<time>/", "both"),
        ("healer.verbose", "true", "Print every healing step to the console", "both"),
        ("healer.visual", "false", "Draw the healing steps on the page - for headed demos", "both"),
    ]),
]

BROWSER_NAMES = {
    "playwright": "chromium | msedge | chrome | firefox | webkit",
    "selenium": "edge | chrome | firefox | safari",
}

LEGACY = {"healer.screenshots": lambda v: ("healer.report.screenshots", "none" if v.strip().lower() == "false" else "all")}


def parse(text):
    """key -> value of a .properties file (comments and blank lines dropped, legacy names converted)."""
    values = {}
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        k, v = k.strip(), v.strip()
        if k in LEGACY:
            k, v = LEGACY[k](v)
            values.setdefault(k, v)
            continue
        values[k] = v
    return values


def render(values, driver, title):
    values = dict(values)
    out = [HEADER.format(title=title)]
    used = set()
    for section, keys in LAYOUT:
        out.append(f"\n# ---- {section} " + "-" * max(4, 100 - len(section)) + "\n")
        for key, default, explanation, drivers in keys:
            commented = key.startswith("#")
            name = key.lstrip("#")
            if drivers == "playwright" and driver != "playwright":
                used.add(name)
                continue
            if name == "browser.name":
                explanation = BROWSER_NAMES[driver]
            if explanation:
                out.append(f"# {explanation}\n")
            if name in values:
                out.append(f"{name}={values[name]}\n")
            else:
                out.append(f"{'#' if commented else ''}{name}={default}\n")
            used.add(name)
    extra = [(k, v) for k, v in values.items() if k not in used]
    if extra:
        out.append("\n# ---- Project-specific " + "-" * 83 + "\n")
        for k, v in extra:
            out.append(f"{k}={v}\n")
    return "".join(out)


def keys():
    return [k.lstrip("#") for _, ks in LAYOUT for k, *_ in ks]


if __name__ == "__main__":
    print(render({"app.baseUrl": "http://localhost:8080"}, "playwright", "Example"))
    assert re.search(r"^healer.enabled=true$", render({}, "selenium", "x"), re.M)
