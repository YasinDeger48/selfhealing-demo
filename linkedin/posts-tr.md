# LinkedIn metinleri - Türkçe

Linkleri gönderinin içine değil **ilk yoruma** koy (LinkedIn dış linkli gönderilerin erişimini düşürüyor).
Gönderi başına 3-5 hashtag yeterli.

---

## 1. Tanıtım gönderisi (carousel ile: `carousel/self-healing-tr.pdf`)

> Doküman olarak yükle ("Belge ekle"), başlık: **Locator bozuldu. Test bozulmadı.**

Bir id'nin adı değişti diye build kırmızı olmamalı.

Yeni sürümde `#login-username`, `#user-name` oldu. Kullanıcı için hiçbir şey bozulmadı - ama login'e dokunan her test düştü ve biri sabahını page object güncelleyerek geçirdi. Bunu çok yaşadım, bu yüzden bir çözüm yazdım.

**Self-healing locator framework** - Playwright ve Selenium testleri için açık kaynak bir Java kütüphanesi:

🔹 Selector artık bir şey bulamayınca test düşmüyor; framework elementin kayıtlı parmak izine (tag, id'ler, metin, label, konum) en çok benzeyen elementi buluyor.
🔹 Önce yerelde eşleştiriyor: ücretsiz, milisaniyeler. Emin değilse isteğe bağlı olarak Claude'a soruyor (heal başına ~$0.002).
🔹 Tahmin yürütmüyor: element gerçekten silindiyse "heal edilemez" diyor. Benchmark'ta yanlış element seçimi: 0.
🔹 Test WARN ile geçiyor ve rapor neyi düzelteceğini söylüyor: eski → yeni selector, kaynak dosya satırı ve hazır kod düzeltmesi.

Bozulmuş bir demo mağazada ölçtüm (86 element):
• id'ler değişince: %100
• id + metin + yapı değişince: %87 yerelde, %98.8 Claude ile
• silinen elementler: %100 doğru şekilde reddedildi

JUnit 5/4, TestNG ve Cucumber ile 20 kombinasyonda, paralel koşuda, Java 17/21/25, Linux ve Windows'ta test edildi. Maven Central'da, tek bağımlılık ve tek ayar dosyası.

Kodu, demo siteyi ve uyumluluk testlerini ilk yoruma bıraktım. Kendi projende denersen sonucu duymak isterim. 👇

#TestAutomation #Playwright #Selenium #QA #Java

---

## 2. Video gönderisi (`video/healing-demo-1280x800.webm` - LinkedIn için MP4'e çevir: README)

Bir testin kendini onarışını ilk kez izlemek garip bir his. 🎬

Bu videoda demo mağazanın arayüzü "yeni sürümde" değişti: id'ler, test id'leri, buton metinleri... Test eski selector'larla koşuyor.

Her adımda göreceğin:
❌ eski selector bulunamıyor
🔍 sayfadaki adaylar puanlanıyor (turuncu kutular)
✅ en iyi aday kabul ediliyor (yeşil kutu) ve test devam ediyor

Hepsi yerelde, Claude kapalı, maliyet $0. Sonunda rapor hangi page object satırının güncellenmesi gerektiğini söylüyor.

Overlay bir ayar: `healer.visual=true`. Hem Playwright hem Selenium'da çalışıyor.

Link ilk yorumda. 👇

#TestAutomation #SelfHealing #Playwright #QA

---

## 3. Seri - "Yanlış heal, düşen testten daha kötüdür" (görsel: `images/tr/06-guards.png`)

Self-healing araçlarının en tehlikeli hatası: yanlış elementi "bulmak". 🚨

Test yeşil geçer, ama başka bir butona tıklamıştır. Kırmızı bir test en azından dürüsttür.

Bu yüzden framework'te eşikten önce korumalar var. Skoru ne olursa olsun şunları asla seçmiyor:
• listedeki başka bir kayıt (sepete ekle #8 yerine #5)
• zıt anlamlı kontrol (artır yerine azalt, login yerine logout)
• buton yerine bir alan, `fill` için bir div
• başka bir locator'ın zaten sahip olduğu element

Benchmark'ta 373 bozulan elementte yanlış element seçimi: 0. Silinen elementlerin %100'ü "heal edilemez" olarak raporlandı.

Tahmin yerine dürüst bir hata. 🙂

#TestAutomation #QualityEngineering #SoftwareTesting

---

## 4. Seri - Maliyet (görsel: `images/tr/07-benchmark.png`)

"AI ile test onarma pahalı değil mi?" 💸

Ölçtüm. 86 elementlik demo mağazada 5 bozulma seviyesinde 373 bozuk element:
• Önce yerel heuristic dener - ücretsiz, milisaniyeler. Çoğu heal burada biter.
• Sadece emin olmadığında Claude'a sorar - sadece en iyi yerel adaylar gönderilir.
• Toplam Claude maliyeti: **$0.13**. Heal başına yaklaşık $0.002.

Üstüne: bir kez onarılan locator cache'e yazılıyor, sonraki koşularda tekrar ödeme yok. Koşu başına bütçe de koyabiliyorsun (`healer.llm.maxCostPerRun`).

Kişisel veriler Claude'a gitmeden maskeleniyor.

#AI #TestAutomation #Claude #QA

---

## 5. Seri - Uyumluluk (görsel: `images/tr/09-compatibility.png`)

"Bizim stack'te çalışır mı?" sorusunun cevabını tahminle değil testle verdim. ✅

20 ayrı proje, her biri aynı 10 testi iki kez koşuyor (bir kez yeşil, bir kez bilerek hatalı):
• Playwright ve Selenium × JUnit 5, JUnit 4, TestNG, Cucumber (JUnit 5 / TestNG / JUnit 4 üzerinde)
• paralel koşu, Playwright 1.45 ve Selenium 4.21 gibi eski sürümler
• gerçek siteler: her yüklemede tüm id'lerini değiştiren bir self-healing lab ve bozulmuş demo mağaza

Bu testler son turda 6 gerçek hata buldu - hepsi düzeltildi, notları repoda.

#Java #TestAutomation #Playwright #Selenium

---

## İlk yorum (her gönderinin altına)

🔗 Framework (kaynak kod, dokümantasyon): https://github.com/YasinDeger48/selfhealing-framework
🔗 Demo site, örnek projeler ve uyumluluk matrisi: https://github.com/YasinDeger48/selfhealing-demo
📦 Maven Central: https://central.sonatype.com/namespace/io.github.yasindeger48

```xml
<dependency>
  <groupId>io.github.yasindeger48</groupId>
  <artifactId>healer-playwright</artifactId>   <!-- ya da healer-selenium -->
  <version>2.2.0</version>
</dependency>
```

---

## Profil "Öne çıkanlar" (Featured) açıklaması

Self-healing locator framework - Playwright ve Selenium testleri için açık kaynak Java kütüphanesi. Değişen arayüzde elementi yeniden bulur, testi devam ettirir, düzeltmeyi raporlar. Maven Central'da.
