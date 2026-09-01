# Exercise 01: Show Me Your DB

Bu egzersizde veritabanındaki tabloları, şemaları ve verileri görselleştirmek ve kolayca yönetmek amacıyla **DBeaver Community Edition** tercih edilmiştir.

---

## 1. DBeaver Nedir?

**DBeaver**, geliştiriciler ve veritabanı yöneticileri için geliştirilmiş, açık kaynaklı, platformlar arası (Linux, macOS, Windows) grafiksel bir veritabanı yönetim aracıdır (GUI).

### Neden DBeaver?
- **Çoklu Platform Desteği:** Linux üzerinde hafif ve kararlı çalışır.
- **Zengin Veri Arayüzü (Data Grid):** Tablolardaki milyonlarca satırı sayfalar halinde hızlıca görüntüler.
- **Hızlı Filtreleme ve Arama (ID Lookup):** Belirli bir `user_id`, `product_id` veya `user_session` değerini tek tıkla arama/filtreleme imkanı sunar (Subject kriteri).
- **ER Diyagramları:** Tablo ilişkilerini ve şemaları görselleştirir.
- **Entegre SQL Editörü:** Otomatik tamamlama (autocomplete) ve sorgu yürütme kolaylığı sağlar.

---

## 2. Bağlantı Bilgileri (Connection Settings)

DBeaver üzerinden `piscineds` veritabanına bağlanmak için kullanılan parametreler:

| Parametre | Değer |
|---|---|
| **Veritabanı Türü** | PostgreSQL |
| **Host / Sunucu** | `localhost` veya `127.0.0.1` |
| **Port** | `5432` |
| **Database** | `piscineds` |
| **Username** | `*(42 intra login)* |
| **Password** | `mysecretpassword` |

---

## 3. Adım Adım Kurulum ve Bağlantı

### Adım 1: Yeni Bağlantı Oluşturma
1. DBeaver'ı açın.
2. Sol üstteki **New Database Connection** (fiş simgesi) butonuna tıklayın.
3. Listeden **PostgreSQL** seçeneğini seçip **Next** butonuna basın.

### Adım 2: Parametreleri Girme
- **Host:** `localhost`
- **Port:** `5432`
- **Database:** `piscineds`
- **Authentication:** Database Native
- **Username:** `*(42 intra login)*`
- **Password:** `mysecretpassword`

### Adım 3: Bağlantıyı Test Etme ve Kaydetme
1. Sol alttaki **Test Connection** butonuna basarak Docker üzerindeki PostgreSQL container'ının erişilebilir olduğunu doğrulayın.
2. İlk bağlantıda PostgreSQL sürücüsü (JDBC Driver) eksikse DBeaver otomatik indirme önerir, **Download** seçeneğini onaylayın.
3. **Finish** butonuna basarak bağlantıyı kaydedin.

---

## 4. Temel Kullanım & İnceleme

### Tabloları Görüntüleme
- Sol paneldeki gezginden:  
  `piscineds` $\rightarrow$ `Schemas` $\rightarrow$ `public` $\rightarrow$ `Tables` yolunu izleyin.
- Tablolar: `data_2022_oct`, `data_2022_nov`, `data_2022_dec`, `data_2023_jan`, `items`.

### Verileri İnceleme ve ID Arama
1. İlgili tablonun üzerine çift tıklayın ve üst kısımdaki **Data** sekmesine geçin.
2. **Kayıt Arama (Filtreleme):** Kolon başlığının altındaki filtre satırına aramak istediğiniz değeri yazın (Örn: `product_id = 5773203` veya `user_id = 463240011`).
3. **Sıralama:** Kolon başlığına tıklayarak verileri tarihe (`event_time`) veya fiyata (`price`) göre artan/azalan sıralayabilirsiniz.

### SQL Sorgusu Çalıştırma
- `SQL Editor` $\rightarrow$ `New SQL Script` (veya `F3`) ile yeni sorgu penceresi açıp doğrudan SQL sorguları çalıştırabilirsiniz (`Ctrl + Enter`).

