export const PRODUCTS = [
  { id: 1, name: "Wireless Headphones", category: "electronics", price: 1299, emoji: "🎧",
    description: "Over-ear bluetooth headphones with active noise cancelling and 30 hours of battery life." },
  { id: 2, name: "Smart Watch", category: "electronics", price: 2499, emoji: "⌚",
    description: "Fitness tracking, heart-rate monitor and notifications on your wrist." },
  { id: 3, name: "Mechanical Keyboard", category: "electronics", price: 1899, emoji: "⌨️",
    description: "Hot-swappable mechanical keyboard with RGB backlight." },
  { id: 4, name: "Running Shoes", category: "sports", price: 1599, emoji: "👟",
    description: "Lightweight running shoes with breathable mesh and cushioned sole." },
  { id: 5, name: "Yoga Mat", category: "sports", price: 449, emoji: "🧘",
    description: "Non-slip 6mm yoga mat with carrying strap." },
  { id: 6, name: "Cotton T-Shirt", category: "clothing", price: 299, emoji: "👕",
    description: "100% organic cotton t-shirt, regular fit." },
  { id: 7, name: "Denim Jacket", category: "clothing", price: 1199, emoji: "🧥",
    description: "Classic denim jacket with a modern cut." },
  { id: 8, name: "Coffee Mug", category: "home", price: 149, emoji: "☕",
    description: "Ceramic mug, 350 ml, dishwasher safe." }
];

export const DEMO_USERS = {
  standard_user: { password: "secret123", displayName: "Standard User", email: "jane.doe@shoplab.test" },
  locked_user: { password: "secret123", displayName: "Locked User", email: "locked@shoplab.test", locked: true }
};

export const COUPONS = { SAVE10: 0.10, WELCOME20: 0.20 };

export function findProduct(id) {
  return PRODUCTS.find(p => p.id === Number(id));
}

/** Prices are in Turkish lira; the number format follows the selected language. */
export function formatPrice(value, locale = "en-US") {
  return new Intl.NumberFormat(locale, { style: "currency", currency: "TRY", currencyDisplay: "narrowSymbol" }).format(value);
}
