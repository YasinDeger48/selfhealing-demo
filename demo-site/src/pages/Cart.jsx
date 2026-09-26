import { useState } from "react";
import { Link } from "react-router-dom";
import { COUPONS, findProduct, formatPrice } from "../data.js";
import { useApp } from "../store.jsx";

const EMPTY_FORM = { firstName: "", lastName: "", address: "", city: "", postalCode: "", acceptTerms: false };

export default function Cart() {
  const { cart, updateQty, removeItem, clearCart, showToast, t, locale } = useApp();
  const [coupon, setCoupon] = useState("");
  const [discountRate, setDiscountRate] = useState(0);
  const [couponMessage, setCouponMessage] = useState(null);
  const [pendingRemove, setPendingRemove] = useState(null);
  const [form, setForm] = useState(EMPTY_FORM);
  const [errors, setErrors] = useState([]);
  const [orderNumber, setOrderNumber] = useState(null);

  const subtotal = cart.reduce((s, i) => s + findProduct(i.id).price * i.qty, 0);
  const discount = subtotal * discountRate;
  const shipping = subtotal === 0 || subtotal - discount >= 500 ? 0 : 49.9;
  const total = subtotal - discount + shipping;
  const empty = cart.length === 0;
  const price = v => formatPrice(v, locale);

  const setField = (name, value) => setForm(f => ({ ...f, [name]: value }));

  function applyCoupon() {
    const code = coupon.trim().toUpperCase();
    if (COUPONS[code]) {
      setDiscountRate(COUPONS[code]);
      setCouponMessage({ ok: true, key: "coupon.applied", pct: Math.round(COUPONS[code] * 100) });
    } else {
      setDiscountRate(0);
      setCouponMessage({ ok: false, key: "coupon.invalid" });
    }
  }

  function confirmRemove() {
    removeItem(pendingRemove);
    setPendingRemove(null);
    showToast(t("toast.removed"));
  }

  function handleSubmit(e) {
    e.preventDefault();
    const found = [];
    if (!form.firstName.trim()) found.push("err.firstName");
    if (!form.lastName.trim()) found.push("err.lastName");
    if (!form.address.trim()) found.push("err.address");
    if (!form.city) found.push("err.city");
    if (!/^\d{5}$/.test(form.postalCode)) found.push("err.postal");
    if (!form.acceptTerms) found.push("err.terms");
    setErrors(found);
    if (found.length) return;
    setOrderNumber("SL-" + Date.now().toString().slice(-8));
    clearCart();
  }

  if (orderNumber) {
    return (
      <div id="order-success" className="card order-success visible" data-testid="order-success-message" data-qa="order-confirmation" role="status">
        <h2>{t("order.success")}</h2>
        <p>{t("order.number")} <strong id="order-number" data-testid="order-number" data-qa="order-id">{orderNumber}</strong></p>
        <Link to="/products" id="back-to-products" className="btn btn-primary" data-testid="back-to-products-button" data-qa="back-to-shop" title={t("order.back")}>
          {t("order.back")}
        </Link>
      </div>
    );
  }

  return (
    <>
      <h1 className="page-title" id="cart-title" data-testid="cart-page-title" data-qa="page-title">{t("cart.title")}</h1>

      <div id="cart-content" className="cart-layout" data-testid="cart-content" data-qa="cart-container">
        <div className="card">
          <table className="cart-table" id="cart-table" data-testid="cart-table" data-qa="cart-items-table" aria-label={t("cart.tableAria")}>
            <thead>
              <tr>
                <th>{t("cart.product")}</th>
                <th>{t("cart.option")}</th>
                <th>{t("cart.qty")}</th>
                <th>{t("cart.amount")}</th>
                <th></th>
              </tr>
            </thead>
            <tbody id="cart-items" data-testid="cart-items" data-qa="cart-rows">
              {cart.map((item, index) => {
                const p = findProduct(item.id);
                const name = t(`product.${p.id}.name`);
                const option = [item.color && t(`color.${item.color}`), item.size].filter(Boolean).join(" / ") || "-";
                return (
                  <tr
                    key={`${item.id}-${item.color}-${item.size}`}
                    id={`cart-row-${p.id}-${index}`}
                    className="cart-row"
                    data-testid={`cart-row-${index}`}
                    data-qa="cart-item"
                    aria-label={name}
                  >
                    <td>
                      <Link
                        to={`/products/${p.id}`}
                        id={`cart-item-name-${index}`}
                        className="cart-item-name"
                        data-testid={`cart-item-name-${index}`}
                        data-qa="cart-item-name"
                        title={name}
                      >
                        {p.emoji} {name}
                      </Link>
                    </td>
                    <td className="cart-item-option" data-testid={`cart-item-option-${index}`}>{option}</td>
                    <td>
                      <input
                        type="number"
                        value={item.qty}
                        onChange={e => updateQty(index, Math.max(1, Math.min(10, Number(e.target.value) || 1)))}
                        id={`cart-qty-${index}`}
                        name="quantity"
                        className="qty-input cart-qty"
                        data-testid={`cart-qty-input-${index}`}
                        data-qa="cart-item-qty"
                        aria-label={t("cart.qtyAria", { name })}
                        title={t("cart.qty")}
                        min="1"
                        max="10"
                      />
                    </td>
                    <td id={`cart-line-total-${index}`} className="cart-line-total" data-testid={`cart-line-total-${index}`} data-qa="cart-item-total">
                      {price(p.price * item.qty)}
                    </td>
                    <td>
                      <button
                        type="button"
                        onClick={() => setPendingRemove(index)}
                        id={`remove-item-${index}`}
                        name="removeItem"
                        className="btn btn-danger btn-remove"
                        data-testid={`remove-item-button-${index}`}
                        data-qa="remove-item"
                        aria-label={t("cart.removeAria", { name })}
                        title={t("cart.remove")}
                      >
                        {t("cart.remove")}
                      </button>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
          <div id="cart-empty" className={"empty-state" + (empty ? " visible" : "")} data-testid="cart-empty-message" data-qa="empty-cart">
            {t("cart.empty")}{" "}
            <Link to="/products" id="empty-cart-shop-link" data-testid="empty-cart-shop-link" data-qa="go-shopping" title={t("cart.startShopping")}>
              {t("cart.startShopping")}
            </Link>
          </div>
        </div>

        <aside className="card" id="order-summary" data-testid="order-summary" data-qa="summary-panel" aria-label={t("summary.aria")}>
          <h3>{t("summary.title")}</h3>
          <div className="summary-row">
            <span>{t("summary.subtotal")}</span>
            <span id="summary-subtotal" className="summary-subtotal" data-testid="summary-subtotal" data-qa="subtotal">{price(subtotal)}</span>
          </div>
          <div className="summary-row">
            <span>{t("summary.discount")}</span>
            <span id="summary-discount" className="summary-discount" data-testid="summary-discount" data-qa="discount">-{price(discount)}</span>
          </div>
          <div className="summary-row">
            <span>{t("summary.shipping")}</span>
            <span id="summary-shipping" className="summary-shipping" data-testid="summary-shipping" data-qa="shipping">{price(shipping)}</span>
          </div>
          <div className="summary-row summary-total">
            <span>{t("summary.total")}</span>
            <span id="summary-total" className="summary-total-value" data-testid="summary-total" data-qa="total-price">{price(total)}</span>
          </div>

          <div className="coupon-row">
            <input
              type="text"
              value={coupon}
              onChange={e => setCoupon(e.target.value)}
              id="coupon-code"
              name="couponCode"
              className="form-input input-coupon"
              data-testid="coupon-code-input"
              data-qa="coupon-field"
              aria-label={t("coupon.placeholder")}
              placeholder={t("coupon.placeholder")}
              title={t("coupon.placeholder")}
            />
            <button
              type="button"
              onClick={applyCoupon}
              id="apply-coupon"
              name="applyCoupon"
              className="btn btn-secondary btn-coupon"
              data-testid="apply-coupon-button"
              data-qa="apply-coupon"
              aria-label={t("coupon.applyAria")}
              title={t("coupon.apply")}
            >
              {t("coupon.apply")}
            </button>
          </div>
          <div
            id="coupon-message"
            className={"alert" + (couponMessage ? " visible " + (couponMessage.ok ? "alert-success" : "alert-error") : "")}
            data-testid="coupon-message"
            data-qa="coupon-feedback"
            role="status"
          >
            {couponMessage && t(couponMessage.key, { pct: couponMessage.pct })}
          </div>
          <p style={{ fontSize: 13, color: "var(--muted)" }}>{t("cart.freeShipping")} <code>SAVE10</code></p>
        </aside>
      </div>

      {!empty && (
        <section className="card checkout-section" id="checkout-section" data-testid="checkout-section" data-qa="checkout">
          <h3>{t("delivery.title")}</h3>
          <div
            id="checkout-error"
            className={"alert alert-error" + (errors.length ? " visible" : "")}
            data-testid="checkout-error-message"
            data-qa="checkout-error"
            role="alert"
          >
            {errors.map(k => t(k)).join(" • ")}
          </div>
          <form onSubmit={handleSubmit} id="checkout-form" name="checkoutForm" data-testid="checkout-form" data-qa="checkout-form" noValidate>
            <div className="form-row">
              <div className="form-group">
                <label className="form-label" htmlFor="first-name">{t("delivery.firstName")}</label>
                <input
                  type="text"
                  value={form.firstName}
                  onChange={e => setField("firstName", e.target.value)}
                  id="first-name"
                  name="firstName"
                  className="form-input input-firstname"
                  data-testid="checkout-first-name-input"
                  data-qa="first-name"
                  aria-label={t("delivery.firstName")}
                  placeholder={t("delivery.firstNamePlaceholder")}
                  title={t("delivery.firstName")}
                  autoComplete="given-name"
                />
              </div>
              <div className="form-group">
                <label className="form-label" htmlFor="last-name">{t("delivery.lastName")}</label>
                <input
                  type="text"
                  value={form.lastName}
                  onChange={e => setField("lastName", e.target.value)}
                  id="last-name"
                  name="lastName"
                  className="form-input input-lastname"
                  data-testid="checkout-last-name-input"
                  data-qa="last-name"
                  aria-label={t("delivery.lastName")}
                  placeholder={t("delivery.lastNamePlaceholder")}
                  title={t("delivery.lastName")}
                  autoComplete="family-name"
                />
              </div>
            </div>
            <div className="form-group">
              <label className="form-label" htmlFor="address">{t("delivery.address")}</label>
              <textarea
                value={form.address}
                onChange={e => setField("address", e.target.value)}
                id="address"
                name="address"
                className="form-textarea input-address"
                data-testid="checkout-address-input"
                data-qa="address"
                aria-label={t("delivery.address")}
                placeholder={t("delivery.addressPlaceholder")}
                title={t("delivery.address")}
              />
            </div>
            <div className="form-row">
              <div className="form-group">
                <label className="form-label" htmlFor="city">{t("delivery.city")}</label>
                <select
                  value={form.city}
                  onChange={e => setField("city", e.target.value)}
                  id="city"
                  name="city"
                  className="form-select select-city"
                  data-testid="checkout-city-select"
                  data-qa="city"
                  aria-label={t("delivery.city")}
                  title={t("delivery.city")}
                >
                  <option value="">{t("delivery.citySelect")}</option>
                  <option value="istanbul">Istanbul</option>
                  <option value="ankara">Ankara</option>
                  <option value="izmir">Izmir</option>
                  <option value="bursa">Bursa</option>
                </select>
              </div>
              <div className="form-group">
                <label className="form-label" htmlFor="postal-code">{t("delivery.postalCode")}</label>
                <input
                  type="text"
                  value={form.postalCode}
                  onChange={e => setField("postalCode", e.target.value)}
                  id="postal-code"
                  name="postalCode"
                  className="form-input input-postal"
                  data-testid="checkout-postal-code-input"
                  data-qa="postal-code"
                  aria-label={t("delivery.postalCode")}
                  placeholder="34000"
                  title={t("delivery.postalCode")}
                  inputMode="numeric"
                  maxLength={5}
                />
              </div>
            </div>
            <div className="form-group">
              <label className="form-check" htmlFor="accept-terms">
                <input
                  type="checkbox"
                  checked={form.acceptTerms}
                  onChange={e => setField("acceptTerms", e.target.checked)}
                  id="accept-terms"
                  name="acceptTerms"
                  className="checkbox-terms"
                  data-testid="checkout-terms-checkbox"
                  data-qa="accept-terms"
                  aria-label={t("delivery.termsAria")}
                  title={t("delivery.termsTitle")}
                />
                {t("delivery.terms")}
              </label>
            </div>
            <button
              type="submit"
              id="place-order"
              name="placeOrder"
              className="btn btn-primary btn-place-order"
              data-testid="place-order-button"
              data-qa="place-order"
              aria-label={t("order.placeAria")}
              title={t("order.placeAria")}
            >
              {t("order.place")}
            </button>
          </form>
        </section>
      )}

      <div
        id="remove-modal"
        className={"modal-backdrop" + (pendingRemove !== null ? " open" : "")}
        data-testid="remove-item-modal"
        data-qa="confirm-remove-dialog"
        role="dialog"
        aria-modal="true"
        aria-labelledby="remove-modal-title"
      >
        <div className="modal">
          <h3 id="remove-modal-title">{t("modal.removeTitle")}</h3>
          <p>{t("modal.removeText")}</p>
          <div className="modal-actions">
            <button
              type="button"
              onClick={() => setPendingRemove(null)}
              id="remove-cancel"
              className="btn btn-secondary"
              data-testid="remove-cancel-button"
              data-qa="cancel-remove"
              aria-label={t("modal.cancel")}
              title={t("modal.cancel")}
            >
              {t("modal.cancel")}
            </button>
            <button
              type="button"
              onClick={confirmRemove}
              id="remove-confirm"
              className="btn btn-primary"
              data-testid="remove-confirm-button"
              data-qa="confirm-remove"
              aria-label={t("modal.confirm")}
              title={t("modal.confirm")}
            >
              {t("modal.confirm")}
            </button>
          </div>
        </div>
      </div>
    </>
  );
}
