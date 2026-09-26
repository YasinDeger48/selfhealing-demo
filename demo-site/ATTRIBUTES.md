# ShopLab — Attribute Inventory

Generated from the rendered DOM of the original site (English, before any mutation).
Product cards and cart rows repeat; tables show the first one, N = product id / row index. Language selector: [data-testid=language-select].

## Login — `/login`

| tag | id | name | class | data-testid | data-qa | aria-label | placeholder | role |
|---|---|---|---|---|---|---|---|---|
| select | `language-select` | `language` | `form-select select-language` | `language-select` | `language-switcher` | `Language` |  |  |
| div | `login-card` |  | `card login-card` | `login-card` | `login-container` |  |  |  |
| div | `login-error` |  | `alert alert-error` | `login-error-message` | `login-error` |  |  | `alert` |
| form | `login-form` | `loginForm` |  | `login-form` | `login-form` |  |  |  |
| input | `login-username` | `username` | `form-input input-username` | `login-username-input` | `username-field` | `Username` | `Enter your username` |  |
| input | `login-password` | `password` | `form-input input-password` | `login-password-input` | `password-field` | `Password` | `Enter your password` |  |
| input | `remember-me` | `rememberMe` | `checkbox-remember` | `login-remember-checkbox` | `remember-me` | `Remember me` |  |  |
| a | `forgot-password-link` |  | `link-forgot` | `login-forgot-password-link` | `forgot-password` | `Forgot password?` |  |  |
| button | `login-button` | `loginButton` | `btn btn-primary btn-block btn-login` | `login-submit-button` | `login-button` | `Sign in` |  |  |
| p | `demo-hint` |  | `demo-hint` | `login-demo-hint` |  |  |  |  |
| div | `toast` |  | `toast` | `toast-message` | `toast` |  |  | `status` |

## Product list + shared header — `/products`

| tag | id | name | class | data-testid | data-qa | aria-label | placeholder | role |
|---|---|---|---|---|---|---|---|---|
| header | `site-header` |  | `site-header` | `site-header` | `header` |  |  |  |
| a | `brand-logo` |  | `brand` | `header-logo` | `logo` | `ShopLab home` |  |  |
| nav | `main-nav` |  | `main-nav` | `main-nav` | `main-navigation` | `Main menu` |  | `navigation` |
| a | `nav-products` |  | `nav-link active` | `nav-products-link` | `nav-products` | `Products` |  |  |
| a | `nav-cart` |  | `nav-link` | `nav-cart-link` | `nav-cart` | `Cart` |  |  |
| span | `cart-count` |  | `cart-badge` | `cart-count-badge` | `cart-badge` | `Items in cart` |  |  |
| a | `nav-contact` |  | `nav-link` | `nav-contact-link` | `nav-contact` | `Contact` |  |  |
| div |  |  | `user-area` | `header-user-area` |  |  |  |  |
| select | `language-select` | `language` | `form-select select-language` | `language-select` | `language-switcher` | `Language` |  |  |
| span | `header-username` |  | `username-label` | `header-username` | `current-user` |  |  |  |
| button | `logout-button` | `logout` | `btn btn-secondary btn-logout` | `logout-button` | `logout` | `Log out` |  |  |
| h1 | `products-title` |  | `page-title` | `products-page-title` | `page-title` |  |  |  |
| div | `products-toolbar` |  | `toolbar` | `products-toolbar` | `toolbar` |  |  |  |
| input | `product-search` | `search` | `form-input input-search` | `product-search-input` | `search-field` | `Search products` | `Search products...` |  |
| select | `category-filter` | `category` | `form-select select-category` | `category-filter-select` | `category-filter` | `Category filter` |  |  |
| select | `sort-select` | `sort` | `form-select select-sort` | `product-sort-select` | `sort-dropdown` | `Sort` |  |  |
| div | `result-count` |  | `result-count` | `product-result-count` | `result-count` |  |  |  |
| div | `product-grid` |  | `product-grid` | `product-grid` | `product-list` |  |  | `list` |
| article | `product-card-N` |  | `product-card card-electronics` | `product-card-N` | `product-item` | `Wireless Headphones` |  | `listitem` |
| a | `product-name-N` |  | `product-name` | `product-name-N` | `product-title` |  |  |  |
| span | `product-price-N` |  | `product-price` | `product-price-N` | `product-price` |  |  |  |
| a | `view-product-N` |  | `btn btn-secondary btn-view` | `view-product-N` | `view-details` | `View Wireless Headphones details` |  |  |
| button | `add-to-cart-N` | `addToCart` | `btn btn-primary btn-add-cart` | `add-to-cart-N` | `add-to-cart` | `Add Wireless Headphones to cart` |  |  |
| div | `empty-state` |  | `empty-state` | `products-empty-state` | `no-results` |  |  |  |
| footer |  |  | `site-footer` | `site-footer` |  |  |  |  |
| div | `toast` |  | `toast` | `toast-message` | `toast` |  |  | `status` |

## Product detail — `/products/1`

| tag | id | name | class | data-testid | data-qa | aria-label | placeholder | role |
|---|---|---|---|---|---|---|---|---|
| nav | `breadcrumb` |  | `breadcrumb` | `product-breadcrumb` | `breadcrumb` | `Breadcrumb` |  |  |
| a | `breadcrumb-products` |  |  | `breadcrumb-products-link` | `breadcrumb-back` |  |  |  |
| span | `breadcrumb-current` |  |  | `breadcrumb-current` |  |  |  |  |
| div | `product-detail` |  | `detail-grid` | `product-detail` | `product-detail-container` |  |  |  |
| div | `detail-image` |  | `detail-image` | `product-detail-image` |  |  |  |  |
| span | `detail-category` |  | `product-category` | `product-detail-category` | `detail-category` |  |  |  |
| h1 | `detail-name` |  | `page-title product-title` | `product-detail-name` | `detail-title` |  |  |  |
| div | `detail-price` |  | `detail-price` | `product-detail-price` | `detail-price` |  |  |  |
| div | `color-options` |  | `option-group` | `color-options` | `color-selector` | `Color selection` |  | `radiogroup` |
| button | `color-black` | `color` | `option-btn color-option selected` | `color-option-black` | `color-black` | `Black` |  | `radio` |
| button | `color-white` | `color` | `option-btn color-option` | `color-option-white` | `color-white` | `White` |  | `radio` |
| button | `color-blue` | `color` | `option-btn color-option` | `color-option-blue` | `color-blue` | `Blue` |  | `radio` |
| div | `size-options` |  | `option-group` | `size-options` | `size-selector` |  |  |  |
| select | `size-select` | `size` | `form-select select-size` | `size-select` | `size-dropdown` | `Size selection` |  |  |
| div | `size-error` |  | `field-error` | `size-error-message` | `size-error` |  |  | `alert` |
| div | `quantity-control` |  | `qty-control` | `quantity-control` | `quantity-selector` |  |  |  |
| button | `quantity-decrease` | `decrease` | `qty-btn qty-minus` | `quantity-decrease-button` | `qty-minus` | `Decrease quantity` |  |  |
| input | `quantity-input` | `quantity` | `qty-input` | `quantity-input` | `qty-value` | `Quantity` |  |  |
| button | `quantity-increase` | `increase` | `qty-btn qty-plus` | `quantity-increase-button` | `qty-plus` | `Increase quantity` |  |  |
| button | `detail-add-to-cart` | `addToCart` | `btn btn-primary btn-add-cart` | `product-detail-add-to-cart` | `detail-add-to-cart` | `Add to cart` |  |  |
| a | `continue-shopping` |  | `btn btn-secondary` | `continue-shopping-link` | `continue-shopping` | `Continue Shopping` |  |  |
| section | `product-tabs` |  | `tabs` | `product-tabs` | `product-tabs` |  |  |  |
| button | `tab-description` |  | `tab-btn active` | `tab-description` | `tab-desc` |  |  | `tab` |
| button | `tab-specs` |  | `tab-btn` | `tab-specs` | `tab-specs` |  |  | `tab` |
| button | `tab-reviews` |  | `tab-btn` | `tab-reviews` | `tab-reviews` |  |  | `tab` |
| div | `panel-description` |  | `tab-panel active` | `panel-description` | `panel-desc` |  |  | `tabpanel` |
| p | `detail-description` |  |  | `product-detail-description` |  |  |  |  |
| div | `panel-specs` |  | `tab-panel` | `panel-specs` | `panel-specs` |  |  | `tabpanel` |
| div | `panel-reviews` |  | `tab-panel` | `panel-reviews` | `panel-reviews` |  |  | `tabpanel` |
| div | `toast` |  | `toast` | `toast-message` | `toast` |  |  | `status` |

## Cart / checkout — `/cart`

| tag | id | name | class | data-testid | data-qa | aria-label | placeholder | role |
|---|---|---|---|---|---|---|---|---|
| h1 | `cart-title` |  | `page-title` | `cart-page-title` | `page-title` |  |  |  |
| div | `cart-content` |  | `cart-layout` | `cart-content` | `cart-container` |  |  |  |
| table | `cart-table` |  | `cart-table` | `cart-table` | `cart-items-table` | `Items in your cart` |  |  |
| tbody | `cart-items` |  |  | `cart-items` | `cart-rows` |  |  |  |
| tr | `cart-row-1-N` |  | `cart-row` | `cart-row-N` | `cart-item` | `Wireless Headphones` |  |  |
| a | `cart-item-name-N` |  | `cart-item-name` | `cart-item-name-N` | `cart-item-name` |  |  |  |
| td |  |  | `cart-item-option` | `cart-item-option-N` |  |  |  |  |
| input | `cart-qty-N` | `quantity` | `qty-input cart-qty` | `cart-qty-input-N` | `cart-item-qty` | `Wireless Headphones quantity` |  |  |
| td | `cart-line-total-N` |  | `cart-line-total` | `cart-line-total-N` | `cart-item-total` |  |  |  |
| button | `remove-item-N` | `removeItem` | `btn btn-danger btn-remove` | `remove-item-button-N` | `remove-item` | `Remove Wireless Headphones` |  |  |
| div | `cart-empty` |  | `empty-state` | `cart-empty-message` | `empty-cart` |  |  |  |
| a | `empty-cart-shop-link` |  |  | `empty-cart-shop-link` | `go-shopping` |  |  |  |
| aside | `order-summary` |  | `card` | `order-summary` | `summary-panel` | `Order summary` |  |  |
| span | `summary-subtotal` |  | `summary-subtotal` | `summary-subtotal` | `subtotal` |  |  |  |
| span | `summary-discount` |  | `summary-discount` | `summary-discount` | `discount` |  |  |  |
| span | `summary-shipping` |  | `summary-shipping` | `summary-shipping` | `shipping` |  |  |  |
| span | `summary-total` |  | `summary-total-value` | `summary-total` | `total-price` |  |  |  |
| input | `coupon-code` | `couponCode` | `form-input input-coupon` | `coupon-code-input` | `coupon-field` | `Coupon code` | `Coupon code` |  |
| button | `apply-coupon` | `applyCoupon` | `btn btn-secondary btn-coupon` | `apply-coupon-button` | `apply-coupon` | `Apply coupon` |  |  |
| div | `coupon-message` |  | `alert` | `coupon-message` | `coupon-feedback` |  |  | `status` |
| section | `checkout-section` |  | `card checkout-section` | `checkout-section` | `checkout` |  |  |  |
| div | `checkout-error` |  | `alert alert-error` | `checkout-error-message` | `checkout-error` |  |  | `alert` |
| form | `checkout-form` | `checkoutForm` |  | `checkout-form` | `checkout-form` |  |  |  |
| input | `first-name` | `firstName` | `form-input input-firstname` | `checkout-first-name-input` | `first-name` | `First name` | `Your first name` |  |
| input | `last-name` | `lastName` | `form-input input-lastname` | `checkout-last-name-input` | `last-name` | `Last name` | `Your last name` |  |
| textarea | `address` | `address` | `form-textarea input-address` | `checkout-address-input` | `address` | `Address` | `Your full address` |  |
| select | `city` | `city` | `form-select select-city` | `checkout-city-select` | `city` | `City` |  |  |
| input | `postal-code` | `postalCode` | `form-input input-postal` | `checkout-postal-code-input` | `postal-code` | `Postal code` | `34000` |  |
| input | `accept-terms` | `acceptTerms` | `checkbox-terms` | `checkout-terms-checkbox` | `accept-terms` | `I accept the terms of sale` |  |  |
| button | `place-order` | `placeOrder` | `btn btn-primary btn-place-order` | `place-order-button` | `place-order` | `Place order` |  |  |
| div | `remove-modal` |  | `modal-backdrop` | `remove-item-modal` | `confirm-remove-dialog` |  |  | `dialog` |
| button | `remove-cancel` |  | `btn btn-secondary` | `remove-cancel-button` | `cancel-remove` | `Cancel` |  |  |
| button | `remove-confirm` |  | `btn btn-primary` | `remove-confirm-button` | `confirm-remove` | `Remove` |  |  |
| div | `toast` |  | `toast` | `toast-message` | `toast` |  |  | `status` |

## Contact — `/contact`

| tag | id | name | class | data-testid | data-qa | aria-label | placeholder | role |
|---|---|---|---|---|---|---|---|---|
| h1 | `contact-title` |  | `page-title` | `contact-page-title` | `page-title` |  |  |  |
| section | `contact-card` |  | `card` | `contact-card` | `contact-container` |  |  |  |
| div | `contact-success` |  | `alert alert-success` | `contact-success-message` | `contact-success` |  |  | `status` |
| div | `contact-error` |  | `alert alert-error` | `contact-error-message` | `contact-error` |  |  | `alert` |
| form | `contact-form` | `contactForm` |  | `contact-form` | `contact-form` |  |  |  |
| input | `contact-name` | `fullName` | `form-input input-fullname` | `contact-name-input` | `full-name` | `Full name` | `Your first and last name` |  |
| input | `contact-email` | `email` | `form-input input-email` | `contact-email-input` | `email` | `Email address` | `name@example.com` |  |
| input | `contact-phone` | `phone` | `form-input input-phone` | `contact-phone-input` | `phone` | `Phone number` | `+90 5xx xxx xx xx` |  |
| select | `contact-subject` | `subject` | `form-select select-subject` | `contact-subject-select` | `subject` | `Subject` |  |  |
| div |  |  | `radio-group` | `contact-preference-group` | `contact-preference` | `Contact preference` |  | `radiogroup` |
| input | `pref-email` | `preference` | `radio-pref` | `contact-pref-email` | `pref-email` | `By email` |  |  |
| input | `pref-phone` | `preference` | `radio-pref` | `contact-pref-phone` | `pref-phone` | `By phone` |  |  |
| input | `pref-sms` | `preference` | `radio-pref` | `contact-pref-sms` | `pref-sms` | `By SMS` |  |  |
| textarea | `contact-message` | `message` | `form-textarea input-message` | `contact-message-input` | `message` | `Your message` | `Write your message (at least 10 characters)` |  |
| div | `char-counter` |  | `result-count` | `contact-char-counter` | `char-count` |  |  |  |
| input | `contact-attachment` | `attachment` | `form-input input-file` | `contact-attachment-input` | `attachment` | `Attachment (optional)` |  |  |
| input | `newsletter` | `newsletter` | `checkbox-newsletter` | `contact-newsletter-checkbox` | `newsletter` | `Subscribe to promotions` |  |  |
| button | `contact-submit` | `send` | `btn btn-primary btn-send` | `contact-submit-button` | `send-message` | `Send message` |  |  |
| button | `contact-clear` | `clear` | `btn btn-secondary btn-clear` | `contact-clear-button` | `clear-form` | `Clear form` |  |  |
| aside | `contact-info` |  | `card` | `contact-info` | `contact-info-panel` |  |  |  |
| button | `faq-button` | `faq` | `btn btn-secondary btn-block` | `faq-open-button` | `open-faq` | `Frequently Asked Questions` |  |  |
| div | `faq-modal` |  | `modal-backdrop` | `faq-modal` | `faq-dialog` |  |  | `dialog` |
| button | `faq-close` |  | `btn btn-primary` | `faq-close-button` | `close-faq` | `Close` |  |  |
| div | `toast` |  | `toast` | `toast-message` | `toast` |  |  | `status` |
