package com.tripforge.cucumber;

import com.microsoft.playwright.Page;
import com.selfhealing.healer.playwright.SelfHealingPage;

/** State shared by the hooks and the step definitions of one scenario (Cucumber creates one per scenario). */
public class World {
    public Page page;
    public SelfHealingPage healer;
}
