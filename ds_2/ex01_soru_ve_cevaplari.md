# 12. Ex01 Soru ve Cevapları

## Sorgumuz

```sql
SELECT
    TO_CHAR(DATE_TRUNC('month', event_time), 'Mon') AS month,
    COUNT(DISTINCT user_id) AS customer_count,
    SUM(price) AS total_sales
FROM customers
WHERE event_type = 'purchase'
  AND event_time >= '2022-10-01'
  AND event_time <  '2023-03-01'
GROUP BY DATE_TRUNC('month', event_time)
ORDER BY DATE_TRUNC('month', event_time);
```

Bu sorgunun amacı, `customers` tablosundaki `purchase` event'lerini Ekim 2022–Şubat 2023 arasındaki aylara göre gruplayarak her ay için ay adını, farklı müşteri sayısını ve toplam satış tutarını bulmaktır.

## 1. SELECT

```sql
SELECT
```

`SELECT`, sorgunun sonucunda hangi bilgileri görmek istediğimizi belirtir. Burada üç sonuç kolonu oluşturuyoruz:

```text
month
customer_count
total_sales
```

---

## 2. `TO_CHAR(DATE_TRUNC('month', event_time), 'Mon') AS month`

Bu ifadeyi iki aşamada düşünmek kolaydır:

```text
event_time
    ↓
DATE_TRUNC()
    ↓
ayın başlangıcı
    ↓
TO_CHAR()
    ↓
"Oct"
```

Önce:

```sql
DATE_TRUNC('month', event_time)
```

çalışır. Sonra sonucu:

```sql
TO_CHAR(..., 'Mon')
```

ile metne çeviririz.

---

## 3. DATE_TRUNC nedir?

`DATE_TRUNC`, date truncate yani tarihi belirli bir hassasiyet seviyesine kadar kırpmak anlamında düşünülebilir.

Genel kullanım:

```sql
DATE_TRUNC('birim', tarih_zaman_değeri)
```

Örneğin:

```sql
DATE_TRUNC('month', '2022-10-17 14:35:42'::timestamp)
```

sonucu:

```text
2022-10-01 00:00:00
```

olur.

Yani ay dışındaki daha küçük zaman parçaları başlangıç değerlerine çekilir.

### Yaygın birimler

```sql
DATE_TRUNC('year', event_time)
```

```text
2022-10-17 14:35:42
→ 2022-01-01 00:00:00
```

```sql
DATE_TRUNC('quarter', event_time)
```

```text
2022-10-17
→ 2022-10-01
```

```sql
DATE_TRUNC('month', event_time)
```

```text
2022-10-17 14:35:42
→ 2022-10-01 00:00:00
```

```sql
DATE_TRUNC('week', event_time)
```

Haftanın başlangıcına kırpar. PostgreSQL'de haftanın başlangıcı Pazartesi'dir.

```sql
DATE_TRUNC('day', event_time)
```

```text
2022-10-17 14:35:42
→ 2022-10-17 00:00:00
```

```sql
DATE_TRUNC('hour', event_time)
```

```text
2022-10-17 14:35:42
→ 2022-10-17 14:00:00
```

```sql
DATE_TRUNC('minute', event_time)
```

```text
2022-10-17 14:35:42
→ 2022-10-17 14:35:00
```

```sql
DATE_TRUNC('second', event_time)
```

```text
2022-10-17 14:35:42.837
→ 2022-10-17 14:35:42
```

Önemli fikir:

> `DATE_TRUNC` tarihi metne çevirmez; tarih/zaman değerini yine tarih/zaman olarak döndürür.

---

## 4. DATE_TRUNC burada neden gerekli?

Örneğin elimizde:

```text
2022-10-01 10:15
2022-10-01 14:20
2022-10-02 09:30
2022-10-17 18:00
2022-10-31 23:50
```

olsun.

Bunları "Ekim 2022" altında toplamak istiyoruz.

```sql
DATE_TRUNC('month', event_time)
```

hepsini:

```text
2022-10-01 00:00:00
```

değerine indirger.

Dolayısıyla:

```sql
GROUP BY DATE_TRUNC('month', event_time)
```

hepsini aynı gruba koyabilir.

---

## 5. TO_CHAR nedir?

`TO_CHAR`, tarih/saat veya sayısal değerleri belirli bir formatta **text** haline getirmek için kullanılır.

Genel kullanım:

```sql
TO_CHAR(değer, 'format')
```

Örneğin:

```sql
TO_CHAR(event_time, 'Mon')
```

→ `Oct`

```sql
TO_CHAR(event_time, 'Month')
```

→ `October`

```sql
TO_CHAR(event_time, 'YYYY')
```

→ `2022`

```sql
TO_CHAR(event_time, 'YYYY-MM-DD')
```

→ `2022-10-17`

```sql
TO_CHAR(event_time, 'YYYY-MM-DD HH24:MI:SS')
```

→ `2022-10-17 14:35:42`

### Yaygın formatlar

| Format | Anlamı | Örnek |
|---|---|---|
| `YYYY` | 4 haneli yıl | `2022` |
| `YY` | 2 haneli yıl | `22` |
| `MM` | 2 haneli ay | `10` |
| `Mon` | Kısa ay adı | `Oct` |
| `Month` | Tam ay adı | `October` |
| `DD` | Gün | `17` |
| `Day` | Gün adı | `Monday` |
| `HH24` | 24 saatlik saat | `14` |
| `MI` | Dakika | `35` |
| `SS` | Saniye | `42` |

Bunlar birleştirilebilir:

```sql
TO_CHAR(event_time, 'DD Mon YYYY')
```

→

```text
17 Oct 2022
```

Önemli fark:

```text
DATE_TRUNC → tarih/zaman değerini kırpar
TO_CHAR    → değeri metne dönüştürür
```

---

## 6. `AS month`

```sql
AS month
```

hesapladığımız ifadeye sonuç kolonunda `month` adını verir.

Örneğin:

```sql
TO_CHAR(...) AS month
```

sonucunda kolon adı:

```text
month
```

olur.

Aynı şekilde:

```sql
COUNT(DISTINCT user_id) AS customer_count
SUM(price) AS total_sales
```

ifadeleri de sonuç kolonlarına isim verir.

---

## 7. COUNT(DISTINCT user_id)

```sql
COUNT(DISTINCT user_id) AS customer_count
```

Bir ay içerisindeki farklı kullanıcıları sayar.

Örneğin:

```text
user_id
-------
U1
U1
U1
U2
U2
U3
```

varsa:

```sql
COUNT(DISTINCT user_id)
```

sonucu:

```text
3
```

olur.

---

## 8. SUM(price)

```sql
SUM(price) AS total_sales
```

Her ay grubundaki `price` değerlerini toplar.

Örneğin:

```text
10.00
25.50
30.00
```

için:

```sql
SUM(price)
```

→ `65.50`

olur.

---

## 9. FROM customers

```sql
FROM customers
```

verilerin hangi tablodan alınacağını belirtir.

Buradaki kaynak tablo:

```text
customers
```

tablosudur.

---

## 10. WHERE

```sql
WHERE event_type = 'purchase'
```

yalnızca `purchase` event'lerini sorguya dahil eder.

Mantıksal olarak:

```text
customers
    ↓
purchase kayıtlarını filtrele
    ↓
GROUP BY
    ↓
SUM / COUNT
```

şeklinde düşünebiliriz.

---

## 11. Tarih filtresi

```sql
AND event_time >= '2022-10-01'
AND event_time <  '2023-03-01'
```

şu aralığı ifade eder:

```text
2022-10-01 00:00:00 dahil
          ↓
Ekim
Kasım
Aralık
Ocak
Şubat
          ↓
2023-03-01 00:00:00 hariç
```

Bu kullanım Şubat'ın 28 veya 29 gün çekip çekmediğini bizim hesaplamamıza gerek bırakmaz.

Özellikle timestamp filtrelerinde:

```sql
>= başlangıç
< sonraki dönemin başlangıcı
```

kalıbı güvenlidir.

Örneğin:

```sql
event_time <= '2023-02-28'
```

yazmak sorunlu olabilir; çünkü `'2023-02-28'` timestamp bağlamında günün başlangıcı olan `2023-02-28 00:00:00` olarak yorumlanabilir. Böylece 28 Şubat günü içindeki daha sonraki saatler kaçırılabilir.

---

## 12. GROUP BY

```sql
GROUP BY DATE_TRUNC('month', event_time)
```

aynı aya ait kayıtları aynı gruba koyar.

Örneğin:

```text
2022-10-01 10:00
2022-10-05 14:00
2022-10-17 09:00
```

için `DATE_TRUNC('month', event_time)`:

```text
2022-10-01 00:00:00
```

olacağından bu kayıtlar aynı gruptadır.

Sonra her grup için:

```sql
COUNT(DISTINCT user_id)
SUM(price)
```

hesaplanır.

Dolayısıyla:

```text
GROUP BY → grupları belirler
SUM/COUNT → her grubun değerini hesaplar
```

---

## 13. ORDER BY

```sql
ORDER BY DATE_TRUNC('month', event_time)
```

oluşan sonuçları kronolojik sıraya koyar.

Örneğin:

```text
2022-10-01
2022-11-01
2022-12-01
2023-01-01
2023-02-01
```

sırasında gösterilir.

Ancak kullanıcıya gösterilen değer `TO_CHAR(..., 'Mon')` nedeniyle:

```text
Oct
Nov
Dec
Jan
Feb
```

olur.

Buradaki önemli fikir:

> Sıralama gerçek tarih üzerinden, gösterim ise `TO_CHAR` ile yapılmış metin üzerinden gerçekleşir.

Bu nedenle `ORDER BY month` yerine tarih ifadesini kullanmak daha güvenlidir.

---

# 14. Soru 2 — GROUP BY ve ORDER BY neden aşağıda?

SQL'in yazım sırası genel olarak:

```text
SELECT
FROM
WHERE
GROUP BY
HAVING
ORDER BY
LIMIT
```

şeklindedir.

Dolayısıyla `GROUP BY` ve `ORDER BY` satırlarının `SUM(price)` satırının altında olması doğrudur.

Ancak bu:

> `SELECT` önce çalışıyor, sonra `GROUP BY` çalışıyor

anlamına gelmez.

Öğrenmek için sorgunun **mantıksal çalışma sırasını** kabaca şöyle düşünebiliriz:

```text
FROM
  ↓
WHERE
  ↓
GROUP BY
  ↓
aggregate hesaplamaları (SUM, COUNT...)
  ↓
HAVING
  ↓
SELECT
  ↓
ORDER BY
  ↓
LIMIT
```

Gerçek PostgreSQL execution planı optimizer tarafından farklılaştırılabilir; bu liste SQL'in öğrenilmesi için kullanılan mantıksal sıradır.

---

# 15. GROUP BY ile ORDER BY aynı şey değildir

Bunları özellikle ayırmak gerekir.

### GROUP BY

```sql
GROUP BY DATE_TRUNC('month', event_time)
```

şunu sorar:

> Hangi kayıtlar aynı grubun içinde olacak?

### ORDER BY

```sql
ORDER BY DATE_TRUNC('month', event_time)
```

şunu sorar:

> Oluşan sonuç gruplarını hangi sırada göstereyim?

Örneğin:

```text
GROUP BY
→ Ekim, Kasım, Aralık, Ocak, Şubat gruplarını oluştur

ORDER BY
→ Bu grupları kronolojik sırada göster
```

---

# 16. Sorgunun tamamını insan diliyle okuyalım

```sql
SELECT
    TO_CHAR(DATE_TRUNC('month', event_time), 'Mon') AS month,
    COUNT(DISTINCT user_id) AS customer_count,
    SUM(price) AS total_sales
FROM customers
WHERE event_type = 'purchase'
  AND event_time >= '2022-10-01'
  AND event_time <  '2023-03-01'
GROUP BY DATE_TRUNC('month', event_time)
ORDER BY DATE_TRUNC('month', event_time);
```

Bunu Türkçe olarak şöyle okuyabiliriz:

> `customers` tablosundan 1 Ekim 2022 dahil olmak üzere 1 Mart 2023'e kadar olan `purchase` event'lerini al.
>
> Bunları aylarına göre grupla.
>
> Her ay için farklı `user_id` sayısını hesapla.
>
> Her ayın `price` değerlerini topla.
>
> Ayı `Oct`, `Nov`, `Dec` gibi göster.
>
> Sonuçları gerçek tarih sırasına göre göster.

Örneğin:

```text
month | customer_count | total_sales
------+----------------+------------
Oct   | 120            | 4500.00
Nov   | 135            | 5100.00
Dec   | 180            | 7200.00
Jan   | 150            | 6100.00
Feb   | 165            | 6800.00
```

---

# 17. Bu sorgudan çıkarılması gereken ana fikir

Bu sorguda dört yapının görevini birbirinden ayırmak önemlidir:

```text
DATE_TRUNC
    ↓
Zamanı belirli bir seviyeye indirger.
"Bu event hangi aya ait?"

GROUP BY
    ↓
Aynı aya ait event'leri aynı gruba koyar.

TO_CHAR
    ↓
Tarihi kullanıcıya göstermek istediğimiz metin biçimine çevirir.
"Bu ayı Oct olarak göster."

ORDER BY
    ↓
Oluşan sonuçları hangi sırada göstereceğini belirler.
```

Bu ayrımı oturttuğunda sorgunun tamamını okumak çok daha kolay hale gelir.
