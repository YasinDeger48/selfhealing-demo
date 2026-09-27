# TripForge self-healing lab tests

Tests for the public lab page <https://trip-forge-lbuh.vercel.app/self-healing-lab>. Every page load
generates new ids, test ids, names and classes (a random 8-character suffix), renames labels and reorders
the fields. The page also contains decoys: "Example reservation", "Find example booking", "Approve journey
details" and "Go back".

The page object (`SelfHealingLabPage`) uses selectors recorded from **one** load (suffix `fe465c1e`).
They never match again, so every step is healed:

1. No fingerprint has been recorded (the selector never worked), so one is **derived from the selector**
   (`#passenger-surname-fe465c1e` -> id ~ "passenger-surname" + a generated part).
2. The local heuristic finds the element (`passenger-surname-3fc4aa85` has the same id apart from the generated
   part) and skips the decoys.
3. The healed element's real fingerprint (placeholder, label, name, position ...) is **learned** into
   `.healer/fingerprints.json` for the next runs.

| Test | What it checks |
|------|----------------|
| `lookupShowsItinerary` | Booking lookup (TFH-2026 / IPEK) shows TF-222 Istanbul -> Madrid (3 heals) |
| `fullVerificationCompletes` | Full flow reaches `SELF-HEALING-COMPLETE` (6 heals) |
| `survivesRepeatedReloads` | Same flow on 3 reloads, each with a new locator set (18 heals) |

## Run

The framework comes from Maven Central (`io.github.yasindeger48`), nothing to install. In this folder:

```bash
# headless, local healing only ($0)
mvn test -Dhealer.llm.enabled=false

# watch it: browser opens, healing steps are drawn on the page
mvn test -Dbrowser.headless=false -Dhealer.visual=true -Dbrowser.slowmo=300 -Dtest=SelfHealingLabTest#fullVerificationCompletes

# start from zero (forget learned fingerprints and cached heals)
rm -rf .healer
```

Report: `target/healer-report/healing-report.html` (and `.pdf`).

Claude is used only when the local heuristic is not confident; set `ANTHROPIC_API_KEY` and leave
`healer.llm.enabled=true` to allow it. Try breaking the selectors in `SelfHealingLabPage` further
(e.g. `button:has-text('Find booking')`) to see where local healing stops and Claude takes over.
