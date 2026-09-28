# LinkedIn texts - English

Put the links into the **first comment**, not the post (LinkedIn shows posts with external links to fewer people).
3-5 hashtags per post are enough.

---

## 1. Launch post (with the carousel: `carousel/self-healing-en.pdf`)

> Upload as a document ("Add a document"), title: **Your locator broke. Your test didn't.**

A renamed id should not cost you a red build.

A release renames `#login-username` to `#user-name`. Nothing is broken for the user - but every test that touches the login fails, and someone spends the morning updating page objects. I have been that someone too often, so I built a fix.

**Self-healing locator framework** - an open-source Java library for Playwright and Selenium tests:

🔹 When a selector finds nothing, the test doesn't fail: the framework finds the element that best matches its recorded fingerprint (tag, ids, text, label, position).
🔹 Local matching first: free, milliseconds. Only when it is not sure, it can ask Claude (optional, ~$0.002 per heal).
🔹 It doesn't guess: if an element is really gone, it says "not healable". Wrong elements picked in the benchmark: 0.
🔹 The test passes with a WARN, and the report tells you what to fix: old → new selector, source line and a ready-made code fix.

Measured on a broken demo shop (86 elements):
• ids renamed: 100%
• ids + texts + structure changed: 87% locally, 98.8% with Claude
• deleted elements: 100% correctly refused

Tested in 20 combinations with JUnit 5/4, TestNG and Cucumber, in parallel, on Java 17/21/25, Linux and Windows. On Maven Central - one dependency, one settings file.

Code, demo site and compatibility tests are in the first comment. If you try it on your project, I'd love to hear how it went. 👇

#TestAutomation #Playwright #Selenium #QA #Java

---

## 2. Video post (`video/healing-demo-1280x800.webm` - convert to MP4 for LinkedIn: README)

Watching a test repair itself for the first time is a strange feeling. 🎬

In this video the demo shop's UI changed in a "new release": ids, test ids, button texts... The test runs with the old selectors.

At every step you see:
❌ the old selector finds nothing
🔍 the candidates on the page are scored (orange boxes)
✅ the best one is accepted (green box) and the test goes on

All local, Claude off, $0. At the end, the report says which page-object line to update.

The overlay is one setting: `healer.visual=true`. Playwright and Selenium.

Link in the first comment. 👇

#TestAutomation #SelfHealing #Playwright #QA

---

## 3. Series - "A wrong heal is worse than a failed test" (picture: `images/en/06-guards.png`)

The most dangerous bug of a self-healing tool: "finding" the wrong element. 🚨

The test goes green - but it clicked another button. A red test is at least honest.

So the framework has guards that come before any threshold. Whatever the score, it never picks:
• another item of a list (add-to-cart #5 instead of #8)
• the opposite control (decrease for increase, logout for login)
• a field for a button, a div for `fill`
• an element another locator already owns

In the benchmark: 0 wrong elements across 373 broken ones, and 100% of the deleted elements reported as "not healable".

An honest failure instead of a guess. 🙂

#TestAutomation #QualityEngineering #SoftwareTesting

---

## 4. Series - Cost (picture: `images/en/07-benchmark.png`)

"Isn't healing tests with AI expensive?" 💸

I measured it. 373 broken elements, 5 levels of breakage, on an 86-element demo shop:
• The local heuristic goes first - free, milliseconds. Most heals end here.
• Claude is asked only when that is not sure - with the best local candidates only.
• Total Claude cost: **$0.13**. About $0.002 per heal.

On top: a healed locator is cached, later runs pay nothing again. And you can set a budget per run (`healer.llm.maxCostPerRun`).

Personal data is masked before anything is sent to Claude.

#AI #TestAutomation #Claude #QA

---

## 5. Series - Compatibility (picture: `images/en/09-compatibility.png`)

"Will it work with our stack?" - answered with tests, not guesses. ✅

20 projects, each running the same 10 tests twice (once green, once with a deliberate failure):
• Playwright and Selenium × JUnit 5, JUnit 4, TestNG, Cucumber (on JUnit 5 / TestNG / JUnit 4)
• parallel runs, older versions such as Playwright 1.45 and Selenium 4.21
• real sites: a self-healing lab that changes every id on every load, and the broken demo shop

In the latest round these tests found 6 real bugs - all fixed, with notes in the repository.

#Java #TestAutomation #Playwright #Selenium

---

## First comment (under every post)

🔗 Framework (source, docs): https://github.com/YasinDeger48/selfhealing-framework
🔗 Demo site, example projects, compatibility matrix: https://github.com/YasinDeger48/selfhealing-demo
📦 Maven Central: https://central.sonatype.com/namespace/io.github.yasindeger48

```xml
<dependency>
  <groupId>io.github.yasindeger48</groupId>
  <artifactId>healer-playwright</artifactId>   <!-- or healer-selenium -->
  <version>2.2.0</version>
</dependency>
```

---

## Profile "Featured" description

Self-healing locator framework - an open-source Java library for Playwright and Selenium tests. Finds the element
again when the UI changes, keeps the test running, reports the fix. On Maven Central.
