# 42 Data Science Piscine — DS_2 Tutorial
## Data Visualization ve Customer Clustering

> **Kaynak:** 42 Training Piscine datascience - 2 / Data Viz (`ds_2.pdf`)
>
> Bu rehber, PDF'deki exercise'leri başlangıç seviyesindeki bir öğrencinin anlayabileceği şekilde açıklamak için hazırlanmıştır. PDF'nin istediği şeylerle, projeyi yaparken kullanılması önerilen teknik yöntemler birbirinden ayrılmıştır.

---

# İçindekiler

- [DS_2'nin amacı](#ds_2nin-amacı)
- [Kullanılacak dil ve araçlar](#kullanılacak-dil-ve-araçlar)
- [Projeye başlamadan önce veri hazırlığı](#projeye-başlamadan-önce-veri-hazırlığı)
- [Exercise 00 — American Apple Pie](#exercise-00--american-apple-pie)
- [Exercise 01 — Initial Data Exploration](#exercise-01--initial-data-exploration)
- [Exercise 02 — My Beautiful Mustache](#exercise-02--my-beautiful-mustache)
- [Exercise 03 — Highest Building](#exercise-03--highest-building)
- [Exercise 04 — Elbow](#exercise-04--elbow)
- [Exercise 05 — Clustering](#exercise-05--clustering)
- [Clustering algoritmaları](#clustering-algoritmaları)
- [Ex05 grafiklerini okuma](#ex05-grafiklerini-okuma)
- [Önerilen proje klasörü](#önerilen-proje-klasörü)
- [Peer evaluation için bilinmesi gerekenler](#peer-evaluation-için-bilinmesi-gerekenler)
- [Son çalışma sırası](#son-çalışma-sırası)
- [Submission kontrol listesi](#submission-kontrol-listesi)

---

# DS_2'nin amacı

PDF'nin giriş bölümünde data analyst'in rolü; geçmiş ve güncel veriyi anlamak, grafikleri kullanarak sayıları ekiplerle açıklamak, öneriler geliştirmek ve karar vermeye yardımcı araçlar oluşturmak şeklinde tanımlanıyor.

PDF örnek araçlar olarak **R, Excel, Power BI ve Jupyter Notebook** veriyor ve bu modülde **hangi dili kullanacağının sana bırakıldığını** söylüyor.

Ayrıca iki önemli uyarı var:

- Ex00'da Module 01 Data Warehouse'a bağlanman gerekiyor.
- Grafiklerin Şubat verisi olmadan hazırlanmış örnekleri verilmiş; daha sonra bunların **yeni veriyle, yani Şubat verisi dahil edilerek yeniden yapılması** isteniyor.

Bu nedenle DS_2'yi sadece "grafik çizme" projesi olarak düşünme. Genel hikâye şöyledir:

```text
Veri
  ↓
Veriyi anlama
  ↓
İstatistiksel özetler
  ↓
Grafikler
  ↓
Müşteri özellikleri oluşturma
  ↓
Müşteri davranışlarını gruplama
  ↓
Gruplara iş anlamı verme
```

---

# Kullanılacak dil ve araçlar

## Dil: Python

**Benim önerim: Python kullan.**

Bu seçim PDF'nin kurallarına uygundur; çünkü PDF dili sana bırakıyor.

Python'u seçmenin DS_2 açısından avantajı, veri analizi, görselleştirme ve clustering işlerini aynı ekosistem içinde yapabilmendir.

Önerilen stack:

| Görev | Araç |
|---|---|
| Programlama dili | Python |
| Notebook / çalışma ortamı | Jupyter Notebook |
| Veri tabanı | PostgreSQL |
| SQL arayüzü | DBeaver |
| Tablo / veri analizi | Pandas |
| Sayısal işlemler | NumPy |
| Grafik | Matplotlib |
| İstatistiksel grafik | Seaborn |
| Clustering / ML | Scikit-learn |
| PostgreSQL ↔ Python | SQLAlchemy + psycopg2 |

## Language ve tool farkı

PDF'deki:

> "They often use tools such as ... R, Excel, Power BI, Jupyter Notebook ..."

ifadesi ilk bakışta karışık görünebilir. Çünkü burada dil ile uygulama/araç aynı şeymiş gibi sıralanmış.

Daha doğru ayrım:

```text
Python        = programlama dili
Jupyter       = Python kodunu notebook şeklinde çalıştırdığın ortam
Pandas        = Python kütüphanesi
Matplotlib    = Python grafik kütüphanesi
Scikit-learn  = Python machine-learning kütüphanesi
PostgreSQL    = database sistemi
DBeaver       = database'e bağlandığın GUI / SQL aracı
```

Dolayısıyla iki ayrı "zorunlu seçim" yapmıyorsun. Bir **teknoloji yığını** seçiyorsun.

Önerilen yapı:

```text
PostgreSQL
    ↓
veri saklama + SQL + JOIN + GROUP BY
    ↓
Python
    ↓
Pandas + NumPy
    ↓
Matplotlib + Seaborn
    ↓
Scikit-learn
```

## PostgreSQL / DBeaver ile her şeyi yapabilir miyiz?

Büyük kısmını veri hazırlama tarafında evet; fakat DS_2'nin tamamını yalnızca SQL ile yapmak iyi bir fikir değildir.

PostgreSQL'de çok rahat yapılabilecekler:

```sql
WHERE
GROUP BY
COUNT
SUM
AVG
MIN
MAX
DISTINCT
JOIN
DATE_TRUNC
```

Örneğin:

```sql
SELECT
    user_id,
    COUNT(*) AS frequency,
    SUM(price) AS monetary
FROM customers
WHERE event_type = 'purchase'
GROUP BY user_id;
```

Ama Python tarafı özellikle şu işlemlerde çok daha uygundur:

- grafik çizmek,
- DataFrame ile analiz yapmak,
- preprocessing / scaling,
- K-Means uygulamak,
- cluster sonuçlarını görselleştirmek.

En temiz yaklaşım:

```text
PostgreSQL = veri kaynağı ve SQL
DBeaver     = PostgreSQL'i inceleme / sorgulama aracı
Python      = analiz + visualization + clustering
Jupyter     = çalışmayı belgelediğin ortam
```

---

# Projeye başlamadan önce veri hazırlığı

Önceki projelerde oluşturduğun `customers` tablosunu temel veri kaynağı olarak kullanabilirsin. `items` ile yaptığın `product_id` JOIN'i de ürün bilgisine ihtiyacın olan yerlerde kullanılabilir.

## Şubat verisini kontrol et

PDF, grafiklerin Şubat verisiyle yeniden yapılmasını istiyor. Bu yüzden önce tarih aralığını kontrol et:

```python
df["event_time"].min()
df["event_time"].max()
```

Daha sonra ayları kontrol etmek için:

```python
df["event_time"].dt.to_period("M").value_counts().sort_index()
```

Burada yaklaşık olarak şunları görmek istersin:

```text
2022-10
2022-11
2022-12
2023-01
2023-02
```

## Temel veri kontrolleri

```python
df.head()
df.info()
df.isna().sum()
df.dtypes
```

Tarih sütunu gerçekten datetime değilse:

```python
df["event_time"] = pd.to_datetime(df["event_time"])
```

Price sayısal değilse:

```python
df["price"] = pd.to_numeric(df["price"], errors="coerce")
```

## Python'dan PostgreSQL'e bağlanma

Örneğin SQLAlchemy ile:

```python
from sqlalchemy import create_engine
import pandas as pd

engine = create_engine(
    "postgresql+psycopg2://USER:PASSWORD@HOST:5432/DATABASE"
)

query = """
SELECT *
FROM customers;
"""

df = pd.read_sql(query, engine)
```

Gerçek kullanıcı adı, parola, host ve database adını kendi ortamına göre kullanmalısın.

---

# Exercise 00 — American Apple Pie

## PDF'nin istediği

PDF'nin istediği şey:

- kendi pie chart'ını yapmak,
- insanların sitede ne yaptığını anlamaya çalışmak,
- Module 01 Data Warehouse'a bağlanmak.

## Amaç

Verideki `event_type` dağılımını hızlıca görmek.

Örneğin veride:

```text
view
cart
remove_from_cart
purchase
```

gibi event türleri varsa, bunların toplam event içindeki oranını gösterebilirsin.

## Pie chart nedir?

Pie chart, toplamı 100% kabul edip kategorilerin bu toplam içindeki payını gösterir.

Örneğin:

```text
purchase = 6,200
all events = 100,000
```

ise:

```text
6200 / 100000 × 100 = 6.2%
```

## SQL

```sql
SELECT
    event_type,
    COUNT(*) AS event_count
FROM customers
GROUP BY event_type
ORDER BY event_count DESC;
```

## Python

```python
import matplotlib.pyplot as plt

counts = df["event_type"].value_counts()

plt.figure(figsize=(7, 7))
plt.pie(
    counts.values,
    labels=counts.index,
    autopct="%1.1f%%"
)
plt.title("Site Event Distribution")
plt.show()
```

## Bu grafikten ne öğreniyoruz?

Örneğin `view` çok yüksek, `purchase` çok düşükse:

```text
çok kişi ürünü görüyor
        ↓
çok az kişi satın alıyor
```

gibi bir business sorusu ortaya çıkabilir.

Bu grafik henüz clustering değildir. Ama bütün analiz sürecinin ilk adımı olan **veriyi tanıma** işini yapar.

---

# Exercise 01 — Initial Data Exploration

## PDF'nin istediği

PDF açıkça şunları istiyor:

- sadece `event_type = purchase` kayıtlarını tutmak,
- Ekim 2022 başından Şubat 2023 sonuna kadar veri kullanmak,
- aşağıdaki mantıktaki 3 grafiği oluşturmak.

PDF örneklerinde görülen üç temel metrik:

1. Number of customers
2. Total sales
3. Average spend/customer

## İlk adım: purchase filtresi

```python
purchase_df = df[df["event_type"] == "purchase"].copy()
```

Bu çok önemli.

`view` bir satın alma değildir.

`cart` bir satın alma değildir.

`remove_from_cart` bir satın alma değildir.

Bu exercise satın alma davranışına odaklanıyor.

---

## Grafik A — Number of Customers

### Y ekseni ne?

```text
Number of customers
```

Yani belirli zaman aralığında satın alma yapan **benzersiz müşteri sayısı**.

Burada kritik nokta `purchase event sayısı` ile `customer sayısı` arasındaki farktır.

Örneğin:

```text
user_10 → purchase A
user_10 → purchase B
user_10 → purchase C
```

3 purchase event vardır ama benzersiz müşteri sayısı:

```text
1
```

olur.

Bu yüzden müşteri sayarken çoğu durumda:

```python
nunique()
```

kullanılır.

Örneğin günlük benzersiz müşteri sayısı:

```python
daily_customers = (
    purchase_df
    .groupby(purchase_df["event_time"].dt.date)["user_id"]
    .nunique()
)
```

### Grafik ne anlatıyor?

Zaman içinde:

> "Kaç farklı müşteri satın alma yaptı?"

sorusunu cevaplar.

---

## Grafik B — Total Sales

PDF örneğinde y ekseni yaklaşık olarak:

```text
total sales in million of A
```

şeklindedir.

Buradaki `A`, PDF'nin belirttiği **Altairian Dollars** birimidir.

### Hesap

Bir ay içindeki tüm purchase fiyatlarını toplarsın:

```text
monthly total sales
=
 o ayın purchase kayıtlarındaki price toplamı
```

SQL:

```sql
SELECT
    DATE_TRUNC('month', event_time) AS month,
    SUM(price) AS total_sales
FROM customers
WHERE event_type = 'purchase'
GROUP BY DATE_TRUNC('month', event_time)
ORDER BY month;
```

Python'da:

```python
monthly_sales = (
    purchase_df
    .set_index("event_time")
    .resample("MS")["price"]
    .sum()
)
```

Grafikte milyon cinsinden göstermek istersen:

```python
monthly_sales_million = monthly_sales / 1_000_000
```

### Grafik ne anlatıyor?

> "Site hangi aylarda daha fazla satış yaptı?"

sorusunu cevaplar.

---

## Grafik C — Average Spend / Customer

Bu grafik:

```text
müşteri başına ortalama harcama
```

gösterir.

Basit formül:

```text
total sales
----------------------------
unique purchasing customers
```

Örneğin:

```text
Total sales = 1,000,000 A
Customers   = 30,000
```

ise:

```text
Average spend/customer = 33.33 A
```

Python:

```python
daily = (
    purchase_df
    .groupby(purchase_df["event_time"].dt.date)
    .agg(
        total_sales=("price", "sum"),
        customers=("user_id", "nunique")
    )
)

daily["avg_spend_customer"] = (
    daily["total_sales"] / daily["customers"]
)
```

## Ex01'in ana fikri

Üç grafik aslında üç farklı soruyu cevaplıyor:

```text
Kaç müşteri satın aldı?
        ↓
Number of customers

Ne kadar para geldi?
        ↓
Total sales

Müşteri başına ne kadar para geldi?
        ↓
Average spend/customer
```

---

# Exercise 02 — My Beautiful Mustache

## PDF'nin istediği

PDF şu istatistikleri istiyor:

- mean
- median
- min
- max
- first quartile
- second quartile
- third quartile

Ayrıca:

- satın alınan item price'ları için box plot,
- kullanıcı başına average basket price için box plot.

PDF'deki örnek istatistiklerde şu değerler gösteriliyor:

```text
count = 741644
mean  = 5.575068
std   = 10.264594
min   = -79.370000
Q1    = 1.590000
Q2    = 3.330000
Q3    = 6.030000
max   = 327.780000
```

Bu rakamlar PDF'deki örnek output'tur. Kendi güncellenmiş verinde yeniden hesaplamalısın.

---

## Mean

Mean aritmetik ortalamadır.

```text
2 + 4 + 6
--------- = 4
    3
```

Python:

```python
prices.mean()
```

---

## Median

Median, sıralanmış verinin ortasındaki değerdir.

```text
1, 3, 5
```

median = `3`.

Çift sayıda gözlem varsa ortadaki iki değerin ortalaması alınır:

```text
1, 3, 5, 7
```

```text
(3 + 5) / 2 = 4
```

Python:

```python
prices.median()
```

---

## Min ve Max

```text
min = en küçük değer
max = en büyük değer
```

Python:

```python
prices.min()
prices.max()
```

---

## Quartile nedir?

Quartile, veriyi dört bölüme ayırmak için kullanılan yüzdelik noktalarıdır.

```text
0%          25%          50%          75%         100%
|------------|------------|------------|-------------|
             Q1           Q2           Q3
```

- `Q1` = 25. percentile
- `Q2` = 50. percentile = median
- `Q3` = 75. percentile

Python:

```python
prices.quantile(0.25)
prices.quantile(0.50)
prices.quantile(0.75)
```

---

## Box plot nedir?

Box plot bir sayısal dağılımı kompakt biçimde özetler.

Temel parçalar:

```text
        outlier
           •
           |
---|------[---|---]------|---
   |          |          |
  Q1        median      Q3
```

Detay:

- kutunun sol tarafı = Q1
- kutunun içindeki çizgi = median = Q2
- kutunun sağ tarafı = Q3
- kutunun genişliği = IQR
- whisker'ların dışında kalan noktalar çoğu zaman outlier olarak gösterilir

### IQR

```text
IQR = Q3 - Q1
```

IQR, ortadaki %50'lik bölümün yayılımını temsil eder.

### Outlier sınırı

Yaygın box-plot kuralı:

```text
lower = Q1 - 1.5 × IQR
upper = Q3 + 1.5 × IQR
```

Bunun dışında kalan noktalar outlier olarak işaretlenebilir.

---

## PDF'deki negatif price neden var?

PDF örneğinde:

```text
min = -79.37
```

görünüyor.

Bu durumun nedenini PDF açıklamıyor.

Bu nedenle negatif kayıtları sadece grafik daha güzel görünsün diye otomatik olarak silme.

Önce incele:

```python
purchase_df[purchase_df["price"] < 0]
```

Sonra verinin iş kuralını anlamaya çalış.

Önemli nokta:

> Kaynak doküman negatif değerlerin sebebini açıklamadığı için bu sebep hakkında kesin bir yorum yapmak doğru değildir.

---

## İlk box plot — purchased item prices

Akış:

```text
purchase records
      ↓
price sütunu
      ↓
box plot
```

Örnek:

```python
import seaborn as sns
import matplotlib.pyplot as plt

plt.figure(figsize=(8, 4))
sns.boxplot(x=purchase_df["price"])
plt.xlabel("Price (Altairian Dollars)")
plt.title("Purchased Item Prices")
plt.show()
```

### Grafik neden sıkışık görünebilir?

Birçok ürün düşük fiyatlıyken birkaç ürün çok pahalıysa dağılım sağa doğru uzayabilir.

Örneğin:

```text
1  2  2  3  3  4  5  6  8  10  150  300
```

Ana dağılım solda sıkışmış görünür; birkaç büyük değer x eksenini uzatır.

---

## İkinci box plot — average basket price per user

Burada artık tek tek ürün fiyatlarına bakmıyoruz.

Önce kullanıcı bazında bir basket metriği çıkarıyoruz.

Örneğin mantık:

```text
user_1 → basket metric = 28.5 A
user_2 → basket metric = 33.1 A
user_3 → basket metric = 42.0 A
...
```

Sonra bu kullanıcı bazlı değerlerin dağılımına box plot uyguluyoruz.

### Çok önemli ayrım

```text
item price
```
ile

```text
average basket price per user
```

aynı şey değildir.

Birincisi ürün fiyatlarının dağılımıdır.

İkincisi kullanıcı seviyesine yükseltilmiş bir alışveriş sepeti metriğidir.

Burada basket'in tam olarak nasıl tanımlanacağı dataset'in kolon yapısına bağlıdır. PDF bu formülü ayrıntılı biçimde vermediği için gerçek veri yapısına bakarak belirlemek gerekir.

---

# Exercise 03 — Highest Building

## PDF'nin istediği

İki grafik isteniyor:

- order'ların frequency'sine göre dağılım,
- müşterilerin sitede harcadığı Altairian Dollars miktarına göre dağılım.

## Frequency nedir?

Bu bağlamda frequency, müşterinin kaç satın alma/order gerçekleştirdiğini ifade eden müşteri davranışı metriği olarak düşünülebilir.

Örneğin:

```text
user_A → 1
user_B → 2
user_C → 8
user_D → 2
```

Ardından şu soruya bakarsın:

```text
frequency = 1 olan kaç müşteri var?
frequency = 2 olan kaç müşteri var?
frequency = 3 olan kaç müşteri var?
...
```

## Monetary value nedir?

Monetary value, müşterinin toplam harcamasıdır.

```text
user_A → 42 A
user_B → 100 A
user_C → 180 A
```

gibi.

Python:

```python
monetary = (
    purchase_df
    .groupby("user_id")["price"]
    .sum()
)
```

## Histogram nedir?

Histogram sayısal veriyi aralıklara böler ve her aralıkta kaç gözlem olduğunu gösterir.

Örneğin:

```text
Frequency
0-10    → 65000 customers
10-20   → 15000 customers
20-30   → 5000 customers
30-40   → 1000 customers
```

Bu bize örneğin müşterilerin çoğunun az sayıda satın alma yaptığını gösterebilir.

## Ex03 neden önemli?

Çünkü Ex03 seni Ex04 ve Ex05'te kullanacağın müşteri davranışlarına hazırlıyor:

```text
Frequency → ne kadar sık alışveriş yapıyor?
Monetary  → ne kadar para harcıyor?
```

---

# Exercise 04 — Elbow

## PDF'nin istediği

PDF iki şeyi özellikle istiyor:

- optimal cluster sayısını anlamak için Elbow Method kullanmak,
- neden seçtiğin cluster sayısını açıklayabilmek.

Bu exercise, Ex05'in hazırlığıdır.

---

## Önce cluster nedir?

Cluster = birbirine benzer özelliklere sahip gözlemlerin grubu.

Customer örneği:

```text
A → sık alışveriş + çok para
B → az alışveriş + az para
C → sık alışveriş + orta para
D → uzun zamandır alışveriş yapmıyor
```

Algoritma benzer müşterileri aynı grupta toplamaya çalışabilir.

---

## Clustering neden kullanılır?

Çoğu durumda elimizde hazır bir:

```text
customer_type
```

kolonu yoktur.

Ama davranış verileri vardır.

Clustering şu soruya cevap arar:

> "Benzer davranan müşteriler hangi gruplarda toplanıyor?"

Bu nedenle clustering **unsupervised learning** örneğidir.

---

## Unsupervised learning nedir?

Supervised learning'de input ve bilinen target vardır:

```text
X → input
Y → doğru etiket
```

Clustering'de ise başlangıçta hedef etiketi yoktur:

```text
X var
Y yok
```

Algoritma grupları kendi yapısından çıkarmaya çalışır.

---

## Neden cluster sayısı seçiyoruz?

Örneğin K-Means kullanırken:

```python
KMeans(n_clusters=4)
```

dersen algoritmaya 4 cluster istediğini söylemiş olursun.

Ama:

```text
Neden 4?
Neden 3 değil?
Neden 5 değil?
```

sorusunun bir gerekçesi olmalıdır.

Elbow Method burada kullanılır.

---

## Inertia nedir?

K-Means'te inertia, her gözlemin kendi cluster centroid'ine olan uzaklıklarının karelerinin toplamıyla ilişkili bir ölçüdür.

Sezgisel olarak:

> Aynı cluster içindeki noktalar kendi merkezlerine ne kadar yakın?

Noktalar merkezlerine yaklaştıkça inertia düşer.

K sayısını artırdıkça inertia'nın düşmesi normaldir. Çünkü daha fazla cluster kullanarak veriyi daha küçük parçalara bölebilirsin.

Ama çok fazla cluster kullanmak business açısından gereksiz veya anlamsız olabilir.

---

## Elbow Method nedir?

Farklı K değerlerini denersin:

```text
K = 1
K = 2
K = 3
...
K = 10
```

Her biri için inertia hesaplanır.

Örneğin hayali değerler:

```text
K=1  → 270000
K=2  → 160000
K=3  → 105000
K=4  →  85000
K=5  →  73000
K=6  →  65000
K=7  →  59000
```

Küçük K'dan başlayınca büyük iyileşmeler vardır. Bir noktadan sonra ek cluster'ın sağladığı iyileşme küçülmeye başlar.

Grafik kabaca:

```text
Inertia
  |
  |\
  | \
  |  \
  |   \__
  |      \___
  +------------------- K
       ↑
     elbow
```

Bükülmenin başladığı nokta "elbow" olarak adlandırılır.

### Çok önemli

Elbow Method sana her zaman matematiksel olarak tek ve tartışmasız bir K vermez.

Seçimini şu üç şeyi birlikte değerlendirerek savun:

```text
Elbow noktası
+
cluster'ların yorumlanabilirliği
+
business amacı
```

---

## Elbow kodu

Önce kullanacağın feature'ları seç:

```python
features = rfm[[
    "recency",
    "frequency",
    "monetary"
]]
```

Sonra standardize et:

```python
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
X = scaler.fit_transform(features)
```

K değerlerini dene:

```python
from sklearn.cluster import KMeans

inertias = []

for k in range(1, 11):
    model = KMeans(
        n_clusters=k,
        random_state=42,
        n_init=10
    )
    model.fit(X)
    inertias.append(model.inertia_)
```

Grafik:

```python
plt.figure(figsize=(8, 5))
plt.plot(range(1, 11), inertias, marker="o")
plt.xlabel("Number of clusters (K)")
plt.ylabel("Inertia")
plt.title("Elbow Method")
plt.show()
```

---

# Exercise 05 — Clustering

## PDF'nin istediği

PDF şu hedefi veriyor:

- müşterileri ticari hedefleme için gruplamak,
- en az 4 grup oluşturmak,
- bir clustering algorithm kullanmak,
- grupların en az 2 grafikle gösterilmesi.

PDF örnek olarak şu tür gruplardan söz ediyor:

```text
new customer
inactive customer
loyal customer
gold / silver / platinum
```

Buradaki isimler örnek business segmentleridir.

---

## Çok önemli: Cluster numarası ile business segment aynı şey değildir

Algoritma sana şunu verebilir:

```text
Cluster 0
Cluster 1
Cluster 2
Cluster 3
```

Bu etiketler otomatik olarak:

```text
gold
silver
platinum
inactive
```

anlamına gelmez.

Önce cluster'ların özelliklerine bakarsın; sonra onlara business anlamı verirsin.

---

# RFM: Customer clustering için temel özellikler

RFM:

```text
R = Recency
F = Frequency
M = Monetary
```

## Recency

Müşterinin son alışverişinden itibaren geçen süre.

Örneğin referans tarih:

```text
2023-03-01
```

Son alışveriş:

```text
2023-02-28
```

ise recency yaklaşık:

```text
1 gün
```

Son alışveriş:

```text
2022-11-01
```

ise recency çok daha büyüktür.

**Recency küçükse müşteri daha yakın zamanda alışveriş yapmıştır.**

---

## Frequency

Müşterinin kaç satın alma gerçekleştirdiği.

```text
A → 30
B → 5
C → 1
```

30, 5'ten daha yüksek frequency'dir.

---

## Monetary

Müşterinin toplam harcaması.

```text
A → 1000 A
B → 250 A
C → 10 A
```

1000 daha yüksek monetary value'dir.

---

# Customer-level tablo neden gerekiyor?

K-Means'e event tablosunu olduğu gibi vermek istemiyoruz.

Event tablosunda bir müşteri birçok satıra sahip olabilir:

```text
user_id | event_time | price | event_type
-------------------------------------------
A       | ...        | 10    | purchase
A       | ...        | 20    | purchase
A       | ...        | 15    | purchase
B       | ...        | 5     | purchase
```

Clustering için daha uygun yapı:

```text
user_id | recency | frequency | monetary
-----------------------------------------
A       | 2       | 3         | 45
B       | 30      | 1         | 5
```

Yani:

> **bir satır = bir müşteri**

olmalı.

---

## RFM tablosu oluşturma

Örnek yaklaşım:

```python
reference_date = (
    purchase_df["event_time"].max()
    + pd.Timedelta(days=1)
)

rfm = (
    purchase_df
    .groupby("user_id")
    .agg(
        last_purchase=("event_time", "max"),
        frequency=("event_time", "count"),
        monetary=("price", "sum")
    )
)

rfm["recency"] = (
    reference_date - rfm["last_purchase"]
).dt.days

rfm = rfm.reset_index()
```

Bu örnekte:

```text
frequency = purchase sayısı
monetary  = toplam price
recency   = referans tarihten son purchase'a kadar geçen gün
```

Not: PDF, RFM formülünü bu ayrıntı seviyesinde standartlaştırmıyor. Buradaki formül, customer segmentation için yaygın ve anlaşılır bir uygulama örneğidir.

---

# Neden scaling gerekiyor?

K-Means mesafe tabanlıdır.

Farz edelim:

```text
recency   = 10
frequency = 20
monetary  = 500
```

Monetary diğerlerinden çok daha büyük ölçeğe sahip.

Euclidean distance kabaca:

```text
sqrt(
    (x1-y1)^2 +
    (x2-y2)^2 +
    (x3-y3)^2
)
```

şeklindedir.

Bu durumda büyük ölçekli `monetary` mesafe hesabında çok daha baskın hale gelebilir.

---

## StandardScaler

```python
from sklearn.preprocessing import StandardScaler

features = rfm[[
    "recency",
    "frequency",
    "monetary"
]]

scaler = StandardScaler()
X = scaler.fit_transform(features)
```

StandardScaler feature'ları benzer bir ölçeğe getirir; tipik olarak her feature'ın mean'i yaklaşık 0, standard deviation'ı yaklaşık 1 olur.

---

# K-Means

## K-Means nedir?

K-Means, çok kullanılan bir clustering algoritmasıdır.

Sezgisel çalışma mantığı:

```text
1. K tane centroid başlat
2. Her müşteriyi en yakın centroid'e ata
3. Her cluster'ın yeni merkezini hesapla
4. Müşteri atamalarını tekrar yap
5. Sonuç yeterince değişmeyene kadar devam et
```

---

## Centroid nedir?

Centroid bir cluster'ın merkezini temsil eden noktadır.

Örneğin:

```text
Customer 1 → (2, 10)
Customer 2 → (4, 20)
Customer 3 → (6, 30)
```

Bu üç noktanın merkezi feature bazındaki ortalamadır:

```text
x = (2+4+6)/3 = 4

y = (10+20+30)/3 = 20
```

Yani centroid:

```text
(4, 20)
```

olur.

K-Means'in amacı müşterileri en yakın centroid'lere göre kümelere ayırmaktır.

---

## K-Means uygulama

Elbow'dan sonra örneğin `K = 4` seçtiğimizi varsayalım:

```python
from sklearn.cluster import KMeans

kmeans = KMeans(
    n_clusters=4,
    random_state=42,
    n_init=10
)

rfm["cluster"] = kmeans.fit_predict(X)
```

Artık:

```text
user_id | recency | frequency | monetary | cluster
----------------------------------------------------
A       | 2       | 20        | 500      | 3
B       | 60      | 1         | 10       | 0
C       | 8       | 6         | 100      | 2
```

gibi bir tablon vardır.

---

# Cluster profiling

Cluster'ları isimlendirmeden önce ortalamalarını / medyanlarını incele.

```python
profile = (
    rfm
    .groupby("cluster")
    [["recency", "frequency", "monetary"]]
    .mean()
)

print(profile)
```

Daha kapsamlı profil:

```python
profile = (
    rfm
    .groupby("cluster")
    .agg(
        customers=("user_id", "count"),
        mean_recency=("recency", "mean"),
        median_recency=("recency", "median"),
        mean_frequency=("frequency", "mean"),
        median_frequency=("frequency", "median"),
        mean_monetary=("monetary", "mean"),
        median_monetary=("monetary", "median"),
    )
)
```

Örneğin hayali sonuç:

```text
cluster  recency  frequency  monetary
0           90        1         10
1            2       20        500
2           10        5          80
3            5       10         250
```

Bu durumda kabaca:

```text
0 → inactive'e benzeyebilir
1 → çok değerli / loyal olabilir
2 → düşük frekanslı regular olabilir
3 → güçlü regular olabilir
```

Bunlar **örnek yorumlardır**. Gerçek isimlendirmeyi kendi sonuçlarına göre yapmalısın.

---

# Ex05 — Birinci grafik: segment büyüklüğü

PDF örneğinde:

```text
Y ekseni:
Loyal customers
New customers
inactive
```

gibi segmentler vardır.

X ekseni:

```text
number of customers
```

dır.

Yani grafik:

> "Her customer segmentinde kaç kişi var?"

sorusunu cevaplar.

Örneğin:

```text
Loyal    → 39586
New      → 38253
Inactive → 12133
```

gibi değerler PDF örneğinde görülebilir.

Bu değerleri kendi güncel veri setin için yeniden hesaplamalısın.

## Neden bu grafik business açısından önemli?

Çünkü segment büyüklüğünü görmek doğrudan kampanya planlamasına yardım eder.

Örneğin:

```text
inactive
  → müşteriyi geri getirecek kampanya

new
  → welcome offer

loyal
  → loyalty / VIP offer
```

Bu yüzden clustering'in amacı yalnızca noktaları farklı renklere boyamak değildir.

---

# Ex05 — İkinci grafik: scatter plot

PDF örneklerinde müşteri gruplarını 2 boyutta göstermek için scatter plot kullanılıyor.

Örneğin:

```text
X = Recency
Y = Frequency
```

Her nokta bir müşteridir.

---

## Scatter plot nedir?

Scatter plot, iki sayısal değişkeni noktalar halinde gösterir.

Örneğin:

```text
Frequency
100 |             •
 80 |        •  •   •
 60 |    •      • •
 40 | •   •  •
 20 | • •
  0 +------------------------
      0  20  40  60  80  Recency
```

Bir noktanın:

```text
x = 20
y = 60
```

olması:

```text
recency = 20
days
frequency = 60
```

gibi okunabilir.

---

# X ekseni ve Y ekseni nasıl okunur?

## X = Recency

Sağa gittikçe recency artıyorsa:

```text
solda  → daha yeni alışveriş
sağda  → daha uzun süre önce alışveriş
```

Yani recency için sağa doğru gitmek genellikle "daha aktif" anlamına gelmez. Tam tersine, daha yüksek recency daha uzun süredir satın almamış olmayı ifade eder.

## Y = Frequency

Yukarı çıktıkça:

```text
frequency ↑
```

yani müşterinin satın alma sayısı artar.

---

# Scatter plot'taki renkler ne demek?

Her renk farklı cluster'ı gösterir.

Örneğin:

```text
mavi   → cluster 0
yeşil  → cluster 1
mor    → cluster 2
sarı   → cluster 3
```

Rengin kendisinin matematiksel bir anlamı yoktur.

Renk sadece:

> "bu nokta şu cluster'a ait"

demek için kullanılır.

---

# Büyük sarı noktalar / X işaretleri ne?

PDF'deki büyük noktalar genellikle **centroid**leri temsil eder.

Küçük noktalar:

```text
müşteriler
```

Büyük noktalar:

```text
cluster merkezleri
```

olarak düşünülebilir.

Şema:

```text
        •
      •   •
    •   C   •
      •   •
        •
```

Buradaki `C` centroid'tir.

---

# PDF'deki "Median Recency" ve "Median Frequency"

PDF'nin bazı grafiklerinde `Median Recency` ve `Median Frequency` gibi ifadeler görülür.

Bunlar o cluster içindeki değerlerin medyanını ifade eder.

Örneğin bir cluster'ın recency değerleri:

```text
1, 2, 3, 5, 100
```

ise median:

```text
3
```

dir.

Bu değer mean değildir.

---

# PDF'deki `??` veya `?` işaretleri

Örnek grafiklerde veya metinlerde:

```text
Average "Loyal customers": ?? A
```

gibi placeholder'lar görebilirsin.

Bunlar:

> "Bu değeri sen hesaplamalısın."

anlamındadır.

Yani `??` veri setindeki gerçek bir değer veya Python syntax'ı değildir.

Örneğin cluster'ı loyal olarak adlandırdıysan ve istenen metrik ortalama monetary ise, o cluster'a ait müşterilerin ilgili değerlerini hesaplayıp yerine kendi sonucunu koyarsın.

---

# Clustering algoritmaları

PDF yalnızca:

> "You have to use a Clustering Algorithms"

diyor. Tek bir algoritma adı zorunlu olarak verilmemiş.

Bu nedenle clustering algoritmalarının temel ailelerini bilmek yararlı.

## K-Means

En temel centroid tabanlı yöntemlerden biridir.

İyi bir başlangıç noktasıdır çünkü:

- kolay açıklanır,
- hızlıdır,
- sayısal customer features ile uyumludur,
- Elbow Method ile K incelemesine uygundur.

Dezavantajları:

- K seçmek gerekir,
- outlier'lardan etkilenebilir,
- feature scaling önemlidir,
- cluster şekilleri konusunda belirli varsayımları vardır.

**DS_2 için ilk tercihim K-Means.**

---

## Hierarchical / Agglomerative Clustering

Başlangıçta gözlemler ayrı gruplardır ve yakın olan gruplar aşama aşama birleştirilir.

Örneğin:

```text
A B C D
↓
(A,B) (C,D)
↓
((A,B),(C,D))
```

gibi bir hiyerarşi oluşabilir.

Dendrogram ile gösterilmesi yaygındır.

---

## DBSCAN

DBSCAN yoğunluk tabanlı bir yöntemdir.

Özellikle:

- noise / outlier tespiti,
- daire şeklinde olması gerekmeyen cluster'lar

gibi durumlarda yararlıdır.

Avantaj:

```text
noise ayrıştırabilir
```

Dezavantaj:

```text
parametre seçimi önemlidir
```

ve farklı yoğunluktaki gruplarda zorlanabilir.

---

## Gaussian Mixture Model

Gaussian Mixture Model, veriyi birden fazla olasılık dağılımının karışımı olarak modellemeye çalışır.

K-Means'teki gibi yalnızca kesin bir cluster etiketi vermek yerine bir gözlemin farklı cluster'lara ait olma olasılıklarını modellemek mümkündür.

---

## Başka algoritmalar var mı?

Evet.

Örneğin:

- Spectral Clustering
- Mean Shift
- OPTICS
- BIRCH

gibi başka yaklaşımlar da vardır.

Bu yüzden "kaç tane clustering algoritması var?" sorusunun sabit bir cevabı yoktur.

DS_2 için hepsini uygulaman gerekmiyor. **K-Means ile sağlam bir çözüm oluşturmak yeterli ve mantıklı bir başlangıçtır.**

---

# Ex05'te clustering'in gerçek amacı

Şirket açısından sonuç şu değildir:

```text
Cluster 0
Cluster 1
Cluster 2
Cluster 3
```

Asıl hedef:

```text
müşteri davranışı
      ↓
segment
      ↓
marketing action
```

Örneğin:

```text
New
  → welcome offer

Inactive
  → win-back coupon

High-value loyal
  → premium / VIP offer
```

Bu nedenle cluster'ları yorumlamak en az algoritmayı çalıştırmak kadar önemlidir.

---

# Ex04 + Ex05 için tam pipeline

```text
PURCHASE DATA
     ↓
CUSTOMER-LEVEL AGGREGATION
     ↓
RFM
     ↓
DATA CHECK
     ↓
STANDARDIZATION
     ↓
ELBOW METHOD
     ↓
K SELECTION
     ↓
K-MEANS
     ↓
CLUSTER LABELS
     ↓
CLUSTER PROFILING
     ↓
BUSINESS SEGMENT NAMES
     ↓
AT LEAST 2 GRAPHS
```

---

# Neden cluster'ları adlandırmadan önce profile bakıyoruz?

Çünkü K-Means sana sadece sayılar verir:

```text
0
1
2
3
```

Ama business dünyasında:

```text
New customer
Inactive customer
Loyal customer
High-value customer
```

gibi anlamlı isimler gerekir.

Örneğin:

```text
Cluster 0
recency      = yüksek
frequency    = düşük
monetary     = düşük
```

ise inactive yorumu mantıklı olabilir.

Başka cluster:

```text
recency      = düşük
frequency    = yüksek
monetary     = yüksek
```

ise loyal / high-value yorumu daha mantıklı olabilir.

Bu isimler **algoritmanın otomatik olarak ürettiği gerçekler değil, cluster profile'a dayanan yorumlardır.**

---

# Mean mi Median mi?

Customer spending gibi değişkenlerde outlier olabilir.

Örneğin:

```text
10
12
15
20
21
22
5000
```

Mean çok yükselir.

Median ise ortadaki müşteri davranışını daha iyi temsil edebilir.

Bu nedenle cluster profile oluştururken hem mean hem median bakmak yararlı olabilir.

---

# Önerilen proje klasörü

PDF submission için belirli dosya adları veriyor. Çalışma ortamında notebook kullanmak istiyorsan şu yapı rahat olabilir:

```text
ds_2/
│
├── ex00/
│   └── pie.ipynb
│
├── ex01/
│   └── chart.ipynb
│
├── ex02/
│   └── mustache.ipynb
│
├── ex03/
│   └── Building.ipynb
│
├── ex04/
│   └── elbow.ipynb
│
├── ex05/
│   └── Clustering.ipynb
│
└── README.md
```

Ancak submission sırasında PDF'nin istediği dosya adlarına ve extension'a dikkat et.

PDF'de istenen isimler:

```text
ex00 → pie.*
ex01 → chart.*
ex02 → mustache.*
ex03 → Building.*
ex04 → elbow.*
ex05 → Clustering.*
```

---

# Peer evaluation için bilinmesi gerekenler

## "Neden Python?"

Şöyle açıklayabilirsin:

> Python'u seçtim çünkü data analysis, visualization ve clustering işlemlerini aynı ekosistemde yapabiliyorum. PostgreSQL'i veri kaynağı olarak kullanıp Python tarafında Pandas, Matplotlib, Seaborn ve Scikit-learn kullanıyorum.

## "PostgreSQL neden?"

> Veriyi merkezi olarak saklamak ve SQL ile filtreleme, aggregation ve JOIN işlemlerini yapmak için.

## "DBeaver nedir?"

> PostgreSQL gibi database sistemlerine bağlanıp SQL yazmak ve veriyi incelemek için kullanılan bir arayüz.

## "Jupyter neden?"

> Kod, açıklama, sonuç ve grafik aynı notebook içinde tutulabildiği için data analysis çalışmasını takip etmeyi kolaylaştırıyor.

## "Neden sadece PostgreSQL kullanmadın?"

> SQL veri hazırlama ve aggregation için çok uygun. Ancak grafik, preprocessing, scaling ve clustering gibi işlemler için Python ekosistemi daha uygun.

## "Neden K-Means?"

> Sayısal customer-level features kullandığım için K-Means basit ve yorumlanabilir bir başlangıç clustering yöntemi. Ayrıca Elbow Method ile K değerini inceleyebiliyorum.

## "Centroid nedir?"

> Bir cluster'ın merkezini temsil eden feature ortalaması noktasıdır. K-Means müşterileri en yakın centroid'e göre gruplar.

## "Elbow neden kullandın?"

> Farklı K değerlerinde inertia'yı karşılaştırmak için. Büyük düşüşlerin azalmaya başladığı kırılma noktasını ve cluster'ların business olarak yorumlanabilirliğini birlikte değerlendiriyorum.

## "Recency nedir?"

> Müşterinin son satın almasından itibaren geçen süre. Düşük recency, müşterinin daha yakın zamanda satın aldığını gösterir.

## "Frequency nedir?"

> Müşterinin kaç kez satın alma yaptığı.

## "Monetary nedir?"

> Müşterinin toplam harcaması.

---

# Son çalışma sırası

Bu projeye sıfırdan başlıyorsan şu sırayı takip et:

## Aşama A — Ortamı kur

```text
Python
Jupyter
Pandas
Matplotlib
Seaborn
Scikit-learn
SQLAlchemy
psycopg2
```

## Aşama B — Database bağlantısını test et

DBeaver'de önce SQL'in çalıştığından emin ol.

Sonra aynı veriyi Python'dan oku.

## Aşama C — Data validation

```python
df.head()
df.info()
df.isna().sum()
df["event_time"].min()
df["event_time"].max()
```

## Aşama D — Ex00

```text
event_type
   ↓
count
   ↓
pie chart
```

## Aşama E — Ex01

```text
purchase only
   ↓
customers
sales
average spend
   ↓
3 charts
```

## Aşama F — Ex02

```text
purchase prices
   ↓
mean / median / quartiles
   ↓
box plot
   ↓
customer basket metric
   ↓
second box plot
```

## Aşama G — Ex03

```text
customer aggregation
   ↓
frequency
monetary
   ↓
distribution charts
```

## Aşama H — Ex04

```text
RFM
   ↓
scaling
   ↓
K=1..10
   ↓
inertia
   ↓
elbow
```

## Aşama I — Ex05

```text
RFM
   ↓
KMeans
   ↓
cluster labels
   ↓
cluster profile
   ↓
segment names
   ↓
2+ graphs
```

---

# Submission kontrol listesi

## Genel

- [ ] PostgreSQL bağlantısı çalışıyor.
- [ ] February verisi dahil.
- [ ] `event_time` doğru datetime tipinde.
- [ ] `price` doğru numeric tipinde.
- [ ] Null / hatalı kayıtlar kontrol edildi.

## Ex00

- [ ] Data Warehouse'a bağlanıldı.
- [ ] Event type dağılımı hesaplandı.
- [ ] Pie chart oluşturuldu.

## Ex01

- [ ] Sadece purchase kullanıldı.
- [ ] October 2022 → February 2023 aralığı kapsandı.
- [ ] Number of customers grafiği var.
- [ ] Total sales grafiği var.
- [ ] Average spend/customer grafiği var.
- [ ] X/Y eksenleri anlaşılır.

## Ex02

- [ ] Mean
- [ ] Median
- [ ] Min
- [ ] Max
- [ ] Q1
- [ ] Q2
- [ ] Q3
- [ ] Item price box plot
- [ ] Average basket price/user box plot
- [ ] Outlier'ların ne olduğu açıklanabiliyor.

## Ex03

- [ ] Frequency dağılımı
- [ ] Monetary dağılımı
- [ ] Grafik eksenleri anlaşılır

## Ex04

- [ ] Farklı K değerleri denendi.
- [ ] Inertia hesaplandı.
- [ ] Elbow grafiği var.
- [ ] K seçimi açıklanabiliyor.

## Ex05

- [ ] En az 4 grup
- [ ] Clustering algorithm kullanıldı.
- [ ] Cluster profile çıkarıldı.
- [ ] Segment isimleri profile dayanıyor.
- [ ] En az 2 grafik
- [ ] Scatter plot eksenleri açıklanabiliyor.
- [ ] Centroid açıklanabiliyor.
- [ ] `??` / placeholder değerlerin kendi verinden hesaplanması sağlandı.

---

# En önemli zihinsel model

DS_2'yi şu zincir olarak düşün:

```text
                     DATA
                       │
                       ▼
                 POSTGRESQL
                       │
                  SQL / JOIN
                       │
                       ▼
                    PANDAS
                       │
          ┌────────────┴────────────┐
          │                         │
          ▼                         ▼
   DATA VISUALIZATION         CUSTOMER FEATURES
          │                         │
          │                  RFM / diğer metrics
          │                         │
          │                         ▼
          │                    SCALING
          │                         │
          │                         ▼
          │                      ELBOW
          │                         │
          │                         ▼
          │                     K-MEANS
          │                         │
          └────────────┬────────────┘
                       ▼
                CUSTOMER SEGMENTS
                       │
                       ▼
                BUSINESS ACTION
```

En önemli cümle:

> **Veriyi önce anla, sonra ölç, sonra görselleştir, ardından müşteri özellikleri çıkar, benzer müşterileri grupla ve sonunda bu gruplara business anlamı ver.**

Bu mantığı kavrarsan DS_2'deki exercise'ler birbirinden kopuk görevler gibi görünmez; hepsi aynı data-analysis hikâyesinin parçaları haline gelir.
