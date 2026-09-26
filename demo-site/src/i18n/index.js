import en from "./en.js";
import de from "./de.js";
import ru from "./ru.js";
import ja from "./ja.js";
import tr from "./tr.js";
import ar from "./ar.js";

/** Supported languages; English is the default. `locale` drives number/currency formatting. */
export const LANGUAGES = [
  { code: "en", label: "English", locale: "en-US", dir: "ltr" },
  { code: "de", label: "Deutsch", locale: "de-DE", dir: "ltr" },
  { code: "ru", label: "Русский", locale: "ru-RU", dir: "ltr" },
  { code: "ja", label: "日本語", locale: "ja-JP", dir: "ltr" },
  { code: "tr", label: "Türkçe", locale: "tr-TR", dir: "ltr" },
  { code: "ar", label: "العربية", locale: "ar", dir: "rtl" }
];

export const DEFAULT_LANGUAGE = "en";

const DICTIONARIES = { en, de, ru, ja, tr, ar };

export function language(code) {
  return LANGUAGES.find(l => l.code === code) || LANGUAGES[0];
}

/** Translates a key, filling {placeholders}; falls back to English, then to the key itself. */
export function translate(code, key, params) {
  const text = (DICTIONARIES[code] && DICTIONARIES[code][key]) ?? en[key] ?? key;
  if (!params) return text;
  return text.replace(/\{(\w+)\}/g, (m, name) => (params[name] ?? m));
}
