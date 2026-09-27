"""Brings every example project's healer.properties into the common layout (tools/healer_config.py), keeping the values
it already has; adds the "ci" profile and ignores healer-local.properties where missing.
Run: python tools/apply_config.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import healer_config  # noqa: E402

# folder, driver, title
PROJECTS = [
    ("shoplab-tests", "playwright", "ShopLab tests - Playwright + JUnit 5"),
    ("shoplab-selenium-tests", "selenium", "ShopLab tests - Selenium + JUnit 5"),
    ("tripforge-tests", "playwright", "TripForge tests - Playwright + JUnit 5"),
    ("tripforge-cucumber-tests", "playwright", "TripForge tests - Playwright + Cucumber"),
    ("tripforge-testng-tests", "playwright", "TripForge tests - Playwright + TestNG"),
    (os.path.join("healing-framework", "integration", "gradle-junit5"), "playwright", "Gradle check - Playwright + JUnit 5"),
]

CI = """# The "ci" profile: -Dhealer.profile=ci (or HEALER_PROFILE=ci). Loaded on top of healer.properties.
# CI machines usually have no Edge and nobody watches the browser or opens the report.
browser.name={browser}
browser.headless=true
healer.verbose=false
healer.report.open=never
healer.report.history=false
"""


def main():
    for folder, driver, title in PROJECTS:
        res = os.path.join(ROOT, folder, "src", "test", "resources")
        path = os.path.join(res, "healer.properties")
        values = healer_config.parse(open(path, encoding="utf-8").read())
        open(path, "w", encoding="utf-8", newline="\n").write(healer_config.render(values, driver, title))
        ci = os.path.join(res, "healer-ci.properties")
        if not os.path.exists(ci) and "gradle" not in folder:
            open(ci, "w", encoding="utf-8", newline="\n").write(CI.format(browser="chromium" if driver == "playwright" else "chrome"))
        ignore = os.path.join(ROOT, folder, ".gitignore")
        text = open(ignore, encoding="utf-8").read() if os.path.exists(ignore) else ""
        if "healer-local.properties" not in text:
            open(ignore, "a", encoding="utf-8", newline="\n").write(("" if text.endswith("\n") or not text else "\n")
                                                                   + "# personal settings (healer-local.properties)\nhealer-local.properties\n")
        print("configured", folder)


if __name__ == "__main__":
    main()
