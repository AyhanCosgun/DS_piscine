# SQL ve PostgreSQL Temel Rehberi

Bu not, `ds_0` projesinde kullanacagin SQL dilini ve PostgreSQL'e ozgu pratikleri
anlatir. Ozellikle `ex02/table.sql` dosyasindaki tablo olusturma ve CSV yukleme
mantigini anlaman icin hazirlandi.

Mevcut `ex02/table.sql` dosyan:

```sql
CREATE TABLE data_2022_oct (
    event_time TIMESTAMPTZ,
    event_type VARCHAR(32),
    product_id INTEGER,
    price NUMERIC(10, 2),
    user_id BIGINT,
    user_session UUID
);

\copy data_2022_oct FROM '../subject/customer/data_2022_oct.csv' WITH (FORMAT csv, HEADER true);
```

Bu dosya iki ana is yapiyor:

1. `data_2022_oct` adinda bir tablo olusturuyor.
2. CSV dosyasindaki satirlari bu tabloya yukluyor.

## SQL Nedir?

SQL, "Structured Query Language" ifadesinin kisaltmasidir. Turkce dusunursek
"yapilandirilmis sorgu dili" demektir.

SQL ile veritabanina sunlari soylersin:

- Tablo olustur.
- Tabloyu sil.
- Tabloya veri ekle.
- Tablodan veri oku.
- Belirli sartlara uyan satirlari getir.
- Satirlari grupla.
- Toplam, ortalama, sayim gibi hesaplar yap.
- Tablolari birbirine bagla.
- Veriyi guncelle veya sil.

SQL genel bir dildir, ama her veritabani sistemi kendi lehcesine sahiptir.

Ornegin:

- PostgreSQL
- MySQL
- MariaDB
- SQLite
- SQL Server
- Oracle

Bu projede kullandigimiz sistem PostgreSQL oldugu icin bu not PostgreSQL odaklidir.

## SQL ile psql Arasindaki Fark

Bu ayrim cok onemli.

`SQL`, veritabanina gonderilen sorgu dilidir:

```sql
SELECT *
FROM data_2022_oct
LIMIT 10;
```

`psql` ise PostgreSQL'in terminal programidir. Yani veritabanina baglanmak ve SQL
komutlarini calistirmak icin kullandigin arac.

`psql` icinde SQL komutlari disinda bazi ozel komutlar da vardir. Bunlar genelde
ters slash ile baslar:

```text
\dt
\d data_2022_oct
\copy
\q
```

Bu komutlar SQL dilinin parcasi degildir. Bunlar psql programinin kendi komutlaridir.

Ornek:

```sql
SELECT * FROM data_2022_oct LIMIT 10;
```

Bu SQL'dir.

```text
\dt
```

Bu psql komutudur.

## Soru 1: Bu Dilde Temel Veri Tipleri Nelerdir?

SQL'de tablo olustururken her kolonun veri tipini belirtirsin. Bu, veritabanina
"bu kolonda nasil veri saklanacak?" sorusunun cevabini verir.

Ornegin:

```sql
product_id INTEGER
price NUMERIC(10, 2)
event_type VARCHAR(32)
```

Bu sayede PostgreSQL sunlari bilir:

- `product_id` tam sayidir.
- `price` ondalikli sayidir.
- `event_type` kisa metindir.

Her seyi `TEXT` olarak saklamak kolay gorunur, ama ileride filtreleme, siralama,
hesaplama ve tablo birlestirme islemlerini bozar veya zorlastirir.

### ex02/table.sql Icindeki Veri Tipleri

Mevcut tablon:

```sql
CREATE TABLE data_2022_oct (
    event_time TIMESTAMPTZ,
    event_type VARCHAR(32),
    product_id INTEGER,
    price NUMERIC(10, 2),
    user_id BIGINT,
    user_session UUID
);
```

Bu tablo 6 kolon ve 6 farkli veri tipi kullaniyor.

### TIMESTAMPTZ

```sql
event_time TIMESTAMPTZ
```

`TIMESTAMPTZ`, PostgreSQL'de `timestamp with time zone` ifadesinin kisa adidir.

Yani tarih + saat + saat dilimi bilgisi tutar.

CSV'deki ornek deger:

```text
2022-10-01 00:00:00 UTC
```

Bu degerde sunlar var:

- Tarih: `2022-10-01`
- Saat: `00:00:00`
- Saat dilimi: `UTC`

Bu yuzden `TIMESTAMPTZ` dogru secimdir.

Eger bunu `TEXT` yapsaydin veritabani bu degerin tarih oldugunu bilmezdi. O zaman
zamana gore siralama, tarih araligi filtreleme ve gun/ay/yil bazli analiz yapmak
daha zor olurdu.

Ornek sorgu:

```sql
SELECT *
FROM data_2022_oct
WHERE event_time >= '2022-10-15 00:00:00 UTC'
LIMIT 10;
```

Burada PostgreSQL `event_time` kolonunun tarih-saat oldugunu bildigi icin karsilastirmayi
dogru yapar.

### VARCHAR(32)

```sql
event_type VARCHAR(32)
```

`VARCHAR`, degisken uzunluklu metin demektir.

`VARCHAR(32)` ise "en fazla 32 karakter uzunlugunda metin" demektir.

Buradaki `32`, bellekte kesin 32 karakter ayriliyor anlamina gelmez. Maksimum izin
verilen karakter sayisidir.

Ornek event type degerleri:

```text
view
cart
purchase
remove_from_cart
```

Bu degerler kisa metinlerdir. En uzunu `remove_from_cart`, yani 16 karakterdir. Bu
yuzden `VARCHAR(32)` yeterlidir.

#### Neden str degil?

Python'da metin tipi:

```python
str
```

C dilinde karakter:

```c
char
```

SQL'de ise veri tipleri veritabani sisteminin kendi tipleridir. PostgreSQL'de metin
icin genellikle sunlar kullanilir:

```sql
CHAR(n)
VARCHAR(n)
TEXT
```

Yani SQL'de Python'daki gibi `str` yazmazsin. C'deki gibi genel olarak `char *` da
yazmazsin. Veritabanina metnin nasil saklanacagini SQL veri tipiyle soylersin.

#### CHAR, VARCHAR, TEXT farki

```sql
CHAR(10)
```

Sabit uzunluklu metindir. Deger daha kisaysa boslukla doldurulabilir. Cogu durumda
gereksizdir.

```sql
VARCHAR(10)
```

En fazla 10 karakterlik degisken uzunluklu metindir.

```sql
TEXT
```

Uzunluk siniri belirtmeden metin tutar.

Ornek:

```sql
CREATE TABLE examples (
    code CHAR(3),
    name VARCHAR(50),
    description TEXT
);
```

Bu projede:

```sql
event_type VARCHAR(32)
```

mantikli cunku event type degerleri kisa ve sinirli metinlerdir.

### INTEGER

```sql
product_id INTEGER
```

`INTEGER`, tam sayi tipidir.

PostgreSQL'de `INTEGER` genelde 4 byte yer kaplar ve yaklasik olarak su araliktaki
sayilari tutar:

```text
-2 milyar ile +2 milyar arasi
```

CSV'deki product id ornegi:

```text
5773203
```

Bu bir tam sayidir. Ondalik kismi yoktur. Bu yuzden `INTEGER` uygundur.

Ornek sorgu:

```sql
SELECT *
FROM data_2022_oct
WHERE product_id = 5773203;
```

### NUMERIC(10, 2)

```sql
price NUMERIC(10, 2)
```

`NUMERIC`, kesin hassasiyetli ondalik sayi tipidir. Para/fiyat gibi degerler icin
`FLOAT` yerine genellikle `NUMERIC` tercih edilir.

`NUMERIC(10, 2)` ifadesindeki sayilar:

```text
10 -> toplam basamak sayisi
2  -> virgülden sonraki basamak sayisi
```

ASCII ile soyle yazalim:

```text
NUMERIC(10, 2)
        |   |
        |   +-- ondalik kisimda 2 basamak
        +------ toplam 10 basamak
```

Yani su tarz degerleri tutabilir:

```text
2.62
13.48
99999999.99
```

Toplam 10 basamak oldugu icin ondalik kisim 2 basamaksa tam kisim icin 8 basamak
kalir.

Fiyat icin neden `FLOAT` degil?

`FLOAT` yaklasik sayi tipidir. Bilgisayarin ikili sayi sistemi yuzunden bazi ondalik
sayilari tam temsil edemez.

Para hesaplarinda bu istenmez. O yuzden:

```sql
price NUMERIC(10, 2)
```

daha dogrudur.

Ornek:

```sql
SELECT SUM(price)
FROM data_2022_oct
WHERE event_type = 'purchase';
```

### BIGINT

```sql
user_id BIGINT
```

`BIGINT`, buyuk tam sayi tipidir. PostgreSQL'de 8 byte yer kaplar.

`INTEGER` 4 byte, `BIGINT` 8 byte'tir.

`user_id` gibi kimlik degerleri zamanla cok buyuyebilir. Bu yuzden `BIGINT` daha
guvenli bir secimdir.

Ornek sorgu:

```sql
SELECT *
FROM data_2022_oct
WHERE user_id = 463240011;
```

Bu ornekteki sayi `INTEGER` icine de sigar, ama kullanici ID sistemleri buyuyebilecegi
icin `BIGINT` kullanmak mantiklidir.

### UUID

```sql
user_session UUID
```

`UUID`, "Universally Unique Identifier" demektir. Benzersiz kimlik degerleri icin
kullanilir.

CSV'deki ornek:

```text
26dd6e6e-4dac-4778-8d2c-92e149dab885
```

Bu klasik UUID formatidir:

```text
8-4-4-4-12 hexadecimal karakter
```

Eger bunu `TEXT` yapsaydin PostgreSQL format kontrolu yapmazdi. `UUID` yaptiginda
PostgreSQL bu degerin gercekten UUID formatinda olup olmadigini kontrol eder.

Ornek sorgu:

```sql
SELECT *
FROM data_2022_oct
WHERE user_session = '26dd6e6e-4dac-4778-8d2c-92e149dab885';
```

### Diger Sik Kullanilan PostgreSQL Veri Tipleri

#### BOOLEAN

Dogru/yanlis degeri tutar.

```sql
is_active BOOLEAN
```

Degerler:

```text
true
false
```

#### SMALLINT

Kucuk tam sayi tipidir. 2 byte yer kaplar.

```sql
age SMALLINT
```

#### REAL ve DOUBLE PRECISION

Yaklasik ondalikli sayi tipleridir.

```sql
temperature REAL
score DOUBLE PRECISION
```

Bilimsel/olcum verilerinde kullanilabilir, ama para icin genellikle `NUMERIC` daha
dogrudur.

#### DATE

Sadece tarih tutar.

```sql
birth_date DATE
```

Ornek:

```text
2026-08-21
```

#### TIME

Sadece saat tutar.

```sql
start_time TIME
```

Ornek:

```text
14:30:00
```

#### TIMESTAMP

Tarih + saat tutar, ama saat dilimi bilgisi yoktur.

```sql
created_at TIMESTAMP
```

#### TIMESTAMPTZ

Tarih + saat + saat dilimi mantigi ile calisir.

```sql
event_time TIMESTAMPTZ
```

Bu projedeki `event_time` icin daha uygundur cunku CSV'de `UTC` bilgisi var.

#### JSON ve JSONB

JSON yapisinda veri tutar.

```sql
metadata JSONB
```

`JSONB`, PostgreSQL'de genellikle daha kullanisli ve indekslenebilir JSON tipidir.

#### ARRAY

Liste benzeri degerler tutabilir.

```sql
tags TEXT[]
```

Ama veritabani tasariminda her zaman ilk tercih olmayabilir. Cogu durumda ayri tablo
daha dogru olur.

## Soru 2: En Cok Kullanacagin Temel Komutlar ve Yapilar

SQL komutlarini kabaca iki gruba ayirabiliriz:

```text
DDL -> tablo/veritabani yapisini tanimlayan komutlar
DML -> veri okuma, ekleme, guncelleme, silme komutlari
```

DDL: Data Definition Language

```sql
CREATE TABLE
ALTER TABLE
DROP TABLE
```

DML: Data Manipulation Language

```sql
SELECT
INSERT
UPDATE
DELETE
```

### CREATE TABLE

Tablo olusturur.

```sql
CREATE TABLE data_2022_oct (
    event_time TIMESTAMPTZ,
    event_type VARCHAR(32),
    product_id INTEGER,
    price NUMERIC(10, 2),
    user_id BIGINT,
    user_session UUID
);
```

Genel form:

```sql
CREATE TABLE table_name (
    column_name data_type,
    column_name data_type,
    column_name data_type
);
```

Her kolon icin:

```text
kolon adi + veri tipi
```

yazarsin.

### DROP TABLE

Tabloyu siler.

```sql
DROP TABLE data_2022_oct;
```

Bu komut dikkatli kullanilmalidir. Tabloyu ve icindeki veriyi siler.

### DROP TABLE IF EXISTS

Tablo varsa siler, yoksa hata vermez.

```sql
DROP TABLE IF EXISTS data_2022_oct;
```

Bu ozellikle scriptleri tekrar calistirirken kullanislidir.

Mesela ayni `CREATE TABLE` komutunu ikinci kez calistirirsan tablo zaten varsa hata
alirsin:

```text
relation "data_2022_oct" already exists
```

Bunu onlemek icin script basina sunu koyabilirsin:

```sql
DROP TABLE IF EXISTS data_2022_oct;

CREATE TABLE data_2022_oct (
    event_time TIMESTAMPTZ,
    event_type VARCHAR(32),
    product_id INTEGER,
    price NUMERIC(10, 2),
    user_id BIGINT,
    user_session UUID
);
```

### SELECT

Tablodan veri okur.

```sql
SELECT *
FROM data_2022_oct;
```

`*`, tum kolonlar demektir.

Buyuk tabloda her seyi getirmek iyi fikir degildir. Bu projedeki CSV milyonlarca satir
iceriyor. O yuzden genelde `LIMIT` ile kullan:

```sql
SELECT *
FROM data_2022_oct
LIMIT 10;
```

### Belirli Kolonlari Secmek

```sql
SELECT event_time, event_type, price
FROM data_2022_oct
LIMIT 10;
```

Bu sadece 3 kolonu getirir:

```text
event_time
event_type
price
```

### FROM

Verinin hangi tablodan okunacagini belirtir.

```sql
FROM data_2022_oct
```

`SELECT` genelde `FROM` ile birlikte kullanilir:

```sql
SELECT price
FROM data_2022_oct;
```

### WHERE

Satir filtrelemek icin kullanilir.

```sql
SELECT *
FROM data_2022_oct
WHERE event_type = 'purchase'
LIMIT 10;
```

Bu sadece `event_type` degeri `purchase` olan satirlari getirir.

Metin degerleri tek tirnakla yazilir:

```sql
'purchase'
```

Sayi degerleri tirnaksiz yazilir:

```sql
5773203
```

### Karsilastirma Operatorleri

```sql
=     esit
<>    esit degil
!=    esit degil, PostgreSQL'de calisir
>     buyuk
<     kucuk
>=    buyuk veya esit
<=    kucuk veya esit
```

Ornek:

```sql
SELECT *
FROM data_2022_oct
WHERE price > 100
LIMIT 10;
```

### AND, OR, NOT

Birden fazla kosul yazmak icin kullanilir.

```sql
SELECT *
FROM data_2022_oct
WHERE event_type = 'purchase'
  AND price > 50
LIMIT 10;
```

```sql
SELECT *
FROM data_2022_oct
WHERE event_type = 'cart'
   OR event_type = 'purchase'
LIMIT 10;
```

```sql
SELECT *
FROM data_2022_oct
WHERE NOT event_type = 'view'
LIMIT 10;
```

### IN

Bir degerin bir liste icinde olup olmadigini kontrol eder.

```sql
SELECT *
FROM data_2022_oct
WHERE event_type IN ('cart', 'purchase')
LIMIT 10;
```

Bu sunun daha kisa halidir:

```sql
WHERE event_type = 'cart'
   OR event_type = 'purchase'
```

### BETWEEN

Aralik filtresi icin kullanilir.

```sql
SELECT *
FROM data_2022_oct
WHERE price BETWEEN 10 AND 20
LIMIT 10;
```

Tarih icin:

```sql
SELECT *
FROM data_2022_oct
WHERE event_time BETWEEN '2022-10-01' AND '2022-10-07'
LIMIT 10;
```

### LIKE

Metin icinde desen aramak icin kullanilir.

```sql
SELECT *
FROM data_2022_oct
WHERE event_type LIKE 'pur%'
LIMIT 10;
```

`%`, "buraya herhangi bir sey gelebilir" demektir.

```text
'pur%' -> pur ile baslayanlar
'%cart%' -> icinde cart gecenler
```

PostgreSQL'de buyuk/kucuk harf duyarsiz arama icin `ILIKE` kullanilabilir:

```sql
SELECT *
FROM data_2022_oct
WHERE event_type ILIKE 'PUR%'
LIMIT 10;
```

### ORDER BY

Sonuclari siralamak icin kullanilir.

```sql
SELECT *
FROM data_2022_oct
ORDER BY price DESC
LIMIT 10;
```

`DESC`, buyukten kucuge siralar.

```sql
SELECT *
FROM data_2022_oct
ORDER BY price ASC
LIMIT 10;
```

`ASC`, kucukten buyuge siralar. Varsayilan zaten `ASC`tir.

Tarihe gore siralama:

```sql
SELECT *
FROM data_2022_oct
ORDER BY event_time DESC
LIMIT 10;
```

Bu en yeni 10 olayi getirir.

### LIMIT

Sonucta kac satir gelecegini sinirlar.

```sql
SELECT *
FROM data_2022_oct
LIMIT 100;
```

Buyuk tablolarda `LIMIT` cok onemlidir. Aksi halde milyonlarca satiri DBeaver'a veya
terminale getirmeye calisirsin.

### OFFSET

Ilk kac satiri atlayacagini belirtir.

```sql
SELECT *
FROM data_2022_oct
ORDER BY event_time
LIMIT 10 OFFSET 20;
```

Bu ilk 20 satiri atlar, sonraki 10 satiri getirir.

### COUNT

Satir sayar.

```sql
SELECT COUNT(*)
FROM data_2022_oct;
```

Kosullu sayim:

```sql
SELECT COUNT(*)
FROM data_2022_oct
WHERE event_type = 'purchase';
```

### SUM, AVG, MIN, MAX

Toplam, ortalama, minimum ve maksimum hesaplar.

```sql
SELECT SUM(price)
FROM data_2022_oct
WHERE event_type = 'purchase';
```

```sql
SELECT AVG(price)
FROM data_2022_oct;
```

```sql
SELECT MIN(price), MAX(price)
FROM data_2022_oct;
```

### GROUP BY

Satirlari gruplar.

Ornek: event type'a gore kac satir var?

```sql
SELECT event_type, COUNT(*)
FROM data_2022_oct
GROUP BY event_type;
```

Muhtemel sonuc:

```text
event_type        count
-----------------------
view              ...
cart              ...
purchase          ...
remove_from_cart  ...
```

Ornek: event type'a gore toplam fiyat:

```sql
SELECT event_type, SUM(price)
FROM data_2022_oct
GROUP BY event_type;
```

### HAVING

`GROUP BY` sonrasi gruplari filtreler.

`WHERE`, tek tek satirlari filtreler.

`HAVING`, gruplama sonrasi olusan gruplari filtreler.

Ornek:

```sql
SELECT user_id, COUNT(*) AS event_count
FROM data_2022_oct
GROUP BY user_id
HAVING COUNT(*) > 100
ORDER BY event_count DESC;
```

Bu 100'den fazla eventi olan kullanicilari getirir.

### AS

Kolonlara veya hesaplara takma ad verir.

```sql
SELECT COUNT(*) AS total_rows
FROM data_2022_oct;
```

```sql
SELECT event_type, COUNT(*) AS event_count
FROM data_2022_oct
GROUP BY event_type;
```

### DISTINCT

Tekrar eden degerleri tekilleştirir.

```sql
SELECT DISTINCT event_type
FROM data_2022_oct;
```

Bu event type cesitlerini getirir.

```sql
SELECT COUNT(DISTINCT user_id)
FROM data_2022_oct;
```

Bu farkli kullanici sayisini verir.

### INSERT

Tabloya yeni satir ekler.

```sql
INSERT INTO data_2022_oct (
    event_time,
    event_type,
    product_id,
    price,
    user_id,
    user_session
)
VALUES (
    '2022-10-01 00:00:00 UTC',
    'cart',
    5773203,
    2.62,
    463240011,
    '26dd6e6e-4dac-4778-8d2c-92e149dab885'
);
```

Bu projede milyonlarca satir oldugu icin tek tek `INSERT` kullanmak mantikli degildir.
CSV yuklemek icin `COPY` veya `\copy` kullanilir.

### UPDATE

Var olan satirlari gunceller.

```sql
UPDATE data_2022_oct
SET price = 3.00
WHERE product_id = 5773203;
```

Bu komut dikkatli kullanilmalidir.

Eger `WHERE` yazmazsan:

```sql
UPDATE data_2022_oct
SET price = 3.00;
```

tablodaki tum satirlarin fiyatini 3.00 yaparsin. Bu genelde buyuk hatadir.

### DELETE

Satir siler.

```sql
DELETE FROM data_2022_oct
WHERE event_type = 'view';
```

`WHERE` kullanmadan:

```sql
DELETE FROM data_2022_oct;
```

tablodaki tum satirlari siler. Dikkatli kullan.

### ALTER TABLE

Var olan tablo yapisini degistirir.

Kolon eklemek:

```sql
ALTER TABLE data_2022_oct
ADD COLUMN source_file TEXT;
```

Kolon silmek:

```sql
ALTER TABLE data_2022_oct
DROP COLUMN source_file;
```

Kolon tipini degistirmek:

```sql
ALTER TABLE data_2022_oct
ALTER COLUMN price TYPE NUMERIC(12, 2);
```

### JOIN

Iki tabloyu iliskili kolonlar uzerinden birlestirir.

Bu projede ileride `data_2022_oct` ile `items` tablosunu `product_id` uzerinden
birlestirmek isteyebilirsin.

Ornek:

```sql
SELECT
    c.event_time,
    c.event_type,
    c.product_id,
    c.price,
    i.category_code,
    i.brand
FROM data_2022_oct AS c
JOIN items AS i
  ON c.product_id = i.product_id
LIMIT 10;
```

Burada:

```text
c -> data_2022_oct tablosunun takma adi
i -> items tablosunun takma adi
```

`ON`, iki tablonun hangi sartla eslestirilecegini belirtir.

### INNER JOIN, LEFT JOIN

`JOIN` genelde `INNER JOIN` anlamina gelir. Sadece iki tabloda da eslesen satirlari
getirir.

```sql
SELECT *
FROM data_2022_oct AS c
INNER JOIN items AS i
  ON c.product_id = i.product_id;
```

`LEFT JOIN`, soldaki tablodaki tum satirlari getirir; sag tabloda eslesme yoksa sag
taraf kolonlari `NULL` olur.

```sql
SELECT *
FROM data_2022_oct AS c
LEFT JOIN items AS i
  ON c.product_id = i.product_id;
```

### NULL

`NULL`, "deger yok" demektir. Bos string veya 0 ile ayni sey degildir.

Ornek:

```text
category_code bos olabilir
```

SQL'de NULL kontrolu boyle yapilir:

```sql
SELECT *
FROM items
WHERE category_code IS NULL;
```

Yanlis:

```sql
WHERE category_code = NULL
```

Dogru:

```sql
WHERE category_code IS NULL
```

NULL olmayanlari bulmak:

```sql
WHERE category_code IS NOT NULL
```

## COPY ve \copy

Bu proje icin cok onemli.

CSV dosyasini tabloya yuklemek icin PostgreSQL'de iki farkli kullanim goreceksin:

```sql
COPY
```

ve:

```text
\copy
```

Bunlar birbirine benzer ama ayni sey degildir.

### COPY Nedir?

`COPY`, PostgreSQL server komutudur. SQL komutudur.

Ornek:

```sql
COPY data_2022_oct
FROM '/some/server/path/data_2022_oct.csv'
WITH (FORMAT csv, HEADER true);
```

Burada dosya yolu PostgreSQL server tarafindan okunur.

Docker kullaniyorsan PostgreSQL server container icinde calisir. Bu durumda path de
container icinden gorulebilir bir path olmalidir.

Yani host bilgisayarindaki:

```text
../subject/customer/data_2022_oct.csv
```

dosyasini container icindeki PostgreSQL server dogrudan goremez. Bunun icin dosyayi
container'a mount etmek veya kopyalamak gerekir.

### \copy Nedir?

`\copy`, psql komutudur. SQL degildir.

Mevcut dosyanda su var:

```sql
\copy data_2022_oct FROM '../subject/customer/data_2022_oct.csv' WITH (FORMAT csv, HEADER true);
```

Bu komut psql tarafindan calistirilir. Dosyayi psql client okur, sonra veriyi PostgreSQL
server'a gonderir.

Bu yuzden `\copy`, Docker kullandiginda cok pratiktir:

- CSV dosyasi host makinede durur.
- `psql` host makinede calisir.
- `psql` dosyayi okur.
- Veriyi PostgreSQL container'ina gonderir.

### COPY ve \copy Farki

Ozet tablo:

```text
COPY
  SQL komutudur.
  Dosyayi PostgreSQL server okur.
  Path server tarafindan gorulebilir olmalidir.
  Docker'da dosya container icinde veya mount edilmis olmalidir.

\copy
  psql meta-komutudur.
  Dosyayi psql client okur.
  Path komutu calistirdigin terminale gore yorumlanir.
  Docker kullanan local projelerde genelde daha pratiktir.
```

### FORMAT csv

```sql
WITH (FORMAT csv, HEADER true)
```

`FORMAT csv`, dosya formatinin CSV oldugunu soyler.

CSV:

```text
comma-separated values
```

Yani virgulle ayrilmis degerler.

### HEADER true

```sql
HEADER true
```

CSV'nin ilk satiri veri degil, kolon adlari demektir.

Customer CSV'nin ilk satiri:

```text
event_time,event_type,product_id,price,user_id,user_session
```

Bu satir tabloya veri olarak eklenmemelidir. `HEADER true` bunu soyler.

### \copy Komutunu Calistirma

`table.sql` dosyasini psql icinde calistirmak icin ex02 klasorundeyken:

```bash
psql -U acosgun -d piscineds -h localhost -W -f table.sql
```

Burada:

```text
-f table.sql
```

psql'e "bu dosyadaki komutlari calistir" demektir.

`table.sql` icindeki path:

```text
../subject/customer/data_2022_oct.csv
```

ex02 klasorunden bakinca dogrudur:

```text
ex02/../subject/customer/data_2022_oct.csv
```

Bu da:

```text
subject/customer/data_2022_oct.csv
```

dosyasina gider.

## Soru 3: Terminalden Veritabanina Baglandim, En Sik Hangi Komutlari Kullanacagim?

Terminalden baglanmak icin:

```bash
psql -U acosgun -d piscineds -h localhost -W
```

Sifre:

```text
mysecretpassword
```

Baglaninca prompt soyle gorunur:

```text
piscineds=#
```

Bu noktadan sonra hem SQL komutlari hem de psql komutlari kullanabilirsin.

## En Sik Kullanilan psql Komutlari

### \l

Database'leri listeler.

```text
\l
```

### \c

Baska database'e baglanir.

```text
\c piscineds
```

### \dt

Mevcut schema'daki tablolari listeler.

```text
\dt
```

Eger tabloyu yeni olusturduysan ve gormek istiyorsan ilk kullanacagin komutlardan biri
budur.

### \dt public.*

`public` schema'sindaki tablolari listeler.

```text
\dt public.*
```

### \d table_name

Tablo yapisini gosterir.

```text
\d data_2022_oct
```

Kolon adlarini ve veri tiplerini gorursun.

### \d+ table_name

Tablo yapisini daha detayli gosterir.

```text
\d+ data_2022_oct
```

Boyut gibi ekstra bilgiler de verebilir.

### \du

PostgreSQL kullanicilarini/rollerini listeler.

```text
\du
```

### \conninfo

Hangi database'e, hangi kullaniciyla, hangi hosttan bagli oldugunu gosterir.

```text
\conninfo
```

Bu cok kullanislidir. Yanlis database'e baglanip tabloyu baska yerde arama problemini
onler.

### \i file.sql

Bir SQL dosyasini psql icinden calistirir.

```text
\i ex02/table.sql
```

Eger zaten `ex02` klasorundeysen:

```text
\i table.sql
```

### \copy

CSV import/export icin kullanilir.

```text
\copy data_2022_oct FROM '../subject/customer/data_2022_oct.csv' WITH (FORMAT csv, HEADER true);
```

### \timing

Sorgularin kac ms/saniye surdugunu gosterir.

```text
\timing
```

Tekrar yazarsan kapatir.

Buyuk veriyle calisirken cok faydalidir.

### \x

Expanded display modunu acar/kapatir.

```text
\x
```

Satirda cok kolon varsa sonucu daha okunabilir gosterir.

### \q

psql'den cikar.

```text
\q
```

## En Sik Kullanilan SQL Komutlari ve Anahtar Kelimeler

### CREATE TABLE

Tablo olusturur.

```sql
CREATE TABLE data_2022_oct (
    event_time TIMESTAMPTZ,
    event_type VARCHAR(32),
    product_id INTEGER,
    price NUMERIC(10, 2),
    user_id BIGINT,
    user_session UUID
);
```

### DROP TABLE IF EXISTS

Tablo varsa siler.

```sql
DROP TABLE IF EXISTS data_2022_oct;
```

Script tekrar calistirilabilir olsun istiyorsan kullanislidir.

### SELECT

Veri okur.

```sql
SELECT *
FROM data_2022_oct
LIMIT 10;
```

### FROM

Hangi tablodan veri okunacagini belirtir.

```sql
FROM data_2022_oct
```

### WHERE

Satir filtreler.

```sql
SELECT *
FROM data_2022_oct
WHERE event_type = 'purchase'
LIMIT 10;
```

### ORDER BY

Siralar.

```sql
SELECT *
FROM data_2022_oct
ORDER BY event_time DESC
LIMIT 10;
```

### LIMIT

Satir sayisini sinirlar.

```sql
SELECT *
FROM data_2022_oct
LIMIT 100;
```

### GROUP BY

Gruplama yapar.

```sql
SELECT event_type, COUNT(*)
FROM data_2022_oct
GROUP BY event_type;
```

### HAVING

Gruplanmis sonuclari filtreler.

```sql
SELECT user_id, COUNT(*) AS event_count
FROM data_2022_oct
GROUP BY user_id
HAVING COUNT(*) > 100;
```

### DISTINCT

Tekil degerleri getirir.

```sql
SELECT DISTINCT event_type
FROM data_2022_oct;
```

### INSERT INTO

Satir ekler.

```sql
INSERT INTO data_2022_oct (
    event_time,
    event_type,
    product_id,
    price,
    user_id,
    user_session
)
VALUES (
    '2022-10-01 00:00:00 UTC',
    'view',
    123,
    9.99,
    456,
    '26dd6e6e-4dac-4778-8d2c-92e149dab885'
);
```

### UPDATE

Satir gunceller.

```sql
UPDATE data_2022_oct
SET event_type = 'purchase'
WHERE user_session = '26dd6e6e-4dac-4778-8d2c-92e149dab885';
```

### DELETE FROM

Satir siler.

```sql
DELETE FROM data_2022_oct
WHERE event_type = 'view';
```

### ALTER TABLE

Tablo yapisini degistirir.

```sql
ALTER TABLE data_2022_oct
ADD COLUMN imported_at TIMESTAMPTZ;
```

### JOIN

Tablolari birlestirir.

```sql
SELECT
    c.event_time,
    c.product_id,
    c.price,
    i.brand
FROM data_2022_oct AS c
JOIN items AS i
  ON c.product_id = i.product_id
LIMIT 10;
```

### CREATE INDEX

Sorgulari hizlandirmak icin indeks olusturur.

```sql
CREATE INDEX idx_data_2022_oct_product_id
ON data_2022_oct (product_id);
```

Indeks, kitap sonundaki dizin gibi dusunulebilir. PostgreSQL belirli degerleri daha
hizli bulabilir.

Ama her kolona indeks eklemek iyi fikir degildir. Indeksler disk kaplar ve veri ekleme
islemlerini yavaslatabilir.

### TRUNCATE

Tablodaki tum satirlari hizlica siler, tablo yapisini korur.

```sql
TRUNCATE TABLE data_2022_oct;
```

`DROP TABLE` tabloyu komple siler.

`TRUNCATE` tabloyu silmez, sadece icindeki veriyi bosaltir.

## Kullanacagin Pratik Sorgu Ornekleri

### Ilk 10 satiri gor

```sql
SELECT *
FROM data_2022_oct
LIMIT 10;
```

### Toplam satir sayisini bul

```sql
SELECT COUNT(*)
FROM data_2022_oct;
```

### Kolon tiplerini terminalden gor

```text
\d data_2022_oct
```

### Event tiplerini listele

```sql
SELECT DISTINCT event_type
FROM data_2022_oct;
```

### Her event tipinden kac tane var?

```sql
SELECT event_type, COUNT(*) AS count
FROM data_2022_oct
GROUP BY event_type
ORDER BY count DESC;
```

### Sadece satin alma olaylarini getir

```sql
SELECT *
FROM data_2022_oct
WHERE event_type = 'purchase'
LIMIT 100;
```

### En pahali 20 olayi getir

```sql
SELECT *
FROM data_2022_oct
ORDER BY price DESC
LIMIT 20;
```

### Belirli kullanicinin hareketlerini getir

```sql
SELECT *
FROM data_2022_oct
WHERE user_id = 463240011
ORDER BY event_time;
```

### Gunluk event sayisi

```sql
SELECT
    event_time::date AS day,
    COUNT(*) AS event_count
FROM data_2022_oct
GROUP BY day
ORDER BY day;
```

Buradaki:

```sql
event_time::date
```

PostgreSQL type cast ifadesidir. `TIMESTAMPTZ` degerini sadece tarih kismina cevirir.

### Gunluk purchase sayisi

```sql
SELECT
    event_time::date AS day,
    COUNT(*) AS purchase_count
FROM data_2022_oct
WHERE event_type = 'purchase'
GROUP BY day
ORDER BY day;
```

### Gunluk toplam purchase tutari

```sql
SELECT
    event_time::date AS day,
    SUM(price) AS revenue
FROM data_2022_oct
WHERE event_type = 'purchase'
GROUP BY day
ORDER BY day;
```

## SQL Yazarken Dikkat Edilecek Noktalar

### Noktali Virgul

SQL komutlari genelde `;` ile biter.

```sql
SELECT * FROM data_2022_oct LIMIT 10;
```

psql'de `;` yazmazsan komut bitmedi sanilir ve alt satira gecilir.

### Tek Tirnak ve Cift Tirnak

Metin degerleri tek tirnakla yazilir:

```sql
WHERE event_type = 'purchase'
```

Cift tirnak ise identifier, yani tablo/kolon adi icin kullanilir:

```sql
SELECT "event_type"
FROM "data_2022_oct";
```

Genelde tablo ve kolon adlarini kucuk harf + alt cizgi ile yazarsan cift tirnaga
ihtiyacin olmaz:

```text
data_2022_oct
event_type
product_id
```

Bu iyi pratiktir.

### Buyuk/Kucuk Harf

SQL anahtar kelimeleri buyuk veya kucuk yazilabilir:

```sql
select * from data_2022_oct;
```

calisir.

Ama okunabilirlik icin genelde anahtar kelimeleri buyuk yazmak tercih edilir:

```sql
SELECT *
FROM data_2022_oct;
```

### NULL ile Karsilastirma

Yanlis:

```sql
WHERE brand = NULL
```

Dogru:

```sql
WHERE brand IS NULL
```

NULL olmayan:

```sql
WHERE brand IS NOT NULL
```

### Buyuk Tablolarda LIMIT Kullan

Bu projede tablolar milyonlarca satir. DBeaver veya psql icinde:

```sql
SELECT *
FROM data_2022_oct;
```

calistirmak cok buyuk sonuc uretir.

Baslangicta hep:

```sql
LIMIT 10
```

veya:

```sql
LIMIT 100
```

kullan.

### Scriptleri Tekrar Calistirilabilir Yap

Bir SQL dosyasini tekrar tekrar calistiracaksan basina sunu koymak faydali olabilir:

```sql
DROP TABLE IF EXISTS data_2022_oct;
```

Sonra tabloyu olustur:

```sql
CREATE TABLE data_2022_oct (...);
```

Bu sayede "tablo zaten var" hatasi almazsin.

Ama dikkat: Bu tabloyu ve icindeki veriyi siler. Import yeniden yapilacaksa uygundur.

## ex02/table.sql Dosyasini Daha Dayanikli Yapmak Icin

Mevcut dosyan calisir:

```sql
CREATE TABLE data_2022_oct (
    event_time TIMESTAMPTZ,
    event_type VARCHAR(32),
    product_id INTEGER,
    price NUMERIC(10, 2),
    user_id BIGINT,
    user_session UUID
);

\copy data_2022_oct FROM '../subject/customer/data_2022_oct.csv' WITH (FORMAT csv, HEADER true);
```

Tekrar calistirabilir hale getirmek icin su sekle getirilebilir:

```sql
DROP TABLE IF EXISTS data_2022_oct;

CREATE TABLE data_2022_oct (
    event_time TIMESTAMPTZ,
    event_type VARCHAR(32),
    product_id INTEGER,
    price NUMERIC(10, 2),
    user_id BIGINT,
    user_session UUID
);

\copy data_2022_oct
FROM '../subject/customer/data_2022_oct.csv'
WITH (FORMAT csv, HEADER true);
```

Bu haliyle:

1. Eski tablo varsa siler.
2. Tabloyu yeniden olusturur.
3. CSV'yi yeniden yukler.

Subject acisindan kolon isimleri ve tipleri ayni kaldigi icin mantik bozulmaz.

## Kisa Komut Ozeti

Terminalden baglan:

```bash
psql -U acosgun -d piscineds -h localhost -W
```

SQL dosyasi calistir:

```bash
psql -U acosgun -d piscineds -h localhost -W -f ex02/table.sql
```

Tablolari listele:

```text
\dt
```

Tablo yapisini gor:

```text
\d data_2022_oct
```

Ilk 10 satiri getir:

```sql
SELECT *
FROM data_2022_oct
LIMIT 10;
```

Satir say:

```sql
SELECT COUNT(*)
FROM data_2022_oct;
```

Event tiplerini say:

```sql
SELECT event_type, COUNT(*)
FROM data_2022_oct
GROUP BY event_type;
```

psql'den cik:

```text
\q
```

