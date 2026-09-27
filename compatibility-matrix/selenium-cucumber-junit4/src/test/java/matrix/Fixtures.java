package matrix;

/** Bundled test pages and a framework-neutral assertion (works under every runner). */
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

    /** Fails only when the run is started with -Dmatrix.fail=true. */
    public static void failWhenAsked() {
        check(!Boolean.getBoolean("matrix.fail"), "deliberate failure (-Dmatrix.fail=true)");
    }
}
