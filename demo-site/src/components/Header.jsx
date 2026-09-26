import { Link, NavLink, useNavigate } from "react-router-dom";
import { useApp } from "../store.jsx";
import LanguageSelect from "./LanguageSelect.jsx";

const navClass = ({ isActive }) => "nav-link" + (isActive ? " active" : "");

export default function Header() {
  const { user, cartCount, logout, t } = useApp();
  const navigate = useNavigate();

  function handleLogout(e) {
    e.preventDefault();
    logout();
    navigate("/login");
  }

  return (
    <header className="site-header" id="site-header" data-testid="site-header" data-qa="header">
      <div className="header-inner">
        <Link
          to="/products"
          className="brand"
          id="brand-logo"
          data-testid="header-logo"
          data-qa="logo"
          aria-label={t("nav.homeAria")}
          title="ShopLab"
        >
          Shop<span>Lab</span>
        </Link>

        <nav className="main-nav" id="main-nav" role="navigation" aria-label={t("nav.menuAria")} data-testid="main-nav" data-qa="main-navigation">
          <NavLink
            to="/products"
            id="nav-products"
            className={navClass}
            data-testid="nav-products-link"
            data-qa="nav-products"
            aria-label={t("nav.products")}
            title={t("nav.products")}
          >
            {t("nav.products")}
          </NavLink>
          <NavLink
            to="/cart"
            id="nav-cart"
            className={navClass}
            data-testid="nav-cart-link"
            data-qa="nav-cart"
            aria-label={t("nav.cart")}
            title={t("nav.cart")}
          >
            {t("nav.cart")}{" "}
            <span
              id="cart-count"
              className="cart-badge"
              data-testid="cart-count-badge"
              data-qa="cart-badge"
              aria-label={t("nav.badgeAria")}
            >
              {cartCount}
            </span>
          </NavLink>
          <NavLink
            to="/contact"
            id="nav-contact"
            className={navClass}
            data-testid="nav-contact-link"
            data-qa="nav-contact"
            aria-label={t("nav.contact")}
            title={t("nav.contact")}
          >
            {t("nav.contact")}
          </NavLink>
        </nav>

        <div className="user-area" data-testid="header-user-area">
          <LanguageSelect />
          <span id="header-username" className="username-label" data-testid="header-username" data-qa="current-user" title={user?.email}>
            {user?.displayName}
            <small id="header-user-email" className="user-email" data-testid="header-user-email">{user?.email}</small>
          </span>
          <button
            type="button"
            onClick={handleLogout}
            id="logout-button"
            name="logout"
            className="btn btn-secondary btn-logout"
            data-testid="logout-button"
            data-qa="logout"
            aria-label={t("nav.logoutAria")}
            title={t("nav.logoutAria")}
          >
            {t("nav.logout")}
          </button>
        </div>
      </div>
    </header>
  );
}
