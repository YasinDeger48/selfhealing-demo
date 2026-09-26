"""ShopLab attribute mutator - breaks test locators on purpose (e.g. for self-healing demos).

Usage:
    python mutate.py --level low|medium|high|extreme   # apply mutations (levels are cumulative)
    python mutate.py --level removed                   # negative test: delete elements (must NOT be healed)
    python mutate.py --reset                           # restore the original site
    python mutate.py --list                            # show every mutation without applying
    python mutate.py --rebaseline                      # accept current files as the new original
    --force                                            # discard manual edits when restoring

Attributes (id, data-testid, class ...) live in the React components under src/; visible text,
aria-labels, titles and placeholders live in the translation files. Text mutations change the
English file (src/i18n/en.js) - English is the default language, so that is what tests see.
With `npm run dev` running, Vite hot-reloads every change into the browser immediately.

Every run starts from the pristine copy in .original/, so runs are repeatable.
The applied mutations are written to mutations-applied.json.
"""

import argparse
import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
BACKUP = ROOT / ".original"
LOG_FILE = ROOT / "mutations-applied.json"
LEVELS = ["low", "medium", "high", "extreme"]
ALL = "*"
EN = "i18n/en.js"

# (level, file under src/, description, old, new)
# - Literal replacements, applied to every occurrence.
# - When `old` starts with a letter, it only matches at an attribute/word start
#   (id="x" never matches inside data-testid="x").
# - Mutations run in list order, so later entries see the result of earlier ones.
MUTATIONS = [
    # ---------------- low: id / data-testid renames ----------------
    ("low", "pages/Login.jsx", "Login username: id renamed",
     'id="login-username"', 'id="user-name"'),
    ("low", "pages/Login.jsx", "Login username: label htmlFor follows id",
     'htmlFor="login-username"', 'htmlFor="user-name"'),
    ("low", "pages/Login.jsx", "Login username: data-testid renamed",
     'data-testid="login-username-input"', 'data-testid="username-input"'),
    ("low", "pages/Login.jsx", "Login button: id renamed",
     'id="login-button"', 'id="btn-signin"'),
    ("low", "pages/Login.jsx", "Login button: data-testid renamed",
     'data-testid="login-submit-button"', 'data-testid="signin-button"'),
    ("low", "pages/Products.jsx", "Search box: id renamed",
     'id="product-search"', 'id="search-input"'),
    ("low", "pages/Products.jsx", "Search box: data-testid renamed",
     'data-testid="product-search-input"', 'data-testid="search-box"'),
    ("low", "components/ProductCard.jsx", "Add-to-cart buttons: id prefix renamed",
     'id={`add-to-cart-${p.id}`}', 'id={`btn-add-${p.id}`}'),
    ("low", "components/ProductCard.jsx", "Add-to-cart buttons: data-testid prefix renamed",
     'data-testid={`add-to-cart-${p.id}`}', 'data-testid={`product-add-btn-${p.id}`}'),
    ("low", "components/Header.jsx", "Header cart badge: id renamed",
     'id="cart-count"', 'id="basket-count"'),
    ("low", "components/Header.jsx", "Header cart badge: data-testid renamed",
     'data-testid="cart-count-badge"', 'data-testid="basket-badge"'),
    ("low", "pages/Cart.jsx", "Place order button: id renamed",
     'id="place-order"', 'id="submit-order"'),
    ("low", "pages/Cart.jsx", "Place order button: data-testid renamed",
     'data-testid="place-order-button"', 'data-testid="complete-order-button"'),
    ("low", "pages/Contact.jsx", "Contact email: id renamed",
     'id="contact-email"', 'id="email-address"'),
    ("low", "pages/Contact.jsx", "Contact email: label htmlFor follows id",
     'htmlFor="contact-email"', 'htmlFor="email-address"'),
    ("low", "pages/Contact.jsx", "Contact email: data-testid renamed",
     'data-testid="contact-email-input"', 'data-testid="email-field"'),

    # ---------------- medium: class / name / data-qa / visible text ----------------
    ("medium", "pages/Login.jsx", "Login password: class changed",
     'className="form-input input-password"', 'className="form-control pwd-field"'),
    ("medium", "pages/Login.jsx", "Login password: name changed",
     'name="password"', 'name="pass"'),
    ("medium", "pages/Login.jsx", "Login password: data-qa changed",
     'data-qa="password-field"', 'data-qa="pwd"'),
    ("medium", EN, "Login button: text changed",
     '"login.submit": "Sign In"', '"login.submit": "Log In"'),
    ("medium", EN, "Login button: aria-label changed",
     '"login.submitAria": "Sign in"', '"login.submitAria": "Log in"'),
    ("medium", "components/ProductCard.jsx", "Add-to-cart buttons: class changed",
     'className="btn btn-primary btn-add-cart"', 'className="btn btn-primary js-cart-add"'),
    ("medium", EN, "Add-to-cart buttons: text changed",
     '"products.addToCart": "Add to Cart"', '"products.addToCart": "Add to Bag"'),
    ("medium", "pages/Products.jsx", "Category filter: name changed",
     'name="category"', 'name="cat"'),
    ("medium", "pages/Products.jsx", "Category filter: class changed",
     'className="form-select select-category"', 'className="form-select filter-cat"'),
    ("medium", "pages/Products.jsx", "Category filter: data-testid changed",
     'data-testid="category-filter-select"', 'data-testid="filter-category"'),
    ("medium", "pages/ProductDetail.jsx", "Size select: id changed",
     'id="size-select"', 'id="variant-size"'),
    ("medium", "pages/ProductDetail.jsx", "Size select: label htmlFor follows id",
     'htmlFor="size-select"', 'htmlFor="variant-size"'),
    ("medium", "pages/ProductDetail.jsx", "Size select: data-testid changed",
     'data-testid="size-select"', 'data-testid="variant-size-dropdown"'),
    ("medium", EN, "Detail add-to-cart: text changed",
     '"detail.add": "Add to Cart"', '"detail.add": "Add to Bag"'),
    ("medium", "pages/Cart.jsx", "Coupon input: id changed",
     'id="coupon-code"', 'id="promo-code"'),
    ("medium", "pages/Cart.jsx", "Coupon input: data-testid changed",
     'data-testid="coupon-code-input"', 'data-testid="promo-input"'),
    ("medium", EN, "Place order button: text changed",
     '"order.place": "Place Order"', '"order.place": "Checkout"'),
    ("medium", "pages/Contact.jsx", "Contact submit: data-qa changed",
     'data-qa="send-message"', 'data-qa="submit"'),
    ("medium", EN, "Contact submit: text changed",
     '"contact.send": "Send"', '"contact.send": "Send Message"'),

    # ---------------- high: structural changes / stripped attributes ----------------
    ("high", "pages/Login.jsx", "Login username: data-qa stripped",
     '\n              data-qa="username-field"', ''),
    ("high", EN, "Login username: placeholder changed",
     '"login.usernamePlaceholder": "Enter your username"', '"login.usernamePlaceholder": "Email or username"'),
    ("high", "pages/Login.jsx", "Login button: wrapped in a new container div",
     '<button\n            type="submit"\n            id="btn-signin"',
     '<div className="submit-wrapper">\n          <button\n            type="submit"\n            id="btn-signin"'),
    ("high", "pages/Login.jsx", "Login button: wrapper closed",
     '{t("login.submit")}\n          </button>', '{t("login.submit")}\n          </button>\n          </div>'),
    ("high", "pages/Products.jsx", "Search box: data-qa changed",
     'data-qa="search-field"', 'data-qa="global-search"'),
    ("high", EN, "Search box: placeholder changed",
     '"products.search": "Search products..."', '"products.search": "What are you looking for?"'),
    ("high", "pages/Contact.jsx", "Contact submit: tag changed button -> a",
     '<button\n                type="submit"\n                id="contact-submit"',
     '<a\n                href="#"\n                role="button"\n                onClick={handleSubmit}\n                id="contact-submit"'),
    ("high", "pages/Contact.jsx", "Contact submit: closing tag changed",
     '{t("contact.send")}\n              </button>', '{t("contact.send")}\n              </a>'),
    ("high", "components/Header.jsx", "Logout: button re-tagged as link",
     '<button\n            type="button"\n            onClick={handleLogout}',
     '<a\n            href="#"\n            role="button"\n            onClick={handleLogout}'),
    ("high", "components/Header.jsx", "Logout: closing tag changed",
     '{t("nav.logout")}\n          </button>', '{t("nav.logout")}\n          </a>'),
    ("high", EN, "Logout: text changed",
     '"nav.logout": "Logout"', '"nav.logout": "Sign Out"'),

    # ---------------- extreme: every identifier renamed to a synonym ----------------
    # String similarity cannot link these (Password/Passphrase, Apply/Redeem, Place Order/Buy Now);
    # healing them needs an understanding of meaning - this level exercises the LLM stage.
    ("extreme", "pages/Login.jsx", "Login password: label htmlFor changed",
     'htmlFor="login-password"', 'htmlFor="credential"'),
    ("extreme", "pages/Login.jsx", "Login password: id changed",
     'id="login-password"', 'id="credential"'),
    ("extreme", "pages/Login.jsx", "Login password: data-testid changed",
     'data-testid="login-password-input"', 'data-testid="secret-input"'),
    ("extreme", "pages/Login.jsx", "Login password: class changed",
     'className="form-control pwd-field"', 'className="form-control secret-field"'),
    ("extreme", "pages/Login.jsx", "Login password: data-qa changed",
     'data-qa="pwd"', 'data-qa="secret"'),
    ("extreme", EN, "Login password: label / aria-label / title changed",
     '"login.password": "Password"', '"login.password": "Passphrase"'),
    ("extreme", EN, "Login password: placeholder changed",
     '"login.passwordPlaceholder": "Enter your password"', '"login.passwordPlaceholder": "Type your passphrase"'),
    ("extreme", "pages/Cart.jsx", "Coupon button: id changed",
     'id="apply-coupon"', 'id="redeem-btn"'),
    ("extreme", "pages/Cart.jsx", "Coupon button: name changed",
     'name="applyCoupon"', 'name="redeem"'),
    ("extreme", "pages/Cart.jsx", "Coupon button: class changed",
     'className="btn btn-secondary btn-coupon"', 'className="btn btn-secondary btn-redeem"'),
    ("extreme", "pages/Cart.jsx", "Coupon button: data-testid changed",
     'data-testid="apply-coupon-button"', 'data-testid="redeem-code"'),
    ("extreme", "pages/Cart.jsx", "Coupon button: data-qa changed",
     'data-qa="apply-coupon"', 'data-qa="redeem"'),
    ("extreme", EN, "Coupon button: aria-label changed",
     '"coupon.applyAria": "Apply coupon"', '"coupon.applyAria": "Redeem code"'),
    ("extreme", EN, "Coupon button: text / title changed",
     '"coupon.apply": "Apply"', '"coupon.apply": "Redeem"'),
    ("extreme", "pages/Cart.jsx", "Place order button: id changed",
     'id="submit-order"', 'id="btn-checkout-final"'),
    ("extreme", "pages/Cart.jsx", "Place order button: name changed",
     'name="placeOrder"', 'name="purchase"'),
    ("extreme", "pages/Cart.jsx", "Place order button: class changed",
     'className="btn btn-primary btn-place-order"', 'className="btn btn-primary cta-purchase"'),
    ("extreme", "pages/Cart.jsx", "Place order button: data-testid changed",
     'data-testid="complete-order-button"', 'data-testid="purchase-cta"'),
    ("extreme", "pages/Cart.jsx", "Place order button: data-qa changed",
     'data-qa="place-order"', 'data-qa="buy-now"'),
    ("extreme", EN, "Place order button: aria-label / title changed",
     '"order.placeAria": "Place order"', '"order.placeAria": "Buy now"'),
    ("extreme", EN, "Place order button: text changed",
     '"order.place": "Checkout"', '"order.place": "Buy Now"'),
    ("extreme", "components/Header.jsx", "Cart badge: id changed",
     'id="basket-count"', 'id="hdr-qty"'),
    ("extreme", "components/Header.jsx", "Cart badge: class changed",
     'className="cart-badge"', 'className="pill-counter"'),
    ("extreme", "components/Header.jsx", "Cart badge: data-testid changed",
     'data-testid="basket-badge"', 'data-testid="header-items"'),
    ("extreme", "components/Header.jsx", "Cart badge: data-qa changed",
     'data-qa="cart-badge"', 'data-qa="items-qty"'),
    ("extreme", EN, "Cart badge: aria-label changed",
     '"nav.badgeAria": "Items in cart"', '"nav.badgeAria": "Basket quantity"'),
]


# Negative scenario (not cumulative): elements are REMOVED, not renamed. A healer must NOT "heal"
# these - the right outcome is a failing step. Includes a look-alike trap: only product 8 loses its
# add-to-cart button while seven identical buttons remain on the page.
REMOVALS = [
    ("removed", "components/ProductCard.jsx", "Add-to-cart button removed from product 8 only (look-alike trap)",
     '          <button\n            type="button"\n            onClick={() => onAddToCart(p)}',
     '          {p.id !== 8 && <button\n            type="button"\n            onClick={() => onAddToCart(p)}'),
    ("removed", "components/ProductCard.jsx", "Add-to-cart button: conditional closed",
     '{t("products.addToCart")}\n          </button>', '{t("products.addToCart")}\n          </button>}'),
    ("removed", "pages/Cart.jsx", "Coupon apply button removed",
     '<button\n              type="button"\n              onClick={applyCoupon}',
     '{false && <button\n              type="button"\n              onClick={applyCoupon}'),
    ("removed", "pages/Cart.jsx", "Coupon apply button: conditional closed",
     '{t("coupon.apply")}\n            </button>', '{t("coupon.apply")}\n            </button>}'),
    ("removed", "components/Header.jsx", "Header cart badge removed",
     '<span\n              id="cart-count"', '{false && <span\n              id="cart-count"'),
    ("removed", "components/Header.jsx", "Header cart badge: conditional closed",
     '{cartCount}\n            </span>', '{cartCount}\n            </span>}'),
    ("removed", "pages/Products.jsx", "Product search box removed",
     '<input\n            type="search"', '{false && <input\n            type="search"'),
    ("removed", "pages/Products.jsx", "Product search box: conditional closed",
     'title={t("products.searchAria")}\n          />', 'title={t("products.searchAria")}\n          />}'),
]
SCENARIOS = LEVELS + ["removed"]


def site_files():
    """Files (relative to src/) that mutations and backups cover: components and translations."""
    base = BACKUP if BACKUP.exists() else SRC
    files = list(base.rglob("*.jsx")) + list((base / "i18n").glob("*.js"))
    return sorted(p.relative_to(base).as_posix() for p in files)


def pattern_for(old):
    escaped = re.escape(old)
    if re.match(r"[^\W\d_]", old):
        escaped = r"(?<![\w-])" + escaped
    return re.compile(escaped)


def ensure_backup():
    if BACKUP.exists():
        return
    for rel in site_files():
        target = BACKUP / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(SRC / rel, target)
    print(f"Original sources backed up to {BACKUP.name}/")


def manual_edits():
    """Files that differ from the backup although mutate.py did not change them (hand edits)."""
    if not BACKUP.exists() or LOG_FILE.exists():
        return []
    return [rel for rel in site_files()
            if (SRC / rel).read_bytes() != (BACKUP / rel).read_bytes()]


def restore(force=False):
    if not BACKUP.exists():
        return
    edited = manual_edits()
    if edited and not force:
        sys.exit("ERROR: these files have manual edits that would be overwritten: "
                 + ", ".join(edited) + "\n  Re-run with --force to discard them.")
    expected = {}
    for rel in site_files():
        src_file = SRC / rel
        if src_file.read_bytes() != (BACKUP / rel).read_bytes():
            shutil.copy2(BACKUP / rel, src_file)  # copy only changed files to keep HMR quiet
            original = (BACKUP / rel).read_text(encoding="utf-8")
            expected[rel] = [t for m in MUTATIONS + REMOVALS if m[1] == rel for t in tokens_for(m[3]) if t in original]
    wait_until_served(expected)


def apply(level, force=False):
    ensure_backup()
    edited = manual_edits()
    if edited and not force:
        sys.exit("ERROR: these files have manual edits that would be overwritten: "
                 + ", ".join(edited) + "\n  Re-run with --force to discard them.")
    if level == "removed":
        mutations = REMOVALS
    else:
        active = LEVELS[: LEVELS.index(level) + 1]
        mutations = [m for m in MUTATIONS if m[0] in active]
    files = site_files()
    # Start from the pristine copy and write every file at most once, in its final state: a restore
    # followed by a quick second write can be missed by file watchers (Vite hot reload on OneDrive).
    contents = {rel: (BACKUP / rel).read_text(encoding="utf-8") for rel in files}
    applied = []

    for lvl, target, desc, old, new in mutations:
        targets = files if target == ALL else [target]
        pattern = pattern_for(old)
        hits = 0
        for rel in targets:
            contents[rel], n = pattern.subn(lambda _m: new, contents[rel])
            hits += n
        if hits == 0:
            sys.exit(f"ERROR: mutation did not match anything: [{lvl}] {target} - {desc}\n  old: {old!r}")
        applied.append({"level": lvl, "file": "src/" + target, "description": desc,
                        "old": old, "new": new, "occurrences": hits})

    expected = {}
    for rel, text in contents.items():
        if (SRC / rel).read_text(encoding="utf-8") != text:
            (SRC / rel).write_text(text, encoding="utf-8")
            expected[rel] = [t for m in mutations if m[1] == rel for t in tokens_for(m[4]) if t in text]
    wait_until_served(expected)
    LOG_FILE.write_text(json.dumps({"level": level, "mutations": applied}, ensure_ascii=False, indent=2),
                        encoding="utf-8")

    print(f"Applied {len(applied)} mutations (level: {level}). Details: {LOG_FILE.name}")
    for m in applied:
        print(f"  [{m['level']:<7}] {m['file']:<30} {m['description']} ({m['occurrences']}x)")


DEV_SERVER = "http://localhost:8080"


def served(rel):
    """The dev server's current version of src/<rel>, or None when no dev server is running."""
    import time
    import urllib.request
    try:
        with urllib.request.urlopen(f"{DEV_SERVER}/src/{rel}?t={int(time.time() * 1000)}", timeout=3) as r:
            return r.read().decode("utf-8", "replace")
    except Exception:
        return None


def tokens_for(text):
    """Distinctive strings of a mutation that survive Vite's JSX transform (quoted values, conditions)."""
    found = re.findall(r'"([^"\n]{3,})"', text)
    found += [t for t in ("false &&", "p.id !== 8") if t in text]
    return found


def wait_until_served(expected):
    """
    File watchers on synced folders (OneDrive) can miss a change, and the browser would keep getting the
    old page. Wait until the dev server serves every changed file with its expected content; if it does not,
    rewrite the file to trigger the watcher again. No-op when the dev server is not running.
    """
    import time
    for rel, tokens in expected.items():
        if not tokens:
            continue
        for attempt in range(3):
            deadline = time.time() + 5
            ok = False
            while time.time() < deadline:
                body = served(rel)
                if body is None:
                    return
                if all(t in body for t in tokens):
                    ok = True
                    break
                time.sleep(0.3)
            if ok:
                break
            path = SRC / rel
            path.write_text(path.read_text(encoding="utf-8"), encoding="utf-8")   # touch again
        else:
            print(f"WARNING: the dev server still serves an old src/{rel} - restart `npm run dev`")


def main():
    parser = argparse.ArgumentParser(description="Break ShopLab locators on purpose.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--level", choices=SCENARIOS,
                       help="apply mutations up to this level; 'removed' deletes elements instead (negative test)")
    group.add_argument("--reset", action="store_true", help="restore the original site")
    group.add_argument("--list", action="store_true", help="list mutations without applying")
    group.add_argument("--rebaseline", action="store_true",
                       help="accept the current files as the new original (after permanent site changes)")
    parser.add_argument("--force", action="store_true", help="discard manual edits when restoring")
    args = parser.parse_args()

    if args.rebaseline:
        if LOG_FILE.exists():
            sys.exit("ERROR: site is mutated. Run --reset first, then make your changes and --rebaseline.")
        shutil.rmtree(BACKUP, ignore_errors=True)
        ensure_backup()
    elif args.list:
        for lvl, target, desc, old, new in MUTATIONS + REMOVALS:
            print(f"[{lvl:<7}] {target:<28} {desc}\n            {old!r} -> {new!r}")
    elif args.reset:
        if not BACKUP.exists():
            print("Nothing to reset - site is already original.")
            return
        restore(args.force)
        LOG_FILE.unlink(missing_ok=True)
        print("Site restored to original.")
    else:
        apply(args.level, args.force)


if __name__ == "__main__":
    main()
