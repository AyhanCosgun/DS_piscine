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

---

# Ek Sorular: Satirlar, Korelasyon ve Ex01 Sonuclari

Bu bolum, Ex01'i sadece calisan bir kod parcasindan ibaret gormek yerine, cikan sayilarin ne dedigini anlayabilmen icin eklenmistir.

## 1) CSV satirlarini dogru mu anladim?

Evet, anladigin sey dogru.

- Her satir, veri setinin temsil ettigi bir hayali Force savascisinin/`knight`in kaydidir.
- `Sensitivity`, `Strength`, `Empowered` gibi 30 sayisal sutun, o kaydin olculmus beceri degerleridir. Bunlar **feature**lardir.
- `Train_knight.csv`de ek olarak bulunan `knight` sutunu, o satirin etiketi yani gercek sinifidir: `Jedi` ya da `Sith`.
- `Test_knight.csv`de `knight` yoktur. Ilgili satirlarin sinifini veri seti sana vermez.

Tek kucuk terminoloji notu: `knight` burada bir kisinin adi degil, PDF'nin target sutununa verdigi addir. Bu CSV'nin icinde target degeri olarak kelimenin kendisi degil, `Jedi` veya `Sith` metni yaziyor.

Bir satiri soyut olarak soyle dusunebilirsin:

```text
Empowered=0.18, Stims=140.0, Strength=120.0, ... , knight=Jedi
```

Bu, "bu kaydin olculen becerileri bunlar; gercek etiketi Jedi" demektir.

## 2) Testteki bir savasci kesin Jedi veya Sith mi, yoksa olasilikli mi?

Bu veri setinin tasarladigi problem **iki sinifli, kapali kumeli (closed-set) siniflandirma** problemidir. Yani veri seti varsayimina gore her kaydin gercek, tek bir sinifi vardir: ya Jedi ya Sith. "Hicbiri" veya "hem Jedi hem Sith" diye ucuncu bir etiket tanimlanmamistir.

Fakat bir **modelin tahmini** olasilikli olabilir. Ornegin ileride kuracagin bir model sunu uretebilir:

```text
P(Jedi | beceriler) = 0.72
P(Sith | beceriler) = 0.28
```

Bu, kisinin %72 Jedi ve %28 Sith oldugu anlamina gelmez. Model, feature'larin verdigi kanita dayanarak "Jedi tahminimden ne kadar eminim?" diye cevap verir. Sonra bir karar esigiyle tek etiket secilir: genellikle `P(Jedi) >= 0.50` ise Jedi, aksi halde Sith.

Gercek hayatta bir birey hem iki kategoriye ait olabilir veya hicbirine ait olmayabilir. O zaman problem cok etiketli (multi-label) ya da acik kumeli (open-set) olarak baska turlu tasarlanir. Bu subject boyle bir durum tanimlamiyor; test satirlarini bu iki siniftan birine ait kabul etmelisin.

## 3) `pd.read_csv(path)` ilk satiri otomatik olarak kolon adi mi yapar?

Evet. `pandas.read_csv(path)` varsayilan olarak `header="infer"` kullanir. Dosyanin ilk satiri metinsel basliklardan olusuyorsa onu kolon adlari olarak yorumlar; sonraki satirlari veri kabul eder.

Bu dosyanin baslangici kavramsal olarak soyledir:

```text
Sensitivity,Hability,Strength,...,Grasping,knight
11.2,18.4,92.1,...,0.07,Jedi
...
```

Dolayisiyla su koddan sonra `df.columns` icinde `Sensitivity`, `Hability`, ..., `knight` bulunur; baslik satiri veri satiri olmaz:

```python
df = pd.read_csv(path)
print(df.columns)
```

Bu SQL importundan farkli gorunebilir, cunku SQL aracinda baslik satirinin varligini ayri bir secenekle isaretlemis olabilirsin. Pandas bunu varsayilan olarak senin yerine yapar. Dosyada baslik olmasaydi acikca belirtirdin:

```python
df = pd.read_csv(path, header=None)
df = pd.read_csv(path, header=None, names=["feature_1", "feature_2"])
```

`header=None` kullanman bu mevcut CSV icin yanlis olur: `Sensitivity` satirini veri gibi okumaya calisir ve sayisal islemler bozulur.

## 4) Pearson ve point-biserial korelasyon nedir?

### Pearson korelasyonu

**Pearson product-moment correlation coefficient**, iki sayisal degiskenin dogrusal olarak birlikte nasil degistigini olcen `r` katsayisidir. Iki feature icin genel formulu soyledir:

```text
                    sum((x_i - x_mean) * (y_i - y_mean))
r(x, y) = ---------------------------------------------------------
          sqrt(sum((x_i - x_mean)^2) * sum((y_i - y_mean)^2))
```

Bu formulun sezgisel anlami:

1. Her degerden kendi ortalamasini cikarirsin. Boylece "ortalamanin ustunde mi, altinda mi?" bilgisi kalir.
2. Iki sapmayi carpabilirsin. Ikisi de ayni anda pozitif veya ayni anda negatifse carpim pozitiftir; biri yukari giderken digeri asagi gidiyorsa negatiftir.
3. Toplam bu beraber degisimi verir.
4. Paydadaki standartlastirma sayesinde sonuc olcekten bagimsiz olur ve `-1` ile `+1` arasinda kalir.

Esdeger bicimde Pearson korelasyonu, kovaryansin standart sapmalara bolunmus halidir:

```text
r(x, y) = cov(x, y) / (std(x) * std(y))
```

Pearson dogrusal iliskiyi gorur. Ornegin `y = x^2` U seklinde kusursuz bir iliski olabilir, ama x hem negatif hem pozitif degerler aliyorsa Pearson `r` sifira yakin cikabilir. Bu yuzden `r = 0`, "hicbir turden baglanti yok" degil, "belirgin dogrusal baglanti yok" demektir.

### Point-biserial correlation

**Point-biserial correlation**, bir degisken surekli sayisal, digeri dogal olarak iki sinifli oldugunda kullanilan korelasyondur. Bu projede:

- surekli degisken: ornegin `Empowered`, `Push` veya `Midi-chlorien`;
- ikili degisken: `knight`, `Jedi=1` ve `Sith=0` diye kodlanmis hali.

Matematiksel formulu yaygin olarak soyle yazilir:

```text
           (M_1 - M_0) * sqrt(n_1 * n_0 / n^2)
r_pb = ------------------------------------------
                         s_x
```

Burada `M_1`, target'i 1 olan grubun feature ortalamasi; `M_0`, target'i 0 olan grubun feature ortalamasidir. `n_1` ve `n_0` iki grubun satir sayilari, `n` toplam satir sayisi, `s_x` ise feature'in tum verideki standart sapmasidir.

Bu formulun cok onemli sonucu sudur: Target'i 0/1 olarak kodladiginda point-biserial korelasyon, **aynen Pearson korelasyonudur**. Yani bu iki satir ayni `r` degerini hesaplar:

```python
feature.corr(binary_target, method="pearson")
pointbiserialr(binary_target, feature).statistic
```

Point-biserial adi, "bir degisken iki nokta/iki sinif, digeri surekli" durumunu daha acik tarif ettigi icin kullanilir. Bu subjectteki teknik durum budur.

### Diger yaygin iliski olculeri

"Korelasyon" tek bir evrensel fonksiyon degildir. Degiskenlerin turune ve aradigin iliskiye gore secilir.

| Olcu | Ne zaman kullanilir? | Bu projeyle iliskisi |
| --- | --- | --- |
| Pearson `r` | Iki sayisal degisken, dogrusal iliski | 0/1 kodlanmis `knight` ile kullanilabilir |
| Point-biserial `r_pb` | Bir surekli, bir gercek ikili degisken | Ex01'in daha acik istatistiksel adi |
| Spearman `rho` | Sirali/rank veriler, monoton ama dogrusal olmayan iliski, aykiri deger duyarliligini azaltmak | Alternatif kesif olcusu olabilir |
| Kendall `tau` | Siralamalar, kucuk orneklem veya cok bagli deger | Spearman'a alternatif rank korelasyonu |
| Phi coefficient | Iki degisken de ikili | 0/1 kodlanmis iki kategorik alan varsa |
| Cramer's V | Iki kategorik degisken, ikiden fazla kategori olabilir | Feature'lar metinsel kategori olsaydi dusunulurdu |
| Eta / correlation ratio | Kategorik grup ile surekli degisken, dogrusal olmayan grup farki | Siniflarin feature dagilimlari icin ek analiz olabilir |
| Mutual information / distance correlation | Daha genel, dogrusal olmayan bagimlilik arandiginda | ML feature kesfinde ek bir arac olabilir |

Her olcuye bakmak zorunda degilsin. Ex01 icin PDF'nin gosterdigi, pandas'ta kolayca hesaplanan ve 0/1 hedefle matematiksel olarak dogru olan secim Pearson/point-biserial'dir.

## 5) `r` 0, 1 ve -1'e yakin olunca ne anlama gelir?

Burada iki farkli "1" kavrami var; karistirmamak cok onemli:

- `Jedi=1`, `Sith=0`: target'i hesap icin sayiya cevirirken yaptigin **etiket kodlama**.
- `r = 1.0`: iki degisken arasindaki **kusursuz pozitif korelasyon katsayisi**.

Birbirleriyle ayni sey degildir.

Bu projede `Jedi=1`, `Sith=0` kullandiginda her feature sonucu soyle okunur:

| `r` degeri | Dogru yorum |
| --- | --- |
| `r` +1'e yakin | Feature buyudukce satirin Jedi olmasiyla guclu pozitif dogrusal baglanti var |
| `r` 0'a yakin | Feature ortalamalari/sinirli dogrusal baglanti iki sinifi ayirmiyor |
| `r` -1'e yakin | Feature buyudukce satirin Sith olmasiyla guclu dogrusal baglanti var |

Ornegin `Empowered = 0.793652`, bu feature'in yuksek degerlerinin veri setinde Jedi koduyla guclu pozitif iliskili oldugunu soyler. **"Bu satirin %79.3652 Jedi olma ihtimali var" demek degildir.** Korelasyon bir olasilik veya model tahmini degil, tum veri setindeki iki degisken icin tek bir ozet katsayidir.

`Deflection = -0.026489`, feature degeri arttikca Sith koduna dogru cok hafif bir yon oldugunu soyler; ancak mutlak deger cok kucuk oldugu icin pratikte neredeyse dogrusal iliski yoktur.

Hedef kodlamasini tersine cevirirsen:

```python
y = train_data["knight"].map({"Jedi": 0, "Sith": 1})
```

`Empowered` yaklasik `-0.793652` olur, `Deflection` yaklasik `+0.026489` olur. Mutlak degerler degismez. Bu nedenle bir feature'in tek basina dogrusal sinif sinyalinin gucunu karsilastirirken `abs(r)` kullanilir.

`-1` ile `+1` araligi **her feature-target cifti icin** gecerlidir. Ex01'de 30 farkli korelasyon sonucu uretilir: `Empowered` ile target, `Stims` ile target, `Push` ile target gibi. Bu aralik target'in "tek sonucunun" araligi degildir.

Ikili target durumunda `r = +1` veya `r = -1` son derece guclu bir durum olurdu: her sinifin feature degerleri kendi icinde hic yayilmadan, iki ayri sabit degerde toplanmis olurdu. Gercek veride siniflarin kendi ic varyasyonu oldugu icin buna yaklasmak zordur.

Yuksek `abs(r)` faydali bir ilk ipucudur, fakat feature'in tek basina kesin karar verdigi garantisi degildir. Siniflar yine de ortusebilir; ayrica tek tek zayif gorunen iki feature birlikte cok faydali olabilir.

## 6) Ex01'de hangi fonksiyon daha mantikli? Sektorde hangisi kullanilir?

Bu subject icin benim onerim:

```python
correlations = X.corrwith(y, method="pearson")
```

Sebebi, 30 feature ile **tek bir target** arasinda 30 korelasyonu bir kerede, okunakli bicimde vermesidir. Kodun niyetini de acikca anlatir.

| Arac | Ne zaman en uygun? | Ex01 icin karar |
| --- | --- | --- |
| `Series.corr()` | Yalnizca bir feature-target cifti, deney veya hata ayiklama | Dogru ama 30 sutun icin dongu yazman gerekir |
| `DataFrame.corrwith()` | Bir DataFrame'deki her feature'i tek bir Series ile karsilastirma | En uygun secim |
| `scipy.stats.pointbiserialr()` | `r` ile birlikte p-value, hipotez testi veya istatistiksel raporlama gerektiginde | Semantik olarak cok uygun; tum feature'lar icin dongu/apply gerekir |

Profesyonel calismada bunlar rakip kamplar degildir:

- `pandas.corr`, `corrwith` veya `DataFrame.corr()` EDA'da hizli korelasyon tablosu icin cok yaygindir.
- `scipy.stats.pointbiserialr`, `pearsonr`, `spearmanr` gibi fonksiyonlar katsayiya ek olarak p-value ve bazen guven araligi/hypothesis-testing gerektiginde kullanilir.
- Model kurarken feature secimi yalnizca korelasyona birakilmaz. Cross-validation, regularized model katsayilari, permutation importance, `sklearn` feature-selection araclari ve alan bilgisiyle birlikte degerlendirilir.

Bu nedenle ogrenme sirasi olarak once `Series`, `DataFrame` ve index hizalamasini anlamak; sonra bu Ex01'de `corrwith` kullanmak; p-value neden gerekli oldugunda `scipy.stats`e gecmek iyi bir siradir. Subjectin cikti gereksinimi yalnizca korelasyon tablosu oldugu icin `corrwith` yeterlidir.

## 7) `X.corrwith(y, method="pearson").sort_values(ascending=False)` tam olarak ne yapiyor?

Kodun parcalari su anlama gelir:

```python
X = train_data.drop(columns="knight")
y = train_data["knight"].map({"Jedi": 1, "Sith": 0})
```

- `X`, boyutu `(398, 30)` olan DataFrame'dir: her sutun bir feature, her satir bir savascidir.
- `y`, uzunlugu `398` olan bir Series'tir: ayni satirlar icin `0` veya `1` target degeri.

Ardindan:

```python
correlations = X.corrwith(y, method="pearson").sort_values(ascending=False)
```

1. `X.corrwith(y, method="pearson")`, X'in **her sutunu** icin `o_sutun.corr(y, method="pearson")` hesaplar.
2. Pandas bunu satir indexlerine gore hizalar. Eksik deger olsaydi, o feature ve target icin karsilikli eksik olmayan satirlari kullanirdi. Bu CSV'de eksik deger yoktur.
3. Sonuc, uzunlugu 30 olan bir `Series`tir. Index'leri feature adlari, degerleri korelasyon katsayilaridir:

```text
Empowered     0.793652
Prescience    0.790066
...
Survival     -0.043099
```

4. `.sort_values(ascending=False)`, bu Series'i sayisal degerine gore buyukten kucuge siralar. Bu kodlamada Jedi ile pozitif iliskili feature'lar ustte, Sith yonundeki negatif feature'lar altta gorunur.

Bu islem `X`i veya `y`yi degistirmez. Asagidaki daha uzun dongu ile ayni fikirdir:

```python
correlations = pd.Series({
    column: X[column].corr(y, method="pearson")
    for column in X.columns
}).sort_values(ascending=False)
```

"En guclu iliski" isaretten bagimsiz aranacaksa siralama farkli olmalidir:

```python
strongest_by_magnitude = correlations.sort_values(key=lambda values: values.abs(), ascending=False)
```

Bu mevcut veri setinde yuksek pozitif degerler zaten baskin oldugu icin ilk feature ayni kalir. Baska bir veri setinde cok guclu negatif iliski varsa, sadece `ascending=False` kullanmak onu listenin altina iter.

## 8) Neden elle `knight: 1.0` ekliyoruz? Bu "hep Jedi" mi demek?

Hayir. `1.0` burada Jedi kodu veya tahmin sonucu degildir.

Once `X = train_data.drop(columns="knight")` satiri, target'i feature tablosundan bilerek cikariyor. Bu nedenle `X.corrwith(y)` yalnizca 30 feature icin sonuc doner; `knight` kendiliginden o sonuca dahil olmaz.

PDF ornek tablosu `knight  1.000000` satiriyla basladigi icin bu goruntuyu yakalamak amaciyla su satir eklenir:

```python
result = pd.concat([pd.Series({"knight": 1.0}), correlations])
```

Istatistiksel anlami, bir degiskenin kendisiyle korelasyonudur:

```text
corr(y, y) = cov(y, y) / (std(y) * std(y))
           = var(y) / var(y)
           = 1
```

Target'ta hem Jedi hem Sith oldugu ve varyansi sifir olmadigi surece bu her zaman `1.0` olur. Yeni bilgi tasimaz; yalnizca korelasyon matrisinin diagonalindeki matematiksel kimligi ve PDF'nin cikti bicimini gosterir. `Jedi=1` kodu ile `corr(knight, knight)=1.0` ayni rakami kullansa da anlami tamamen farklidir.

Bu satir teknik olarak zorunlu degildir. PDF bu satiri istemeseydi yalnizca `print(correlations)` yeterli olurdu. Target satirini elle eklemeden bir korelasyon matrisiyle de otomatik uretebilirsin:

```python
numeric_frame = X.assign(knight=y)
result = numeric_frame.corr(method="pearson")["knight"].sort_values(ascending=False)
```

Bu ikinci yaklasim, `knight`i sayisal gecici sutun olarak matrise ekledigi icin diagonal `1.0` degerini otomatik hesaplar. Ex01 icin `corrwith` daha dogrudan ve okunaklidir.

## 9) Benim Ex01 sonucum PDF orneginden farkli; negatifler ve Midi-chlorien histogrami neden boyle?

### PDF ornegi ile fark

Senin ciktin, bu depodaki `Train_knight.csv` icin tutarli gorunuyor. Onceki bolumde belirtilen PDF/CSV surum farki burada da goruluyor: PDF ornegi `Force` sutununu gosterirken bu CSV `Pull` sutununu iceriyor. Sayilarin birkac son hanesinin ve kimi sutunlarin farkli olmasi, PDF orneginin baska bir veri/surumle uretilmis olduguna isaret eder.

Yerel veri uzerinde kodun su mantigi dogrudur:

```python
y = train_data["knight"].map({"Jedi": 1, "Sith": 0})
correlations = train_data.drop(columns="knight").corrwith(y, method="pearson")
```

Dolayisiyla degerlendirmede sabit PDF sayilarini taklit etmeye calisma; gonderilen CSV'den dinamik hesapla.

### Negatif degerler hata mi?

Hayir. Negatif deger, `Jedi=1`, `Sith=0` kodlamasinda feature buyurken target'in Sith yonune cok az kaydigi anlamina gelir. Ornegin:

```text
Push        -0.019446
Deflection  -0.026489
Survival    -0.043099
```

Bu sayilarin mutlak degerleri cok kucuk oldugu icin yonleri pratik bir tahmin sinyali olarak guvenilir degildir. Ters kodlama yapsan hepsi pozitif olurdu, ama yine cok zayif kalirlardi.

### Neden `Midi-chlorien` en kucuk mutlak korelasyon ama histogramda farkli gorunuyor?

Bu cok iyi bir gozlem; cevabi, histogramla Pearson'un ayni seyi olcmemesidir.

1. Point-biserial/Pearson, ikili target ile feature arasinda esasen **standartlastirilmis ortalama farkini ve dogrusal yonu** olcer. `Midi-chlorien`de ortalamalar neredeyse aynidir:

```text
                 Jedi       Sith
ortalama       0.062687   0.062576
medyan         0.061360   0.061345
```

Bu nedenle `r = 0.008132` cikar: neredeyse sifir dogrusal/ortalama farki. `scipy.stats.pointbiserialr` ile p-value yaklasik `0.8715`tir; bu veri boyutunda gozlenen farkin sans eseri gorulmesi cok olasidir.

2. Histogram ise dagilimin sekline, yayilimina, kuyruklarina ve bin secimine bakarak gozunde bir izlenim olusturur. Iki grubun ortalamasi ayni kalirken varyanslari veya sekilleri farkli gorunebilir. `Midi-chlorien` icin standart sapmalar Jedi'de yaklasik `0.00744`, Sith'te `0.00610`dur. Bu sekil/yayilim farki, ortalama temelli Pearson katsayisini buyutmek zorunda degildir.

3. Mevcut `Histogram.py`de iki sinif icin `ax.hist(..., bins=40)` iki kez ayri cagriliyor. Matplotlib her grup icin bin sinirlarini o grubun kendi minimum/maksimumundan hesaplayabilir. Mavi ve kirmizi cubuklar bu nedenle ayni x araliklarini temsil etmeyebilir. Ayrica Jedi 152, Sith 246 satirdir ve `density=True` kullanilmadigi icin cubuk yukseklikleri olasilik yogunlugunu degil ham sayiyi gosterir. Bu iki ayrinti, "ne kadar ortusuyor?" goz karari icin grafigi daha az guvenilir yapar.

Iki grubu daha adil karsilastirmak icin ortak bin sinirlari ve yogunluk kullan:

```python
import numpy as np

edges = np.histogram_bin_edges(train_data[column], bins=40)
for label, group in train_data.groupby("knight"):
    ax.hist(group[column], bins=edges, density=True, alpha=0.45, label=label)
```

4. "Iki sinifin tum dagilimlari farkli mi?" sorusu Pearson'dan farkli bir sorudur. Ornegin Kolmogorov-Smirnov (KS) testi iki ampirik dagilimin en buyuk CDF farkina bakar. Bu veride `Midi-chlorien` icin KS istatistigi yaklasik `0.127`, `Push` icin `0.089`, `Deflection` icin `0.107`dir. Yani `Midi-chlorien`de sekil farki diger ikisinden gozle daha belirgin gorunebilir. Ancak kendi p-value'su yaklasik `0.086`dir; geleneksel `%5` esiginde bu da guclu kanit sayilmaz.

Sonuc olarak cizim ile korelasyonun ayni sirayi vermesi beklenmez. Histogram bir EDA aracidir; Pearson/point-biserial hedefle dogrusal ortalama iliskisinin bir ozetidir. Ikisini birlikte kullanmak, tek bir resim veya tek bir sayiya gereksiz guvenmekten daha saglamdir.
