# DS_3 PIPELINE

## Büyük resim: Aslında bu 6 egzersizde ne yapıyoruz?

En yukarıdan bakarsak:

```text
                         VERİ
                          │
                          ▼
                ┌──────────────────┐
                │ Ex00: Histogram  │
                │ Veriyi tanı      │
                └────────┬─────────┘
                         │
                         ▼
                ┌──────────────────┐
                │ Ex01: Correlation│
                │ Feature ↔ Target │
                └────────┬─────────┘
                         │
                         ▼
                ┌──────────────────┐
                │ Ex02: Scatter    │
                │ Görsel ayırma    │
                └────────┬─────────┘
                         │
                         ▼
                ┌──────────────────┐
                │ Ex03: Standard.  │
                │ Feature scaling  │
                └────────┬─────────┘
                         │
                         ▼
                ┌──────────────────┐
                │ Ex04: Normaliz.  │
                │ Feature scaling  │
                └────────┬─────────┘
                         │
                         ▼
                ┌──────────────────┐
                │ Ex05: Split      │
                │ Train/Validation │
                └──────────────────┘
```

Yani bu proje şu sırayı öğretmeye çalışıyor:

> **Önce veriyi anla → ilişkileri ölç → görselleştir → uygun biçime getir → model geliştirme için veri kümelerini ayır.**

Bu yüzden senin “her yaptığımız şeyin mantıklı bir gerekçesi olmalı” yaklaşımın burada gerçekten doğru yaklaşım.

---

# Önce çok önemli bir ayrım: Bunların hangisi Machine Learning?

Bu altı egzersizin hepsi doğrudan “model eğitmek” değildir.

Kabaca:

### Ex00–Ex02

Bunlar esas olarak:

**Exploratory Data Analysis (EDA)**  
yani **keşifsel veri analizi**.

Henüz bir makine öğrenmesi modeli eğitmiyorsun.

### Ex03–Ex04

Bunlar:

**Data preprocessing / feature scaling**

yani veriyi modelleme öncesinde uygun bir biçime getirme.

### Ex05

Bu:

**Dataset splitting**

yani modeli değerlendirebilmek için veri kümelerini ayırma.

Henüz örneğin:

```python
model.fit(...)
model.predict(...)
```

gibi bir şey yapmıyorsun.

Ama bunlar gerçek ML pipeline'ının temel hazırlık adımları.

---

# Ex00 — Histogram

Subject'in istediği şey:

> `Test_knight.csv` üzerinde histogram oluşturmak; `Train_knight.csv` üzerinde ise knight hedefi ile feature'ların ilişkisini aynı histogramlarda görmek. fileciteturn0file0L58-L72

## Veri bilimi açısından adı ne?

Bunun temel adı:

**Univariate exploratory analysis**

veya

**Distribution analysis**

olarak düşünülebilir.

Histogram sana bir feature'ın:

$$
X
$$

dağılımını gösterir.

Örneğin:

```text
Strength

       █
       █
   █   █
   █ █ █
 █ █ ███
──────────────
```

Buradan şunları gözlemleyebilirsin:

- değerler nerede yoğun?
- dağılım simetrik mi?
- çarpık mı?
- uç değerler var mı?
- yaklaşık hangi aralıkta?
- iki grubun dağılımları farklı mı?

---

## Train'de neden Jedi ve Sith'i ayrı histogramlarla gösteriyoruz?

Çünkü artık elimizde:

$$
X = \text{feature}
$$

ve

$$
Y = \text{knight}
$$

var.

Mesela:

$$
X=\text{Strength}
$$

için:

```text
Jedi  → mavi
Sith  → kırmızı
```

çizdiğinde soru şu oluyor:

> Strength değerinin dağılımı Jedi ve Sith arasında farklı mı?

Bu doğrudan ML açısından çok önemli bir soru:

> **Bu feature target'ı ayırt etmeye yardımcı olabilir mi?**

Henüz model yok. Ama model kurmadan önce veriyi incelemeye başlıyorsun.

---

# Ex00'un büyük amacı

Ex00 aslında:

> **"Veriyi tanıyorum."**

aşaması.

Örneğin bir feature şöyle görünüyorsa:

```text
Jedi: █████████
Sith:      █████████
```

bu feature'ın sınıfları ayırma açısından ilginç olabileceğini düşünürsün.

Ama:

```text
Jedi: █████████
Sith: █████████
```

aynı dağılımda ise o feature'ın sınıfları ayırması daha zor görünebilir.

Bu henüz matematiksel bir kanıt değil; **keşifsel gözlem**.

---

# Ex01 — Correlation

Subject burada açıkça:

> target (`knight`) ile tüm feature'lar arasındaki en güçlü correlation'ları bulmanı istiyor. fileciteturn0file0L76-L84

Bu egzersizin veri bilimi açısından adı:

**Feature–target association analysis**

ve burada özel olarak:

**Pearson correlation analysis**

yapıyorsun.

---

## Neden yapıyoruz?

Ex00'da görsel olarak:

> “Bu feature önemli olabilir.”

diye bakıyordun.

Ex01'de bunu sayısallaştırıyorsun:

$$
r_{X,Y}
$$

Örneğin subject'in örneğinde:

$$
\text{corr(Empowered, knight)}=0.793566
$$

gibi değerler var. fileciteturn0file0L85-L113

Bu sana:

> "Bu feature ile target arasında doğrusal ilişki ne kadar güçlü?"

sorusuna cevap veriyor.

---

## Neden `Jedi/Sith`'i 0/1 yaptık?

Çünkü `knight` kategorik:

```text
Jedi
Sith
```

Pearson hesabına doğrudan string veremezsin.

Dolayısıyla bunu binary indicator'a çeviriyorsun:

$$
Y\in\{0,1\}
$$

ve böylece:

$$
corr(X,Y)
$$

hesaplayabiliyorsun.

Burada konuştuğumuz gibi **0 ve 1 sihirli sayılar değil**. İki sınıfı sayısal olarak temsil ediyorlar.

Bu durumda Pearson correlation, binary target ile sürekli feature arasındaki **point-biserial correlation** olarak da yorumlanabilir.

---

# Ex01'in büyük amacı

Ex00:

> "Gözümle baktığımda ne görüyorum?"

Ex01:

> "Bunu bir sayıyla ifade edebilir miyim?"

Yani:

```text
EDA
 │
 ├── Görsel gözlem
 │
 └── Sayısal ilişki ölçümü
```

Bu ikisi birlikte feature'ları anlamaya yarıyor.

---

# Ex02 — Scatter plots

Subject burada 4 grafik istiyor:

- Train için 2 grafik
- Test için 2 grafik
- bunlardan biri sınıfları görsel olarak ayırmalı
- diğeri sınıfları karıştırmalı. fileciteturn0file0L118-L128

Subject'in örneklerinde gerçekten bir feature pair'i sınıfları oldukça iyi ayırıyor, başka bir pair ise sınıfları daha fazla karıştırıyor. fileciteturn2file0

---

## Bunun adı ne?

**Bivariate exploratory analysis**

ve özellikle:

**Scatter plot / feature-space visualization**

.

Şimdi tek feature yerine iki feature birlikte düşünüyorsun:

$$
(X_1,X_2)
$$

Örneğin:

```text
x = Empowered
y = Prescience
```

Her knight artık düzlemde bir nokta:

$$
(x_i,y_i)
$$

oluyor.

---

## Burada aslında neye bakıyoruz?

Asıl soru:

> **Feature uzayında sınıflar birbirinden geometrik olarak ayrılabiliyor mu?**

Örneğin:

```text
Sith   •••••••
       •••••
              •
                 •••••••
                    ••••
Jedi  •••••••
      •••••••
```

gibi bir yapı görürsen, iki feature'ın birlikte sınıf ayrımı hakkında bilgi taşıdığını görürsün.

Buna:

**class separability**

veya

**class separation in feature space**

diyebiliriz.

---

## Burada çok önemli bir nokta var

Ex01'de tek tek:

$$
corr(X_1,Y)
$$

ve

$$
corr(X_2,Y)
$$

ölçtün.

Ex02'de ise artık:

$$
(X_1,X_2)
$$

birlikte nasıl davranıyor diye bakıyorsun.

Bu önemli, çünkü:

> Tek tek çok güçlü görünmeyen iki feature birlikte faydalı bir geometrik yapı oluşturabilir.

Yani correlation bütün hikâye değildir.

---

# Ex03 — Standardization

Şimdi ilk üç egzersizde:

```text
Veriyi tanıdık
   ↓
İlişkileri ölçtük
   ↓
Görsel olarak feature-space'e baktık
```

Şimdi verinin **ölçeğiyle** ilgileniyoruz.

Subject Ex03'te:

- veriyi standardize et
- yazdır
- önceki grafiklerden birini standardize edilmiş veriyle çiz
- Train ve Test ile çalışsın

diyor. fileciteturn0file0L131-L140

---

## Bunun adı ne?

**Feature standardization**

veya:

**Z-score standardization**

.

Standart formül:

$$
z=\frac{x-\mu}{\sigma}
$$

Burada:

- \(\mu\): ortalama
- \(\sigma\): standart sapma

---

## Neden yapıyoruz?

Çünkü feature'ların ölçekleri farklı olabilir.

Örneğin:

```text
Strength       10 - 200
Delay           0 - 1
Mass            40 - 120
```

Bir algoritma için bunların büyüklükleri farklı anlamlara gelebilir.

Özellikle:

- distance-based methods
- gradient-based methods
- regularized models
- PCA
- k-nearest neighbors
- k-means
- SVM gibi yöntemlerde

feature scaling önemli olabilir.

Örneğin Öklid mesafesi:

$$
d(x,y)
=
\sqrt{
(x_1-y_1)^2+
(x_2-y_2)^2
}
$$

olsun.

Eğer:

```text
X1: 0–1000
X2: 0–1
```

ise \(X_1\)'in mesafeye katkısı doğal olarak çok daha büyük olabilir.

Standardization ile ikisini karşılaştırılabilir bir ölçeğe getirirsin.

---

## Ama önemli bir nokta

Ex03'te scaling yapmanın amacı **correlation hesaplamak değil**.

Pearson correlation için feature'ları standardize etmek gerekmiyordu; Ex01 zaten ham veride yapılabiliyordu.

Scaling'in asıl önemi, ileride kullanılabilecek birçok ML algoritması için feature'ları uygun bir ölçekte ifade etmektir.

---

# Ex04 — Normalization

Subject Ex04'te:

- normalize et
- yazdır
- Ex02'deki diğer grafiklerle normalize edilmiş veriyi göster
- Train ve Test ile çalışsın

diyor. fileciteturn0file0L150-L160

Bu sefer yine **feature scaling** yapıyoruz ama standardization'dan farklı bir dönüşüm kullanıyoruz.

---

## Buradaki genel fikir

Normalization genellikle feature'ları belirli bir aralığa taşır.

Bu subject'in örnek grafiğinde eksenlerin yaklaşık:

$$
0\le x\le1,\qquad 0\le y\le1
$$

aralığında olması ve örnek çıktıda `0.52`, `0.02`, `0.54`, ... gibi değerler verilmesi, burada **Min-Max benzeri [0,1] normalization** kullanıldığını güçlü biçimde düşündürüyor. Fakat subject metni kullanılan formülü açıkça yazmıyor; yalnızca "Normalize" diyor. fileciteturn2file0

Tipik formül:

$$
x'=
\frac{x-x_{\min}}
{x_{\max}-x_{\min}}
$$

Böylece:

$$
x_{\min}\rightarrow0
$$

ve

$$
x_{\max}\rightarrow1
$$

olur.

---

# Standardization ile normalization arasındaki büyük fark

| | Standardization | Normalization |
|---|---|---|
| Tipik formül | \(\frac{x-\mu}{\sigma}\) | \(\frac{x-x_{\min}}{x_{\max}-x_{\min}}\) |
| Hedef | mean ≈ 0, std ≈ 1 | genellikle [0,1] |
| Sabit aralık | Hayır | Evet |
| Adı | Z-score scaling | Min-Max scaling |

Ama terminolojiye dikkat: Gerçek kaynaklarda **"normalization" ve "standardization" bazen farklı şekillerde adlandırılabilir**. Burada subject'in kendi kullandığı ayrım üzerinden gidiyoruz.

---

# Peki Ex03 ve Ex04 neden ikisi birden var?

Aslında çok güzel bir ders veriyor:

> **"Bir veri setini ölçeklendirmenin tek bir yöntemi yoktur."**

Veriye ve kullanacağın yönteme göre:

$$
X
\rightarrow
Z
$$

veya

$$
X
\rightarrow
X'
$$

gibi farklı dönüşümler yapabilirsin.

Ve grafik üzerinde bunun etkisini görebilirsin.

---

# Ex05 — Split

Bence bütün projenin machine-learning açısından en önemli egzersizi burası.

Subject:

> `Train_knight.csv` dosyasını rastgele şekilde `Training_knight.csv` ve `Validation_knight.csv` olarak böl.

ve

> her birinde yüzde kaç tuttuğunu ve nedenini açıklayabilmelisin

diyor. fileciteturn0file0L171-L180

Subject'in verdiği şema da:

```text
Dataset
   │
   ├── Training
   └── Testing

Training
   │
   ├── Training
   └── Validation
```

şeklinde. fileciteturn2file0

---

# Bunun adı ne?

**Train/validation/test split**

veya:

**Dataset partitioning**

.

---

# Neden validation diye ayrı bir veri oluşturuyoruz?

Çünkü model geliştirirken modelin veriye ne kadar iyi uyduğunu görmek istiyorsun.

Örneğin:

```text
Training data
      ↓
   model.fit()
      ↓
 Validation data
      ↓
 model değerlendirme
```

Training data:

> modelin öğrenmesi için.

Validation data:

> model seçimleri / hyperparameter ayarları / yaklaşımı kontrol etmek için.

Test data:

> en sonunda modelin daha önce görmediği verideki performansını ölçmek için.

---

# En önemli ayrım

Bu üç kavramı kesinlikle birbirine karıştırmamak gerekiyor:

### Training set

Model **öğrenir**.

### Validation set

Modeli geliştirirken **karar vermene yardımcı olur**.

### Test set

En sonunda modelin **daha önce görmediği verideki performansını** ölçmek için kullanılır.

---

# O yüzden Ex05 çok önemli

Önceki egzersizlerde sen:

```text
Veriyi anlamaya
```

çalışıyordun.

Ex05'te:

> "Modeli değerlendirirken kendimizi nasıl kandırmayacağız?"

sorusuna giriş yapıyorsun.

Çünkü modeli tüm veride eğitip yine aynı veride test edersen:

```text
model → veriyi zaten gördü
```

olur.

Bu gerçek genelleme performansını ölçmez.

Bu yüzden veri ayrılır.

---

# Şimdi bütün projeyi tek bir ML hikâyesi olarak okuyalım

Bence senin aradığın "neden-sonuç" zinciri tam olarak şu:

---

## Aşama 1 — Ex00

### "Verim nasıl davranıyor?"

Histogramlarla:

$$
P(X)
$$

hakkında fikir edinmeye çalışıyorsun.

Dağılım, yayılım, outlier, farklı sınıf dağılımları...

Bu:

**EDA**

---

## Aşama 2 — Ex01

### "Feature ile hedef arasında ilişki var mı?"

$$
corr(X_i,Y)
$$

hesaplıyorsun.

Bu:

**association / correlation analysis**

---

## Aşama 3 — Ex02

### "Feature'ları birlikte ele alırsam sınıflar geometrik olarak ayrılıyor mu?"

$$
(X_i,X_j)
$$

düzleminde noktaları çiziyorsun.

Bu:

**feature-space visualization**

---

## Aşama 4 — Ex03

### "Feature ölçeklerini ortaklaştırabilir miyim?"

Ölçekleri:

$$
z=\frac{x-\mu}{\sigma}
$$

ile düzenliyorsun.

Bu:

**standardization / feature scaling**

---

## Aşama 5 — Ex04

### "Feature'ları sabit bir aralığa taşıyabilir miyim?"

Örneğin:

$$
x'=
\frac{x-x_{\min}}
{x_{\max}-x_{\min}}
$$

ile [0,1] aralığına getiriyorsun.

Bu:

**normalization / Min-Max scaling**

---

## Aşama 6 — Ex05

### "Artık model geliştirirken veriyi nasıl ayıracağım?"

```text
Training
Validation
Testing
```

ayrımını öğreniyorsun.

Bu:

**dataset splitting / model evaluation setup**

---

# Ve aslında bir sonraki ML projesinde zincir şöyle devam eder

Bu piscine burada bitiyor ama gerçek ML projesine şu şekilde bağlanıyor:

```text
RAW DATA
   │
   ▼
EDA
(Ex00–Ex02)
   │
   ▼
Preprocessing
(Ex03–Ex04)
   │
   ▼
Split
(Ex05)
   │
   ├──────────────┐
   ▼              ▼
Training       Validation
   │              │
   ▼              │
Fit model         │
   │              │
   └──────┬───────┘
          ▼
   Model selection
   / hyperparameters
          │
          ▼
      Final model
          │
          ▼
       Test data
          │
          ▼
   Final evaluation
```

İşte burada gerçek **machine learning workflow** ortaya çıkıyor.

---

# Çok önemli bir bağlantı: Ex01 neden scaling gerektirmiyordu?

Bu da bütün resmi birbirine bağlayan güzel bir nokta.

Pearson correlation:

$$
r=
\frac{Cov(X,Y)}
{\sigma_X\sigma_Y}
$$

olduğu için lineer ölçeklemeler korelasyonun değerini değiştirmez:

$$
corr(X,Y)
=
corr(aX+b,Y)
$$

(\(a>0\) için).

Dolayısıyla Ex01'de:

```text
raw data
   ↓
Pearson correlation
```

yapmak yeterli.

Ex03'te scaling istemelerinin sebebi **correlation için gerekli olması değil**.

Scaling'in asıl önemi daha sonra gelecek **ML algoritmaları için veri hazırlamak**.

Yani egzersizler birbirleriyle çelişmiyor.

---

# Ex00 → Ex05 arasındaki kavramsal gelişim

Bence bunu şu altı soruyla ezberlemek çok daha faydalı:

| Ex | Sorduğumuz soru | Alan |
|---|---|---|
| **00** | Veriler nasıl dağılıyor? | EDA |
| **01** | Feature ile target arasında ilişki var mı? | Correlation analysis |
| **02** | İki feature sınıfları görsel olarak ayırabiliyor mu? | Feature-space visualization |
| **03** | Feature ölçeklerini ortaklaştırabilir miyim? | Standardization |
| **04** | Feature'ları sabit bir aralığa taşıyabilir miyim? | Normalization |
| **05** | Veriyi model geliştirme ve değerlendirme için nasıl bölerim? | Train/Validation/Test split |

Bunun arkasındaki daha büyük soru ise:

$$
\boxed{\text{"Bu veriden güvenilir bir ML modeli çıkarmaya hazır mıyım?"}}
$$

Ex00–Ex02:

> **Veriyi anlamaya çalış.**

Ex03–Ex04:

> **Veriyi modelleme için uygun hale getir.**

Ex05:

> **Modeli adil biçimde geliştirebilmek ve değerlendirebilmek için veriyi ayır.**

---

## Bir de senin özellikle önem verdiğin "her şeyin gerekçesi olmalı" açısından

Bu projede şu ayrımları kafanda tutarsan, egzersizler artık birbirinden kopuk görünmez:

```text
Histogram
    ↓
"Ne var?"

Correlation
    ↓
"Ne ile ilişkili?"

Scatter
    ↓
"Birlikte nasıl ayrılıyor?"

Standardization
    ↓
"Ölçek problemini nasıl yönetirim?"

Normalization
    ↓
"Başka bir ölçekleme yöntemi nasıl çalışır?"

Split
    ↓
"Modeli nasıl dürüstçe değerlendiririm?"
```

Ve **çok önemli bir nüans**:

Ex00–Ex04'te yaptığın işlemlerin çoğu henüz "model kurmak" değil. Bunlar **model kurmadan önce ve model kurarken kullanılan veri analizi/preprocessing araçlarını tanımak**. Ex05 ise ilk defa doğrudan model geliştirme sürecinin deneysel tasarımına, yani training/validation/test ayrımına giriyor.

Bu yüzden şu an Ex03'te `StandardScaler` kullanırken “neden Test'in ortalamasını 0 yapmıyoruz?” diye sormana aslında **ML pipeline mantığını doğru yerden sorguluyorsun**. Bu noktadan sonra en önemli kavramlardan biri de **"fit etmek veri hakkında bilgi öğrenmektir; transform etmek öğrenilmiş dönüşümü uygulamaktır"** ayrımı. Bu ayrımı oturttuğunda scaler, encoder, imputer ve hatta bazı feature-selection yöntemlerinin neden yalnızca training data üzerinde `fit` edildiği çok daha doğal hale gelir.


---

# DS_4 PIPELINE

## Büyük resim: DS_4'te aslında ne yapıyoruz?

DS_3'te ağırlıklı olarak **veriyi tanıdık, ilişkileri inceledik, görselleştirdik, ölçeklendirdik ve validation için veri ayırdık**. DS_4 ise bunun doğal devamı: artık elimizdeki verilerden gerçekten **sınıflandırma modelleri kuruyor, bu modellerin performansını ölçüyor, feature'ları sadeleştiriyor ve birden fazla modeli birleştiriyoruz**.

DS_4 subject'i kendisini "The futur" olarak tanımlıyor ve veri bilimcisinin geçmiş verilerden otomatik öğrenme modelleriyle "geleceği" tahmin etme rolünden söz ediyor. fileciteturn3file0L2-L5 fileciteturn3file0L45-L52

En yukarıdan bakarsak:

```text
                         DS_3'TEN GELEN VERİ
                                  │
                                  ▼
                    Training / Validation / Test
                                  │
                                  ▼
                 ┌──────────────────────────────┐
                 │ Ex00: Confusion Matrix      │
                 │ Model sonucu doğru mu?      │
                 └──────────────┬───────────────┘
                                │
                                ▼
                 ┌──────────────────────────────┐
                 │ Ex01: Heatmap / Correlation  │
                 │ Feature'lar nasıl ilişkili?  │
                 └──────────────┬───────────────┘
                                │
                                ▼
                 ┌──────────────────────────────┐
                 │ Ex02: Variance                │
                 │ Hangi boyutlar bilgi taşıyor?│
                 └──────────────┬───────────────┘
                                │
                                ▼
                 ┌──────────────────────────────┐
                 │ Ex03: VIF / Feature Selection│
                 │ Redundant feature'ları azalt  │
                 └──────────────┬───────────────┘
                                │
                                ▼
                 ┌──────────────────────────────┐
                 │ Ex04: Tree / Random Forest   │
                 │ İlk gerçek sınıflandırıcı    │
                 └──────────────┬───────────────┘
                                │
                                ▼
                 ┌──────────────────────────────┐
                 │ Ex05: KNN                    │
                 │ Farklı bir sınıflandırıcı    │
                 └──────────────┬───────────────┘
                                │
                                ▼
                 ┌──────────────────────────────┐
                 │ Ex06: Voting Classifier      │
                 │ Modelleri birleştir          │
                 └──────────────────────────────┘
```

Subject'in belirlediği sıra da tam olarak Ex00'dan Ex06'ya bu şekilde ilerliyor: Confusion Matrix, Heatmap, Variances, Feature Selection, Tree, KNN ve Voting Classifier. fileciteturn3file0L55-L65 fileciteturn3file0L81-L88 fileciteturn3file0L91-L100 fileciteturn3file0L127-L138 fileciteturn3file0L148-L160 fileciteturn3file0L299-L312 fileciteturn3file0L323-L333

---

# Ex00 — Confusion Matrix

Subject burada senden **confusion matrix'i hesaplamanı, yazdırmanı ve görüntülemeni** istiyor. Hesaplamaları kendin yapman gerekiyor; yalnızca grafiği göstermek için kütüphane kullanabilirsin. Ayrıca bu egzersizi daha sonra tekrar kullanacağın özellikle belirtiliyor. fileciteturn3file0L55-L66

## Veri bilimi / ML açısından adı ne?

**Classification evaluation** yani sınıflandırma modelinin sonuçlarını değerlendirme.

Confusion matrix'in temel amacı:

> **Modelin hangi sınıfları doğru, hangilerini yanlış tahmin ettiğini sayısal olarak görmek.**

İkili sınıflandırmada temel dört sayı vardır:

```text
True Positive   (TP)
True Negative   (TN)
False Positive  (FP)
False Negative  (FN)
```

Örneğin gerçek sınıf ile model tahminini karşılaştırırsın:

```text
                    Tahmin
                 Jedi    Sith
Gerçek Jedi        TP      FN
Gerçek Sith        FP      TN
```

Buradaki satır/sütun yönünün kullandığın implementasyonda açıkça tanımlanması önemlidir; subject'in örneğinde yalnızca sayısal matrix gösteriliyor. Subject'in verdiği örnekte matrix:

```text
[[25 24]
 [30 21]]
```

ve bunun yanında precision, recall, f1-score ve accuracy yazdırılıyor. fileciteturn3file0L69-L77

---

## Precision, Recall, F1 ve Accuracy neden var?

### Precision

$$
Precision = \frac{TP}{TP+FP}
$$

Modelin "pozitif" dediği örneklerin ne kadarı gerçekten pozitiftir?

### Recall

$$
Recall = \frac{TP}{TP+FN}
$$

Gerçekte pozitif olanların ne kadarını yakaladık?

### F1-score

$$
F1 = 2\frac{Precision\cdot Recall}{Precision+Recall}
$$

Precision ile recall'un harmonik ortalamasıdır. İkisini birlikte yüksek tutmayı ister.

### Accuracy

$$
Accuracy = \frac{TP+TN}{TP+TN+FP+FN}
$$

Toplam örneklerin ne kadarını doğru sınıflandırdık?

---

## Ex00'ın büyük amacı

Ex00 aslında:

> **"Bir modelin tahminlerini nasıl ölçerim?"**

sorusunu öğretiyor.

Bundan sonra Ex04, Ex05 ve Ex06'da gerçekten modeller kurduğunda artık:

```text
model
   ↓
predictions
   ↓
truth ile karşılaştır
   ↓
confusion matrix
   ↓
precision / recall / F1
```

zincirini kullanacaksın.

Subject'in "You will have to re-use this exercice later on" demesinin nedeni de tam olarak bu değerlendirme altyapısının sonraki modeller için tekrar kullanılacak olmasıdır. fileciteturn3file0L64-L66

---

# Ex01 — Heatmap / Correlation

Subject Ex01'te veriler arasındaki **correlation coefficient**'ları görmek için bir heatmap oluşturmanı istiyor. fileciteturn3file0L81-L88

## Veri bilimi açısından adı ne?

**Correlation analysis** ve **feature relationship visualization**.

Ex00'da bir modelin sonucunu değerlendiriyorduk. Burada tekrar verinin kendisine dönüyoruz ve feature'ların **birbirleriyle nasıl ilişkili olduğunu** görmeye çalışıyoruz.

Örneğin:

$$
corr(X_1,X_2)
$$

çok yüksekse, iki feature benzer doğrusal bilgi taşıyor olabilir.

Heatmap bunu bütün feature çiftlerini tek bir tabloda görmemizi sağlar:

```text
             X1      X2      X3      X4
X1          1.00    0.91    0.12    0.05
X2          0.91    1.00    0.18    0.03
X3          0.12    0.18    1.00    0.72
X4          0.05    0.03    0.72    1.00
```

Renkler, yüksek pozitif / negatif ve düşük korelasyonları hızlı görmeyi sağlar.

---

## Neden bunu yapıyoruz?

Çünkü feature'lar arasında ciddi ilişki varsa:

```text
X1 ─────────────┐
                ├── benzer bilgi
X2 ─────────────┘
```

olabilir.

Bu durum özellikle **multicollinearity** kavramına götürür.

Yani:

> Bir feature'ı diğer feature'larla büyük ölçüde açıklayabiliyor muyuz?

sorusu ortaya çıkar.

Bu, doğrudan Ex03'te kullanacağımız VIF kavramına bağlanıyor.

Dolayısıyla Ex01'in büyük amacı:

> **"Feature'lar arasında ne kadar redundant / ilişkili bilgi var?"**

konusuna hazırlık yapmak.

Subject yalnızca heatmap ve correlation coefficient gereksinimini açıkça yazıyor; burada hangi sonraki yöntemle devam edileceğini ayrıca açıklamıyor. fileciteturn3file0L81-L88

---

# Ex02 — Variances

Subject burada her skill'in variance'ını hesaplamanı, variance'ları toplamanı, **%90 seviyesine ulaşmak için kaç component gerektiğini** bulmanı ve cumulative variance'ı gösteren bir grafik çizmeni istiyor. fileciteturn3file0L91-L100

Örnek çıktıda da variance yüzdeleri ile cumulative variance yüzdeleri veriliyor. İlk birkaç component toplam varyansın büyük kısmını taşıyor ve cumulative değer %90'ı geçiyor. fileciteturn3file0L101-L118

## Veri bilimi açısından adı ne?

Bu egzersiz:

**variance analysis / dimensionality reduction preparation**

olarak düşünülebilir.

İstenen "component" ve "cumulative variance" kavramları, doğal olarak **Principal Component Analysis (PCA)** ile çok yakından ilişkilidir. Ancak subject'in bu bölümde PCA adını açıkça kullanmadığını da not etmek gerekir; metinde doğrudan variance ve components üzerinden görev tanımlanıyor. fileciteturn3file0L94-L100

---

## Variance neden önemli?

Bir feature'ın variance'ı kabaca:

$$
Var(X)=\frac{1}{n}\sum_{i=1}^{n}(x_i-\bar{x})^2
$$

şeklindedir.

Variance yüksekse veri o eksende daha fazla yayılmıştır.

Buradaki daha büyük fikir:

> **Verideki değişkenliğin ne kadarı az sayıda boyutta toplanıyor?**

Örneğin 30 feature varsa:

```text
Feature space:

X1 X2 X3 X4 ... X30
```

ama toplam varyansın büyük kısmı ilk birkaç component tarafından açıklanabiliyorsa, daha düşük boyutlu bir temsil düşünmek mümkün olabilir.

Bu konu **dimensionality reduction** alanına girer.

---

## Cumulative variance neden çiziliyor?

Örneğin:

```text
Component 1 → 44.9%
Component 2 → 18.5%
Component 3 →  9.2%
Component 4 →  6.4%
...
```

olsun.

Cumulative:

```text
1 component  → 44.9%
2 components → 63.4%
3 components → 72.6%
4 components → 79.0%
...
7 components → 90.45%
```

gibi ilerleyebilir.

Böylece:

> "Toplam değişkenliğin yaklaşık %90'ını korumak için kaç boyut gerekiyor?"

sorusuna cevap verebilirsin.

---

# Ex03 — Feature Selection / VIF

Subject açıkça veride **multicollinearity** olduğunu söylüyor ve bunu tespit etmek için **Variance Inflation Factor (VIF)** kullanmanı istiyor. Ayrıca VIF'i gösterip yalnızca VIF'i 5'in altına düşüren feature'ları tutmanı istiyor. fileciteturn3file0L127-L138

## Veri bilimi açısından adı ne?

**Feature selection** ve daha özel olarak:

**multicollinearity detection with VIF**.

---

## Multicollinearity nedir?

Örneğin:

$$
X_2 \approx 3X_1
$$

gibi çok güçlü bir ilişki varsa, `X1` ve `X2` neredeyse aynı bilgiyi taşıyor olabilir.

Bir lineer model kurduğunu düşün:

$$
y=\beta_0+\beta_1X_1+\beta_2X_2
$$

Eğer `X1` ve `X2` birbirine çok benziyorsa, modelin "hangisinin etkisi ne kadar?" sorusunu kararlı biçimde cevaplaması zorlaşabilir.

---

## VIF ne yapıyor?

Her feature için diğer feature'ların onu ne kadar açıklayabildiğini ölçer.

Standart tanım:

$$
VIF_j = \frac{1}{1-R_j^2}
$$

Buradaki \(R_j^2\), `X_j` feature'ını diğer feature'larla açıklayan regresyonun determination coefficient'ıdır.

Eğer:

$$
R_j^2\rightarrow1
$$

ise:

$$
VIF_j\rightarrow\infty
$$

olur.

Yani feature diğer feature'lar tarafından neredeyse tamamen açıklanabiliyor demektir.

Subject ayrıca tolerance değerini de örnek çıktıda gösteriyor. Tolerance ile VIF arasındaki standart ilişki:

$$
Tolerance = \frac{1}{VIF}
$$

şeklindedir. Subject'in örnek çıktısında her feature için VIF ve Tolerance birlikte gösteriliyor. fileciteturn3file0L137-L145

---

## Neden feature selection yapıyoruz?

Amaç sadece feature sayısını azaltmak değildir.

Asıl amaçlardan biri:

```text
çok sayıda feature
       ↓
çok miktarda redundant bilgi
       ↓
modelin gereksiz karmaşıklığı
       ↓
daha problemli / daha zor yorumlanan yapı
```

yerine:

```text
daha az ama daha az redundant feature
```

elde etmektir.

Bu işleme:

**feature selection**

denir.

Burada subject'in verdiği seçim kuralı özellikle:

$$
VIF < 5
$$

olacak şekilde feature'ları tutmaktır. fileciteturn3file0L136-L138

VIF bir "feature iyi/kötü" skoru değildir; esas olarak **feature'lar arasındaki çoklu doğrusal bağımlılık** konusunda teşhis aracıdır.

---

# Ex04 — Decision Tree / Random Forest

Artık gerçek bir supervised learning modeline geçiyoruz.

Subject iki seçenek veriyor:

- **Decision Tree Classifier**
- **Random Forest Classifier**

Ayrıca ağacı grafik olarak göstermeni, `Train_knight.csv` ve `Test_knight.csv` dosyalarını argüman olarak almanı, `Tree.txt` dosyasına satır satır `Jedi` / `Sith` tahminleri yazmanı ve minimum **90% F1-score** sağlamanı istiyor. Subject ayrıca DS_3'ten gelen `Training_knight.csv` ve `Validation_knight.csv` dosyalarına muhtemelen ihtiyaç duyacağını belirtiyor. fileciteturn3file0L148-L160 fileciteturn3file0L163-L167 fileciteturn3file0L293-L295

## Veri bilimi açısından adı ne?

**Supervised classification**.

Daha özel olarak:

**Decision Tree classification**

veya:

**Random Forest classification**.

Artık elimizde:

$$
X = \text{feature'lar}
$$

ve:

$$
y = \text{Jedi/Sith}
$$

var ve modelden:

$$
\hat{y}=f(X)
$$

öğrenmesini bekliyoruz.

---

# Decision Tree'nin temel fikri

Decision Tree, feature uzayını ardışık sorularla böler.

Örneğin:

```text
             Strength < 0.49 ?
                /         \\
              Evet        Hayır
              /             \\
      Prescience < 0.01 ?   Sith
         /      \\
      Jedi      Sith
```

Yani model:

> "Şu feature şu eşikten küçük mü?"

gibi kararlar vererek sonunda sınıfa ulaşır.

Subject'in örnek ağacında `X[27] <= 0.489`, `X[20] <= 0.345` gibi eşikler ve her node için `gini`, `samples`, `value` değerleri gösteriliyor. fileciteturn3file0L163-L181

### Gini nedir?

Decision tree node'undaki sınıf karışıklığını ölçen impurity ölçülerinden biridir:

$$
Gini=1-\sum_k p_k^2
$$

Bir node safsa, yani bütün örnekler aynı sınıftaysa:

$$
Gini=0
$$

olur.

Subject'in örnek ağacında da birçok saf node için `gini = 0.0` görülüyor. fileciteturn3file0L210-L218

---

# Random Forest nedir?

Tek bir karar ağacı yerine çok sayıda karar ağacını bir araya getiren bir **ensemble learning** yöntemidir.

Temel fikir kabaca:

```text
Training data
     │
     ├── Tree 1
     ├── Tree 2
     ├── Tree 3
     ├── ...
     └── Tree N
             │
             ▼
          voting
             │
             ▼
        final class
```

Ağaçlar farklı örneklemeler ve rastgele feature seçimleriyle çeşitlendirilir. Böylece tek bir ağaca göre daha toplu bir karar elde edilir.

Subject'in verdiği seçenek "Decision Tree Classifier or Random Forest Classifier" olduğu için Ex04'te bu iki model ailesinden biriyle çalışabilirsin. fileciteturn3file0L151-L156

---

## Ex04'ün büyük amacı

Buraya kadar:

```text
Ex00 → modeli nasıl değerlendiririm?
Ex01 → feature'lar birbirleriyle nasıl ilişkili?
Ex02 → verideki varyans nasıl dağılmış?
Ex03 → redundant feature'ları nasıl azaltırım?
```

Artık:

> **"Bu feature'lardan gerçekten bir sınıflandırıcı öğrenebilir miyim?"**

sorusuna geçiyoruz.

---

# Ex05 — KNN

Subject Ex05'te **K-Nearest Neighbours (KNN)** modeli kurmanı, validation verisi üzerinde farklı `k` değerlerine göre precision'ı hesaplamanı, grafiği göstermenı ve minimum **92% F1-score** elde etmeni istiyor. Ayrıca `Training_knight.csv` ve `Validation_knight.csv` dosyalarına ihtiyaç duyacağını belirtiyor. fileciteturn3file0L299-L312 fileciteturn3file0L315-L320

## Veri bilimi açısından adı ne?

**Instance-based / distance-based supervised classification**.

KNN'nin temel fikri çok basit:

> **Yeni bir noktanın sınıfını, feature uzayındaki en yakın örneklerine bakarak tahmin et.**

Örneğin \(k=5\) ise:

```text
Yeni nokta
    ●

  ● Jedi
    ● Jedi
  ● Sith
    ● Jedi
      ● Sith
```

En yakın 5 komşunun çoğunluğu Jedi ise model Jedi tahmini yapabilir.

---

# `k` neden önemli?

`k`, komşuluk büyüklüğünü belirleyen **hyperparameter**'dır.

### Küçük k

Model çok lokal karar verir.

```text
k = 1
```

gibi durumda tek bir komşunun sınıfı çok etkili olur.

### Büyük k

Daha geniş bir bölgenin ortalama davranışına bakılır.

Ama çok büyük `k`, lokal yapıları fazla yumuşatabilir.

Dolayısıyla:

> **Uygun `k` değerini seçmek gerekir.**

Subject'in özellikle validation verisinde `k` değerine göre precision hesaplamanı istemesi bunun içindir. fileciteturn3file0L306-L311

---

# Burada DS_3 neden yeniden önemli?

KNN mesafeye dayanır.

Örneğin Öklid mesafesi:

$$
d(x,y)=
\sqrt{\sum_i(x_i-y_i)^2}
$$

olduğu için feature ölçekleri çok önemlidir.

Eğer:

```text
Feature A → 0–1000
Feature B → 0–1
```

ise A'nın mesafeye katkısı doğal olarak çok daha büyük olabilir.

Bu yüzden DS_3'te öğrendiğin:

- **standardization**
- **normalization**

konuları KNN için doğrudan önem kazanıyor.

İşte DS_3 ile DS_4 arasındaki en güzel bağlantılardan biri bu:

```text
DS_3
scaling
   ↓
DS_4
KNN distance calculation
```

---

## Ex05'in büyük amacı

Ex04'te ağaç tabanlı bir model kurdun.

Ex05'te tamamen farklı bir fikir kullanan:

> **"Ben bir karar ağacı kurmak yerine, yeni noktaya en yakın eğitim örneklerine bakayım."**

yaklaşımını öğreniyorsun.

Ve `Validation` sayesinde `k` gibi bir model ayarını seçmeye başlıyorsun.

Bu, **hyperparameter tuning / model selection** kavramına giriş niteliğinde.

---

# Ex06 — Voting Classifier

Subject burada bir **üçüncü model seçmeni** ve ardından bir **Voting Classifier** oluşturmanı istiyor. Program yine Train/Test'i alıp `Voting.txt` dosyasına `Jedi` / `Sith` tahminleri yazacak ve minimum **94% F1-score** gereksinimi var. Subject, Training ve Validation dosyalarına da muhtemelen ihtiyaç duyacağını söylüyor. fileciteturn3file0L323-L333 fileciteturn3file0L337-L339

## Veri bilimi açısından adı ne?

**Ensemble learning**.

Daha özel olarak:

**Voting classifier**.

Temel fikir:

```text
             Model 1
                │
                ├─────┐
             Model 2│  │
                │   │  │
                ├───┤  │
             Model 3│  │
                │   │  │
                └───┴──┘
                    │
                 voting
                    │
                    ▼
              final prediction
```

Yani tek bir modelin kararına güvenmek yerine farklı modellerin tahminlerini bir araya getiriyorsun.

Subject'in "third model" demesinin nedeni, Ex04 ve Ex05'te kullandığın model ailelerine ek olarak başka bir model daha seçip ensemble'a dahil etmen. Subject hangi üçüncü modeli seçmen gerektiğini belirtmiyor. fileciteturn3file0L326-L331

---

# Voting neden işe yarayabilir?

Farklı modeller aynı hataları yapmak zorunda değildir.

Örneğin:

```text
Model A → Jedi
Model B → Sith
Model C → Jedi
```

ise majority voting sonucu:

```text
Jedi
```

olabilir.

Büyük fikir:

> **Farklı modellerin kararlarını birleştirerek tek bir modelin hatasını azaltmaya çalışmak.**

Bu yüzden buna:

**ensemble method**

denir.

Burada "azaltmak" bir hedef / yöntem motivasyonudur; belirli bir veri setinde gerçekten daha iyi performans vereceği ancak validation/test sonuçlarıyla görülür.

---

# DS_4'ün bütün hikâyesi

Şimdi bütün egzersizleri tek bir zincir halinde okuyalım:

```text
DS_3'TEN GELEN HAZIR VERİ
            │
            ▼
Ex00 — Confusion Matrix
"Tahminlerimi nasıl ölçerim?"
            │
            ▼
Ex01 — Correlation Heatmap
"Feature'lar birbirleriyle nasıl ilişkili?"
            │
            ▼
Ex02 — Variance
"Değişkenlik hangi boyutlarda yoğun?"
            │
            ▼
Ex03 — VIF / Feature Selection
"Birbirinin tekrarını yapan feature'ları nasıl azaltırım?"
            │
            ▼
Ex04 — Tree / Random Forest
"Bir supervised classifier öğrenebilir miyim?"
            │
            ▼
Ex05 — KNN
"Farklı bir, mesafeye dayalı classifier nasıl çalışıyor?"
            │
            ▼
Ex06 — Voting
"Birden fazla modelin kararını birleştirebilir miyim?"
```

Bu yüzden DS_4, DS_3'ün devamı olarak okununca daha anlamlı hale geliyor:

```text
DS_3
────
Veriyi anla
   ↓
Feature ilişkilerini incele
   ↓
Feature-space'i görselleştir
   ↓
Feature'ları ölçeklendir
   ↓
Train / Validation ayır

                ↓↓↓

DS_4
────
Model performansını ölç
   ↓
Feature ilişkilerini tekrar incele
   ↓
Varyansı değerlendir
   ↓
Multicollinearity'yi azalt
   ↓
Decision Tree / Random Forest
   ↓
KNN
   ↓
Voting ensemble
```

---

# DS_3 → DS_4: Makine öğrenmesi açısından asıl büyük resim

İki modülü tek bir gerçek ML projesinin hazırlık ve modelleme aşamaları gibi düşünürsek:

```text
                    RAW DATA
                       │
                       ▼
              Exploratory Analysis
              (DS_3 Ex00–Ex02)
                       │
                       ▼
                 Preprocessing
              (DS_3 Ex03–Ex04)
                       │
                       ▼
              Dataset Partitioning
                 (DS_3 Ex05)
                       │
                       ▼
             Feature Diagnostics
              (DS_4 Ex01–Ex03)
                       │
                       ▼
                Model Training
              (DS_4 Ex04–Ex06)
                       │
             ┌─────────┴─────────┐
             ▼                   ▼
         Validation             Test
             │                   │
             ▼                   ▼
     model / k / seçim      final prediction
             │
             └─────────┬─────────┘
                       ▼
               Performance Metrics
             (Confusion Matrix / F1)
```

Burada önemli olan, bütün adımların aynı anda her projede aynı sırayla uygulanmak zorunda olduğu fikrine kapılmamak. Gerçek projelerde EDA, preprocessing, feature selection, model seçimi ve validation arasında ileri-geri iterasyonlar olabilir. Bu piscine ise bu temel kavramları ayrı egzersizler halinde tanıtıyor.

## Altı temel soru yerine artık on iki temel soru

DS_3'teki soruların üzerine DS_4'te şunlar ekleniyor:

```text
DS_3
00  Veriler nasıl dağılıyor?
01  Feature ile target arasında ilişki var mı?
02  İki feature birlikte sınıfları ayırabiliyor mu?
03  Feature'ları nasıl standardize ederim?
04  Feature'ları nasıl normalize ederim?
05  Veriyi training / validation / test için nasıl ayırırım?

DS_4
00  Modelin doğru ve yanlış tahminlerini nasıl ölçerim?
01  Feature'lar birbirleriyle ne kadar ilişkili?
02  Varyans hangi boyutlarda toplanıyor?
03  Multicollinearity'yi nasıl tespit edip azaltırım?
04  Bir karar ağacı / random forest nasıl sınıflandırır?
05  Komşuluk ve mesafe üzerinden nasıl sınıflandırırım?
06  Birden fazla modelin kararını nasıl birleştiririm?
```

Böyle baktığında DS_3 ve DS_4 artık birbirinden kopuk egzersizler değil; **veriyi tanıma → veriyi hazırlama → feature'ları inceleme/seçme → modelleri kurma → modelleri değerlendirme → modelleri birleştirme** çizgisinde ilerleyen bir öğrenme zinciri haline geliyor.
