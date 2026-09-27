"""Runs `mvn test` in every generated project and writes RESULTS.md (see README.md)."""
import json, os, re, shutil, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
MVN = "mvn.cmd" if os.name == "nt" else "mvn"
EXPECTED = {"healRenamedButton", "plainLanguageStep", "deliberateFailure", "Heal a renamed button", "Plain-language step",
            "Deliberate failure"}


def expected(project):
    """matrix.json written by generate.py: number of report tests and deliberate failures, parallel or not."""
    f = os.path.join(HERE, project, "matrix.json")
    return json.load(open(f, encoding="utf-8")) if os.path.exists(f) else {"tests": 3, "failures": 1, "parallel": False}


def run(project, fail=False):
    d = os.path.join(HERE, project)
    if not fail:   # start from zero: a store left by an earlier run would find the elements without healing
        shutil.rmtree(os.path.join(d, "target", "healer-store"), ignore_errors=True)
    t0 = time.time()
    cmd = [MVN, "-B", "test"] + (["-Dmatrix.fail=true"] if fail else [])
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
        r["steps"] = sum(len(t.get("steps", [])) for t in tests)
        failed = [t for t in tests if t.get("status") == "FAILED"]
        r["failedTests"] = len(failed)
        r["triage"] = ",".join(sorted({(t.get("triage") or {}).get("category", "none") for t in failed}))
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
        if r["heals"] < 1:
            notes.append("no heal recorded")
        if r["found"] < 1:
            notes.append("plain-language step not recorded")
        if r["unattributed"]:
            notes.append(f"{r['unattributed']} event(s) not tied to a test")
        extra = [i for i in r["reportIds"] if not any(e in i for e in EXPECTED)]
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
    results = []
    for p in projects:
        print("running", p, flush=True)
        r = run(p)
        r["verdict"] = verdict(r)
        # second run: one test fails on purpose - the build must fail and the report must analyse it
        f = run(p, fail=True)
        problems = []
        if f["build"] == "OK":
            problems.append("a failing test did NOT fail the build")
        want = expected(p)["failures"]
        if f.get("failedTests", 0) != want:
            problems.append(f"{f.get('failedTests', 0)} failed test(s) in the report instead of {want}")
        elif f.get("triage") != "ASSERTION":
            problems.append("failure analysis: " + str(f.get("triage")))
        r["failRun"] = "OK" if not problems else "; ".join(problems)
        print("  ", r["verdict"], "| failing run:", r["failRun"], flush=True)
        results.append(r)
    # a partial run (only some projects) keeps the other projects' last results
    previous = os.path.join(HERE, "results.json")
    if len(sys.argv) > 1 and os.path.exists(previous):
        ran = {r["project"] for r in results}
        results = sorted([r for r in json.load(open(previous, encoding="utf-8")) if r["project"] not in ran] + results,
                         key=lambda r: r["project"])
    json.dump(results, open(previous, "w", encoding="utf-8"), indent=2)
    lines = ["# Compatibility results", "",
             "| Combination | Build | Surefire provider | Tests run | Report tests | Heals | Found by description | Steps | Threads | Result | Failing test fails the build |",
             "|---|---|---|---:|---:|---:|---:|---:|---:|---|---|"]
    for r in results:
        lines.append(f"| {r['project']} | {r['build']} | {r['provider']} | {r['surefireTests']} | {r.get('reportTests', 0)} | "
                     f"{r.get('heals', '-')} | {r.get('found', '-')} | {r.get('steps', '-')} | {r.get('threads') or '-'} | {r['verdict']} | {r['failRun']} |")
    open(os.path.join(HERE, "RESULTS.md"), "w", encoding="utf-8", newline="\n").write("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
