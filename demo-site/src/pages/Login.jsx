import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useApp } from "../store.jsx";
import LanguageSelect from "../components/LanguageSelect.jsx";

export default function Login() {
  const { login, showToast, t } = useApp();
  const navigate = useNavigate();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [remember, setRemember] = useState(false);
  const [error, setError] = useState("");

  function handleSubmit(e) {
    e.preventDefault();
    const result = login(username.trim(), password);
    if (result.ok) navigate("/products");
    else setError(result.error);
  }

  function handleForgot(e) {
    e.preventDefault();
    showToast(t("toast.resetSent"));
  }

  return (
    <main className="login-wrapper">
      <div className="login-lang">
        <LanguageSelect />
      </div>
      <div className="card login-card" id="login-card" data-testid="login-card" data-qa="login-container">
        <span className="brand">Shop<span>Lab</span></span>
        <p className="login-subtitle">{t("login.subtitle")}</p>

        <div
          id="login-error"
          className={"alert alert-error" + (error ? " visible" : "")}
          role="alert"
          data-testid="login-error-message"
          data-qa="login-error"
          aria-live="assertive"
        >
          {error && t(error)}
        </div>

        <form onSubmit={handleSubmit} id="login-form" name="loginForm" data-testid="login-form" data-qa="login-form" noValidate>
          <div className="form-group">
            <label className="form-label" htmlFor="login-username">{t("login.username")}</label>
            <input
              type="text"
              value={username}
              onChange={e => setUsername(e.target.value)}
              id="login-username"
              name="username"
              className="form-input input-username"
              data-testid="login-username-input"
              data-qa="username-field"
              aria-label={t("login.username")}
              placeholder={t("login.usernamePlaceholder")}
              title={t("login.username")}
              autoComplete="username"
            />
          </div>

          <div className="form-group">
            <label className="form-label" htmlFor="login-password">{t("login.password")}</label>
            <input
              type="password"
              value={password}
              onChange={e => setPassword(e.target.value)}
              id="login-password"
              name="password"
              className="form-input input-password"
              data-testid="login-password-input"
              data-qa="password-field"
              aria-label={t("login.password")}
              placeholder={t("login.passwordPlaceholder")}
              title={t("login.password")}
              autoComplete="current-password"
            />
          </div>

          <div className="login-footer">
            <label className="form-check" htmlFor="remember-me">
              <input
                type="checkbox"
                checked={remember}
                onChange={e => setRemember(e.target.checked)}
                id="remember-me"
                name="rememberMe"
                className="checkbox-remember"
                data-testid="login-remember-checkbox"
                data-qa="remember-me"
                aria-label={t("login.remember")}
                title={t("login.remember")}
              />
              {t("login.remember")}
            </label>
            <a
              href="#"
              onClick={handleForgot}
              id="forgot-password-link"
              className="link-forgot"
              data-testid="login-forgot-password-link"
              data-qa="forgot-password"
              aria-label={t("login.forgot")}
              title={t("login.forgot")}
            >
              {t("login.forgot")}
            </a>
          </div>

          <button
            type="submit"
            id="login-button"
            name="loginButton"
            className="btn btn-primary btn-block btn-login"
            data-testid="login-submit-button"
            data-qa="login-button"
            aria-label={t("login.submitAria")}
            title={t("login.submitAria")}
          >
            {t("login.submit")}
          </button>
        </form>

        <p className="demo-hint" id="demo-hint" data-testid="login-demo-hint">
          {t("login.demoHint")} <code>standard_user</code> / <code>secret123</code>
        </p>
      </div>
    </main>
  );
}
