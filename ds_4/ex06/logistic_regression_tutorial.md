# Logistic Regression: Matematiksel ve İstatistiksel Hikâye

Bu doküman, Logistic Regression'ı yalnızca formülleri ezberleyerek değil, her adımın **neden gerekli olduğunu** anlayarak öğrenmek için hazırlanmıştır. Baştan sona aynı 10 gözlem ve 3 özellik (feature) kullanılacaktır. Hesaplamalar Python'da `StandardScaler` ve `LogisticRegression` ile gerçekten çalıştırılmıştır; katsayılar veya olasılıklar örnek olsun diye uydurulmamıştır.

> **Önemli ayrım:** Aşağıdaki sayısal sonuçlar bu dokümanda tanımlanan 10 satırlık veri kümesine, `StandardScaler` ayarlarına ve scikit-learn'ün L2 düzenlileştirmeli `LogisticRegression(C=1.0, solver="lbfgs")` modeline aittir. Başka veri, ölçekleme, `C` veya yazılım ayarı farklı katsayılar üretebilir.

## 0. Problemimiz ve veri kümesi

İki sınıflı bir problem düşünelim:

- `y = 0`: sınıf 0 (örneğin Jedi)
- `y = 1`: sınıf 1 (örneğin Sith)

Her gözlemi üç sayıyla tarif ediyoruz: `x1`, `x2`, `x3`. Bunlar ölçülen üç özelliktir. Gerçek hayatta özelliklerin neyi temsil ettiği probleme bağlıdır; burada matematiğe odaklanmak için genel özellikler olarak düşünelim.

| Gözlem | x1 | x2 | x3 | Gerçek y |
|---:|---:|---:|---:|---:|
| 1 | 1.0 | 2.0 | 1.0 | 0 |
| 2 | 1.5 | 1.8 | 1.2 | 0 |
| 3 | 2.0 | 1.0 | 1.5 | 0 |
| 4 | 2.2 | 1.5 | 1.0 | 0 |
| 5 | 2.5 | 2.0 | 1.8 | 0 |
| 6 | 3.0 | 1.0 | 2.0 | 1 |
| 7 | 3.2 | 2.5 | 2.2 | 1 |
| 8 | 4.0 | 3.0 | 2.5 | 1 |
| 9 | 4.2 | 2.0 | 3.0 | 1 |
| 10 | 5.0 | 3.5 | 3.2 | 1 |

İlk beş gözlemin etiketi 0, son beş gözlemin etiketi 1'dir. Bu küçük ve öğretici bir veri kümesidir; gerçek projelerde sınıflar bu kadar düzenli ayrılmayabilir. Etiketler, modelin öğrenirken kullanacağı doğru cevaplardır. Modelin görevi bu etiketleri ezberlemek değil, özelliklerle sınıf arasındaki ilişkiyi öğrenip yeni gözlemlerde tahmin yapmaktır.

---

## Adım 1 — Özellikleri neden standardize ediyoruz?

### 1.1. Standardizasyon ne yapar?

Her özellik sütunu için önce ortalamayı hesaplarız. Ardından her gözlemden ortalamayı çıkarır ve standart sapmaya böleriz:

`x_standard = (x - mean) / standard_deviation`

Bu işlem iki şeyi aynı anda yapar:

1. Sütunun merkezini yaklaşık 0'a taşır.
2. Sütunun ölçeğini standart sapma birimine dönüştürür; sonuçtaki sütunun varyansı 1 olur (scikit-learn `StandardScaler`, standart sapmayı hesaplarken varsayılan olarak `ddof=0` kullanır).

Standardizasyon **etiket sütununa uygulanmaz**. `y` hâlâ 0 veya 1'dir; sadece `X` içindeki özellikler dönüştürülür.

### 1.2. Neden faydalıdır?

Diyelim ki bir özellik milimetreyle 0–1000 aralığında, başka bir özellik metreyle 0–2 aralığında ölçülüyor. Ölçekler çok farklı olduğunda katsayıların sayısal büyüklüklerini doğrudan karşılaştırmak yanıltıcı olur. Ayrıca L2 regularization gibi katsayı büyüklüğünü cezalandıran yöntemlerde, ölçek farkı hangi özelliğin ne kadar cezalandırıldığına etki eder. Standardizasyon, özellikleri benzer bir ölçeğe getirerek optimizasyonu da çoğu zaman daha kolay ve dengeli hâle getirir.

Standardizasyon, her özelliğin aynı derecede önemli olduğunu **kanıtlamaz**. Yalnızca birim ve ölçek farklılıklarını azaltır. Ayrıca aykırı değerlere dayanıklı bir işlem değildir; uç değerler ortalama ve standart sapmayı etkileyebilir.

### 1.3. Bu veri kümesinde gerçek hesap

Python `StandardScaler` ile hesaplanan sütun ortalamaları ve ölçek değerleri:

| Özellik | Ortalama | StandardScaler ölçeği (std) |
|---|---:|---:|
| x1 | 2.860000 | 1.20099958 |
| x2 | 2.030000 | 0.76032888 |
| x3 | 1.940000 | 0.74993333 |

Örneğin 1. gözlemin `x1=1.0` değeri için:

`x1_standard = (1.0 - 2.86) / 1.20099958 ≈ -1.5487`

Bu, gözlemin x1 bakımından ortalamanın yaklaşık 1.55 standart sapma altında olduğunu söyler. Negatif değer “özellik kötü” demek değildir; yalnızca ortalamanın altında olduğunu belirtir.

Aynı yöntemle 10 gözlemin tüm özellikleri dönüştürülür:

| Gözlem | x1_standard | x2_standard | x3_standard | y |
|---:|---:|---:|---:|---:|
| 1 | -1.5487 | -0.0395 | -1.2534 | 0 |
| 2 | -1.1324 | -0.3025 | -0.9868 | 0 |
| 3 | -0.7161 | -1.3547 | -0.5867 | 0 |
| 4 | -0.5495 | -0.6971 | -1.2534 | 0 |
| 5 | -0.2998 | -0.0395 | -0.1867 | 0 |
| 6 | 0.1166 | -1.3547 | 0.0800 | 1 |
| 7 | 0.2831 | 0.6182 | 0.3467 | 1 |
| 8 | 0.9492 | 1.2758 | 0.7467 | 1 |
| 9 | 1.1157 | -0.0395 | 1.4135 | 1 |
| 10 | 1.7818 | 1.9334 | 1.6801 | 1 |

Bu tablodaki yuvarlamalar yalnızca görüntüleme içindir. Model, tam hassasiyetli değerlerle eğitilmiştir.

**Veri sızıntısı uyarısı:** Gerçek bir eğitim/doğrulama düzeninde scaler yalnızca eğitim verisine `fit` edilir; doğrulama/test verisine yalnızca `transform` uygulanır. Burada bütün 10 satırı birlikte standardize etmemizin sebebi, yalnızca matematiği elle izlenebilir bir örnek üzerinde öğretmektir. Gerçek test verisi eğitimdeki ortalama ve standart sapmayla dönüştürülmelidir.

---

## Adım 2 — Asıl hedefimiz nedir? `z = wᵀx + b`

Bir gözlemin standardize edilmiş özellik vektörü `x = (x1, x2, x3)` olsun. Model önce doğrusal bir puan hesaplar:

`z = w1*x1 + w2*x2 + w3*x3 + b`

Burada:

- `w1, w2, w3`: öğrenilecek ağırlıklar/katsayılar.
- `b`: bias/intercept, yani sabit terim.
- `z`: sınıf etiketi değil, sınıf 1 yönündeki doğrusal puandır.

Vektör yazımıyla `z = wᵀx + b`. `wᵀx`, iki vektörün iç çarpımıdır; her özelliğin ağırlıklı katkısını toplar.

### 2.1. Ağırlıklar ne anlama gelir?

Diğer özellikler sabit tutulduğunda `w1`, standardize edilmiş `x1` bir birim artarsa `z` puanının ne kadar değiştiğini belirtir. Pozitif ağırlık `z`'yi artırır; negatif ağırlık azaltır. Ancak bu, tek başına nedensellik anlamına gelmez ve özellikler birbiriyle ilişkiliyse katsayıları tek tek yorumlamak dikkat gerektirir.

`b`, tüm özellikler 0 iken puanın ne olduğunu belirler. Standardize edilmiş özelliklerde 0, her sütunun eğitim ortalamasına karşılık gelir. Dolayısıyla `b`, ortalama özellik profili için başlangıç puanını belirlemeye yardımcı olur.

### 2.2. Neden doğrudan 0 veya 1 üretmiyoruz?

Doğrusal puan `z` herhangi bir gerçek sayı olabilir: `-5`, `0.3`, `12` vb. Bunu doğrudan sınıf diye yorumlayamayız. Ayrıca özelliklerin ağırlıklı toplamı olasılık değildir; 1'den büyük veya 0'dan küçük çıkabilir. Bu yüzden puanı olasılığa dönüştüren bir fonksiyona ihtiyacımız vardır. Logistic Regression bunu sigmoid fonksiyonuyla yapar; bir sonraki adımda sigmoidin neden doğal bir seçim olduğunu göreceğiz.

### 2.3. Öğrenme problemi

Ağırlıkları ve bias'ı öyle seçmek istiyoruz ki modelin verdiği olasılıklar gerçek etiketlerle olabildiğince uyumlu olsun. “Uyumlu” olmayı sayısal olarak ölçen bir kayıp fonksiyonuna ihtiyacımız var. Eğitim algoritması, bu kaybı azaltan katsayıları arar.

Bu noktada iki ayrı kavramı ayıralım:

- **Model:** `x`'ten `p` olasılığına giden matematiksel yapı.
- **Öğrenme/optimizasyon:** eğitim verisindeki etiketleri kullanarak `w` ve `b`'yi belirleme süreci.

---

## Adım 3 — Odds, sigmoid ve cross-entropy neden birbirine bağlanıyor?

Bu adım hikâyenin merkezidir. Logistic Regression'da sigmoid ve cross-entropy birbirinden bağımsız, rastgele seçilmiş parçalar değildir. Olasılığı doğrusal bir puanla ilişkilendirmek ve sonra bu olasılıkları istatistiksel olarak öğrenmek için tutarlı bir yapı kurarlar.

### 3.1. Olasılık tek başına ne söyler?

Bir gözlem için `p = P(y=1 | x)` diyelim. Bu, özellikleri `x` olan gözlemin sınıf 1'e ait olma olasılığıdır. İki sınıf bulunduğu için `P(y=0 | x) = 1-p`.

Örneğin `p=0.8`, modelin sınıf 1 olasılığını %80, sınıf 0 olasılığını %20 olarak değerlendirdiğini söyler. Fakat doğrusal bir ifade `z = wᵀx+b` herhangi bir gerçek sayı alır; doğrudan p olarak kullanılamaz.

### 3.2. Odds (olasılık oranı) nedir?

Odds, bir olayın gerçekleşme olasılığının gerçekleşmeme olasılığına oranıdır:

`odds = p / (1-p)`

Bu, p ile aynı şey değildir. Örnekler:

| p | 1-p | odds = p/(1-p) | Yorum |
|---:|---:|---:|---|
| 0.50 | 0.50 | 1 | İki sonuç eşit olasılıklı |
| 0.75 | 0.25 | 3 | Olay lehine 3'e 1 |
| 0.80 | 0.20 | 4 | Olay lehine 4'e 1 |
| 0.20 | 0.80 | 0.25 | Olay aleyhine; ters odds 4'e 1 |
| 0.90 | 0.10 | 9 | Olay lehine 9'a 1 |

Odds, “olur/olmaz olasılıklarının oranı”dır. Örneğin p=0.8 için odds 4'tür; bu, olasılığın %400 olduğu anlamına gelmez. Olayın olasılığı %80'dir; odds ise 0.8/0.2=4 oranıdır.

Odds neden kullanışlı? Olasılık 0 ile 1 arasında sıkışmıştır. Odds ise 0 ile sonsuz arasında değer alır. Daha önemlisi, odds'un doğal logaritması olan **log-odds** tüm gerçek sayıları alabilir:

`log-odds = log(p/(1-p))`

p=0.5 olduğunda log-odds=0; p>0.5 olduğunda pozitiftir; p<0.5 olduğunda negatiftir. Böylece sınıf 1'e eğilim ile sınıf 0'a eğilim, sıfırın iki tarafıyla temsil edilebilir.

### 3.3. Logistic Regression'ın temel varsayımı

Logistic Regression, olasılığın kendisinin değil, **log-odds'un özelliklerin doğrusal fonksiyonu** olduğunu varsayar:

`log(p/(1-p)) = w1*x1 + w2*x2 + w3*x3 + b = z`

Bu varsayımın matematiksel hikmeti şudur:

1. `z` doğrusal bir model olduğu için katsayıları öğrenmek ve yorumlamak kolaydır.
2. Log-odds herhangi bir gerçek sayı alabildiği için doğrusal puanla eşleştirilebilir.
3. Bu eşitlik olasılık aralığı olan (0,1)'e geri çevrilebilir.

Buradaki doğrusal ilişki, `p`'nin `x` ile doğrusal olduğu anlamına **gelmez**. Doğrusal olan `log(p/(1-p))`'dir.

### 3.4. Sigmoid formülü nereden geliyor?

Başlangıç eşitliğimiz:

`log(p/(1-p)) = z`

Her iki tarafın üstelini alalım:

`p/(1-p) = exp(z)`

Her iki tarafı `1-p` ile çarpalım:

`p = exp(z)*(1-p)`

Parantezi açalım:

`p = exp(z) - exp(z)*p`

p'li terimleri aynı tarafa alalım:

`p + exp(z)*p = exp(z)`

p'yi ortak çarpan yapalım:

`p*(1+exp(z)) = exp(z)`

Bölelim:

`p = exp(z)/(1+exp(z))`

Payı ve paydayı `exp(z)`'ye bölersek:

`p = 1/(1+exp(-z))`

İşte sigmoid fonksiyonu budur:

`sigmoid(z) = 1/(1+exp(-z))`

Dolayısıyla sigmoid, yalnızca “0 ile 1 arasında sonuç veren güzel bir eğri” olduğu için seçilmiş değildir. Log-odds'u doğrusal puana eşitleme varsayımını olasılık biçimine çözdüğümüzde doğal olarak ortaya çıkar.

### 3.5. z, odds ve p arasındaki tam ilişki

Önce `z` hesaplanır, sonra:

- `odds = exp(z)`
- `p = odds/(1+odds) = 1/(1+exp(-z))`

Örnekler:

| z | odds = exp(z) | p = sigmoid(z) | Yorum |
|---:|---:|---:|---|
| -2 | 0.1353 | 0.1192 | Sınıf 1 olasılığı düşük |
| 0 | 1.0000 | 0.5000 | İki sınıf eşit olasılıklı |
| 1 | 2.7183 | 0.7311 | Sınıf 1 olasılığı yaklaşık %73.1 |
| 2 | 7.3891 | 0.8808 | Sınıf 1 olasılığı yüksek |

z=0 iken odds=1 ve p=0.5 olur. Standart 0.5 karar eşiği kullanıldığında karar sınırı `z=0`, yani `wᵀx+b=0` düzlemidir. Üç özellik uzayında bu bir düzlem; iki özellikte bir doğru; daha yüksek boyutta bir hiper-düzlemdir.

### 3.6. Katsayıların odds yorumu

`log-odds = w1*x1 + ... + b` olduğundan, diğer özellikler sabitken `xj` bir birim artarsa log-odds `wj` kadar değişir. Odds ise `exp(wj)` katına çarpılır.

Örneğin bir katsayı `wj=0.7` olsaydı, bir birim artış odds'u `exp(0.7) ≈ 2.01` katına çıkarırdı; bu “olasılık 0.7 artar” demek değildir. Olasılık değişimi mevcut p düzeyine bağlıdır. Bu yorum, standardize edilmiş özellikte “bir standart sapmalık artış” için geçerlidir.

---

## Adım 4 — Binary cross-entropy kaybı nereden geliyor?

Sigmoid bize her gözlem için bir olasılık verir. Fakat hangi `w` ve `b` değerlerinin iyi olduğunu nasıl ölçeceğiz? Bunun için gerçek etiket ile tahmin edilen olasılığı karşılaştıran bir amaç fonksiyonu gerekir.

### 4.1. Önce tek bir gözlemi düşünelim

Bir gözlemin gerçek etiketi `y` yalnızca 0 veya 1 olabilir. Modelin sınıf 1 olasılığı `p` olsun.

- Gerçek etiket `y=1` ise modelin bu gözleme yüksek p vermesini isteriz.
- Gerçek etiket `y=0` ise modelin düşük p vermesini isteriz; çünkü sınıf 0 olasılığı `1-p`'dir.

İki durumu tek formülde yazabiliriz:

`P(y | x) = p^y * (1-p)^(1-y)`

Neden bu formül çalışır?

- y=1 koyarsak: `p^1*(1-p)^0 = p`.
- y=0 koyarsak: `p^0*(1-p)^1 = 1-p`.

Bu ifade, Bernoulli dağılımının olasılık kütle fonksiyonudur. İkili etiket için modelin gözlenen etikete verdiği olasılığı tek formülde gösterir.

### 4.2. Maksimum olabilirlik (maximum likelihood) fikri

Katsayılar doğruysa, modelin gerçekten gözlediğimiz etiketlere yüksek olasılık vermesini bekleriz. Bu nedenle `w` ve `b` için, gözlenen etiketlerin olasılığını en büyük yapan değerleri arayabiliriz. Buna **maksimum olabilirlik tahmini** denir.

Gözlemlerin birbirinden bağımsız olduğu varsayımı altında tüm etiketlerin ortak olabilirliği, tek tek olasılıkların çarpımıdır:

`L(w,b) = Π[i=1..n] p_i^(y_i) * (1-p_i)^(1-y_i)`

Çarpımlar çok küçük sayılara dönüşebildiği için ve çarpımı toplama dönüştürmek optimizasyonu kolaylaştırdığı için logaritma alırız:

`log L(w,b) = Σ[i=1..n] [y_i*log(p_i) + (1-y_i)*log(1-p_i)]`

Logaritma artan bir fonksiyondur; dolayısıyla `L`'yi büyüten parametreler `log L`'yi de büyütür. Makine öğrenmesinde çoğunlukla “maksimize et” yerine “minimize et” biçimi kullanılır. Bu yüzden negatif log-olabilirliği alırız:

`J(w,b) = -Σ[i=1..n] [y_i*log(p_i) + (1-y_i)*log(1-p_i)]`

Gözlem sayısına bölmek, kaybı toplam yerine gözlem başına ortalama hâline getirir:

`J(w,b) = -(1/n) * Σ[i=1..n] [y_i*log(p_i) + (1-y_i)*log(1-p_i)]`

Bu, **binary cross-entropy** (ikili çapraz entropi) veya **ortalama negatif log-olabilirlik**tir. Bu bağlamda iki isim, aynı matematiksel kayıp ifadesini anlatır.

### 4.3. Neden logaritma ve neden eksi işareti var?

**Logaritma:** Bağımsız gözlemlerin olasılıkları çarpılır; log alınca çarpım toplam olur. Ayrıca bir gözleme verilen çok küçük olasılık çok büyük bir negatif log-olasılık cezası üretir.

**Eksi işareti:** Olasılık en fazla 1 olduğundan `log(p)` ve `log(1-p)` sıfır veya negatiftir. Negatif log-olabilirlik böylece minimize edilmesi gereken pozitif bir kayıp olarak yazılır.

**Ortalama:** Toplam kayıp veri sayısıyla büyür. Ortalama almak kaybı gözlem başına raporlar ve veri kümeleri arasında kıyaslamayı kolaylaştırır. Sabit n için toplamı veya ortalamayı minimize etmek aynı katsayıları verir (başka ceza terimlerinin ölçeklendirilmesi kullanılan yazılımın amaç fonksiyonuna bağlıdır).

### 4.4. Tek formül, iki sınıf

Tek gözlem için:

`loss(y,p) = -[y*log(p) + (1-y)*log(1-p)]`

y=1 ise:

`loss(1,p) = -log(p)`

y=0 ise:

`loss(0,p) = -log(1-p)`

Yani model doğru sınıfa yüksek olasılık verdikçe kayıp küçülür. Yanlış sınıfa çok yüksek güven duyarsa kayıp hızla büyür.

| Gerçek y | Tahmin p | Kayıp |
|---:|---:|---:|
| 1 | 0.90 | `-log(0.90) ≈ 0.105` |
| 1 | 0.60 | `-log(0.60) ≈ 0.511` |
| 1 | 0.10 | `-log(0.10) ≈ 2.303` |
| 0 | 0.10 | `-log(0.90) ≈ 0.105` |
| 0 | 0.40 | `-log(0.60) ≈ 0.511` |
| 0 | 0.90 | `-log(0.10) ≈ 2.303` |

Örneğin gerçek sınıf 1 iken p=0.1 vermek, doğru sınıfa yalnızca %10 olasılık atamaktır; kayıp 2.303 olur. Gerçek sınıf 1 iken p=0.9 vermek çok daha uyumludur; kayıp yaklaşık 0.105'tir.

Bu kayıp, yalnızca tahmin edilen sınıf etiketine bakmaz; olasılığın ne kadar güvenli olduğunu da dikkate alır. İki model aynı sınıf etiketlerini tahmin etse bile olasılıkları farklıysa cross-entropy değerleri farklı olabilir.

### 4.5. “Cross-entropy” adı nereden geliyor?

Gerçek etiket için dağılımı, tek doğru sınıfa %100 olasılık veren dağılım olarak düşünebiliriz. Model ise sınıf 0 ve 1'e `(1-p, p)` dağılımını verir. Cross-entropy, gerçek dağılımın model dağılımı altında beklenen negatif log-olasılığıdır. İkili ve tek etiketli durumda bu ifade yukarıdaki binary cross-entropy formülüne indirgenir.

Bu yüzden kayıp, “modelin gerçek cevaba ne kadar olasılık verdiği” sorusunu ölçer. Doğru sınıfa düşük olasılık verildiğinde cezalandırma büyür.

### 4.6. O zaman katsayıları nasıl öğreniyoruz?

Her aday `w` ve `b` için:

1. Her satırda `z_i = wᵀx_i+b` hesaplanır.
2. `p_i = sigmoid(z_i)` hesaplanır.
3. Gerçek `y_i` ile `p_i` kullanılarak tüm satırların ortalama cross-entropy kaybı bulunur.
4. Optimizasyon algoritması kaybı azaltacak yönde katsayıları günceller.
5. Kayıp ve/veya katsayı değişimleri yeterince küçülünce algoritma durur.

Bu bir “doğru katsayıları formülden doğrudan çekip çıkarma” işlemi değildir. Genellikle sayısal optimizasyondur. Logistic Regression'ın yaygın kayıp fonksiyonu konveks yapıdadır; standart doğrusal ikili Logistic Regression'da L2 cezası da konveksliği korur. Bu, yerel minimumlarda takılma sorununu birçok sinir ağı problemine kıyasla daha yönetilebilir kılar. Ancak veri yapısı ve sayısal koşullar yine önemlidir.

### 4.7. Cross-entropy'nin sigmoid ile birlikte kullanılması neden kullanışlı?

`p = sigmoid(z)` ve cross-entropy birlikte kullanıldığında, `z`'ye göre tek gözlem kaybının türevi çok sadeleşir:

$$\frac{d\ell_i}{dz_i}=p_i-y_i$$

Bunun anlamı sezgiseldir:

- p, y'den büyükse model sınıf 1 olasılığını fazla vermiştir; gradyan pozitiftir.
- p, y'den küçükse model sınıf 1 olasılığını az vermiştir; gradyan negatiftir.
- p=y ise bu ideal uç durumda gradyan sıfırdır.

Ortalama kaybın ağırlıklar bakımından gradyanı:

$$\frac{\partial J}{\partial w_j}=\frac{1}{n}\sum_{i=1}^{n}(p_i-y_i)x_{ij}$$

Bias için:

$$\frac{\partial J}{\partial b}=\frac{1}{n}\sum_{i=1}^{n}(p_i-y_i)$$

Gradyan, kaybın hangi yönde arttığını gösterir. Gradient descent türü bir yöntem, parametreleri gradyanın ters yönünde günceller. Örneğin:

$$w_j^{(k+1)}=w_j^{(k)}-\eta\frac{\partial J}{\partial w_j}$$

Buradaki `learning_rate`, bir güncellemede ne kadar adım atılacağını belirler. Adım çok büyükse minimumun çevresinde sıçrayabilir; çok küçükse öğrenme yavaşlar. `lbfgs` gibi algoritmalar, yalnızca sabit öğrenme oranlı basit gradient descent kullanmak yerine eğriliğe dair yaklaşık bilgiden de yararlanır.

---

## Adım 5 — Gerçek eğitim: katsayıları ve ara sonuçları hesaplayalım

### 5.1. Kullanılan gerçek ayarlar

Aşağıdaki sonuçlar Python'da scikit-learn ile hesaplandı:

```python
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

model = LogisticRegression(
    C=1.0,
    solver="lbfgs",
    max_iter=10000,
    tol=1e-12
)
model.fit(X_scaled, y)
```

scikit-learn sürümü: `1.8.0`. Varsayılan ceza L2'dir. `C=1.0`, regularization gücünün ters ölçek parametresidir; C küçüldükçe ceza genellikle güçlenir, C büyüdükçe zayıflar. `lbfgs`, kaybı sayısal olarak minimize eden optimizasyon algoritmasıdır. `max_iter=10000` üst iterasyon sınırıdır; algoritma bu örnekte 10 iterasyonda yakınsamıştır.

### 5.2. Öğrenilen katsayılar

Model standardize edilmiş özellikler üzerinde şu katsayıları öğrendi:

| Parametre | Öğrenilen değer |
|---|---:|
| `w1` | 0.97355533 |
| `w2` | 0.17341045 |
| `w3` | 0.96429329 |
| `b` | 0.15413836 |

Böylece modelin doğrusal puanı:

`z = 0.97355533*x1_standard + 0.17341045*x2_standard + 0.96429329*x3_standard + 0.15413836`

**Dikkat:** Bu katsayılar standardize edilmiş x sütunları içindir. Ham x değerlerini doğrudan bu denklemde kullanmak yanlış olur. Ham ölçekte denklem istenirse katsayılar standardizasyon dönüşümüne göre ayrıca çevrilmelidir.

Bu veri kümesinde x1 ve x3 pozitif ağırlıklara sahip ve benzer büyüklüktedir; diğer özellikler sabitken artmaları sınıf 1 yönündeki puanı artırır. x2'nin katsayısı daha küçüktür. Bu, bu küçük veri ve bu regularization ayarı altında öğrenilen koşullu ilişkiyi ifade eder; tek başına nedensellik veya evrensel özellik önemi kanıtı değildir.

### 5.3. Eğitim sırasında görülen somut sonuçlar

Modelin eğitim sonunda her gözlem için hesapladığı z, p ve sınıf tahmini:

| Gözlem | Gerçek y | z | p = P(y=1\|x) | Tahmin |
|---:|---:|---:|---:|---:|
| 1 | 0 | -2.569147 | 0.071151 | 0 |
| 2 | 0 | -1.952283 | 0.124305 | 0 |
| 3 | 0 | -1.343680 | 0.206906 | 0 |
| 4 | 0 | -1.710438 | 0.153107 | 0 |
| 5 | 0 | -0.324545 | 0.419569 | 0 |
| 6 | 1 | 0.109860 | 0.527438 | 1 |
| 7 | 1 | 0.871262 | 0.705008 | 1 |
| 8 | 1 | 2.019547 | 0.882834 | 1 |
| 9 | 1 | 2.596517 | 0.930637 | 1 |
| 10 | 1 | 3.844291 | 0.979047 | 1 |

0.5 eşik kuralıyla bu eğitim verisindeki 10 gözlemin tümü doğru sınıflandırıldı. Fakat bu küçük eğitim kümesinde %100 doğruluk görülmesi, modelin yeni veride mutlaka %100 başarılı olacağı anlamına gelmez. Genelleme başarısını değerlendirmek için ayrı doğrulama/test verisi veya uygun çapraz doğrulama gerekir.

### 5.4. Gerçek cross-entropy ve regularization

Bu modelin eğitim olasılıkları üzerinden ortalama binary cross-entropy:

`BCE ≈ 0.23554733`

L2 cezasının bu kurulumdaki normalize edilmiş amaç fonksiyonuna katkısı:

`L2 katkısı = (w1^2 + w2^2 + w3^2)/(2*C*n) ≈ 0.09538714`

Dolayısıyla bu ölçekle yazılan toplam amaç değeri:

`J_regularized ≈ 0.23554733 + 0.09538714 = 0.33093447`

Regularization'ın sebebi, yalnızca eğitim kaybını küçültmek uğruna katsayıların gereğinden fazla büyümesini önlemeye yardımcı olmaktır. Bu, aşırı öğrenme riskini azaltabilir. Burada scikit-learn'ün `C=1.0` ayarı kullanılmıştır; amaç fonksiyonunun yazılım içindeki toplam/ortalama ölçeklendirmesi ve ceza tanımı önemlidir. Yukarıdaki sayılar, aynı normalize edilmiş ölçekle ifade edilmiştir.

### 5.5. Öğrenme süreci hakkında önemli bir nüans

`lbfgs` her adımda basitçe “bir öğrenme oranıyla katsayıya ekleme yap” şeklinde çalışmaz; kayıp fonksiyonunun eğriliğini yaklaşık olarak kullanarak daha gelişmiş parametre adımları seçer. Bu nedenle her iç iterasyondaki bütün ara katsayıları elle verilmiş sabit bir gradient-descent dizisi gibi düşünmemek gerekir. Yukarıdaki nihai katsayılar, belirtilen kodun gerçek sonucudur; iterasyon sayısı 10'dur. Aynı algoritmanın iç ara noktaları sürüm, tolerans ve sayısal ayrıntılara bağlı olabilir.

---

## Adım 6 — Üç gözlem için z, odds, p ve sınıf tahmini

Şimdi öğrenilen gerçek katsayıları kullanarak üç gözlemi baştan hesaplayalım. Bu tabloda x değerleri **standardize edilmiş özelliklerdir**.

Model:

`z = 0.97355533*x1 + 0.17341045*x2 + 0.96429329*x3 + 0.15413836`

Ardından:

`odds = exp(z)`

`p = odds/(1+odds) = 1/(1+exp(-z))`

Karar kuralı: `p >= 0.5` ise sınıf 1, aksi hâlde sınıf 0.

### Gözlem 1 — Eğitim kümesinin ilk satırı

Standardize edilmiş özellikler: `x = (-1.5487, -0.0395, -1.2534)`.

Gerçek modelin tam hassasiyetli hesaplamasından:

- `z ≈ -2.569147`
- `odds = exp(z) ≈ 0.0765`
- `p ≈ 0.071151`
- Tahmin: sınıf 0, çünkü `p < 0.5`.
- Gerçek etiket: `y=0`.

Burada odds 1'den küçüktür; sınıf 1 lehine değil, sınıf 0 lehine kanıt vardır. p yaklaşık %7.1'dir.

### Gözlem 2 — Eğitim kümesinin altıncı satırı

Standardize edilmiş özellikler: `x = (0.1166, -1.3547, 0.0800)`.

Modelin tam hassasiyetli hesaplamasından:

- `z ≈ 0.109860`
- `odds = exp(z) ≈ 1.1161`
- `p ≈ 0.527438`
- Tahmin: sınıf 1, çünkü `p >= 0.5`.
- Gerçek etiket: `y=1`.

Bu karar sınırına yakın bir örnektir: olasılık %52.7 civarındadır. Sınıf 1 tahmini yapılır, ancak modelin güveni çok yüksek değildir. Sınıflandırma kararı ile olasılığın güven düzeyi birbirinden farklı kavramlardır.

### Gözlem 3 — Eğitim kümesinin onuncu satırı

Standardize edilmiş özellikler: `x = (1.7818, 1.9334, 1.6801)`.

Modelin tam hassasiyetli hesaplamasından:

- `z ≈ 3.844291`
- `odds = exp(z) ≈ 46.7`
- `p ≈ 0.979047`
- Tahmin: sınıf 1, çünkü `p >= 0.5`.
- Gerçek etiket: `y=1`.

Odds yaklaşık 46.7 olduğundan modelin tahmininde sınıf 1, sınıf 0'a kıyasla çok daha yüksek olasılığa sahiptir. p yaklaşık %97.9'dur.

### Üç örneğin özeti

| Gözlem | z | odds | p | Tahmin | Gerçek y |
|---:|---:|---:|---:|---:|---:|
| 1 | -2.569147 | 0.0765 | 0.071151 | 0 | 0 |
| 6 | 0.109860 | 1.1161 | 0.527438 | 1 | 1 |
| 10 | 3.844291 | 46.7 | 0.979047 | 1 | 1 |

Tablodaki odds değerleri okunabilirlik için yuvarlanmıştır; z ve p, modelin hesapladığı değerlere dayanır.

---

## Bütün hikâyenin mantıksal zinciri

1. **Veri:** Her satırda üç özellik ve bilinen bir ikili etiket var.
2. **Standardizasyon:** Özellikleri karşılaştırılabilir ölçeğe getiriyoruz; hedef etikete dokunmuyoruz.
3. **Doğrusal puan:** `z = wᵀx+b` ile özelliklerin ağırlıklı birleşimini oluşturuyoruz.
4. **Olasılık modeli:** `z`'yi log-odds olarak yorumluyoruz; buradan sigmoid aracılığıyla p'yi elde ediyoruz.
5. **Kayıp:** Gerçek etiketin model altında aldığı olasılığın negatif logaritmasını cezalandırıyoruz. Tüm gözlemlerin ortalaması binary cross-entropy oluyor.
6. **Optimizasyon:** Kayıp (ve seçilmişse regularization) küçülecek şekilde `w` ve `b` sayısal olarak öğreniliyor.
7. **Tahmin:** Yeni bir gözlemde önce z, sonra p hesaplanıyor; belirlenen eşik ile sınıf kararı veriliyor.
8. **Değerlendirme:** Eğitim verisindeki başarı tek başına yeterli değil; görülmemiş verideki başarı ayrıca ölçülmeli.

Kısacası Logistic Regression, “doğrusal bir puanı sigmoid ile olasılığa dönüştür, gerçek etiketlere verdiğin olasılıklar için negatif log-olabilirliği minimize et” yaklaşımıdır. Sigmoid olasılık modelini, cross-entropy ise bu olasılık modelinin veriye ne kadar uyduğunu ölçen öğrenme hedefini sağlar.

---

# Ek Açıklamalar — Amaç fonksiyonu, konvekslik, L2 ve `lbfgs`

Bu ek, önceki bölümlerdeki optimizasyon ifadelerini parametrelerin açık fonksiyonları olarak gösterir ve kavramlar arasındaki bağı kurar. Denklemler tarayıcıda düzgün işlenebilmesi için tek satırlık `$$ ... $$` biçiminde yazılmıştır.

## Soru 1 — Kayıp fonksiyonu w ve b'nin açık bir fonksiyonu olarak nasıl görünür?

Üç özellikli bir gözlem için önce doğrusal puanı tanımlarız:

$$z_i(w_1,w_2,w_3,b)=w_1x_{i1}+w_2x_{i2}+w_3x_{i3}+b$$

Sigmoid, bu puanı sınıf 1 olasılığına dönüştürür:

$$p_i(w_1,w_2,w_3,b)=\frac{1}{1+e^{-(w_1x_{i1}+w_2x_{i2}+w_3x_{i3}+b)}}$$

Dolayısıyla p_i bağımsız bir değişken değildir; her gözlem için sabit olan x değerlerine ve öğrenilecek w_1,w_2,w_3,b parametrelerine bağlı bir ara çıktıdır. Bunu kayıp fonksiyonuna yerleştirince açık bağımlılık ortaya çıkar:

$$J(w_1,w_2,w_3,b)=-\frac{1}{n}\sum_{i=1}^{n}\left[y_i\log p_i(w_1,w_2,w_3,b)+(1-y_i)\log\left(1-p_i(w_1,w_2,w_3,b)\right)\right]$$

Aynı fonksiyonun sigmoid yerine doğrudan doğrusal puan z_i kullanılarak yazılmış eşdeğer, sayısal açıdan da kullanışlı biçimi şöyledir:

$$J(w_1,w_2,w_3,b)=\frac{1}{n}\sum_{i=1}^{n}\left[\log\left(1+e^{z_i}\right)-y_i z_i\right]$$

Burada z_i, w_1,w_2,w_3,b'nin kısaltmasıdır. Bu eşitlik, fonksiyonun dört parametreli bir yüzey olduğunu söyler. Tek parametre değişkeniyle çizilen grafik bir eğridir; iki parametre için bir yüzeydir; dört parametre için bunu sıradan iki boyutlu bir grafikle bütünüyle çizmek mümkün değildir. Yine de bir parametreyi değiştirip diğerlerini sabit tutarak bir kesit çizilebilir.

Örneğin yalnızca w_1'i değiştirip w_2,w_3,b'yi sabit tutarsak J(w_1) adlı tek değişkenli bir kesit elde ederiz. Konveks bir kesit, aşağıdaki gibi kase biçimindedir:

```text
J(w1)
  ^
  |       *           *
  |         *       *
  |           *   *
  |             *       <- en düşük nokta
  +------------------------> w1
```

Bu çizim şematiktir; gerçek eğrinin simetrik olması veya minimumun w_1=0 noktasında bulunması gerekmez.

### Neden minimum arıyoruz? Minimum mutlaka var mıdır?

Kayıp, modelin gerçek etiketlere verdiği olasılıkların ne kadar uyumlu olduğunu sayısallaştırır. Daha küçük cross-entropy, gözlenen doğru etiketlere genel olarak daha yüksek olasılık verildiğini ifade eder. Eğitim, bu kaybı azaltan parametreleri arar.

Fakat önemli bir matematiksel nüans var: **her veri kümesinde, cezasız Logistic Regression kaybının sonlu parametrelerde minimuma ulaşması garanti değildir.** Eğer iki sınıf doğrusal olarak kusursuz ayrılabiliyorsa, katsayıların büyüklüğü sürekli artırılarak eğitim kaybı sıfıra yaklaşabilir; ama sonlu bir w,b değeri kaybı tam sıfır yapmayabilir. Bu durumda minimum yerine erişilemeyen bir infimum söz konusu olabilir.

Pozitif L2 regularization, ağırlıkların sınırsız büyümesini cezalandırır ve genellikle sonlu, kararlı bir çözümü destekler. Yine de teknik varlık koşulları veri tasarımına, bias'ın cezalandırılıp cezalandırılmamasına ve sınıf dağılımına bağlıdır. Bu yüzden “minimum mutlaka vardır” yerine “bu standart, uygun koşullardaki problemde bir minimum aranır; L2 sonlu ve kararlı çözümü destekler” demek daha doğrudur.

## Soru 2 — Konvekslik, yerel minimum ve L2 cezası

### Konveks ne demektir?

Bir fonksiyonun iki noktası arasındaki doğru parçası fonksiyon grafiğinin altında kalıyorsa fonksiyon konvekstir. Bir değişken için sezgisel şekli kase gibidir. Matematiksel olarak her iki parametre vektörü θ_a ve θ_b ile 0 ≤ t ≤ 1 için şu koşul geçerlidir:

$$J(t\theta_a+(1-t)\theta_b)\le tJ(\theta_a)+(1-t)J(\theta_b)$$

Burada θ = (w_1,w_2,w_3,b). Konvekslik, fonksiyonun her yerde yukarı doğru kıvrılan bir yapıda olduğunu söyler; birden fazla farklı yerel çukurun bulunmasını engeller.

### Logistic Regression'ın kaybı neden konvekstir?

Tek gözlemin kaybını doğrusal puan üzerinden yazalım:

$$\ell_i(z_i)=\log(1+e^{z_i})-y_i z_i$$

z'ye göre birinci türev:

$$\frac{d\ell_i}{dz_i}=\sigma(z_i)-y_i=p_i-y_i$$

İkinci türev:

$$\frac{d^2\ell_i}{dz_i^2}=p_i(1-p_i)\ge 0$$

Çünkü sigmoid çıktısı 0 ile 1 arasındadır; bu yüzden p_i(1-p_i) negatif olamaz. İkinci türevin negatif olmaması, tek gözlem kaybının z bakımından konveks olduğunu gösterir.

z_i, parametrelerin doğrusal fonksiyonudur. Bu nedenle bütün gözlemlerin kayıplarını toplamak ve pozitif n sayısına bölmek konveksliği bozmaz. Matris biçiminde ortalama kaybın Hessian matrisi şöyledir:

$$\nabla^2 J(\theta)=\frac{1}{n}X^T R X$$

Burada X, özellik matrisi (bias için gerekirse birler sütunu eklenmiş tasarım matrisi); R ise köşegeninde p_i(1-p_i) bulunan köşegen matristir. Herhangi bir v vektörü için:

$$v^T X^T R Xv=(Xv)^T R(Xv)\ge 0$$

çünkü R'nin köşegen elemanları negatif değildir. Dolayısıyla Hessian pozitif yarı tanımlıdır ve amaç fonksiyonu konvekstir. Bazı verilerde bu matris pozitif tanımlı olmayabilir; bu durumda minimum yine bulunabilir ama parametre çözümü tek olmayabilir veya bazı yönlerde eğrilik çok zayıf olabilir.

### “Yerel minimumda takılmak” ne demektir?

Yerel minimum, yalnızca yakın çevresindeki noktalardan daha düşük kayba sahip noktadır. Global minimum ise tüm parametre uzayındaki en düşük değerdir. Konveks bir fonksiyonda her yerel minimum aynı zamanda global minimumdur. Bu nedenle klasik doğrusal ikili Logistic Regression'da sinir ağlarında sık görülen çok sayıda farklı yerel çukur sorunu tipik olarak yoktur.

```text
Konveks:                 Konveks olmayan örnek:
J                        J
^       __               ^    _      __
|     /    \             | __/  \____/  \__
|____/      \___         |       ^       ^
+-------------> θ        +------------------> θ
       tek çukur                  farklı yerel çukurlar
```

Şekiller şematiktir. Konveks olmayan fonksiyonda bir algoritma, bulunduğu çukurun yakınında gradyanı sıfıra yaklaştırıp daha iyi bir başka çukura ulaşamayabilir. Konveks fonksiyonda bu tür farklı kalitede yerel minimumlar yoktur. Bununla birlikte kötü ölçeklenme, sayısal hassasiyet, çok düz bölgeler veya durdurma toleransı optimizasyonu yine zorlaştırabilir.

### L2 cezası nedir ve neden konveksliği korur?

L2 regularization, ağırlıkların kareleri toplamını amaç fonksiyonuna ekler. Bu dokümandaki ortalama-kayıp ölçeğinde:

$$J_{reg}(w,b)=J(w,b)+\frac{1}{2Cn}\sum_{j=1}^{3}w_j^2$$

b terimi burada cezaya dahil edilmemiştir; scikit-learn LogisticRegression'ın yaygın L2 düzenlileştirme tanımında intercept genellikle bu ağırlık cezasına dahil edilmez. Katsayı kareleri negatif olamaz ve büyük mutlak katsayılar daha büyük ceza üretir.

Tek bir ağırlık için w_j^2 fonksiyonunun ikinci türevi 2'dir; dolayısıyla kare fonksiyonu konvekstir. Pozitif bir sabitle çarpmak ve konveks J'ye eklemek konveksliği korur. λ = 1/(Cn) dersek cezanın Hessian'ı ağırlıklar bakımından λI'dir; bu matris pozitif yarı tanımlıdır. Böylece toplam Hessian, iki pozitif yarı tanımlı matrisin toplamıdır ve yine pozitif yarı tanımlıdır.

L2 cezası katsayıları sıfıra doğru küçültmeye teşvik eder; katsayıların mutlaka sıfır olmasını sağlamaz. Amaç, yalnızca eğitim verisini açıklamak için aşırı büyük katsayılara ihtiyaç duyan çözümleri pahalılaştırmak ve genelleme performansına yardımcı olmaktır. L2 her zaman test başarısını artırmayı garanti etmez; bunun için validation/test ölçümü gerekir.

## Soru 3 — `C` parametresi neyi kontrol eder?

Bu dosyada kullanılan yazımda L2 katkısı:

$$J_{L2}=\frac{w_1^2+w_2^2+w_3^2}{2Cn}$$

C, regularization gücüyle ters ilişkili bir parametredir:

- Küçük C → ceza katsayısı 1/(2Cn) büyür → büyük ağırlıklar daha pahalı olur → daha güçlü regularization.
- Büyük C → ceza katsayısı küçülür → ağırlıklara daha az ceza verilir → daha zayıf regularization.
- C → sonsuz olduğunda ceza katkısı sıfıra yaklaşır; model cezasız Logistic Regression'a yaklaşır.

Sayısal örnek: aynı w ve aynı n sabitken C=0.5 kullanılırsa, C=1'e göre ceza iki katına çıkar. C=2 kullanılırsa ceza yarıya iner. Bu karşılaştırma yalnızca ceza teriminin katsayısını anlatır; model yeniden eğitilince w değerleri de değişeceği için gerçek toplam kayıp tam olarak bu oranla değişmek zorunda değildir.

Buradaki önemli ayrım: C doğrudan bir ağırlık değildir; optimizasyon sırasında hangi ağırlık büyüklüklerinin ne kadar cezalandırılacağını belirleyen hiperparametredir. Veri ölçekleri değişirse regularization'ın etkisi de değişebileceğinden standardizasyon çoğu zaman önemlidir.

## Soru 4 — `lbfgs` nedir? Gradient descent'ten farkı ne?

`lbfgs`, “Limited-memory Broyden–Fletcher–Goldfarb–Shanno” ifadesinin kısaltmasıdır. Türev bilgisi kullanan, quasi-Newton (yaklaşık Newton) türü bir optimizasyon yöntemidir. Buradaki “limited-memory”, tam Hessian matrisini saklamak yerine son adımlardaki parametre ve gradyan değişimlerinden eğrilik hakkında sınırlı miktarda bilgi tutmasını anlatır.

Basit gradient descent güncellemesi:

$$\theta_{k+1}=\theta_k-\eta_k\nabla J(\theta_k)$$

Burada η adım büyüklüğüdür. Yalnızca gradyan yönünü kullanır; adım büyüklüğü seçimi çok önemlidir. Adım aşırı büyükse hedefin iki yanına sıçrayabilir; çok küçükse yavaş ilerler.

Newton yöntemi, gradyanın yanında Hessian'ın eğrilik bilgisini de kullanır:

$$\theta_{k+1}=\theta_k-[\nabla^2J(\theta_k)]^{-1}\nabla J(\theta_k)$$

Tam Hessian'ı hesaplayıp tersini almak yüksek boyutlu problemlerde pahalı olabilir. L-BFGS, Hessian veya ters Hessian'ı açıkça saklamak yerine, yakın geçmişteki gradyan/parametre değişimlerinden ters Hessian etkisini yaklaşıklar. Sonra bu yaklaşık eğrilik bilgisini kullanarak bir arama yönü belirler ve genellikle line search ile uygun adım boyunu seçer.

Özetle L-BFGS, “her seferinde sabit learning rate ile yalnızca gradyanın tersine gitmek” değildir. Gradyan + geçmiş adımlardan çıkarılan eğrilik bilgisi + adım araması kullanır. Bu nedenle çoğu küçük/orta ölçekli Logistic Regression probleminde hızlı yakınsayabilir. Fakat her veri kümesinde en iyi solver olacağı garanti değildir; scikit-learn'de `max_iter`, `tol`, veri ölçeği ve solver seçimi sonucu etkiler.

## Soru 5 — “Amaç değeri” ne demektir?

Amaç fonksiyonu, optimizasyon algoritmasının küçültmeye (veya başka problemlerde büyütmeye) çalıştığı sayısal ölçüttür. Bu örnekte amaç fonksiyonu, ortalama binary cross-entropy ile L2 cezasının toplamıdır:

$$J_{reg}(w,b)=J_{BCE}(w,b)+J_{L2}(w)$$

Verilen katsayılar için dosyada raporlanan değerler:

$$J_{BCE}\approx 0.23554733$$

$$J_{L2}\approx 0.09538714$$

$$J_{reg}\approx 0.23554733+0.09538714=0.33093447$$

0.33093447, bu parametreler ve bu ölçeklendirme için amaç fonksiyonunun aldığı tek bir sayıdır. Algoritma, farklı w,b adaylarında bu sayıyı hesaplayıp azaltmaya çalışır. Bu değer doğrudan “%33 başarı” veya “%33 hata” demek değildir; olasılık kalitesi ve ceza teriminin birleşiminden oluşan bir optimizasyon ölçüsüdür. Modelleri karşılaştırırken aynı kayıp tanımı ve aynı ölçeklendirme kullanılmalıdır.

Bir yazılımın kullandığı amaç fonksiyonunun toplam mı ortalama mı olduğu ve ceza terimini hangi ölçekte eklediği önemlidir. Bu nedenle yukarıdaki sayılar, dosyada açıkça belirtilen normalize edilmiş formülün açıklamasıdır; scikit-learn'ün iç uygulamasındaki ölçeklendirmeyle bire bir eşdeğerlik iddiası, kullanılan sürümün tanımı kontrol edilmeden yapılmamalıdır.

## Soru 6 — Türev ve gradyan denklemlerinin matematiksel yazımı

Aşağıdaki ifadeler, metin olarak yazılmış türev denklemlerinin matematiksel gösterimidir. Burada n gözlem sayısı, x_ij i'inci gözlemin j'inci özelliği, p_i modelin sınıf 1 olasılığı ve y_i gerçek etikettir.

Tek gözlemin kaybının doğrusal puana göre türevi:

$$\frac{\partial \ell_i}{\partial z_i}=p_i-y_i$$

Ortalama kaybın j'inci ağırlığa göre kısmi türevi:

$$\frac{\partial J}{\partial w_j}=\frac{1}{n}\sum_{i=1}^{n}(p_i-y_i)x_{ij}$$

Bias/intercept için türev:

$$\frac{\partial J}{\partial b}=\frac{1}{n}\sum_{i=1}^{n}(p_i-y_i)$$

Ağırlık vektörünün gradyanı, tüm ağırlık türevlerinin vektörüdür:

$$\nabla_w J=\frac{1}{n}X^T(p-y)$$

Bias ile birlikte parametre vektörü θ=(w,b) olarak tanımlanırsa tam gradyan, ağırlık gradyanı ile bias türevini bir araya getirir:

$$\nabla_\theta J=\begin{bmatrix}\frac{1}{n}X^T(p-y)\\[3pt]\frac{1}{n}\sum_{i=1}^{n}(p_i-y_i)\end{bmatrix}$$

Basit gradient descent güncellemesi:

$$w_j^{(k+1)}=w_j^{(k)}-\eta\frac{\partial J}{\partial w_j}$$

Vektör biçiminde:

$$w^{(k+1)}=w^{(k)}-\eta\nabla_w J$$

L2 terimi bu dokümandaki ölçekle eklendiğinde j'inci ağırlığa eklenen ceza türevi:

$$\frac{\partial J_{L2}}{\partial w_j}=\frac{w_j}{Cn}$$

Dolayısıyla düzenlileştirilmiş amaç fonksiyonunun ağırlık gradyanı:

$$\nabla_w J_{reg}=\frac{1}{n}X^T(p-y)+\frac{1}{Cn}w$$

Bu ek gradyan terimi büyük ağırlıkları sıfıra doğru çeken bir katkı yapar. Bias ceza terimine dahil edilmediğinden onun gradyanı bu yazımda değişmez.

> **Notasyon uyarısı:** `∂J/∂w_j` bir skaler kısmi türevdir; `∇_w J` ise bütün ağırlıklara göre türevleri bir araya getiren vektördür. Bu iki gösterim aynı bilgiyi farklı boyutlarda sunar.
