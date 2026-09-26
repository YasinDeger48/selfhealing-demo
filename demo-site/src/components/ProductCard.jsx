import { Link } from "react-router-dom";
import { formatPrice } from "../data.js";
import { useApp } from "../store.jsx";

export default function ProductCard({ product, onAddToCart }) {
  const { t, locale } = useApp();
  const p = product;
  const name = t(`product.${p.id}.name`);
  return (
    <article
      id={`product-card-${p.id}`}
      className={`product-card card-${p.category}`}
      data-testid={`product-card-${p.id}`}
      data-qa="product-item"
      role="listitem"
      aria-label={name}
    >
      <div className="product-image" aria-hidden="true">{p.emoji}</div>
      <div className="product-body">
        <span className="product-category">{t(`category.${p.category}`)}</span>
        <Link
          to={`/products/${p.id}`}
          id={`product-name-${p.id}`}
          className="product-name"
          data-testid={`product-name-${p.id}`}
          data-qa="product-title"
          title={name}
        >
          {name}
        </Link>
        <span
          id={`product-price-${p.id}`}
          className="product-price"
          data-testid={`product-price-${p.id}`}
          data-qa="product-price"
        >
          {formatPrice(p.price, locale)}
        </span>
        <div className="product-actions">
          <Link
            to={`/products/${p.id}`}
            id={`view-product-${p.id}`}
            className="btn btn-secondary btn-view"
            data-testid={`view-product-${p.id}`}
            data-qa="view-details"
            aria-label={t("products.detailsAria", { name })}
            title={t("products.details")}
          >
            {t("products.details")}
          </Link>
          <button
            type="button"
            onClick={() => onAddToCart(p)}
            id={`add-to-cart-${p.id}`}
            name="addToCart"
            className="btn btn-primary btn-add-cart"
            data-testid={`add-to-cart-${p.id}`}
            data-qa="add-to-cart"
            aria-label={t("products.addToCartAria", { name })}
            title={t("products.addToCart")}
          >
            {t("products.addToCart")}
          </button>
        </div>
      </div>
    </article>
  );
}
