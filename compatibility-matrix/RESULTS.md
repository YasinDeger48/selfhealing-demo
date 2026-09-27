# Compatibility results

| Combination | Build | Surefire provider | Tests run | Report tests | Heals | TripForge heals | ShopLab heals | Found by description | Steps | Threads | Video/trace of failed tests | Result | Failing test fails the build |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|
| playwright-cucumber-junit4 | OK | JUnitPlatformProvider | 10 | 10 | 3 | 9 | 14 | 1 | 61 | - | 1/1 | OK | OK |
| playwright-cucumber-junit5 | OK | JUnitPlatformProvider | 10 | 10 | 3 | 9 | 14 | 1 | 61 | - | 1/1 | OK | OK |
| playwright-cucumber-junit5-parallel | OK | JUnitPlatformProvider | 20 | 20 | 6 | 18 | 28 | 1 | 122 | 3 | 2/2 | OK | OK |
| playwright-cucumber-testng | OK | JUnitPlatformProvider | 10 | 10 | 3 | 9 | 14 | 1 | 61 | - | 1/1 | OK | OK |
| playwright-cucumber-testng-parallel | OK | JUnitPlatformProvider | 20 | 20 | 6 | 18 | 28 | 1 | 122 | 3 | 2/2 | OK | OK |
| playwright-junit4 | OK | JUnitPlatformProvider | 10 | 10 | 2 | 9 | 14 | 1 | 39 | - | 1/1 | OK | OK |
| playwright-junit5 | OK | JUnitPlatformProvider | 10 | 10 | 2 | 9 | 14 | 1 | 39 | - | 1/1 | OK | OK |
| playwright-junit5-parallel | OK | JUnitPlatformProvider | 20 | 20 | 4 | 18 | 28 | 2 | 78 | 3 | 2/2 | OK | OK |
| playwright-junit5-pw1.45 | OK | JUnitPlatformProvider | 10 | 10 | 2 | 9 | 14 | 1 | 39 | - | 1/1 | OK | OK |
| playwright-testng | OK | JUnitPlatformProvider | 10 | 10 | 2 | 9 | 14 | 1 | 39 | - | 1/1 | OK | OK |
| playwright-testng-parallel | OK | JUnitPlatformProvider | 20 | 20 | 4 | 18 | 28 | 1 | 78 | 3 | 2/2 | OK | OK |
| selenium-cucumber-junit4 | OK | JUnitPlatformProvider | 10 | 10 | 3 | 9 | 14 | 1 | 64 | - | - | OK | OK |
| selenium-cucumber-junit5 | OK | JUnitPlatformProvider | 10 | 10 | 3 | 9 | 14 | 1 | 64 | - | - | OK | OK |
| selenium-cucumber-testng | OK | JUnitPlatformProvider | 10 | 10 | 3 | 9 | 14 | 1 | 64 | - | - | OK | OK |
| selenium-junit4 | OK | JUnitPlatformProvider | 10 | 10 | 2 | 9 | 14 | 1 | 42 | - | - | OK | OK |
| selenium-junit5 | OK | JUnitPlatformProvider | 10 | 10 | 2 | 9 | 14 | 1 | 42 | - | - | OK | OK |
| selenium-junit5-parallel | OK | JUnitPlatformProvider | 20 | 20 | 4 | 18 | 28 | 1 | 84 | 3 | - | OK | OK |
| selenium-junit5-se4.21 | OK | JUnitPlatformProvider | 10 | 10 | 2 | 9 | 14 | 1 | 42 | - | - | OK | OK |
| selenium-testng | OK | JUnitPlatformProvider | 10 | 10 | 2 | 9 | 14 | 1 | 42 | - | - | OK | OK |
| selenium-testng-parallel | OK | JUnitPlatformProvider | 20 | 20 | 4 | 18 | 28 | 1 | 84 | 3 | - | OK | OK |
