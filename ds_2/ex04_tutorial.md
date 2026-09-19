# ex04 — Elbow ve K-Means: matematiksel bir okuma

Bu not, [`ex04/elbow.py`](ex04/elbow.py) dosyasındaki akışı açıklar. Kodun SQL kısmı her `user_id` için üç RFM değişkenini üretir:

- **Recency (R):** 1 Mart 2023'e göre son satın alımdan beri geçen gün sayısı. Küçük olması müşterinin yakın zamanda alışveriş yaptığını gösterir.
- **Frequency (F):** 1 Ekim 2022–1 Mart 2023 aralığındaki satın alma sayısı.
- **Monetary (M):** aynı aralıktaki toplam harcama (`sum(price)`).

K-Means'e `user_id` verilmez; o bir tanımlayıcıdır, müşterilerin benzerliği hakkında sayısal bir eksen değildir. Modele sadece `(R, F, M)` verilir.

## Ortak örnek: 10 müşterilik küçük RFM evreni

110.000 satırı her aşamada görmek yerine, bütün cevaplarda aşağıdaki aynı 10 müşteriyi izleyeceğiz. Parasal değerler Altairian Dollars olsun. Bu örnek bilinçli olarak yeni/aktif/değerli müşterilerden eski/pasif müşterilere doğru sıralanmıştır; gerçek veride noktalar genellikle bunun kadar düzenli değildir.

| Müşteri | R (gün) | F (satın alma) | M (harcama) |
|---|---:|---:|---:|
| M01 | 2 | 12 | 1200 |
| M02 | 5 | 10 | 1050 |
| M03 | 9 | 8 | 900 |
| M04 | 18 | 7 | 720 |
| M05 | 27 | 5 | 550 |
| M06 | 42 | 4 | 380 |
| M07 | 58 | 3 | 260 |
| M08 | 75 | 2 | 150 |
| M09 | 91 | 1 | 95 |
| M10 | 120 | 1 | 60 |

Her müşteri, üç-boyutlu uzayda bir noktadır: örneğin M01, `x_1 = (2, 12, 1200)` noktasıdır. Gerçek projede bu nokta bulutu yaklaşık 110.000 noktadan oluşur.

> **Önemli sınır:** Bu veri öğretim amacıyla seçilmiştir. Aşağıdaki sayısal standardizasyon sonuçları bu 10 satıra aittir; sizin 110.000 satırlık verinizde ortalama, standart sapma, inertia ve nihai kümeler farklı olacaktır.

## 1) Soru: `sklearn` nedir; açılımı ve kullanım alanları nelerdir?

`sklearn`, Python'da içe aktarma adı olan **scikit-learn** kütüphanesidir. “sklearn” resmî bir harf-kısaltması değildir. Adın kökeni şöyledir:

- `sci` = science (bilim),
- `kit` = araç takımı; başlangıçta SciPy çevresindeki bilimsel araç takımlarından (*scikits*) biri,
- `learn` = machine learning (makine öğrenmesi).

Yani pratikte `sklearn`, **scikit-learn** demektir. NumPy/SciPy/Matplotlib ekosistemi üzerine kurulmuş, açık kaynak bir makine öğrenmesi kütüphanesidir. Resmî dokümantasyonun güzel tarafı, algoritmaları ortak bir arayüzle sunmasıdır: çoğu modelde önce nesneyi kurar, `fit(...)` ile veriden parametreleri öğrenir, sonra `predict(...)`, `transform(...)` veya özniteliklerine erişiriz.

Başlıca kullanım aileleri ve küçük örnekleri:

| İş | Soru tipi | Örnek sklearn aracı |
|---|---|---|
| Regresyon | Sayısal sonuç tahmini | `LinearRegression` — ev fiyatı / harcama tahmini |
| Sınıflandırma | Bilinen etiket seçimi | `LogisticRegression` — müşteri churn eder mi? |
| Kümeleme | Etiket yokken benzer grupları bulma | `KMeans` — RFM müşteri segmentleri |
| Ön işleme | Veriyi model için dönüştürme | `StandardScaler`, `OneHotEncoder`, `SimpleImputer` |
| Değerlendirme/seçim | Modeli sınama ve ayarlama | `train_test_split`, `cross_val_score` |

Örnekler:

```python
from sklearn.linear_model import LinearRegression

# Etiketli (supervised) örnek: metrekareden fiyat öğrenmek
X = [[60], [80], [100]]
y = [2_000_000, 2_600_000, 3_300_000]
model = LinearRegression().fit(X, y)
print(model.predict([[90]]))
```

```python
from sklearn.cluster import KMeans

# Etiketsiz (unsupervised) örnek: müşterileri RFM benzerliğine göre ayırmak
X = [[2, 12, 1200], [120, 1, 60], [9, 8, 900]]
labels = KMeans(n_clusters=2, random_state=42, n_init=10).fit_predict(X)
```

İkinci örnekte `y` yoktur: algoritmaya “M01 sadık müşteri”, “M10 pasif müşteri” diye doğru cevap verilmez. K-Means yalnızca seçilen sayısal uzaydaki yakınlık yapısından gruplar çıkarır. Bu yüzden bu proje **denetimsiz (unsupervised) makine öğrenmesi**dir.

Resmî başlangıç sayfası, kütüphanenin supervised ve unsupervised öğrenmenin yanında ön işleme, model seçimi ve değerlendirme araçları sağladığını belirtir. [scikit-learn ana sayfası](https://scikit-learn.org/stable/) ve [SSS: isim ve “scikit” kökeni](https://scikit-learn.org/stable/faq.html) iyi başlangıç kaynaklarıdır.

## 2) Soru: Olası centroid kombinasyonları deneniyor mu; K-Means neden hızlı, normalizasyon ve sınıfların iş bölümü nedir?

Kısa cevap: **Hayır, `KMeans` 110.000 müşteriden seçilebilecek bütün 4'lü başlangıçları denemez.**

### Problem gerçekten ne kadar zor?

`n = 110000`, `k = 4` ise yalnız “centroidleri verideki dört müşteri arasından seçelim” varsayımında bile aday başlangıç sayısı

$$
\binom{110000}{4}
= \frac{110000\cdot109999\cdot109998\cdot109997}{24}
\approx 6.1\times10^{18}
$$

olur. Bu zaten uygulanamazdır. Üstelik gerçek optimumda centroidlerin veri noktası olması gerekmez: bir kümenin aritmetik ortalamasıdır ve sürekli uzayda bulunabilir. Olası küme atamalarını düşünmek daha da büyük, kombinatoryal bir problemdir. Genel K-Means amaç fonksiyonunun küresel optimumunu bulma problemi zordur (pratikte NP-zor olarak bilinir).

K-Means'in çözmek istediği problem şudur. `x_i ∈ R^d` müşteri noktaları, `C_1, …, C_k` kümeler ve `μ_j` onların centroidleri olsun:

$$
\underset{C_1,\ldots,C_k,\;\mu_1,\ldots,\mu_k}{\operatorname{minimize}}
\quad
J = \sum_{j=1}^{k}\sum_{x_i\in C_j}\lVert x_i-\mu_j\rVert_2^2.
$$

Bu `J`, kodunuzdaki **inertia** veya **WCSS**'dir (*within-cluster sum of squares*). Her müşterinin, atandığı centroid'e olan kareli Öklid uzaklığını toplar. Küçük `J`, kümelerin kendi içlerinde daha sıkı olduğu anlamına gelir.

### Brute force yerine Lloyd/K-Means döngüsü

`KMeans.fit(X_scaled)` tipik olarak şu iki adımı dönüşümlü çalıştırır:

1. **Atama adımı:** centroidler sabitse, her `x_i` en yakın centroid'e atanır:

   $$a_i = \arg\min_j\lVert x_i-\mu_j\rVert_2^2.$$

2. **Güncelleme adımı:** üyeler sabitse, `J`'yi en aza indiren centroid o kümedeki noktaların ortalamasıdır:

   $$\mu_j = \frac{1}{|C_j|}\sum_{x_i\in C_j}x_i.$$

İkinci ifadenin neden ortalama olduğunu türevle görebiliriz. Tek bir küme için

$$
f(\mu)=\sum_{x_i\in C}\lVert x_i-\mu\rVert^2
\quad\Rightarrow\quad
\nabla_\mu f=2|C|\mu-2\sum_{x_i\in C}x_i=0,
$$

dolayısıyla `μ = ortalama(C)`; Hessian `2|C|I` pozitif tanımlıdır. Yani **atamalar sabitken** bu adım küresel optimumdur. Aynı şekilde centroidler sabitken en yakına atamak da optimumdur. Fakat ikisini birden serbest bırakınca problem konveks değildir; döngü her turda `J`'yi azaltır ya da aynı bırakır, sonlu sayıda atama nedeniyle durur, ama yalnızca bir **yerel optimuma** ulaşabilir.

Bu, linear regression ile önemli farktır. Olağan en küçük kareler linear regression'da amaç fonksiyonu katsayılarda konvekstir ve normal denklemlerle küresel optimum elde edilir (tekillik yoksa benzersizdir). K-Means'de hem gizli/discrete atamalar hem centroidler bilinmez; `fit` bir tahmin–iyileştirme prosedürüdür, regresyondaki kapalı form çözüm değildir.

### Başlangıç “rastgele” mi?

Varsayılan `init='k-means++'` ile tamamen gelişigüzel değildir:

1. İlk merkez veri noktalarından rastgele seçilir.
2. Sonraki adayların seçilme olasılığı, en yakın seçilmiş merkeze olan **kareli uzaklıkları** ile artar.
3. Böylece birbirinden uzak başlangıç merkezleri tercih edilir; boşuna aynı yoğun bölgeye dört merkez koyma ihtimali azalır.

scikit-learn, bunu açgözlü (*greedy*) bir k-means++ çeşidi olarak uygular: her merkez adımında birkaç aday dener ve inertia azalması en iyi olan adayı seçer. Yine de rastlantı vardır. Kodunuzdaki `n_init=10`, farklı başlangıçlarla **10 bağımsız yerel arama** yapar ve o sabit `k` için inertia'sı en küçük olan sonucu saklar. Bu, bütün kombinasyonları denemek değildir ve küresel optimum garantisi de vermez; iyi bir pratik sağlamlık önlemidir.

`random_state=42` rastlantıyı kaldırmaz, onu **tekrar üretilebilir** yapar: aynı veri, aynı scikit-learn sürümü ve aynı parametrelerde tekrar çalıştırınca aynı pseudo-rastgele başlangıç dizisini alırsınız. `42` özel ya da daha iyi bir sayı değildir.

### 10 müşterilik örnekte döngünün zihinsel resmi

Önce 3. ve 4. cevaplardaki standardize edilmiş uzayda dört başlangıç merkezi seçildiğini varsayalım. Atama adımından sonra örneğin şu bölünme oluşabilir:

| Geçici küme | Üyeler | Ham uzaydaki yeni centroid `(R, F, M)` |
|---|---|---|
| A | M01, M02, M03 | `(5.33, 10.00, 1050.00)` |
| B | M04, M05 | `(22.50, 6.00, 635.00)` |
| C | M06, M07 | `(50.00, 3.50, 320.00)` |
| D | M08, M09, M10 | `(95.33, 1.33, 101.67)` |

Örneğin A'nın recency centroid'i `(2+5+9)/3 = 5.33`'tür. Sonraki atama turunda her müşteri A–D'nin **standardize edilmiş** centroidlerine uzaklıklarına göre tekrar değerlendirilir; üyelik değişirse bu ortalamalar yeniden hesaplanır. Hiçbir atama değişmeyince sonuç sabitlenir. Gerçek `fit`'te cluster numaraları (`0,1,2,3`) A–D anlamına gelmez ve çalışmadan çalışmaya yer değiştirebilir; anlamı, her kümenin RFM özetiyle sonradan veririz.

### Neden 110.000 × 10 değer makul sürede çalışır?

Bir Lloyd turunun baskın işi her noktanın `k` merkezden her birine `d` boyutta uzaklığını hesaplamaktır: yaklaşık `O(nkd)`. `t` iterasyon ve `r=n_init` tekrar için `O(rtnkd)` düşünülür. Sizin durumda `d=3`, `k≤10`, `r=10` ve `t` pratikte çoğunlukla `max_iter=300` sınırından epey küçüktür. Ayrıca uzaklık hesapları Python'da tek tek döngüyle değil, derlenmiş/vektörleştirilmiş sayısal kodla yapılır.

Elbow döngüsünde `k=1+...+10=55` olduğundan kaba toplam maliyet `O(10 × t × 110000 × 55 × 3)` ölçeğindedir. Bu kayda değer bir hesap olsa da `\binom{110000}{4}` denemesinden astronomik derecede küçüktür. Çok daha büyük veri için `MiniBatchKMeans` de kullanılabilir; burada 110 bin × 3 veri için normal `KMeans` makul bir başlangıçtır.

### Normalizasyon ve kodunuzdaki iş bölümü

Normalizasyon **inertia hesaplandıktan sonra** yapılmaz. Önce bir kez yapılır; her `k` için K-Means ve inertia aynı ölçekli `X_scaled` üzerinde çalışır. `k` büyüdükçe inertia zorunlu olarak düşer; bu nedenle “k=1..10 arasında inertia'sı en küçük olanı seçelim” mantığı yanlıştır. `k=110000` seçilse her nokta kendi kümesi olur ve inertia `0` olurdu. `n_init=10` içindeki adaylar arasında en küçük inertia seçilir; farklı `k` değerleri arasında elbow ile **azalan marjinal kazanç** aranır.

| Kod parçası | Sorumluluğu | Bu aşamada veri |
|---|---|---|
| `StandardScaler()` | Boş bir dönüştürücü nesnesi kurar; henüz veri istatistiği hesaplamaz. | Henüz yok |
| `scaler.fit_transform(rfm_sütunları)` | Ortalama/standart sapmayı veriden öğrenir (**fit**) ve her değeri z-skoruna çevirir (**transform**). | `X_scaled`: 110.000 × 3 |
| `KMeans(n_clusters=k, ...)` | `k` merkezli bir K-Means model nesnesi ve ayarlarını kurar; henüz küme yoktur. | Henüz yok |
| `kmeans.fit(X_scaled)` | k-means++ başlatma + atama/güncelleme döngüsünü `n_init` kez yürütür; en iyi sonucu modelde saklar. | `labels_`, `cluster_centers_`, `inertia_` |

K-Means ve inertia'nın tanımı için resmî [KMeans API sayfasına](https://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html), algoritmanın ayrıntıları için [clustering kılavuzuna](https://scikit-learn.org/stable/modules/clustering.html#k-means) bakılabilir.

## 3) Soru: `StandardScaler()` tam olarak ne yapar, neden gerekli?

`StandardScaler()` bir **dönüştürme nesnesi oluşturur**. Varsayılan ayarları `copy=True`, `with_mean=True`, `with_std=True`'dir. Veri henüz bu satırda değişmez; nesne, daha sonra `fit` ile her sütun için ortalama ve standart sapmayı saklayacak bir “kalıp”tır.

Varsayılan dönüşüm her özellik/sütun için şudur:

$$
z_{ij}=\frac{x_{ij}-\bar{x}_j}{s_j},
\qquad
s_j=\sqrt{\frac{1}{n}\sum_{i=1}^{n}(x_{ij}-\bar{x}_j)^2}.
$$

Burada `j`, R/F/M sütununu ifade eder. scikit-learn `StandardScaler` bu hesapta `ddof=0` ile, yani paydada `n` olan nüfus standart sapmasını kullanır. Dönüşüm sonrası her sıfır-varyanslı olmayan sütunun eğitim verisindeki ortalaması yaklaşık `0`, varyansı `1` olur.

### Aynı 10 müşteriye uygulanışı

Yukarıdaki ham tablonun sütun istatistikleri:

| Sütun | Ortalama `x̄` | Varyans | Standart sapma `s` |
|---|---:|---:|---:|
| Recency | 44.70 | 1461.61 | 38.23 |
| Frequency | 5.30 | 13.21 | 3.63 |
| Monetary | 536.50 | 154220.25 | 392.71 |

Örneğin M01'in recency değeri `2` olduğundan:

$$z_R=(2-44.7)/38.23\approx -1.117.$$

M01'in frequency ve monetary z-skorları sırasıyla yaklaşık `1.843` ve `1.690` olur. Bütün veri dönüşünce:

| Müşteri | `z(R)` | `z(F)` | `z(M)` |
|---|---:|---:|---:|
| M01 | -1.117 | 1.843 | 1.690 |
| M02 | -1.038 | 1.293 | 1.308 |
| M03 | -0.934 | 0.743 | 0.926 |
| M04 | -0.698 | 0.468 | 0.467 |
| M05 | -0.463 | -0.083 | 0.034 |
| M06 | -0.071 | -0.358 | -0.399 |
| M07 | 0.348 | -0.633 | -0.704 |
| M08 | 0.793 | -0.908 | -0.984 |
| M09 | 1.211 | -1.183 | -1.124 |
| M10 | 1.970 | -1.183 | -1.213 |

### Neden gerekli?

K-Means kareli Öklid uzaklığı kullandığı için ölçeğe duyarlıdır. Ham bir uzaklıkta örneğin iki müşteri arasındaki farklar şu biçimde toplanır:

$$d^2=(\Delta R)^2+(\Delta F)^2+(\Delta M)^2.$$

`M` yüzler/binler, `F` ise tek haneler seviyesindedir. Dolayısıyla ham kullanımda `ΔM²` neredeyse bütün mesafeyi domine eder; model, “müşteri benzerliği” yerine çoğunlukla yalnız toplam harcamayı kümeler. Bu matematiksel olarak bir hata değildir; harcamaya bilinçli olarak çok daha yüksek ağırlık vermek istiyorsanız istenen davranış olabilir. Fakat R, F ve M'nin segment kararına yaklaşık eşit ölçekli katkı vermesini istiyorsak standardizasyon gerekir.

Standardizasyon şunu ifade eder: “Bu üç değişkende **bir standart sapmalık** farkın kümelenmede benzer ağırlığı olsun.” Değişkenleri aynı birime çevirmek değil, uzaklık fonksiyonundaki örtük ağırlıkları dengelemektir.

İki dikkat noktası:

- `StandardScaler`, veriyi normal dağılıma dönüştürmez; sadece merkezler ve ölçekler. RFM'de monetary/frequency çoğu zaman sağa çarpık ve aykırı değerlidir. Çok uç harcamalar varsa önce `log1p` veya `RobustScaler` düşünmek analiz tercihidir.
- Sıfır varyanslı bir sütun (her müşteride aynı değer) ayırt edici bilgi taşımaz. Scaler bölme hatası vermemek için ölçeği güvenli biçimde ele alır, ama böyle bir sütunu modelden çıkarmak genellikle daha anlamlıdır.

Resmî [StandardScaler dokümantasyonu](https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.StandardScaler.html), formülü ve aykırı değerlere duyarlılık uyarısını içerir.

## 4) Soru: `scaler.fit_transform()` nedir; parametreleri nelerdir ve neden kullanılır?

Kodunuzdaki satır:

```python
X_scaled = scaler.fit_transform(
    df_rfm[["recency", "frequency", "monetary"]]
)
```

iki işlemi tek çağrıda yapar:

```python
scaler.fit(X_train)       # sütun başına mean_, var_, scale_ öğrenir
X_scaled = scaler.transform(X_train)  # (X - mean_) / scale_ uygular
```

`fit_transform(X, y=None, **fit_params)`, genel sklearn transformer arayüzüdür. Bu `StandardScaler` için önemli girdiler şöyledir:

| Öğe | Anlamı |
|---|---|
| `X` | Dönüştürülecek özellik matrisi. Burada DataFrame'in 3 sayısal sütunu, şekli `(110000, 3)` civarındadır. |
| `y=None` | Denetimli problemlerdeki hedef/etiket için ortak API parametresi. StandardScaler denetimsizdir; `y` kullanmaz. |
| `**fit_params` | Genel arayüzün ek ayarları. Bu basit çağrıda verilmiyor. |
| Dönüş değeri | Dönüştürülmüş matris; tipik olarak NumPy `ndarray`. Sütun adları bu diziye taşınmaz. |

`fit_transform`'ın ayrı kurucu parametreleri yoktur; davranışı `StandardScaler(...)` kurarken belirlenen `copy`, `with_mean`, `with_std` parametrelerinden gelir. Tek çağrı hem daha okunaklı hem bazı transformer'larda `fit` ardından `transform` çağırmaktan daha verimli olabilir.

Örnek veri üzerinde elde edilen `mean_`, `var_`, `scale_` değerleri 3. cevaptaki tablodur. Çağrıdan sonra kavramsal olarak:

```python
scaler.mean_   # array([44.7, 5.3, 536.5])
scaler.var_    # array([1461.61, 13.21, 154220.25])
scaler.scale_  # array([38.23, 3.63, 392.71])
X_scaled[0]    # array([-1.117, 1.843, 1.690])  # M01
```

Bu proje keşif/segmentasyon çalışması olduğu için bütün mevcut müşteri verisi üzerinde `fit_transform` normaldir. Ancak daha sonra eğitim verisiyle bir model kurup ayrı test ya da yeni müşteri verisini değerlendiren bir supervised senaryoda doğru desen şudur:

```python
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)  # istatistikleri yalnız train'den öğren
X_test_scaled = scaler.transform(X_test)        # test'e aynı dönüşümü uygula
X_new_scaled = scaler.transform(X_new_customer) # yeni müşteriye de aynı dönüşüm
```

Test/yeni veriye tekrar `fit_transform` yapmak, onların ortalama ve sapmasını modele sızdırır; ayrıca yeni müşteriyi eski müşterilerle aynı geometri içinde kıyaslamamış olursunuz. `transform`, önceden öğrenilmiş `mean_` ve `scale_` değerlerini kullanır; kritik ayrım budur.

## 5) Soru: `KMeans(...)`, `fit(X_scaled)` ve parametreleri ne yapar?

Kod:

```python
kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
kmeans.fit(X_scaled)
```

İlk satır modeli **oluşturur ve yapılandırır**; henüz hiçbir müşteri kümelenmemiştir. İkinci satır 2. cevapta anlatılan optimizasyonu gerçekten çalıştırır.

| Parametre | Kodunuzdaki değer | Etkisi |
|---|---:|---|
| `n_clusters` | döngüdeki `k` (`1..10`) | Kaç centroid/küme aranacağını sabitler. K-Means bunu kendisi keşfetmez. |
| `random_state` | `42` | Başlangıçtaki pseudo-rastgeleliği sabitler; sonuçların tekrarlanmasına yardım eder. |
| `n_init` | `10` | Farklı başlangıçlarla algoritmayı 10 kez çalıştırır; bu `k` için en küçük inertia sonucunu tutar. |
| `init` | belirtilmedi; varsayılan `k-means++` | Başlangıç merkezlerini birbirinden ayrık seçmeye çalışan yöntem. |
| `max_iter` | belirtilmedi; varsayılan `300` | Bir tek başlangıç çalışmasının üst iterasyon sınırı. |
| `tol` | belirtilmedi; varsayılan `1e-4` | Merkez değişimi yeterince küçükse yakınsama kabul edilir. |

`fit(X_scaled)` sonrasında faydalı model öznitelikleri şunlardır:

```python
kmeans.cluster_centers_  # şekil (k, 3): standardize uzaydaki centroidler
kmeans.labels_           # şekil (n_samples,): her müşterinin 0..k-1 etiketi
kmeans.inertia_          # seçilen en iyi başlatmanın WCSS değeri
kmeans.n_iter_           # seçilen çalışmanın kaç iterasyon sürdüğü
```

`labels_`deki `0`, `1`, `2`, `3` değerleri ordinal değildir: “3 numaralı küme 2'den daha iyi” gibi bir anlam taşımaz. ex05'te kümeyi anlamlandırmak için her etiketin **ham RFM ortalamasını/medyanını ve müşteri sayısını** çıkarmak gerekir. Örneğin ortalama R küçük, F ve M büyük olan küme “sadık/yüksek değer”; R büyük, F ve M küçük olan küme “pasif/geri kazanılacak” diye adlandırılabilir.

Bu kodun elbow döngüsündeki tam zamanı:

```python
inertias = []
for k in range(1, 11):
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    kmeans.fit(X_scaled)
    inertias.append(kmeans.inertia_)
```

Her tur bağımsız yeni bir modeldir. `k=4` çalışması `k=3`ün merkezlerini devralmaz; ikisi aynı standardize edilmiş müşteri noktalarına ayrı ayrı uygulanır. `inertias` sonunda 10 sayılık bir liste olur ve grafik bu listeyi çizer.

## 6) Soru: Grafikte elbow `k=3` gibi; ex05 neden en az 4 grup istiyor, ex04 boşa mı yapıldı?

Hayır, elbow boşa yapılmadı. Mevcut [`elbow.png`](ex04/elbow.png) grafiğinizde eğri yaklaşık olarak şöyle okunuyor:

| k | Yaklaşık inertia | Bir önceki k'ya göre azalma |
|---:|---:|---:|
| 1 | 332 bin | — |
| 2 | 216 bin | 116 bin |
| 3 | 136 bin | 80 bin |
| 4 | 103 bin | 33 bin |
| 5 | 86 bin | 17 bin |
| 6 | 74 bin | 12 bin |

`k=3`e kadar büyük, `k=4`te hâlâ anlamlı ama bariz biçimde küçülmüş, sonrasında ise daha küçük kazanımlar var. Bu nedenle yalnız görsele dayanarak “tek doğru cevap kesinlikle 3” demek fazla kuvvetli olur. Daha dürüst yorum: **dirsek 3–4 aralığında; 4 savunulabilir ve iş gereksinimiyle uyumludur.** Özellikle çizgide yön değişimi `k=3`ten `k=4`e geçişten sonra belirginleşiyor.

Elbow yöntemi bir teorem ya da otomatik karar kuralı değildir; amaç fonksiyonu her `k` artışında düşmek zorunda olduğu için, getirinin nerede azaldığını görsel olarak ölçen sezgisel bir model-seçim aracıdır. Aynı veri için iş hedefi, yorumlanabilirlik, segmentlerin büyüklüğü ve kampanyaların uygulanabilirliği de `k` seçiminde geçerlidir.

Subject'in ex05 talebi sadece istatistiksel geometri değildir. “New customer, inactive customer, loyalty status: gold + silver + platinum” örnekleri, ticari olarak en az dört farklı aksiyon grubu istediğini söyler. Kaba bir pazarlama eşlemesi örneği:

| Olası segment | RFM deseni | Olası aksiyon |
|---|---|---|
| Yeni / potansiyelli | düşük R, düşük–orta F/M | hoş geldin ve ikinci alışveriş teklifi |
| Aktif / gelişen | düşük–orta R, orta F/M | çapraz satış veya kupon |
| Sadık / yüksek değer | düşük R, yüksek F ve M | gold/silver/platinum avantajı |
| Pasif / kaybedilme riski | yüksek R, düşük F/M | geri kazanım e-postası |

Dolayısıyla ex04'ün görevi, “4 grubun veri açısından aşırı ayrıntılı olup olmadığını” sınamak ve seçimi gerekçelendirmekti; ex05'in kısıtı ise en az dört ticari segment üretmektir. Grafiğiniz bu iki gereksinimi çeliştirmiyor: 4'e geçişte inertia hâlâ kayda değer düşüyor ve 4 segment, istenen kampanya türlerini ayrı aksiyonlara çevirmeye izin veriyor.

ex05 raporunda şu tarz savunulabilir bir cümle kullanılabilir:

> Elbow eğrisi en keskin azalmanın `k=3`e kadar olduğunu, `k=4`te ise hâlâ anlamlı bir ek azalma bulunduğunu; `k≥5` için marjinal kazancın belirgin biçimde zayıfladığını gösteriyor. Dirsek 3–4 bandındadır. Subject'in en az dört eyleme dönük müşteri segmenti şartı ve `k=4`ün yeterli inertia kazanımı nedeniyle `k=4` seçilmiştir. Son karar, kümelerin RFM profillerinin pazarlama açısından ayrışıp ayrışmadığıyla doğrulanacaktır.

Ek kontrol olarak, `k=3`, `k=4` ve `k=5` için cluster büyüklüklerini ve RFM özetlerini karşılaştırın. Eğer `k=4`, yalnızca iyi tanımlı bir kümeyi iki anlamsız alt parçaya bölüyorsa 3 daha doğal olabilir; fakat ex05'te iş gereksinimi nedeniyle yine dört uygulanabilir grup tasarlamanız gerekir. Tersine, dördüncü küme belirgin bir “yeni” veya “pasif” profil ayırıyorsa, hem grafik hem iş hedefi 4'ü destekler. İsterseniz ek nicel kontrol olarak silhouette score da hesaplanabilir; fakat o, elbow'un yerine geçen mutlak hakem değildir ve kümeler küresel/konveks değilse yanıltıcı olabilir.

## Sonuç: `elbow.py` satırlarının kısa akışı

```text
PostgreSQL / customers
        │  SQL: user_id başına R, F, M hesapla
        ▼
df_rfm: yaklaşık 110000 × 4  (user_id, recency, frequency, monetary)
        │  user_id hariç; StandardScaler.fit_transform
        ▼
X_scaled: yaklaşık 110000 × 3  (her sütun ort. 0, varyans 1)
        │  k = 1, 2, ..., 10 için
        │  KMeans(..., n_init=10).fit(X_scaled)
        ▼
inertias: her k için en iyi başlangıcın WCSS'i
        │
        ▼
elbow.png: marjinal kazancı ve makul k aralığını gör
```

Bu örnekte kritik matematiksel ayrım şudur: scaler verinin **geometrisini/mesafe ağırlıklarını** belirler; K-Means o geometri içinde, sabit `k` için WCSS'i yerel olarak azaltır; elbow ise `k` arttıkça zorunlu düşen WCSS'in **ne zaman azalan getiriye geçtiğini** yorumlamaya yarar.

# SKLEARN TUTORIAL

> Bu bölüm dosyanın sonuna 19 Eylül 2026'da eklendi. Başlangıç satırı: **376**.

Bu bölüm, `scikit-learn`in (import adıyla `sklearn`) genel çalışma dilini ve ana kullanım ailelerini tanıtır. Amaç bütün algoritmaların iç matematiğini ezberlemek değil, bir problem görünce doğru aileyi seçebilmek ve nesnenin hangi metot/özniteliğini kullanacağını bilmektir.

Bu örneklerin çalışması için ayrı bir sanal ortamda aşağıdaki paketler yeterlidir:

```bash
python3 -m pip install scikit-learn numpy pandas joblib
```

Örneklerin çoğu `sklearn.datasets` ile küçük yapay veya yerleşik veri üretir. Bu sayede PostgreSQL bağlantısına ya da CSV dosyasına gerek kalmadan doğrudan denenebilirler.

## 1. Temel sözlük: örnek, özellik, hedef ve estimator

Bir veri matrisi genellikle `X` ile gösterilir ve şekli `(n_samples, n_features)` olur:

- Her **satır** bir gözlem/örnektir: burada bir müşteri.
- Her **sütun** bir özellik/özniteliktir: örneğin `recency`, `frequency`, `monetary`.
- `y`, varsa hedef/etikettir: örneğin “müşteri gelecek ay satın aldı mı?” (`0/1`) veya “gelecek ay ne kadar harcar?” (sayısal değer).

scikit-learn'de model veya dönüştürücü nesnelerinin ortak adı **estimator**dır. Genel akış şudur:

```python
# 1) Constructor: modelin ayarlarını seç; henüz veri öğrenilmedi.
estimator = SomeEstimator(hyperparameter=value)

# 2) fit: veriden parametreleri öğren.
estimator.fit(X_train, y_train)       # supervised örnek
# estimator.fit(X_train)              # unsupervised örnek

# 3) Uygun metotla sonucu kullan.
prediction = estimator.predict(X_new) # predictor ise
X_new_2 = estimator.transform(X_new)  # transformer ise
```

Constructor içindeki ayarlar **hyperparameter**dır: örneğin `KMeans(n_clusters=4)`te `4`, veri görülmeden bizim seçtiğimiz ayardır. `fit` sonrasında öğrenilen değerler ise genellikle sonunda alt çizgi bulunan özniteliklerdir: `coef_`, `mean_`, `labels_`, `cluster_centers_`. Alt çizgi, “fit ile sonradan oluştu” geleneksel işaretidir.

### Sık kullanılan ortak metotlar ve öznitelikler

| Tür | Ne zaman kullanılır? | Metot / öznitelik |
|---|---|---|
| Predictor | Bir `y` tahmin edilecekse | `fit(X, y)`, `predict(X)`, çoğunlukla `score(X, y)` |
| Olasılıklı classifier | Sınıf olasılığı/karar eşiği gerekiyorsa | `predict_proba(X)`, `classes_` |
| Transformer | `X` biçimini/ölçeğini değiştirmek için | `fit(X)`, `transform(X)`, `fit_transform(X)` |
| Clusterer | Etiket yokken grup bulmak için | `fit(X)`, `fit_predict(X)`, `labels_` |
| Model-selection nesnesi | Doğrulama ile model/parametre seçmek için | `fit(X, y)`, `best_params_`, `best_estimator_` |

`score`un anlamı estimator'a göre değişir. `LinearRegression.score` varsayılan olarak R², classifier'ların çoğunda accuracy, `KMeans.score` ise inertia'nın negatifidir. Bu nedenle ciddi değerlendirmede metriği adıyla açıkça çağırmak (`mean_absolute_error`, `f1_score`, `silhouette_score` gibi) daha anlaşılırdır.

## 2. Hangi problem için hangi aile?

| Elinizdeki soru | `y` var mı? | Başlangıç ailesi | Tipik araç |
|---|---|---|---|
| “Gelecek ay harcama kaç olacak?” | Evet, sayısal | Regresyon | `LinearRegression`, `RandomForestRegressor` |
| “Müşteri churn eder mi?” | Evet, sınıf | Sınıflandırma | `LogisticRegression`, `RandomForestClassifier` |
| “Benzer müşteriler hangi gruplarda?” | Hayır | Kümeleme | `KMeans`, `DBSCAN` |
| “Veriyi iki eksende görselleştireyim / gürültüyü azaltayım.” | Hayır | Boyut indirgeme | `PCA` |
| “Olağandışı sipariş var mı?” | Çoğunlukla hayır | Aykırı değer tespiti | `IsolationForest`, `LocalOutlierFactor` |
| “Eksik değer ve metin kategorileri nasıl hazırlanır?” | `y`den bağımsız | Ön işleme | `SimpleImputer`, `StandardScaler`, `OneHotEncoder` |
| “Hangi model gerçekten genelleşiyor; parametre ne olmalı?” | Genellikle evet | Değerlendirme/seçim | `cross_validate`, `GridSearchCV` |

Bir müşteri problemi birden çok aile kullanabilir. Örneğin önce eksik değerleri doldurup kategorileri kodlar, sonra churn classifier'ını pipeline içinde eğitir, cross-validation ile değerlendirir, en sonunda feature importance incelersiniz.

## 3. Veri hazırlama ve dönüşüm ailesi (`sklearn.preprocessing`, `impute`, `compose`)

Mesafe, gradyan ya da düzenlileştirme kullanan modellerde sayısal sütunların ölçeği önemlidir. Kategorik metinler doğrudan çoğu modele verilemez; eksikler de çoğu estimator için kabul edilmez. Bu aile modelden **önce** veriyi geçerli ve anlamlı bir sayısal matrise çevirir.

### 3.1 `StandardScaler`: sayısal ölçekleme

**Ne zaman?** K-Means, lojistik regresyon, SVM, k-NN, PCA gibi mesafe veya katsayı cezası kullanan yöntemlerde. Ağaç tabanlı modellerde (`DecisionTree`, `RandomForest`) genellikle gerekli değildir.

```python
import numpy as np
from sklearn.preprocessing import StandardScaler

# Sütunlar: [recency, frequency, monetary]
X = np.array([[2, 12, 1200], [30, 5, 520], [100, 1, 70]], dtype=float)

scaler = StandardScaler(with_mean=True, with_std=True)
X_scaled = scaler.fit_transform(X)

print(X_scaled.round(3))
print("Öğrenilen ortalamalar:", scaler.mean_)
print("Öğrenilen ölçekler:", scaler.scale_)

# Yeni müşteri için YENİDEN fit etme: aynı eski ölçeği uygula.
new_customer = np.array([[10, 7, 700]], dtype=float)
print(scaler.transform(new_customer).round(3))
```

Ana metotlar: `fit` → `mean_`, `var_`, `scale_` öğrenir; `transform` → bunlarla dönüştürür; `inverse_transform` → z-skorundan ham birime döner. `fit_transform`, eğitim verisi için ilk ikisinin kısa yoludur.

### 3.2 Eksik değer: `SimpleImputer`

**Ne zaman?** `NaN` içeren sayısal/kategorik sütunlarınız varsa. Sayısal sütunda medyan, kategorik sütunda en sık değer çoğu zaman güvenli temel seçimdir. Eksikliği sıfırla doldurmak ancak sıfırın gerçekten anlamlı olduğu durumda doğrudur.

```python
import numpy as np
from sklearn.impute import SimpleImputer

X = np.array([[2.0, 1200.0], [np.nan, 550.0], [40.0, np.nan]])
imputer = SimpleImputer(strategy="median")
X_filled = imputer.fit_transform(X)

print(X_filled)
print("Sütun medyanları:", imputer.statistics_)
```

Başlıca `strategy` değerleri `"mean"`, `"median"`, `"most_frequent"` ve `"constant"`tır. `statistics_`, fit sırasında seçilen doldurma değerlerini gösterir.

### 3.3 Kategorik sütun: `OneHotEncoder`

**Ne zaman?** `country`, `device`, `category_code` gibi nominal kategoriler varsa. `"mobile" = 1`, `"desktop" = 2` gibi sıradan sayıya çevirmek, modelin var olmayan bir sıralama/mesafe görmesine yol açabilir. One-hot, her kategori için 0/1 sütunu açar.

```python
import numpy as np
from sklearn.preprocessing import OneHotEncoder

X_device = np.array([["mobile"], ["desktop"], ["mobile"]])
encoder = OneHotEncoder(handle_unknown="ignore", sparse_output=False)
encoded = encoder.fit_transform(X_device)

print(encoder.get_feature_names_out(["device"]))
print(encoded)
print(encoder.transform([["tablet"]]))  # hata yerine tümü 0
```

`categories_` öğrenilen kategori listelerini tutar. `handle_unknown="ignore"`, eğitimde görülmeyen bir kategoriyle tahminde hata alınmasını engeller. Nadir kategorilerde `min_frequency` parametresiyle seyrek sınıfları birleştirmek de mümkündür.

### 3.4 Farklı sütunlara farklı işlem: `ColumnTransformer`

**Ne zaman?** Bir DataFrame'de hem sayısal hem kategorik sütun varsa. `StandardScaler` sadece sayısala, `OneHotEncoder` sadece kategoriye uygulanmalıdır. `ColumnTransformer` bu işlemleri isimle seçilen sütunlara dağıtır.

```python
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler

customers = pd.DataFrame({
    "recency": [2, 30, None, 90],
    "monetary": [1200, 550, 300, 80],
    "device": ["mobile", "desktop", "mobile", "tablet"],
})

preprocessor = ColumnTransformer([
    ("numeric", SimpleImputer(strategy="median"), ["recency", "monetary"]),
    ("device", OneHotEncoder(handle_unknown="ignore"), ["device"]),
])

X_ready = preprocessor.fit_transform(customers)
print(X_ready.toarray() if hasattr(X_ready, "toarray") else X_ready)
```

Bu örnek önce sayısal eksikleri doldurur, cihaz sütununu one-hot'a çevirir. Bir sonraki bölümde bunu `Pipeline` içinde ölçekleyip modelle bağlayacağız. Dönüşüm sonrası hangi sütunun nereden geldiğini görmek için `preprocessor.get_feature_names_out()` kullanılabilir.

### 3.5 Özellik üretimi: `PolynomialFeatures` ve metin vektörleştirme

**Ne zaman?** Doğrusal bir modele değişken etkileşimi/kare terimleri eklemek istiyorsanız `PolynomialFeatures`; ürün adı, yorum veya e-posta gibi serbest metni sayılara çevirmek istiyorsanız `TfidfVectorizer` kullanılır.

```python
import numpy as np
from sklearn.preprocessing import PolynomialFeatures
from sklearn.feature_extraction.text import TfidfVectorizer

X = np.array([[1, 2], [3, 4]])
poly = PolynomialFeatures(degree=2, include_bias=False)
print(poly.get_feature_names_out(["R", "F"]))
print(poly.fit_transform(X))  # R, F, R^2, R*F, F^2

texts = ["red shoes sale", "blue shoes", "red bag"]
tfidf = TfidfVectorizer(stop_words="english")
X_text = tfidf.fit_transform(texts)
print(tfidf.get_feature_names_out())
print(X_text.toarray().round(2))
```

`PolynomialFeatures` sütun sayısını hızla büyüttüğü için yüksek derece/çok değişkenle dikkatli kullanılmalıdır. `TfidfVectorizer.fit_transform` sözlüğü (`vocabulary_`) öğrenir ve seyrek (*sparse*) bir belge-terim matrisi üretir.

## 4. Denetimli öğrenme: regresyon (`sklearn.linear_model`, `ensemble`)

**Soru tipi:** Eğitimdeki her satır için sürekli sayısal `y` vardır. Örnekler: bir müşterinin gelecek ay harcaması, ev fiyatı, teslimat süresi, enerji tüketimi.

### 4.1 `LinearRegression`: yorumlanabilir doğrusal başlangıç

**Ne zaman?** İlişki yaklaşık doğrusal görünüyorsa veya yorumlanabilir bir baseline gerekiyorsa. Model yaklaşık olarak `y = β₀ + β₁x₁ + ... + β_px_p` öğrenir.

```python
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score

# X = metrekare; y = fiyat (milyon TL)
X_train = np.array([[50], [70], [90], [110]], dtype=float)
y_train = np.array([2.0, 2.5, 3.1, 3.6])
X_test = np.array([[80], [100]], dtype=float)
y_test = np.array([2.8, 3.3])

model = LinearRegression().fit(X_train, y_train)
y_pred = model.predict(X_test)

print("Tahmin:", y_pred.round(2))
print("Eğim coef_:", model.coef_)
print("Sabit intercept_:", model.intercept_)
print("MAE:", mean_absolute_error(y_test, y_pred))
print("R²:", r2_score(y_test, y_pred))
```

Önemli öznitelikler `coef_` (özellik katsayıları) ve `intercept_`tir. `predict` tahmin üretir. `score(X, y)` regresörlerde varsayılan R² verir ama raporda metrik adını yazmak daha iyidir. Büyük katsayılar, özellik ölçekleri farklıysa mutlak önem anlamına gelmez.

### 4.2 `Ridge` / `Lasso`: çok özellik ve regularization

**Ne zaman?** Çok sayıda veya birbiriyle ilişkili özellik olduğunda. `Ridge`, katsayıların karelerini; `Lasso`, mutlak değerlerini cezalandırır. Lasso bazı katsayıları tam sıfır yapabildiği için basit feature selection davranışı da sağlar.

```python
import numpy as np
from sklearn.linear_model import Ridge, Lasso
from sklearn.preprocessing import StandardScaler

X = np.array([[1, 100], [2, 120], [3, 130], [4, 150], [5, 170]], dtype=float)
y = np.array([10, 12, 13, 15, 17], dtype=float)
X_scaled = StandardScaler().fit_transform(X)

for name, model in [("ridge", Ridge(alpha=1.0)), ("lasso", Lasso(alpha=0.1))]:
    model.fit(X_scaled, y)
    print(name, "coef_ =", model.coef_.round(3), "prediction =", model.predict(X_scaled[:1]))
```

Temel hyperparameter `alpha`dır: büyüdükçe regularization güçlenir. Ölçekleme önemlidir; ceza katsayı büyüklüğüne uygulandığından, farklı birimli özellikler aksi hâlde eşitsiz cezalandırılır.

### 4.3 Doğrusal olmayan ilişki: `RandomForestRegressor`

**Ne zaman?** Eşikler, karmaşık etkileşimler ve doğrusal olmayan ilişki varsa; güçlü, az ön işlem gerektiren bir baseline için. Çok sayıda karar ağacının ortalamasını alır.

```python
from sklearn.datasets import make_regression
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

X, y = make_regression(n_samples=300, n_features=5, noise=20, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

forest = RandomForestRegressor(
    n_estimators=300, max_depth=8, random_state=42, n_jobs=-1
).fit(X_train, y_train)

print("MAE:", round(mean_absolute_error(y_test, forest.predict(X_test)), 2))
print("Ağaç-temelli önem:", forest.feature_importances_.round(3))
```

`n_estimators` ağaç sayısıdır; daha fazla ağaç maliyeti artırır ama tahmini genellikle kararlılaştırır. `max_depth` aşırı öğrenmeyi sınırlamaya yardım eder. `feature_importances_` hızlı bir ipucudur, fakat korelasyonlu özelliklerde yanıltıcı olabilir; sonraki inspection bölümündeki permutation importance daha güvenilir bir kontrol sağlar.

## 5. Denetimli öğrenme: sınıflandırma (`linear_model`, `ensemble`, `svm`, `neighbors`)

**Soru tipi:** `y` kesikli sınıftır. Örnekler: churn `evet/hayır`, fraud `normal/şüpheli`, ürün kategorisi, müşteri segmentinin bilinen etiketi. Sınıflandırma ile K-Means karıştırılmamalıdır: classifier'a geçmişte doğru etiketlenmiş örnekler verilir; K-Means etiketi kendi bulur.

### 5.1 `LogisticRegression`: olasılıklı ve açıklanabilir classifier

**Ne zaman?** İkili veya çok sınıflı problemde yorumlanabilir, güçlü bir baseline istenirse. İsminde “regression” olsa da sınıflandırıcıdır; lojistik fonksiyonla sınıf olasılığı üretir.

```python
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix

X, y = make_classification(
    n_samples=400, n_features=6, n_informative=4,
    weights=[0.7, 0.3], random_state=42
)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, stratify=y, random_state=42
)

clf = LogisticRegression(max_iter=1000, random_state=42).fit(X_train, y_train)
y_pred = clf.predict(X_test)

print("Sınıflar:", clf.classes_)
print("İlk 3 churn olasılığı:", clf.predict_proba(X_test[:3]).round(3))
print(confusion_matrix(y_test, y_pred))
print(classification_report(y_test, y_pred, digits=3))
```

`predict` varsayılan karar eşiğine göre sınıf verir; `predict_proba` her sınıfın olasılığını verir. İş maliyeti önemliyse 0.5 eşiği sabit kural değildir: fraud'da kaçırma maliyeti yüksekse daha düşük eşik seçilebilir. `coef_`, ölçeklenmiş özelliklerde yön ve göreli etki için yorumlanabilir; bu nedenle `StandardScaler` + `LogisticRegression` pipeline'ı sık kullanılır.

### 5.2 `RandomForestClassifier`: doğrusal olmayan güçlü baseline

**Ne zaman?** Tablo verisinde karmaşık etkileşimler varsa ve açıklanabilir doğrusal sınır yeterli değilse. Ölçekleme zorunlu değildir; yine de eksikler/kategoriler önceden ele alınmalıdır.

```python
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

X, y = load_iris(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, stratify=y, random_state=42
)

clf = RandomForestClassifier(n_estimators=200, random_state=42).fit(X_train, y_train)
print("Accuracy:", accuracy_score(y_test, clf.predict(X_test)))
print("Sınıf olasılıkları:", clf.predict_proba(X_test[:2]).round(3))
```

Sık kullanılan hyperparameter'lar `n_estimators`, `max_depth`, `min_samples_leaf` ve `max_features`tir. Dengesiz sınıflarda `class_weight="balanced"` bir başlangıç seçeneğidir; başarıyı yalnız accuracy ile değil precision, recall ve F1 ile değerlendirin.

### 5.3 Yakın komşular ve SVM: `KNeighborsClassifier`, `SVC`

**Ne zaman?** `KNeighborsClassifier` küçük/orta veri ve yerel benzerlik; `SVC` net ama doğrusal olmayan sınıf sınırları için düşünülebilir. Her ikisi mesafe kullandığı için ölçekleme gerekir; büyük veri için eğitim/tahmin maliyetleri dikkatle ölçülmelidir.

```python
from sklearn.datasets import load_wine
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split

X, y = load_wine(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, random_state=42)

knn = make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=5))
knn.fit(X_train, y_train)
print("Test accuracy:", knn.score(X_test, y_test))
```

`n_neighbors` küçükse model daha esnek/gürültüye duyarlı, büyükse daha pürüzsüz olabilir. SVM için benzer kullanım `make_pipeline(StandardScaler(), SVC(C=1.0, probability=True))` biçimindedir; `C` ceza/uyum dengesini, `gamma` RBF çekirdeğinin yerelliğini etkiler.

## 6. Denetimsiz öğrenme ailesi

Bu ailede çoğu zaman `y` yoktur. Sonuç “gerçek doğru sınıf” değildir; seçtiğiniz temsil, uzaklık ve varsayımlara göre verinin yapısının bir özeti/hipotezidir. Bu nedenle iş anlamı ve görselleştirme ile kontrol gerekir.

### 6.1 Kümeleme: `KMeans`

**Ne zaman?** Kümeler kabaca kompakt/küresel, benzer büyüklükte ve Öklid uzaklığı anlamlıysa. RFM segmentasyonu bu projedeki ana örnektir.

```python
from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

X, _ = make_blobs(n_samples=200, centers=4, cluster_std=0.7, random_state=42)
kmeans = KMeans(n_clusters=4, init="k-means++", n_init=10, random_state=42)
labels = kmeans.fit_predict(X)

print("Etiketler:", labels[:10])
print("Centroidler:\n", kmeans.cluster_centers_.round(2))
print("Inertia:", round(kmeans.inertia_, 2))
print("Silhouette:", round(silhouette_score(X, labels), 3))
```

`fit_predict(X)` = `fit(X)` ardından `labels_` alma kısa yoludur. `cluster_centers_`, `labels_`, `inertia_`, `n_iter_` temel özniteliklerdir. `n_clusters`, `n_init`, `random_state` ve gerekirse `max_iter` ana ayarlardır. K-Means öncesi RFM gibi sütunlar ölçeklenmelidir.

### 6.2 Yoğunluk/şekil tabanlı kümeleme: `DBSCAN`

**Ne zaman?** Kümeler küresel değilse, küme sayısı baştan bilinmiyorsa veya gürültü noktalarını ayırmak istiyorsanız. `DBSCAN`, yoğun bölgeleri birleştirir; `-1` etiketi gürültüdür.

```python
from sklearn.datasets import make_moons
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler

X, _ = make_moons(n_samples=250, noise=0.06, random_state=42)
X = StandardScaler().fit_transform(X)
dbscan = DBSCAN(eps=0.25, min_samples=5)
labels = dbscan.fit_predict(X)

print("Bulunan etiketler:", sorted(set(labels)))
print("Gürültü noktası sayısı:", (labels == -1).sum())
```

`eps`, komşuluk yarıçapıdır; `min_samples`, yoğun sayılmak için gereken minimum komşu sayısıdır. Bu iki değer ölçeğe çok duyarlıdır; scaling burada özellikle kritiktir. `DBSCAN`da K-Means'teki gibi `cluster_centers_` yoktur.

### 6.3 Boyut indirgeme: `PCA`

**Ne zaman?** Çok sayıda sayısal özelliği daha az eksende özetlemek, korelasyonlu değişkenleri sıkıştırmak veya 2D/3D görselleştirmek istiyorsanız. PCA denetimsiz, doğrusal bir dönüşümdür; yeni bileşenler varyansı en çok açıklayan dik yönlerdir.

```python
from sklearn.datasets import load_wine
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

X, y = load_wine(return_X_y=True)
X_scaled = StandardScaler().fit_transform(X)
pca = PCA(n_components=2, random_state=42)
X_2d = pca.fit_transform(X_scaled)

print("Eski/yeni şekil:", X.shape, X_2d.shape)
print("Bileşenlerin açıkladığı varyans:", pca.explained_variance_ratio_.round(3))
print("Toplam:", round(pca.explained_variance_ratio_.sum(), 3))
print("Yükler components_ şekli:", pca.components_.shape)
```

`n_components=2` görselleştirme için yaygındır; `n_components=0.95`, varyansın %95'ini koruyacak bileşen sayısını seçebilir. `components_` her ana bileşenin orijinal değişkenlerdeki yön/yüklerini, `explained_variance_ratio_` açıklanan varyansı verir. PCA öncesi ölçekleme genellikle gereklidir; aksi hâlde büyük birimli sütun bileşenleri domine eder.

### 6.4 Aykırı değer tespiti: `IsolationForest`

**Ne zaman?** Şüpheli işlem, olağandışı müşteri davranışı veya veri kalitesi anomalisi aranıyorsa ve güvenilir etiket yoksa. Isolation Forest, sıradışı noktaların rastgele bölmelerle daha kısa yoldan izole edildiği fikrini kullanır.

```python
import numpy as np
from sklearn.ensemble import IsolationForest

rng = np.random.RandomState(42)
normal = rng.normal(loc=[10, 100], scale=[2, 15], size=(100, 2))
unusual = np.array([[40, 400], [-15, 10]])
X = np.vstack([normal, unusual])

detector = IsolationForest(contamination=0.02, random_state=42)
labels = detector.fit_predict(X)  # +1: normal, -1: anomaly
scores = detector.decision_function(X)
print("Aykırı indisleri:", np.where(labels == -1)[0])
print("Son iki karar skoru:", scores[-2:].round(3))
```

`contamination`, beklenen aykırı oranı için bir eşik ayarıdır; gerçek işte rastgele seçilmemeli, iş bilgisiyle/validasyonla belirlenmelidir. `fit_predict`in `-1/+1` sözleşmesi sınıflandırmadaki `0/1` etiketiyle karıştırılmamalıdır.

### 6.5 Yoğunluk tahmini: `KernelDensity`

**Ne zaman?** Bir değişkenin veya düşük boyutlu uzayın olasılık yoğunluğunu pürüzsüz biçimde tahmin etmek; alışılmadık düşük yoğunluklu noktaları görmek istiyorsanız. Yüksek boyutta zorlaşır.

```python
import numpy as np
from sklearn.neighbors import KernelDensity

X = np.array([[1.0], [1.2], [1.4], [3.8], [4.0], [4.2]])
kde = KernelDensity(kernel="gaussian", bandwidth=0.25).fit(X)
grid = np.array([[1.3], [2.5], [4.1]])
log_density = kde.score_samples(grid)
print(list(zip(grid.ravel(), log_density.round(3))))
```

`bandwidth` pürüzsüzlük ayarıdır: küçük değer çok dalgalı, büyük değer fazla düz yoğunluk üretir. `score_samples` olasılık değil **log yoğunluk** döndürür; karşılaştırırken büyük değer daha yoğun bölgeyi ifade eder.

## 7. Özellik seçimi ve model inceleme (`feature_selection`, `inspection`)

### 7.1 `SelectKBest`: en ilgili k özelliği seçmek

**Ne zaman?** Çok fazla sütun varsa, basit bir filtreyle en yararlı görünenleri azaltmak istiyorsanız. Bu seçim yalnızca eğitim katında yapılmalıdır; pipeline bunu güvenli yapar.

```python
from sklearn.datasets import load_breast_cancer
from sklearn.feature_selection import SelectKBest, f_classif

X, y = load_breast_cancer(return_X_y=True)
selector = SelectKBest(score_func=f_classif, k=5)
X_small = selector.fit_transform(X, y)

print("Yeni şekil:", X_small.shape)
print("Seçilen sütun indisleri:", selector.get_support(indices=True))
print("ANOVA skorları:", selector.scores_[selector.get_support()].round(2))
```

`get_support()` boolean maske, `get_support(indices=True)` seçili indisleri verir. `f_classif` sınıflandırma için tek değişkenli ANOVA F testidir. Regresyonda `f_regression` gibi uygun `score_func` seçilir. Bu yöntem özelliklerin birlikte etkileşimini değil, tek tek ilişkisini ölçer.

### 7.2 `permutation_importance`: tahmine gerçek katkı kontrolü

**Ne zaman?** Eğitilmiş herhangi bir modelde bir sütun karıştırıldığında test başarısının ne kadar bozulduğunu ölçmek için. Ağaçtaki yerleşik `feature_importances_` değerini tamamlayan model-bağımsız bir yöntemdir.

```python
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.inspection import permutation_importance
from sklearn.model_selection import train_test_split

X, y = load_iris(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42, stratify=y)
model = RandomForestClassifier(random_state=42).fit(X_train, y_train)

result = permutation_importance(model, X_test, y_test, n_repeats=20, random_state=42)
print("Ortalama önem:", result.importances_mean.round(3))
print("Belirsizlik (std):", result.importances_std.round(3))
```

Önem, **test** veya validation verisinde ölçülmelidir. Güçlü korelasyonlu iki özellik birbirinin yerine geçebileceği için, tek tek karıştırıldığında önemleri olduğundan küçük görünebilir.

## 8. Doğru deney: bölme, metrik ve cross-validation (`model_selection`, `metrics`)

Bir modeli eğitim verisine iyi uydurmak, yeni müşterilerde iyi çalışacağını kanıtlamaz. Veri bölme ve metrik seçimi, modelin kendisi kadar önemlidir.

### 8.1 `train_test_split` ve problem-uygun metrikler

```python
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
from sklearn.model_selection import train_test_split

X, y = make_classification(n_samples=500, weights=[0.9, 0.1], random_state=42)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, stratify=y, random_state=42
)
model = LogisticRegression(max_iter=1000).fit(X_train, y_train)
y_pred = model.predict(X_test)
y_prob = model.predict_proba(X_test)[:, 1]

print("accuracy :", round(accuracy_score(y_test, y_pred), 3))
print("precision:", round(precision_score(y_test, y_pred), 3))
print("recall   :", round(recall_score(y_test, y_pred), 3))
print("F1       :", round(f1_score(y_test, y_pred), 3))
print("ROC-AUC  :", round(roc_auc_score(y_test, y_prob), 3))
```

`stratify=y`, sınıf oranını eğitim/teste yaklaşık korur; dengesiz churn/fraud verisinde önemlidir. Accuracy %90 iken model azınlık sınıfının hiçbirini bulamıyor olabilir. Pozitif müşteriye yanlış kampanya göndermek pahalıysa precision, churn müşterisini kaçırmak pahalıysa recall, olasılık sıralamasını değerlendirmek için ROC-AUC/PR-AUC daha anlamlı olabilir.

Regresyonda yaygın metrikler `mean_absolute_error` (aynı birimde tipik mutlak hata), `mean_squared_error` / `root_mean_squared_error` (büyük hataya daha fazla ceza) ve `r2_score`dur.

### 8.2 `cross_validate`: tek bölmeye bağımlı kalmamak

**Ne zaman?** Veri az/orta boyuttaysa veya model karşılaştırmasında daha kararlı tahmin gerekiyorsa. K-fold cross-validation, veriyi dönüşümlü eğitim/doğrulama parçalarına ayırır.

```python
from sklearn.datasets import load_diabetes
from sklearn.linear_model import Ridge
from sklearn.model_selection import cross_validate
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

X, y = load_diabetes(return_X_y=True)
pipe = make_pipeline(StandardScaler(), Ridge(alpha=1.0))
result = cross_validate(
    pipe, X, y, cv=5,
    scoring=("r2", "neg_mean_absolute_error"),
    return_train_score=False,
)

print("Fold R²:", result["test_r2"].round(3))
print("Ortalama R²:", round(result["test_r2"].mean(), 3))
print("Ortalama MAE:", round(-result["test_neg_mean_absolute_error"].mean(), 3))
```

scikit-learn kayıp metriklerini “büyük daha iyidir” ortak kuralına uydurmak için negatif döndürür; bu yüzden `neg_mean_absolute_error` sonucu ekranda yeniden `-` ile çevrilir. Zaman serisinde rasgele KFold yerine `TimeSeriesSplit`, aynı müşteriden birden çok satır varsa group-aware bölücüler kullanılmalıdır.

## 9. `Pipeline`: dönüşüm ile modeli tek güvenli nesnede birleştirmek

Pipeline şu sorunun cevabıdır: “Scaler'ı yalnız eğitim verisine fit edip, test/yeni veriye aynı dönüşümü modelle birlikte nasıl uygularım?” Pipeline, veri sızıntısını engeller ve üretimdeki tahmin akışını tek nesneye toplar.

```python
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

df = pd.DataFrame({
    "recency": [2, 5, 30, 60, 90, 120, 8, 45],
    "monetary": [1200, 900, 500, 250, 80, 40, 1100, 320],
    "device": ["mobile", "desktop", "mobile", "tablet", "desktop", "mobile", "tablet", "desktop"],
    "churn": [0, 0, 0, 1, 1, 1, 0, 1],
})
X = df.drop(columns="churn")
y = df["churn"]
X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, random_state=42)

numeric = Pipeline([
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler()),
])
preprocessor = ColumnTransformer([
    ("numeric", numeric, ["recency", "monetary"]),
    ("category", OneHotEncoder(handle_unknown="ignore"), ["device"]),
])
pipe = Pipeline([
    ("preprocess", preprocessor),
    ("classifier", LogisticRegression(max_iter=1000)),
])

pipe.fit(X_train, y_train)
print("Test score:", pipe.score(X_test, y_test))
print("Yeni müşteri churn olasılığı:", pipe.predict_proba(pd.DataFrame([{
    "recency": 75, "monetary": 110, "device": "mobile"
}]))[:, 1])
```

Pipeline'ın ana metotları yine `fit`, `predict`, `predict_proba`, `score`dur; çağrı otomatik olarak önce tüm transformer'ları, sonra son estimator'ı işletir. Adımlara `pipe.named_steps["classifier"]` ile erişilir. Hyperparameter aramasında adım adı çift alt çizgiyle kullanılır: `classifier__C`, `preprocess__numeric__scaler__with_std` gibi.

## 10. Hyperparameter arama: `GridSearchCV` ve `RandomizedSearchCV`

**Ne zaman?** Bir-iki model için makul ayarların hangisinin daha iyi genelleştiğini cross-validation ile seçmek istiyorsanız. Test setini bu seçimde kullanmayın; test, en son tarafsız değerlendirme için saklanır.

```python
from sklearn.datasets import load_wine
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

X, y = load_wine(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, random_state=42)
pipe = make_pipeline(StandardScaler(), SVC())

search = GridSearchCV(
    estimator=pipe,
    param_grid={"svc__C": [0.1, 1, 10], "svc__gamma": ["scale", 0.01, 0.1]},
    cv=5,
    scoring="f1_macro",
    n_jobs=-1,
)
search.fit(X_train, y_train)
print("En iyi ayar:", search.best_params_)
print("CV skoru:", round(search.best_score_, 3))
print("Dokunulmamış test skoru:", round(search.score(X_test, y_test), 3))
```

`GridSearchCV` bütün parametre kombinasyonlarını dener; alan büyükse `RandomizedSearchCV` daha düşük maliyetli rastgele örnekleme yapar. `best_estimator_`, en iyi ayarla yeniden fit edilmiş pipeline'dır; `cv_results_` bütün kombinasyonların sonuç tablosudur. Arama uzayını aşırı büyütmek hem pahalı hem de validation'a aşırı uyum riski taşır.

## 11. Dataset yardımcıları ve görselleştirme

### 11.1 Yerleşik/yapay veri: `datasets`

Öğrenmek, test yazmak ve algoritmayı denemek için `load_iris`, `load_wine`, `load_diabetes`, `make_classification`, `make_regression`, `make_blobs` yararlıdır.

```python
from sklearn.datasets import load_iris, make_blobs

iris = load_iris(as_frame=True)
print(iris.data.head())
print(iris.target_names)

X, labels = make_blobs(n_samples=50, centers=3, n_features=2, random_state=42)
print(X.shape, labels.shape)
```

`as_frame=True` ile DataFrame/Series biçiminde, `return_X_y=True` ile doğrudan `(X, y)` biçiminde veri alınabilir. Yapay veri üreticilerinde `random_state` deneyin tekrar üretilebilirliği için sabitlenmelidir.

### 11.2 `ConfusionMatrixDisplay` ve `RocCurveDisplay`

**Ne zaman?** Sınıflandırıcı hatalarının hangi sınıflar arasında olduğunu veya karar eşiğinden bağımsız performansı görselleştirmek istediğinizde.

```python
import matplotlib.pyplot as plt
from sklearn.datasets import load_breast_cancer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import ConfusionMatrixDisplay, RocCurveDisplay
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

X, y = load_breast_cancer(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, random_state=42)
model = make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000)).fit(X_train, y_train)

ConfusionMatrixDisplay.from_estimator(model, X_test, y_test)
plt.show()
RocCurveDisplay.from_estimator(model, X_test, y_test)
plt.show()
```

`from_estimator` modeli, `X`i ve `y`yi alıp gerekli tahmin/olasılık çağrılarını kendisi yapar. Confusion matrix hata türlerini, ROC eğrisi eşik değiştikçe true-positive/false-positive dengesini gösterir.

## 12. Modeli saklamak: `joblib`

**Ne zaman?** Eğitim tamamlandıktan sonra aynı pipeline'ı yeniden fit etmeden yeni müşteri tahmininde kullanmak istiyorsanız. Transformer ve model ayrı değil, **tek pipeline** olarak saklanmalıdır; böylece yeni veriye aynı kodlama/ölçekleme uygulanır.

```python
import joblib
from sklearn.datasets import load_iris
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

X, y = load_iris(return_X_y=True)
pipe = make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000)).fit(X, y)

joblib.dump(pipe, "iris_classifier.joblib")
loaded_pipe = joblib.load("iris_classifier.joblib")
print(loaded_pipe.predict(X[:2]))
```

Yalnız güvenilen kaynaktan gelen `joblib`/pickle dosyalarını yükleyin; bunlar yüklenirken keyfî kod çalıştırma riski taşıyabilir. Ayrıca ortam sürümlerini (`scikit-learn`, NumPy, Python) kayıt altına alın; farklı sürümde yüklemek desteklenmeyen veya farklı sonuç üreten bir durum olabilir.

## 13. Pratik karar akışı ve bu projeye uygulanışı

RFM projenizde doğru minimal sklearn akışı şöyledir:

```python
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

rfm_columns = df_rfm[["recency", "frequency", "monetary"]]
X_scaled = StandardScaler().fit_transform(rfm_columns)

kmeans = KMeans(n_clusters=4, n_init=10, random_state=42)
df_rfm["cluster"] = kmeans.fit_predict(X_scaled)

summary = df_rfm.groupby("cluster")[["recency", "frequency", "monetary"]].agg(
    ["count", "mean", "median"]
)
print(summary)
print("WCSS / inertia:", kmeans.inertia_)
```

Ardından cluster numarasını değil RFM özetini yorumlayın. Düşük recency + yüksek frequency/monetary kümesi yüksek değerli/sadık, yüksek recency + düşük frequency/monetary kümesi pasif/geri kazanım adayı olabilir. Bu isimler K-Means tarafından öğrenilmez; iş hedefiyle analistin verdiği yorumdur.

### Son kontrol listesi

1. Soru sayısal bir hedef mi, sınıf mı, etiketsiz yapı mı? Önce aileyi buna göre seçin.
2. `X` satır/sütun yönünü, veri tiplerini, `NaN`leri ve kategorileri kontrol edin.
3. Mesafe/katsayı-ceza kullanan modelde scaler'ı pipeline içine koyun.
4. Eğitim/test ayrımını model seçmeden önce yapın; test setini en sona saklayın.
5. İş maliyetine uygun metriği kullanın; yalnız `score()`a güvenmeyin.
6. `random_state`ı deney tekrarlanabilirliği için sabitleyin.
7. Hyperparameter seçimini cross-validation ile, dönüşümler dahil pipeline üzerinde yapın.
8. Sonucu ham RFM/iş diliyle açıklayın; model çıktısının kendi başına karar olmadığını unutmayın.

Bu bölümdeki API düzeni ve pipeline/cross-validation tavsiyeleri resmî [scikit-learn Getting Started](https://scikit-learn.org/stable/getting_started.html) rehberiyle, algoritma ailelerinin kapsamı ise [User Guide](https://scikit-learn.org/stable/user_guide.html) ile uyumludur.

