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
