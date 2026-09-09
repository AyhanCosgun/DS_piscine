# Seaborn Rehberi

## Sıfırdan başlayanlar için Seaborn + Matplotlib karşılaştırmalı anlatım

> **Kısa cevap:** Seaborn, Python'da istatistiksel veri görselleştirmeyi
> kolaylaştıran, Matplotlib üzerine kurulmuş yüksek seviyeli bir
> görselleştirme kütüphanesidir.
>
> Matplotlib "grafiğin her parçasını kontrol edeyim" yaklaşımında çok
> güçlüdür. Seaborn ise "veri setimi verip hızlıca anlamlı ve güzel bir
> grafik oluşturayım" yaklaşımını öne çıkarır.
>
> Bu nedenle Seaborn, Matplotlib'in yerine geçmekten çok **Matplotlib'i
> tamamlar**.

------------------------------------------------------------------------

# 1. Önce büyük resmi anlayalım

Python'da veri görselleştirme dünyasını kabaca şöyle düşünebilirsin:

``` text
                    Python
                      |
             Veri görselleştirme
                      |
          +-----------+-----------+
          |                       |
      Matplotlib               Seaborn
          |                       |
   Düşük/orta seviye        Yüksek seviye
   ayrıntılı kontrol        hızlı istatistiksel
                            grafikler
          \                       /
           \                     /
            +-------------------+
                  Birlikte
                 kullanılabilir
```

Seaborn, Matplotlib'in rakibi olarak ortaya çıkmış tamamen bağımsız bir
sistem değildir.

Seaborn'un önemli özelliklerinden biri, **Matplotlib'in üzerinde
çalışmasıdır**.

Bu yüzden şunu yapabilirsin:

``` python
import seaborn as sns
import matplotlib.pyplot as plt

sns.lineplot(data=df, x="date", y="sales")

plt.title("Daily Sales")
plt.xlabel("Date")
plt.ylabel("Sales")

plt.show()
```

Burada grafiği Seaborn oluştururken, `plt.title()`, `plt.xlabel()` ve
`plt.show()` gibi Matplotlib araçlarını kullanıyoruz.

Bu kombinasyon Seaborn kullanımının çok önemli bir parçasıdır.

------------------------------------------------------------------------

# 2. Matplotlib nedir?

Önce Matplotlib'i anlamak Seaborn'u anlamayı kolaylaştırır.

Örneğin:

``` python
import matplotlib.pyplot as plt

x = [1, 2, 3, 4, 5]
y = [10, 20, 15, 30, 25]

plt.plot(x, y)

plt.xlabel("X")
plt.ylabel("Y")
plt.title("My Graph")

plt.show()
```

Burada Matplotlib'e oldukça doğrudan talimat veriyoruz:

-   şu x değerlerini kullan
-   şu y değerlerini kullan
-   çizgi çiz
-   x ekseninin adını değiştir
-   y ekseninin adını değiştir
-   başlık ekle
-   grafiği göster

Matplotlib'in felsefesi büyük ölçüde:

> **"Grafiğin nasıl çizileceğini bana ayrıntılı olarak söyle."**

şeklindedir.

Bu çok güçlüdür.

Ama veri analizi sırasında sürekli aynı tür işlemleri yapıyorsan kod
biraz fazla ayrıntılı hale gelebilir.

------------------------------------------------------------------------

# 3. Seaborn neden ortaya çıktı?

Örneğin elinde şöyle bir DataFrame olduğunu düşün:

``` python
import pandas as pd

df = pd.DataFrame({
    "age": [20, 21, 22, 23, 24, 25],
    "salary": [20000, 22000, 25000, 28000, 30000, 35000]
})
```

İki değişken arasındaki ilişkiyi görmek istiyorsun.

Matplotlib ile:

``` python
plt.scatter(df["age"], df["salary"])
plt.xlabel("Age")
plt.ylabel("Salary")
plt.show()
```

Seaborn ile:

``` python
sns.scatterplot(data=df, x="age", y="salary")
plt.show()
```

Kodlar çok farklı görünmüyor.

Asıl fark daha büyük DataFrame'lerde ortaya çıkar.

Seaborn, özellikle **tabular data / DataFrame** ile çalışmayı merkeze
alır.

Örneğin:

``` python
sns.scatterplot(
    data=df,
    x="age",
    y="salary"
)
```

Burada Seaborn'a:

> "`df` içindeki `age` ve `salary` sütunlarını kullan"

diyorsun.

Bu yaklaşım veri analizi için çok kullanışlıdır.

------------------------------------------------------------------------

# 4. Seaborn'un en önemli avantajı: DataFrame odaklı olması

Diyelim ki:

``` python
df
```

şöyle:

    age   salary department
  ----- -------- ------------
     20    20000 IT
     21    22000 IT
     22    25000 Sales
     23    28000 Sales
     24    30000 IT
     25    35000 Sales

Şunu yazabilirsin:

``` python
sns.scatterplot(
    data=df,
    x="age",
    y="salary",
    hue="department"
)
```

`hue` sayesinde:

> department sütununa göre noktaların kategorilerini ayır

demiş oluyorsun.

Bu, Seaborn'un güçlü olduğu alanlardan biridir.

Matplotlib'de aynı işi elle yapmak mümkündür ama daha fazla kod yazman
gerekebilir.

------------------------------------------------------------------------

# 5. Seaborn ve Matplotlib arasındaki temel fark

En önemli ayrımı şöyle düşün:

## Matplotlib

``` text
Grafik nesnesi
     |
     +-- eksen
     +-- çizgi
     +-- nokta
     +-- başlık
     +-- legend
     +-- grid
     +-- renk
     +-- ...
```

Grafiğin her parçası üzerinde ayrıntılı kontrol sağlar.

## Seaborn

``` text
DataFrame
   |
   +-- x sütunu
   +-- y sütunu
   +-- kategori
   +-- renk
   +-- stil
   +-- boyut
          |
          v
      İstatistiksel
      grafik
```

Seaborn, veri sütunlarının anlamını kullanarak grafiği daha yüksek
seviyede tanımlamana izin verir.

------------------------------------------------------------------------

# 6. Seaborn'un Matplotlib'in yerine geçmediğini unutma

Bu çok önemli.

Şunu düşünme:

``` text
Matplotlib eski
Seaborn yeni
```

Bu doğru değildir.

Daha doğru bir model:

``` text
Matplotlib
   ↓
Temel grafik altyapısı
   ↑
Seaborn
   ↓
İstatistiksel / DataFrame odaklı
yüksek seviyeli arayüz
```

Seaborn kullanırken bile sık sık:

``` python
import matplotlib.pyplot as plt
```

kullanırsın.

Örneğin:

``` python
sns.lineplot(data=df, x="date", y="sales")

plt.title("Sales")
plt.xlabel("Date")
plt.ylabel("Revenue")

plt.tight_layout()
plt.show()
```

Burada:

-   Seaborn → grafiği oluşturuyor
-   Matplotlib → grafiğin geri kalanını kontrol ediyor

------------------------------------------------------------------------

# 7. Kurulum

Genellikle:

``` bash
pip install seaborn
```

ile kurulabilir.

Python kodunda:

``` python
import seaborn as sns
```

şeklinde import edilir.

Matplotlib:

``` python
import matplotlib.pyplot as plt
```

Seaborn:

``` python
import seaborn as sns
```

şeklinde kullanılır.

------------------------------------------------------------------------

# 8. İlk Seaborn grafiğimiz

En basit örneklerden biri:

``` python
import seaborn as sns
import matplotlib.pyplot as plt

x = [1, 2, 3, 4, 5]
y = [10, 20, 15, 30, 25]

sns.lineplot(x=x, y=y)

plt.show()
```

Burada:

``` python
sns.lineplot()
```

çizgi grafiği oluşturur.

------------------------------------------------------------------------

# 9. Seaborn ile DataFrame kullanmak

Daha gerçekçi kullanım:

``` python
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.DataFrame({
    "month": ["Jan", "Feb", "Mar", "Apr"],
    "sales": [100, 120, 150, 130]
})

sns.lineplot(
    data=df,
    x="month",
    y="sales"
)

plt.show()
```

Burada:

``` python
data=df
```

Seaborn'a veri kaynağını söylüyor.

``` python
x="month"
```

x ekseninin hangi sütun olduğunu söylüyor.

``` python
y="sales"
```

y ekseninin hangi sütun olduğunu söylüyor.

Bu yapı Seaborn'da tekrar tekrar karşına çıkacaktır.

------------------------------------------------------------------------

# 10. `data`, `x` ve `y` mantığını oturt

Seaborn öğrenirken en önemli şeylerden biri budur.

Genellikle:

``` python
sns.someplot(
    data=df,
    x="column1",
    y="column2"
)
```

şeklinde düşün.

Örneğin:

``` python
sns.scatterplot(
    data=df,
    x="height",
    y="weight"
)
```

şunu demektir:

``` text
df
 |
 +-- height → x
 |
 +-- weight → y
```

------------------------------------------------------------------------

# 11. Line plot

Çizgi grafiği:

``` python
sns.lineplot(
    data=df,
    x="date",
    y="sales"
)
```

Örneğin zaman serilerinde çok kullanışlıdır.

Senin önceki örneğine benzer:

``` python
sns.lineplot(
    data=df_daily,
    x="day_date",
    y="customer_count"
)
```

Ardından Matplotlib ile:

``` python
plt.ylabel("Number of customers")
plt.tight_layout()
plt.show()
```

------------------------------------------------------------------------

# 12. Scatter plot

İki sayısal değişken arasındaki ilişkiyi görmek için:

``` python
sns.scatterplot(
    data=df,
    x="age",
    y="salary"
)
```

Örneğin:

``` text
salary
  |
  |              •
  |          •
  |       •
  |    •
  | •
  +---------------- age
```

------------------------------------------------------------------------

# 13. `hue`: kategorilere göre renk

Seaborn'un en kullanışlı özelliklerinden biri:

``` python
sns.scatterplot(
    data=df,
    x="age",
    y="salary",
    hue="department"
)
```

Burada:

``` python
hue="department"
```

şu anlama gelir:

> department değerlerini renklerle ayır.

Örneğin:

``` text
IT      → bir renk
Sales   → başka renk
HR      → başka renk
```

Bu özellik özellikle veri analizi sırasında çok kullanışlıdır.

------------------------------------------------------------------------

# 14. `style`: kategorilere göre şekil

Sadece renk değil, marker şekli de değiştirebilirsin:

``` python
sns.scatterplot(
    data=df,
    x="age",
    y="salary",
    hue="department",
    style="department"
)
```

Böylece kategoriler hem renk hem şekil ile ayrılabilir.

------------------------------------------------------------------------

# 15. `size`: kategoriye göre nokta büyüklüğü

Örneğin:

``` python
sns.scatterplot(
    data=df,
    x="age",
    y="salary",
    size="experience"
)
```

Burada `experience` değeri arttıkça noktaların boyutu değişebilir.

Böylece tek grafikte birden fazla boyutu gösterebilirsin.

------------------------------------------------------------------------

# 16. Bar plot

Kategorik verileri karşılaştırmak için:

``` python
sns.barplot(
    data=df,
    x="department",
    y="salary"
)
```

Burada önemli bir nokta var:

Seaborn'un `barplot` fonksiyonu sadece "veriyi çiz" mantığında değildir.

Varsayılan davranışında kategoriler için **istatistiksel bir özet**
hesaplar.

Örneğin:

``` text
department    salary
IT            30000
IT            40000
IT            50000
```

için barplot ortalama maaşı gösterebilir.

Yani:

``` text
raw data
   ↓
istatistiksel aggregation
   ↓
grafik
```

------------------------------------------------------------------------

# 17. Count plot

Kategorilerin kaç defa bulunduğunu görmek için:

``` python
sns.countplot(
    data=df,
    x="department"
)
```

Örneğin:

``` text
IT       █████████
Sales    ██████
HR       ███
```

Burada ayrıca y sütunu vermen gerekmez.

Seaborn kategorilerin kaç kez tekrarlandığını sayar.

------------------------------------------------------------------------

# 18. Histogram

Bir sayısal değişkenin dağılımını görmek için:

``` python
sns.histplot(
    data=df,
    x="age"
)
```

Histogram:

``` text
frekans
  |
  |       ███
  |   █   ███
  |   █ █ ███
  | █ █ ███ █
  +----------------
        age
```

------------------------------------------------------------------------

# 19. KDE

Dağılımın daha yumuşak bir tahminini görmek için:

``` python
sns.kdeplot(
    data=df,
    x="salary"
)
```

KDE:

> Kernel Density Estimate

anlamına gelir.

Histogram gibi "kaç tane gözlem hangi aralıkta?" sorusunu görmeye
yardımcı olur fakat dağılımı daha sürekli bir eğri şeklinde gösterir.

------------------------------------------------------------------------

# 20. Box plot

İstatistiksel veri analizinde çok önemli grafiklerden biridir:

``` python
sns.boxplot(
    data=df,
    x="department",
    y="salary"
)
```

Box plot özellikle:

-   medyan
-   çeyrekler
-   dağılım
-   aykırı değerler

hakkında fikir verir.

Kabaca:

``` text
       |
       |
   ┌───┴───┐
   │       │
───┤  ───  ├───
   │       │
   └───┬───┘
       |
       •
```

------------------------------------------------------------------------

# 21. Violin plot

Box plot ile KDE'nin fikirlerini birleştiren grafiklerden biri:

``` python
sns.violinplot(
    data=df,
    x="department",
    y="salary"
)
```

Dağılımın şeklini daha ayrıntılı gösterebilir.

------------------------------------------------------------------------

# 22. Pairplot

Seaborn'un çok güzel özelliklerinden biri:

``` python
sns.pairplot(df)
```

DataFrame'deki birden fazla sayısal değişkenin ikili ilişkilerini
topluca incelemene yardımcı olur.

Örneğin:

``` text
       age   salary   exp
age      •      •      •
salary   •      •      •
exp      •      •      •
```

Bu özellikle veri setini ilk keşfederken kullanışlıdır.

------------------------------------------------------------------------

# 23. Heatmap

Bir matrisin değerlerini renk yoğunluğu ile göstermek için:

``` python
sns.heatmap(data)
```

En sık kullanım alanlarından biri korelasyon matrisidir.

Örneğin:

``` python
corr = df.corr(numeric_only=True)

sns.heatmap(
    corr,
    annot=True
)

plt.show()
```

`annot=True` hücrelerin içinde sayısal değerlerin de gösterilmesini
sağlar.

------------------------------------------------------------------------

# 24. `sns.set_theme()` nedir?

Senin önceki sorundaki Figure 1 → Figure 2 dönüşümünde kullandığımız:

``` python
sns.set_theme()
```

Seaborn'un genel görsel temasını etkinleştirir.

Örneğin:

``` python
import seaborn as sns

sns.set_theme()
```

sonrasında oluşturulan grafiklerin genel görünümü değişir.

Bu yüzden:

``` python
sns.set_theme()

plt.plot(x, y)
plt.show()
```

gibi bir kullanım bile Matplotlib grafiğinin görünümünü değiştirebilir.

Bu çok önemli bir ayrıntıdır:

> Seaborn kullanmak için mutlaka `sns.lineplot()` kullanmak zorunda
> değilsin.

Seaborn'un tema/stil ayarlarını kullanıp grafiği Matplotlib ile de
çizebilirsin.

------------------------------------------------------------------------

# 25. Seaborn sadece grafik fonksiyonlarından ibaret değildir

Seaborn'da iki şeyi birbirinden ayır:

## A. Grafik oluşturma

``` python
sns.lineplot(...)
sns.scatterplot(...)
sns.barplot(...)
sns.boxplot(...)
```

## B. Görsel tema/stil

``` python
sns.set_theme()
```

Bu yüzden:

``` python
sns.set_theme()

plt.plot(x, y)

plt.show()
```

geçerli ve mantıklı bir kullanımdır.

------------------------------------------------------------------------

# 26. Seaborn stilleri

Seaborn'da farklı stil seçenekleri bulunur.

Örneğin:

``` python
sns.set_style("whitegrid")
```

veya:

``` python
sns.set_style("darkgrid")
```

veya:

``` python
sns.set_style("white")
```

veya:

``` python
sns.set_style("dark")
```

Örneğin:

``` python
sns.set_style("whitegrid")

plt.plot(x, y)
plt.show()
```

Bu özellikle grid görünümünü değiştirmek için kullanışlıdır.

------------------------------------------------------------------------

# 27. Figure 1'ini Figure 2'ye yaklaştırmak

Senin önceki kodun:

``` python
fig1 = plt.figure(figsize=(10, 8))

plt.plot(
    df_daily["day_date"],
    df_daily["customer_count"]
)

plt.ylabel(
    "Number of customers",
    fontsize=14
)

plt.grid()

plt.tight_layout()
plt.show()
```

Seaborn teması eklenmiş hali:

``` python
import seaborn as sns
import matplotlib.pyplot as plt

sns.set_theme()

fig1 = plt.figure(figsize=(10, 8))

plt.plot(
    df_daily["day_date"],
    df_daily["customer_count"]
)

plt.ylabel(
    "Number of customers",
    fontsize=14
)

plt.tight_layout()
plt.show()
```

Burada grafiği hâlâ:

``` python
plt.plot()
```

ile çiziyorsun.

Sadece:

``` python
sns.set_theme()
```

ile Seaborn'un stil ayarlarını kullanıyorsun.

------------------------------------------------------------------------

# 28. Aynı grafiği Seaborn ile çizmek

Alternatif olarak:

``` python
sns.set_theme()

fig1 = plt.figure(figsize=(10, 8))

sns.lineplot(
    data=df_daily,
    x="day_date",
    y="customer_count"
)

plt.ylabel("Number of customers", fontsize=14)

plt.tight_layout()
plt.show()
```

Burada:

``` python
plt.plot()
```

yerine:

``` python
sns.lineplot()
```

kullanılmış oldu.

------------------------------------------------------------------------

# 29. `plt.plot()` ile `sns.lineplot()` arasındaki temel fark

Matplotlib:

``` python
plt.plot(
    df_daily["day_date"],
    df_daily["customer_count"]
)
```

Burada iki diziyi doğrudan veriyorsun:

``` text
x → df_daily["day_date"]
y → df_daily["customer_count"]
```

Seaborn:

``` python
sns.lineplot(
    data=df_daily,
    x="day_date",
    y="customer_count"
)
```

Burada DataFrame'i verip sütunların adlarını söylüyorsun:

``` text
data → df_daily
x    → "day_date"
y    → "customer_count"
```

Seaborn'un DataFrame odaklı yaklaşımı burada açıkça görülüyor.

------------------------------------------------------------------------

# 30. `palette`

Kategorilere göre renk seçmek için:

``` python
sns.scatterplot(
    data=df,
    x="age",
    y="salary",
    hue="department",
    palette="Set2"
)
```

`palette`, kategorik değerler için kullanılacak renk grubunu belirler.

Örneğin:

``` python
palette="deep"
palette="muted"
palette="bright"
palette="pastel"
palette="dark"
palette="colorblind"
```

gibi hazır paletler kullanılabilir.

------------------------------------------------------------------------

# 31. Tek bir renk kullanmak

Örneğin:

``` python
sns.lineplot(
    data=df,
    x="date",
    y="sales"
)
```

ve renk belirtmek istersen:

``` python
sns.lineplot(
    data=df,
    x="date",
    y="sales",
    color="blue"
)
```

Burada `palette` ile `color` arasındaki farkı unutma:

``` text
color
  ↓
tek grafik / tek renk

palette
  ↓
birden fazla kategori için
renk seti
```

------------------------------------------------------------------------

# 32. Legend

Seaborn birçok durumda legend'ı otomatik oluşturabilir.

Örneğin:

``` python
sns.scatterplot(
    data=df,
    x="age",
    y="salary",
    hue="department"
)
```

`department` için legend oluşturulur.

Matplotlib ile legend'ı çoğu zaman kendin yönetirsin:

``` python
plt.plot(x, y, label="Sales")
plt.legend()
```

Seaborn burada veri kolonlarının anlamını kullanarak daha fazla işi
otomatik yapar.

------------------------------------------------------------------------

# 33. `catplot`

Kategorik grafiklerin genel bir arayüzü olarak düşünülebilir:

``` python
sns.catplot(
    data=df,
    x="department",
    y="salary",
    kind="box"
)
```

`kind` ile grafik tipini seçebilirsin.

Örneğin:

``` python
kind="strip"
kind="swarm"
kind="box"
kind="violin"
kind="boxen"
kind="bar"
kind="count"
```

------------------------------------------------------------------------

# 34. `relplot`

İlişki grafiklerini daha yüksek seviyede oluşturmak için:

``` python
sns.relplot(
    data=df,
    x="age",
    y="salary",
    hue="department"
)
```

`kind` ile:

``` python
kind="scatter"
kind="line"
```

seçilebilir.

------------------------------------------------------------------------

# 35. `displot`

Dağılım grafiklerinin genel arayüzlerinden biridir:

``` python
sns.displot(
    data=df,
    x="salary"
)
```

Örneğin:

``` python
kind="hist"
kind="kde"
kind="ecdf"
```

kullanılabilir.

------------------------------------------------------------------------

# 36. Facet mantığı

Seaborn'un çok güçlü taraflarından biri veriyi kategorilere göre ayrı
panellere bölmektir.

Örneğin:

``` python
sns.relplot(
    data=df,
    x="age",
    y="salary",
    col="department"
)
```

Bu durumda:

``` text
        IT          Sales         HR

       grafik       grafik       grafik
```

gibi ayrı paneller oluşturulabilir.

Bu yaklaşım veri analizinde çok kullanışlıdır.

------------------------------------------------------------------------

# 37. `row` ve `col`

Örneğin:

``` python
sns.relplot(
    data=df,
    x="age",
    y="salary",
    row="gender",
    col="department"
)
```

Veriyi iki kategorik boyuta göre bölebilirsin.

Kabaca:

``` text
             IT       Sales

Group A     grafik    grafik

Group B     grafik    grafik
```

------------------------------------------------------------------------

# 38. Seaborn'da eksen nesnesi kullanmak

Matplotlib öğrenirken muhtemelen şunu göreceksin:

``` python
fig, ax = plt.subplots()

sns.lineplot(
    data=df,
    x="date",
    y="sales",
    ax=ax
)
```

Burada:

``` python
ax=ax
```

Seaborn'a:

> "Bu grafiği şu Matplotlib Axes üzerinde çiz."

demektir.

Bu, Seaborn ve Matplotlib'in birlikte çalışmasının en önemli
mekanizmalarından biridir.

------------------------------------------------------------------------

# 39. Neden `fig, ax = plt.subplots()` daha çok tercih edilir?

Başlangıçta:

``` python
plt.figure()
```

kullanımı gayet anlaşılır.

Ancak daha büyük projelerde:

``` python
fig, ax = plt.subplots()
```

yaklaşımı çok kullanışlıdır.

Örneğin:

``` python
fig, ax = plt.subplots(figsize=(10, 8))

sns.lineplot(
    data=df_daily,
    x="day_date",
    y="customer_count",
    ax=ax
)

ax.set_ylabel("Number of customers")

plt.tight_layout()
plt.show()
```

Burada:

``` text
fig
 ↓
tüm figure/pencere

ax
 ↓
grafiğin çizildiği eksen alanı
```

şeklinde düşünebilirsin.

------------------------------------------------------------------------

# 40. Birden fazla grafik

Örneğin:

``` python
fig, axes = plt.subplots(2, 1)

sns.lineplot(
    data=df,
    x="date",
    y="sales",
    ax=axes[0]
)

sns.lineplot(
    data=df,
    x="date",
    y="customers",
    ax=axes[1]
)

plt.tight_layout()
plt.show()
```

Burada tek figure içinde iki ayrı axes vardır.

``` text
+----------------------+
|      sales           |
|                      |
+----------------------+
|      customers       |
|                      |
+----------------------+
```

------------------------------------------------------------------------

# 41. Ayrı pencereler istiyorsan

Her biri ayrı figure:

``` python
plt.figure()

sns.lineplot(...)

plt.show()

plt.figure()

sns.scatterplot(...)

plt.show()
```

veya:

``` python
fig1 = plt.figure()
sns.lineplot(...)

fig2 = plt.figure()
sns.scatterplot(...)

plt.show()
```

Matplotlib figure yönetimi burada devreye girer.

Seaborn'un bu konuda ayrı bir pencere sistemi yoktur; figure yönetimini
Matplotlib yapar.

------------------------------------------------------------------------

# 42. Matplotlib mi Seaborn mu?

Basit bir karar tablosu:

  İhtiyaç                                 Tercih
  --------------------------------------- ----------------
  Basit çizgi grafiği                     İkisi de
  DataFrame ile hızlı grafik              Seaborn
  İstatistiksel grafikler                 Seaborn
  Box plot                                Seaborn
  Violin plot                             Seaborn
  Korelasyon heatmap                      Seaborn
  Hızlı exploratory data analysis         Seaborn
  Her ayrıntıyı kontrol etmek             Matplotlib
  Özel annotation                         Matplotlib
  Çok özel grafik tasarımı                Matplotlib
  Grafik nesnelerini ayrıntılı yönetmek   Matplotlib
  Sunum için ince ayar                    İkisi birlikte

------------------------------------------------------------------------

# 43. İkisini birlikte kullanmak genellikle en iyi seçenektir

Gerçek projelerde:

``` python
import seaborn as sns
import matplotlib.pyplot as plt
```

çok doğal bir kombinasyondur.

Örneğin:

``` python
sns.set_theme()

fig, ax = plt.subplots(figsize=(10, 6))

sns.lineplot(
    data=df,
    x="date",
    y="sales",
    ax=ax
)

ax.set_title("Monthly Sales")
ax.set_xlabel("Month")
ax.set_ylabel("Sales")

ax.grid(True)

plt.tight_layout()
plt.show()
```

Burada görev paylaşımı:

``` text
Seaborn
  ↓
veri odaklı grafiği oluştur

Matplotlib
  ↓
grafiğin ayrıntılarını yönet
```

------------------------------------------------------------------------

# 44. Seaborn'un otomatik istatistik hesaplaması

Seaborn'un önemli farklarından biri de budur.

Örneğin:

``` python
sns.barplot(
    data=df,
    x="department",
    y="salary"
)
```

Bu sadece her satırı çubuk olarak çizmek değildir.

Seaborn kategorilere göre bir istatistiksel özet oluşturur.

Bu yüzden Seaborn'un ismi de önemlidir:

> **Statistical Data Visualization**

Seaborn özellikle istatistiksel veri analizini kolaylaştırmak için
tasarlanmıştır.

------------------------------------------------------------------------

# 45. Ham veriyi çizmek ile istatistiksel özet çizmek farklıdır

Bu ayrımı özellikle öğren.

Matplotlib:

``` python
plt.bar(
    ["IT", "Sales"],
    [35000, 30000]
)
```

Burada değerleri sen hesaplamışsın.

Seaborn:

``` python
sns.barplot(
    data=df,
    x="department",
    y="salary"
)
```

Burada Seaborn veriyi analiz edip kategorik özet oluşturabilir.

Bu nedenle Seaborn'un grafik fonksiyonlarının "istatistiksel anlamı"
olabilir.

------------------------------------------------------------------------

# 46. `errorbar`

Bazı istatistiksel grafiklerde belirsizlik aralıkları da gösterilebilir.

Örneğin:

``` python
sns.barplot(
    data=df,
    x="department",
    y="salary",
    errorbar=None
)
```

Burada hata çubuklarını kapatabilirsin.

Bu ayrıntı Seaborn'un neden sadece "daha güzel Matplotlib" olmadığını
gösterir.

Seaborn aynı zamanda istatistiksel bir görselleştirme yaklaşımıdır.

------------------------------------------------------------------------

# 47. Seaborn ile veri keşfi

Yeni bir veri seti aldığında şu tür grafikler çok faydalı olabilir:

``` python
sns.histplot(data=df, x="age")
```

``` python
sns.boxplot(data=df, x="department", y="salary")
```

``` python
sns.scatterplot(
    data=df,
    x="age",
    y="salary",
    hue="department"
)
```

``` python
sns.heatmap(
    df.corr(numeric_only=True),
    annot=True
)
```

Bunlar sana veri hakkında hızlıca fikir verebilir.

Bu nedenle Seaborn özellikle **EDA (Exploratory Data Analysis)**
aşamasında çok kullanılır.

------------------------------------------------------------------------

# 48. Seaborn öğrenirken hangi fonksiyonları önce öğrenmelisin?

Hepsini aynı anda öğrenmeye çalışma.

Şu sırayı öneririm:

## 1. Tema

``` python
sns.set_theme()
sns.set_style()
```

## 2. Temel ilişkisel grafikler

``` python
sns.lineplot()
sns.scatterplot()
```

## 3. Kategorik grafikler

``` python
sns.barplot()
sns.countplot()
sns.boxplot()
sns.violinplot()
```

## 4. Dağılımlar

``` python
sns.histplot()
sns.kdeplot()
sns.displot()
```

## 5. İlişki keşfi

``` python
sns.pairplot()
sns.heatmap()
```

## 6. Facet / çoklu grafikler

``` python
sns.relplot()
sns.catplot()
```

Bu sırayla ilerlersen öğrenmesi çok daha kolay olur.

------------------------------------------------------------------------

# 49. Matplotlib bilgini çöpe atma

Seaborn öğrenmeye başladığında:

> "Artık Matplotlib kullanmayacağım."

deme.

Tam tersine, Matplotlib bilgisi Seaborn'u anlamanı kolaylaştırır.

Örneğin Seaborn:

``` python
sns.lineplot(...)
```

ile grafik oluşturduktan sonra:

``` python
plt.title(...)
plt.xlabel(...)
plt.ylabel(...)
plt.xlim(...)
plt.ylim(...)
plt.xticks(...)
plt.yticks(...)
plt.legend(...)
plt.tight_layout()
plt.show()
```

gibi Matplotlib komutlarını kullanmaya devam edebilirsin.

------------------------------------------------------------------------

# 50. Seaborn'da bilmen gereken önemli kavramlar

## `data`

Veri kaynağı:

``` python
data=df
```

## `x`

X eksenindeki değişken:

``` python
x="age"
```

## `y`

Y eksenindeki değişken:

``` python
y="salary"
```

## `hue`

Renkle kategori ayırma:

``` python
hue="department"
```

## `style`

Marker/çizgi stilini kategoriye göre ayırma:

``` python
style="department"
```

## `size`

Boyutla değişken gösterme:

``` python
size="experience"
```

## `palette`

Renk paleti:

``` python
palette="Set2"
```

## `ax`

Belirli bir Matplotlib Axes üzerinde çizme:

``` python
ax=ax
```

Bu parametreleri öğrenmek Seaborn kullanımının büyük kısmını anlamanı
sağlar.

------------------------------------------------------------------------

# 51. Matplotlib → Seaborn zihinsel dönüşümü

Matplotlib:

``` python
plt.plot(
    df["date"],
    df["sales"]
)
```

Seaborn:

``` python
sns.lineplot(
    data=df,
    x="date",
    y="sales"
)
```

------------------------------------------------------------------------

Matplotlib:

``` python
plt.scatter(
    df["age"],
    df["salary"]
)
```

Seaborn:

``` python
sns.scatterplot(
    data=df,
    x="age",
    y="salary"
)
```

------------------------------------------------------------------------

Matplotlib:

``` python
plt.bar(
    categories,
    values
)
```

Seaborn:

``` python
sns.barplot(
    data=df,
    x="category",
    y="value"
)
```

Ama burada Seaborn'un istatistiksel aggregation yapabileceğini unutma.

------------------------------------------------------------------------

# 52. Senin mevcut projendeki kullanım

Senin `df_daily` örneğini ele alırsak:

``` python
fig1 = plt.figure(figsize=(10, 8))

plt.plot(
    df_daily["day_date"],
    df_daily["customer_count"]
)

plt.ylabel(
    "Number of customers",
    fontsize=14
)

plt.grid()

plt.tight_layout()
plt.show()
```

Bunu Seaborn ile:

``` python
import seaborn as sns
import matplotlib.pyplot as plt

sns.set_theme()

fig, ax = plt.subplots(figsize=(10, 8))

sns.lineplot(
    data=df_daily,
    x="day_date",
    y="customer_count",
    ax=ax
)

ax.set_ylabel(
    "Number of customers",
    fontsize=14
)

plt.tight_layout()
plt.show()
```

şeklinde yazabilirsin.

Ama önemli nokta:

**Bu örnekte Seaborn kullanmak zorunlu değil.**

Çünkü tek bir zaman serisini çizmek için Matplotlib zaten gayet yeterli.

Seaborn'un avantajı, veri setinin yapısı ve istatistiksel görselleştirme
ihtiyacı karmaşıklaştıkça daha fazla ortaya çıkar.

------------------------------------------------------------------------

# 53. Seaborn ne zaman gerçekten avantaj sağlar?

Örneğin elinde:

``` text
event_time
user_id
event_type
product_id
price
category_code
brand
```

gibi sütunları olan bir müşteri/event veri seti varsa Seaborn çok
kullanışlı hale gelir.

Örneğin:

``` python
sns.countplot(
    data=customers,
    x="event_type"
)
```

ile event türlerinin dağılımını hızlıca görebilirsin.

Ya da:

``` python
sns.boxplot(
    data=customers,
    x="event_type",
    y="price"
)
```

ile event türlerine göre fiyat dağılımlarını inceleyebilirsin.

Ya da:

``` python
sns.scatterplot(
    data=customers,
    x="price",
    y="user_session",
    hue="event_type"
)
```

gibi grafikler oluşturabilirsin.

------------------------------------------------------------------------

# 54. Seaborn'un sınırları

Seaborn her şey için daha iyi değildir.

Çok özel bir grafik yapmak istediğinde:

``` python
from matplotlib.patches import Rectangle
```

gibi Matplotlib'in düşük seviyeli özelliklerine ihtiyaç duyabilirsin.

Örneğin:

-   özel annotation
-   karmaşık şekiller
-   özel eksen yerleşimleri
-   özel koordinat sistemleri
-   çok ayrıntılı grafik tasarımı
-   yayın kalitesinde ince ayarlar

gibi durumlarda Matplotlib'in doğrudan API'si daha uygun olabilir.

------------------------------------------------------------------------

# 55. En önemli sonuç

Seaborn'u şöyle hatırla:

``` text
Matplotlib
=
Grafiğin motoru ve ayrıntılı kontrol

Seaborn
=
DataFrame + istatistik + kolay API + güzel varsayılanlar
```

Daha da basitleştirirsek:

``` text
Matplotlib:
"Grafiği nasıl çizeyim?"

Seaborn:
"Verim ne anlatıyor ve bunu nasıl hızlı
bir şekilde görselleştirebilirim?"
```

Bu yüzden ikisini rakip olarak düşünmek yerine:

``` python
import seaborn as sns
import matplotlib.pyplot as plt
```

ikilisini **birlikte kullanmayı** öğrenmek en faydalı yaklaşımdır.

------------------------------------------------------------------------

# 56. Başlangıç için mini Seaborn cheat sheet

``` python
import seaborn as sns
import matplotlib.pyplot as plt

# Genel tema
sns.set_theme()

# Çizgi
sns.lineplot(data=df, x="date", y="sales")

# Nokta
sns.scatterplot(data=df, x="age", y="salary")

# Kategoriye göre renk
sns.scatterplot(
    data=df,
    x="age",
    y="salary",
    hue="department"
)

# Bar
sns.barplot(data=df, x="department", y="salary")

# Sayım
sns.countplot(data=df, x="department")

# Histogram
sns.histplot(data=df, x="salary")

# KDE
sns.kdeplot(data=df, x="salary")

# Box plot
sns.boxplot(data=df, x="department", y="salary")

# Violin
sns.violinplot(data=df, x="department", y="salary")

# Korelasyon
sns.heatmap(df.corr(numeric_only=True), annot=True)

# Değişkenleri topluca inceleme
sns.pairplot(df)

plt.show()
```

------------------------------------------------------------------------

# 57. Son olarak öğrenme stratejisi

Sen zaten Matplotlib kullanmaya başladığın için Seaborn'u sıfırdan
tamamen ayrı bir kütüphane gibi öğrenmene gerek yok.

Şu bağlantıyı kur:

``` text
Matplotlib bildiğim grafik
          ↓
Seaborn'da karşılığı nedir?
          ↓
Seaborn hangi işi otomatik yapıyor?
          ↓
Matplotlib ile nasıl ince ayar yapabilirim?
```

Örneğin önce:

``` python
plt.plot(df["x"], df["y"])
```

sonra:

``` python
sns.lineplot(data=df, x="x", y="y")
```

sonra:

``` python
sns.lineplot(
    data=df,
    x="x",
    y="y",
    hue="category"
)
```

sonra:

``` python
fig, ax = plt.subplots()

sns.lineplot(
    data=df,
    x="x",
    y="y",
    hue="category",
    ax=ax
)

ax.set_title("My Analysis")
ax.set_xlabel("X")
ax.set_ylabel("Y")

plt.show()
```

Bu şekilde ilerlersen Seaborn ile Matplotlib arasındaki ilişki çok daha
hızlı oturur.

------------------------------------------------------------------------

# Özet

**Matplotlib:** düşük seviyeye daha yakın, çok güçlü ve ayrıntılı
kontrol sağlayan temel görselleştirme kütüphanesi.

**Seaborn:** Matplotlib üzerine kurulmuş, özellikle Pandas
DataFrame'leri ve istatistiksel veri görselleştirmeyi kolaylaştıran
yüksek seviyeli kütüphane.

**Seaborn neden gerekli?**

Çünkü veri analizi sırasında sık yaptığın işlemleri daha kısa ve anlamlı
bir API ile ifade eder:

``` python
sns.scatterplot(
    data=df,
    x="age",
    y="salary",
    hue="department"
)
```

gibi tek bir çağrıyla veri kolonlarını grafik özelliklerine
bağlayabilir.

**En iyi yaklaşım:**

``` text
Seaborn → hızlı ve istatistiksel grafik oluşturma
      +
Matplotlib → ayrıntılı grafik kontrolü
```

İkisini birlikte bilmek, yalnızca birini bilmekten daha güçlü bir
kombinasyondur.
