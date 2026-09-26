import { useMemo, useState } from "react";
import { PRODUCTS } from "../data.js";
import { useApp } from "../store.jsx";
import ProductCard from "../components/ProductCard.jsx";

export default function Products() {
  const { addToCart, showToast, t, locale } = useApp();
  const [search, setSearch] = useState("");
  const [category, setCategory] = useState("all");
  const [sort, setSort] = useState("default");

  const visible = useMemo(() => {
    const term = search.trim().toLocaleLowerCase(locale);
    const name = p => t(`product.${p.id}.name`);
    const sorters = {
      "default": (a, b) => a.id - b.id,
      "price-asc": (a, b) => a.price - b.price,
      "price-desc": (a, b) => b.price - a.price,
      "name-asc": (a, b) => name(a).localeCompare(name(b), locale)
    };
    return PRODUCTS
      .filter(p => name(p).toLocaleLowerCase(locale).includes(term) && (category === "all" || p.category === category))
      .sort(sorters[sort]);
  }, [search, category, sort, t, locale]);

  function handleAdd(product) {
    addToCart(product.id);
    showToast(t("toast.added", { name: t(`product.${product.id}.name`) }));
  }

  return (
    <>
      <h1 className="page-title" id="products-title" data-testid="products-page-title" data-qa="page-title">{t("products.title")}</h1>

      <div className="toolbar" id="products-toolbar" data-testid="products-toolbar" data-qa="toolbar">
        <div className="search-box">
          <input
            type="search"
            value={search}
            onChange={e => setSearch(e.target.value)}
            id="product-search"
            name="search"
            className="form-input input-search"
            data-testid="product-search-input"
            data-qa="search-field"
            aria-label={t("products.searchAria")}
            placeholder={t("products.search")}
            title={t("products.searchAria")}
          />
        </div>
        <select
          value={category}
          onChange={e => setCategory(e.target.value)}
          id="category-filter"
          name="category"
          className="form-select select-category"
          data-testid="category-filter-select"
          data-qa="category-filter"
          aria-label={t("products.categoryAria")}
          title={t("products.categoryAria")}
        >
          <option value="all">{t("products.allCategories")}</option>
          <option value="electronics">{t("category.electronics")}</option>
          <option value="sports">{t("category.sports")}</option>
          <option value="clothing">{t("category.clothing")}</option>
          <option value="home">{t("category.home")}</option>
        </select>
        <select
          value={sort}
          onChange={e => setSort(e.target.value)}
          id="sort-select"
          name="sort"
          className="form-select select-sort"
          data-testid="product-sort-select"
          data-qa="sort-dropdown"
          aria-label={t("products.sortAria")}
          title={t("products.sortAria")}
        >
          <option value="default">{t("sort.default")}</option>
          <option value="price-asc">{t("sort.priceAsc")}</option>
          <option value="price-desc">{t("sort.priceDesc")}</option>
          <option value="name-asc">{t("sort.nameAsc")}</option>
        </select>
      </div>

      <div id="result-count" className="result-count" data-testid="product-result-count" data-qa="result-count" aria-live="polite">
        {t("products.count", { n: visible.length })}
      </div>

      <div id="product-grid" className="product-grid" data-testid="product-grid" data-qa="product-list" role="list">
        {visible.map(p => <ProductCard key={p.id} product={p} onAddToCart={handleAdd} />)}
      </div>

      <div
        id="empty-state"
        className={"empty-state" + (visible.length === 0 ? " visible" : "")}
        data-testid="products-empty-state"
        data-qa="no-results"
      >
        {t("products.empty")}
      </div>
    </>
  );
}
