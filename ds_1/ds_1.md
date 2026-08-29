# DS_1: Data Warehouse (ETL) — Kapsamlı Rehber ve Soru-Cevap

Bu belge, **Data Science Piscine - Modül 1 (Data Warehouse)** sürecindeki mimari kararları, SQL yöntemlerini, veri mühendisliği pratiklerini ve sık sorulan soruların detaylı yanıtlarını içerir.

---

## Soru 1
> **ex00 `ds_0`'daki "Show me your DB" ile aynı herhalde, başka bir şey yapmaya gerek yok, doğru mu?**

### Cevap:
**Evet, mantık ve amaç olarak tamamen aynıdır.**

- **Subject İsteri:** Veritabanındaki tabloları ve verileri kolayca görselleştirebileceğiniz, özellikle bir ID üzerinden hızlı arama yapabileceğiniz bir GUI aracı (DBeaver, pgAdmin, Postico vb.) kullanmak.
- **Değerlendirme (Evaluation) Süreci:** Değerlendiren kişi sizden GUI aracınızı (DBeaver) açmanızı, veritabanına bağlanmanızı ve tabloları/satırları göstermenizi isteyecektir.
- **Teslimat (Turn-in):** Subject'te turn-in dosyası belirtilmemiştir (`Files to turn in: ` boştur). Tıpkı `ds_0/ex01`'de yaptığımız gibi, `ds_1/ex00/` dizini altına DBeaver bağlantı ayarlarını ve kullanımını anlatan kısa bir `README.md` koymak standart ve düzenli bir yaklaşımdır.

---

## Soru 2
> **ex01'de bu birleştirme işlemini nasıl yapmalıyım? JOIN, UNION vb. birleştirme yöntemleri duymuştum, bunların farkları ne, burada en uygunu hangisi? Bir de hangi kolon üzerinden birleştirme yapmamız bekleniyor acaba?**

### Cevap:

### 1. JOIN vs. UNION Farkı
Veritabanı dünyasında iki temel birleştirme yaklaşımı vardır:

```
          JOIN (Yatay / Kolon Bazlı)                   UNION (Dikey / Satır Bazlı)
   Tablo A           Tablo B      Sonuç           Tablo A       Tablo B       Sonuç
┌────┬────┐       ┌────┬────┐  ┌────┬────┬────┐ ┌────┬────┐  ┌────┬────┐  ┌────┬────┐
│ id │ c1 │   +   │ id │ c2 │= │ id │ c1 │ c2 │ │ c1 │ c2 │+ │ c1 │ c2 │= │ c1 │ c2 │
├────┼────┤       ├────┼────┤  ├────┼────┼────┤ ├────┼────┤  ├────┼────┤  ├────┼────┤
│ 1  │ A  │       │ 1  │ X  │  │ 1  │ A  │ X  │ │ A  │ 10 │  │ C  │ 30 │  │ A  │ 10 │
└────┴────┘       └────┴────┘  └────┴────┴────┘ │ B  │ 20 │  │ D  │ 40 │  │ B  │ 20 │
                                                └────┴────┘  └────┴────┘  │ C  │ 30 │
                                                                          │ D  │ 40 │
                                                                          └────┴────┘
```

- **`JOIN` (Yatay Birleştirme):** Farklı tablolardaki **farklı bilgileri**, ortak bir anahtar kolon (`product_id` gibi) üzerinden yan yana bağlar.
- **`UNION` / `UNION ALL` (Dikey Birleştirme):** **Aynı şemaya (aynı kolonlara) sahip** farklı tablolardaki satırları alt alta ekler.

### 2. Burada Hangisi En Uygundur?
Subject metninde İngilizce günlük dilde *"You have to join all the data_202*_*** tables together"* ifadesi geçse de, teknik olarak **aylık müşteri tabloları (`data_2022_oct`, `data_2022_nov`, `data_2022_dec`, `data_2023_jan`) tamamen aynı kolon yapısına sahiptir**:
`(event_time, event_type, product_id, price, user_id, user_session)`

Farklı aylara ait satırları tek bir büyük `customers` tablosunda toplamak istediğimiz için burada **doğru yöntem dikey birleştirme yani `UNION` / `UNION ALL`'dur.**

### 3. Hangi Kolon Üzerinden Birleştirilir?
`UNION` işleminde belirli bir "eşleşme kolonu" (ON koşulu) kullanılmaz. Kolonların sırası ve veri tipleri birebir eşleştiği için tüm satırlar doğrudan alt alta eklenir.

**Örnek SQL Yaklaşımı:**
```sql
CREATE TABLE customers AS
SELECT * FROM data_2022_oct
UNION ALL
SELECT * FROM data_2022_nov
UNION ALL
SELECT * FROM data_2022_dec
UNION ALL
SELECT * FROM data_2023_jan;
```
> **Not:** `UNION` otomatik olarak mükerrer satırları ayıklamaya çalışır ancak 16+ milyon satırda çok yavaştır. ex02'de özel bir tekilleştirme yapacağımız için ex01'de doğrudan ve hızlı olan `UNION ALL` tercih edilir.

---

## Soru 3
> **ex02'de kastedilen duplicate'ler acaba tabloların (CSV dosyalarının) kendisinde mi var? Yoksa birleştirme işleminden sonra duplicate'ler mi oluşuyor? Bunları nasıl temizlerim? Bu arada "duplicate" tam olarak ne anlama gelecek burada, "event_time'ı çok yakın ama diğer kısımları tamamen aynı olan satırlar" anlamına mı gelecek yani?**

### Cevap:

### 1. Duplicate'ler Nereden Geliyor?
Duplicate'ler **ham CSV verilerinin bizzat kendi içinde** vardır. Gerçek hayattaki e-ticaret sitelerinde kullanıcılar bir butona art arda çift tıkladığında veya ağ kesintisi nedeniyle tarayıcı/mobil uygulama aynı olayı tekrar gönderdiğinde telemetri sistemine mükerrer kayıtlar düşer.

### 2. Bu Projede "Duplicate" Ne Anlama Geliyor?
Subject'te iki türlü duplicate kastedilmektedir:
1. **Tam Mükerrer Satırlar (Exact Duplicates):** Tüm kolonları (`event_time`, `event_type`, `product_id`, `price`, `user_id`, `user_session`) birbirinin tıpatıp aynısı olan satırlar.
2. **Zaman Aralıklı Mükerrer Satırlar (Near-Duplicates / $\le 1$ saniye):**  
   Subject'teki kritik uyarı:
   > *"Sometimes the server sends the same instruction with 1 second interval, so you must also remove them."*
   
   Örnek:
   ```
   2022-10-01 00:00:32, remove_from_cart, 5779403, ...
   2022-10-01 00:00:33, remove_from_cart, 5779403, ...
   ```
   Aynı kullanıcı (`user_id`, `user_session`), aynı ürünü (`product_id`), aynı eylemle (`event_type`), **1 saniye veya daha az aralıkla** tetiklemişse bu da duplicate kabul edilir ve silinmelidir.

### 3. Bunlar SQL ile Nasıl Temizlenir?
16+ milyon satır üzerinde satır satır `DELETE` çalıştırmak PostgreSQL'de saatler sürebilir. En temiz ve performanslı yöntem **Window Functions (`LAG` veya `ROW_NUMBER`)** kullanarak geçici temiz tablo oluşturmaktır (CTAS: Create Table As Select):

```sql
-- Örnek Mantık: LAG fonksiyonu ile bir önceki olayın zamanını kontrol etme
CREATE TABLE customers_clean AS
WITH marked_duplicates AS (
    SELECT *,
           LAG(event_time) OVER (
               PARTITION BY event_type, product_id, price, user_id, user_session
               ORDER BY event_time
           ) AS prev_event_time
    FROM customers
)
SELECT event_time, event_type, product_id, price, user_id, user_session
FROM marked_duplicates
WHERE prev_event_time IS NULL 
   OR EXTRACT(EPOCH FROM (event_time - prev_event_time)) > 1;

-- Eski tabloyu silip yenisini adlandırma
DROP TABLE customers;
ALTER TABLE customers_clean RENAME TO customers;
```

---

## Soru 4
> **ex03'te JOIN ile birleştirmemiz gerektiğini nereden anlıyoruz? Veri kaybetmeyi engellediği için mi? Burada veri kaybetmeyi engellemenin yolları nelerdir, nelere dikkat edilmeli?**

### Cevap:

### 1. Neden JOIN Kullanıyoruz?
- `customers` tablosu: Kullanıcı işlemlerini içerir (`product_id`, `event_time`, `user_id`, `price` vb.).
- `items` tablosu: Ürün katalog detaylarını içerir (`product_id`, `category_id`, `category_code`, `brand`).

İki tablonun **şemaları farklıdır** fakat aralarında ortak bir anahtar kolon (`product_id`) vardır. `customers` tablosuna ürünün kategori ve marka bilgilerini eklemek (zenginleştirmek) istediğimiz için bu işlem **Yatay Birleştirme (JOIN)** gerektirir.

### 2. "Be careful not to lose any information" — Veri Kaybını Engelleme

SQL'deki JOIN türleri ve veri kaybı riskleri:
- **`INNER JOIN` (Riskli!):** Eğer `customers` tablosunda geçen bir `product_id`, `items.csv` tablosunda tanımlı değilse, `INNER JOIN` o müşteri hareketini **tamamen tablodan siler!** Bu ciddi bir veri kaybıdır.
- **`LEFT JOIN` (Doğru Tercih):** `customers` tablosundaki her satırı kesinlikle korur. Eğer ürün katalogda yoksa, `category_id`, `category_code` ve `brand` alanlarına `NULL` basar ama müşteri hareketini kaybetmez.

```sql
-- Doğru Birleştirme Şablonu:
CREATE TABLE customers_fusion AS
SELECT 
    c.event_time,
    c.event_type,
    c.product_id,
    c.price,
    c.user_id,
    c.user_session,
    i.category_id,
    i.category_code,
    i.brand
FROM customers c
LEFT JOIN items i ON c.product_id = i.product_id;
```

### Nelere Dikkat Edilmeli?
1. **Bire-Çok (1-to-Many) Çoğalma Riski:** Eğer `items` tablosunda aynı `product_id` birden fazla satırda varsa, `LEFT JOIN` işlemi `customers` tablosundaki işlem satırlarını katlar (satır sayısı artar). Bu yüzden `items` tablosunda `product_id`'nin tekil (unique) olduğundan emin olunmalıdır.
2. **Kayıt Sayısı Kontrolü:** Birleştirme öncesindeki `customers` satır sayısı ile birleştirme sonrasındaki `customers` satır sayısı **birebir eşit** olmalıdır.

---

## Soru 5
> **Proje başlığı Data Warehouse kavramı ve ETL kavramı ile alakalı başka bilmem gereken şeyler var mı? Bunlar Data Science'ta bilinen kavramlar mı?**

### Cevap:
**Evet, bunlar modern Veri Bilimi (Data Science) ve Veri Mühendisliğinin (Data Engineering) temel yapı taşlarıdır.**

### 1. Data Warehouse (DWH - Veri Ambarı) Nedir?
- **OLTP (Operasyonel Veritabanları):** Uygulamaların anlık çalıştığı sistemlerdir (Örn: sipariş geçme, bakiye güncelleme). Hızlı tekil yazma ve okuma odaklıdır (Normalizasyon - 3NF).
- **OLAP / Data Warehouse (Analitik Veritabanları):** Raporlama, iş zekası (BI) ve makine öğrenmesi modelleri için tasarlanmış büyük veri depolarıdır. Tüm geçmiş veriyi tek bir yerde toplar, temizler ve analiz için hızlı okunabilir (denormalize) hale getirir.

Bu projede:
- `ds_0`'da ham tabloları yükleyerek bir **Staging Area (Geçici Hazırlık Alanı)** kurdunuz.
- `ds_1`'de tabloları birleştirip, tekilleştirip, zenginleştirerek analize hazır bir **Data Warehouse (`customers` tablosu)** oluşturdunuz.
- `ds_2`, `ds_3`, `ds_4` modüllerinde veri analistleri ve bilimcileri olarak doğrudan bu Data Warehouse üzerinden grafik ve model üreteceksiniz.

### 2. ETL (Extract - Transform - Load) Nedir?
Veri boru hatlarının (Data Pipelines) standart yaşam döngüsüdür:
1. **Extract (Çıkar):** Farklı kaynaklardan (CSV, API, PostgreSQL, Loglar) ham veriyi çekme $\rightarrow$ `ds_0`.
2. **Transform (Dönüştür/Temizle):** Veri tiplerini ayarlama, mükerrer kayıtları ayıklama, eksik verileri işleme, tabloları birleştirme $\rightarrow$ `ds_1`.
3. **Load (Yükle):** Temizlenmiş ve modellenmiş veriyi son kullanıcıların (veri bilimcilerinin) sorgulayabileceği nihai ambar tablolarına yazma $\rightarrow$ `ds_1/ex03`.

### 3. Veri Biliminde Neden Bu Kadar Önemli?
- **"Garbage In, Garbage Out":** Kirli, tekilleştirilmemiş veya eksik veriyle eğitilen makine öğrenmesi modelleri hatalı tahminler üretir.
- **Sektör Gerçeği:** Bir Veri Bilimcisinin vaktinin **%70-80'i** veri hazırlama, temizleme ve ETL adımlarında geçer. 42 Piscine'inin `ds_0` ve `ds_1` ile başlamasının sebebi size bu sağlam temeli kazandırmaktır.

---

## Soru 6 (Ek Soru 1)
> **Bu birleştirme türlerini biraz daha detaylandırıp örneklendirebilir misin? UNION, UNION ALL, başka UNION çeşitleri varsa, LEFT JOIN, RIGHT JOIN, JOIN, başka çeşitleri varsa, bunların görevlerini farklarını basit örnekler ile örnekleyerek açıkla.**

### Cevap:

SQL'de veri birleştirmeleri temel olarak **Dikey (Küme / Set İşlemleri)** ve **Yatay (Tablo İlişkilendirme / JOIN)** olmak üzere ikiye ayrılır.

---

### A) DİKEY BİRLEŞTİRMELER (Küme Operatörleri - Satır Bazlı)

İki tablonun **kolon sayıları ve veri tipleri aynı** olduğunda satırları alt alta eklemek için kullanılır.

#### Örnek Tablolarımız:
```
   [Tablo_A]              [Tablo_B]
┌────┬─────────┐       ┌────┬─────────┐
│ id │  isim   │       │ id │  isim   │
├────┼─────────┤       ├────┼─────────┤
│ 1  │ Elma    │       │ 2  │ Armut   │
│ 2  │ Armut   │       │ 3  │ Muz     │
└────┴─────────┘       └────┴─────────┘
```

#### 1. `UNION` (Dikey Birleştir + Mükerrerleri Ayıkla)
İki tablodaki satırları alt alta ekler ve aynı olan (duplicate) satırları eler (tekilleştirir).
```sql
SELECT * FROM Tablo_A
UNION
SELECT * FROM Tablo_B;
```
**Sonuç (3 Satır):**
```
┌────┬─────────┐
│ 1  │ Elma    │
│ 2  │ Armut   │  <-- 'Armut' her iki tabloda da vardı, tek satıra indi.
│ 3  │ Muz     │
└────┴─────────┘
```

#### 2. `UNION ALL` (Dikey Birleştir + Hepsini Koru - Hızlı)
İki tablodaki satırları hiç kontrol etmeden doğrudan alt alta ekler. Mükerrer satırları elemez, bu yüzden `UNION`'a göre **çok daha hızlıdır**.
```sql
SELECT * FROM Tablo_A
UNION ALL
SELECT * FROM Tablo_B;
```
**Sonuç (4 Satır):**
```
┌────┬─────────┐
│ 1  │ Elma    │
│ 2  │ Armut   │  <-- Tablo_A'dan
│ 2  │ Armut   │  <-- Tablo_B'den (Mükerrer satır korundu)
│ 3  │ Muz     │
└────┴─────────┘
```

#### 3. `INTERSECT` (Kesişim Kümesi)
Sadece her iki tabloda da **ortak olan** satırları getirir.
```sql
SELECT * FROM Tablo_A
INTERSECT
SELECT * FROM Tablo_B;
```
**Sonuç (1 Satır):**
```
┌────┬─────────┐
│ 2  │ Armut   │
└────┴─────────┘
```

#### 4. `EXCEPT` (veya `MINUS` - Fark Kümesi)
Birinci tabloda olup ikinci tabloda **olmayan** satırları getirir.
```sql
SELECT * FROM Tablo_A
EXCEPT
SELECT * FROM Tablo_B;
```
**Sonuç (1 Satır):**
```
┌────┬─────────┐
│ 1  │ Elma    │
└────┴─────────┘
```

---

### B) YATAY BİRLEŞTİRMELER (JOIN Operatörleri - Kolon Bazlı)

İki tablodaki bilgileri ortak bir anahtar kolon (`product_id` veya `id` gibi) üzerinden yan yana bağlamak için kullanılır.

#### Örnek Tablolarımız:
```
  [Musteri_Siparis (Sol)]              [Urun_Katalog (Sağ)]
┌────────────┬────────────┬────────┐ ┌────────────┬────────────┐
│ siparis_id │ product_id │ miktar │ │ product_id │  kategori  │
├────────────┼────────────┼────────┤ ├────────────┼────────────┤
│ 101        │ 1          │ 5      │ │ 1          │ Elektronik │
│ 102        │ 2          │ 3      │ │ 2          │ Giyim      │
│ 103        │ 99         │ 1      │ │ 3          │ Kitap      │
└────────────┴────────────┴────────┘ └────────────┴────────────┘
```
*(Not: `siparis_id: 103` için `product_id: 99` katalogda yok; katalogdaki `product_id: 3` ise hiç sipariş edilmemiş).*

---

#### 1. `INNER JOIN` (veya sadece `JOIN`)
Yalnızca her iki tabloda da **eşleşen anahtara sahip** satırları getirir. Eşleşmeyen satırlar atılır.
```sql
SELECT * FROM Musteri_Siparis S
INNER JOIN Urun_Katalog K ON S.product_id = K.product_id;
```
**Sonuç (2 Satır):**
```
┌────────────┬────────────┬────────┬────────────┬────────────┐
│ siparis_id │ product_id │ miktar │ product_id │  kategori  │
├────────────┼────────────┼────────┼────────────┼────────────┤
│ 101        │ 1          │ 5      │ 1          │ Elektronik │
│ 102        │ 2          │ 3      │ 2          │ Giyim      │
└────────────┴────────────┴────────┴────────────┴────────────┘
```
*(Sipariş 103 ve Kitap kayboldu).*

---

#### 2. `LEFT JOIN` (veya `LEFT OUTER JOIN`)
**Sol tablodaki (Musteri_Siparis) TÜM satırları korur.** Sağdaki tabloda karşılığı varsa kolonları doldurur, karşılığı yoksa `NULL` yazar.
```sql
SELECT * FROM Musteri_Siparis S
LEFT JOIN Urun_Katalog K ON S.product_id = K.product_id;
```
**Sonuç (3 Satır):**
```
┌────────────┬────────────┬────────┬────────────┬────────────┐
│ siparis_id │ product_id │ miktar │ product_id │  kategori  │
├────────────┼────────────┼────────┼────────────┼────────────┤
│ 101        │ 1          │ 5      │ 1          │ Elektronik │
│ 102        │ 2          │ 3      │ 2          │ Giyim      │
│ 103        │ 99         │ 1      │ NULL       │ NULL       │ <-- Sipariş silinmedi!
└────────────┴────────────┴────────┴────────────┴────────────┘
```

---

#### 3. `RIGHT JOIN` (veya `RIGHT OUTER JOIN`)
**Sağ tablodaki (Urun_Katalog) TÜM satırları korur.** Solda karşılığı yoksa `NULL` yazar.
```sql
SELECT * FROM Musteri_Siparis S
RIGHT JOIN Urun_Katalog K ON S.product_id = K.product_id;
```
**Sonuç (3 Satır):**
```
┌────────────┬────────────┬────────┬────────────┬────────────┐
│ siparis_id │ product_id │ miktar │ product_id │  kategori  │
├────────────┼────────────┼────────┼────────────┼────────────┤
│ 101        │ 1          │ 5      │ 1          │ Elektronik │
│ 102        │ 2          │ 3      │ 2          │ Giyim      │
│ NULL       │ NULL       │ NULL   │ 3          │ Kitap      │ <-- Hiç satılmayan kitap
└────────────┴────────────┴────────┴────────────┴────────────┘
```

---

#### 4. `FULL OUTER JOIN`
Hem soldaki hem sağdaki **bütün satırları** korur. Eşleşmeyen her yere `NULL` koyar.
```sql
SELECT * FROM Musteri_Siparis S
FULL OUTER JOIN Urun_Katalog K ON S.product_id = K.product_id;
```
**Sonuç (4 Satır):**
```
┌────────────┬────────────┬────────┬────────────┬────────────┐
│ siparis_id │ product_id │ miktar │ product_id │  kategori  │
├────────────┼────────────┼────────┼────────────┼────────────┤
│ 101        │ 1          │ 5      │ 1          │ Elektronik │
│ 102        │ 2          │ 3      │ 2          │ Giyim      │
│ 103        │ 99         │ 1      │ NULL       │ NULL       │
│ NULL       │ NULL       │ NULL   │ 3          │ Kitap      │
└────────────┴────────────┴────────┴────────────┴────────────┘
```

---

#### 5. `CROSS JOIN` (Kartezyen Çarpım)
Koşulsuz olarak Sol tablodaki her satırı Sağ tablodaki her satırla tek tek eşleştirir. ($M \times N$ satır üretir).

---

## Soru 7 (Ek Soru 2)
> **Önceki açıklamadaki "Kayıt Sayısı Kontrolü: Birleştirme öncesindeki customers satır sayısı ile birleştirme sonrasındaki customers satır sayısı birebir eşit olmalıdır." kısmını tam oturtamadım. LEFT JOIN items tablosunda customers'ta olmayan bir product_id'ye ait satır olduğu durumda ne yapıyor ki? Birleştirme tablosuna eklemiyor mu? Böylece customers satır sayısı artmayacak mı?**

### Cevap:

**Hayır, artmaz! `LEFT JOIN`'in çalışma mantığı tam olarak şudur:**

`LEFT JOIN` yaparken odak noktamız **SOLDAKİ (`customers`) tablodur**. `LEFT JOIN`, sağdaki (`items`) tablonun tamamını alıp masaya dökmez; yalnızca **soldaki her bir satır için sağdan parça arar.**

### Durum Senaryoları:

1. **Senaryo A (`customers`'taki ürün `items`'ta var):**  
   Müşteri `product_id = 1` almış. `items` tablosunda `product_id = 1` aranır $\rightarrow$ Bulunur. O satıra kategori ve marka eklenir.  
   $\rightarrow$ **Satır sayısı: 1 satır olarak kalır.**

2. **Senaryo B (`customers`'taki ürün `items`'ta YOK):**  
   Müşteri `product_id = 999` almış (katalogdan silinmiş eski ürün). `items`'ta aranır $\rightarrow$ Bulunamaz.  
   `LEFT JOIN` bu satırı silmez; kategori ve marka kolonlarına `NULL` yazar.  
   $\rightarrow$ **Satır sayısı: 1 satır olarak kalır.**

3. **Senaryo C (`items`'ta olan ama `customers`'ta HİÇ OLMAYAN ürün):**  
   Katalogda `product_id = 555` adında bir ürün var ama bugüne kadar hiçbir müşteri bu ürünü görüntülememiş veya satın almamış.  
   `LEFT JOIN` sol tablodaki satırlar üzerinden döner. Sol tabloda `555`'e ait bir müşteri hareketi olmadığı için **bu ürünü birleştirme tablosuna ASLA EKLEMEZ ve YOK SAYAR!**  
   $\rightarrow$ *(Bu ürünün sonuca eklenmesi ancak `RIGHT JOIN` veya `FULL OUTER JOIN` ile mümkün olurdu).*

### Peki Satır Sayısı Ne Zaman Artar? (Tehlike Noktası!)
Satır sayısı sadece ve sadece **`items` tablosunda AYNI `product_id` birden fazla satırda varsa (mükerrer ise)** artar!
Örneğin `items` tablosunda `product_id = 1` için 2 farklı satır varsa, müşterinin 1 adet işlem satırı sağdaki 2 satırla da eşleşir ve çıktı tablosunda **2 satıra çoğalır (Kartezyen çoğalma - Fan out).**

Eğer `items` tablosunda her `product_id` tekilse (unique), `customers` tablosunun satır sayısı **kesinlikle ne 1 eksilir ne de 1 artar!**

---

## Soru 8 (Ek Soru 3)
> **Subject açıklamalarına göre duplicate temizleme işi sadece birleştirilmiş customers tablosuna yapılıyor, yanlış mı anlıyorum?
> "Bire-Çok (1-to-Many) Çoğalma Riski: Eğer items tablosunda aynı product_id birden fazla satırda varsa, LEFT JOIN işlemi customers tablosundaki işlem satırlarını katlar (satır sayısı artar). Bu yüzden items tablosunda product_id'nin tekil (unique) olduğundan emin olunmalıdır." bu açıklamaya göre customers ile items'i birleştirmeden önce items için de bir duplicate temizliği gerekmez mi? Subject bunu söylememiş ama bizden bekliyor mu acaba?**

### Cevap:

### 🚨 Gerçek Veri İncelemesi: `item.csv` dosyasında duplicate var mı?
Veri setimizdeki `subject/item/item.csv` dosyasını terminalden doğrudan analiz ettiğimizde çok kritik bir bulgu ortaya çıkmaktadır:

- Toplam satır sayısı: **109.580**
- Tekrar eden (duplicate) `product_id` sayısı: **45.138 adet!**

Örnek satırlar (`product_id = 5712790`):
```csv
5712790,1487580005268456192,,f.o.x
5712790,,,
5712790,1487580005268456192,,
```
Görüldüğü üzere aynı ürün için hem dolu bilgiler (`f.o.x` markalı) hem de eksik/boş bilgiler içeren 3 farklı satır bulunmaktadır!

### Neden Subject Doğrudan Söylemedi Ama Bizden Bunu Bekliyor?
1. **Subject Uyarısı:** Subject ex03'te özellikle şunu vurgular:
   > *"You must combine the 'customers' tables with 'items' in the 'customers' table. **Be careful not to lose any information**"*
2. Eğer `items` tablosunu tekilleştirmeden doğrudan `LEFT JOIN` yaparsanız:
   - 1 müşteri işlemi 3 satıra katlanır.
   - Toplam ciro, sipariş adedi ve müşteri metrikleri yapay olarak 3 katına çıkar!
   - Bu durum `ds_2` (Data Viz) ve `ds_4` (Machine Learning) modüllerindeki tüm analizleri ve modelleri **tamamen bozar**.
3. **Çözüm:** `ex03` (fusion) adımında `items` tablosunu birleştirmeden önce, her bir `product_id` için **en dolu/en güncel tek satırı** seçecek şekilde bir alt sorgu (`DISTINCT ON (product_id)` veya filtre) ile `JOIN` yapılmalıdır.

---

## Soru 9 (Ek Soru 4)
> **ex03'teki birleşmeden sonra da bir duplicate temizliği bekleniyor mu? Beklenmiyorsa da sektörde bu tarz büyük birleştirmelerden sonra bir duplicate temizliği yapılır mı, gerek olur mu, böyle bir gelenek var mı?**

### Cevap:

### 1. Bu Projede Bekleniyor mu?
Hayır. Çünkü doğru bir veri mimarisinde:
- `customers` tablosu `ex02`'de zaten temizlenmiştir.
- `items` tablosundaki ürünler `product_id` bazında tekil olarak `LEFT JOIN` ile bağlandığında, **birleşme sonucu yeni hiçbir duplicate ÜRETİLMEZ.**

### 2. Sektörde Durum Nedir? Birleştirmeden Sonra Duplicate Temizliği Yapılır mı?
Sektördeki modern veri mühendisliği standartlarında (Modern Data Stack: dbt, Snowflake, BigQuery, Databricks):

**❌ Kötü Alışkanlık (Antipattern):**  
Büyük bir `JOIN` yaptıktan sonra *"ne olur ne olmaz"* diyerek çıktının sonuna körlemesine `SELECT DISTINCT` veya satır silme çalıştırmak **çok yanlış ve tehlikeli bir yöntemdir**. Çünkü:
- Milyonlarca satırda `DISTINCT` sorguyu inanılmaz yavaşlatır.
- Asıl problem olan "hatalı JOIN ilişkisini" (1-to-many patlamasını) gizler ve kök nedeni çözmez.

**✅ Sektör Standardı (Data Assertion / Kalite Testleri):**  
Sektörde birleştirme bittikten sonra temizlik yapmak yerine **Otomasyon Testleri (Assertions)** çalıştırılır:
1. **Row Count Assertion:** Birleştirme öncesi `customers` satır sayısı ile sonrası eşit mi? (`COUNT(*) = COUNT(*)`)
2. **Primary Key Test:** İşlem anahtarı tekil mi?
3. **Null Check:** Beklenmeyen `NULL` patlaması var mı?

Eğer test başarısız olursa (örneğin satır sayısı artmışsa), veri mühendisi çıktıyı temizlemekle uğraşmaz; doğrudan `JOIN` mantığına ve boyut tablosundaki (`items`) tekillik problemine müdahale eder.

---

## Soru 10 (Ek Sorular 2 - 1)
> **Yatay birleştirmelerde birleştirdikten sonra birleştirme kolonu (ortak kolon) 2 kere mi yazılır, yoksa ortak diye tek bir kolona mı dönüştürülür?**

### Cevap:

SQL'de bu durum sorguyu **nasıl yazdığınıza** bağlıdır:

1. **`SELECT *` Kullanırsanız (Kötü Pratik):**  
   SQL her iki tablodaki tüm kolonları getirir. Ortak kolon iki tabloda da var olduğu için sonuç tablosunda **2 kez `product_id` kolonu** yer alır (Örn: `customers.product_id` ve `items.product_id`). Çoğu veritabanında bu durum kolon adı çakışması (ambiguous column name) hatası üretir.

2. **Kolonları Açıkça Seçerseniz (`SELECT c.product_id, ...` - Doğru Pratik):**  
   Veri ambarı modellemesinde `SELECT *` kullanılmaz. İhtiyaç duyulan kolonlar tek tek belirtilir. Birleştirme kolonu olan `product_id` sol tablodan (`c.product_id`) bir kez seçilir ve sonuç tablosunda **yalnızca 1 adet `product_id` kolonu** bulunur.

```sql
-- Nihai Temiz Tablo Şeması:
SELECT 
    c.event_time,
    c.event_type,
    c.product_id,    -- <-- Tek bir ortak kolon olarak kalır
    c.price,
    c.user_id,
    c.user_session,
    i.category_id,
    i.category_code,
    i.brand
FROM customers c
LEFT JOIN unique_items i ON c.product_id = i.product_id;
```

---

## Soru 11 (Ek Sorular 2 - 2)
> **NULL meselesi: Bu NULL'lar yeni birleştirme tablosuna hangi veri türü ile kaydediliyor? NULL'un kendisi bir veri türü mü yoksa her veri türüne uyan bir tür mü SQL'de? Ayrıca bir CSV'den veri çekildiğinde boş hücreler NULL olarak mı çekiliyor? Ya da bir SQL tablosunu CSV'ye aktarsak NULL kısımlar boş hücre olarak mı geçer? Bu NULL girdiler SQL tablosunda yapılacak sorgu, ayıklama, eşitlik kontrolü vb. durumlarda nasıl davranır?**

### Cevap:

### 1. `NULL` Nedir? Bir Veri Türü müdür?
**Hayır, `NULL` bir veri türü veya değer değildir.** (Sıfır `0`, boş metin `""` veya `false` DEĞİLDİR).
- `NULL`, bir hücrenin **"bilinmeyen", "tanımsız" veya "mevcut olmayan" (missing value)** durumda olduğunu belirten özel bir **işaretçi/durumdur (state marker)**.
- SQL'deki her veri türü (INTEGER, VARCHAR, TIMESTAMPTZ, UUID vb.), eğer tabloda `NOT NULL` kısıtı verilmemişse, `NULL` değerini kabul edebilir.
- Bir `INTEGER` kolonundaki `NULL`, o kolonun tipini bozmaz; o kolon yine `INTEGER` olarak kalır, sadece o satır için değerin "bilinmediğini" ifade eder.

---

### 2. CSV İçe/Dışa Aktarımında (Import/Export) `NULL` Davranışı
- **CSV $\rightarrow$ SQL (`\copy` ile okurken):**  
  PostgreSQL'in CSV modunda iki virgül arasındaki boşluk (`, ,`) varsayılan olarak **`NULL`** kabul edilir ve veritabanına `NULL` olarak yazılır.
- **SQL $\rightarrow$ CSV (Export ederken):**  
  Veritabanındaki `NULL` değerler, CSV dosyasına yazılırken standart olarak **boş hücre** (`, ,`) olarak aktarılır.

---

### 3. `NULL` Değerlerin SQL Mantığındaki Davranışı (3 Değerli Mantık - 3VL)
SQL, klasik `TRUE` / `FALSE` ikili mantığı yerine **Üç Değerli Mantık (TRUE, FALSE, UNKNOWN)** kullanır:

| Durum | SQL İfadesi | Sonuç | Açıklama |
|---|---|---|---|
| **Eşitlik Kontrolü** | `price = NULL` | **UNKNOWN (False gibi davranır)** | İki bilinmeyen birbirine eşit kabul edilemez! |
| **Doğru Kontrol** | `price IS NULL` | **TRUE** | `IS NULL` veya `IS NOT NULL` kullanılmalıdır. |
| **Eşit Değildir** | `brand != 'Apple'` | **NULL olan satırları ELER!** | `brand`'i NULL olan satırlar bu filtreden elenir! |
| **Toplama / Matematik** | `10 + NULL` | **NULL** | Bilinmeyen bir sayıyla 10'u toplarsanız sonuç yine bilinmeyendir. |
| **Toplulaştırma Fonksiyonları** | `AVG(price)`, `SUM(price)` | **NULL'ları yok sayar** | Hesaplamaya sadece dolu değerleri dahil eder. |
| **Sayma (`COUNT`)** | `COUNT(*)` vs `COUNT(brand)` | Farklıdır | `COUNT(*)` tüm satırları sayar; `COUNT(brand)` ise sadece `brand`'i dolu olanları sayar. |

---

## Soru 12 (Ek Sorular 2 - 3)
> **ex03'te yapılacak birleştirme işleminde hangi tablonun baz alınacağını "You must combine the customers tables with items in the customers table" cümlesinden mi çıkarıyoruz? Böyle bir ifade geçmese de "asıl olan müşteri işlemleri olmalı..." şeklinde akıl yürüterek de sonuca ulaşabilir miydik? Sektör pratiğinde böyle durumlarda asıl olan tabloyu ya da FULL OUTER JOIN yapıp yapmayacağımızı nasıl belirleriz?**

### Cevap:

**Evet! Cümle hiç olmasa dahi Veri Ambarı Modelleme (Dimensional Modeling) prensipleriyle aynı sonuca ulaşırdık.**

Veri Ambarı dünyasında (Kimball Metodolojisi) tablolar ikiye ayrılır:

```
┌──────────────────────────────────────────────────┐     ┌───────────────────────────────────┐
│     FACT TABLE (Olay / Hareket Tablosu)          │     │  DIMENSION TABLE (Boyut Tablosu)  │
│                [customers]                       │     │              [items]              │
├──────────────────────────────────────────────────┤     ├───────────────────────────────────┤
│ • Zaman serisi hareketlerini tutar (sipariş, vb) │◄────┤ • Ürünün özelliklerini açıklar    │
│ • Milyonlarca satırdır                           │     │ • Statik katalog verisidir        │
│ • Ciro, dönüşüm oranı gibi metrikler buradan çıkar│    │ • Kategori, marka gibi sıfatlardır│
└──────────────────────────────────────────────────┘     └───────────────────────────────────┘
```

### Hangi JOIN Türünü Seçeceğimizi Nasıl Belirleriz?
- **`FULL OUTER JOIN` Neden Yapılmaz?**  
  Eğer `FULL OUTER JOIN` yaparsanız, katalogda olup hiç satılmamış/tıklanmamış 10.000 ürün için `event_time = NULL`, `user_id = NULL`, `event_type = NULL` olan **"hayalet işlem satırları"** oluşur. Bu satırlar müşteri analitiğini, günlük aktif kullanıcı (DAU) ve zaman serisi grafiklerini bozar.
- **`INNER JOIN` Neden Yapılmaz?**  
  Katalogda tanımlanması unutulmuş bir ürün satıldığında, `INNER JOIN` o satışı tablodan siler ve şirketin cirosu veritabanında eksik görünür (veri kaybı).
- **`LEFT JOIN` (Fact $\rightarrow$ Dimension):**  
  İşlem hareketini (`customers`) merkeze alır, katalogdan (`items`) sıfatları ekler. Katalogda ürün yoksa bile satışı korur. Bu yüzden analitik sistemlerde **Fact tablosundan Dimension tablosuna her zaman `LEFT JOIN` atılır.**

---

## Soru 13 (Ek Sorular 2 - 4)
> **ex02 için verilen duplicate temizleme kodunun tam halini verip detaylıca, basit örneklerle açıklar mısın? LAG fonksiyonu nasıl çalışıyor? CTAS, WITH, AS, OVER, PARTITION BY, EXTRACT, EPOCH anahtar kelimeleri ne demek? Neden `> 1` kullandık, `< 1` olması gerekmez mi?**

### Cevap:

Önce kodun tam ve çalışır halini verelim, ardından her satırı ve kavramı adım adım parçalayalım:

### Tam ve Çalışır SQL Kodu (`remove_duplicates.sql`)
```sql
\echo '================================================================================'
\echo 'Processing: remove_duplicates.sql'

-- 1. ADIM: Temiz veriyi yeni bir tabloya (CTAS) aktarıyoruz
DROP TABLE IF EXISTS customers_clean;

CREATE TABLE customers_clean AS
WITH ranked_events AS (
    SELECT 
        event_time,
        event_type,
        product_id,
        price,
        user_id,
        user_session,
        LAG(event_time) OVER (
            PARTITION BY user_id, user_session, event_type, product_id, price
            ORDER BY event_time
        ) AS prev_event_time
    FROM customers
)
SELECT 
    event_time,
    event_type,
    product_id,
    price,
    user_id,
    user_session
FROM ranked_events
WHERE prev_event_time IS NULL 
   OR EXTRACT(EPOCH FROM (event_time - prev_event_time)) > 1;

-- 2. ADIM: Eski kirli tabloyu silip temiz tabloyu 'customers' yapıyoruz
DROP TABLE customers;
ALTER TABLE customers_clean RENAME TO customers;

\echo 'Duplicate records successfully removed from customers table.'
\echo '================================================================================'
```

---

### Kavramlar ve Anahtar Kelimeler Sözlüğü:

#### 1. CTAS (`CREATE TABLE ... AS SELECT`)
- Bir `SELECT` sorgusunun çıktısını doğrudan yeni bir fiziksel tablo olarak oluşturur.
- **Neden `DELETE FROM` yerine CTAS?** 16 milyon satırlık bir tabloda milyonlarca satırı `DELETE` ile silmek, PostgreSQL'in her satır için transaction log (WAL) ve kilit mekanizması işletmesine neden olur ve saatler sürebilir. CTAS ise temiz satırları sırayla diske yazar ve **saniyeler içinde** tamamlanır.

#### 2. `WITH ... AS` (CTE - Common Table Expression)
- Ana sorgunun üstünde tanımlanan **geçici, adlandırılmış sanal bir tablodur**. Sorgunun okunabilirliğini artırır.

#### 3. Window Fonksiyonu Mekanizması (`OVER`, `PARTITION BY`, `ORDER BY`)
- Normal `GROUP BY` satırları birleştirip tek satıra indirir (özetler).
- **Window Fonksiyonu (`OVER`)** ise her satırı yerinde korur, ancak satırın arkasına ilişkili diğer satırlara bakabilen bir "pencere" açar.
- **`PARTITION BY user_id, user_session, event_type, product_id, price`:**  
  Tabloyu küçük sanal gruplara (odalara) böler. Aynı kullanıcının aynı oturumda aynı ürüne yaptığı aynı eylemleri aynı odaya toplar.
- **`ORDER BY event_time`:** O odanın içindeki satırları kronolojik olarak (eskiden yeniye) sıralar.

#### 4. `LAG(event_time)` Fonksiyonu
- Sıralanmış pencere içinde **"bir önceki satırın"** değerini okur ve yanına sütun olarak ekler.

#### Basit Örnekle Canlandırma:
```
[customers Tablosundaki Ham Satırlar]
Satır 1: 00:00:10 | user_1 | cart | prod_A
Satır 2: 00:00:11 | user_1 | cart | prod_A  <-- 1 sn sonra (Duplicate!)
Satır 3: 00:00:45 | user_1 | cart | prod_A  <-- 34 sn sonra (Farklı zaman - Geçerli)

[LAG Fonksiyonu Çalıştıktan Sonraki Tablo (ranked_events)]
Satır   event_time   prev_event_time   Fark (Saniye)
─────   ──────────   ───────────────   ─────────────
1       00:00:10     NULL              Yok (İlk tıklama)
2       00:00:11     00:00:10          1 saniye  (Duplicate!)
3       00:00:45     00:00:11          34 saniye (Geçerli)
```

#### 5. `EXTRACT(EPOCH FROM (event_time - prev_event_time))`
- İki zamanı birbirinden çıkarınca (`00:00:11 - 00:00:10`) sonuç bir `INTERVAL` (zaman aralığı) tipidir.
- `EXTRACT(EPOCH FROM ...)` bu zaman aralığını saf **saniye cinsinden sayıya (float)** dönüştürür (Örn: `1.0` veya `34.0`).

#### 6. Neden `> 1` Kullandık? (`< 1` Olması Gerekmez miydi?)
İşte en kritik mantık noktası:
- SQL'deki `WHERE` koşulu **"HANGİ SATIRLARI TUTMAK / SEÇMEK İSTİYORSUN?"** sorusunun cevabıdır (silinecekleri değil, kalacakları filtreler).
- Eğer fark $\le 1$ ise bu satır **Hatalı / Duplicate**'tir (Bunu İSTEMİYORUZ).
- Eğer fark $> 1$ ise veya `prev_event_time IS NULL` ise (yani o kullanıcının ilk tıklamasıysa), bu satır **GEÇERLİ VE TEMİZ** bir satırdır (Bunu TABLODA TUTMAK İSTİYORUZ).
- Bu yüzden `WHERE prev_event_time IS NULL OR fark > 1` yazarak temiz satırları seçip yeni tabloya kaydediyoruz!

---

## Soru 14 (Ek Sorular 2 - 5)
> **`item.csv` dosyası neyin dosyası tam olarak? Bunlar elimizdeki ürünlerin listesi değil mi? Neden duplicate var ki o zaman, aynı ürün için neden birden fazla satır oluşturulup kaydedilmiş olabilir? Burada "en dolu/en güncel satırı" hangi kriterlerle seçmek mantıklı olacak?**

### Cevap:

### 1. `item.csv` Nedir?
E-ticaret platformundaki ürünlerin üst verilerini (Metadata / Katalog) içeren boyut tablosudur:
- `product_id`: Ürünün benzersiz numarası
- `category_id`: Kategorinin sayısal ID'si
- `category_code`: Kategorinin hiyerarşik adı (`appliances.environment.air_heater` gibi)
- `brand`: Ürünün markası (`apple`, `samsung`, `f.o.x` gibi)

---

### 2. Neden Duplicate Var? Gerçek Hayatta Bu Nasıl Oluşur?
Bir ürün kataloğunda duplicate olmasının 3 temel veri mühendisliği sebebi vardır:
1. **Zaman İçinde Güncellenen Kayıtlar (SCD - Slowly Changing Dimensions):**  
   Ürün ilk eklendiğinde sadece ID'si girilmiş (`5712790,,,`), daha sonra kategori eklenmiş (`5712790,1487580005268456192,,`), en son marka eklenmiştir (`5712790,1487580005268456192,,f.o.x`). Ham sistem logları bu güncellemeleri üstüne yazmak yerine her adımı ayrı satır olarak kaydetmiştir.
2. **Farklı Sistemlerin / Servislerin Birleşimi:** Kategori servisi ayrı, stok servisi ayrı log üretmiş olabilir.
3. **Eksik / Kirli Veri Girişi:** Web scraping veya toplu içe aktarım sırasında boş kalan kayıtlar silinmemiştir.

---

### 3. "En Dolu Satırı" Seçme Kriterlerimiz Ne Olmalı?
Bir satırın kalitesini belirleyen şey **boş olmayan kolon sayısı ve zenginliğidir**:
1. **1. Öncelik (`category_code` ve `brand` dolu olanlar):** Analizlerde en çok marka ve kategori ismi kullanılır. Bu kolonları `NULL` veya boş string (`''`) olmayan satır en değerlidir.
2. **2. Öncelik (`category_id` dolu olanlar):** Sayısal kategori ID'si bulunan satırlar.
3. **3. Öncelik:** Tamamen boş olan satırlar en son tercih edilir.

---

## Soru 15 (Ek Sorular 2 - 6)
> **ex03 (fusion) adımında `items` tablosunu birleştirmeden önce en dolu satırı seçecek sorguyu verip en ince ayrıntısına kadar açıklar mısın?**

### Cevap:

### Tam ve Çalışır SQL Kodu (`fusion.sql`)
```sql
\echo '================================================================================'
\echo 'Processing: fusion.sql'

-- 1. ADIM: customers ve tekilleştirilmiş items tablolarını birleştiriyoruz
DROP TABLE IF EXISTS customers_fusion;

CREATE TABLE customers_fusion AS
WITH unique_items AS (
    SELECT DISTINCT ON (product_id)
        product_id,
        category_id,
        category_code,
        brand
    FROM items
    ORDER BY 
        product_id,
        (category_code IS NOT NULL AND category_code <> '') DESC,
        (brand IS NOT NULL AND brand <> '') DESC,
        category_id DESC NULLS LAST
)
SELECT 
    c.event_time,
    c.event_type,
    c.product_id,
    c.price,
    c.user_id,
    c.user_session,
    i.category_id,
    i.category_code,
    i.brand
FROM customers c
LEFT JOIN unique_items i ON c.product_id = i.product_id;

-- 2. ADIM: Eski customers tablosunu silip zenginleştirilmiş tabloyu customers yapıyoruz
DROP TABLE customers;
ALTER TABLE customers_fusion RENAME TO customers;

\echo 'Fusion completed successfully! customers table is now enriched with items.'
\echo '================================================================================'
```

---

### Adım Adım Kod Açıklaması:

#### 1. `DISTINCT ON (product_id)` (PostgreSQL'e Özgü Güçlü Operatör)
- Standart `DISTINCT`, tüm kolonların birebir aynı olduğu satırları teke indirir.
- **`DISTINCT ON (product_id)`** ise: *"Bana her farklı `product_id` için **sadece 1 satır** ver"* demektir.
- Peki birden fazla satır varsa **hangisini** seçecektir? İşte bunu altındaki `ORDER BY` belirler! `DISTINCT ON`, sıralamada **en tepeye (1. sıraya) gelen ilk satırı** alır, geri kalanları atar.

#### 2. `ORDER BY` Kriterlerinin Mantığı:
PostgreSQL'de mantıksal şartlar `TRUE` veya `FALSE` üretir. `DESC` sıralamada `TRUE` (1), `FALSE` (0)'dan önce gelir:
- `product_id`: `DISTINCT ON` kuralı gereği ilk sırada olmak zorundadır.
- `(category_code IS NOT NULL AND category_code <> '') DESC`: Kategori adı dolu olan satırlar `TRUE` alarak en üste çıkar.
- `(brand IS NOT NULL AND brand <> '') DESC`: Markası dolu olan satırlar bir sonraki öncelikle üste çıkar.
- `category_id DESC NULLS LAST`: Kategori ID'si dolu olanlar `NULL` olanların önüne geçer.

Bu sayede her ürünün **en dolu, en eksiksiz tekil satırı** seçilir ve `customers` tablosuna `LEFT JOIN` ile bağlandığında:
1. Hiçbir müşteri hareketi silinmez (veri kaybı sıfır).
2. Hiçbir müşteri hareketi katlanıp çoğalmaz (satır sayısı birebir korunur).
3. Müşteri işlemleri marka ve kategori bilgileriyle kusursuz şekilde zenginleşmiş olur.
