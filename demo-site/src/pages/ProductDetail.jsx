import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { PRODUCTS, findProduct, formatPrice } from "../data.js";
import { useApp } from "../store.jsx";

const COLORS = ["black", "white", "blue"];

const TABS = [
  { key: "description", qa: "tab-desc" },
  { key: "specs", qa: "tab-specs" },
  { key: "reviews", qa: "tab-reviews" }
];

const clampQty = v => Math.max(1, Math.min(10, Number(v) || 1));

export default function ProductDetail() {
  const { id } = useParams();
  const product = findProduct(id) || PRODUCTS[0];
  const { addToCart, showToast, t, locale } = useApp();
  const [color, setColor] = useState("black");
  const [size, setSize] = useState("");
  const [sizeError, setSizeError] = useState(false);
  const [qty, setQty] = useState(1);
  const [tab, setTab] = useState("description");
  const name = t(`product.${product.id}.name`);

  useEffect(() => {
    document.title = "ShopLab - " + name;
  }, [name]);

  function handleAdd() {
    if (!size) {
      setSizeError(true);
      return;
    }
    setSizeError(false);
    addToCart(product.id, qty, color, size);
    showToast(t("toast.addedQty", { qty, name }));
  }

  return (
    <>
      <nav className="breadcrumb" id="breadcrumb" aria-label={t("detail.breadcrumbAria")} data-testid="product-breadcrumb" data-qa="breadcrumb">
        <Link to="/products" id="breadcrumb-products" data-testid="breadcrumb-products-link" data-qa="breadcrumb-back" title={t("detail.backAria")}>
          {t("nav.products")}
        </Link>{" / "}
        <span id="breadcrumb-current" data-testid="breadcrumb-current">{name}</span>
      </nav>

      <div className="detail-grid" id="product-detail" data-testid="product-detail" data-qa="product-detail-container">
        <div id="detail-image" className="detail-image" data-testid="product-detail-image" aria-hidden="true">{product.emoji}</div>

        <div className="detail-info">
          <span id="detail-category" className="product-category" data-testid="product-detail-category" data-qa="detail-category">
            {t(`category.${product.category}`)}
          </span>
          <h1 id="detail-name" className="page-title product-title" data-testid="product-detail-name" data-qa="detail-title">
            {name}
          </h1>
          <div id="detail-price" className="detail-price" data-testid="product-detail-price" data-qa="detail-price">
            {formatPrice(product.price, locale)}
          </div>

          <div className="option-group" id="color-options" data-testid="color-options" data-qa="color-selector" role="radiogroup" aria-label={t("detail.colorAria")}>
            <div className="form-label">{t("detail.color")}</div>
            <div className="option-list">
              {COLORS.map(c => (
                <button
                  key={c}
                  type="button"
                  onClick={() => setColor(c)}
                  id={`color-${c}`}
                  name="color"
                  className={"option-btn color-option" + (color === c ? " selected" : "")}
                  data-testid={`color-option-${c}`}
                  data-qa={`color-${c}`}
                  role="radio"
                  aria-checked={color === c}
                  aria-label={t(`color.${c}`)}
                  title={t(`color.${c}`)}
                >
                  {t(`color.${c}`)}
                </button>
              ))}
            </div>
          </div>

          <div className="option-group" id="size-options" data-testid="size-options" data-qa="size-selector">
            <label className="form-label" htmlFor="size-select">{t("detail.size")}</label>
            <select
              value={size}
              onChange={e => setSize(e.target.value)}
              id="size-select"
              name="size"
              className="form-select select-size"
              data-testid="size-select"
              data-qa="size-dropdown"
              aria-label={t("detail.sizeAria")}
              title={t("detail.size")}
            >
              <option value="">{t("detail.sizeSelect")}</option>
              <option value="S">S</option>
              <option value="M">M</option>
              <option value="L">L</option>
              <option value="XL">XL</option>
            </select>
            <div
              id="size-error"
              className={"field-error" + (sizeError ? " visible" : "")}
              data-testid="size-error-message"
              data-qa="size-error"
              role="alert"
            >
              {t("detail.sizeError")}
            </div>
          </div>

          <div className="option-group">
            <label className="form-label" htmlFor="quantity-input">{t("detail.qty")}</label>
            <div className="qty-control" id="quantity-control" data-testid="quantity-control" data-qa="quantity-selector">
              <button
                type="button"
                onClick={() => setQty(q => clampQty(q - 1))}
                id="quantity-decrease"
                name="decrease"
                className="qty-btn qty-minus"
                data-testid="quantity-decrease-button"
                data-qa="qty-minus"
                aria-label={t("detail.qtyDec")}
                title={t("detail.qtyDec")}
              >
                −
              </button>
              <input
                type="number"
                value={qty}
                onChange={e => setQty(clampQty(e.target.value))}
                id="quantity-input"
                name="quantity"
                className="qty-input"
                data-testid="quantity-input"
                data-qa="qty-value"
                aria-label={t("detail.qty")}
                title={t("detail.qty")}
                min="1"
                max="10"
              />
              <button
                type="button"
                onClick={() => setQty(q => clampQty(q + 1))}
                id="quantity-increase"
                name="increase"
                className="qty-btn qty-plus"
                data-testid="quantity-increase-button"
                data-qa="qty-plus"
                aria-label={t("detail.qtyInc")}
                title={t("detail.qtyInc")}
              >
                +
              </button>
            </div>
          </div>

          <div className="detail-actions">
            <button
              type="button"
              onClick={handleAdd}
              id="detail-add-to-cart"
              name="addToCart"
              className="btn btn-primary btn-add-cart"
              data-testid="product-detail-add-to-cart"
              data-qa="detail-add-to-cart"
              aria-label={t("detail.addAria")}
              title={t("detail.addAria")}
            >
              {t("detail.add")}
            </button>
            <Link
              to="/products"
              id="continue-shopping"
              className="btn btn-secondary"
              data-testid="continue-shopping-link"
              data-qa="continue-shopping"
              aria-label={t("detail.continue")}
              title={t("detail.continue")}
            >
              {t("detail.continue")}
            </Link>
          </div>
        </div>
      </div>

      <section className="tabs" id="product-tabs" data-testid="product-tabs" data-qa="product-tabs">
        <div className="tab-list" role="tablist" aria-label={t("detail.tabsAria")}>
          {TABS.map(tb => (
            <button
              key={tb.key}
              type="button"
              onClick={() => setTab(tb.key)}
              id={`tab-${tb.key}`}
              className={"tab-btn" + (tab === tb.key ? " active" : "")}
              data-testid={`tab-${tb.key}`}
              data-qa={tb.qa}
              role="tab"
              aria-selected={tab === tb.key}
              aria-controls={`panel-${tb.key}`}
              title={t(`tabs.${tb.key}`)}
            >
              {t(`tabs.${tb.key}`)}
            </button>
          ))}
        </div>
        <div id="panel-description" className={"tab-panel" + (tab === "description" ? " active" : "")} role="tabpanel" data-testid="panel-description" data-qa="panel-desc">
          <p id="detail-description" data-testid="product-detail-description">{t(`product.${product.id}.description`)}</p>
        </div>
        <div id="panel-specs" className={"tab-panel" + (tab === "specs" ? " active" : "")} role="tabpanel" data-testid="panel-specs" data-qa="panel-specs">
          <ul>
            <li>{t("specs.warranty")}</li>
            <li>{t("specs.shipping")}</li>
            <li>{t("specs.returns")}</li>
          </ul>
        </div>
        <div id="panel-reviews" className={"tab-panel" + (tab === "reviews" ? " active" : "")} role="tabpanel" data-testid="panel-reviews" data-qa="panel-reviews">
          <p><strong>Ayşe K.</strong> — ★★★★★ {t("review.1")}</p>
          <p><strong>Mehmet T.</strong> — ★★★★☆ {t("review.2")}</p>
        </div>
      </section>
    </>
  );
}
