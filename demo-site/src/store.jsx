/* App state: auth, cart and toast. Persisted in localStorage - there is no backend. */
import { createContext, useCallback, useContext, useEffect, useRef, useState } from "react";
import { DEMO_USERS } from "./data.js";
import { DEFAULT_LANGUAGE, language, translate } from "./i18n/index.js";

const STORAGE = { user: "shoplab_user", cart: "shoplab_cart", lang: "shoplab_lang" };
const AppContext = createContext(null);

function readJson(key, fallback) {
  try {
    const raw = localStorage.getItem(key);
    return raw ? JSON.parse(raw) : fallback;
  } catch {
    return fallback;
  }
}

export function AppProvider({ children }) {
  const [user, setUser] = useState(() => readJson(STORAGE.user, null));
  const [cart, setCart] = useState(() => readJson(STORAGE.cart, []));
  const [toast, setToast] = useState({ message: "", visible: false });
  const [lang, setLang] = useState(() => {
    try {
      return localStorage.getItem(STORAGE.lang) || DEFAULT_LANGUAGE;
    } catch {
      return DEFAULT_LANGUAGE;
    }
  });
  const toastTimer = useRef(null);

  useEffect(() => {
    if (user) localStorage.setItem(STORAGE.user, JSON.stringify(user));
    else localStorage.removeItem(STORAGE.user);
  }, [user]);

  useEffect(() => {
    localStorage.setItem(STORAGE.cart, JSON.stringify(cart));
  }, [cart]);

  useEffect(() => {
    localStorage.setItem(STORAGE.lang, lang);
    document.documentElement.lang = lang;
    document.documentElement.dir = language(lang).dir;
  }, [lang]);

  const t = useCallback((key, params) => translate(lang, key, params), [lang]);
  const locale = language(lang).locale;

  const login = useCallback((username, password) => {
    const account = DEMO_USERS[username];
    if (!username || !password) return { ok: false, error: "login.errRequired" };
    if (!account || account.password !== password) return { ok: false, error: "login.errInvalid" };
    if (account.locked) return { ok: false, error: "login.errLocked" };
    setUser({ username, displayName: account.displayName, email: account.email });
    return { ok: true };
  }, []);

  const logout = useCallback(() => {
    setUser(null);
    setCart([]);
  }, []);

  const addToCart = useCallback((productId, qty = 1, color = null, size = null) => {
    setCart(prev => {
      const index = prev.findIndex(i => i.id === productId && i.color === color && i.size === size);
      if (index === -1) return [...prev, { id: productId, qty, color, size }];
      return prev.map((item, i) => (i === index ? { ...item, qty: item.qty + qty } : item));
    });
  }, []);

  const updateQty = useCallback((index, qty) => {
    setCart(prev => prev.map((item, i) => (i === index ? { ...item, qty } : item)));
  }, []);

  const removeItem = useCallback(index => {
    setCart(prev => prev.filter((_, i) => i !== index));
  }, []);

  const clearCart = useCallback(() => setCart([]), []);

  const showToast = useCallback(message => {
    setToast({ message, visible: true });
    clearTimeout(toastTimer.current);
    toastTimer.current = setTimeout(() => setToast(t => ({ ...t, visible: false })), 2500);
  }, []);

  const cartCount = cart.reduce((sum, i) => sum + i.qty, 0);

  return (
    <AppContext.Provider value={{ user, login, logout, cart, cartCount, addToCart, updateQty,
                                  removeItem, clearCart, toast, showToast, lang, setLang, t, locale }}>
      {children}
    </AppContext.Provider>
  );
}

export function useApp() {
  return useContext(AppContext);
}
