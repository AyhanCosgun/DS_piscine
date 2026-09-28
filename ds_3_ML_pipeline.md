# Büyük resim: Aslında bu 6 egzersizde ne yapıyoruz?

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

\[
X
\]

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

\[
X = \text{feature}
\]

ve

\[
Y = \text{knight}
\]

var.

Mesela:

\[
X=\text{Strength}
\]

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

\[
r_{X,Y}
\]

Örneğin subject'in örneğinde:

\[
\text{corr(Empowered, knight)}=0.793566
\]

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

\[
Y\in\{0,1\}
\]

ve böylece:

\[
corr(X,Y)
\]

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

\[
(X_1,X_2)
\]

Örneğin:

```text
x = Empowered
y = Prescience
```

Her knight artık düzlemde bir nokta:

\[
(x_i,y_i)
\]

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

\[
corr(X_1,Y)
\]

ve

\[
corr(X_2,Y)
\]

ölçtün.

Ex02'de ise artık:

\[
(X_1,X_2)
\]

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

\[
z=\frac{x-\mu}{\sigma}
\]

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

\[
d(x,y)
=
\sqrt{
(x_1-y_1)^2+
(x_2-y_2)^2
}
\]

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

\[
0\le x\le1,\qquad 0\le y\le1
\]

aralığında olması ve örnek çıktıda `0.52`, `0.02`, `0.54`, ... gibi değerler verilmesi, burada **Min-Max benzeri [0,1] normalization** kullanıldığını güçlü biçimde düşündürüyor. Fakat subject metni kullanılan formülü açıkça yazmıyor; yalnızca "Normalize" diyor. fileciteturn2file0

Tipik formül:

\[
x'=
\frac{x-x_{\min}}
{x_{\max}-x_{\min}}
\]

Böylece:

\[
x_{\min}\rightarrow0
\]

ve

\[
x_{\max}\rightarrow1
\]

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

\[
X
\rightarrow
Z
\]

veya

\[
X
\rightarrow
X'
\]

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

\[
P(X)
\]

hakkında fikir edinmeye çalışıyorsun.

Dağılım, yayılım, outlier, farklı sınıf dağılımları...

Bu:

**EDA**

---

## Aşama 2 — Ex01

### "Feature ile hedef arasında ilişki var mı?"

\[
corr(X_i,Y)
\]

hesaplıyorsun.

Bu:

**association / correlation analysis**

---

## Aşama 3 — Ex02

### "Feature'ları birlikte ele alırsam sınıflar geometrik olarak ayrılıyor mu?"

\[
(X_i,X_j)
\]

düzleminde noktaları çiziyorsun.

Bu:

**feature-space visualization**

---

## Aşama 4 — Ex03

### "Feature ölçeklerini ortaklaştırabilir miyim?"

Ölçekleri:

\[
z=\frac{x-\mu}{\sigma}
\]

ile düzenliyorsun.

Bu:

**standardization / feature scaling**

---

## Aşama 5 — Ex04

### "Feature'ları sabit bir aralığa taşıyabilir miyim?"

Örneğin:

\[
x'=
\frac{x-x_{\min}}
{x_{\max}-x_{\min}}
\]

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

\[
r=
\frac{Cov(X,Y)}
{\sigma_X\sigma_Y}
\]

olduğu için lineer ölçeklemeler korelasyonun değerini değiştirmez:

\[
corr(X,Y)
=
corr(aX+b,Y)
\]

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

\[
\boxed{\text{"Bu veriden güvenilir bir ML modeli çıkarmaya hazır mıyım?"}}
\]

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
