import { LANGUAGES } from "../i18n/index.js";
import { useApp } from "../store.jsx";

export default function LanguageSelect() {
  const { lang, setLang, t } = useApp();
  return (
    <select
      value={lang}
      onChange={e => setLang(e.target.value)}
      id="language-select"
      name="language"
      className="form-select select-language"
      data-testid="language-select"
      data-qa="language-switcher"
      aria-label={t("lang.label")}
      title={t("lang.label")}
    >
      {LANGUAGES.map(l => (
        <option key={l.code} value={l.code}>{l.label}</option>
      ))}
    </select>
  );
}
