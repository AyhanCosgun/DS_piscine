# ds_0 - Creation of a DB: Subject Aciklamasi

Bu proje, 42 Data Science Piscine icindeki ilk veritabani projesidir. Ana fikir sudur:
elinde internetten satis yapan bir sirketin CSV dosyalari var; bu dosyalari PostgreSQL
veritabanina duzgun sekilde koyman gerekiyor. Sonraki modullerde bu verileri temizleme,
donusturme ve analiz etme isleri gelecegi icin, burada veriyi dogru saklamak cok onemli.

Bu dosya `ds_0.pdf` subject dosyasina ve mevcut klasordeki CSV dosyalarina gore
hazirlandi.

## Mevcut Dosyalar

Ana dizinde subject PDF'i var:

```text
ds_0.pdf
```

Veri dosyalari ise su sekilde:

```text
subject/customer/data_2022_oct.csv
subject/customer/data_2022_nov.csv
subject/customer/data_2022_dec.csv
subject/customer/data_2023_jan.csv
subject/item/item.csv
```

Customer CSV dosyalarinin kolonlari ayni:

```text
event_time,event_type,product_id,price,user_id,user_session
```

Item CSV dosyasinin kolonlari:

```text
product_id,category_id,category_code,brand
```

Customer dosyalari cok buyuk. Mevcut satir sayilari yaklasik olarak soyle:

```text
data_2022_oct.csv  -> 4.102.284 satir
data_2022_nov.csv  -> 4.635.838 satir
data_2022_dec.csv  -> 3.533.287 satir
data_2023_jan.csv  -> 4.264.753 satir
item.csv           ->   109.580 satir
```

Bu yuzden bu proje sadece "bir tablo olusturayim" projesi degil; buyuk CSV dosyalarini
veritabanina dogru, tekrar calistirilabilir ve sonradan analiz edilebilir sekilde alma
projesidir.

## Genel Kurallar

Subject'e gore projeyi cluster bilgisayarinda, sanal makinede veya dogrudan kendi
makinendeki araclarla yapabilirsin. Onemli olan degerlendirme sirasinda her seyin
calisir olmasidir.

Genel beklentiler:

- Gerekli yazilimlar degerlendirmeden once kurulu ve ayarli olmali.
- Calismalar git reposuna konmali; sadece repodaki dosyalar degerlendirilir.
- Klasor ve dosya isimleri subject'teki isimlerle uyumlu olmali.
- Proje degerlendirmesi, degerlendirilen kisinin bilgisayarinda yapilir.

Bu son madde onemli: Veritabanini sadece kendi kafanda calistirmak yetmez. Peer evaluator
senin bilgisayarinda ya da senin kurulumunda bu isleri gorebilmeli. Bu yuzden kurulumun,
komutlarin ve dosya isimlerin net olmali.

## Subject Basindaki Uyari Ne Demek?

Subject'te su uyari var:

```text
Be careful with this "piscine". Even if you manage to validate a module,
you may be stuck later if you haven’t cleaned up or stored your data properly.
```

Burada vurgulanan sey su:

Bu piscine birbirinden kopuk tek tek egzersizlerden olusan bir seri gibi gorunebilir,
ama aslinda sonraki moduller onceki modullerde hazirladigin veriye dayanabilir. Yani
bugun veriyi veritabanina yanlis tiplerle, eksik kolonlarla, bozuk isimlerle veya kirli
sekilde koyarsan, bugunku modulu gecsen bile sonraki modullerde analiz, temizleme veya
join islemleri yaparken takilabilirsin.

Ornekler:

- `event_time` kolonunu metin olarak saklarsan, ileride tarihe gore filtreleme ve siralama
  zorlasir.
- `price` kolonunu metin olarak saklarsan, toplam satis tutari gibi hesaplamalar problemli
  olur.
- `product_id` ile `items.product_id` tipleri uyumsuz olursa, ileride iki tabloyu
  birlestirmek zorlasir.
- CSV dosyalarini tekrar tekrar import edip ayni veriyi cogaltirsan, analiz sonuclari
  yanlis cikar.
- Kolon isimlerini CSV'deki gibi birebir kullanmazsan, otomatik scriptler veya sonraki
  subject beklentileri bozulabilir.

Kisacasi bu uyari "sadece validasyonu gecmeye calisma; veriyi uzun vadede kullanilabilir
sekilde sakla" demek. Bu projede duzenli tablo isimleri, uygun veri tipleri, tekrar
calistirilabilir scriptler ve temiz import mantigi cok onemli.

## Temel Kavramlar

### Veritabani Nedir?

Veritabani, veriyi duzenli tablolarda saklayan sistemdir. CSV dosyasi da tablo gibi
gorunur ama veritabani CSV'den daha gucludur:

- Veriyi tiplerle saklar: tarih, sayi, metin, UUID gibi.
- Buyuk veride sorgu calistirmayi kolaylastirir.
- Tablolar arasinda iliski kurmaya izin verir.
- Filtreleme, siralama, gruplama ve hesaplama islemlerini SQL ile yaparsin.

Bu projede kullanilacak sistem PostgreSQL'dir.

### PostgreSQL Nedir?

PostgreSQL acik kaynakli bir iliskisel veritabani sistemidir. Iliskisel demek, verinin
tablolar halinde tutulmasi ve tablolar arasinda mantikli baglantilar kurulabilmesi
demektir.

Bu projede ornegin:

- `data_2022_oct` satis/olay verilerini tutar.
- `items` urun bilgilerini tutar.
- Iki tabloda da `product_id` oldugu icin ileride bu tablolar birlestirilebilir.

### SQL Nedir?

SQL, veritabaniyla konusmak icin kullanilan dildir.

Ornek:

```sql
SELECT *
FROM data_2022_oct
LIMIT 10;
```

Bu komut `data_2022_oct` tablosundan ilk 10 satiri getirir.

### Tablo, Kolon, Satir

CSV'deki her dosya veritabaninda bir tabloya donusebilir.

CSV:

```text
event_time,event_type,product_id,price,user_id,user_session
2022-10-01 00:00:00 UTC,cart,5773203,2.62,463240011,26dd...
```

Veritabaninda:

- Tablo adi: `data_2022_oct`
- Kolonlar: `event_time`, `event_type`, `product_id`, `price`, `user_id`, `user_session`
- Satir: Her bir olay kaydi

## Exercise 00 - Create Postgres DB

### Subject Beklentisi

Teslim klasoru:

```text
ex00/
```

Teslim edilecek dosyalardan biri:

```text
docker-compose.yml
setup.sh
VM-instructions.txt
```

Allowed functions:

```text
All
```

Beklenen PostgreSQL ayarlari:

```text
username: senin student login'in
database: piscineds
password: mysecretpassword
```

Subject su komutla baglanabilmeyi istiyor:

```bash
psql -U your_login -d piscineds -h localhost -W
```

Sifre:

```text
mysecretpassword
```

Baglanti basarili olunca prompt su sekilde gorunmeli:

```text
piscineds=#
```

### Hangi Teslim Secenegi Daha Mantikli?

Uc secenek var:

1. `docker-compose.yml`
2. `setup.sh`
3. `VM-instructions.txt`

Bunlar arasinda en mantikli ve en sik secenek genellikle `docker-compose.yml` olur.

Neden?

- Proje PostgreSQL kurulumu istiyor; Docker Compose bunu tekrar edilebilir hale getirir.
- Peer evaluator senin makinede ayni PostgreSQL servisini kolayca baslatabilir.
- Veritabani kullanici adi, sifre, database adi ve port gibi ayarlar dosyada net gorunur.
- `setup.sh` makinenin mevcut durumuna daha bagimli olabilir.
- `VM-instructions.txt` sadece talimat dosyasidir; otomatik kurulum saglamaz.
- Subject ozellikle "Docker sececeksen Inception projesindeki standart ve iyi pratiklere
  uygun olmali" diyor. Bu da Docker Compose'un beklenen ve ciddi bir secenek oldugunu
  gosteriyor.

Bu yuzden ex00 icin onerilen teslim:

```text
ex00/docker-compose.yml
```

### Docker Compose Nedir?

Docker, uygulamalari container denen izole ortamlarda calistirmaya yarar. PostgreSQL'i
bilgisayarina dogrudan kurmak yerine bir container icinde calistirabilirsin.

Docker Compose ise bir veya birden fazla container'i `docker-compose.yml` dosyasiyla
tanimlayip calistirmaya yarar.

Ornek kullanim:

```bash
docker compose up -d
```

Bu komut compose dosyasindaki servisleri arka planda baslatir.

```bash
docker compose down
```

Bu komut servisleri durdurur.

```bash
docker compose logs
```

Bu komut servis loglarini gosterir.

```bash
docker compose ps
```

Bu komut calisan servisleri listeler.

PostgreSQL icin compose dosyasinda genelde sunlar olur:

- `image`: Hangi PostgreSQL imaji kullanilacak?
- `container_name`: Container adi ne olacak?
- `environment`: Kullanici, sifre, database adi gibi ortam degiskenleri.
- `ports`: Container icindeki PostgreSQL portu host makineye nasil acilacak?
- `volumes`: Veritabani verisi container silinse bile kalici olsun mu?
- `restart`: Container hangi durumda yeniden baslasin?

Docker Compose secilirse iyi pratik olarak veriyi kalici tutmak icin volume kullanmak
mantiklidir. Aksi halde container silindiginde database de kaybolabilir.

### psql Komutu Detayli Aciklama

Subject'in verdigi komut:

```bash
psql -U your_login -d piscineds -h localhost -W
```

Bu komut PostgreSQL'e terminalden baglanmak icin kullanilir.

Parcalari:

```text
psql
```

PostgreSQL'in komut satiri istemcisidir. Veritabanina baglanip SQL komutlari yazmani
saglar.

```text
-U your_login
```

`-U`, hangi PostgreSQL kullanicisiyle baglanacagini belirtir. Subject burada
`your_login` demis; gercekte bunu kendi 42 login'inle degistirmelisin.

Ornek:

```bash
psql -U ayhan -d piscineds -h localhost -W
```

```text
-d piscineds
```

`-d`, baglanilacak database adini belirtir. Subject database adinin kesin olarak
`piscineds` olmasini istiyor.

```text
-h localhost
```

`-h`, veritabani sunucusunun host adresini belirtir. `localhost`, "bu bilgisayar"
demektir. Docker Compose kullanirsan PostgreSQL container icinde calisir ama portu
bilgisayarina acildigi icin `localhost` uzerinden baglanabilirsin.

```text
-W
```

`-W`, psql'in sifre sormasini zorlar. Komutu calistirinca senden password ister.
Subject'e gore sifre:

```text
mysecretpassword
```

Baglanti basarili olursa su prompt gelir:

```text
piscineds=#
```

Bu prompt artik `piscineds` veritabaninin icinde oldugunu ve SQL komutlari
yazabilecegini gosterir.

Ornek:

```sql
\dt
```

Bu psql komutu mevcut tablolari listeler.

```sql
\q
```

psql'den cikis yapar.

## Exercise 01 - Show Me Your DB

### Subject Beklentisi

Teslim klasoru:

```text
ex01/
```

Files to turn in kismi subject'te bos gorunuyor. Yani burada spesifik bir dosya adi
verilmemis. Bu egzersizin asil beklentisi, veritabanini rahatca gorsellestirebildigini
ve veri uzerinde gezinebildigini gostermendir.

Allowed tools:

```text
pgAdmin, Postico, DBeaver or any other tool of your choice
```

Beklenti:

- Veritabanini kolayca gorsellestiren bir arac bul.
- Bu arac tablo gezmeyi ve veri manipule etmeyi kolaylastirsin.
- Ozellikle record ID'ler uzerinden veri bulmak ve incelemek kolay olsun.

### Hangi Arac Daha Uygun?

Bu proje icin en uygun secenek genellikle `DBeaver` olur.

Neden?

- Linux'ta rahat kullanilir.
- PostgreSQL destegi iyidir.
- Ucretsiz ve yaygin kullanilir.
- Tablo yapisini, kolon tiplerini, satirlari ve SQL sorgularini tek arayuzde gosterir.
- CSV import/export, tablo gezme, filtreleme ve record duzenleme gibi islerde kullanislidir.
- 42 cluster veya Linux ortaminda Postico'ya gore daha uygundur; Postico daha cok macOS
  odakli bir aractir.

`pgAdmin` de PostgreSQL icin resmi ve guclu bir aractir, ama yeni baslayan biri icin
DBeaver genelde daha sade ve kullanisli olabilir. Bu nedenle ex01 icin tercih onerim:

```text
DBeaver
```

### Ornek Ciktida Hangi Arac Secilmis?

Subject'te ex01 icin bir ekran goruntusu veya "su arac secildi" gibi net bir ornek cikti
yok. Sadece allowed tools satirinda `pgAdmin, Postico, DBeaver or any other tool of your
choice` yaziyor. Yani subject belirli bir araci zorunlu tutmuyor.

Ex00'da verilen `psql` komutu ise DBeaver/pgAdmin gibi gorsel arac degil; terminalden
PostgreSQL'e baglanmak icin kullanilan komut satiri aracidir.

### DBeaver ile Baglanti Mantigi

DBeaver'da PostgreSQL baglantisi acarken genelde su bilgiler girilir:

```text
Host: localhost
Port: 5432
Database: piscineds
Username: senin_loginin
Password: mysecretpassword
```

Sonra "Test Connection" ile baglanti denenir. Baglanti calisiyorsa tablolar sol panelde
gorunur.

## Exercise 02 - First Table

### Subject Beklentisi

Teslim klasoru:

```text
ex02/
```

Teslim edilecek dosya:

```text
table.*
```

Buradaki `*`, uzantinin serbest oldugunu gosterir. Ornegin:

```text
table.sql
table.sh
```

Subject'in istedigi is:

- `customer` klasorundeki bir CSV dosyasindan PostgreSQL tablosu olustur.
- Tablo adi CSV dosyasinin uzantisiz adi olmali.
- Ornek: `data_2022_oct.csv` dosyasindan tablo olusturuyorsan tablo adi
  `data_2022_oct` olmali.
- Kolon isimleri CSV dosyasindaki kolon isimleriyle birebir ayni olmali.
- Veri tipleri uygun secilmeli.
- En az alti farkli veri tipi kullanilmis olmali.
- Ilk kolon mutlaka tarih-saat kolonu olmali.

### Customer CSV Kolonlari

Customer dosyalarinda kolonlar:

```text
event_time,event_type,product_id,price,user_id,user_session
```

Ornek satir:

```text
2022-10-01 00:00:00 UTC,cart,5773203,2.62,463240011,26dd6e6e-4dac-4778-8d2c-92e149dab885
```

Bu satirin anlami:

- `event_time`: Olayin zamani
- `event_type`: Olay tipi, mesela `cart`, `purchase`, `remove_from_cart`, `view`
- `product_id`: Urun kimligi
- `price`: Urun fiyati
- `user_id`: Kullanici kimligi
- `user_session`: Kullanici oturum kimligi

### "At Least Six Different Data Types" Ne Demek?

Subject'teki ifade:

```text
their data types must be appropriate. You must use **at least six different data types**.
```

Burada senden kolonlari sadece `TEXT` yapmaman isteniyor. Her kolonun anlamina uygun
PostgreSQL veri tipi secmelisin. "En az alti farkli data type" demek, tablo taniminda
birbirinden farkli en az 6 PostgreSQL tipi kullanman bekleniyor demektir.

Customer CSV'de 6 kolon oldugu icin mantikli yorum sudur: Her kolon icin uygun ve
farkli bir tip sec.

Ornek uygun tip eslestirmesi:

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

Burada 6 farkli tip var:

```text
TIMESTAMPTZ
VARCHAR
INTEGER
NUMERIC
BIGINT
UUID
```

Neden bunlar mantikli?

- `event_time TIMESTAMPTZ`: CSV'deki tarih sonunda `UTC` var. Bu saat dilimi bilgisidir.
  PostgreSQL'de bunu saklamak icin `TIMESTAMP WITH TIME ZONE`, kisa adiyla `TIMESTAMPTZ`,
  uygundur.
- `event_type VARCHAR(32)`: `cart`, `purchase`, `remove_from_cart`, `view` gibi kisa
  metinler tutar.
- `product_id INTEGER`: Urun ID'leri tam sayidir.
- `price NUMERIC(10, 2)`: Para/fiyat bilgisi icin kayan nokta hatalarindan kacmak adina
  `NUMERIC` daha uygundur.
- `user_id BIGINT`: Kullanici ID'si tam sayidir; buyuyebilecegi icin `BIGINT` guvenli
  secimdir.
- `user_session UUID`: Oturum degeri UUID formatindadir:
  `26dd6e6e-4dac-4778-8d2c-92e149dab885`

Buradaki asil ders su: Veritabani tablosu tasarlarken her seyi metin olarak almak kolay
ama kotu bir pratiktir. Verinin dogasina uygun tip secmelisin.

### "A DATETIME Column as the First Column is Mandatory" Ne Demek?

Subject'teki ifade:

```text
A DATETIME column as the **first column** is mandatory.
```

Burada "ilk kolon tarih-saat bilgisi icermeli" deniyor. Customer CSV'lerinde zaten ilk
kolon:

```text
event_time
```

Bu kolonun degeri:

```text
2022-10-01 00:00:00 UTC
```

Yani yil, ay, gun, saat, dakika, saniye ve saat dilimi bilgisi var.

Onemli nokta: PostgreSQL'de `DATETIME` diye MariaDB/MySQL'deki gibi standart bir tip
kullanilmaz. PostgreSQL'de bunun karsiligi genellikle sunlardan biridir:

```text
TIMESTAMP
TIMESTAMP WITH TIME ZONE
TIMESTAMPTZ
```

Bu projede CSV'de `UTC` bulundugu icin en mantikli secim:

```sql
event_time TIMESTAMPTZ
```

Bu kolon neden lazim?

- Satis olaylarini zamana gore siralamak icin.
- Aylik/gunluk/saatlik analiz yapmak icin.
- "Son 4 ayin satislari" gibi filtreler yapmak icin.
- Kullanici davranisini zaman cizelgesinde izlemek icin.
- Ileride veri temizleme ve analiz modullerinde zaman temelli islemler yapabilmek icin.

Ilk kolon olmasi da subject'in tablo duzeni beklentisidir. CSV'deki kolon sirasina sadik
kalmak, otomatik import ve sonraki kontroller icin daha guvenlidir.

### `**` Isaretlerinin Ozel Anlami Var Mi?

Subject PDF'inde gorunen `**at least six different data types**` ve `**first column**`
ifadelerindeki `**`, Markdown yaziminda kalin vurgulama icin kullanilir.

Yani teknik olarak SQL veya PostgreSQL sembolu degildir. Subject bu kisimlari ozellikle
vurgulamak istemis:

- En az 6 farkli veri tipi kullan.
- Tarih-saat kolonu ilk kolon olsun.

`**` karakterlerini SQL koduna yazman gerekmez.

### Ex02 Icin Pratik Yorum

Ex02'de tek bir customer CSV dosyasindan bir tablo olusturman bekleniyor. En mantikli
dosya `data_2022_oct.csv` olabilir cunku subject ornegi de `data_2022_oct` ismini
veriyor.

Teslim dosyasi olarak temiz bir SQL dosyasi kullanmak mantikli:

```text
ex02/table.sql
```

Bu dosyada tabloyu olusturan SQL bulunabilir. Import icin `COPY` veya psql tarafinda
`\copy` kullanilabilir.

Genel fark:

- `COPY`: Dosyayi PostgreSQL server tarafindan okur.
- `\copy`: Dosyayi psql client tarafindan okur.

Docker kullanirken dosya yolu problemlerini azaltmak icin `\copy` cogu zaman daha
pratik olabilir.

## Exercise 03 - Automatic Table

### Subject Beklentisi

Teslim klasoru:

```text
ex03/
```

Teslim edilecek dosya:

```text
automatic_table.*
```

Ornek:

```text
automatic_table.sh
automatic_table.sql
```

Subject'in istedigi is:

- `customer` klasorundeki tum CSV dosyalarini otomatik bul.
- Her CSV dosyasi icin ayri bir PostgreSQL tablosu olustur.
- Her tablo adi CSV dosyasinin uzantisiz adi olmali.

Ornek:

```text
data_2022_oct.csv -> data_2022_oct
data_2022_nov.csv -> data_2022_nov
data_2022_dec.csv -> data_2022_dec
data_2023_jan.csv -> data_2023_jan
```

### Directory Structure Ornegi Ne Anlama Geliyor?

Subject ex03'te bir directory structure ornegi gosteriyor. Bu, "bu klasor yapisini
aynen tablo yapmak zorundasin" demek degil. Bu kisim sana CSV dosyalarinin nerede
bulunacagini ve scriptinin hangi dosyalari otomatik yakalamasi gerektigini anlatmak
icin verilmis.

Yani evet, proje sayfasindan indirdigin `subject/customer` klasorundeki CSV dosyalari
tablo olusturmak icin kullanilacak kaynak dosyalardir. Ama "ekstra hicbir sey yok"
demek tam dogru olmaz. Ekstra yapman gereken sey, bu dosyalari otomatik gezen ve her
biri icin tablo olusturan bir script veya SQL akisi hazirlamaktir.

Manuel olarak tek tek sunlari yapmak ex02 mantigidir:

```text
data_2022_oct icin tablo olustur
data_2022_nov icin tablo olustur
...
```

Ex03'te beklenen daha otomatik bir mantiktir:

```text
customer klasorundeki tum .csv dosyalarini bul
her dosya icin tablo adini dosya adindan cikar
tabloyu olustur
veriyi import et
```

### Dikkat Edilecek Nokta

Mevcut klasorde LibreOffice lock dosyalari da gorunuyor:

```text
.~lock.data_2022_dec.csv#
.~lock.data_2023_jan.csv#
```

Bunlar gercek CSV verisi degildir. Otomatik script yazarken sadece gercek `.csv`
dosyalarini yakalamalisin. Ornegin `*.csv` deseni bu lock dosyalarini genelde almaz
cunku onlar `.csv#` ile biter. Yine de gizli dosyalari dikkate almamak iyi pratiktir.

## Exercise 04 - Items Table

### Subject Beklentisi

Teslim klasoru:

```text
ex04/
```

Teslim edilecek dosya:

```text
items_table.*
```

Subject'in istedigi is:

- `item.csv` dosyasindaki kolon isimlerini kullanarak `items` adinda bir tablo olustur.
- Tablo en az uc farkli veri tipi icermeli.

Mevcut dosya:

```text
subject/item/item.csv
```

PDF'in directory structure orneginde `items` klasoru ve `items.csv` gibi ifadeler
gorunuyor; mevcut indirilen klasorde ise `subject/item/item.csv` var. Bu durumda canlı
dosya yapisini kaynak almak daha mantikli: veri dosyasi `item.csv`, olusturulacak tablo
adi ise subject'in soyledigi gibi `items` olmali.

### Item CSV Kolonlari

```text
product_id,category_id,category_code,brand
```

Ornek satir:

```text
5712790,1487580005268456192,,f.o.x
```

Anlamlari:

- `product_id`: Urun kimligi
- `category_id`: Kategori kimligi
- `category_code`: Kategori kodu, bazen bos olabilir
- `brand`: Marka adi, bazen bos olabilir

### "At Least Three Different Data Types" Ne Demek?

Subject'teki ifade:

```text
The table must contain at least **three different data types**.
```

Bu da ex02'deki mantigin daha kucuk hali. Item tablosunda kolonlari sadece `TEXT`
yapmani istemiyor. En az 3 farkli PostgreSQL veri tipi kullanmalisin.

Ornek uygun tablo:

```sql
CREATE TABLE items (
    product_id INTEGER,
    category_id BIGINT,
    category_code VARCHAR(255),
    brand TEXT
);
```

Burada 4 kolon var ve en az 3 farkli tip kullaniliyor:

```text
INTEGER
BIGINT
VARCHAR
TEXT
```

Neden bu tipler?

- `product_id INTEGER`: Urun ID'si tam sayi.
- `category_id BIGINT`: Kategori ID'leri cok buyuk sayilar; `INTEGER` icin fazla buyuk
  olabilir. Bu yuzden `BIGINT` daha dogru.
- `category_code VARCHAR(255)`: Kategori kodu metindir ve genelde belirli uzunlukta olur.
- `brand TEXT`: Marka adi metindir; bos olabilir ve uzunlugu degisebilir.

Burada `category_code` ve `brand` ikisi de metin gibi gorunur. Subject en az 3 farkli
tip istedigi icin birini `VARCHAR`, digerini `TEXT` yapmak teknik olarak farkli iki
PostgreSQL tipi kullanmak anlamina gelir. Daha kati tasarim dusunulurse ikisi de
`TEXT` secilebilir, ama o zaman farkli tip sayisini saglamak icin baska bir tasarim
gerekir. Bu subject baglaminda yukaridaki eslestirme uygun ve pratiktir.

### Directory Structure Ornegi Ne Anlama Geliyor?

Ex04'teki directory structure ornegi, ex03'teki gibi veri dosyalarinin nerede oldugunu
gostermek icindir. Hazir gelen CSV dosyasi tablo olusturmak icin kaynak dosyadir.

Yapman gereken ekstra is:

- `item.csv` dosyasinin kolonlarina uygun `items` tablosunu olusturmak.
- En az 3 farkli veri tipi kullanmak.
- Veriyi bu tabloya import etmek.

Yani subject dosyasinin icindeki CSV'ler sadece "hazir veri"; proje tesliminde asil
beklenen, bu verileri PostgreSQL'e aktaran SQL/script dosyalaridir.

## Onerilen Proje Yaklasimi

Bu proje icin temiz bir yol su olabilir:

```text
ex00/docker-compose.yml
ex01/README.md veya kisa not dosyasi
ex02/table.sql
ex03/automatic_table.sh
ex04/items_table.sql
```

Subject ex01 icin dosya istemiyor gibi gorunse de, kendi acindan hangi araci kullandigini
ve nasil baglandigini not etmek faydali olur. Degerlendirmede DBeaver'i acip veritabanini
gostermen yeterli olabilir.

## Onerilen Veri Tipleri Ozeti

Customer tablolari icin:

```sql
event_time   TIMESTAMPTZ
event_type   VARCHAR(32)
product_id   INTEGER
price        NUMERIC(10, 2)
user_id      BIGINT
user_session UUID
```

Items tablosu icin:

```sql
product_id    INTEGER
category_id   BIGINT
category_code VARCHAR(255)
brand         TEXT
```

## Neden Veri Tipi Bu Kadar Onemli?

Veritabani veri tipleri sadece formalite degildir. Sorgularin dogru calismasini belirler.

Yanlis:

```sql
price TEXT
```

Bu durumda `price` metin olur. Toplam fiyat hesaplamak veya fiyata gore siralamak
beklenmedik davranabilir.

Dogru:

```sql
price NUMERIC(10, 2)
```

Bu durumda PostgreSQL bunun parasal/ondalik sayi oldugunu bilir.

Yanlis:

```sql
event_time TEXT
```

Bu durumda tarih filtreleri zorlasir.

Dogru:

```sql
event_time TIMESTAMPTZ
```

Bu durumda sunlar kolaylasir:

```sql
SELECT *
FROM data_2022_oct
WHERE event_time >= '2022-10-15';
```

## Bu Projede Basari Kriteri

Projeyi subject'e uygun yapmak icin sunlari saglamalisin:

- PostgreSQL veritabanina `psql -U login -d piscineds -h localhost -W` ile baglanilabilmeli.
- Kullanici adi 42 login'in olmali.
- Database adi `piscineds` olmali.
- Sifre `mysecretpassword` olmali.
- Customer CSV dosyasindan en az bir tablo elle olusturulabilmeli.
- Customer klasorundeki tum CSV'ler otomatik tabloya donusturulebilmeli.
- `items` tablosu `item.csv` dosyasindan olusturulabilmeli.
- Kolon isimleri CSV basliklariyla birebir ayni olmali.
- Veri tipleri kolonlarin anlamina uygun olmali.
- Tarih-saat kolonu customer tablosunda ilk kolon olmali.
- Veriler sonraki modullerde kullanilabilecek kadar temiz ve duzenli saklanmali.

