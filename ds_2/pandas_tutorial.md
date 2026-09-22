# SQL Bilenler İçin Pandas Rehberi: `groupby`, `agg` ve Kümeleme Metrikleri (`pandas_tutorial.md`)

Bu rehber, SQL bilgisi sağlam olup Pandas sözdizimine (syntax) yeni alışanlar için hazırlanmıştır. SQL'deki `GROUP BY`, `AGGREGATE FUNCTIONS` (`SUM`, `AVG`, `COUNT`), `ALIAS` (`AS`) ve `WINDOW FUNCTIONS` (`SUM() OVER ()`) mantıklarının Pandas'taki birebir karşılıklarını adım adım, örnek tablolarla ve denenebilir Python kodlarıyla anlatır.

---

## İçindekiler
1. [Büyük Resim: SQL ve Pandas Zihniyeti Karşılaştırması](#1-büyük-resim-sql-ve-pandas-zihniyeti-karşılaştırması)
2. [Örnek Veri Setimiz (Toy Dataset)](#2-örnek-veri-setimiz-toy-dataset)
3. [Adım 1: Yeni Kolon Atama (`df["cluster"] = ...`)](#3-adım-1-yeni-kolon-atama-dfcluster--)
4. [Adım 2: `groupby("cluster")` Mantığı (Split-Apply-Combine)](#4-adım-2-groupbycluster-mantığı-split-apply-combine)
5. [Adım 3: `.agg()` ve Modern "Named Aggregation" (İsimli Toplama)](#5-adım-3-agg-ve-modern-named-aggregation-isimli-toplama)
6. [Adım 4: SQL Window Function Mantığı ve Yüzde Hesapları](#6-adım-4-sql-window-function-mantığı-ve-yüzde-hesapları)
7. [Adım 5: `revenue_index` Nedir? (İş Zekası / Benchmark Metriği)](#7-adım-5-revenue_index-nedir-iş-zekası--benchmark-metriği)
8. [Clustering.py Kodunun Birebir SQL Karşılığı](#8-clusteringpy-kodunun-birebir-sql-karşılığı)
9. [Kopyala-Çalıştır Bağımsız Test Kodu](#9-kopyala-çalıştır-bağımsız-test-kodu)

---

## 1. Büyük Resim: SQL ve Pandas Zihniyeti Karşılaştırması

SQL'de her şey tek bir `SELECT ... FROM ... GROUP BY` deklaratif ifadesi içinde yazılırken, Pandas'ta işlemler adım adım zincirlenir veya ayrı satırlarda DataFrame üzerine uygulanır.

| İşlem | SQL Karşılığı | Pandas Karşılığı |
|---|---|---|
| Tablo / Sonuç Kümesi | `TABLE` / `VIEW` | `pd.DataFrame` |
| Kolon Seçme | `SELECT user_id, price` | `df[["user_id", "price"]]` |
| Gruplama | `GROUP BY cluster` | `df.groupby("cluster")` |
| İsimlendirerek Toplama | `SUM(price) AS revenue` | `.agg(revenue=("price", "sum"))` |
| Satır Sayısı | `COUNT(*)` | `("user_id", "size")` |
| Null Olmayan Sayısı | `COUNT(kolon)` | `("kolon", "count")` |
| Ortalama | `AVG(kolon)` | `("kolon", "mean")` |
| Medyan (Ortanca) | `PERCENTILE_CONT(0.5)...` | `("kolon", "median")` |
| Toplam Tablo Toplamı | `SUM(revenue) OVER ()` | `df["revenue"].sum()` |
| Yeni Kolon Türetme | `SELECT c.*, col_a / col_b AS ratio` | `df["ratio"] = df["col_a"] / df["col_b"]` |

---

## 2. Örnek Veri Setimiz (Toy Dataset)

Konuyu soyut formüller yerine 10 kişilik somut bir e-ticaret müşteri tablosuyla görelim.

Varsayalım ki `df_rfm` tablomuz şu verileri içeriyor:
* `user_id`: Müşteri ID'si
* `recency`: Müşterinin son alışverişinden bu yana geçen gün sayısı (Düşük = Yeni alışveriş yapmış)
* `frequency`: Müşterinin toplam sipariş sayısı (Yüksek = Sadık müşteri)
* `monetary`: Müşterinin harcadığı toplam tutar (A cinsinden)
* `cluster`: Makine öğrenimi algoritmasının (K-Means) atadığı küme numarası (0, 1, 2)

```text
┌─────────┬─────────┬───────────┬──────────┬─────────┐
│ user_id │ recency │ frequency │ monetary │ cluster │
├─────────┼─────────┼───────────┼──────────┼─────────┤
│    1001 │       5 │        12 │   450.00 │       0 │
│    1002 │      12 │         8 │   320.00 │       0 │
│    1003 │       8 │        15 │   600.00 │       0 │
│    1004 │      85 │         2 │    45.00 │       1 │
│    1005 │     120 │         1 │    20.00 │       1 │
│    1006 │      90 │         1 │    30.00 │       1 │
│    1007 │      95 │         3 │    70.00 │       1 │
│    1008 │       3 │        35 │  2100.00 │       2 │
│    1009 │       1 │        42 │  2800.00 │       2 │
│    1010 │       4 │        28 │  1800.00 │       2 │
└─────────┴─────────┴───────────┴──────────┴─────────┘
```

Bu tabloda sezgisel olarak 3 grup var:
- **Cluster 0:** Yakın zamanda gelmiş, orta düzey harcayan müşteriler.
- **Cluster 1:** Uzun süredir gelmeyen (terk etmeye yakın), az harcamış müşteriler.
- **Cluster 2:** Sık sık gelen ve çok yüksek harcayan VIP müşteriler.

---

## 3. Adım 1: Yeni Kolon Atama (`df["cluster"] = ...`)

```python
df_rfm["cluster"] = kmeans.fit_predict(X_scaled)
```

### Ne Yapar?
1. `kmeans.fit_predict(X_scaled)` fonksiyonu arka planda 10 satırlık verinin her bir satırı için bir küme etiketi üretir: `[0, 0, 0, 1, 1, 1, 1, 2, 2, 2]`.
2. `df_rfm["cluster"] = ...` ifadesi, SQL'deki `ALTER TABLE df_rfm ADD COLUMN cluster INT; UPDATE ...` veya `SELECT *, <küme_tahmini> AS cluster` mantığıyla DataFrame'in sağ tarafına `"cluster"` adında yeni bir sütun ekler.

---

## 4. Adım 2: `groupby("cluster")` Mantığı (Split-Apply-Combine)

```python
df_rfm.groupby("cluster")
```

### Ne Yapar?
SQL'de `GROUP BY cluster` yazdığınızda PostgreSQL motoru ne yapıyorsa, Pandas da aynısını yapar:

1. **Split (Bölme):** Tabloyu `cluster` sütunundaki değerlere göre (0, 1, 2) sanal olarak 3 ayrı alt tabloya böler:
   - **Grup 0 Alt Tablosu:** 3 satır (1001, 1002, 1003)
   - **Grup 1 Alt Tablosu:** 4 satır (1004, 1005, 1006, 1007)
   - **Grup 2 Alt Tablosu:** 3 satır (1008, 1009, 1010)
2. **Apply (Uygulama):** Bir sonraki adımda vereceğimiz fonksiyonlar (`sum`, `mean`, `median`, vb.) bu 3 gruba ayrı ayrı bağımsız olarak uygulanır.
3. **Combine (Birleştirme):** Hesaplanan sonuçlar tekrar birleştirilerek tek bir özet tablo (summary dataframe) oluşturulur.

> [!NOTE]
> Tek başına `df.groupby("cluster")` yazıp ekrana basarsanız bir tablo göremezsiniz; sadece bir `DataFrameGroupBy` nesnesi döner. Çünkü Pandas ona hangi kolonları nasıl toplayacağını söylemenizi bekler!

---

## 5. Adım 3: `.agg()` ve Modern "Named Aggregation" (İsimli Toplama)

İşte Clustering.py'deki en can alıcı blok:

```python
cluster_check = df_rfm.groupby("cluster").agg(
    customers=("user_id", "size"),
    recency_median=("recency", "median"),
    frequency_median=("frequency", "median"),
    monetary_median=("monetary", "median"),
    revenue=("monetary", "sum"),
    revenue_per_customer=("monetary", "mean"),
    median_revenue=("monetary", "median"),
)
```

### Bu Sözdizimi (Syntax) Neden Böyle Yazılır?

Pandas 0.25 (2019) sürümünden önce agg fonksiyonu sözlükler (`{"monetary": ["sum", "mean"]}`) ile yazılıyordu ve ortaya karmaşık çok katmanlı (MultiIndex) çirkin kolon isimleri çıkıyordu.

Modern Pandas'ta SQL'deki `SELECT AGG(kolon) AS yeni_isim` rahatlığını sağlamak için **Named Aggregation** sözdizimi getirilmiştir:

$$\mathbf{yeni\_kolon\_adi = ("kaynak\_kolon", "fonksiyon\_adi")}$$

Parçalarına ayıralım:
```python
customers=("user_id", "size")
```
- **`customers`:** Sonuç tablosunda görünecek yeni kolonun adı ($AS\ customers$).
- **`"user_id"`:** Hangi kolona bakılacağı.
- **`"size"`:** Hangi fonksiyonun çalıştırılacağı ($COUNT(*)$).

### Satır Satır SQL Çevirisi:

```sql
SELECT 
    cluster,
    COUNT(*)                             AS customers,
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY recency)   AS recency_median,
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY frequency) AS frequency_median,
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY monetary)  AS monetary_median,
    SUM(monetary)                        AS revenue,
    AVG(monetary)                        AS revenue_per_customer,
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY monetary)  AS median_revenue
FROM df_rfm
GROUP BY cluster;
```

### Kritik İki Detay:
1. **`size` vs `count` Farkı Nedir?**
   - `"size"`: O gruptaki toplam satır adedini sayar (SQL'deki `COUNT(*)` karşılığıdır; NULL değerleri de satır olarak sayar).
   - `"count"`: O kolondaki **NULL olmayan** değerleri sayar (SQL'deki `COUNT(user_id)` karşılığıdır).
   - Satır sayısı arandığında `"size"` kullanmak standarttır.
2. **Neden hem `revenue_per_customer` (`mean`) hem de `median_revenue` (`median`) alınmış?**
   - Önceki egzersizden (Ex02 Boxplot) hatırlayın: Eğer grupta 1-2 kişi aşırı zenginse ortalama (`mean`) şişer. Medyan ise grubun tipik ortalama müşterisini gösterir. İkisini yan yana görmek grubun homojenliğini anlamamızı sağlar.

---

## 6. Adım 4: SQL Window Function Mantığı ve Yüzde Hesapları

Grup özet tablomuz oluştuktan sonra gelen 3 satır:

```python
cluster_check["customer_share_pct"] = (
    100 * cluster_check["customers"] / cluster_check["customers"].sum()
)
cluster_check["revenue_share_pct"] = (
    100 * cluster_check["revenue"] / cluster_check["revenue"].sum()
)
```

### Matematiksel ve SQL Mantığı:

`cluster_check` artık 3 satırlık bir özet tablodur:
```text
cluster | customers | revenue
--------+-----------+--------
0       |         3 | 1370.00
1       |         4 |  165.00
2       |         3 | 6700.00
```

1. **`cluster_check["customers"]`**:
   Her satırın kendi müşteri adedini verir: `[3, 4, 3]`.
2. **`cluster_check["customers"].sum()`**:
   Bu sütunun tüm satırlarının toplamını tek bir sayı olarak döner: $3 + 4 + 3 = 10$.
3. **Bölme İşlemi (`/`):**
   Pandas vektörel bölme yapar: Her satırın müşteri sayısını toplam müşteri sayısına (10) böler:
   - Grup 0: $3 / 10 = 0.30 \times 100 = \%30$
   - Grup 1: $4 / 10 = 0.40 \times 100 = \%40$
   - Grup 2: $3 / 10 = 0.30 \times 100 = \%30$

### SQL Karşılığı (Window Function):
SQL'de bir satırın değerini tüm tablonun toplamına oranlamak için `OVER()` pencere fonksiyonu kullanılır:
```sql
100.0 * customers / SUM(customers) OVER () AS customer_share_pct,
100.0 * revenue   / SUM(revenue)   OVER () AS revenue_share_pct
```

---

## 7. Adım 5: `revenue_index` Nedir? (İş Zekası / Benchmark Metriği)

```python
cluster_check["revenue_index"] = (
    cluster_check["revenue_per_customer"] / df_rfm["monetary"].mean()
)
```

### Buradaki İnce Ayrım:
- Pay kısmında ne var? `cluster_check["revenue_per_customer"]` $\rightarrow$ **O kümenin** müşteri başı harcama ortalaması.
- Payda kısmında ne var? `df_rfm["monetary"].mean()` $\rightarrow$ **TÜM ŞİRKETİN (Tüm müşterilerin)** müşteri başı genel harcama ortalaması.

### Ne İşe Yarar? (Benchmark Endeksi)
Bu formül şu sorunun yanıtıdır:  
> *"Bu kümedeki bir müşteri, sitemizin ortalama bir müşterisine kıyasla kaç kat değerli?"*

- **Endeks = 1.0 ise:** Bu küme tam şirket ortalamasında harcıyor demektir.
- **Endeks = 0.2 ise:** Bu kümedeki müşteriler şirket ortalamasının beşte biri kadar harcıyor (Düşük değerli / Pasif kitle).
- **Endeks = 3.5 ise:** Bu kümedeki bir müşteri şirket ortalamasından **3.5 kat daha fazla** para bırakıyor! (VIP / Altın kitle).

### SQL Karşılığı:
```sql
revenue_per_customer / (SELECT AVG(monetary) FROM df_rfm) AS revenue_index
```

---

## 8. Clustering.py Kodunun Birebir SQL Karşılığı

İşte sormuş olduğunuz kod bloğunun tamamının tek bir SQL sorgusu olarak tam karşılığı:

```sql
WITH cluster_summary AS (
    SELECT 
        cluster,
        COUNT(*)                                                AS customers,
        PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY recency)    AS recency_median,
        PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY frequency)  AS frequency_median,
        PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY monetary)   AS monetary_median,
        SUM(monetary)                                           AS revenue,
        AVG(monetary)                                           AS revenue_per_customer,
        PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY monetary)  AS median_revenue
    FROM df_rfm
    GROUP BY cluster
)
SELECT 
    *,
    -- Müşteri payı yüzdesi:
    100.0 * customers / SUM(customers) OVER ()                  AS customer_share_pct,
    -- Ciro payı yüzdesi:
    100.0 * revenue   / SUM(revenue)   OVER ()                  AS revenue_share_pct,
    -- Gelir endeksi (Genel şirket ortalamasına oran):
    revenue_per_customer / (SELECT AVG(monetary) FROM df_rfm)   AS revenue_index
FROM cluster_summary
ORDER BY cluster;
```

---

## 9. Kopyala-Çalıştır Bağımsız Test Kodu

Bu kodları kendi terminalinizde hiçbir veritabanına ihtiyaç duymadan doğrudan deneyebilir, her satırın çıktısını anında görebilirsiniz:

```python
import pandas as pd

# 1. Örnek Tablomuzu Oluşturalım
data = {
    "user_id":   [1001, 1002, 1003, 1004, 1005, 1006, 1007, 1008, 1009, 1010],
    "recency":   [   5,   12,    8,   85,  120,   90,   95,    3,    1,    4],
    "frequency": [  12,    8,   15,    2,    1,    1,    3,   35,   42,   28],
    "monetary":  [ 450,  320,  600,   45,   20,   30,   70, 2100, 2800, 1800],
    "cluster":   [   0,    0,    0,    1,    1,    1,    1,    2,    2,    2]
}
df_rfm = pd.DataFrame(data)

print("=== HAM VERİ SETİ (İlk 5 Satır) ===")
print(df_rfm.head())
print("\n" + "="*70 + "\n")

# 2. GROUPBY ve AGG (Named Aggregation)
cluster_check = df_rfm.groupby("cluster").agg(
    customers=("user_id", "size"),
    recency_median=("recency", "median"),
    frequency_median=("frequency", "median"),
    monetary_median=("monetary", "median"),
    revenue=("monetary", "sum"),
    revenue_per_customer=("monetary", "mean"),
    median_revenue=("monetary", "median"),
)

# 3. YÜZDELER VE ENDEKS HESABI (Window Function Mantığı)
cluster_check["customer_share_pct"] = (
    100 * cluster_check["customers"] / cluster_check["customers"].sum()
)
cluster_check["revenue_share_pct"] = (
    100 * cluster_check["revenue"] / cluster_check["revenue"].sum()
)
cluster_check["revenue_index"] = (
    cluster_check["revenue_per_customer"] / df_rfm["monetary"].mean()
)

print("=== KÜMELEME ÖZET TABLOSU (cluster_check) ===")
print(cluster_check.round(2).to_string())
print("\n" + "="*70 + "\n")

# 4. İŞ ZEKASI YORUMU
print("=== METRİK OKUMA VE İŞ YORUMU ===")
for c_id, row in cluster_check.iterrows():
    print(f"Cluster {c_id}:")
    print(f"  - Müşterilerin %{row['customer_share_pct']:.1f}'ini oluşturuyor.")
    print(f"  - Toplam cironun %{row['revenue_share_pct']:.1f}'ini getiriyor.")
    print(f"  - Değer Endeksi: {row['revenue_index']:.2f}x (Ortalamanın {row['revenue_index']:.2f} katı harcıyor)\n")
```

### Bu Scripti Çalıştırdığınızda Alacağınız Çıktı:

```text
=== KÜMELEME ÖZET TABLOSU (cluster_check) ===
         customers  recency_median  frequency_median  monetary_median  revenue  revenue_per_customer  median_revenue  customer_share_pct  revenue_share_pct  revenue_index
cluster                                                                                                                                                                
0                3            8.00             12.00           450.00  1370.00                456.67          450.00                30.0              16.64           0.55
1                4           92.50              1.50            37.50   165.00                 41.25           37.50                40.0               2.00           0.05
2                3            3.00             35.00          2100.00 6700.00               2233.33         2100.00                30.0              81.36           2.71
```

Bu tabloyu okuduğunuz an e-ticaretin altın kuralı olan Pareto Prensibini (80/20 kuralı) görürsünüz:
- **Cluster 2:** Müşterilerin sadece **%30'u** olmasına rağmen, tüm cironun **%81.36'sını** tek başına üretmektedir! (`revenue_index = 2.71x`).
- **Cluster 1:** Müşterilerin **%40'ı** olmasına rağmen, cironun sadece **%2'sini** getirmektedir (`revenue_index = 0.05x`).

