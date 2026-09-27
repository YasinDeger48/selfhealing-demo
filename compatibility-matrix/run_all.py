"""Runs `mvn test` in every generated project and writes RESULTS.md (see README.md).

Needs the ShopLab demo site on http://localhost:8080 (cd ../demo-site && npm run dev). For the run the site is broken
with `mutate.py --level high` and restored afterwards; every project starts from its .healer/ baseline - the
fingerprints ../shoplab-tests or ../shoplab-selenium-tests recorded on the original site - and is reset to it after.
"""
import json, os, re, shutil, subprocess, sys, time, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
MVN = "mvn.cmd" if os.name == "nt" else "mvn"
SHOPLAB = os.environ.get("SHOPLAB_URL", "http://localhost:8080")
BASELINE = {"playwright": os.path.join(ROOT, "shoplab-tests", ".healer", "fingerprints.json"),
            "selenium": os.path.join(ROOT, "shoplab-selenium-tests", ".healer", "fingerprints.json")}
SHOPLAB_KEYS = ("LoginPage.", "ProductsPage.", "Header.")


def reset_store(project):
    """The project's .healer/ back to what generate.py wrote: only the ShopLab fingerprints of the original site."""
    store = os.path.join(HERE, project, ".healer")
    shutil.rmtree(store, ignore_errors=True)
    os.makedirs(store)
    shutil.copy(BASELINE[expected(project).get("driver", "playwright")], os.path.join(store, "fingerprints.json"))


def mutate(*args):
    subprocess.run([sys.executable, os.path.join(ROOT, "demo-site", "mutate.py"), *args], check=True,
                   capture_output=True, text=True)


def expected(project):
    """matrix.json written by generate.py: number of report tests and deliberate failures, parallel or not."""
    f = os.path.join(HERE, project, "matrix.json")
    want = {"tests": 3, "failures": 1, "heals": 1, "parallel": False, "video": False,
            "names": ["healRenamedButton", "plainLanguageStep", "deliberateFailure"]}
    if os.path.exists(f):
        want.update(json.load(open(f, encoding="utf-8")))
    return want


def run(project, fail=False):
    d = os.path.join(HERE, project)
    if not fail:   # start from zero: a store left by an earlier run would find the elements without healing
        reset_store(project)
    t0 = time.time()
    # the failing run only checks the build and the failure analysis: no real-site scenarios
    cmd = [MVN, "-B", "test"] + (["-Dmatrix.fail=true", "-Dmatrix.skipSites=true"] if fail else [])
    p = subprocess.run(cmd, cwd=d, capture_output=True, text=True, encoding="utf-8", errors="replace")
    out = p.stdout + p.stderr
    open(os.path.join(d, "run-fail.log" if fail else "run.log"), "w", encoding="utf-8").write(out)
    tests_run = sum(int(m) for m in re.findall(r"Tests run: (\d+), Failures: \d+, Errors: \d+, Skipped: \d+$", out, re.M)[-1:])
    provider = (re.findall(r"Using auto detected provider (\S+)", out) or ["?"])[-1].split(".")[-1]
    report = os.path.join(d, "target", "healer-report", "healing-report.json")
    r = {"project": project, "build": "OK" if p.returncode == 0 else "FAILED", "surefireTests": tests_run,
         "provider": provider, "seconds": round(time.time() - t0),
         "threads": len(set(re.findall(r"^\[matrix-thread\] (.+)$", out, re.M)))}
    if os.path.exists(report):
        rep = json.load(open(report, encoding="utf-8"))
        tests = rep.get("tests", [])
        events = rep.get("events", [])
        r["reportTests"] = len(tests)
        r["reportIds"] = [t["id"] for t in tests]
        r["passed"] = sum(1 for t in tests if t.get("status") == "PASSED")
        r["heals"] = sum(1 for e in events if e.get("kind") is None and e.get("status") == "HEALED")
        r["found"] = sum(1 for e in events if e.get("kind") == "intent" and e.get("status") == "HEALED")
        r["unattributed"] = sum(1 for e in events if e.get("test") == "(outside test)")
        # a removed element must never be "healed" to another one
        r["wrongHeals"] = sum(1 for e in events if e.get("key") == "Form.cancel" and e.get("status") == "HEALED")
        healed = [e for e in events if e.get("status") == "HEALED" and e.get("kind") is None]
        r["tripforgeHeals"] = sum(1 for e in healed if (e.get("key") or "").startswith("Lab."))
        r["shoplabHeals"] = sum(1 for e in healed if (e.get("key") or "").startswith(SHOPLAB_KEYS))
        r["heals"] = sum(1 for e in healed if (e.get("key") or "").startswith("Form."))
        r["steps"] = sum(len(t.get("steps", [])) for t in tests)
        failed = [t for t in tests if t.get("status") == "FAILED"]
        r["failedTests"] = len(failed)
        r["triage"] = ",".join(sorted({(t.get("triage") or {}).get("category", "none") for t in failed}))
        r["failedWithMedia"] = sum(1 for t in failed if t.get("video") or t.get("trace"))
    else:
        r["reportTests"] = 0
    errors = [l.strip() for l in out.splitlines() if l.startswith("[ERROR]") and ("Tests run" not in l)]
    r["firstError"] = errors[0][:200] if errors else ""
    return r


def verdict(r):
    want = expected(r["project"])
    notes = []
    if r["build"] != "OK":
        notes.append("build failed")
    if r["surefireTests"] == 0:
        notes.append("no test ran")
    if r["reportTests"] == 0:
        notes.append("no report")
    else:
        if r["heals"] < want["heals"]:
            notes.append(f"{r['heals']} heal(s) instead of {want['heals']}")
        if r.get("tripforgeHeals", 0) < 1:
            notes.append("no TripForge heal")
        if r.get("shoplabHeals", 0) < 1:
            notes.append("no ShopLab heal")
        if r.get("wrongHeals"):
            notes.append(f"a removed button was healed to another element ({r['wrongHeals']}x)")
        if r["found"] < 1:
            notes.append("plain-language step not recorded")
        if r["unattributed"]:
            notes.append(f"{r['unattributed']} event(s) not tied to a test")
        extra = [i for i in r["reportIds"] if not any(e in i for e in want["names"])]
        if extra:
            notes.append("extra report tests: " + ", ".join(extra))
        if r["reportTests"] != want["tests"]:
            notes.append(f"{r['reportTests']} report tests instead of {want['tests']}")
    if want["parallel"] and r["threads"] < 2:
        notes.append(f"not parallel ({r['threads']} thread)")
    return "OK" if not notes else "; ".join(notes)


def main():
    projects = sorted(p for p in os.listdir(HERE) if os.path.isfile(os.path.join(HERE, p, "pom.xml")))
    if len(sys.argv) > 1:
        projects = [p for p in projects if p in sys.argv[1:]]
    try:
        urllib.request.urlopen(SHOPLAB, timeout=5)
    except OSError as e:
        sys.exit(f"ShopLab is not running on {SHOPLAB} ({e}) - start it: cd ../demo-site && npm run dev")
    mutate("--level", "high")   # the ShopLab scenarios run against a changed site
    try:
        results = run_projects(projects)
    finally:
        mutate("--reset")
    write(results)


def run_projects(projects):
    results = []
    for p in projects:
        print("running", p, flush=True)
        r = run(p)
        r["verdict"] = verdict(r)
        # second run: one test fails on purpose - the build must fail and the report must analyse it
        f = run(p, fail=True)
        reset_store(p)   # leave the committed baseline as it was
        problems = []
        if f["build"] == "OK":
            problems.append("a failing test did NOT fail the build")
        want = expected(p)["failures"]
        if f.get("failedTests", 0) != want:
            problems.append(f"{f.get('failedTests', 0)} failed test(s) in the report instead of {want}")
        elif f.get("triage") != "ASSERTION":
            problems.append("failure analysis: " + str(f.get("triage")))
        r["media"] = f"{f.get('failedWithMedia', 0)}/{f.get('failedTests', 0)}" if expected(p)["video"] else "-"
        r["failRun"] = "OK" if not problems else "; ".join(problems)
        print("  ", r["verdict"], "| failing run:", r["failRun"], flush=True)
        results.append(r)
    return results


def write(results):
    # a partial run (only some projects) keeps the other projects' last results
    previous = os.path.join(HERE, "results.json")
    if len(sys.argv) > 1 and os.path.exists(previous):
        ran = {r["project"] for r in results}
        results = sorted([r for r in json.load(open(previous, encoding="utf-8")) if r["project"] not in ran] + results,
                         key=lambda r: r["project"])
    json.dump(results, open(previous, "w", encoding="utf-8"), indent=2)
    lines = ["# Compatibility results", "",
             "| Combination | Build | Surefire provider | Tests run | Report tests | Heals | TripForge heals | ShopLab heals | Found by description | Steps | Threads | Video/trace of failed tests | Result | Failing test fails the build |",
             "|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|"]
    for r in results:
        lines.append(f"| {r['project']} | {r['build']} | {r['provider']} | {r['surefireTests']} | {r.get('reportTests', 0)} | "
                     f"{r.get('heals', '-')} | {r.get('tripforgeHeals', '-')} | {r.get('shoplabHeals', '-')} | {r.get('found', '-')} | {r.get('steps', '-')} | {r.get('threads') or '-'} | {r.get('media', '-')} | {r['verdict']} | {r['failRun']} |")
    open(os.path.join(HERE, "RESULTS.md"), "w", encoding="utf-8", newline="\n").write("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
