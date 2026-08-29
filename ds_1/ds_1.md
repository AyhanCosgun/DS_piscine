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

