# ShopLab — Demo E-Commerce Site

React (Vite + React Router) demo e-ticaret sitesi; UI test otomasyonu ve self-healing denemeleri için.
Backend yoktur; oturum, sepet ve dil seçimi `localStorage` içinde tutulur.

**Diller:** English (varsayılan), Deutsch, Русский, 日本語, Türkçe, العربية (sağdan sola).
Dil seçici header'da ve giriş sayfasında (`[data-testid=language-select]`).

## Çalıştırma

```bash
cd demo-site
npm install        # ilk seferde
npm run dev
```

Tarayıcıda: http://localhost:8080 — demo kullanıcı: `standard_user` / `secret123`
(`locked_user` / `secret123` kilitli hesap hatasını gösterir).

## Sayfalar

| Route | Dosya | İçerik |
|---|---|---|
| `/login` | `src/pages/Login.jsx` | kullanıcı adı, şifre, beni hatırla, şifremi unuttum, hata mesajı, dil seçici |
| `/products` | `src/pages/Products.jsx`, `src/components/ProductCard.jsx` | arama, kategori filtresi, sıralama, 8 ürün kartı, sepete ekle |
| `/products/:id` | `src/pages/ProductDetail.jsx` | renk, beden (zorunlu), adet, sekmeler |
| `/cart` | `src/pages/Cart.jsx` | adet güncelleme, kaldırma modalı, kupon (`SAVE10`, `WELCOME20`), teslimat formu |
| `/contact` | `src/pages/Contact.jsx` | form doğrulama, radio, dosya yükleme, SSS modalı, toast |
| (ortak) | `src/components/Header.jsx` | logo, menü, sepet rozeti, dil seçici, kullanıcı adı, çıkış |

Her elementin attribute'ları için bkz. [ATTRIBUTES.md](ATTRIBUTES.md).

## Çeviriler

Metinler `src/i18n/<dil>.js` dosyalarında (anahtar → metin); eksik anahtar İngilizceye düşer.
Yeni dil eklemek: dosyayı oluşturup `src/i18n/index.js` içindeki `LANGUAGES` listesine ekleyin.

## Attribute'ları değiştirmek

Test attribute'larının hepsi (`id`, `name`, `className`, `data-testid`, `data-qa`, `aria-label`,
`placeholder`, `title`, `role`, görünen metin) serbestçe değiştirilebilir — sitenin davranışı
React state'ine bağlıdır. Attribute'lar component'lerde, görünen metin / aria-label / placeholder
çeviri dosyalarında durur. `npm run dev` açıkken kaydettiğiniz anda değişiklik tarayıcıya yansır.

## Locator'ları kırmak — mutate.py

```bash
python mutate.py --list            # tüm mutasyonları göster
python mutate.py --level low       # id / data-testid değişimleri (16)
python mutate.py --level medium    # + class, name, data-qa, görünen metin (35)
python mutate.py --level high      # + yapısal değişiklikler: wrapper, tag değişimi (46)
python mutate.py --level extreme   # + 4 elementin tüm kimlikleri eş anlamlılarla değişir (72)
python mutate.py --level removed   # negatif test: 4 element tamamen silinir (birikimli değil)
python mutate.py --reset           # orijinale dön
```

- Metin mutasyonları İngilizce çeviri dosyasını (`src/i18n/en.js`) değiştirir; testler varsayılan dil olan İngilizceyi görür.
- `extreme`: Password → Passphrase, Apply → Redeem, Place Order → Buy Now ... — metin benzerliğiyle
  çözülemez, anlamı kavrayan bir healer (ör. Claude) gerekir.
- `removed`: kupon butonu, sepet rozeti, arama kutusu ve yalnızca 8. ürünün sepete ekle butonu silinir
  (benzer 7 buton sayfada kalır - tuzak). Doğru davranış: bu locator'lar onarılmamalı, testler düşmeli.
- `npm run dev` açıksa script, sunucunun değişen dosyaların yeni halini servis ettiğini doğrular (OneDrive gibi senkron klasörlerde dosya izleyicisi değişiklik kaçırabiliyor); gerekirse dosyayı yeniden tetikler.
- Seviyeler kümülatiftir ve her çalıştırma orijinalden başlar; uygulananlar `mutations-applied.json` dosyasına yazılır.
- Orijinaller ilk çalıştırmada `.original/` klasörüne yedeklenir. Elle yaptığınız değişikliklerin üzerine
  yazılacaksa script durur (`--force` ile silinir). Siteye kalıcı bir değişiklik yaptıysanız: `python mutate.py --rebaseline`.
