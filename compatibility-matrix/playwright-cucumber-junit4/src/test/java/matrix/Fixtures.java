package matrix;

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
