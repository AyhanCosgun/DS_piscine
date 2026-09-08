# 42 Data Science Piscine — DS_2: Data Viz & Customer Clustering
## Kapsamlı Başlangıç Rehberi, Yol Haritası ve Soru-Cevap Kılavuzu (`ds2_tutorial.md`)

Bu rehber, **42 Data Science Piscine** modüllerinden **DS_2 (Data Viz)** projesini sıfırdan başarıyla tamamlamanız, veri analitiği ve kümeleme (clustering) dünyasının mantığını derinlemesine kavramanız ve peer-evaluation (savunma) aşamasında tam puan almanız için hazırlanmıştır.

---

## İçindekiler
1. [42 Data Science Piscine Büyük Resmi (ds_0'dan ds_4'e)]( #1-42-data-science-piscine-büyük-resmi-ds_0dan-ds_4e)
2. [Soru 1: Hangi Dili ve Yöntemi Kullanmalıyım? PostgreSQL / DBeaver Yeterli mi?](#2-soru-1-hangi-dili-ve-yöntemi-kullanmalıyım-postgresql--dbeaver-yeterli-mi)
3. [Soru 2: "Techno R, Excel, Power BI, Jupyter Notebook..." Ne Demek? Hangi Tool Seçilmeli?](#3-soru-2-techno-r-excel-power-bi-jupyter-notebook-ne-demek-hangi-tool-seçilmeli)
4. [Soru 3: Her Bir Egzersizin Detaylı Analizi ve Yapılışı (ex00 - ex05)](#4-soru-3-her-bir-egzersizin-detaylı-analizi-ve-yapılışı-ex00---ex05)
5. [Soru 4: Ex02'den Sonraki Grafiklerin Anlamı ve PDF'deki "?" / "??" İşaretlerinin Sırrı](#5-soru-4-ex02den-sonraki-grafiklerin-anlamı-ve-pdfdeki---işaretlerinin-sırrı)
6. [Soru 5: Clustering (Kümeleme) Nedir, Ne İşe Yarar? Elbow Method Nasıl Çalışır?](#6-soru-5-clustering-kümeleme-nedir-ne-işe-yarar-elbow-method-nasıl-çalışır)
7. [Soru 6: Kümeleme Algoritmaları Nelerdir, Kaç Tane Vardır ve Nerelerde Kullanılırlar?](#7-soru-6-kümeleme-algoritmaları-nelerdir-kaç-tane-vardır-ve-nerelerde-kullanılırlar)
8. [Soru 7: Ex05 Grafiklerinin Eksenleri Ne Anlama Gelir? Centroid Nedir?](#8-soru-7-ex05-grafiklerinin-eksenleri-ne-anlama-gelir-centroid-nedir)
9. [Adım Adım DS_2 Yol Haritası ve Kod İskeletleri](#9-adım-adım-ds_2-yol-haritası-ve-kod-iskeletleri)
10. [Peer-Evaluation (Savunma) Taktikleri](#10-peer-evaluation-savunma-taktikleri)
11. [Ex00 Soru ve Cevapları](#11-ex00-soru-ve-cevapları)

---

## 1. 42 Data Science Piscine Büyük Resmi (ds_0'dan ds_4'e)

42 Piscine müfredatı rastgele ödevlerden oluşmaz; uçtan uca gerçek bir veri bilimi yaşam döngüsünü (**Data Science Lifecycle**) simüle eder:

```
┌────────────────┐    ┌────────────────┐    ┌────────────────┐    ┌────────────────┐    ┌────────────────┐
│      DS_0      │───►│      DS_1      │───►│      DS_2      │───►│      DS_3      │───►│      DS_4      │
│  Data Ingest   │    │ Data Warehouse │    │    Data Viz    │    │ Exploratory DA │    │ Predictive ML  │
│  (PostgreSQL)  │    │     (ETL)      │    │  (Clustering)  │    │ (StarWars EDA) │    │(Classification)│
└────────────────┘    └────────────────┘    └────────────────┘    └────────────────┘    └────────────────┘
```

1. **DS_0 (Data Ingestion & Storage):** Ham CSV verilerini PostgreSQL ortamına aktarmayı, tablolar kurmayı öğrendiniz (`automatic_table.sh`, `table.sql`).
2. **DS_1 (Data Warehouse & ETL):** Parçalanmış aylık tabloları tek bir merkezde birleştirdiniz (`UNION ALL`), duplicate satırları temizlediniz ve ürün tablolarıyla `JOIN` yaptınız. Temiz bir **Veri Ambarı (DWH)** inşa ettiniz.
3. **DS_2 (Data Visualization & Customer Segmentation - ŞU ANKİ MODÜL):** Veri ambarındaki bu temiz veriyi artık iş zekası (BI) ve analitik için kullanacaksınız. Temel grafiklerle satışları keşfedecek, ardından **Makine Öğrenimi (Clustering)** ile müşterileri karlı segmentlere ayıracaksınız.
4. **DS_3 (The Present / Preprocessing & EDA):** Star Wars Jedi/Sith şövalyeleri veri setinde dağılımları (Histogram), korelasyonları, aykırı değerleri, standardizasyon ve normalizasyon tekniklerini inceleyeceksiniz.
5. **DS_4 (The Future / Predictive Modeling):** DS_3'te temizlenen şövalye verileri üzerinde Karar Ağaçları (Decision Tree / Random Forest), KNN ve Ensembling (Oylama Sınıflandırıcısı) ile geleceği tahmin eden (Supervised ML) modeller kuracaksınız.

> [!IMPORTANT]
> **DS_2'deki Kritik Kural:**  
> Subject'in 3. sayfasındaki resmi uyarı:  
> *"All the graphs are done without the February data, you have to redo them all with the new data"*  
> PDF'deki örnek grafikler Şubat ayı verisi eklenmeden önceki eski görüntülerdir. Siz tüm grafikleri ve kümeleme analizini **Şubat 2023 (`data_2023_jan` / `data_2023_feb`) verilerini de içeren eksiksiz DWH veritabanınızla** sıfırdan oluşturacaksınız!

---

## 2. Soru 1: Hangi Dili ve Yöntemi Kullanmalıyım? PostgreSQL / DBeaver Yeterli mi?

> **Soru:**  
> *"Proje için hangi dili kullanmalıyım, bana bırakılmış ama ?? Bu tabloları postgresql ile ya da dbeaver ile yapamıyor muyuz ? Yoksa python modülleri mi kullanmalıyız ? En ideal yöntem hangisi ?"*

### Cevap:
**En ideal ve sektör standardı yöntem: HİBRİT YÖNTEMDİR (PostgreSQL + Python).**

#### Neden Sadece PostgreSQL veya DBeaver ile Yapılamaz?
- **DBeaver bir çizim veya programlama aracı değildir:** DBeaver sadece veritabanına bağlanıp SQL sorgusu çalıştırmanızı sağlayan bir grafik arayüzüdür (GUI). Grafikler çizip bunları bir dosyaya script olarak kaydedemezsiniz.
- **PostgreSQL grafik çizemez ve K-Means yapamaz:** PostgreSQL bir ilişkisel veritabanı motorudur. Verileri filtreler, gruplar (`GROUP BY`), toplar (`SUM`, `COUNT`), ortalama alır (`AVG`). Ancak ekranda bir pasta grafik (`pie chart`), kutu-bıyık grafiği (`box plot`) veya dağılım grafiği (`scatter plot`) çizemez; K-Means algoritmasını yerleşik olarak barındırmaz.
- **Subject'in Teslim İsteri:** Subject sizden her klasörde çalıştırılabilir birer kod dosyası istemektedir (`pie.*`, `chart.*`, `mustache.*`, `Building.*`, `elbow.*`, `Clustering.*`). Değerlendiren kişi terminalde bu scripti çalıştırdığında grafiklerin ekrana gelmesini bekler.

#### En İdeal İş Bölümü (The Golden Workflow):
1. **Veritabanı Katmanı (PostgreSQL):** Ağır veri hesaplamalarını (filtreleme, aylık toplama, müşteri bazında RFM metrikleri çıkarma) SQL'e yaptırın. Çünkü PostgreSQL 16+ milyon satır üzerinde C hızında gruplama yapar.
2. **Uygulama ve Görselleştirme Katmanı (Python):**
   - `psycopg2` / `SQLAlchemy`: PostgreSQL'den hesaplanmış veriyi çeker.
   - `pandas`: Tabloları DataFrame formatında yönetir.
   - `matplotlib` & `seaborn`: Subject'te istenen tüm grafikleri piksellerine kadar çizer.
   - `scikit-learn`: Ex04 ve Ex05'teki **K-Means** ve **Elbow Method** hesaplamalarını yapar.

---

## 3. Soru 2: "Techno R, Excel, Power BI, Jupyter Notebook..." Ne Demek? Hangi Tool Seçilmeli?

> **Soru:**  
> *" 'They often use tools such as techno R, Excel, Power BI, Jupyter Notebook . . . It is up to you to find the tools that suit you. You are free to use any language of your choice for this module.' ne demek tam olarak ? dili seçtikten sonra bir de tool mu seçeceğiz ? Eğer seçeceksek en uygunu hangisi bu sektörde çalışmayı düşünen bir profesyonel için ?"*

### Cevap:

#### 1. Bu Cümlenin Anlamı Nedir?
Subject yazarları burada gerçek dünyada bir Veri Analistinin (Data Analyst) kullandığı ekosistemi tasvir etmek istemiş; ancak **Programlama Dili** (`Python`, `R`), **İş Zekası / BI Aracı** (`Power BI`, `Tableau`), **Elektronik Tablo** (`Excel`) ve **Geliştirme Ortamı** (`Jupyter Notebook`) gibi kavramları günlük dilde aynı torbaya ("techno / tools") koymuştur.

Burada iki ayrı seçim yapmıyorsunuz; bir **teknoloji yığını (tech-stack)** seçiyorsunuz.

```
┌────────────────────────────────────────────────────────────────────────┐
│                        SEKTÖR TEKNOLOJİ YIĞINI                         │
├───────────────────┬───────────────────┬────────────────────────────────┤
│ Katman            │ Sektör Standardı  │ Bu Projedeki Görevi            │
├───────────────────┼───────────────────┼────────────────────────────────┤
│ Veritabanı        │ PostgreSQL        │ Veri depolama, sorgulama       │
│ Programlama Dili  │ Python            │ Tüm mantık, otomasyon          │
│ Analiz Kütüphanesi│ Pandas, NumPy     │ Veri işleme, RFM hesaplama     │
│ Görselleştirme    │ Matplotlib,Seaborn│ Grafiklerin üretimi            │
│ Makine Öğrenimi   │ Scikit-Learn      │ K-Means, Elbow, StandardScaler │
│ Geliştirme Ortamı │ VS Code / Jupyter │ Kod geliştirme ve test         │
└───────────────────┴───────────────────┴────────────────────────────────┘
```

#### 2. Neden Power BI veya Excel Değil?
- **42 Cluster Ortamı:** 42 kampüs bilgisayarlarında Power BI çalışmaz (Windows bağımlıdır).
- **Otomasyon ve Değerlendirme:** Evaluator değerlendirme yaparken `python3 pie.py` veya `python3 chart.py` yazıp çıktıyı anında görmek ister. Excel veya Power BI dosyasını açıp değerlendirmek 42 standartlarına uymaz.

#### 3. Sektör Profesyoneli İçin En Uygun Tercih:
Bugün küresel ölçekte veri bilimi, veri mühendisliği ve yapay zeka alanında çalışan profesyonellerin **%85'inden fazlası Python ekosistemini** kullanır. Python öğrenmek sizi doğrudan iş dünyasına hazırlar.

---

## 4. Soru 3: Her Bir Egzersizin Detaylı Analizi ve Yapılışı (ex00 - ex05)

> **Soru:**  
> *"Her bir exercise için ne istendiğini ve nasıl yapılacağını, hangi tool yapılacağını detaylıca açıkla. Bu konulara yeni başlayan birisi anlayabilmeli."*

### Cevap:

### Exercise 00: American Apple Pie (`pie.*`)
- **İstenen:** Sitedeki kullanıcıların ne yaptığını (`event_type`) gösteren bir **Pasta Grafiği (Pie Chart)** oluşturmak ve DS_1'deki Veri Ambarına bağlanmak.
- **Mantık:** Veritabanındaki `customers` tablosunda `event_type` kolonunu gruplayıp her bir olayın sayısını bulacağız:
  - `view` (ürün inceleme - genelde %70-80 ile en büyük dilim)
  - `cart` (sepete ekleme)
  - `remove_from_cart` (sepetten çıkarma)
  - `purchase` (satın alma)
- **Nasıl Yapılır?**
  1. SQL ile `SELECT event_type, COUNT(*) FROM customers GROUP BY event_type;` sorgusu çalıştırılır.
  2. Python'da `matplotlib.pyplot.pie()` kullanılarak dilimler ve yüzde değerleri (`autopct='%1.1f%%'`) çizdirilir.

---

### Exercise 01: Initial Data Exploration (`chart.*`)
- **İstenen:** 
  1. Yalnızca `event_type = 'purchase'` olan verileri filtrelemek.
  2. Fiyatların "Altairian Dollars" (A) cinsinden olduğunu bilmek.
  3. Ekim 2022 başından Şubat 2023 sonuna kadar **3 adet zaman serisi grafiği** oluşturmak.
- **3 Grafik Nelerdir?**
  - **Grafik 1 (Number of customers):** Zaman içinde (günlük veya aylık) alışveriş yapan **tekil müşteri sayısı** (`COUNT(DISTINCT user_id)` / `nunique()`).
  - **Grafik 2 (Total sales in million of A):** Aylık toplam ciro (`SUM(price)`). Milyon cinsinden ifade edilir.
  - **Grafik 3 (Average spend/customer in A):** Müşteri başına ortalama harcama (`Total Sales / Distinct Customers`).
- **Nasıl Yapılır?**
  SQL veya Pandas ile `event_time` kolonu aylara/günlere göre gruplanır (`DATE_TRUNC('month', event_time)` veya `df.resample('M')`), ardından `matplotlib.pyplot.plot()` veya `sns.lineplot()` ile çizdirilir.

---

### Exercise 02: My Beautiful Mustache (`mustache.*`)
- **İstenen:**
  1. Satın alınan ürün fiyatlarının (`price`) istatistiksel özetini yazdırmak:
     - `count`, `mean` (ortalama), `std` (standart sapma), `min`, `max`, `first quartile (25%)`, `median (50%)`, `third quartile (75%)`.
  2. Fiyatların dağılımını gösteren bir **Kutu-Bıyık Grafiği (Box Plot)** çizmek.
  3. Kullanıcı başına ortalama sepet tutarı (**average basket price per user**) için ikinci bir box plot çizmek.
- **Nasıl Yapılır?**
  - İstatistikler için Pandas `df['price'].describe()` fonksiyonu birebirdir.
  - Box plot için `seaborn.boxplot(x=df['price'])` kullanılır.
  - İkinci grafik için önce her kullanıcının oturum/sepet başına ortalaması hesaplanır (`groupby(['user_id', 'user_session'])['price'].sum()`), sonra onun box plot'u çizilir.

---

### Exercise 03: Highest Building (`Building.*`)
- **İstenen:**
  1. Müşterilerin sipariş sıklığına göre sipariş adedini gösteren bir sütun grafiği (**bar chart / histogram**).
  2. Müşterilerin sitede harcadığı toplam paraya (Monetary value) göre dağılımını gösteren ikinci bir sütun grafiği.
- **Nasıl Yapılır?**
  - Her müşteri için toplam sipariş sayısı (`Frequency`) ve toplam harcama (`Monetary`) hesaplanır.
  - Dağılımı göstermek için `matplotlib.pyplot.hist()` veya `sns.histplot()` ile aralıklara (bins) bölünerek çizdirilir.

---

### Exercise 04: Elbow (`elbow.*`)
- **İstenen:** Müşterileri e-posta ile hedeflemek için gruplamak istiyoruz. Optimum küme sayısını ($k$) belirlemek için **Elbow Method (Dirsek Yöntemi)** grafiği oluşturmak ve seçilen $k$ sayısının nedenini savunabilmek.
- **Nasıl Yapılır?**
  - Müşteri bazında RFM (Recency, Frequency, Monetary) özet tablosu oluşturulur.
  - Sayısal değerler `StandardScaler` ile ölçeklendirilir.
  - $k=1$'den $k=10$'a kadar bir döngüde `KMeans(n_clusters=k)` eğitilir ve `model.inertia_` (hata kareleri toplamı) listeye eklenir.
  - $k$ değerlerine karşılık `inertia` çizgisi çizilir. Bükülmenin (dirseğin) olduğu nokta tespit edilir.

---

### Exercise 05: Clustering (`Clustering.*`)
- **İstenen:**
  1. Müşterileri en az **4 gruba** ayırmak (Örn: New customer, Inactive customer, Loyal customer, Platinum/Gold VIP...).
  2. Bir **Clustering Algoritması** (Örn: K-Means) kullanmak.
  3. Grupların en az **2 farklı grafiksel temsilini** oluşturmak.
- **Nasıl Yapılır?**
  - Ex04'te belirlediğiniz optimum $k$ (örneğin $k=4$ veya $k=5$) ile K-Means modeli fit edilir.
  - Her müşteriye bir küme etiketi atanır (`cluster_0`, `cluster_1`, ...).
  - Kümelerin ortalama Recency, Frequency ve Monetary değerlerine bakılarak anlamlı iş isimleri verilir.
  - En az iki grafik üretilir:
    1. Segmentlerdeki müşteri sayılarını gösteren Bar Chart.
    2. Kümeleri ve merkezlerini (**Centroids**) gösteren 2D/3D Scatter Plot.

---

## 5. Soru 4: Ex02'den Sonraki Grafiklerin Anlamı ve PDF'deki "?" / "??" İşaretlerinin Sırrı

> **Soru:**  
> *"Özellikle ex02 den sonra grafiklerin ne grafiği olduğu da anlaşılmıyor bazen. Grafikleri de detaylıca açıkla. Ayrıca bazılarında bazı yerlerde '?' var, bunları da açıkla."*

### Cevap:

### 1. Ex02: "Mustache" Neden Kutu Grafiğidir?
Fransızcada Box Plot grafiğine **"Boîte à moustaches"** (bıyıklı kutu) denir; Ecole 42 Fransız menşeili olduğu için egzersize esprili bir dille *"My beautiful mustache"* adını vermiştir.

```text
                  Outliers (Aykırı Değerler)
                      •    •   •
   Min      Q1      Median     Q3       Max
────┬───────┌─────────┬────────┐─────────┬───────► Fiyat Ekseni
    │       │         │        │         │
 ───┴───────┤         │        ├─────────┴───
 (Sol Bıyık)└─────────┴────────┘ (Sağ Bıyık)
               IQR (%50 Kutu)
```
- **Kutunun İçi:** Verinin tam ortasındaki %50'lik dilimdir (Q1 ile Q3 arası).
- **Ortadaki Çizgi:** Medyan (ortanca) değerdir.
- **Bıyıklar (Whiskers):** Normal dağılım sınırlarıdır ($Q1 - 1.5 \times IQR$ ve $Q3 + 1.5 \times IQR$).
- **Sağdaki Noktalar:** Normalin çok üstündeki lüks ürünler veya aykırı değerlerdir (Outliers).
- **Negatif Fiyat (`min = -79.37`):** Ham veri setinde iade, hediye çeki veya veri kayıt hatasından kaynaklanan negatif değerler vardır; bu durumu fark ettiğinizi savunmada belirtmeniz gerekir.

---

### 2. Ex03: Neden "Highest Building" (En Yüksek Bina)?
E-ticaret sitelerinde müşterilerin %80'i yalnızca 1 veya 2 kez sipariş verir. 10'dan fazla sipariş verenlerin sayısı çok azdır.
Bu veriyi histograma döktüğünüzde, $x=1$ ve $x=2$ sütunları **New York'taki Empire State gökdeleni gibi tavana fırlar**, diğer sütunlar ise yer seviyesinde kalır. Egzersizin adı bu görsel benzerlikten gelmektedir!

---

### 3. Ex04: "Elbow" (Dirsek) Grafiği
Bu grafik, bir kolun bükülmüş dirseğine benzer. 
- $k=1$'den başlarken hata (Inertia) uçurum gibi düşer.
- Belli bir $k$ sayısından sonra düşüş hızı yavaşlar ve yataylaşır.
- Bükülmenin en net olduğu dirsek eklemi (elbow point), en ideal küme sayısıdır.

---

### 4. PDF'deki "?" ve "??" İşaretlerinin Gerçek Sırrı

Subject PDF'sinin 13. ve 14. sayfalarındaki görselleri OCR ile taradığımızda şu metinlerle karşılaşırız:
```text
Average "Loyal customers": ?? A
Average "New customers": ?? A
Average "inactive": ?? A
Title: Clusters of customers ??
```

> [!CAUTION]
> **Bu soru işaretleri bir hata, bug veya eksik kod DEĞİLDİR!**  
> Bunlar subject yazarının bıraktığı **PLACEHOLDER (Doldurulması Gereken Boşluk)** işaretleridir.  
> 
> **Anlamı şudur:**  
> Subject yazarı sizin yerinize sayıları yazamaz; çünkü siz modeli Şubat ayını da katarak kendi veritabanınızda çalıştıracaksınız. Bu soru işaretleri size der ki:  
> *"Ben buraya '??' koydum; sen kendi çalıştırdığın K-Means sonucuna göre 'Sadık Müşterilerimin ortalama harcaması 45.2 A', 'Yeni müşterilerimin ortalama harcaması 12.8 A' şeklinde kendi gerçek sayılarını bulup grafiğin üzerine veya raporuna yazacaksın!"*

---

## 6. Soru 5: Clustering (Kümeleme) Nedir, Ne İşe Yarar? Elbow Method Nasıl Çalışır?

> **Soru:**  
> *"Clustering kavramını detaylıca açıkla. Bunun amacı nedir, ne işe yarar, nasıl yapılır ? Elbow Method nedir, örnekli açıkla ?"*

### Cevap:

### 1. Clustering Nedir ve Amacı Nedir?
Clustering, **Denetimsiz Makine Öğrenimi (Unsupervised Learning)** yöntemidir.
- **Supervised (Denetimli):** Veride hedef etiket bellidir (Örn: "Bu hasta kanser mi? Evet/Hayır").
- **Unsupervised (Denetimsiz):** Elimizde hiçbir hazır etiket yoktur! Veritabanında *"Bu müşteri sadıktır, bu müşteri terk etmek üzeredir"* diye bir kolon yazmaz.

**Amacı:** Benzer davranışlar sergileyen veri noktalarını matematiksel uzaklıklarına göre keşfedip aynı sepetlerde (kümelerde) toplamaktır.

### 2. Müşteri Segmentasyonunda Nasıl Yapılır? (RFM Modeli)
Ham transaction tablosunu K-Means'e veremezsiniz; çünkü bir müşterinin 50 satırı varken diğerinin 1 satırı vardır. Veri **müşteri seviyesine (Customer-Level)** indirgenmelidir:

```text
Ham Veri (Loglar)                      RFM Tablosu (1 Satır = 1 Müşteri)
┌─────────┬────────────┬───────┐      ┌─────────┬─────────┬───────────┬──────────┐
│ user_id │ event_time │ price │ ───► │ user_id │ Recency │ Frequency │ Monetary │
├─────────┼────────────┼───────┤      ├─────────┼─────────┼───────────┼──────────┤
│ 101     │ 2023-02-20 │ 50    │      │ 101     │ 3 gün   │ 2 sipariş │ 80 A     │
│ 101     │ 2023-02-23 │ 30    │      │ 102     │ 95 gün  │ 1 sipariş │ 15 A     │
│ 102     │ 2022-11-10 │ 15    │      └─────────┴─────────┴───────────┴──────────┘
└─────────┴────────────┴───────┘
```
- **Recency (Yenilik):** Müşterinin son alışverişinden bugüne kaç gün geçti? (Küçük olması iyidir).
- **Frequency (Sıklık):** Müşteri toplam kaç kez alışveriş yaptı? (Büyük olması iyidir).
- **Monetary (Parasal Değer):** Müşteri toplam kaç Altairian Doları harcadı? (Büyük olması iyidir).

---

### 3. Elbow Method Nedir ve Nasıl Çalışır?
K-Means algoritmasına başlarken parametre olarak $k$ sayısını (kaç küme istediğimizi) bizim vermemiz gerekir. Peki patrona gidip *"Neden 4 küme yaptın?"* sorusuna nasıl bilimsel cevap vereceğiz?

İşte **Elbow Method** bu seçimi kanıtlama aracıdır:
1. Algoritma her nokta ile o noktanın bağlı olduğu küme merkezi arasındaki mesafeyi ölçer.
2. Bu mesafelerin karelerinin toplamına **Inertia (veya WCSS - Within-Cluster Sum of Squares)** denir.
3. Kümeler mükemmel ve sıkıysa Inertia küçüktür.

**Örnek Senaryo:**
```text
Inertia
  ▲
  │  ● (k=1, Inertia = 280.000)  [Tek küme: herkes çorba, hata devasa]
  │   \
  │    \
  │     ● (k=2, Inertia = 150.000) [Büyük düşüş]
  │      \
  │       ● (k=3, Inertia = 90.000)  [Ciddi toparlanma]
  │        \
  │         ● (k=4, Inertia = 60.000) <=== DİRSEK NOKTASI (ELBOW)!
  │          └───● (k=5, Inertia = 52.000) [Bundan sonraki düşüşler önemsiz]
  │               └───● (k=6, Inertia = 46.000)
  └────────────────────────────────────────► k (Küme Sayısı)
```
- $k=1$'den $k=4$'e kadar hata dev adımlarla azalır.
- $k=4$'ten sonra yeni küme eklemek hatayı çok az düşürür ama iş modelini gereksiz karmaşıklaştırır.
- Bu yüzden grafik kol dirseği gibi $k=4$ noktasında kırılır: **Optimum küme sayısı 4'tür!**

---

## 7. Soru 6: Kümeleme Algoritmaları Nelerdir, Kaç Tane Vardır ve Nerelerde Kullanılırlar?

> **Soru:**  
> *"ex05 te geçen 'You have to use a Clustering Algorithms' kısmındaki bu algoritmalar neler, kaç tane var ve hangi amaçlar için kullanılıyorlar? Detaylı ve örnekli açıklama yap."*

### Cevap:

Literatürde onlarca kümeleme algoritması vardır; ancak makine öğrenimi dünyasında bunlar **4 ana aileye** ayrılır:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        KÜMELEME ALGORİTMALARI AİLESİ                        │
├──────────────────────┬──────────────────────┬───────────────────────────────┤
│ Aile                 │ Temsilci Algoritmalar│ En Uygun Olduğu Alan          │
├──────────────────────┼──────────────────────┼───────────────────────────────┤
│ 1. Merkez Tabanlı    │ K-Means, K-Medoids   │ Sayısal veriler, küresel      │
│    (Centroid-based)  │                      │ müşteri segmentasyonu (RFM)   │
├──────────────────────┼──────────────────────┼───────────────────────────────┤
│ 2. Hiyerarşik        │ Agglomerative,       │ Küçük veri setleri, soy ağacı,│
│    (Hierarchical)    │ Divisive             │ dendrogram analizleri         │
├──────────────────────┼──────────────────────┼───────────────────────────────┤
│ 3. Yoğunluk Tabanlı  │ DBSCAN, OPTICS       │ Aykırı değer tespiti (Fraud), │
│    (Density-based)   │                      │ düzensiz/hilal şekilli veriler│
├──────────────────────┼──────────────────────┼───────────────────────────────┤
│ 4. Dağılım Tabanlı   │ GMM (Gaussian        │ Olasılıksal kümeleme, iç içe  │
│    (Distribution)    │ Mixture Models)      │ geçmiş gauss dağılımları      │
└──────────────────────┴──────────────────────┴───────────────────────────────┘
```

#### 1. K-Means (Bu Projenin Şampiyonu)
- **Nasıl Çalışır?** Rastgele $k$ adet merkez (centroid) seçer. Her noktayı en yakın merkeze bağlar. Sonra merkezleri o kümedeki noktaların ortalamasına kaydırır. Merkezler sabitlenene kadar tekrarlar.
- **Neden Burada Kullanıyoruz?** Hızlıdır, milyonlarca satıra ölçeklenir, sayısal RFM özellikleri için idealdir ve Elbow grafiğiyle doğrudan doğrulanabilir.

#### 2. Hierarchical / Agglomerative Clustering
- **Nasıl Çalışır?** Başlangıçta her müşteriyi tek başına bir küme sayar. Birbirine en yakın iki müşteriyi birleştirir. Adım adım tüm veriyi tek bir ağaçta (Dendrogram) toplar.
- **Kullanım:** Biyolojide gen dizilimleri, şirket organizasyon şemaları. (Milyonlarca satırda çok yavaştır, bu projede K-Means tercih edilir).

#### 3. DBSCAN (Density-Based Spatial Clustering of Applications with Noise)
- **Nasıl Çalışır?** Noktaların birbirine olan yoğunluğuna bakar. Yoğun bölgeleri küme yapar; tenha yerlerde tek başına kalan noktaları doğrudan **GÜRÜLTÜ / AYKIRI DEĞER (NOISE = -1)** ilan eder.
- **Kullanım:** Kredi kartı sahtekarlığı (Fraud Detection), GPS rota analizi.

#### 4. Gaussian Mixture Models (GMM)
- **Nasıl Çalışır?** "Yumuşak Kümeleme" (Soft Clustering) yapar. Bir müşteriye sadece "Cluster 1" demez; *"%70 ihtimalle Sadık, %30 ihtimalle Uyuyan"* der.

---

## 8. Soru 7: Ex05 Grafiklerinin Eksenleri Ne Anlama Gelir? Centroid Nedir?

> **Soru:**  
> *"Özellikle ex05 in grafiklerinden birşey anlamadım, yatay eksende dikey eksende yazan kavramlar ne demek, centroid ne demek v.b. ?"*

### Cevap:

Subject PDF'sindeki Ex05 sayfalarında yer alan görselleri adım adım deşifre edelim:

### 1. Sayfa 12'deki Bar Grafiği (Segment Dağılımı):
- **Dikey Eksen (Y Ekseni):** Belirlediğiniz iş segmentlerinin isimleridir:
  - `Loyal customers` (Sadık müşteriler)
  - `New customers` (Yeni müşteriler)
  - `inactive` (Terk etmiş / Uyuyan müşteriler)
- **Yatay Eksen (X Ekseni):** `number of customers` (O segmentte kaç kişi olduğu: örn. 39.586 kişi).

---

### 2. Sayfa 13'teki Dağılım Grafiği (Scatter Plot):
- **Yatay Eksen (X Ekseni): `Median Recency (month)`**  
  Müşterinin son alışverişinin üzerinden kaç ay geçtiğini gösterir.
  - `0`: Bu ay alışveriş yapmış, sımsıcak müşteri!
  - `3 - 4`: 4 aydır hiçbir şey almamış, platformu unutmuş müşteri!
- **Dikey Eksen (Y Ekseni): `Median Frequency`**  
  Müşterinin yaptığı sipariş adedini gösterir.
  - `1 - 2`: Seyrek alışveriş yapanlar.
  - `10 - 20`: Sürekli sipariş veren sadık kullanıcılar.
- **Renkler:** Her bir nokta bir müşteridir ve rengi ait olduğu kümeyi gösterir.

---

### 3. Centroid (Küme Merkezi) Nedir?

```text
        Frequency
            ▲
            │         ● (Cluster 1 Üyeleri)
            │      ●  ★  ●   <=== ★ İŞARETİ CENTROID'DİR!
            │         ●
            │
            │  ▲ (Cluster 2 Üyeleri)
            │▲ ★ ▲
            └─────────────────────────► Recency
```

- **Tanım:** Centroid, o kümedeki **tüm müşterilerin özelliklerinin ağırlık merkezidir (aritmetik ortalama vektörüdür)**.
- **Somut Örnek:**
  Diyelim ki "Gold VIP" kümenizde 10.000 müşteri var.
  Bu 10.000 kişinin ortalamasını aldığınızda:
  - Ortalama Recency = 2 gün
  - Ortalama Frequency = 18 sipariş
  - Ortalama Monetary = 3.200 A
  İşte `(Recency=2, Frequency=18, Monetary=3200)` koordinatındaki sanal nokta o kümenin **CENTROID**'idir.
- **Grafikte Nasıl Görünür?**  
  PDF'de ve profesyonel grafiklerde centroid'ler, müşteri noktalarının tam ortasında parlayan **büyük yıldızlar, çarpı işaretleri (X) veya iri sarı noktalar** olarak gösterilir.

---

## 9. Adım Adım DS_2 Yol Haritası ve Kod İskeletleri

### Adım 1: Python Sanal Ortamı ve Kütüphaneler
```bash
python3 -m venv venv
source venv/bin/activate
pip install pandas numpy matplotlib seaborn scikit-learn sqlalchemy psycopg2-binary
```

---

### Adım 2: Ex00 — `ds_2/ex00/pie.py`
```python
import matplotlib.pyplot as plt
import pandas as pd
from sqlalchemy import create_engine

# 1. PostgreSQL bağlantısı
engine = create_engine("postgresql+psycopg2://acosgun:mysecretpassword@localhost:5432/piscineds")

# 2. Olay türlerini say
query = """
SELECT event_type, COUNT(*) AS count
FROM customers
GROUP BY event_type
ORDER BY count DESC;
"""
df = pd.read_sql(query, engine)

# 3. Pie Chart çizimi
plt.figure(figsize=(8, 8))
plt.pie(df["count"], labels=df["event_type"], autopct="%1.1f%%", startangle=140)
plt.title("Distribution of Customer Events")
plt.tight_layout()
plt.show()
```

---

### Adım 3: Ex01 — `ds_2/ex01/chart.py`
```python
import matplotlib.pyplot as plt
import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("postgresql+psycopg2://acosgun:mysecretpassword@localhost:5432/piscineds")

query = """
SELECT 
    DATE_TRUNC('month', event_time) AS month,
    COUNT(DISTINCT user_id) AS customer_count,
    SUM(price) AS total_sales
FROM customers
WHERE event_type = 'purchase'
GROUP BY DATE_TRUNC('month', event_time)
ORDER BY month;
"""
df = pd.read_sql(query, engine)
df["month_label"] = pd.to_datetime(df["month"]).dt.strftime("%b")
df["total_sales_million"] = df["total_sales"] / 1_000_000
df["avg_spend"] = df["total_sales"] / df["customer_count"]

fig, axes = plt.subplots(1, 3, figsize=(18, 5))

# 1. Number of customers
axes[0].plot(df["month_label"], df["customer_count"], marker="o", color="royalblue")
axes[0].set_title("Number of Customers")
axes[0].set_ylabel("Customers")

# 2. Total sales in million A
axes[1].bar(df["month_label"], df["total_sales_million"], color="forestgreen", alpha=0.7)
axes[1].set_title("Total Sales (Million A)")
axes[1].set_ylabel("Million Altairian Dollars")

# 3. Average spend per customer
axes[2].plot(df["month_label"], df["avg_spend"], marker="s", color="darkorange")
axes[2].set_title("Average Spend / Customer")
axes[2].set_ylabel("A per Customer")

plt.tight_layout()
plt.show()
```

---

### Adım 4: Ex02 — `ds_2/ex02/mustache.py`
```python
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sqlalchemy import create_engine

engine = create_engine("postgresql+psycopg2://acosgun:mysecretpassword@localhost:5432/piscineds")

# Ürün fiyatlarını çek
df = pd.read_sql("SELECT price FROM customers WHERE event_type = 'purchase';", engine)

# İstatistikler
print("=== Satın Alınan Ürün Fiyat İstatistikleri ===")
print(df["price"].describe())

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# 1. Item Price Box Plot
sns.boxplot(ax=axes[0], x=df["price"], color="skyblue")
axes[0].set_title("Purchased Item Prices")
axes[0].set_xlabel("Price (Altairian Dollars)")

# 2. User Average Basket Price Box Plot
basket_df = pd.read_sql("""
    SELECT user_id, AVG(session_total) as avg_basket
    FROM (
        SELECT user_id, user_session, SUM(price) as session_total
        FROM customers
        WHERE event_type = 'purchase'
        GROUP BY user_id, user_session
    ) t
    GROUP BY user_id;
""", engine)

sns.boxplot(ax=axes[1], x=basket_df["avg_basket"], color="lightgreen")
axes[1].set_title("Average Basket Price per User")
axes[1].set_xlabel("Basket Price (Altairian Dollars)")

plt.tight_layout()
plt.show()
```

---

### Adım 5: Ex03 — `ds_2/ex03/Building.py`
```python
import matplotlib.pyplot as plt
import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("postgresql+psycopg2://acosgun:mysecretpassword@localhost:5432/piscineds")

# Müşteri bazında frekans ve parasal tutar
rfm_raw = pd.read_sql("""
    SELECT user_id, COUNT(*) AS frequency, SUM(price) AS monetary
    FROM customers
    WHERE event_type = 'purchase'
    GROUP BY user_id;
""", engine)

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Sipariş sıklığı (Frequency)
axes[0].hist(rfm_raw["frequency"], bins=30, range=(0, 30), color="purple", edgecolor="black")
axes[0].set_title("Number of Orders according to Frequency")
axes[0].set_xlabel("Frequency (Order Count)")
axes[0].set_ylabel("Customers")

# Harcama miktarı (Monetary)
axes[1].hist(rfm_raw["monetary"], bins=30, range=(0, 250), color="teal", edgecolor="black")
axes[1].set_title("Altairian Dollars Spent by Customers")
axes[1].set_xlabel("Monetary Value in A")
axes[1].set_ylabel("Customers")

plt.tight_layout()
plt.show()
```

---

### Adım 6: Ex04 — `ds_2/ex04/elbow.py`
```python
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sqlalchemy import create_engine

engine = create_engine("postgresql+psycopg2://acosgun:mysecretpassword@localhost:5432/piscineds")

# RFM Tablosunu oluştur
rfm = pd.read_sql("""
    SELECT 
        user_id,
        EXTRACT(DAY FROM (NOW() - MAX(event_time))) AS recency,
        COUNT(*) AS frequency,
        SUM(price) AS monetary
    FROM customers
    WHERE event_type = 'purchase'
    GROUP BY user_id;
""", engine)

# Ölçeklendirme
scaler = StandardScaler()
X_scaled = scaler.fit_transform(rfm[["recency", "frequency", "monetary"]])

# Elbow döngüsü
inertias = []
K_range = range(1, 11)
for k in K_range:
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    kmeans.fit(X_scaled)
    inertias.append(kmeans.inertia_)

# Çizim
plt.figure(figsize=(8, 5))
plt.plot(K_range, inertias, marker="o", color="crimson")
plt.title("The Elbow Method")
plt.xlabel("Number of clusters (k)")
plt.ylabel("Inertia (WCSS)")
plt.grid(True)
plt.show()
```

---

### Adım 7: Ex05 — `ds_2/ex05/Clustering.py`
```python
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sqlalchemy import create_engine

engine = create_engine("postgresql+psycopg2://acosgun:mysecretpassword@localhost:5432/piscineds")

# RFM verisini çek
rfm = pd.read_sql("""
    SELECT 
        user_id,
        EXTRACT(DAY FROM (NOW() - MAX(event_time))) AS recency,
        COUNT(*) AS frequency,
        SUM(price) AS monetary
    FROM customers
    WHERE event_type = 'purchase'
    GROUP BY user_id;
""", engine)

scaler = StandardScaler()
features = ["recency", "frequency", "monetary"]
X_scaled = scaler.fit_transform(rfm[features])

# Optimum k=4 ile kümeleme
kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
rfm["cluster"] = kmeans.fit_predict(X_scaled)

# Kümeleri profilleyip isimlendirelim
cluster_summary = rfm.groupby("cluster")[features].mean()
print("Kümelerin Ortalama Değerleri:")
print(cluster_summary)

# Örnek İsimlendirme Eşleştirmesi (Profil sonuçlarına göre):
segment_names = {
    0: "Loyal Customers",
    1: "New Customers",
    2: "Inactive Customers",
    3: "Platinum VIP"
}
rfm["segment"] = rfm["cluster"].map(segment_names)

# GRAFİK 1: Segment Büyüklükleri (Bar Plot)
plt.figure(figsize=(8, 4))
sns.countplot(data=rfm, y="segment", palette="Set2")
plt.title("Customer Distribution by Segment")
plt.xlabel("Number of Customers")
plt.tight_layout()
plt.show()

# GRAFİK 2: Kümeler ve Centroidler (Scatter Plot: Recency vs Frequency)
plt.figure(figsize=(9, 6))
sns.scatterplot(data=rfm, x="recency", y="frequency", hue="segment", alpha=0.6, palette="Set1")

# Centroidleri orijinal ölçeğe geri çevirip çizelim
centroids = scaler.inverse_transform(kmeans.cluster_centers_)
plt.scatter(centroids[:, 0], centroids[:, 1], s=250, c="yellow", edgecolor="black", marker="X", label="Centroids")

plt.title("Customer Clusters with Centroids")
plt.xlabel("Recency (Days)")
plt.ylabel("Frequency (Orders)")
plt.legend()
plt.tight_layout()
plt.show()
```

---

## 10. Peer-Evaluation (Savunma) Taktikleri

Evaluator geldiğinde kendinizden emin bir şekilde şu yanıtları verin:

1. **"Neden Python ve Matplotlib seçtin?"**  
   *"PostgreSQL veriyi saklamak ve SQL ile ağır filtrelemeyi yapmak için harika; ancak görselleştirme, istatistiksel dağılımlar ve makine öğrenimi algoritmaları için sektör standardı Python ekosistemidir (Pandas, Seaborn, Scikit-Learn)."*
2. **"Neden K-Means ve RFM kullandın?"**  
   *"E-ticaret sektöründe müşteriyi doğrudan etiketleyen bir sütun bulunmaz. Müşteriyi en iyi tanımlayan 3 davranışsal özellik vardır: Ne zaman geldi (Recency), ne sıklıkla geldi (Frequency) ve ne kadar harcadı (Monetary). Bu metrikleri StandardScaler ile normalize edip K-Means ile benzer müşterileri kümeledim."*
3. **"Neden 4 küme seçtin?"**  
   *"Ex04'teki Elbow Method grafiğimde $k=4$ noktasına kadar Inertia çok hızlı düşerken, 4'ten sonra düşüş hızı plato çizdi. Matematiksel dirsek noktası $k=4$'tü ve bu da pazarlama ekibinin yönetebileceği 4 mantıklı gruba (Yeni, Sadık, Uyuyan, VIP) tam olarak karşılık geldi."*
4. **"Grafikteki sarı 'X' işaretleri neyi temsil ediyor?"**  
   *"Onlar her kümenin ağırlık merkezi olan Centroid'lerdir. O gruptaki tüm müşterilerin koordinatlarının aritmetik ortalamasıdır."*
5. **"PDF'deki '??' işaretleri neydi?"**  
   *"Onlar yazarın koyduğu placeholder'lardı. Her öğrencinin kendi veri setinde hesaplayacağı dinamik değerleri simgeliyordu. Ben de kendi modelimin ürettiği ortalamaları grafiğime yansıttım."*

---

## 11. Ex00 Soru ve Cevapları

Bu bölüm, `ds_2/ex00/pie.py` scriptinde kullanılan mimariyi, kütüphanelerin iç mekanizmalarını, subject isterlerini ve sektördeki veri bilimi pratiklerini en ince ayrıntısına kadar açıklar.

---

### 1. `pie.py` Kodunun Genel Mimarisi ve Akışı

`pie.py` kodu, klasik bir **Veri Ambarından Analitik Görselleştirme Üretme** boru hattıdır (Data Pipeline):

```
┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐
│   PostgreSQL    │ ───►  │   SQLAlchemy    │ ───►  │     Pandas      │ ───►  │   Matplotlib    │
│  (customers db) │ (SQL) │ (Bağlantı Havuzu│ (df)  │ (Veri İnceleme  │       │  (Pie Chart GUI │
│  19M+ Satır     │       │  engine.connect)│       │  Counts/Types)  │       │   Penceresi)    │
└─────────────────┘       └─────────────────┘       └─────────────────┘       └─────────────────┘
```

1. **Bağlantı Tanımı:** `create_engine` ile veritabanının adresi ve kimlik bilgileri tanımlanır.
2. **Sorgu Çalıştırma:** `with engine.connect()` ile veritabanı havuzundan bir bağlantı alınır ve SQL sorgusu PostgreSQL'e iletilir.
3. **DataFrame Oluşturma:** PostgreSQL 19+ milyon satırı kendi içinde toplayıp sadece 4 satırlık sonucu Pandas `DataFrame` nesnesi olarak Python'a döndürür.
4. **Veri Ayrıştırma:** Olay türleri ve sayıları kolonlardan okunur.
5. **Görselleştirme:** Matplotlib `plt.pie` fonksiyonu bu 4 sayıyı orantılayarak pasta grafiği çizer ve `plt.show()` ile masaüstünde pencere olarak görüntüler.

---

### 2. Alt Soruların Detaylı Açıklamaları

---

#### a) SQLAlchemy Nedir, Ne İçin Kullanılır? `create_engine` Fonksiyonu Detayları

- **SQLAlchemy Nedir?**  
  Python ekosisteminin en kapsamlı ve sektör standardı **Veritabanı Araç Takımı (Database Toolkit)** ve **ORM (Object Relational Mapper)** kütüphanesidir. İki katmandan oluşur:
  1. *Core (Çekirdek):* Veritabanı bağlantı havuzlarını (connection pooling), dialect çeviricilerini ve ham SQL işlemlerini yönetir.
  2. *ORM:* Veritabanı tablolarını Python sınıfları (class) ile eşler. Bu projede doğrudan SQL çalıştırdığımız için **Core** yeteneklerini kullanıyoruz.

- **`create_engine` Fonksiyonu Nedir ve Nasıl Çalışır?**  
  Veritabanıyla iletişim kuracak olan merkezi yönetim nesnesini (`Engine`) üretir.  
  > [!NOTE]
  > **Önemli Mantık (Lazy Initialization):** `create_engine(...)` satırı çalıştığı anda fiziksel olarak veritabanına bağlanmaz! Yalnızca bağlantı kurallarını ve havuzunu hazırlar. Gerçek fiziksel bağlantı, ilk sorgu atıldığında veya `engine.connect()` dendiğinde kurulur.

- **Parametreleri:**
  - **`url` (1. zorunlu parametre):** Bağlantı URL dizesidir.  
    Format: `dialect+driver://username:password@host:port/database`
    - `postgresql`: Veritabanı motoru (dialect)
    - `psycopg2`: Python ile PostgreSQL arasındaki C tabanlı sürücü (driver)
    - `acosgun:mysecretpassword`: Kullanıcı adı ve parola
    - `localhost:5432`: Sunucu adresi ve varsayılan PostgreSQL portu
    - `piscineds`: Hedef veritabanı adı
  - **`echo=False` (Opsiyonel, bool):** `True` yapılırsa, arka planda çalıştırılan tüm saf SQL komutları terminale loglanır (debug için çok faydalıdır).
  - **`pool_size=5` (Opsiyonel, int):** Havuzda sürekli açık tutulacak bağlantı sayısı.
  - **`max_overflow=10` (Opsiyonel, int):** Havuz dolduğunda geçici açılabilecek ekstra bağlantı kotası.

- **Dönüş Değeri:**  
  Bir `sqlalchemy.engine.base.Engine` nesnesi döndürür. Bu nesne bağlantı havuzunu (Pool) ve SQL çeviricisini (Dialect) içinde barındırır.

---

#### b) Veritabanı Şifresinin Kodda Açık Olması ve `ds_2.pdf` İncelemesi

- **`ds_2.pdf` Subject Dosyası Ne Diyor?**  
  Subject dosyasının 3. ve 14. sayfaları incelendiğinde:
  - Turn-in dosyaları yalnızca `pie.*`, `chart.*`, `mustache.*`, `Building.*`, `elbow.*`, `Clustering.*` olarak sınırlandırılmıştır.
  - Bir `.env` dosyası, `requirements.txt` veya ekstra konfigürasyon dosyası teslim etmeniz **istenmemektedir**.
  - Sayfa 14'teki kural: *"The evaluation process will happen on the computer of the evaluated group."* (Değerlendirme sizin bilgisayarınızda yapılacaktır).
  - Havuz projelerinde Docker ortamı ve veritabanı kimlik bilgileri (`acosgun:mysecretpassword`, `localhost:5432/piscineds`) ödev konusu gereği sabittir.

- **Şifreyi Gizlemek / `.env` Oluşturmak Bekleniyor mu?**  
  **Hayır, bu projede beklenmiyor.** Şifrenin kod içinde açık (hardcoded) olması puan kırdırmaz. Hatta evaluator kodunuzu çalıştırdığında ekstra bir ortam değişkeni ayarlamak zorunda kalmadan doğrudan `python pie.py` yazıp sonucu görmesini sağlar.

- **Sektör Standardı Nedir?**  
  Gerçek şirket projelerinde şifreler **asla** koda yazılmaz. `python-dotenv` kütüphanesiyle `.env` dosyasından veya Kubernetes/Cloud Secret Manager üzerinden çekilir:
  ```python
  import os
  db_password = os.getenv("DB_PASSWORD")
  ```
  Savunmada evaluatöre *"Gerçek hayatta burayı `os.getenv` ile `.env`'den çekeriz ancak 42 değerlendirme ortamında tak-çalıştır olabilmesi için sabit bıraktım"* demeniz tam puanlık bir veri mühendisi refleksidir.

---

#### c) Bu Projede Flake8 Kurallarına Uymak Bekleniyor mu?

- **`ds_2.pdf` İncelemesi:**  
  Subject'in 3. sayfasında *"You are free to use any language of your choice for this module"* ve her egzersizde *"Allowed functions: All"* denmektedir.
- Projede Python zorunlu dahi tutulmamış (R, C++, Julia vb. serbesttir). Dolayısıyla 42 C havuzundaki **Norminette gibi zorunlu bir Flake8 kontrol mekanizması YOKTUR.**
- Flake8 uyumsuzluğu (örneğin 79 karakteri aşan satırlar, girintiler) projenin başarısız olmasına sebep olmaz. Ancak kodunuzun temiz, okunabilir ve PEP 8 standartlarına yakın olması peer-evaluation sırasında evaluatörün gözünde güvenilirliğinizi artırır.

---

#### d) SQL Tarafında Gruplama vs. Python'da Filtreleme: Hangisi Neden Tercih Edilir?

**Kesinlikle ve tartışmasız SQL tarafında gruplama tercih edilir!**

| Kriter | SQL'de Gruplama (`GROUP BY`) | Python'da Gruplama (`df.groupby`) |
|---|---|---|
| **Veri Transferi (Ağ/Disk)** | Yalnızca **4 satır** (birkaç bayt) çekilir. | **19.175.907 satır** (~2 GB ham veri) çekilir. |
| **RAM (Bellek) Tüketimi** | Neredeyse 0 MB RAM harcar. | Python belleğinde 2-3 GB yer kaplar, sistemi dondurabilir. |
| **İşlem Süresi** | C ile yazılmış PostgreSQL motorunda **1-2 saniye**. | Ağdan transfer dakikalar sürer, Python'da OOM (Out Of Memory) çökmesi yaşanabilir. |

> [!IMPORTANT]
> **Sektörün Altın Kuralı (Compute Pushdown):**  
> *"Veriyi hesaplamaya götürme; hesaplamayı verinin durduğu yere (veritabanına) götür."*  
> Veri Bilimciler ve Veri Mühendisleri, filtreleme, birleştirme (JOIN) ve toplulaştırma (Aggregation) işlemlerini her zaman veritabanı motoruna yaptırır; Python'a yalnızca özetlenmiş temiz sonucu çeker.

---

#### e) Her Alıştırmada Yeni Engine/Bağlantı/Tablo mu Açılmalı?

- **Tablo Açısından:**  
  **Kesinlikle hayır!** Yeni bir tablo oluşturmuyorsunuz. DS_1'de hazırladığınız tek bir `customers` tablosu vardır. `ex00`, `ex01`, `ex02`, `ex03`, `ex04` ve `ex05` alıştırmalarının tümü bu aynı `customers` tablosundan beslenir (salt okunur / read-only).
- **Engine ve Bağlantı Açısından (42 Standartları):**  
  42 değerlendirmesinde her alıştırma bağımsız olarak test edilir:  
  Evaluatör önce `cd ex00 && python pie.py` çalıştırır, sonra `cd ../ex01 && python chart.py` çalıştırır.  
  Her klasörün kendi kendine yeten bağımsız bir script (**self-contained script**) olması zorunludur. Bu yüzden her alıştırma dosyasında (`pie.py`, `chart.py`, vb.) bağlantı satırını (`engine = create_engine(...)`) baştan yazmak 42 için en doğru yöntemdir.
- **Sektör Standardı:**  
  Büyük bir projede her dosyada connection string kopyalanmaz. Ortak bir `database.py` modülü yazılır ve diğer dosyalar `from database import get_connection` şeklinde merkezi bağlantıyı çağırır.

---

#### f) `engine.connect()` Kullanımı ve `Connection` Nesnesi Nedir?

- **Nasıl Çalışır?**  
  `engine.connect()` çağrıldığında SQLAlchemy arka plandaki bağlantı havuzundan (Connection Pool) hazırda bekleyen canlı bir veritabanı soketini (psycopg2 socket) ödünç alır.
- **Veri Tipi:**  
  `sqlalchemy.engine.base.Connection` sınıfına ait bir nesnedir.
- **Neden Context Manager (`with ... as connection`) ile Kullanılır?**  
  Veritabanı bağlantıları işletim sistemi kaynaklarıdır (file descriptor/socket). Eğer açık bırakılırlarsa veritabanı kilitlenir.  
  `with` bloğu tamamlandığında (veya bir hata fırlatıldığında), `connection` nesnesi **otomatik olarak havuza iade edilir (release back to pool)**. Fiziksel soket kapatılıp yok edilmez, bir sonraki sorgu için havuzda dinlenmeye çekilir.
- **Özellikleri:**  
  - `connection.execute(text("..."))`: Ham SQL çalıştırma imkanı sunar.
  - `connection.begin()` / `connection.commit()` / `connection.rollback()`: İşlem (transaction) yönetimini destekler.
  - Thread-safe'tir; çoklu iş parçacıklarında güvenle çalışır.

---

#### g) `pd.read_sql` Fonksiyonu Detayları ve `read_sql_query` Farkı

- **`pd.read_sql` Nedir?**  
  Pandas'ın SQL verilerini doğrudan `DataFrame` nesnesine dönüştüren ana köprü fonksiyonudur. Bir **"Dispatcher / Wrapper" (Yönlendirici Çatı Fonksiyon)** olarak çalışır:
  - Eğer parametre olarak bir SQL sorgu metni verirseniz (`SELECT ...`), arka planda otomatik olarak `pd.read_sql_query()` fonksiyonunu çalıştırır.
  - Eğer parametre olarak sadece bir tablo adı verirseniz (`"customers"`), arka planda `pd.read_sql_table()` fonksiyonunu çalıştırır.

- **Temel Parametreleri:**
  1. `sql`: Çalıştırılacak SQL sorgu metni (`str` veya `sqlalchemy.text`) ya da tablo adı.
  2. `con`: SQLAlchemy `Engine` veya `Connection` nesnesi (bağlantı kaynağı).
  3. `index_col` (Opsiyonel): Çekilen kolonlardan birini DataFrame'in satır indeksi yapmak için kullanılır (Örn: `index_col='event_type'`).
  4. `params` (Opsiyonel): SQL injection'ı önlemek için sorguya güvenli parametre geçmek için kullanılır (Örn: `params={'tip': 'purchase'}`).
  5. `parse_dates` (Opsiyonel): Tarih kolonlarını otomatik olarak Python `datetime` tipine çevirir (Örn: `parse_dates=['event_time']`).
  6. `chunksize` (Opsiyonel, int): Milyonlarca satırı parça parça (chunk) okumak için generator üretir.

- **Dönüş Değeri:**  
  SQL sonucundaki kolon isimlerini sütun başlığı, satırları da kayıtlar olarak içeren bir **`pandas.DataFrame`** nesnesidir.

- **`read_sql` vs `read_sql_query` Farkı:**  
  Teknik olarak `read_sql` sorgu verildiğinde zaten `read_sql_query`'yi çağırır. Doğrudan `read_sql_query` kullanmak niyetinizi ("ben sadece sorgu çalıştıracağım, tablo adı vermeyeceğim") daha belirgin hale getirir; ancak pratikte ikisi de tamamen aynı sonucu üretir.

---

#### h) `plt.pie` Kullanımı ve Parametreleri Detayları

Matplotlib'in dairesel pasta grafiği çizim fonksiyonudur.

```python
plt.pie(
    counts,
    labels=event_types,
    autopct="%1.1f%%",
    startangle=140,
    colors=['#4C72B0', '#55A868', '#C44E52', '#8172B3'],
    explode=(0, 0.05, 0, 0),
    shadow=True
)
```

- **`x` (1. parametre, örn: `counts`):**  
  Dilimlerin büyüklüklerini belirleyen sayısal dizi. Matplotlib bu sayıların toplamını alır ve her bir sayının toplama oranına göre dilim açısını ($360^\circ \times \frac{değer}{toplam}$) hesaplar.
- **`labels` (örn: `event_types`):**  
  Her dilimin dış kenarına yazılacak isimler listesi (`view`, `cart` vb.).
- **`autopct` (Automatic Percentage Format):**  
  Dilimlerin **içine** yüzdelik değerleri otomatik hesaplayıp yazdırma formatıdır.
  - **`"%1.1f%%"` Şablonunun Deşifresi:**
    - `%`: Format belirtecinin başlangıcı.
    - `1.1f`: Değeri ondalıklı sayı (float) olarak yazdır; virgülden sonra **1 basamak** göster (Örn: `50.3%`). Eğer `"%1.2f%%"` yazsaydınız `50.34%` yazardı.
    - `%%`: Python formatlama dilinde ekrana gerçek bir `%` işareti basmak için çift yüzde kullanılır.
  - İstenirse buraya bir lambda fonksiyonu verilerek hem yüzde hem de gerçek adet aynı anda yazdırılabilir.
- **`startangle`:**  
  İlk dilimin saat 3 hizasından (matematiksel $0^\circ$) itibaren saatin tersi yönünde kaç derece döndürülerek çizilmeye başlanacağını belirler. `startangle=140` pastayı daha estetik ve dengeli konumlandırır.
- **`colors`:** Dilimlerin özel renk kodları listesi.
- **`explode`:** Vurgulanmak istenen bir dilimi pastadan birkaç milimetre dışarı fırlatmak için kullanılır (Örn: `(0, 0.1, 0, 0)` sepete ekleme dilimini dışarı kaydırır).
- **`shadow=True`:** Pastanın altına hafif bir 3D derinlik gölgesi ekler.

---

#### j) `plt.tight_layout()` Kullanmazsak Ne Olur? Ne İşe Yarar?

- **Kullanmazsak Ne Olur?**  
  Matplotlib varsayılan olarak grafik penceresinin kenar boşluklarını (margins) sabit bırakır.  
  Eğer etiketleriniz uzunsa, grafik başlığınız iki satırsa veya pasta grafiğinin dilim yazıları dışarı taşıyorsa, bu yazılar **pencerenin kenarından kesilir (clipping problemi)** veya pencere dışına taşarak görünmez hale gelir.
- **Ne Yapar?**  
  `plt.tight_layout()`, figürdeki tüm görsel nesnelerin (başlıklar, eksen etiketleri, dilim yazıları, alt grafikler) sınırlarını dinamik olarak hesaplar ve kenar boşluklarını milimetrik olarak yeniden ayarlar. Böylece tüm metinler pencereye eksiksiz, ferah ve sıkışmadan sığar.
- **Hangi Durumlarda Hayat Kurtarır?**  
  Özellikle Ex01, Ex02 ve Ex03'te yan yana 2 veya 3 alt grafik (`plt.subplots(1, 3)`) çizdirdiğimizde grafiklerin eksen yazılarının birbirinin üstüne binmesini engellemek için **zorunlu bir sektörel standarttır**.

---

  # 12. Ex01 Soru ve Cevapları

---

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


