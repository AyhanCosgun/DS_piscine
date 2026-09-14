# 42 Data Science Piscine - DS_2 Tutorial
## Data Visualization + Customer Clustering

> Bu rehber `ds_2.pdf` içeriği temel alınarak hazırlanmıştır. Amaç, projeyi daha önce data science yapmamış birinin bile adım adım anlayabileceği şekilde açıklamaktır.
>
> **Ana öneri:** PostgreSQL'i veri kaynağı / Data Warehouse ve veri hazırlama için, DBeaver'i SQL arayüzü ve kontrol için, Python + Jupyter Notebook'u ise analiz, grafik ve clustering için kullan.

---

# 0. DS_2'nin büyük resmi

DS_2 iki ana konu üzerine kurulu:

1. **Data Visualization** - veriyi grafiklerle anlatmak.
2. **Customer Clustering** - müşterileri davranışlarına göre gruplamak.

PDF'de data analyst'in geçmiş ve güncel veriyi anlaması, grafikleri ekiplerle paylaşması ve karar vermeye yardımcı araçlar üretmesi anlatılıyor. Ayrıca R, Excel, Power BI ve Jupyter Notebook gibi araçlar örnekleniyor ve dili seçmenin serbest olduğu belirtiliyor. Ex00'da Module 01 Data Warehouse'a bağlanman isteniyor. PDF ayrıca sonraki grafiklerin Şubat verisi dahil edilerek yeniden yapılması gerektiğini söylüyor.

Genel akış:

```text
Oct 2022 CSV
Nov 2022 CSV
Dec 2022 CSV
Jan 2023 CSV
Feb 2023 CSV
      |
      v
PostgreSQL Data Warehouse
      |
      |-- customers / events
      |-- items / product catalog
      |
      v
SQL ile hazırlama
      |
      v
Python + Pandas
      |
      +--> ex00: Pie chart
      +--> ex01: Zaman serisi grafikleri
      +--> ex02: İstatistik + box plot
      +--> ex03: Customer frequency / monetary dağılımları
      +--> ex04: Elbow Method
      +--> ex05: Clustering + en az 2 grafik
```

En önemli zihinsel model:

> **Önce veriyi anla -> ölç -> görselleştir -> müşteri özellikleri çıkar -> benzer müşterileri grupla -> gruplara iş anlamı ver.**

---

# 1. Hangi dili kullanmalıyım?

## Net öneri: Python

Bu proje için en rahat ve öğretici seçim:

- Python
- Jupyter Notebook
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Scikit-learn
- PostgreSQL
- DBeaver

Buradaki amaç PostgreSQL'i bırakmak değil. Tam tersine, **PostgreSQL + Python** birlikte kullanmak.

## Neden Python?

DS_2'de sadece SQL sorgulamıyorsun. Şunları da yapıyorsun:

- istatistik hesaplama,
- grafik çizme,
- DataFrame ile çalışma,
- feature engineering,
- clustering,
- model çıktısını görselleştirme.

Python bunların hepsini aynı ekosistemde yapabiliyor.

---

# 2. PostgreSQL / DBeaver ile yapılamaz mı?

## Yapılabilir, ama tamamını yalnızca SQL ile yapmak iyi seçim değil.

### PostgreSQL

Veritabanıdır. Örnek:

```sql
SELECT
    user_id,
    COUNT(*) AS purchase_count,
    SUM(price) AS total_spent
FROM customers
WHERE event_type = 'purchase'
GROUP BY user_id;
```

Bu tarz veri hazırlama ve aggregation işlerinde PostgreSQL çok güçlüdür.

### DBeaver

DBeaver PostgreSQL'in kendisi değildir. PostgreSQL'e bağlandığın masaüstü arayüzüdür.

Kabaca:

```text
PostgreSQL = database sistemi
DBeaver    = database'e bağlandığın GUI / SQL çalışma aracı
```

### Python

Python özellikle:

- analiz,
- grafik,
- istatistik,
- machine learning,
- clustering

için daha uygundur.

## Benim önerdiğim görev paylaşımı

```text
PostgreSQL
  -> saklama
  -> JOIN
  -> WHERE
  -> GROUP BY
  -> SUM / COUNT / MIN / MAX
  -> tarih bazlı SQL aggregation

Python / Pandas
  -> DataFrame analizi
  -> istatistik
  -> feature engineering
  -> visualization
  -> clustering

DBeaver
  -> SQL çalıştırma
  -> tabloyu kontrol etme
  -> kolonları inceleme

Jupyter
  -> bütün analizi adım adım yazma ve göstermek
```

Bu nedenle **SQL yerine Python** veya **Python yerine PostgreSQL** seçmek zorunda değilsin. İkisini bir pipeline içinde kullanmak en iyi yaklaşım.

---

# 3. "Language" ile "Tool" farkı nedir?

PDF'deki:

> "They often use tools such as techno R, Excel, Power BI, Jupyter Notebook..."

ve:

> "You are free to use any language of your choice for this module."

ifadeleri ilk bakışta karışabilir.

## Language = programlama dili

Örneğin:

- Python
- R
- JavaScript

## Tool = çalışmayı yaptığın araç / ortam / uygulama

Örneğin:

- Jupyter Notebook
- Excel
- Power BI
- DBeaver
- VS Code
- RStudio

Ama bu araçların hepsi aynı kategoride değildir.

Örnek stack:

```text
Python              = programlama dili
Jupyter Notebook    = analiz / notebook ortamı
Pandas              = Python kütüphanesi
Matplotlib          = grafik kütüphanesi
Seaborn             = grafik kütüphanesi
Scikit-learn        = machine learning kütüphanesi
PostgreSQL          = database
DBeaver             = database GUI
```

Dolayısıyla "önce dili seç, sonra mutlaka başka bir tool seç" gibi kesin bir kural yok. Daha doğru düşünce:

> **İşe uygun bir teknoloji yığını seçiyorum.**

DS_2 için:

```text
Language:      Python
Notebook:      Jupyter
Database:      PostgreSQL
DB GUI:        DBeaver
Data analysis: Pandas / NumPy
Visualization: Matplotlib / Seaborn
Clustering:    Scikit-learn
```

---

# 4. Jupyter Notebook neden iyi bir seçim?

Data Science'ta kod, açıklama ve grafik aynı yerde tutulabilir.

Örneğin:

```python
df.head()
```

ardından Markdown hücresinde:

> Purchase event'lerini seçiyoruz.

Sonra:

```python
purchase_df = df[df["event_type"] == "purchase"]
```

ve hemen ardından grafik.

Bu yapı peer evaluation sırasında ne yaptığını açıklamayı da kolaylaştırır.

---

# 5. Gerekli Python paketleri

```bash
pip install pandas numpy matplotlib seaborn scikit-learn sqlalchemy psycopg2-binary jupyter
```

İstersen virtual environment:

```bash
python -m venv .venv
```

Linux/macOS:

```bash
source .venv/bin/activate
```

Sonra paketler.

Jupyter:

```bash
jupyter notebook
```

veya:

```bash
jupyter lab
```

---

# 6. Python'dan PostgreSQL'e bağlanma

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

print(df.head())
```

Akış:

```text
PostgreSQL
    |
    | SQL query
    v
Pandas DataFrame
```

---

# 7. Veri temizliğinde temel kontroller

İlk kontrol:

```python
df.info()
df.head()
df.isna().sum()
df.dtypes
```

Tarih:

```python
df["event_time"] = pd.to_datetime(df["event_time"])
```

Price:

```python
df["price"] = pd.to_numeric(df["price"], errors="coerce")
```

Bütün projenin doğru gitmesi için veri tipleri önemli.

---

# 8. February verisi neden kritik?

PDF, verilen örnek grafiklerin February datası olmadan hazırlandığını ve **hepsinin yeni data ile tekrar yapılması gerektiğini** söylüyor.

Önceki çalışmanda Oct-Nov-Dec-Jan birleştirdiysen DS_2'de February'nin pipeline'a dahil olduğundan emin ol.

Kontrol:

```python
df["event_time"].dt.to_period("M").value_counts().sort_index()
```

Şunları görmeyi bekle:

```text
2022-10
2022-11
2022-12
2023-01
2023-02
```

---

# EXERCISE 00
# American Apple Pie

PDF'nin istediği:

- kendi pie chart'ını yapmak,
- insanların sitede ne yaptığını anlamak,
- Module 01 Data Warehouse'a bağlanmak.

Örnek event türleri:

```text
view
cart
remove_from_cart
purchase
```

## Amaç

İlk aşamada "veriye genel bakış" kazanmak.

Örneğin:

```text
view             46.7%
cart             27.9%
remove_from_cart 19.2%
purchase          6.2%
```

gibi bir dağılım görürsen şu business sorusu doğar:

> Siteyi kullanan kişilerin ne kadarı satın alma aşamasına geçiyor?

Bu, veri analizinin temel yaklaşımıdır.

---

# 9. Pie chart nedir?

Pie chart kategorilerin toplam içindeki oranlarını gösterir.

Formül:

```text
percentage = category_count / total_count * 100
```

Örneğin:

```text
purchase = 6200
total    = 100000
```

ise:

```text
6.2%
```

---

# 10. Ex00 nasıl yapılır?

SQL:

```sql
SELECT
    event_type,
    COUNT(*) AS event_count
FROM customers
GROUP BY event_type
ORDER BY event_count DESC;
```

Python:

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

---

# EXERCISE 01
# Initial Data Exploration

PDF'nin istediği:

1. `event_type == "purchase"` kayıtlarını tutmak.
2. October 2022 başından February 2023 sonuna kadar 3 grafik yapmak.

PDF örnekleri:

1. Number of customers
2. Total sales
3. Average spend/customers

---

# 11. "Keep only purchase" ne demek?

Dataset'te farklı event türleri olabilir:

```text
view
cart
remove_from_cart
purchase
```

Bu exercise satın alma davranışını incelemek istediği için:

```python
purchase_df = df[df["event_type"] == "purchase"].copy()
```

---

# 12. Grafik 1 - Number of Customers

PDF'deki örneğin amacı:

> Zaman boyunca satın alma yapan benzersiz müşteri sayısını görmek.

Mantık:

```text
x = zaman
 y = unique customers
```

Örneğin günlük:

```text
Oct 10 -> 1020 customers
Oct 11 -> 760 customers
Oct 12 -> 1050 customers
```

Burada dikkat:

**purchase event sayısı ile unique customer sayısı aynı değildir.**

Örneğin:

```text
user_10 purchase item_A
user_10 purchase item_B
user_10 purchase item_C
```

3 purchase event vardır ama unique customer sayısı 1'dir.

Bu nedenle customer sayısı için çoğu durumda:

```python
nunique()
```

kullanırsın.

Örneğin:

```python
daily_customers = (
    purchase_df
    .groupby(purchase_df["event_time"].dt.date)["user_id"]
    .nunique()
)
```

---

# 13. Grafik 2 - Total Sales

PDF örneğinde y ekseni yaklaşık olarak:

```text
total sales in million of A
```

x ekseni:

```text
month
```

`A` burada **Altairian Dollars**'ı ifade ediyor.

Hesap:

```text
monthly total sales = o aydaki purchase price toplamı
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

Python:

```python
monthly_sales = (
    purchase_df
    .set_index("event_time")
    .resample("MS")["price"]
    .sum()
)
```

Milyon cinsinden göstermek:

```python
monthly_sales / 1_000_000
```

---

# 14. Grafik 3 - Average Spend per Customer

PDF'deki amaç:

> Müşteri başına ortalama harcamayı zaman içinde göstermek.

Örneğin:

```text
Oct = 32 A
Nov = 35 A
Dec = 31 A
Jan = 33 A
Feb = ...
```

Temel formül:

```text
total sales / unique purchasing customers
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

Python örneği:

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

---

# 15. Ex01 grafiklerini nasıl okumalıyım?

PDF'deki örneklerde:

### Grafik 1

```text
x = time
 y = number of customers
```

### Grafik 2

```text
x = month
 y = total sales
```

### Grafik 3

```text
x = time
 y = average spend/customer
```

Yani her grafikte önce:

> **X ekseni neyi temsil ediyor?**

sonra:

> **Y ekseni neyi ölçüyor?**

diye bak.

---

# EXERCISE 02
# My Beautiful Mustache

PDF'nin istediği:

- mean
- median
- min
- max
- first quartile
- second quartile
- third quartile
- purchased item price box plot
- average basket price per user box plot

Bu exercise temel istatistik ve box plot mantığını öğretir.

---

# 16. Mean

Mean = aritmetik ortalama.

```text
2, 4, 6
```

ortalama:

```text
(2 + 4 + 6) / 3 = 4
```

Python:

```python
price.mean()
```

---

# 17. Median

Median = sıralanmış verinin ortasındaki değer.

```text
1, 3, 5
```

median = 3.

Çift sayıda:

```text
1, 3, 5, 7
```

ortadaki 3 ve 5'in ortalaması alınır:

```text
4
```

Python:

```python
price.median()
```

---

# 18. Min / Max

```text
min = en küçük değer
max = en büyük değer
```

---

# 19. Quartile nedir?

Quartile veriyi dört bölüme ayırır.

```text
0%          25%          50%          75%         100%
|------------|------------|------------|-------------|
             Q1           Q2           Q3
```

- Q1 = 25. percentile
- Q2 = 50. percentile = median
- Q3 = 75. percentile

PDF örneğinde yaklaşık:

```text
Q1 = 1.59
Q2 = 3.33
Q3 = 6.03
```

---

# 20. Box plot nedir?

Box plot bir dağılımın merkezini, yayılımını ve outlier'larını özetler.

Yatay örnek:

```text
             box
        [-------------]
        Q1    |       Q3
              |
            median
```

Kutunun:

```text
sol tarafı  = Q1
ortadaki çizgi = median / Q2
sağ tarafı = Q3
```

Kutunun genişliği:

```text
IQR = Q3 - Q1
```

Whisker'lar kutunun dış tarafındaki normal aralığı gösterir. Whisker dışındaki tekil noktalar çoğunlukla outlier olarak çizilir.

---

# 21. IQR nedir?

```text
IQR = Q3 - Q1
```

Örneğin:

```text
Q1 = 2
Q3 = 6
```

ise:

```text
IQR = 4
```

IQR ortadaki %50'lik bölümün yayılımını anlatır.

---

# 22. Outlier nedir?

Klasik box-plot kuralında:

```text
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR
```

bu sınırların dışında kalan gözlemler outlier olarak gösterilebilir.

PDF'deki ilk box plot'ta merkezde küçük bir box ve çok uzakta noktalar görmenin nedeni büyük olasılıkla fiyat dağılımındaki sıra dışı değerlerdir.

---

# 23. Negative price neden var?

PDF'nin örnek çıktısında:

```text
min = -79.370000
```

görülüyor.

Bu çok önemli bir inceleme noktasıdır.

Şunu yap:

```python
purchase_df[purchase_df["price"] < 0]
```

ve negatif fiyatların gerçek kayıtlarda ne anlama geldiğine bak.

PDF bu negatif değerlerin nedenini açıklamıyor. Dolayısıyla sırf grafik güzel görünsün diye bunları otomatik silmek doğru olmaz. Önce veri anlamını araştır.

---

# 24. İlk box plot - purchased item prices

Pipeline:

```text
purchase events
      |
      v
price
      |
      v
box plot
```

Örnek:

```python
plt.figure(figsize=(8, 4))
sns.boxplot(x=purchase_df["price"])
plt.xlabel("price")
plt.title("Purchased Item Prices")
plt.show()
```

PDF'deki görüntünün merkezde çok sıkışık görünmesi normal olabilir. Çünkü birkaç büyük fiyat x eksenini çok genişletirse, ortadaki box görsel olarak daralır.

---

# 25. İkinci box plot - Average Basket Price per User

Burada artık item price dağılımına değil, **müşteri bazında oluşan basket metriğine** bakıyorsun.

Örneğin:

```text
user_1 -> 28.5
user_2 -> 33.1
user_3 -> 31.8
user_4 -> 42.0
```

gibi customer-level değerleri çıkarıp bunların box plot'unu yaparsın.

Önemli ayrım:

```text
item price != average basket price
```

Basket hesabının tam biçimi dataset'teki kolonlara göre belirlenmelidir. Eğer basket/order ID gibi alan varsa onu kullanmak daha doğru olabilir.

---

# 26. Ex02 için istatistik kodu

```python
prices = purchase_df["price"]

print("count :", prices.count())
print("mean  :", prices.mean())
print("median:", prices.median())
print("min   :", prices.min())
print("Q1    :", prices.quantile(0.25))
print("Q2    :", prices.quantile(0.50))
print("Q3    :", prices.quantile(0.75))
print("max   :", prices.max())
```

---

# EXERCISE 03
# Highest Building

PDF iki grafik istiyor:

1. orders according to frequency
2. Altairian Dollars spent on the site by customers

PDF örneğindeki eksenlerde:

```text
frequency
monetary value in A
```

ve y ekseninde:

```text
customers
```

yer alıyor.

---

# 27. Frequency nedir?

Frequency:

> bir müşterinin kaç kez satın alma / order yaptığı.

Örneğin:

```text
A -> 1
B -> 2
C -> 8
D -> 2
```

Sonra:

```text
frequency = 1 olan kaç müşteri?
frequency = 2 olan kaç müşteri?
frequency = 3 olan kaç müşteri?
...
```

diye dağılıma bakarsın.

---

# 28. Histogram nedir?

Histogram sayısal verileri aralıklara bölerek her aralıkta kaç gözlem olduğunu gösterir.

Örneğin:

```text
0-10   -> 65000 customers
10-20  -> 15000 customers
20-30  -> 5000 customers
30-40  -> 1000 customers
```

Bu grafik:

> müşteri kitlesinin büyük kısmının düşük frequency'de toplandığını

gösterebilir.

---

# 29. Monetary value nedir?

Müşterinin toplam harcadığı para.

```python
monetary = (
    purchase_df
    .groupby("user_id")["price"]
    .sum()
)
```

Örneğin:

```text
A -> 42 A
B -> 100 A
C -> 180 A
```

---

# 30. Ex03 neden Ex05'e hazırlık yapıyor?

Çünkü iki temel davranış özelliğini öğreniyorsun:

```text
Frequency = ne kadar sık?
Monetary  = ne kadar harcıyor?
```

Bunlar daha sonra customer segmentation için feature olarak kullanılabilir.

---

# EXERCISE 04
# Elbow

PDF şunu istiyor:

- Elbow Method ile "optimal" cluster sayısını anlamak,
- seçtiğin cluster sayısını açıklayabilmek.

---

# 31. Cluster nedir?

Cluster:

> benzer özelliklere sahip gözlemlerden oluşan grup.

Örneğin müşteriler:

```text
A -> çok alışveriş + yüksek harcama
B -> az alışveriş + düşük harcama
C -> sık alışveriş + orta harcama
D -> uzun süredir alışveriş yapmıyor
```

ise bunları benzer davranışlara göre gruplamak isteyebilirsin.

---

# 32. Clustering'in amacı nedir?

Çünkü çoğu zaman veride doğrudan:

```text
customer_type
```

etiketi bulunmaz.

Ama:

```text
recency
frequency
monetary
```

gibi davranış bilgileri vardır.

Clustering:

> önceden etiketlenmemiş müşterileri benzerliklerine göre gruplamaya çalışır.

Bu yüzden clustering **unsupervised learning** alanındadır.

---

# 33. Unsupervised learning nedir?

Supervised learning'de:

```text
X = input
Y = doğru etiket
```

vardır.

Örneğin:

```text
features -> churned / not churned
```

Clustering'de ise başlangıçta:

```text
X var
etiket yok
```

vardır.

Algoritma grupları keşfetmeye çalışır.

---

# 34. Cluster sayısını neden seçiyoruz?

K-Means gibi bazı algoritmalara:

```python
n_clusters=4
```

şeklinde K vermek gerekir.

Ama neden 4?

Neden 3 değil?

Neden 6 değil?

Bunu araştırmak için Elbow Method kullanılabilir.

---

# 35. Elbow Method nedir?

Farklı K değerleri denersin:

```text
K = 1, 2, 3, ..., 10
```

Her K için clustering kalitesini temsil eden bir metrik izlersin. K-Means'te yaygın metrik **inertia**dır.

---

# 36. Inertia nedir?

Sezgisel olarak:

> Cluster içindeki noktaların centroid'lerine olan kareli uzaklıklarının toplamı.

Noktalar kendi centroid'lerine yaklaştıkça:

```text
inertia ↓
```

olur.

K arttıkça inertia genellikle düşer. Çünkü daha fazla cluster kullanmak noktaları daha küçük gruplara ayırır.

Ama:

```text
K = çok büyük
```

seçmek business açısından anlamsız olabilir.

---

# 37. Neden "Elbow"?

Örnek şekil:

```text
Inertia
  |
  |\
  | \
  |  \
  |   \
  |    \__
  |       \___
  +-------------------> K
```

Küçük K'larda inertia çok hızlı düşebilir. Bir noktadan sonra düşüş yavaşlar.

Bu kırılma noktası "dirsek" gibi görünür.

Örneğin:

```text
K=1 -> 270000
K=2 -> 160000
K=3 -> 105000
K=4 ->  85000
K=5 ->  73000
K=6 ->  65000
K=7 ->  59000
```

Burada 1->2, 2->3 ve 3->4 kazanımları daha büyükken sonrasında iyileşme azalabilir. Bu yüzden 3-4 civarı incelenebilir.

**Elbow tek başına sihirli bir sayı üretmez.** Business yorumlanabilirliği de gerekir. PDF'nin "kaç cluster seçtiğini ve nedenini açıklayabilmelisin" demesinin nedeni budur.

---

# 38. Elbow Method kodu

Önce feature'ları seç:

```python
features = df[[
    "recency",
    "frequency",
    "monetary"
]]
```

Scale et:

```python
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
X = scaler.fit_transform(features)
```

K'ları dene:

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
plt.plot(range(1, 11), inertias, marker="o")
plt.xlabel("Number of clusters")
plt.ylabel("Inertia")
plt.title("The Elbow Method")
plt.show()
```

---

# EXERCISE 05
# Clustering

PDF'nin istediği:

- en az 4 grup,
- clustering algorithm kullanmak,
- grupların en az 2 grafik temsilini yapmak.

PDF'de örnek segment fikirleri:

```text
new customer
inactive customer
loyal customers
gold / silver / platinum
```

---

# 39. "At least 4 groups" ne demek?

En az 4 customer segment oluşturmalısın.

Örnek:

```text
1 - New
2 - Inactive
3 - Regular
4 - Loyal
```

veya daha ayrıntılı:

```text
New
Inactive
Silver
Gold
Platinum
```

Burada kritik ayrım:

```text
Cluster 0
Cluster 1
Cluster 2
Cluster 3
```

etiketleri otomatik olarak:

```text
gold
silver
platinum
inactive
```

değildir.

Algoritma sadece grupları verir. **İş anlamını sen, cluster istatistiklerini inceleyerek verirsin.**

---

# 40. K-Means nedir?

K-Means'in sezgisel algoritması:

1. K tane başlangıç centroid'i seç.
2. Her müşteriyi en yakın centroid'e ata.
3. Her cluster için yeni centroid hesapla.
4. Yeniden atama yap.
5. Değişim çok azalıncaya kadar devam et.

---

# 41. Centroid nedir?

Centroid:

> bir cluster'ın merkezini temsil eden nokta.

Örneğin:

```text
(2, 10)
(4, 20)
(6, 30)
```

üç noktasının centroid'i:

```text
x = (2+4+6)/3 = 4
y = (10+20+30)/3 = 20
```

yani:

```text
(4, 20)
```

Centroid müşteri değildir. Cluster'ı temsil eden merkez noktadır.

---

# 42. K-Means neden "means"?

Çünkü centroid her feature için cluster içindeki **ortalama (mean)** değerlerle güncellenir.

---

# 43. Clustering algoritmaları hangileri?

"Kaç tane clustering algoritması var?" sorusunun sabit bir cevabı yoktur. Çok sayıda yöntem ve varyasyon vardır.

DS_2 açısından bilmen gereken önemli örnekler:

## K-Means

- sayısal feature'lar,
- hızlı segmentation,
- kompakt kümeler

için iyi bir başlangıçtır.

Eksileri:

- K verilmesi gerekir,
- ölçeklemeden etkilenir,
- outlier'lardan etkilenebilir,
- cluster şekilleri konusunda varsayımları vardır.

**DS_2 için ilk tercih: K-Means.**

## Hierarchical / Agglomerative Clustering

Noktaları küçük gruplardan başlayarak birleştirerek hiyerarşi oluşturur.

Genellikle dendrogram ile görselleştirilir.

## DBSCAN

Yoğunluk tabanlı bir yöntemdir.

Özellikle:

- noise / outlier tespiti,
- dairesel olmayan şekilli cluster'lar

için kullanılabilir.

## Gaussian Mixture Model

Veriyi birden fazla olasılık dağılımının karışımı olarak modellemeye çalışır. K-Means'in kesin atamasına göre olasılıksal üyelik mantığı sağlar.

Başka örnekler de vardır:

- Spectral Clustering
- Mean Shift
- OPTICS
- BIRCH

Bunların hepsini projede uygulamak gerekmiyor.

---

# 44. Neden K-Means ile başlamak iyi?

Customer segmentation için elinde sayısal feature'lar varsa:

```text
recency
frequency
monetary
```

K-Means basit, hızlı ve açıklanabilirdir. Elbow Method ile K'yı araştırabilirsin.

Peer defense sırasında anlatması da kolaydır.

---

# 45. RFM nedir?

Customer segmentation'da çok kullanılan bir feature setidir:

```text
R = Recency
F = Frequency
M = Monetary
```

---

# 46. Recency nedir?

Müşterinin son satın alımının referans tarihine ne kadar uzak olduğunu söyler.

Örneğin referans:

```text
2023-03-01
```

Son satın alma:

```text
2023-02-28
```

ise:

```text
recency = 1 day
```

Son satın alma çok eskiyse recency büyür.

Çok önemli:

```text
recency düşük  = daha yeni / daha aktif
recency yüksek = daha uzun süredir gelmiyor
```

---

# 47. Frequency nedir?

Müşterinin kaç satın alma yaptığı.

```text
A -> 25
B -> 3
C -> 1
```

25 daha yüksek frequency'dir.

---

# 48. Monetary nedir?

Müşterinin toplam harcaması.

```text
A -> 900 A
B -> 120 A
C -> 10 A
```

---

# 49. Neden RFM mantıklı?

Çünkü üç soruyu aynı anda cevaplar:

```text
Recency   -> ne kadar yakın zamanda geldi?
Frequency -> ne kadar sık geliyor?
Monetary  -> ne kadar para harcıyor?
```

Bu müşteri davranışını tek bir sayıya göre bakmaktan daha iyi temsil eder.

---

# 50. RFM tablosu oluşturma

Örnek:

```python
reference_date = purchase_df["event_time"].max() + pd.Timedelta(days=1)

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

Sonuç:

```text
user_id | recency | frequency | monetary
-----------------------------------------
1       | 2       | 12        | 350
2       | 40      | 1         | 8
3       | 5       | 30        | 1000
```

---

# 51. Neden scaling gerekiyor?

Diyelim:

```text
recency   = 10
frequency = 20
monetary  = 500
```

K-Means distance hesaplar.

Euclidean distance kabaca:

```text
sqrt((x1-y1)^2 + (x2-y2)^2 + (x3-y3)^2)
```

Monetary 500 civarındayken recency 10 civarındaysa monetary mesafeyi çok daha fazla etkileyebilir.

Bu durumda clustering beklenmedik şekilde para harcamasına aşırı ağırlık verebilir.

---

# 52. StandardScaler nedir?

Feature'ları karşılaştırılabilir bir ölçeğe getirir.

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

Her feature yaklaşık olarak:

```text
mean ~ 0
std  ~ 1
```

ölçeğine taşınır.

---

# 53. K-Means uygulaması

Örneğin Elbow incelemesinden sonra K=4 seçildi diyelim:

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
1       | 2       | 12        | 350      | 2
2       | 40      | 1         | 8        | 0
3       | 5       | 30        | 1000     | 3
```

gibi bir tablo vardır.

---

# 54. Cluster 0, 1, 2, 3 ne demek?

Bunlar sadece algoritmanın verdiği ID'lerdir.

Örneğin:

```text
cluster 0 = inactive
cluster 1 = new
cluster 2 = regular
cluster 3 = loyal
```

olabilir.

Ama bu isimleri **sen cluster statistics'e bakıp savunmalısın.**

---

# 55. Cluster profiling

Şunu yap:

```python
profile = (
    rfm
    .groupby("cluster")[["recency", "frequency", "monetary"]]
    .mean()
)

print(profile)
```

Örneğin:

```text
cluster   recency   frequency   monetary
0            90         1          10
1             2        20         500
2            10         5          80
3             5        10         250
```

Bunun olası iş yorumu:

```text
0 -> inactive
1 -> loyal / very high value
2 -> lower-frequency regular
3 -> strong regular
```

Bu isimler örnektir. Gerçek isimlendirme çıkan verilere göre yapılmalı.

---

# 56. Cluster count grafiği

PDF'nin ilk Ex05 grafik örneğinde yatay bar chart benzeri bir grafik var.

Y ekseni:

```text
Loyal customers
New customers
inactive
```

X ekseni:

```text
number of customers
```

Yani grafik:

> her segmentte kaç müşteri olduğunu gösteriyor.

Örneğin PDF'de yaklaşık:

```text
Loyal customers -> 39586
New customers   -> 38253
inactive        -> 12133
```

gibi değerler gösteriliyor.

---

# 57. Bu grafik neden önemli?

Clustering sadece matematik değildir. Sonuçların business karşılığı olmalıdır.

Örneğin:

```text
inactive -> reactivation coupon
new      -> welcome offer
loyal    -> VIP / premium reward
```

Bu nedenle:

> **cluster -> yorum -> aksiyon**

zinciri önemlidir.

---

# 58. Ex05 scatter plot - yatay ve dikey eksenler

PDF'deki ikinci temel grafik bir scatter plot'tur.

Mantık:

```text
X axis = Recency
Y axis = Frequency
```

Her nokta bir müşteridir.

Örneğin bir nokta:

```text
x = 20
y = 50
```

ise:

```text
recency = 20
frequency = 50
```

olan bir müşteriyi temsil eder.

---

# 59. Scatter plot nedir?

Her gözlem bir nokta ile gösterilir.

Örneğin:

```text
Frequency
100 |             .
 80 |       .  .     .
 60 |   .       . .
 40 | .   . .
 20 | . .    .
  0 +----------------------
     0   20   40   60  Recency
```

Bu grafik iki sayısal değişkenin dağılımını görmemizi sağlar.

---

# 60. Neden farklı renkler var?

Her renk farklı bir cluster anlamına gelir.

Örneğin:

```text
kırmızı  = cluster 0
mavi     = cluster 1
yeşil    = cluster 2
mor      = cluster 3
```

Renklerin kendisinin özel matematiksel anlamı yoktur. Renk sadece grupları birbirinden ayırmak için kullanılır.

---

# 61. Büyük sarı noktalar ne?

PDF'deki büyük sarı noktalar **centroid**'lerdir.

Küçük noktalar:

```text
customers
```

Büyük merkez noktalar:

```text
centroids
```

---

# 62. Centroid'i sezgisel olarak nasıl düşünmelisin?

Bir cluster'da:

```text
(20,50)
(22,48)
(25,52)
(28,55)
```

müşterileri olsun.

Centroid yaklaşık:

```text
x = 23.75
y = 51.25
```

olur.

Bu merkez cluster'ın tipik noktasını temsil eder.

---

# 63. K-Means müşteriyi nasıl atıyor?

En basit bakışla:

> Müşteri hangi centroid'e daha yakınsa o cluster'a atanır.

Örneğin iki centroid:

```text
C1 ----------------- C2
```

olsun.

Bir müşteri C1'e daha yakınsa:

```text
cluster 1
```

olur.

Bu işlem iteratif biçimde tekrar tekrar yapılır.

---

# 64. "Median Recency" ve "Median Frequency" ne demek?

PDF'deki üst grafiklerden birinde yaklaşık:

```text
X = Median Recency (month)
Y = Median Frequency
```

kullanılmış.

Buradaki median ortalama değildir.

Örneğin bir cluster'ın recency değerleri:

```text
1, 2, 2, 3, 10
```

ise median = 2'dir.

Dolayısıyla:

```text
Median Recency
```

= o cluster'daki müşterilerin recency değerlerinin medyanı.

Benzer şekilde:

```text
Median Frequency
```

= o cluster'daki frequency değerlerinin medyanı.

---

# 65. "Average 'Loyal customers': ?? A" ne demek?

PDF'de bazı değerler:

```text
??
```

olarak bırakılmış.

Bunlar **placeholder**'dır.

Örneğin:

```text
Average "Loyal customers": ?? A
```

şu anlama gelir:

> loyal olarak adlandırdığın gruptaki ilgili parasal metriğin ortalamasını sen hesapla.

Burada `??` gerçek veri değildir ve literal olarak yazdırılmak zorunda değildir.

---

# 66. "A" ne?

PDF'de fiyatların Altairian Dollars olduğu söyleniyor.

Bu nedenle:

```text
25 A
```

= 25 Altairian Dollars.

---

# 67. Ex05'te neden minimum 2 grafik?

PDF minimum 2 graphic representation istiyor.

İyi bir kombinasyon:

## Grafik 1

```text
segment / cluster
        vs
number of customers
```

## Grafik 2

```text
Recency
   vs
Frequency
```

ve clusterları renklerle göster.

Centroid'leri de büyük marker ile göster.

---

# 68. Ex05 scatter plot için örnek

Örneğin:

```python
plt.figure(figsize=(10, 7))

sns.scatterplot(
    data=rfm,
    x="recency",
    y="frequency",
    hue="cluster"
)

plt.xlabel("Recency")
plt.ylabel("Frequency")
plt.title("Customer Clusters")
plt.show()
```

Centroid gösterirken önemli bir ayrıntı var: K-Means scaled data üzerinde çalışıyorsa centroid'ler de scaled uzayda bulunur. Grafiğin gerçek recency/frequency eksenlerinde olmasını istiyorsan centroid'i doğru koordinat sistemine geri taşımak gerekir.

Özellikle üç feature ile clustering yaptıysan:

```text
recency
frequency
monetary
```

ve yalnızca:

```text
recency vs frequency
```

grafiği çiziyorsan, görselleştirmede kullandığın iki feature için centroid değerlerini doğru şekilde elde et.

---

# 69. 3D grafik zorunlu mu?

Hayır.

RFM üç feature olduğu için 3D scatter plot yapmak mümkündür:

```text
Recency
Frequency
Monetary
```

Ama başlangıç için 2D grafikler daha okunabilir ve peer defense'te açıklaması daha kolaydır.

---

# 70. Customer-level table neden gerekiyor?

Event-level tabloda bir müşteri için çok sayıda satır vardır:

```text
2023-01-01 | A | product_1 | 10
2023-01-05 | A | product_2 | 20
2023-01-10 | A | product_3 | 15
```

Clustering'e doğrudan bunu verirsen algoritma müşteri değil event'leri gruplar.

Oysa amacımız:

> **bir satır = bir müşteri**

olmalı.

Örneğin:

```text
user_id | recency | frequency | monetary
-----------------------------------------
A       | 2       | 14        | 400
B       | 45      | 1         | 9
C       | 5       | 25        | 1000
```

---

# 71. SQL ile customer-level aggregation

```sql
WITH purchases AS (
    SELECT *
    FROM customers
    WHERE event_type = 'purchase'
)
SELECT
    user_id,
    COUNT(*) AS frequency,
    SUM(price) AS monetary,
    MAX(event_time) AS last_purchase
FROM purchases
GROUP BY user_id;
```

Sonrasında Python'da recency hesaplanabilir.

---

# 72. Recency için referans tarih

Örneğin:

```python
reference_date = purchase_df["event_time"].max() + pd.Timedelta(days=1)
```

Böylece en son tarihte satın alan müşteri için:

```text
recency = 1
```

olur.

Sabit bir project end date de seçebilirsin. Önemli olan bütün müşterilere aynı referans tarihini uygulamak.

---

# 73. New customer nasıl yorumlanır?

`frequency = 1` tek başına "new customer" demek değildir.

Daha doğru düşünce:

- ilk purchase çok yeni,
- frequency düşük,
- recency düşük

olan biri new customer olmaya daha yakındır.

Cluster etiketini bu özelliklerle birlikte yorumlamak gerekir.

---

# 74. Inactive nasıl yorumlanabilir?

Örnek:

```text
recency yüksek
frequency düşük
monetary düşük
```

olan grup inactive olabilir.

Yine de önce cluster statistics'i incele.

---

# 75. Gold / Silver / Platinum nasıl atanır?

Örneğin:

```text
low recency
high frequency
high monetary
```

olan bir grup yüksek değerli / loyal olabilir.

Daha zayıf ama düzenli bir cluster:

```text
medium recency
medium frequency
medium monetary
```

ise Gold/Silver benzeri bir iş etiketi alabilir.

Ama isimlendirme cluster sonuçlarına göre yapılmalıdır. Algoritmanın cluster numarası kendi başına loyalty seviyesi değildir.

---

# 76. Cluster profiling tablosu oluştur

```python
profile = (
    rfm.groupby("cluster")
       .agg(
           customers=("user_id", "count"),
           median_recency=("recency", "median"),
           median_frequency=("frequency", "median"),
           median_monetary=("monetary", "median"),
           mean_recency=("recency", "mean"),
           mean_frequency=("frequency", "mean"),
           mean_monetary=("monetary", "mean")
       )
)

print(profile)
```

Bu tablo şunu cevaplamana yardım eder:

> "Bu cluster neden loyal?"

---

# 77. Neden median bazen mean'den daha iyi?

Customer spending dağılımında outlier olabilir.

```text
10
12
15
20
21
22
5000
```

Mean çok büyür. Median ortadaki tipik değeri daha iyi temsil eder.

Bu yüzden customer segmentation'da mean ve median'ı beraber incelemek faydalıdır.

---

# 78. Ex02 -> Ex03 -> Ex04 -> Ex05 bağlantısı

Exercises birbirinden bağımsız düşünülmemeli.

```text
Ex02
istatistik + dağılım
   |
   v
Ex03
customer behavior
   |
   v
Ex04
cluster sayısı
   |
   v
Ex05
müşteri segmentation
```

Yani DS_2'nin tamamı bir veri analiz hikayesi gibi okunabilir.

---

# 79. Önerilen proje klasörü

```text
ds_2/
|
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

PDF teslim adlarını şu şekilde veriyor:

```text
pie.*
chart.*
mustache.*
Building.*
elbow.*
Clustering.*
```

Bu yüzden submission öncesi **dosya adlarının ve klasörlerin tam olarak beklenen isimde olduğundan emin ol.**

---

# 80. SQL mi Pandas mı?

## SQL kullan

- WHERE
- JOIN
- GROUP BY
- COUNT
- SUM
- MIN / MAX
- DATE_TRUNC
- DISTINCT

## Pandas kullan

- DataFrame işlemleri
- hızlı keşif
- grafik öncesi hazırlık
- feature engineering
- clustering için input matrix hazırlama

Bu ayrım performans ve okunabilirlik açısından da faydalıdır.

---

# 81. Baştan sona profesyonel workflow

## Aşama 1 - Database

PostgreSQL'deki temel veriyi doğrula:

```sql
SELECT COUNT(*) FROM customers;
```

## Aşama 2 - February kontrolü

```python
df["event_time"].min()
df["event_time"].max()
```

ve aylara bak.

## Aşama 3 - Ex00

```text
event_type
   |
   v
counts
   |
   v
pie chart
```

## Aşama 4 - Ex01

```text
purchase only
   |
   +--> customer counts
   +--> monthly sales
   +--> average spend/customer
```

## Aşama 5 - Ex02

```text
purchase prices
   |
   +--> mean / median / quartiles
   +--> box plot
   |
   +--> customer basket metric
   +--> second box plot
```

## Aşama 6 - Ex03

```text
customer-level
   |
   +--> frequency distribution
   +--> monetary distribution
```

## Aşama 7 - Ex04

```text
RFM
 |
 v
scaling
 |
 v
K=1..10
 |
 v
inertia
 |
 v
elbow
```

## Aşama 8 - Ex05

```text
RFM
 |
 v
KMeans
 |
 v
cluster labels
 |
 v
profile
 |
 +--> segment count chart
 +--> scatter plot
 |
 v
business interpretation
```

---

# 82. En sık yapılan hatalar

## Hata 1 - Tüm event'leri purchase sanmak

Doğrusu:

```python
purchase_df = df[df["event_type"] == "purchase"]
```

## Hata 2 - customer count ile event count'u karıştırmak

Customer sayısı gerektiğinde çoğu zaman:

```python
nunique()
```

gerekir.

## Hata 3 - recency'yi ters anlamak

```text
recency düşük  = yakın zamanda alışveriş
recency yüksek = uzun süredir alışveriş yok
```

## Hata 4 - frequency / monetary'yi karıştırmak

```text
frequency = kaç kez
monetary  = ne kadar para
```

## Hata 5 - scaling yapmadan K-Means çalıştırmak

Özellikle feature'lar çok farklı ölçeklerdeyse sonuç etkilenebilir.

## Hata 6 - Cluster ID'lerini sıraya koymak

```text
cluster 0 < cluster 1 < cluster 2
```
şeklinde doğal bir kalite sırası yoktur.

## Hata 7 - Elbow'u sadece göz kararıyla seçmek

K seçerken:

- elbow şekli,
- cluster stability / yorumlanabilirliği,
- business amacı

beraber düşünülmeli.

## Hata 8 - Centroid'i müşteri zannetmek

Centroid = cluster merkezi.

## Hata 9 - Outlier'ları otomatik silmek

Özellikle Ex02'deki negatif ve uç price değerlerini önce incele.

---

# 83. Peer defense için hazır açıklamalar

## Ex00

> Event type distribution'ı görmek için pie chart kullandım. Her dilim toplam event sayısının içindeki oranı gösteriyor.

## Ex01

> Sadece purchase event'lerini filtreledim ve October 2022 ile February 2023 arasındaki customer count, total sales ve average spend değişimini görselleştirdim.

## Ex02

> Price distribution'ı mean, median ve quartile'larla özetledim. Box plot ile dağılımı ve outlier'ları gösterdim.

## Ex03

> Customer purchase frequency ve monetary value dağılımını inceleyerek customer behavior'ı analiz ettim.

## Ex04

> Farklı K değerleri için K-Means inertia'sını hesapladım ve Elbow Method ile uygun cluster sayısını araştırdım.

## Ex05

> Customer-level RFM features oluşturdum, standardize ettim, K-Means uyguladım ve cluster'ları hem customer count grafiği hem de 2D scatter plot ile görselleştirdim.

---

# 84. "Neden K-Means?" sorusuna cevap

> Elimde sayısal customer-level features var ve müşterileri davranışlarına göre segmentlere ayırmak istiyorum. K-Means bu tür sayısal feature'lar için basit ve yorumlanabilir bir başlangıç yöntemi. Ayrıca Elbow Method ile cluster sayısını araştırabiliyorum.

---

# 85. "Neden StandardScaler?" sorusuna cevap

> Recency, frequency ve monetary farklı ölçeklerde. Monetary'nin büyük sayıları distance hesabında baskın hale gelmesin diye feature'ları benzer ölçeğe getiriyorum.

---

# 86. "Centroid nedir?" sorusuna cevap

> Centroid, cluster'daki noktaların feature bazındaki ortalamasını temsil eden merkez noktadır. K-Means gözlemleri en yakın centroid'e atar ve centroid'leri tekrar hesaplayarak algoritmayı iteratif şekilde günceller.

---

# 87. "Elbow neden kullandın?" sorusuna cevap

> Farklı K değerleri için inertia hesapladım. K büyüdükçe inertia düşüyor, fakat bir noktadan sonra iyileşme azalıyor. Bu kırılma noktasını ve business olarak yorumlanabilirliği dikkate alarak K seçtim.

---

# 88. Clustering gerçek hayatta ne için kullanılır?

Örnek segmentler:

```text
Cluster 1
çok sık + çok harcıyor

Cluster 2
az sık + az harcıyor

Cluster 3
önceden aktif ama artık değil

Cluster 4
yeni müşteri
```

Sonra marketing aksiyonları:

```text
1 -> premium offer
2 -> standard offer
3 -> win-back campaign
4 -> welcome campaign
```

Yani clustering'in asıl amacı sadece grafik üretmek değil; **karar vermeye yardımcı müşteri segmentleri oluşturmak**.

---

# 89. Mini sözlük

| Kavram | Anlamı |
|---|---|
| Data Warehouse | Analiz için organize edilmiş merkezi veri deposu |
| PostgreSQL | İlişkisel database sistemi |
| DBeaver | Database GUI / SQL çalışma aracı |
| Python | Programlama dili |
| Pandas | DataFrame / tablo analizi |
| Jupyter | Notebook çalışma ortamı |
| Matplotlib | Grafik kütüphanesi |
| Seaborn | İstatistiksel görselleştirme kütüphanesi |
| Scikit-learn | Machine learning kütüphanesi |
| Mean | Aritmetik ortalama |
| Median | Ortanca değer |
| Q1 | 25. percentile |
| Q2 | 50. percentile / median |
| Q3 | 75. percentile |
| IQR | Q3 - Q1 |
| Outlier | Olağandışı uzak gözlem |
| Histogram | Sayısal veriyi aralıklara bölerek yoğunluğu gösteren grafik |
| Scatter plot | İki sayısal değişkenin nokta grafiği |
| Cluster | Benzer gözlemler grubu |
| Centroid | Cluster merkezi |
| K-Means | Centroid tabanlı clustering algoritması |
| Inertia | K-Means için cluster içi kareli uzaklık toplamı |
| Elbow | Inertia eğrisindeki kırılma / dirsek noktası |
| Recency | Son alışverişten beri geçen süre |
| Frequency | Alışveriş sıklığı |
| Monetary | Toplam harcama |
| RFM | Recency + Frequency + Monetary |

---

# 90. Sana önerdiğim öğrenme sırası

Bu sırayla ilerlemek en rahat yol:

```text
1. Pandas DataFrame
2. groupby
3. count / nunique / sum / mean
4. datetime
5. Matplotlib
6. Seaborn
7. mean / median / quartile
8. box plot
9. histogram
10. scatter plot
11. Euclidean distance
12. clustering mantığı
13. centroid
14. K-Means
15. StandardScaler
16. Elbow Method
17. RFM
18. customer segmentation
```

---

# 91. Net teknoloji önerim

## Dil

**Python**

## Çalışma ortamı

**Jupyter Notebook**

## Database

**PostgreSQL**

## Database GUI

**DBeaver**

## Data analysis

**Pandas + NumPy**

## Visualization

**Matplotlib + Seaborn**

## Clustering

**Scikit-learn**

## İlk clustering algorithm

**K-Means**

## Feature set

İlk deneme:

```text
Recency
Frequency
Monetary
```

Sonra:

```text
StandardScaler
```

Sonra:

```text
Elbow Method
```

ve ardından:

```text
KMeans
```

En sonunda:

```text
cluster profile
+
2 grafik
+
business interpretation
```

---

# 92. Submission checklist

## Genel

- [ ] PostgreSQL bağlantısı çalışıyor.
- [ ] February datası dahil.
- [ ] Tarih ve price veri tipleri doğru.
- [ ] Purchase filtresi doğru.
- [ ] Null / hatalı veriler kontrol edildi.

## Ex00

- [ ] Data Warehouse'a bağlandım.
- [ ] Event distribution hesaplandı.
- [ ] Pie chart var.

## Ex01

- [ ] Yalnızca purchase data kullanıldı.
- [ ] October 2022 - February 2023 kapsanıyor.
- [ ] 3 grafik var.
- [ ] Grafiklerin x/y eksenleri açık.

## Ex02

- [ ] Mean
- [ ] Median
- [ ] Min
- [ ] Max
- [ ] Q1
- [ ] Q2
- [ ] Q3
- [ ] Item-price box plot
- [ ] Average basket price/user box plot

## Ex03

- [ ] Frequency dağılımı
- [ ] Monetary dağılımı
- [ ] Grafik etiketleri anlaşılır

## Ex04

- [ ] K değerleri denendi
- [ ] Inertia hesaplandı
- [ ] Elbow plot var
- [ ] K seçiminin gerekçesi yazıldı

## Ex05

- [ ] En az 4 grup
- [ ] Clustering algorithm kullanıldı
- [ ] Cluster profiling yapıldı
- [ ] Minimum 2 grafik
- [ ] Centroid açıklanabiliyor
- [ ] X/Y eksenleri açıklanabiliyor
- [ ] `??` placeholder'larının ne olduğu anlaşılmış
- [ ] Cluster isimleri istatistiklere göre yorumlandı

---

# 93. Sonuç

PDF herhangi bir programlama dilini seçmene izin veriyor. PostgreSQL / DBeaver kullanman da projeyle uyumlu; özellikle ex00 zaten Module 01 Data Warehouse bağlantısı istiyor. Ancak grafik, istatistik ve clustering aşamalarını tamamen SQL içinde zorlamak yerine aşağıdaki ayrımı kullanmak en temiz yöntemdir:

```text
PostgreSQL -> veri saklama + SQL hazırlama
DBeaver    -> database inspection + SQL
Python     -> analiz + visualization + clustering
Jupyter    -> çalışmayı belgelemek
```

DS_2'yi şu zincir olarak gör:

```text
RAW DATA
   |
   v
POSTGRESQL
   |
   v
SQL
   |
   v
PANDAS
   |
   +------> VISUALIZATION
   |
   v
CUSTOMER FEATURES
   |
   v
STANDARDIZATION
   |
   v
ELBOW
   |
   v
K-MEANS
   |
   v
CLUSTERS
   |
   v
BUSINESS SEGMENTS
```

Bu mantığı kavrarsan exercise'leri yalnızca örnek grafikleri taklit ederek değil, **neden o grafikleri ve neden o clustering adımlarını yaptığını anlayarak** çözebilirsin.
