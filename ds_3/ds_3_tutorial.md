# DS 3 - Ayrintili Calisma Rehberi

Bu rehber, bu depodaki `ds_3.pdf` dosyasinin **Version 1.00, 12 sayfa** olan surumunu ve yanindaki CSV dosyalarini temel alir. Konu, bir siniflandirma modelini egitmeden once gereken veri kesfi ve veri hazirlama islerinin kucuk ama gercekci bir zinciridir.

## Once onemli bir surum notu

Sorudaki bazi alintilar ile bu depodaki PDF ayni alistirma surumune ait degil. Bu ayrim cok onemli; degerlendirmede yerel `ds_3.pdf` esas alinmali.

| Konu | Bu depodaki PDF'nin istedigi |
| --- | --- |
| Ex00 | `Histogram.*`: Test ve Train CSV icin histogramlar |
| Ex01 | `Correlation.*`: hedef ile tum ozelliklerin korelasyon tablosu |
| Ex02 | `points.*`: iki ozellik cifti, hem Train hem Test icin toplam dort scatter plot |
| Ex03 | `standardization.*`: veriyi standardize et, yazdir, Ex02'deki ciftlerden biriyle grafik ciz |
| Ex04 | `Normalization.*`: veriyi normalize et, yazdir, Ex02'deki diger ciftle grafik ciz |
| Ex05 | `split.*`: `Train_knight.csv` dosyasini rastgele training/validation dosyalarina bol |

Sorudaki eski alintida Ex00 sinif sayma, Ex02 iki grafik ve Ex03/04 icin formuller gorunuyor. Bunlar bu PDF'de yok. Bu PDF ayrica dili zorunlu olarak Python yapmiyor, ancak Python + `pandas` + `matplotlib` bu is icin en makul secimdir.

PDF'deki Ex01 ornek tablosunda `Force` sutunu gorunuyor, fakat bu depodaki CSV'de bu adla bir sutun yok, onun yerine `Pull` var. Ornek tabloyu sabit cevap gibi kopyalama. Sutun listesini dosyadan okuyup sonucu dinamik hesapla.

## Projenin buyuk resmi

Hikaye, gecmisteki kisilerin olculmus becerilerinden bir kisinin hangi sinifa ait oldugunu anlamaya calisan bir siniflandirma problemidir. Bu projede henuz bir `LogisticRegression`, karar agaci veya baska bir tahmin modeli kurman istenmiyor. Onun yerine modele gecmeden once su sorulari cevaplamayi ogreniyorsun:

1. Verinin dagilimi nasil, siniflar ve beceriler gorunur bicimde ayrisiyor mu?
2. Hangi sayisal beceriler hedef sinifla daha cok iliskili?
3. Iki beceriyi birlikte cizersem iki sinif ayrisiyor mu, yoksa ust uste mi biniyor?
4. Farkli olceklerdeki sutunlari modele uygun hale nasil getiririm?
5. Bir modeli adil bicimde denemek icin elimdeki etiketli veriyi nasil ayiririm?

Bu siralama, tipik bir makine ogrenmesi on-isleme akisinin kucuk bir halidir:

```text
CSV oku -> kesfet/gorsellestir -> iliski olc -> olcekle -> train/validation ayir
```

Bu nedenle DS 3'un ogretmek istedigi alanlar sunlardir:

- Kesifsel veri analizi (EDA): histogramlar, dagilimlar, sinif dengesizligi.
- Denetimli ogrenmenin temelleri: feature/target ayrimi, etiketli ve etiketsiz veri.
- Betimsel istatistik: Pearson korelasyonu ve yorumu.
- Veri gorsellestirme: histogram ve iki boyutlu scatter plot ile sinif ayrisabilirligi.
- Feature scaling: standardization (z-score) ve min-max normalization.
- Model degerlendirme temeli: train-validation split, rastgelelik ve tekrarlanabilirlik.
- Veri sizintisini (data leakage) fark etme: olcekleme istatistikleri ve validation verisinin rolu.

## Veri dosyalari ve temel kelimeler

Bu depodaki gercek durum:

- `Train_knight.csv`: 398 satir, 30 sayisal beceri sutunu ve `knight` hedef sutunu.
- `Test_knight.csv`: 171 satir, ayni 30 sayisal beceri sutunu, fakat `knight` yok.
- Train hedef dagilimi: 152 `Jedi`, 246 `Sith`.
- Her iki CSV'de eksik deger yok.

`Train_knight.csv` etiketlidir: her satirin sonucunu zaten biliyoruz. `Test_knight.csv` etiketsizdir: sinifi verilmedigi icin onu sadece dagilim ve nokta bulutu olarak cizebilirsin; bu projede test icin tahmin uretme gorevi yoktur.

| Terim | Bu projedeki anlami |
| --- | --- |
| Satir / observation | Bir hayali kisinin olculmus beceri kaydi |
| Feature / ozellik | `Sensitivity`, `Strength`, `Empowered` gibi girdi degiskenleri; burada 30 tane var |
| Target / hedef | Tahmin edilmek istenen sonuc; burada `knight` sutunu |
| Class / sinif | Hedefin alabilecegi kategori; burada `Jedi` veya `Sith` |
| Train data | Hem becerileri hem gercek sinifi bilinen 398 satir |
| Test data | Yalnizca becerileri verilen 171 satir |

### Star Wars hikayesi ne demek?

Bu sadece veri setine tema vermek icin kullanilan bir benzetmedir; filmi bilmek proje icin gerekli degildir.

- **Anakin Skywalker**, Star Wars evrenindeki bir karakterdir. Bir Jedi iken karanlik tarafa gecer ve Darth Vader olur.
- **Jedi**, Guclu (Force) daha cok koruyucu/iyi niyetli kullanan tarafi temsil eder.
- **Sith**, Guclu guc, korku ve hakimiyet icin kullanan karsi tarafi temsil eder.
- PDF'deki **knight**, orta cag savascisi anlamindaki bir kelimeyi degil, bu hikayedeki Force kullanan savasci/uyeler icin gevsek bir etiketi anlatir. CSV'de gercek sinif degerleri `Jedi` ve `Sith`tir.
- Metindeki `burn on the dark side` dogal Ingilizce bir deyim degildir. Kastedilen sey buyuk olasilikla **turn to the dark side**: "karanlik tarafa gecmek"tir. "Burn" kelimesi hikayedeki fiziksel yaralanmaya goz kirpiyor olabilir, ama veri bilimi anlami yoktur.

Dolayisiyla problem su teknik soruya iner: "Bir kisinin 30 sayisal becerisinden, etiketi Jedi mi Sith mi diye ayirt etmeye yarayan isaretler var mi?"

## 1) Database kurmak zorunda miyim?

**Hayir. Bu projede database kurmak, CSV'leri database'e aktarmak veya SQL ile calismak istenmiyor.** PDF dogrudan `Train_knight.csv` ve `Test_knight.csv` dosyalariyla calismani soyluyor. Dosyalar da kucuk: toplam 569 satir. Bu buyuklukte bir veri icin `pandas.read_csv()` ile bellekte `DataFrame` olusturmak hem dogal hem de amaca uygundur.

Onceki projelerde milyonlarca satir varsa database; indeksleme, kalici depolama, SQL sorgulari ve bellek yonetimi icin anlamli olabilir. Burada database eklemek ek kavram ve hata noktasi getirir, ama histogram, korelasyon, olcekleme veya split sonucunu iyilestirmez.

Baslangic icin tek gereken kalip budur:

```python
from pathlib import Path
import pandas as pd

TARGET = "knight"

def load_data(filename: str) -> pd.DataFrame:
    root = Path(__file__).resolve().parent.parent
    return pd.read_csv(root / filename)

train = load_data("Train_knight.csv")
test = load_data("Test_knight.csv")
features = [column for column in train.columns if column != TARGET]
```

`Path(__file__)` kullanmak, programi hangi dizinden calistirdigina bagli kalmaktan kurtarir. Ex00-Ex04 icin programi tek bir dosya adi alacak sekilde tasarlamak pratiktir:

```bash
python3 Histogram.py ../Train_knight.csv
python3 Histogram.py ../Test_knight.csv
```

Bu komutlar sadece ornektir; kendi dosya yoluna gore ayarlayabilirsin. Her programda once `df.head()`, `df.shape`, `df.dtypes` ve `df[TARGET].value_counts()` (sutun varsa) ile okumanin dogru oldugunu kontrol et.

## Ex00 - Histogram

### Ne isteniyor?

`ex00/Histogram.*` icinde bir grafik programi yaz. PDF'nin orneklerinde tek bir buyuk figure icinde 30 kucuk histogram paneli gorunuyor:

- `Test_knight.csv` icin her feature'in tum test satirlarindaki dagilimini ciz.
- `Train_knight.csv` icin ayni feature dagilimlarini Jedi ve Sith olarak ayirip ayni eksen uzerine ciz.

Train grafikte iki yari saydam histogramin ust uste binmesi, hangi becerilerde sinif dagilimlarinin farkli gorundugunu ilk bakista anlatir. Test dosyasinda hedef olmadigi icin sinifa gore renklendirme yapma; tum noktalari/verileri tek seri olarak ciz.

### Neden?

Histogram veri dagiliminin sekli, olcegi, aykiri degerleri ve siniflar arasindaki kabaca ayrimi gosterir. Korelasyon tek bir sayidir; histogram ise o sayinin arkasindaki dagilimi gorursun. Ornegin iki sinifin ortalamasi farkli olsa bile cok fazla ortusme olabilir.

### Nasil?

`matplotlib.pyplot.hist` kullan. Her feature icin **ayni bin sinirlarini** ve `alpha` degerini kullan ki Jedi-Sith karsilastirmasi adil olsun. 30 feature oldugu icin `plt.subplots(6, 5, figsize=(...))` iyi bir duzendir.

```python
import matplotlib.pyplot as plt

def draw_histograms(df, title):
    feature_columns = [c for c in df.columns if c != "knight"]
    fig, axes = plt.subplots(6, 5, figsize=(18, 20))

    for column, ax in zip(feature_columns, axes.flat):
        if "knight" in df.columns:
            for label, group in df.groupby("knight"):
                ax.hist(group[column], bins=20, alpha=0.55, label=label)
            ax.legend(fontsize=7)
        else:
            ax.hist(df[column], bins=20, color="seagreen", alpha=0.65,
                    label="All test rows")
            ax.legend(fontsize=7)
        ax.set_title(column, fontsize=9)

    fig.suptitle(title)
    fig.tight_layout()
    plt.show()
```

`bins=20` zorunlu bir sayi degildir; 15-30 arasi makul bir deger secip tutarli kullan. Cok az bin ayrintiyi kaybeder, cok fazla bin ise rastgele gurultuyu buyutur.

## Ex01 - Correlation

### Ne isteniyor?

`ex01/Correlation.*`, `knight` target'i ile her sayisal feature arasindaki korelasyon faktorlerini yazdirmalidir. PDF ornegi hedefin kendisini `1.000000` ve sonra feature'lari en yuksekten dusuge siralanmis olarak gosterir.

Korelasyon, iki degiskenin dogrusal beraber degisimini -1 ile +1 arasinda olcer:

- `+1`: feature buyurken secilen hedef kodu da duzenli bicimde buyuyor.
- `0`: belirgin dogrusal iliski yok.
- `-1`: feature buyurken secilen hedef kodu duzenli bicimde kuculuyor.
- Mutlak deger `|r|` buyudukce dogrusal iliski daha gucludur.

Bu veri setinde hedef sayi degil, `Jedi`/`Sith` metnidir. Bu nedenle once ikili bir sayiya cevirmelisin. PDF'deki pozitif siralamayla uyumlu secim `Jedi -> 1`, `Sith -> 0` olmaktir. Ters kodlarsan tum isaretler tersine doner, fakat mutlak degerler ve feature siralamasinin gucu degismez.

```python
import pandas as pd

df = pd.read_csv("../Train_knight.csv")
y = df["knight"].map({"Jedi": 1, "Sith": 0})
X = df.drop(columns="knight")

correlations = X.corrwith(y, method="pearson").sort_values(ascending=False)
result = pd.concat([pd.Series({"knight": 1.0}), correlations])
print(result.to_string(float_format=lambda value: f"{value:.6f}"))
```

Bu is icin ayri bir zorunlu Python modulu yoktur. `pandas`in `Series.corr()` ve `DataFrame.corrwith()` fonksiyonlari yeterlidir. Istersen `scipy.stats.pointbiserialr` da kullanabilirsin: sayisal bir feature ile 0/1 hedef arasindaki Pearson korelasyonu, istatistikte **point-biserial correlation** olarak da anilir.

Bu yerel CSV ile `Jedi=1`, `Sith=0` kodlamasinda en yuksek iliskiler yaklasik olarak `Empowered` (`0.793652`), `Prescience` (`0.790066`) ve `Stims` (`0.786797`) olur. En zayif mutlak iliskiler `Midi-chlorien`, `Push`, `Deflection` ve `Survival` civarindadir. Sayilari elle yazma; program her zaman CSV'yi okuyup hesaplasin.

### Neden Pearson ve nasil yorumlanir?

Feature'lar surekli sayi, hedef iki sinifli oldugu icin Pearson/point-biserial bu ilk kesif icin uygun ve PDF'nin ornegiyle uyumludur. Korelasyon feature olceklerinden etkilenmez; `Strength`in sayilari buyuk, `Mass`in sayilari kucuk diye korelasyon haksizlasmaz.

Ama "korelasyon yuksek" demek "sebep budur" demek degildir. Sadece bu veri setinde sinifla birlikte degistigini soyler. Dogrusal olmayan bir iliskiyi de kacirabilir. Bu yuzden Ex02'de sonucu scatter plot ile gozle kontrol ediyorsun.

## Ex02 - Scatter plotlar

### Bubble scatter plot mi?

**Hayir.** PDF'deki ornekler normal scatter plot'tur: her satir bir nokta, `x` bir feature, `y` baska bir feature olur. Renk sinifi anlatir. Bubble chart olsaydi noktanin boyutu ucuncu bir degiskeni tasirdi; burada tum noktalar yaklasik ayni boyutta olmali. `plt.scatter(..., s=18, alpha=0.55)` yazabilirsin, ama `s` sabit olmalidir.

### Dort grafik ne demek?

PDF "4 graphs" der. Iki feature cifti sececeksin; her cifti hem Train hem Test dosyasinda cizeceksin:

| Feature cifti | Train grafigi | Test grafigi |
| --- | --- | --- |
| Ayiran cift | Jedi/Sith farkli renklerde | Etiket olmadigi icin tek renkte |
| Karistiran cift | Jedi/Sith farkli renklerde ama ust uste | Etiket olmadigi icin tek renkte |

Toplam `2 x 2 = 4` panel budur. PDF'nin orneginde ustteki iki grafik Train, alttaki iki grafik Test'tir.

"One ... must visually separate the clusters, whereas the second one should mix them" cumlesi sunu ister: veriyi degistirerek yapay ayirim yaratma. Ex01'de kuvvetli iliskili buldugun feature'lari bir arada ciz ve renkli sinif noktalarinin daha farkli bolgelerde toplanmasini goster. Sonra hedefle zayif iliskili feature'lari ciz; renkler belirgin bicimde birbirine karissin. Cok iyi bir ayiran grafik bile kusursuz olmayabilir; aranan sey goreli olarak daha az/ daha cok ortusmedir.

Bu dosyada PDF'nin eksen araliklarina da uyan makul bir secim:

```python
SEPARATING_PAIR = ("Empowered", "Stims")
MIXED_PAIR = ("Push", "Deflection")
```

Ilk ikisi target ile yuksek korelasyonludur. Ikinci ikisi target ile cok zayif korelasyonludur. Sadece PDF resmine bakarak isim ezberlemek yerine, Ex01 sonucundan bu tercihi savun: "Yuksek `|r|` feature'larini ayiran, `|r|` sifira yakin olanlari karistiran cift icin kullandim."

```python
import matplotlib.pyplot as plt

def draw_points(df, x_name, y_name, title):
    fig, ax = plt.subplots(figsize=(7, 5))
    if "knight" in df.columns:
        colors = {"Jedi": "royalblue", "Sith": "salmon"}
        for label, group in df.groupby("knight"):
            ax.scatter(group[x_name], group[y_name], s=18, alpha=0.55,
                       label=label, color=colors[label])
        ax.legend()
    else:
        ax.scatter(df[x_name], df[y_name], s=18, alpha=0.55,
                   label="Test rows", color="seagreen")
        ax.legend()
    ax.set(xlabel=x_name, ylabel=y_name, title=title)
    ax.grid(alpha=0.2)
    plt.show()
```

Test'te `knight` sutunu olmadigindan "bu nokta Jedi" diye renklendirmek veya sinif ayirimi iddia etmek yanlistir. Test cizimi ayni feature ciftlerinin yeni, etiketsiz veri dagilimini gosterir.

## Ex03 - Standardization

### Standardize etmek ne demek?

Her feature sutununu kendi ortalamasina ve standart sapmasina gore z-score'a donusturmektir:

```text
z = (x - mean(x)) / std(x)
```

Her sutun **ayri ayri** islenir. Donusumden sonra o feature'in ortalamasi yaklasik `0`, standart sapmasi yaklasik `1` olur. Degerler negatif olabilir, `1`den buyuk olabilir; standardization araligi `[0, 1]` yapmaz ve veriyi normal dagilima da cevirmek zorunda degildir.

"standardize and print your data"daki **data**, CSV'den okudugun `DataFrame`deki tum satirlar ve feature sutunlaridir. Train girdisinde `knight` bir feature degildir: onu sayisal olcekleme fonksiyonuna sokma, oldugu gibi birak. Test'te zaten bu sutun yoktur. Donusmus tabloyu yazdirmak, her sutunda degisimin uygulandigini kanitlar.

```python
def standardize(df):
    output = df.copy()
    feature_columns = [c for c in df.columns if c != "knight"]
    means = df[feature_columns].mean()
    stds = df[feature_columns].std(ddof=0).replace(0, 1)
    output[feature_columns] = (df[feature_columns] - means) / stds
    return output

scaled = standardize(df)
print(scaled.to_string(index=False))
```

`ddof=0`, `sklearn.preprocessing.StandardScaler`in kullandigi standart sapma tanimiyla uyumludur. Sabit bir sutunda standart sapma 0 olur; bu veri setinde boyle bir sutun yok, ama genel bir programda bolme hatasini onlemek icin onu `1` ile degistirmek ya da 0 degerli sonuc vermek gerekir.

Ex03 ayrica Ex02'deki ciftlerden **birini** standardize edilmis veriyle yeniden cizmeyi ister. Mantikli secim `Empowered` - `Stims` ayiran ciftidir. Eksenlerin sayilari degisir, ama noktalarin goreli geometrisi ve sinif ayrimi degismez; bu da standardizationin birim farklarini kaldirdigini gosterir.

## Ex04 - Normalization

### Normalize etmek ne demek?

Bu baglamda istenen donusum min-max normalizationdir:

```text
x_normalized = (x - min(x)) / (max(x) - min(x))
```

Her feature sutununun en kucuk degeri `0`, en buyuk degeri `1` olur; diger tum degerler `[0, 1]` araligina yerlestirilir.

```python
def normalize(df):
    output = df.copy()
    feature_columns = [c for c in df.columns if c != "knight"]
    minimums = df[feature_columns].min()
    spans = (df[feature_columns].max() - minimums).replace(0, 1)
    output[feature_columns] = (df[feature_columns] - minimums) / spans
    return output

normalized = normalize(df)
print(normalized.to_string(index=False))
```

Ex04'te Ex02'de kullanmadigin **diger** feature ciftiyle (`Push` - `Deflection`) normalize edilmis scatter plot ciz. PDF'nin ornek komut satirinda `./standardization.*` yazmasi bir yazim hatasidir; bu Ex04'un adi ve teslim deseni `Normalization.*`dir.

### Standardization ve normalization ayni sey mi?

Hayir. Ikisi de feature scalingdir ama farkli hedefleri vardir.

| Ozellik | Standardization (z-score) | Min-max normalization |
| --- | --- | --- |
| Formul | `(x - mean) / std` | `(x - min) / (max - min)` |
| Tipik sonuc | Ortalama 0, std 1 | Minimum 0, maksimum 1 |
| Deger araligi | Sinirsiz; negatif ve 1'den buyuk olabilir | `[0, 1]` |
| Aykiri deger etkisi | Vardir ama min-max kadar dogrudan degildir | Cok hassastir; tek buyuk aykiri deger digerlerini sikistirir |
| Ne zaman dusunulur? | Ortalama/standart sapmaya duyarlilik gosteren modeller | Sabit sinirli olcek isteyen veya mesafe tabanli yontemler |

Bu projede ikisini de yazmanin nedeni, "sayilari kucultmek" ile ayni ismi yaptiklarini sanmaman ve gorsel sonucunu karsilastirabilmendir.

### Gercek ML akisi hakkinda onemli not

PDF sadece programin hem Train hem Test CSV ile calismasini ister; hangi istatistiklerin Test'e uygulanacagini aciklamaz. Tek dosya girdi alan bir alistirma programinda her dosyanin kendi `mean/std` veya `min/max` degerleriyle donusum yapmasi, gorsel alistirma icin kabul edilebilir.

Gercek bir tahmin sisteminde ise once sadece training verisinin `mean/std` veya `min/max` degerlerini hesaplarsin; validation ve test verisine **ayni** degerleri uygularsin. Test verisinin istatistiklerini scaler'i "fit" etmek icin kullanmak, gelecekteki veriden bilgi sizintisi olur. Savunmada bu ayrimi soylemek iyi bir veri bilimi refleksidir.

## Ex05 - Split

### Bu islemin literaturde adi nedir?

Bu isleme **train-validation split**, **holdout split** veya **data partitioning** denir. `Train_knight.csv` zaten etiketli tum veridir. Onu iki farkli amacla ayirirsin:

- `Training_knight.csv`: model ileride bu satirlardan oruntu ogrenecek.
- `Validation_knight.csv`: model bu satirlari egitimde hic gormeyecek; basarisi ve overfitting burada kontrol edilecek.

Bu proje model egitmese de, bir sonraki asama icin dogru deney duzenini kurdurur. `Test_knight.csv` validation yerine kullanilmaz; target'i olmadigi icin model performansini olcemezsin.

### Yuzdeyi nasil ve neden secerim?

PDF kesin bir oran dayatmiyor. Savunmasi kolay, yaygin bir tercih **%80 training, %20 validation**dir:

- Verinin buyuk bolumu (%80) modelin oruntu ogrenmesi icin kalir.
- Hic gormedigi anlamli bir bolum (%20), genelleme performansini olcmek icin ayrilir.
- Kucuk bir veri setinde validation'i asiri buyutmek egitim bilgisini gereksiz azaltir; asiri kucultmek ise olcumu cok oynak yapar.

Bu yerel dosyada 398 satir vardir. %20 validation istendiginde satirlar bolunemez: 80 validation ve 318 training satiri elde edilir. Bu sirasiyla `%20.101` ve `%79.899`tur; en yakin pratik 80/20 bolum budur.

Siniflar dengesizdir (152 Jedi, 246 Sith). Bu nedenle **stratified random split** tercih etmek iyi fikirdir: iki dosyada da Jedi/Sith oranini ana veri setine yakin tutar. Sabit `random_state=42`, ayni programi tekrar calistirdiginda ayni bolumu vermesini saglar; bu da hata ayiklama ve degerlendirme icin gereklidir.

```python
import pandas as pd
from sklearn.model_selection import train_test_split

df = pd.read_csv("Train_knight.csv")
training, validation = train_test_split(
    df,
    test_size=0.20,
    random_state=42,
    shuffle=True,
    stratify=df["knight"],
)

training.to_csv("Training_knight.csv", index=False)
validation.to_csv("Validation_knight.csv", index=False)
```

`pandas` ile, ek kutuphane kullanmadan yazilabilecek daha basit alternatif de vardir:

```python
training = df.sample(frac=0.80, random_state=42)
validation = df.drop(training.index)
```

Bu ikinci yontem de rastgele ve tekrarlanabilir bir bolum uretir, ancak `stratify` yapmadigi icin Jedi/Sith oranlari sans eseri biraz kayabilir. PDF sadece rastgele split istedigi icin ikisi de konusu kapsar; sinifli bir problemde ilk yontemi gerekcelendirmek daha gucludur.

Split sonrasinda su kontrolleri yap:

```python
assert len(training) + len(validation) == len(df)
assert training.index.intersection(validation.index).empty
assert list(training.columns) == list(validation.columns) == list(df.columns)
print(len(training), len(validation))
print(training["knight"].value_counts(normalize=True))
print(validation["knight"].value_counts(normalize=True))
```

CSV'ye yazarken `index=False` kullan. Aksi halde pandas'in satir indeksi fazladan, anlamsiz bir sutun olarak dosyaya yazilir.

## Uygulama sirasi ve teslim kontrol listesi

1. `pandas`, `numpy`, `matplotlib` kur; Ex05 icin stratified secimi kullanacaksan `scikit-learn` de kur.
2. Her programi CSV yolunu komut satirindan okuyacak ve Train/Test farkini `"knight" in df.columns` ile anlayacak bicimde yaz.
3. Ex00'da tum feature histogramlarini ciz; Train'de Jedi/Sith legend'i, Test'te tek seri kullan.
4. Ex01'de target'i `Jedi=1`, `Sith=0` olarak gecici sayisal seriye cevir; Pearson korelasyonlarini hesaplayip sirala.
5. Ex02'de iki feature cifti sec; her birini hem Train hem Test icin cizerek dort grafik uret.
6. Ex03'te yalnizca feature'lari standardize et, donusen tabloyu yazdir ve ayiran cifti tekrar ciz.
7. Ex04'te yalnizca feature'lari min-max normalize et, donusen tabloyu yazdir ve karisan cifti tekrar ciz.
8. Ex05'te sadece `Train_knight.csv`yi rastgele iki yeni CSV'ye bol; iki dosyada ayni satirin bulunmadigini kontrol et.
9. Her figure'da baslik, iki eksen adi ve gerekiyorsa legend kullan. Renklerin neyi temsil ettigi belirsiz kalmasin.
10. Kendi ekraninda scriptleri hem Train hem Test ile calistir. Test'te `knight` yokken `KeyError` vermemeliler.

Mevcut dizinde iki bos dosya adi basinda gorunmez bir boslukla olusturulmus: `ex01/ Correlation.py` ve `ex05/ split.py`. PDF'nin teslim desenleri `Correlation.*` ve `split.*` oldugu icin, kodlamaya basladiginda bunlari basta bosluk olmadan tam olarak `Correlation.py` ve `split.py` yap. Diger dosya adlari PDF'deki desenle uyumludur: `Histogram.py`, `points.py`, `standardization.py`, `Normalization.py`.

## Savunmada kisa ve saglam cevaplar

- **Neden database yok?** Veri 398 + 171 satirlik CSV; subject dosyadan calismayi istiyor. `pandas` bellek ici tablo ve gorsellestirme icin yeterli.
- **Neden target'i feature'lara katmadin?** Target tahmin edilmek istenen cevaptir. Onu girdi gibi olceklersen modelin cevabi onceden gormus olur.
- **Neden Jedi/Sith'i 0/1 yaptin?** Pearson sayisal deger ister. Etiket kodlama yalnizca hesap icindir; ters kodlama korelasyon isaretini degistirir, gucunu degistirmez.
- **Neden iki scatter cifti?** Yuksek korelasyonlu feature'lar ayirimi, dusuk korelasyonlular ise ortusmeyi gorsel olarak sinar.
- **Neden iki farkli scaling?** Z-score merkez/standart sapmayi, min-max ise mutlak araligi duzenler; ayni donusum degillerdir.
- **Neden 80/20?** Yeterli egitim verisi ile gercekci validation olcumu arasinda yaygin bir dengedir; 398 satirda 318/80'e yuvarlanir.
- **Neden random seed?** Sonucun tekrar uretilmesini saglar.
- **Neden stratify?** Jedi/Sith oraninin her parca icinde temsil edilmesine yardim eder.

Bu projeyi bitirdiginde elinde henuz bir siniflandirici olmayacak. Ama bir sonraki adimda siniflandirici kurmak icin gereken veri anlayisi, olcekleme ve adil degerlendirme zemini hazir olacak.
