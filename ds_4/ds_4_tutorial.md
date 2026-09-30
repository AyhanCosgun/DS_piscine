# DS_4 TUTORIAL — The Future

> **Amaç:** DS_4 subject'ini yalnızca egzersizleri tek tek çözmek yerine, bir makine öğrenmesi pipeline'ının parçaları olarak anlamak.
>
> Bu dokümanda her egzersiz için şu dört soruya cevap verilir:
>
> 1. **Ne yapıyoruz?**
> 2. **Nasıl yapıyoruz?** — Python / kod mantığı
> 3. **Neden yapıyoruz?** — Data Science / Machine Learning açısından amacı
> 4. **Hangi literatür terimlerini bilmeliyim?**
>
> Subject'in kendi metninde açıkça verilen gereksinimler ile genel Machine Learning bilgisine dayanan açıklamalar birbirinden ayrılmaya çalışılmıştır. Subject bazı yerlerde yöntemi/formülü özellikle belirtmez; bu durumda ilgili yorum açıkça **çıkarım** olarak belirtilir.

---

# 0. Büyük Resim — DS_3'ten DS_4'e geçiş

DS_3'te ağırlıklı olarak veriyi **anlamaya ve hazırlamaya** çalıştık:

```text
DS_3

Ex00  Histogram
      ↓
      Verinin dağılımını gör

Ex01  Correlation
      ↓
      Feature ↔ target ilişkisini ölç

Ex02  Scatter plots
      ↓
      Feature space içinde sınıfları gör

Ex03  Standardization
      ↓
      Feature ölçeklerini düzenle

Ex04  Normalization
      ↓
      Feature'ları başka bir ortak ölçeğe getir

Ex05  Split
      ↓
      Training / Validation ayrımı yap
```

DS_4 artık bunun üzerine **modelleme ve model değerlendirme** ekliyor.

```text
DS_4

Ex00  Confusion Matrix
      ↓
      Bir sınıflandırıcının hatalarını ölç

Ex01  Heatmap / Correlation
      ↓
      Feature'ların birbirleriyle ilişkisini gör

Ex02  Variance / PCA mantığı
      ↓
      Verinin varyansını hangi bileşenler taşıyor?

Ex03  VIF / Feature Selection
      ↓
      Birbirini tekrar eden feature'ları belirle

Ex04  Decision Tree / Random Forest
      ↓
      İlk gerçek sınıflandırma modeli

Ex05  KNN
      ↓
      Mesafe tabanlı ikinci model

Ex06  Voting Classifier
      ↓
      Birden fazla modelin kararını birleştir
```

Büyük resim artık şöyle okunabilir:

```text
                  DATA
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
            Train / Validation split
              (DS_3 Ex05)
                    │
                    ▼
           Feature relationships
              (DS_4 Ex01–Ex03)
                    │
                    ▼
             Model development
              (DS_4 Ex04–Ex06)
                    │
                    ▼
             Validation / metrics
                    │
                    ▼
             Final Test prediction
```

Bu nedenle DS_4'ün başındaki Ex00 aslında "model kurmadan önce evaluation metriğini kendin yaz" diyerek başlıyor; son üç egzersizde ise gerçek classifier'lara geçiliyor.

---

# 1. Temel kavramlar — DS_4 boyunca sürekli karşılaşacağımız sözlük

## 1.1 Classification

**Classification (sınıflandırma)**, bir gözlemi önceden tanımlanmış sınıflardan birine atama problemidir.

Bu projede sınıflar:

```text
Jedi
Sith
```

Bir model şunu yapar:

```text
features
   ↓
classifier
   ↓
Jedi / Sith
```

Bu bir **supervised learning** problemidir; çünkü Training verisinde doğru sınıf (`knight`) biliniyor.

---

## 1.2 Feature ve target

Bir satırın özellikleri:

```text
Sensitivity
Hability
Strength
...
Empowered
Burst
Grasping
```

bunlar **features / predictors / input variables**.

`knight` ise **target / response / label**.

Matematiksel olarak:

$$
X = (X_1,X_2,\ldots,X_p)
$$

ve

$$
Y \in \{Jedi,Sith\}.
$$

Modelin görevi kabaca:

$$
X \longrightarrow Y
$$

ilişkisini öğrenmektir.

---

## 1.3 Binary classification

İki sınıf olduğu için buna **binary classification** denir.

Örneğin sayısal gösterimde:

```text
Jedi = 1
Sith = 0
```

kullanılabilir. Ancak modelin nihai çıktısını subject'in istediği gibi `Jedi` / `Sith` olarak dosyaya yazarsın.

---

## 1.4 Prediction ve truth

Bir classifier iki farklı şey üretir:

**Truth / ground truth**

> Gerçek sınıf.

**Prediction**

> Modelin tahmini sınıf.

Örneğin:

```text
truth      prediction
Jedi       Jedi
Jedi       Sith
Sith       Sith
Sith       Jedi
```

İlk ve üçüncü satır doğru; ikinci ve dördüncü yanlış.

Confusion matrix tam olarak bu karşılaştırmayı özetler.

---

# 2. Ex00 — Confusion Matrix

## 2.1 Subject ne istiyor?

DS_4 Ex00'te confusion matrix'i **kendin hesaplaman** isteniyor. Grafik/görüntü göstermek için bir kütüphane kullanılabilir; fakat hesaplamanın kendisi hazır bir metric fonksiyonuna bırakılmamalı.

Program iki dosya alıyor:

```bash
./Confusion_Matrix.* predictions.txt truth.txt
```

ve örnek çıktı olarak precision, recall, F1, accuracy ve:

```text
[[25 24]
 [30 21]]
```

matrisini gösteriyor.

**Önemli:** Subject'in örneğinde matrix'in satırları `truth`, sütunları `prediction` olarak okunabiliyor ve sınıf sırası `Jedi, Sith` kabul edildiğinde verilen precision/recall/F1 değerleriyle tam olarak uyuşuyor.

---

## 2.2 Confusion Matrix nedir?

Binary classification için dört temel sonuç vardır:

| Gerçek | Tahmin | Adı |
|---|---|---|
| Positive | Positive | **TP** — True Positive |
| Negative | Negative | **TN** — True Negative |
| Negative | Positive | **FP** — False Positive |
| Positive | Negative | **FN** — False Negative |

Buradaki "positive" kelimesi doğrudan "iyi" anlamına gelmez. Sadece üzerinde konuştuğumuz sınıfı **positive class** seçtiğimizi ifade eder.

Örneğin `Jedi` positive kabul edilirse:

```text
Actual Jedi, Predicted Jedi → TP
Actual Sith, Predicted Sith → TN
Actual Sith, Predicted Jedi → FP
Actual Jedi, Predicted Sith → FN
```

---

## 2.3 TP, TN, FP, FN'yi gerçekten anlamak

Şu dört soruyu sırayla sor:

1. Gerçekte hangi sınıf?
2. Model hangi sınıfı söyledi?
3. Aynı mı?
4. Positive class hangisi?

Örneğin `Jedi` positive olsun.

### TP

```text
Gerçek  : Jedi
Tahmin  : Jedi
```

Model Jedi dedi ve gerçekten Jedi çıktı.

### TN

```text
Gerçek  : Sith
Tahmin  : Sith
```

Model Sith dedi ve gerçekten Sith çıktı.

### FP

```text
Gerçek  : Sith
Tahmin  : Jedi
```

Model positive dedi ama aslında negative idi.

### FN

```text
Gerçek  : Jedi
Tahmin  : Sith
```

Model positive olan Jedi'ı kaçırdı.

---

## 2.4 Subject'in matrix'ini okuyalım

Subject:

```text
[[25 24]
 [30 21]]
```

Satırlar gerçek sınıf, sütunlar tahmin ve sıra `Jedi, Sith` ise:

```text
                 Prediction
                 Jedi   Sith
Truth   Jedi      25     24
        Sith      30     21
```

Jedi positive alınırsa:

$$
TP=25
$$

$$
FN=24
$$

$$
FP=30
$$

$$
TN=21
$$

Toplam:

$$
25+24+30+21=100.
$$

---

## 2.5 Accuracy

Doğru tahminlerin toplam oranıdır:

$$
Accuracy = \frac{TP+TN}{TP+TN+FP+FN}
$$

Subject örneğinde:

$$
Accuracy=\frac{25+21}{100}=0.46.
$$

Yani `%46`.

**Ne işe yarar?**

Genel olarak kaç tahminin doğru olduğunu söyler.

**Sorunu:** Sınıflar çok dengesizse yanıltıcı olabilir.

Örneğin 100 kişinin 95'i Sith ise, her zaman Sith diyen aptalca bir model bile %95 accuracy alabilir.

---

## 2.6 Precision

"Model positive dediği durumların ne kadarı gerçekten positive?"

$$
Precision=\frac{TP}{TP+FP}
$$

Subject örneğinde Jedi için:

$$
Precision=\frac{25}{25+30}=0.4545\ldots\approx0.45.
$$

Yani modelin `Jedi` dediği örneklerin yaklaşık %45'i gerçekten Jedi.

---

## 2.7 Recall

"Gerçekte positive olanların ne kadarını yakaladım?"

$$
Recall=\frac{TP}{TP+FN}
$$

Subject örneğinde Jedi için:

$$
Recall=\frac{25}{25+24}=0.5102\ldots\approx0.51.
$$

Yani gerçek Jedi'ların yaklaşık %51'ini yakalamış.

---

## 2.8 Precision ile Recall farkı

Bu ikisini karıştırmamak için:

### Precision

```text
Ben Jedi dediklerimin ne kadarı Jedi?
```

### Recall

```text
Gerçek Jedi'ların ne kadarını yakaladım?
```

Kısaca:

```text
Precision → prediction merkezli
Recall    → truth merkezli
```

---

## 2.9 F1-score

Precision ile recall'un harmonik ortalamasıdır:

$$
F1=2\frac{Precision\cdot Recall}{Precision+Recall}
$$

Aynı formül eşdeğer olarak:

$$
F1=\frac{2TP}{2TP+FP+FN}.
$$

Harmonik ortalama kullanılmasının nedeni, iki metrikten biri çok düşükse F1'in de düşük kalmasını sağlamaktır.

Örneğin:

```text
Precision = 0.99
Recall    = 0.10
```

olduğunda basit aritmetik ortalama yaklaşık `0.545` olurdu. F1 ise yaklaşık `0.18` çıkar. Bu, modelin iki açıdan dengeli olmadığını daha sert biçimde yansıtır.

---

## 2.10 İki sınıfın F1'i nasıl tek F1 oluyor?

Subject her sınıf için:

```text
Jedi  0.xx
Sith  0.xx
```

gösteriyor.

Subject'in örnek çıktısında her sınıf için `f1-score` veriliyor; ancak metin, ayrıca tek bir 'genel F1-score' istemiyor. Bu nedenle genel bir F1 üretilecekse hangi `averaging` yönteminin (`macro`, `weighted`, `micro` vb.) seçildiği ayrıca belirtilmelidir.

İki sınıflı ve yaklaşık dengeli veri için **macro F1** ve **weighted F1** birbirine yakın olabilir; fakat kavramsal olarak farklı metriklerdir. Bu fark ve nedenleri bu dosyanın sonundaki Ex00 ek bölümünde ayrıntılı olarak açıklanmıştır.

---

## 2.11 Ex00 nasıl kodlanır?

Subject hesaplamayı kendin istediği için aşağıdaki gibi elle yapabilirsin.

```python
from pathlib import Path


def load_labels(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]


def confusion_matrix_manual(predictions, truths):
    # Matrix convention:
    # rows    = truth   -> Jedi, Sith
    # columns = predict -> Jedi, Sith
    matrix = [[0, 0],
              [0, 0]]

    class_to_index = {
        "Jedi": 0,
        "Sith": 1,
    }

    for prediction, truth in zip(predictions, truths):
        row = class_to_index[truth]
        col = class_to_index[prediction]
        matrix[row][col] += 1

    return matrix


def metrics_from_matrix(matrix):
    tp_jedi = matrix[0][0]
    fn_jedi = matrix[0][1]
    fp_jedi = matrix[1][0]
    tn_jedi = matrix[1][1]

    precision_jedi = tp_jedi / (tp_jedi + fp_jedi)
    recall_jedi = tp_jedi / (tp_jedi + fn_jedi)
    f1_jedi = 2 * precision_jedi * recall_jedi / (precision_jedi + recall_jedi)

    # Sith as the positive class:
    tp_sith = matrix[1][1]
    fn_sith = matrix[1][0]
    fp_sith = matrix[0][1]
    tn_sith = matrix[0][0]

    precision_sith = tp_sith / (tp_sith + fp_sith)
    recall_sith = tp_sith / (tp_sith + fn_sith)
    f1_sith = 2 * precision_sith * recall_sith / (precision_sith + recall_sith)

    total = sum(sum(row) for row in matrix)
    accuracy = (matrix[0][0] + matrix[1][1]) / total

    return {
        "Jedi": (precision_jedi, recall_jedi, f1_jedi),
        "Sith": (precision_sith, recall_sith, f1_sith),
        "accuracy": accuracy,
        "total": total,
    }
```

### Buradaki önemli programlama fikri

`confusion_matrix_manual()` yalnızca sayım yapıyor.

`metrics_from_matrix()` ise matrix'ten TP/TN/FP/FN çıkarıp metric'leri hesaplıyor.

Bu ayrım kodu daha anlaşılır yapar.

---

# 3. Ex01 — Heatmap / Correlation

## 3.1 Subject ne istiyor?

Ex01:

> Veriler arasındaki correlation coefficient'ı görmek için bir **heatmap** oluştur.

Bu, DS_3 Ex01'de tek tek feature–target correlation değerlerini yazdırma yaklaşımının genişletilmiş bir hali gibi düşünülebilir.

---

## 3.2 Correlation coefficient nedir?

İki sayısal değişkenin **doğrusal ilişkisinin yönünü ve gücünü** ölçen katsayıdır.

Pearson correlation:

$$
r_{XY}=
\frac{Cov(X,Y)}{\sigma_X\sigma_Y}
$$

ve sonucu:

$$
-1\le r\le1.
$$

Kabaca:

```text
+1 → güçlü pozitif doğrusal ilişki
 0 → doğrusal ilişki yok / çok zayıf
-1 → güçlü negatif doğrusal ilişki
```

**Önemli:** `r = 0`, hiçbir türlü ilişki yok demek değildir; özellikle non-linear ilişkiler Pearson ile yakalanmayabilir.

---

## 3.3 Correlation matrix

30 feature varsa her feature çifti için correlation hesaplanır.

Örneğin:

```text
                  Strength  Empowered  Push
Strength             1.00      0.82     0.15
Empowered            0.82      1.00     0.10
Push                 0.15      0.10     1.00
```

Bu tablo **correlation matrix**.

Diagonal her zaman:

$$
cor(X_i,X_i)=1
$$

olduğu için `1.0` olur.

Matrix simetriktir:

$$
cor(X_i,X_j)=cor(X_j,X_i).
$$

---

## 3.4 Heatmap neden kullanılıyor?

30×30 gibi bir tabloyu okumak zor olabilir.

Heatmap'te büyük pozitif/negatif korelasyonlar görsel olarak öne çıkar.

Dolayısıyla soru artık:

> "Hangi feature'lar birbirini tekrar eden bilgi taşıyor olabilir?"

Bu soru DS_4 Ex03'te doğrudan **multicollinearity** ve VIF'e bağlanıyor.

---

## 3.5 Kod

```python
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


df = pd.read_csv("Train_knight.csv")

features = df.drop(columns="knight")

correlation = features.corr(method="pearson")

plt.figure(figsize=(14, 12))
sns.heatmap(
    correlation,
    cmap="coolwarm",
    center=0,
    square=True
)
plt.tight_layout()
plt.show()
```

### Target'ı da görmek istersen

DS_3 Ex01'de yaptığın gibi `knight`'ı 0/1'e encode ederek matrix'e dahil edebilirsin:

```python
encoded = df.copy()
encoded["knight"] = encoded["knight"].map({"Jedi": 1, "Sith": 0})

correlation = encoded.corr(method="pearson")
```

Bu durumda heatmap hem feature↔feature hem feature↔target ilişkilerini gösterir.

---

# 4. Ex02 — Variance ve PCA bağlantısı

## 4.1 Subject ne istiyor?

Ex02:

- her skill'in variance'ını hesapla,
- varyansları biriktirerek `90` seviyesine kaç component ile ulaşıldığına bak,
- kümülatif toplamı gösteren grafik çiz.

Örnek çıktıda verilen değerler yüzde olarak yaklaşık:

```text
44.896...
18.472...
 9.183...
 6.446...
 ...
```

ve cumulative değerler:

```text
44.896
63.368
72.552
...
90.454
92.018
...
100.000
```

### Burada önemli bir yorum

Subject "variance" diyor; fakat **"components" ve cumulative variance percentage** dili, verilen örneğin normal feature varyanslarından ziyade **PCA explained variance ratio** yaklaşımını işaret ediyor.

Bu nedenle burada PCA açıklaması kullanmak güçlü bir **çıkarımdır**; subject metni `PCA` adını açıkça yazmıyor.

---

## 4.2 Variance nedir?

Variance, verilerin ortalama etrafında ne kadar yayıldığını ölçer.

Bir örneklem için:

$$
s^2=\frac{1}{n-1}\sum_{i=1}^{n}(x_i-\bar{x})^2.
$$

Yüksek variance:

> değerler birbirinden daha yaygın.

Düşük variance:

> değerler birbirine daha yakın.

---

## 4.3 Neden PCA'da variance önemli?

**PCA — Principal Component Analysis**, yüksek boyutlu veriyi daha az sayıda yeni eksenle ifade etmeye çalışır.

Yeni eksenler:

$$
PC_1,PC_2,\ldots,PC_p
$$

olur.

PCA ilk component'i verinin en fazla variance'ını açıklayacak yönde seçer.

Sonraki componentler önceki componentlere dik olacak şekilde kalan variance'ı mümkün olduğunca fazla açıklar.

Bu nedenle:

```text
PC1 → %44.9
PC2 → %18.5
PC3 →  %9.2
...
```

gibi değerler görürsün.

---

## 4.4 Explained variance ratio

Bir component'in açıkladığı varyans oranı:

$$
EVR_i=
\frac{\lambda_i}{\sum_j\lambda_j}
$$

şeklinde ifade edilir.

Burada `lambda_i`, PCA'nın ilgili eigenvalue'su gibi düşünülebilir.

Yüzdeye çevirmek için:

$$
100\times EVR_i.
$$

Cumulative explained variance:

$$
C_i=\sum_{j=1}^{i}EVR_j.
$$

Örneğin:

```text
PC1       44.9%
PC1+PC2   63.4%
PC1–PC3   72.6%
...
PC1–PC7   92.0%
```

Bu şu demektir:

> İlk 7 principal component, toplam variance'ın yaklaşık %92'sini açıklıyor.

---

## 4.5 Neden 90% eşiği?

Bu subject'in seçtiği bir pratik eşik.

Amaç:

```text
30 feature
   ↓
çok daha az sayıda component
   ↓
verinin büyük bölümünü koru
```

Örneğin 30 boyutu 7 boyuta indirip variance'ın %90'ından fazlasını koruyabiliyorsan, **dimensionality reduction** açısından ilginç bir sonuç elde etmiş olursun.

Bu, model için otomatik olarak "7 feature yeterlidir" anlamına gelmez. Principal components artık orijinal feature isimleri değildir; onlar feature'ların lineer kombinasyonlarıdır.

---

## 4.6 Neden DS_3 standardization burada tekrar önemli?

PCA variance'a çok duyarlıdır.

Örneğin:

```text
Feature A → 0–1000
Feature B → 0–1
```

ise A'nın ham variance'ı doğal olarak çok büyük olabilir.

Standardization sonrası:

```text
mean ≈ 0
std  ≈ 1
```

yapmak feature'ların PCA üzerindeki başlangıç ölçek farkını azaltır.

Subject de örnekten çok uzak sonuçlar çıkarsa önceki modülde öğrendiklerini yeniden kullanabileceğini belirtiyor. Bu, scaling'in PCA hazırlığında önemli olduğuna güçlü bir işaret.

---

## 4.7 Kod

```python
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA


df = pd.read_csv("Train_knight.csv")

X = df.drop(columns="knight")

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

pca = PCA()
pca.fit(X_scaled)

variance_percent = pca.explained_variance_ratio_ * 100
cumulative_percent = variance_percent.cumsum()

print("Variances (Percentage):")
print(variance_percent)

print("Cumulative Variances (Percentage):")
print(cumulative_percent)

plt.figure(figsize=(10, 6))
plt.plot(
    range(1, len(cumulative_percent) + 1),
    cumulative_percent,
    marker="o"
)
plt.axhline(90, linestyle="--")
plt.xlabel("Number of components")
plt.ylabel("Cumulative explained variance (%)")
plt.grid(True)
plt.tight_layout()
plt.show()
```

### 90%'a kaç component gerektiğini bulmak

```python
n_components_90 = (cumulative_percent < 90).sum() + 1
print(n_components_90)
```

Daha genel ve güvenli biçimde:

```python
import numpy as np

n_components_90 = np.searchsorted(cumulative_percent, 90) + 1
```

---

# 5. Ex03 — Feature Selection ve VIF

## 5.1 Subject ne istiyor?

Subject:

> Data appears too multicollinear.

> Multicollinearity detection için VIF kullanılacak.

> VIF değerlerini göster.

> VIF'i 5'in altına indirecek feature'ları tut ve feature'ları göster.

Örnek:

```text
Empowered   36.763714   0.027201
Stims      405.023336   0.002469
Prescience  60.041733   0.016655
Recovery   799.105946   0.001251
Strength  3786.400419   0.000264
```

---

## 5.2 Multicollinearity nedir?

**Multicollinearity**, predictor/feature'ların birbirleriyle güçlü biçimde doğrusal ilişkili olmasıdır.

Örneğin:

$$
X_3 \approx 2X_1+5X_2.
$$

Bu durumda `X3` büyük ölçüde diğer feature'ların taşıdığı bilgiyi tekrar ediyor olabilir.

Bir classifier'ın tahmini mutlaka bozulmak zorunda değildir. Fakat özellikle **lineer modellerde** coefficient'ların yorumlanmasını ve stabilitesini zorlaştırabilir.

---

## 5.3 VIF nedir?

**VIF — Variance Inflation Factor**.

Bir feature'ın diğer feature'larla ne kadar açıklanabildiğini ölçen bir multicollinearity göstergesidir.

Feature `X_j` için:

$$
VIF_j=\frac{1}{1-R_j^2}
$$

Buradaki `R_j^2`, `X_j`'yi diğer bütün feature'larla açıklayan yardımcı regresyonun R²'sidir.

---

## 5.4 VIF'in sezgisel anlamı

Eğer `Xj` diğer feature'larla hiç açıklanamıyorsa:

$$
R_j^2\approx0
$$

ve:

$$
VIF_j\approx1.
$$

Bu iyi durumda.

Eğer `Xj`, diğer feature'lar tarafından neredeyse tamamen açıklanabiliyorsa:

$$
R_j^2\rightarrow1
$$

ve:

$$
VIF_j\rightarrow\infty.
$$

Yani çok yüksek VIF:

> "Bu feature'ın bilgisi diğer feature'larla büyük ölçüde tekrar ediyor olabilir."

---

## 5.5 Tolerance nedir?

Subject VIF'in yanında tolerance da gösteriyor.

İlişki:

$$
Tolerance=1/VIF.
$$

Örneğin:

$$
VIF=36.763714
$$

ise:

$$
Tolerance\approx0.027201.
$$

Subject'in örneği bununla uyumlu.

---

## 5.6 Neden VIF < 5?

Subject burada pratik eşik olarak:

$$
VIF<5
$$

istiyor.

Bu evrensel matematik yasası değildir; **bu exercise'in seçtiği threshold**.

Genel uygulamalarda farklı eşikler görebilirsin. Burada subject'in gereksinimi `5` olduğu için onu kullan.

---

## 5.7 VIF nasıl hesaplanır?

`statsmodels` kullanabilirsin:

```python
from statsmodels.stats.outliers_influence import variance_inflation_factor
import pandas as pd


def calculate_vif(X):
    rows = []

    for i, column in enumerate(X.columns):
        vif = variance_inflation_factor(X.values, i)
        rows.append({
            "feature": column,
            "VIF": vif,
            "Tolerance": 1.0 / vif,
        })

    return pd.DataFrame(rows).sort_values("VIF", ascending=False)
```

---

## 5.8 Sadece bir kere filtrelemek yeterli mi?

Her zaman değil.

Örneğin:

```text
A VIF = 200
B VIF = 150
C VIF =   7
```

A'yı silince B ve C'nin VIF'leri değişebilir.

Bu yüzden daha sağlam yaklaşım **iterative feature elimination**:

```text
VIF hesapla
   ↓
VIF > 5 mi?
   ↓ yes
En yüksek VIF'li feature'ı çıkar
   ↓
VIF'i yeniden hesapla
   ↓
Tekrar et
   ↓
Tüm VIF'ler < 5
```

Kod:

```python
from statsmodels.stats.outliers_influence import variance_inflation_factor


def reduce_multicollinearity(X, threshold=5.0):
    X = X.copy()

    while True:
        vif_values = []

        for i in range(X.shape[1]):
            vif_values.append(
                variance_inflation_factor(X.values, i)
            )

        vif = pd.Series(vif_values, index=X.columns)

        max_vif = vif.max()
        max_feature = vif.idxmax()

        if max_vif < threshold:
            break

        print(f"Removing {max_feature}: VIF={max_vif:.3f}")
        X = X.drop(columns=max_feature)

    return X, vif
```

### Neden en yüksek VIF'i çıkarıyoruz?

Bu subject'in `VIF < 5` hedefini hızlı ve anlaşılır şekilde gerçekleştiren doğal bir greedy yaklaşımdır. Başka feature-selection yöntemleri de vardır; subject özellikle VIF kullanmanı istediği için burada bunu kullanıyoruz.

---

## 5.9 VIF ile PCA aynı şey değil

Çok önemli:

### PCA

```text
30 original feature
      ↓
7 principal component
```

Yeni eksenler feature'ların lineer kombinasyonudur.

### VIF selection

```text
30 original feature
      ↓
17 original feature
```

Feature'ları siler ama kalan feature isimleri ve fiziksel anlamları korunur.

Bu nedenle iki yöntem aynı problem alanına dokunsa da **aynı işlem değildir**.

---

# 6. Ex04 — Decision Tree / Random Forest

## 6.1 Subject ne istiyor?

Subject iki seçenek veriyor:

- Decision Tree Classifier
- Random Forest Classifier

ve:

- ağacı grafik olarak göster,
- `Train_knight.csv` ilk argüman olsun,
- `Test_knight.csv` ikinci argüman olsun,
- `Tree.txt` oluştur ve her satıra `Jedi` veya `Sith` yaz,
- minimum `%90 F1-score` hedefle.

Subject ayrıca DS_3'ten gelen `Training_knight.csv` ve `Validation_knight.csv` dosyalarına ihtiyaç duyabileceğini söylüyor.

---

## 6.2 Decision Tree nedir?

Decision tree, feature değerlerine eşik soruları sorarak veriyi dallara bölen bir sınıflandırıcıdır.

Örneğin:

```text
            Strength <= 0.48 ?
             /             \
          YES               NO
           /                 \
      Sith ?            Empowered <= 0.35 ?
                         /              \
                       YES              NO
                       Jedi             Sith
```

Gerçek ağaçta eşikler model tarafından öğrenilir.

---

## 6.3 Subject'in ağaç çıktısını okuyalım

Örnekte:

```text
X[27] <= 0.489
gini = 0.471
samples = 381
value = [145, 236]
```

Buradaki anlam:

### `X[27] <= 0.489`

27 numaralı feature'ın değerine bakılıyor.

### `samples = 381`

Bu node'a 381 training sample gelmiş.

### `value = [145, 236]`

Sınıfların dağılımı 145 ve 236.

### `gini = 0.471`

Node'un impurity ölçüsü.

---

## 6.4 Gini impurity

Binary durumda:

$$
Gini=1-p_1^2-p_2^2.
$$

Subject root node'unda:

$$
p_1=145/381
$$

$$
p_2=236/381.
$$

Dolayısıyla:

$$
Gini
=1-(145/381)^2-(236/381)^2
\approx0.471.
$$

Bu, subject'in yazdığı değeri doğrudan açıklıyor.

---

## 6.5 Gini ne anlatıyor?

Bir node tamamen tek sınıftan oluşuyorsa:

```text
[100, 0]
```

Gini:

$$
1-1^2-0^2=0.
$$

Yani tamamen pure.

50–50 bir node:

```text
[50, 50]
```

için:

$$
1-0.5^2-0.5^2=0.5.
$$

Binary classification için maksimum Gini impurity `0.5`'tir.

---

## 6.6 Decision Tree neden faydalı?

Avantajları:

- nonlinear ilişkileri yakalayabilir,
- feature scaling istemez,
- feature threshold'larını doğal biçimde kullanır,
- karar süreci görselleştirilebilir.

Bu yüzden DS_3'te yaptığımız standardization/normalization **Decision Tree'nin matematiksel olarak çalışması için zorunlu değildir**.

Bu nokta çok önemli:

```text
KNN → scaling önemli
Logistic Regression → scaling çoğu durumda önemli
Decision Tree → scaling genellikle gerekli değil
Random Forest → scaling genellikle gerekli değil
```

---

## 6.7 Decision Tree kodu

```python
import pandas as pd
from sklearn.tree import DecisionTreeClassifier, plot_tree
import matplotlib.pyplot as plt


train = pd.read_csv("Train_knight.csv")
test = pd.read_csv("Test_knight.csv")

X_train = train.drop(columns="knight")
y_train = train["knight"]
X_test = test

model = DecisionTreeClassifier(
    max_depth=6,
    min_samples_leaf=2,
    random_state=42
)

model.fit(X_train, y_train)

predictions = model.predict(X_test)

with open("Tree.txt", "w", encoding="utf-8") as f:
    for prediction in predictions:
        f.write(f"{prediction}\n")

plt.figure(figsize=(18, 10))
plot_tree(
    model,
    feature_names=X_train.columns,
    class_names=model.classes_,
    filled=True,
    rounded=True,
    max_depth=4
)
plt.tight_layout()
plt.show()
```

### Neden `max_depth` gibi parametreler var?

Bunlar **hyperparameter**.

Model onları training sırasında otomatik olarak öğrenmez; sen belirliyorsun.

Örneğin:

```text
max_depth = 2   → çok basit
max_depth = 20  → çok karmaşık olabilir
```

Çok derin ağaç training verisini ezberleyebilir:

**overfitting**.

Çok sığ ağaç ise gerçek yapıyı yeterince öğrenemeyebilir:

**underfitting**.

---

## 6.8 Random Forest nedir?

Random Forest, birçok Decision Tree'nin birlikte kullanıldığı bir **ensemble method**.

Temel fikir:

```text
Tree 1 → Jedi
Tree 2 → Sith
Tree 3 → Jedi
Tree 4 → Jedi
Tree 5 → Sith

majority vote → Jedi
```

Random Forest tek ağaca göre daha kararlı bir model olabilir çünkü birçok ağacın kararını birleştirir.

Kod:

```python
from sklearn.ensemble import RandomForestClassifier

model = RandomForestClassifier(
    n_estimators=300,
    max_depth=8,
    random_state=42,
    n_jobs=-1
)
```

---

## 6.9 Ex04'te Validation neden önemli?

Subject açıkça DS_3'te oluşturduğun `Training_knight.csv` ve `Validation_knight.csv` dosyalarını kullanabileceğini söylüyor.

Buradaki mantık:

```text
Training_knight.csv
       ↓
model.fit()
       ↓
Validation_knight.csv
       ↓
F1 ölç
       ↓
hyperparameter değiştir
       ↓
tekrar
```

Sonra seçtiğin yapı ile final training yapılır ve gerçek Test üzerinde prediction üretilir.

Bu, **model selection / hyperparameter tuning** sürecidir.

---

# 7. Ex05 — KNN

## 7.1 Subject ne istiyor?

Ex05:

- `Train_knight.csv` ilk argüman,
- `Test_knight.csv` ikinci argüman,
- `KNN.txt` prediction dosyası,
- Validation üzerinde farklı `k` değerlerine göre precision hesapla,
- grafiği göster,
- minimum `%92 F1-score`.

---

## 7.2 KNN nedir?

**KNN — K-Nearest Neighbors**.

Bir yeni noktanın sınıfını, training setindeki en yakın `k` komşunun sınıfına bakarak belirler.

Örneğin `k=5`:

```text
En yakın 5 komşu:

Jedi
Jedi
Sith
Jedi
Sith

Jedi = 3
Sith = 2

Prediction = Jedi
```

---

## 7.3 k-value nedir?

`k`, kaç komşuya bakacağını belirleyen hyperparameter'dır.

### Küçük k

Örneğin:

```text
k = 1
```

Model yalnızca en yakın komşuya bakar.

Avantaj:
- yerel yapıya çok duyarlı.

Dezavantaj:
- noise ve outlier'lara çok duyarlı.
- yüksek variance riski.

### Büyük k

Örneğin:

```text
k = 50
```

çok daha geniş bir çevreye bakar.

Avantaj:
- daha smooth karar.

Dezavantaj:
- küçük yapıları kaçırabilir.
- fazla genelleştirme yapabilir.

Bu nedenle uygun `k`, validation ile seçilir.

---

## 7.4 Neden KNN'de scaling çok önemli?

KNN mesafe kullanır.

Öklid mesafesi:

$$
d(x,y)=
\sqrt{\sum_j(x_j-y_j)^2}.
$$

Bir feature:

```text
0–1000
```

diğeri:

```text
0–1
```

ise büyük ölçekli feature mesafeyi domine edebilir.

Bu yüzden DS_3 Ex03/Ex04'teki preprocessing burada doğrudan işe yarar.

---

## 7.5 KNN için StandardScaler neden iyi bir başlangıç?

KNN için çoğu durumda:

```python
from sklearn.preprocessing import StandardScaler
```

ile:

$$
z=\frac{x-\mu}{\sigma}
$$

uygulamak iyi bir başlangıçtır.

Özellikle feature'ların fiziksel ölçekleri çok farklıysa distance hesabını daha dengeli hale getirir.

---

## 7.6 Validation ile k seçmek

```python
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import precision_score, f1_score


train = pd.read_csv("Training_knight.csv")
validation = pd.read_csv("Validation_knight.csv")

X_train = train.drop(columns="knight")
y_train = train["knight"]

X_val = validation.drop(columns="knight")
y_val = validation["knight"]

results = []

for k in range(1, 26, 2):
    model = Pipeline([
        ("scaler", StandardScaler()),
        ("knn", KNeighborsClassifier(n_neighbors=k))
    ])

    model.fit(X_train, y_train)
    pred = model.predict(X_val)

    precision = precision_score(y_val, pred, average="weighted")
    f1 = f1_score(y_val, pred, average="weighted")

    results.append({
        "k": k,
        "precision": precision,
        "f1": f1,
    })

results_df = pd.DataFrame(results)
print(results_df)
```

### Neden `1, 3, 5, ...` gibi tek k'lar?

İki sınıflı bir problemde komşu oylarının eşit çıkması ihtimalini azaltmak için tek `k` değerleri pratikte sık kullanılır. Bu bir zorunluluk değildir; subject yalnızca k değerlerini denemeni istiyor.

---

## 7.7 En iyi k'yı nasıl seçeriz?

Burada "best" kelimesi **subject'in başarı kriterine göre** anlaşılmalı.

Subject minimum `%92 F1-score` istiyor. Precision grafiğini de istiyor.

Dolayısıyla validation'da:

1. F1'i hesapla,
2. precision'ı da izle,
3. `k` ile bunların nasıl değiştiğini çiz,
4. hedef F1'e ulaşan mantıklı bir `k` seç.

Örneğin:

```python
best_row = results_df.loc[results_df["f1"].idxmax()]
print(best_row)
```

Ancak eğitim sırasında karar verirken yalnızca validation sonucuna bakmalısın; Test setini bu seçime karıştırmamalısın.

---

## 7.8 Final model ve Test

`k` seçildikten sonra:

```text
Training data
      +
Validation data
      ↓
chosen k
      ↓
final training
      ↓
Test prediction
```

şeklinde ilerleyebilirsin.

Burada önemli nokta: Test labels yoksa Test üzerinde F1 hesaplayamazsın. Test dosyası yalnızca prediction üretmek için gelir.

---

# 8. Logistic Regression — bilmen gereken önemli üçüncü model

> **Bu model DS_4 Ex04 veya Ex05'te zorunlu değildir. Ex06, üçüncü modeli senin seçmene izin verir. Logistic Regression bu nedenle iyi bir örnektir.**

## 8.1 Logistic Regression nedir?

Adı "regression" olsa da binary classification için kullanılabilir.

Önce linear score hesaplanır:

$$
z=w_1x_1+w_2x_2+\cdots+w_px_p+b.
$$

Sonra sigmoid:

$$
\sigma(z)=\frac{1}{1+e^{-z}}
$$

uygulanır.

Sonuç:

$$
0<p<1.
$$

Bu değer pozitif sınıfın tahmini olasılığı gibi yorumlanabilir.

Örneğin:

```text
P(Jedi)=0.82
```

ise threshold `0.5` olduğunda Jedi seçilebilir.

---

## 8.2 Logistic Regression neden ilginç?

Decision Tree nonlinear eşiklerle çalışırken Logistic Regression temel olarak feature'ların **lineer birleşimi** üzerinden karar verir.

Bu nedenle farklı modellerin hata desenleri farklı olabilir.

Bu özellik Ex06'daki ensemble yaklaşımı açısından değerlidir.

---

## 8.3 Neden scaling önemli?

Logistic Regression'da optimizasyon ve regularization feature ölçeklerinden etkilenebilir.

Bu yüzden:

```python
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

model = Pipeline([
    ("scaler", StandardScaler()),
    ("logreg", LogisticRegression(max_iter=2000))
])
```

iyi bir yapı olabilir.

---

# 9. Ex06 — Voting Classifier

## 9.1 Subject ne istiyor?

Ex06:

- üçüncü bir model seç,
- Voting classifier oluştur,
- `Train_knight.csv` + `Test_knight.csv` ile çalış,
- `Voting.txt` oluştur,
- minimum `%94 F1-score`.

Ayrıca yine DS_3'ten gelen Training / Validation dosyalarına ihtiyaç duyabileceğini söylüyor.

---

## 9.2 Ensemble Learning nedir?

**Ensemble learning**, birden fazla modelin kararını birleştirme yaklaşımıdır.

Tek model:

```text
X → Model → Prediction
```

Ensemble:

```text
              ┌→ Model A → pred A
X ────────────┼→ Model B → pred B
              └→ Model C → pred C
                       ↓
                    combine
                       ↓
                   final pred
```

Voting classifier bunun açık ve anlaşılır örneklerinden biridir.

---

## 9.3 Hard voting

Her model doğrudan sınıf söyler:

```text
Tree      → Jedi
KNN       → Sith
Logistic  → Jedi
```

Çoğunluk:

```text
Jedi 2
Sith 1
```

Sonuç:

```text
Jedi
```

---

## 9.4 Soft voting

Modeller olasılık üretir.

Örneğin:

```text
             P(Jedi)
Tree           0.70
KNN            0.60
Logistic       0.90
```

Ortalama:

$$
(0.70+0.60+0.90)/3=0.7333.
$$

Bu durumda ensemble Jedi tarafında daha güçlüdür.

Soft voting için base modellerin `predict_proba()` sağlayabilmesi gerekir.

---

## 9.5 Neden farklı modelleri birleştirmek mantıklı?

Çünkü modeller aynı hataları yapmak zorunda değildir.

Örneğin:

```text
Tree     → nonlinear threshold yapısını iyi yakalar
KNN      → local neighborhood yapısını yakalar
Logistic → genel lineer ayrımı yakalar
```

Bir modelin hata yaptığı bazı örneklerde diğerinin doğru karar vermesi mümkündür.

Bu, ensemble'ın temel motivasyonudur.

---

## 9.6 DS_4 için örnek Voting tasarımı

Üç model:

1. Random Forest
2. KNN
3. Logistic Regression

Örneğin:

```python
from sklearn.ensemble import VotingClassifier, RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

rf = RandomForestClassifier(
    n_estimators=300,
    random_state=42,
    n_jobs=-1
)

knn = Pipeline([
    ("scaler", StandardScaler()),
    ("knn", KNeighborsClassifier(n_neighbors=7))
])

logreg = Pipeline([
    ("scaler", StandardScaler()),
    ("logreg", LogisticRegression(max_iter=2000))
])

voting = VotingClassifier(
    estimators=[
        ("rf", rf),
        ("knn", knn),
        ("logreg", logreg),
    ],
    voting="soft"
)
```

Burada çok önemli bir tasarım ayrıntısı var:

- Random Forest scaling istemiyor.
- KNN scaling istiyor.
- Logistic Regression scaling'den yararlanıyor.

Bu nedenle her modelin preprocessing'ini kendi `Pipeline`'ı içinde tutmak temizdir.

---

# 10. Data Leakage — DS_3 ve DS_4'te en önemli metodolojik risklerden biri

## 10.1 Data leakage nedir?

Modelin eğitim aşamasında normalde bilmemesi gereken bilgiyi öğrenme sürecine sızdırmak.

Örnek:

```python
scaler.fit(all_data)
```

sonra:

```text
Train + Validation + Test
```

ile aynı scaler parametrelerini kullanmak.

Eğer Test dağılımından bilgi training preprocessing aşamasına sızıyorsa değerlendirme yapay biçimde iyileşebilir.

---

## 10.2 Doğru genel akış

```text
Training
   │
   ├── fit preprocessing
   │
   ├── fit model
   │
   └── validate

Validation
   └── transform using training-fitted preprocessing

Test
   └── transform using training-fitted preprocessing
```

Özellikle:

```python
scaler.fit(X_train)

X_train_scaled = scaler.transform(X_train)
X_val_scaled = scaler.transform(X_val)
X_test_scaled = scaler.transform(X_test)
```

mantığını anlamak önemlidir.

---

# 11. Hyperparameter nedir?

Modelin kendisinin training'den öğrenmediği, bizim belirlediğimiz ayarlar.

Örnek:

### Decision Tree

```text
max_depth
min_samples_leaf
criterion
```

### Random Forest

```text
n_estimators
max_depth
min_samples_leaf
```

### KNN

```text
n_neighbors = k
weights
metric
```

### Logistic Regression

```text
C
penalty
solver
```

Bunları validation kullanarak seçmek:

**hyperparameter tuning**.

---

# 12. Overfitting ve Underfitting

## Overfitting

Model training verisini çok iyi öğrenir ama yeni verilere kötü geneller.

Örneğin çok derin Decision Tree:

```text
Training F1  → 0.999
Validation F1 → 0.80
```

## Underfitting

Model hem training hem validation'da zayıftır.

Örneğin aşırı basit model:

```text
Training F1   → 0.75
Validation F1 → 0.73
```

İstenen:

```text
Training iyi
Validation da iyi
```

ve bu performansın Test'te mümkün olduğunca genellenmesi.

---

# 13. Feature Selection neden DS_4 Ex03'te var?

Modelden önce şu probleme bakıyorsun:

```text
Feature A ───┐
Feature B ───┼── aynı bilgiyi taşıyor olabilir
Feature C ───┘
```

Çok benzer feature'ların hepsini modele vermek:

- gereksiz boyutu artırabilir,
- lineer modellerde coefficient yorumunu zorlaştırabilir,
- bazı durumlarda numerical stability problemlerine katkıda bulunabilir.

VIF ile:

```text
30 feature
   ↓
çok yüksek VIF'leri tespit et
   ↓
iteratif çıkarma
   ↓
VIF < 5
   ↓
reduced feature set
```

elde ediyorsun.

Bu reduced feature set daha sonra modellerde kullanılabilir.

---

# 14. DS_3 preprocessing ile DS_4 modellerini eşleştirmek

| Model / Yöntem | Standardization | Min-Max | Neden? |
|---|---|---|---|
| Histogram | Gerekli değil | Gerekli değil | Görselleştirme |
| Pearson correlation | Gerekli değil | Gerekli değil | Correlation lineer ölçeğe invariant |
| PCA | Genellikle önemli | Alternatif olabilir | Varyans ölçekten etkilenir |
| VIF | Şart değil | Şart değil | VIF lineer ilişkilerle ilgili |
| Decision Tree | Genellikle gerekmez | Gerekmez | Eşik tabanlı bölmeler |
| Random Forest | Genellikle gerekmez | Gerekmez | Tree ensemble |
| KNN | **Önemli** | Alternatif | Distance tabanlı |
| Logistic Regression | **Genellikle önemli** | Alternatif | Optimization / regularization |
| Voting | Base modele göre | Base modele göre | Her base model kendi preprocessing'ini gerektirebilir |

Bu tablo DS_3'ün neden DS_4'e hazırlık yaptığını gösterir.

---

# 15. DS_4 egzersizlerinin birbirine bağlantısı

## Ex00

```text
Prediction + Truth
       ↓
Confusion Matrix
       ↓
TP TN FP FN
       ↓
Precision Recall F1 Accuracy
```

Model değerlendirme dilini öğreniyoruz.

---

## Ex01

```text
Features
   ↓
Correlation Matrix
   ↓
Heatmap
   ↓
Feature ↔ Feature ilişkileri
```

Birbirini tekrar eden feature'ları görmeye başlıyoruz.

---

## Ex02

```text
Feature matrix
   ↓
Standardization
   ↓
PCA
   ↓
Explained variance ratio
   ↓
Cumulative variance
   ↓
90% için component sayısı
```

Boyut indirgeme mantığını görüyoruz.

---

## Ex03

```text
Feature matrix
   ↓
VIF
   ↓
Multicollinearity
   ↓
Feature elimination
   ↓
Reduced feature set
```

Bu kez yeni component üretmek yerine **orijinal feature'lardan bazılarını siliyoruz**.

---

## Ex04

```text
Reduced / prepared features
       ↓
Decision Tree / Random Forest
       ↓
Validation
       ↓
F1 ≥ 90 hedefi
       ↓
Test prediction
```

İlk gerçek classifier.

---

## Ex05

```text
Prepared features
       ↓
Scaling
       ↓
KNN(k)
       ↓
Validation üzerinde farklı k'lar
       ↓
k seçimi
       ↓
F1 ≥ 92 hedefi
       ↓
Test prediction
```

Distance-based model ve hyperparameter tuning.

---

## Ex06

```text
Model 1 ─┐
Model 2 ─┼→ Voting classifier → final prediction
Model 3 ─┘
       ↓
F1 ≥ 94 hedefi
```

Ensemble learning.

---

# 16. Validation neden DS_4 boyunca tekrar tekrar karşımıza çıkıyor?

Çünkü modelin hiperparametrelerini Test'e bakarak seçmek yanlış metodolojidir.

Doğru düşünce:

```text
Training
   ↓
Model öğrenir

Validation
   ↓
Model / hyperparameter seçimi

Test
   ↓
Final değerlendirme / prediction
```

Örneğin KNN'de:

```text
k=1  → Validation F1 = 0.88
k=3  → Validation F1 = 0.91
k=5  → Validation F1 = 0.94
k=7  → Validation F1 = 0.93
```

`k=5` seçmek validation sonucuna dayanabilir.

Bunu Test üzerinden seçmek:

```text
k=1  → Test F1 = ...
k=3  → Test F1 = ...
k=5  → Test F1 = ...
...
```

yapıp en iyisini Test'ten seçmek **test leakage** yaratır.

---

# 17. DS_4 için önerilen gerçek çalışma düzeni

Subject'te egzersizleri yaparken şu sırayla ilerlemek zihinsel olarak daha temiz:

```text
1. DS_3 verisini hazırla
       ↓
2. Training / Validation oluştur
       ↓
3. Ex00 ile evaluation metric'lerini elle anla
       ↓
4. Ex01 heatmap ile feature ilişkilerine bak
       ↓
5. Ex02 PCA / explained variance yap
       ↓
6. Ex03 VIF ile feature selection yap
       ↓
7. Ex04 model + validation
       ↓
8. Ex05 KNN + k tuning + validation
       ↓
9. Ex06 ensemble + validation
       ↓
10. Final model ile Test prediction
```

---

# 18. Her model için aynı temel pipeline'ı düşün

Her classifier için zihinsel şablon:

```text
RAW DATA
   │
   ▼
SELECT FEATURES
   │
   ▼
PREPROCESS
   │
   ▼
TRAIN MODEL
   │
   ▼
VALIDATION
   │
   ├── metric hesapla
   ├── hyperparameter değiştir
   └── tekrar train
   │
   ▼
FREEZE MODEL CHOICE
   │
   ▼
TEST PREDICTION
```

Bu şablonu oturtursan Decision Tree, KNN, Logistic Regression, SVM, Random Forest vb. modeller arasındaki ortak yapı çok daha net olur.

---

# 19. Literatür terimleri — hızlı referans

| Terim | Kısa anlamı |
|---|---|
| **Classification** | Örneği bir sınıfa atama |
| **Binary classification** | İki sınıflı classification |
| **Feature / Predictor** | Model girdisi |
| **Target / Label** | Modelin tahmin etmeye çalıştığı çıktı |
| **Supervised learning** | Target'ı bilinen veriden öğrenme |
| **Prediction** | Modelin tahmini |
| **Truth / Ground truth** | Gerçek etiket |
| **TP** | Doğru positive tahmin |
| **TN** | Doğru negative tahmin |
| **FP** | Yanlış positive tahmin |
| **FN** | Yanlış negative tahmin |
| **Confusion Matrix** | TP/TN/FP/FN'yi sınıflara göre özetleyen tablo |
| **Accuracy** | Tüm tahminlerin ne kadarı doğru |
| **Precision** | Positive dediğimiz örneklerin ne kadarı doğru |
| **Recall** | Gerçek positive'ların ne kadarını yakaladık |
| **F1-score** | Precision ve recall'un harmonik ortalaması |
| **Variance** | Değerlerin ortalamaya göre yayılımı |
| **Covariance** | İki değişkenin birlikte nasıl değiştiği |
| **Correlation** | Standardize edilmiş covariance benzeri -1/+1 arası ilişki ölçüsü |
| **Heatmap** | Sayısal matrix'i renklerle gösterme |
| **PCA** | Principal Component Analysis; boyut indirgeme yöntemi |
| **Principal Component** | PCA'nın oluşturduğu yeni eksen |
| **Explained Variance Ratio** | Bir component'in toplam varyansın ne kadarını açıkladığı |
| **Cumulative Explained Variance** | İlk N component'in birlikte açıkladığı oran |
| **Dimensionality Reduction** | Boyut sayısını azaltma |
| **Multicollinearity** | Predictor'ların güçlü doğrusal bağımlılığı |
| **VIF** | Variance Inflation Factor; multicollinearity göstergesi |
| **Tolerance** | `1 / VIF` |
| **Feature Selection** | Kullanılacak feature'ları seçme |
| **Decision Tree** | Eşikler ile dallanan classifier |
| **Gini impurity** | Tree node'un saflık / karışıklık ölçüsü |
| **Random Forest** | Birçok decision tree'den oluşan ensemble |
| **KNN** | En yakın k komşuya göre sınıflandırma |
| **k-value** | KNN'de kaç komşuya bakılacağını belirleyen hyperparameter |
| **Logistic Regression** | Sigmoid ile binary classification yapan lineer model |
| **Hyperparameter** | Training'den doğrudan öğrenilmeyen model ayarı |
| **Overfitting** | Training'i fazla öğrenip genellemede kötüleşme |
| **Underfitting** | Modelin yapıyı yeterince öğrenememesi |
| **Data Leakage** | Evaluation bilgisinin öğrenme sürecine sızması |
| **Ensemble Learning** | Birden fazla modelin kararını birleştirme |
| **Voting Classifier** | Modellerin oylarını birleştiren ensemble |
| **Hard Voting** | Sınıf oylarını birleştirme |
| **Soft Voting** | Tahmin olasılıklarını birleştirme |
| **Validation Set** | Model / hyperparameter seçimi için kullanılan veri |
| **Test Set** | Final değerlendirme için ayrılan veri |

---

# 20. En çok karıştırılan noktalar

## Correlation ≠ Causation

Yüksek correlation:

> "İki değişken birlikte değişiyor."

demektir.

> "Biri diğerine sebep oluyor."

demek değildir.

---

## Variance ≠ Correlation

Variance tek feature'ın yayılımını ölçer.

Correlation iki feature arasındaki doğrusal ilişkiyi ölçer.

---

## Standardization ≠ Normalization

Standardization tipik olarak:

$$
z=\frac{x-\mu}{\sigma}
$$

Normalization ise farklı tanımlara sahip olabilir; bu projede Ex04 için subject'in örnekleri `[0,1]` Min-Max scaling yorumunu güçlü biçimde destekler:

$$
x'=\frac{x-x_{min}}{x_{max}-x_{min}}.
$$

`sklearn.preprocessing.Normalizer` ise bambaşka bir, **sample/satır bazlı normlama** işlemidir.

---

## PCA ≠ Feature Selection

PCA:

```text
X1 X2 X3 X4
 ↓
PC1 PC2
```

Yeni feature'lar üretir.

Feature selection:

```text
X1 X2 X3 X4
 ↓
X1 X3
```

Orijinal feature'lardan bazılarını tutar.

---

## Training accuracy ≠ Generalization

Training'te çok yüksek skor:

> modelin yeni veride de aynı derecede başarılı olacağını garanti etmez.

Bu nedenle Validation ve Test ayrımı gerekir.

---

## Precision ≠ Recall

```text
Precision → "Tahminlerim ne kadar temiz?"
Recall    → "Pozitifleri ne kadar yakaladım?"
```

---

## KNN'de k bir model parametresi değildir

`k`, KNN'in **hyperparameter**'ıdır.

Training sırasında ağırlık gibi öğrenilmez; validation ile seçilir.

---

# 21. DS_4'ün asıl öğrenme hedefi

Bu proje sadece:

```text
DecisionTreeClassifier(...)
KNeighborsClassifier(...)
VotingClassifier(...)
```

yazmayı öğretmiyor.

Asıl önemli zincir:

```text
VERİYİ TANIMLA
       ↓
DEĞİŞKENLERİN İLİŞKİSİNİ ANLA
       ↓
GEREKSİZ / TEKRARLAYAN BİLGİYİ ARA
       ↓
MODEL SEÇ
       ↓
MODELİ TRAINING'DE ÖĞRET
       ↓
VALIDATION İLE KARAR VER
       ↓
METRIC'LERLE DEĞERLENDİR
       ↓
FINAL MODELİ DONDUR
       ↓
TEST'TE PREDICTION YAP
```

Bu nedenle DS_3 ve DS_4'ü birlikte düşündüğünde artık şu büyük şablon ortaya çıkıyor:

```text
                    ┌───────────────────┐
                    │      DATA         │
                    └─────────┬─────────┘
                              │
                              ▼
                    ┌───────────────────┐
                    │ EDA / Understanding│
                    │   DS_3 Ex00–02    │
                    └─────────┬─────────┘
                              │
                              ▼
                    ┌───────────────────┐
                    │   Preprocessing   │
                    │   DS_3 Ex03–04   │
                    └─────────┬─────────┘
                              │
                              ▼
                    ┌───────────────────┐
                    │ Train / Validation│
                    │   DS_3 Ex05      │
                    └─────────┬─────────┘
                              │
                ┌─────────────┼──────────────┐
                │             │              │
                ▼             ▼              ▼
             Heatmap         PCA            VIF
             Ex01            Ex02           Ex03
                │             │              │
                └─────────────┼──────────────┘
                              │
                              ▼
                    ┌───────────────────┐
                    │      Models       │
                    │   Tree / KNN /   │
                    │   Logistic etc.  │
                    └─────────┬─────────┘
                              │
                              ▼
                    ┌───────────────────┐
                    │    Validation     │
                    │ F1 / Precision / │
                    │ Recall / Accuracy│
                    └─────────┬─────────┘
                              │
                              ▼
                    ┌───────────────────┐
                    │   Ensemble /     │
                    │ Voting (Ex06)    │
                    └─────────┬─────────┘
                              │
                              ▼
                    ┌───────────────────┐
                    │  Final Test      │
                    │   Prediction     │
                    └───────────────────┘
```

---

# 22. Son kontrol listesi — Evaluation'dan önce

## Ex00

- [ ] `predictions.txt` ve `truth.txt` sıraları doğru mu?
- [ ] TP/TN/FP/FN tanımlarını açıklayabiliyor muyum?
- [ ] Matrix orientation'ını biliyor muyum?
- [ ] Precision, recall, F1 ve accuracy formüllerini biliyor muyum?
- [ ] Hazır confusion-matrix/metric fonksiyonlarını kullanmadan hesaplayabiliyor muyum?

## Ex01

- [ ] Pearson correlation nedir?
- [ ] Correlation matrix neden simetriktir?
- [ ] Diagonal neden 1'dir?
- [ ] Correlation causation değildir diyebiliyor muyum?

## Ex02

- [ ] Variance nedir?
- [ ] PCA nedir?
- [ ] Principal component nedir?
- [ ] Explained variance ratio nedir?
- [ ] Cumulative variance nasıl yorumlanır?
- [ ] Neden 90% eşiğine bakıyoruz?

## Ex03

- [ ] Multicollinearity nedir?
- [ ] VIF formülünü biliyor muyum?
- [ ] Tolerance = 1/VIF ilişkisini biliyor muyum?
- [ ] Neden VIF'i iteratif hesaplamak daha güvenli?
- [ ] PCA ile feature selection arasındaki farkı biliyor muyum?

## Ex04

- [ ] Decision Tree nasıl bölme yapıyor?
- [ ] Gini impurity nedir?
- [ ] `max_depth` neden hyperparameter?
- [ ] Overfitting neden ortaya çıkabilir?
- [ ] `Tree.txt` formatını doğru üretiyor muyum?

## Ex05

- [ ] KNN nasıl karar veriyor?
- [ ] `k` neden hyperparameter?
- [ ] Küçük ve büyük k'nın etkisini açıklayabiliyor muyum?
- [ ] KNN'de scaling neden önemli?
- [ ] Validation ile k'yı seçebiliyor muyum?
- [ ] Precision ile F1'i birlikte izliyor muyum?

## Ex06

- [ ] Ensemble learning nedir?
- [ ] Hard voting ile soft voting farkı nedir?
- [ ] Farklı modelleri neden birleştiriyorum?
- [ ] Logistic Regression'ın neden classification modeli olduğunu açıklayabiliyor muyum?
- [ ] Test'i model seçimi için kullanmadığımı biliyor muyum?

---

# 23. Tek cümlelik büyük resim

> **DS_3 veriyi anlamayı, dönüştürmeyi ve train/validation olarak ayırmayı; DS_4 ise bu hazırlanmış veri üzerinde feature ilişkilerini incelemeyi, feature selection yapmayı, modeller kurmayı, validation ile model/hyperparameter seçmeyi, classification metric'leriyle değerlendirmeyi ve sonunda ensemble ile daha güçlü bir tahmin sistemi oluşturmayı öğretiyor.**

---

# Kaynak / Subject haritası

Bu tutorial'ın DS_4 kısmındaki subject-spesifik gereksinimler, paylaşılan `ds_4.pdf` içindeki şu bölümler esas alınarak düzenlenmiştir:

- **Exercise 00 — Confusion Matrix:** pp. 4–5
- **Exercise 01 — Heatmap:** p. 6
- **Exercise 02 — Variances:** pp. 7–8
- **Exercise 03 — Feature Selection / VIF:** p. 9
- **Exercise 04 — Forest / Decision Tree or Random Forest:** pp. 10–11
- **Exercise 05 — KNN:** pp. 12–13
- **Exercise 06 — Voting Classifier:** pp. 14–15

Subject'in bazı egzersizlerinde kullanılan yöntemin adı veya matematiksel formülü tam verilmediği için, özellikle **Ex02'de PCA bağlantısı** gibi noktalar subject örneklerinden yapılan açık çıkarımlar olarak ele alınmıştır.
---

# 24. Ex00 — Ek Sorular ve Kavramsal Derinleştirme

Bu bölüm, Ex00'daki `precision`, `recall`, `F1-score`, `accuracy` ve confusion matrix kavramlarının birbirleriyle nasıl ilişkili olduğunu daha dikkatli biçimde açıklamak için eklenmiştir.

## 24.1 Precision ve recall tek başına mı düşünülür, yoksa bir sınıfla beraber mi?

### Kısa cevap

Bir sınıflandırma probleminde `precision` ve `recall`, **hangi sınıfı "pozitif" kabul ettiğine göre tanımlanan sınıf-spesifik ölçülerdir**.

Dolayısıyla özellikle birden fazla sınıf olduğunda yalnızca:

```text
precision = 0.45
```

demek hangi sınıfın precision'ı olduğunu söylemez.

Daha doğru ifadeler:

```text
Jedi precision = 0.45
Sith precision = 0.47
```

veya:

```text
precision for the Jedi class = 0.45
precision for the Sith class = 0.47
```

olur.

Subject'in Ex00 örneğinde de tam olarak sınıf başına değerler veriliyor:

```text
             precision  recall  f1-score  total
Jedi            0.45     0.51     0.48      49
Sith            0.47     0.41     0.44      51
```

Subject ayrıca confusion matrix'i de:

```text
[[25 24]
 [30 21]]
```

şeklinde gösteriyor. fileciteturn0file0L69-L78

### Precision'ın sınıf-spesifik anlamı

Bir sınıfı, örneğin `Jedi` sınıfını pozitif olarak seçelim.

Precision:

$$
Precision_{Jedi}
=
\frac{TP_{Jedi}}
{TP_{Jedi}+FP_{Jedi}}
$$

Yorum:

> Modelin `Jedi` diye tahmin ettiklerinin ne kadarı gerçekten Jedi?

Aynı şey `Sith` için de yapılabilir:

$$
Precision_{Sith}
=
\frac{TP_{Sith}}
{TP_{Sith}+FP_{Sith}}
$$

Burada yalnızca pozitif sınıfın adını değiştiriyoruz. Her sınıfı sırayla "pozitif sınıf" gibi ele alıp diğer sınıf(lar)ı "negatif" kabul etmek, literatürde **one-vs-rest (OvR)** bakış açısıyla ifade edilebilir.

### Recall'ın sınıf-spesifik anlamı

`Jedi` pozitif sınıf kabul edilirse:

$$
Recall_{Jedi}
=
\frac{TP_{Jedi}}
{TP_{Jedi}+FN_{Jedi}}
$$

Yorum:

> Gerçekte Jedi olanların ne kadarını model Jedi olarak yakaladı?

Aynı şekilde `Sith` için:

$$
Recall_{Sith}
=
\frac{TP_{Sith}}
{TP_{Sith}+FN_{Sith}}
$$

### Literatürde bunların ayrı isimleri var mı?

Evet; özellikle binary classification bağlamında şu eşleştirmeler kullanılır:

| Ölçü | Yaygın literatür adı | Formül |
|---|---|---|
| Pozitif sınıf precision | **Positive Predictive Value (PPV)** | $TP/(TP+FP)$ |
| Pozitif sınıf recall | **Sensitivity / True Positive Rate (TPR)** | $TP/(TP+FN)$ |
| Negatif sınıf recall | **Specificity / True Negative Rate (TNR)** | $TN/(TN+FP)$ |
| Negatif sınıf precision | **Negative Predictive Value (NPV)** | $TN/(TN+FN)$ |

Dolayısıyla binary classification'da "recall" çoğu zaman varsayılan olarak **seçtiğimiz pozitif sınıfın recall'ını** ifade eder. Fakat bir rapor tüm sınıflar için ayrı değerler veriyorsa, hangi sınıfa ait olduğu ayrıca belirtilmelidir.

Önemli bir ayrıntı: `Sith recall` ile `Jedi specificity` binary durumda aynı sayıya denk gelebilir; çünkü bir sınıfın recall'ı, diğer sınıfı negatif olarak ele aldığımızda onun specificity'sine karşılık gelir.

---

## 24.2 İki sayının ağırlıklı aritmetik ortalaması ile harmonik ortalaması aynı şey değildir

Kesinlikle aynı şey değiller.

İki sayı $a$ ve $b$ için eşit ağırlıklı aritmetik ortalama:

$$
A=\frac{a+b}{2}
$$

Ağırlıklı aritmetik ortalama ise:

$$
A_w=\frac{w_1a+w_2b}{w_1+w_2}
$$

Harmonik ortalama ise:

$$
H=\frac{2ab}{a+b}
$$

veya:

$$
\frac{1}{H}=\frac{1}{2}\left(\frac{1}{a}+\frac{1}{b}\right)
$$

şeklindedir.

### F1 neden aritmetik ortalama değil?

F1, precision ve recall'un **harmonik ortalamasıdır**:

$$
F1=\frac{2PR}{P+R}
$$

Örneğin:

```text
Precision = 0.90
Recall    = 0.10
```

olsun.

Aritmetik ortalama:

$$
\frac{0.90+0.10}{2}=0.50
$$

Harmonik ortalama:

$$
\frac{2(0.90)(0.10)}{0.90+0.10}=0.18
$$

Aradaki fark çok büyüktür.

Aritmetik ortalama burada `0.50` diyerek iki değerin arasındaki orta noktayı gösterir. Fakat `precision=0.90` iken `recall=0.10` gibi çok dengesiz bir durumu yeterince cezalandırmaz.

F1'in `0.18` çıkması şu mesajı verir:

> Bir ölçü çok iyi olsa bile diğeri çok kötüyse, iki metriğin birlikte iyi olması anlamında F1 de yüksek olmamalıdır.

### Peki weighted arithmetic average kullansak "yanlış" mı olur?

Matematiksel olarak yanlış değildir; fakat elde ettiğin ölçü **F1 olmaz**.

Örneğin eşit ağırlıklı bir birleşim:

$$
0.5P+0.5R
$$

kullanırsan başka bir özet metrik tanımlamış olursun.

Bu metriğin de belli amaçlarla kullanılması mümkün olabilir. Fakat precision ve recall'u F1 adı altında raporlamak istiyorsan formül harmonik ortalama olmalıdır.

Ayrıca ağırlıklı aritmetik ortalama, bir değerin çok yüksek diğerinin çok düşük olduğu durumda aritmetik olarak ortada bir sayı üretir; bu nedenle "iki tarafın da iyi olması" istenen durumları F1 kadar sert biçimde cezalandırmaz.

---

## 24.3 Ağırlıklı ortalama, harmonik ortalama ve sayıların geometrisi

Burada üç temel ortalamayı birlikte düşünmek faydalıdır.

Pozitif iki sayı $a$ ve $b$ için:

### Aritmetik ortalama — Arithmetic Mean

$$
A=\frac{a+b}{2}
$$

Geometrik olarak $a$ ile $b$ sayı doğrusunda iki nokta ise $A$, bunların **tam orta noktasıdır**.

Örneğin $a=2$, $b=8$:

```text
2 ----------- 5 ----------- 8
              ↑
              A
```

### Ağırlıklı aritmetik ortalama — Weighted Arithmetic Mean

$$
A_w=\frac{w_1a+w_2b}{w_1+w_2}
$$

Bu da sayı doğrusundaki bir **ağırlıklı barycenter** gibi düşünülebilir. Büyük ağırlık hangi sayıya verilirse sonuç o sayıya doğru kayar.

Örneğin:

$$
a=2,\qquad b=8,\qquad w_1=3,\qquad w_2=1
$$

ise:

$$
A_w=\frac{3(2)+1(8)}{4}=3.5
$$

Sonuç $2$'ye daha yakındır, çünkü $2$'ye üç kat fazla ağırlık verdik.

### Geometrik ortalama — Geometric Mean

$$
G=\sqrt{ab}
$$

İki boyutlu bir dikdörtgende kenarlar $a$ ve $b$ ise, geometrik ortalama bu dikdörtgenle aynı alana sahip bir karenin kenar uzunluğunu verir:

$$
G^2=ab
$$

Dolayısıyla $G$, "toplama"dan çok **çarpımsal büyüklük** ile ilişkilidir.

### Harmonik ortalama — Harmonic Mean

$$
H=\frac{2ab}{a+b}
$$

Harmonik ortalamayı anlamanın en iyi yollarından biri, sayıları tersine çevirmektir:

$$
\frac{1}{H}
=
\frac{1}{2}
\left(\frac{1}{a}+\frac{1}{b}\right)
$$

Yani harmonik ortalama, sayıların kendilerinin değil **reciprocal (ters) değerlerinin aritmetik ortalamasını alıp tekrar ters çevirmektir**.

Bu yüzden küçük değerler üzerinde çok duyarlıdır.

Örneğin:

$$
H(2,8)=\frac{2(2)(8)}{2+8}=3.2
$$

halbuki:

$$
A(2,8)=5
$$

### Sayıların eşitsizliği ile ilişki

Pozitif sayılarda daima:

$$
H\le G\le A
$$

ve eşitlik ancak:

$$
a=b
$$

olduğunda gerçekleşir.

İki sayı için aritmetik ve harmonik ortalama arasındaki farkın çok güzel bir formu vardır:

$$
A-H
=
\frac{(a-b)^2}{2(a+b)}
$$

Bu formül önemli bir geometrik sezgi verir: $a$ ile $b$ birbirinden uzaklaştıkça, yani dağılım daha dengesiz hale geldikçe, aritmetik ve harmonik ortalama arasındaki fark büyür.

Örneğin $a=b$ ise:

$$
(a-b)^2=0
$$

olduğu için:

$$
A=H
$$

olur.

Bir sayı çok küçük olduğunda harmonik ortalama da hızla küçülür. Örneğin:

$$
A(0.9,0.1)=0.5
$$

ama:

$$
H(0.9,0.1)=0.18
$$

çıkar.

Bu, F1 için son derece işe yarayan özelliktir: precision ve recall'dan biri çok küçükse, F1'i de aşağı çeker.

### Klasik bir uygulama sezgisi: hız

İki eşit mesafeyi sırasıyla $a$ ve $b$ hızlarıyla gidersen toplam ortalama hız aritmetik ortalama değil, harmonik ortalamadır:

$$
V_{avg}=\frac{2ab}{a+b}
$$

Çünkü düşük hızda geçirilen süre daha fazla olur. Bu, harmonik ortalamanın neden "küçük değerlere daha fazla duyarlı" olduğunu fiziksel olarak da sezgisel hale getirir.

---

## 24.4 Ex00 subject gerçekten "genel F1-score" istiyor mu?

Hayır. Burada önceki tutorial metnindeki ifade düzeltilmelidir.

Ex00 subject'inin açıkça yazdığı gereksinim:

> `Print and display matrix confusion`

ve ayrıca bu egzersizin daha sonra tekrar kullanılacağı belirtiliyor. fileciteturn0file0L55-L66

Subject metninde:

> "genel F1-score'u hesapla"

şeklinde ayrı bir gereksinim yok.

Buna karşılık subject'in **örnek çıktısında** her sınıf için `precision`, `recall`, `f1-score`, `total` ve ayrıca `accuracy` ile toplam örnek sayısı gösteriliyor. Sonra confusion matrix yazdırılıyor. fileciteturn0file0L69-L78

Dolayısıyla senin gördüğün yapı doğru:

```text
1. sınıf başına classification report benzeri bölüm

             precision recall f1-score total
Jedi           0.45     0.51   0.48     49
Sith           0.47     0.41   0.44     51

2. genel accuracy bölümü

accuracy       0.46            100

3. confusion matrix

[[25 24]
 [30 21]]
```

Burada `total` sütunu, her gerçek sınıfta kaç örnek olduğunu ifade eder. Başka bir deyişle **support** değeridir.

Dolayısıyla Ex00 için zorunlu olan şey konusunda en güvenli ifade şudur:

> **Subject, confusion matrix'in yanında örnek çıktıda sınıf başına precision/recall/F1 ve accuracy de gösteriyor; fakat ayrı bir "genel F1-score" hesaplanmasını metin olarak açıkça şart koşmuyor.**

Bu nedenle önceki tutorial'daki "Sonra genel bir F1-score isteniyor" cümlesi yanlıştı ve burada düzeltilmiştir.

---

## 24.5 Macro F1 ve Weighted F1 nedir?

Önce her sınıfın kendi F1'i vardır:

$$
F1_i
=
\frac{2P_iR_i}{P_i+R_i}
$$

Birden fazla sınıfta bu değerleri tek bir sayıyla özetlemek için farklı averaging yöntemleri kullanabiliriz.

### Macro F1

Her sınıfa **eşit ağırlık** verir:

$$
F1_{macro}
=
\frac{1}{K}
\sum_{i=1}^{K}F1_i
$$

İki sınıfta:

$$
F1_{macro}
=
\frac{F1_{Jedi}+F1_{Sith}}{2}
$$

Örneğin:

```text
Jedi F1 = 0.48
Sith F1 = 0.44
```

ise:

$$
F1_{macro}=\frac{0.48+0.44}{2}=0.46
$$

Burada sınıfların veri içindeki büyüklükleri önemsenmez. Bir sınıfta 49, diğerinde 51 örnek olması sonucu değiştirmez; iki sınıfa da %50 ağırlık verilir.

### Weighted F1

Her sınıfa kendi **support**'u kadar ağırlık verir:

$$
F1_{weighted}
=
\frac{\sum_{i=1}^{K}n_iF1_i}
{\sum_{i=1}^{K}n_i}
$$

Burada $n_i$, sınıfın gerçek örnek sayısıdır.

Subject örneğindeki support değerleri 49 ve 51 olduğundan:

$$
F1_{weighted}
=
\frac{49(0.48)+51(0.44)}{100}
\approx0.4596
$$

Yani yaklaşık `0.46`.

### Macro F1 ile weighted F1 arasındaki temel fark

```text
Macro F1
→ "Her sınıf benim için eşit derecede önemli."

Weighted F1
→ "Veride daha fazla bulunan sınıf toplam skorda daha fazla ağırlık taşısın."
```

Örneğin:

```text
Sınıf A: 990 örnek, F1 = 0.99
Sınıf B: 10 örnek,  F1 = 0.20
```

Macro F1:

$$
F1_{macro}=\frac{0.99+0.20}{2}=0.595
$$

Weighted F1:

$$
F1_{weighted}
=\frac{990(0.99)+10(0.20)}{1000}
=0.9821
$$

İkisi arasındaki büyük fark, weighted F1'in büyük sınıfın performansı tarafından baskın hale gelebildiğini gösterir.

### F1 ile "precision ve recall'un weighted average'ı" arasındaki fark

Burada çok sık yapılan bir karışıklık var.

`weighted F1` demek:

> Her sınıfın F1'ini hesapla, sonra bu F1'leri support ile ağırlıklandır.

Yani:

$$
F1_{weighted}
=\sum_i w_iF1_i
$$

Bu, önce precision ve recall'u ağırlıklandırıp sonra harmonik ortalama almakla aynı şey değildir.

Örneğin genel weighted precision ve weighted recall:

$$
P_w=\sum_iw_iP_i
$$

$$
R_w=\sum_iw_iR_i
$$

hesaplanıp:

$$
\frac{2P_wR_w}{P_w+R_w}
$$

yapıldığında elde edilen değer genel olarak `weighted F1` ile aynı değildir.

Yani sıra önemlidir:

```text
weighted F1:

per-class P,R
    ↓
per-class F1
    ↓
weighted average
```

ile:

```text
weighted P,R
    ↓
harmonic mean
```

aynı işlem değildir.

### Ex00 açısından hangisini kullanmalıyım?

Burada özellikle dikkatli olmak gerekiyor: **subject metni macro F1 veya weighted F1 istemiyor.** Örnek çıktıda sınıf başına F1 değerleri ve accuracy bulunuyor; hangi genel averaging yönteminin kullanılacağı ayrıca belirtilmiyor. fileciteturn0file0L69-L78

Bu nedenle Ex00'da subject'in örneğini birebir takip ederken öncelikli olarak:

1. sınıf başına TP/TN/FP/FN'den precision, recall ve F1'i hesaplamak,
2. accuracy'yi hesaplamak,
3. confusion matrix'i doğru orientation ile yazdırmak

gerekiyor.

Genel bir `F1` üretmek istersen bunun `macro`, `weighted`, `micro` vb. hangi averaging yöntemi olduğu açıkça belirtilmelidir; aksi halde tek bir sayı verip bunun "genel F1" olduğunu söylemek eksik olur.

---

## 24.6 Ex00 subject örneğini confusion matrix üzerinden tamamen çözmek

Subject'in verdiği matrix'i:

```text
[[25 24]
 [30 21]]
```

olarak ele alalım. Burada satırlar **gerçek sınıfı**, sütunlar ise **tahmin edilen sınıfı** temsil ediyor ve sınıf sırası `[Jedi, Sith]` kabul edildiğinde:

```text
                    Predicted
                  Jedi     Sith
Actual Jedi         25       24
       Sith         30       21
```

olur. Satır toplamları:

$$
25+24=49
$$

ve:

$$
30+21=51
$$

olduğu için subject'in `total` değerleriyle uyuşur. fileciteturn0file0L71-L76

### Jedi'yi pozitif kabul edersek

$$
TP=25,
\qquad
FN=24,
\qquad
FP=30,
\qquad
TN=21
$$

Precision:

$$
P_{Jedi}=\frac{25}{25+30}=0.4545...\approx0.45
$$

Recall:

$$
R_{Jedi}=\frac{25}{25+24}=0.5102...\approx0.51
$$

F1:

$$
F1_{Jedi}
=
\frac{2(0.4545)(0.5102)}{0.4545+0.5102}
\approx0.48
$$

### Sith'i pozitif kabul edersek

Bu sefer confusion matrix'teki roller değişir:

$$
TP=21,
\qquad
FN=30,
\qquad
FP=24,
\qquad
TN=25
$$

Precision:

$$
P_{Sith}=\frac{21}{21+24}=0.4666...\approx0.47
$$

Recall:

$$
R_{Sith}=\frac{21}{21+30}=0.4117...\approx0.41
$$

F1:

$$
F1_{Sith}
=\frac{2(0.4666)(0.4117)}{0.4666+0.4117}
\approx0.44
$$

Böylece subject'in örnek çıktısındaki:

```text
Jedi  0.45  0.51  0.48  49
Sith  0.47  0.41  0.44  51
```

satırlarını doğrudan confusion matrix'ten yeniden üretebiliriz. fileciteturn0file0L71-L76

### Accuracy

Accuracy bütün doğru tahminlerin toplam örnek sayısına oranıdır:

$$
Accuracy
=
\frac{TP_{Jedi}+TP_{Sith}}{100}
=
\frac{25+21}{100}
=0.46
$$

Bu da subject'in `accuracy 0.46 100` satırıyla uyuşur. fileciteturn0file0L71-L76

Bu nedenle Ex00'ın örnek çıktısı, confusion matrix ile birlikte düşünüldüğünde oldukça tutarlı bir **sınıf-başına classification report + accuracy + confusion matrix** çıktısıdır.

