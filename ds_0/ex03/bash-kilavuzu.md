# Bash Script Kılavuzu

Bu belge iki soruyu birlikte cevaplar:

1. Ex03 için neden Bash scripti kullanılabilir, SQL dosyası tek başına yeterli olur mu?
2. Bash diliyle script nasıl yazılır, kullanılan özel ifadeler ne anlama gelir?

---

## 1. Ex03 için Bash mi, SQL mi?

### Yalnızca SQL dosyasıyla yapılabilir mi?

Kısmen evet. PostgreSQL tarafında `psql` ile çalıştırılan bir SQL dosyası içine birden fazla tablo oluşturma ve CSV aktarma komutu yazılabilir:

```sql
CREATE TABLE data_2022_oct (...);
\copy data_2022_oct FROM 'subject/customer/data_2022_oct.csv' WITH (FORMAT csv, HEADER true);

CREATE TABLE data_2022_nov (...);
\copy data_2022_nov FROM 'subject/customer/data_2022_nov.csv' WITH (FORMAT csv, HEADER true);
```

Ancak bu yaklaşımda her dosya için:

- dosya adını,
- tablo adını,
- tablo tanımını,
- `\copy` komutunu

elle yazman gerekir. Yeni bir CSV eklendiğinde SQL dosyasını da değiştirmen gerekir. Bu, Ex03'te istenen otomatik dosya keşfini sağlamaz.

PostgreSQL'in `psql` aracı bazı meta-komutlar ve `\gexec` gibi özelliklerle daha dinamik hale getirilebilir. Yine de dosya sistemindeki tüm CSV dosyalarını bulmak, dosya adlarını güvenli biçimde tablo adlarına dönüştürmek ve işletim sistemiyle konuşmak Bash kadar doğal değildir.

### Bash script neden uygundur?

Bash işletim sistemi ile veritabanı arasında orkestrasyon yapar:

1. Klasördeki dosyaları bulur.
2. Her dosyanın yolunu ve adını işler.
3. `psql` komutunu çağırır.
4. PostgreSQL'e tablo oluşturma ve veri aktarma SQL'ini gönderir.
5. Hata olursa işlemi durdurur.

Örneğin Bash tarafı dosyaları bulur:

```bash
for csv_file in "$CUSTOMER_DIR"/*.csv; do
    table_name="$(basename "$csv_file" .csv)"
    psql ...
done
```

SQL tarafı ise veritabanı işlemini yapar:

```sql
CREATE TABLE ...;
\copy ...;
```

Bu nedenle burada en mantıklı sorumluluk dağılımı şudur:

- Dosya sistemi ve tekrar eden işlem: Bash
- Tablo ve veri işlemleri: PostgreSQL SQL

### İş hayatında ne kullanılır?

Küçük bir görev veya eğitim projesinde Bash + `psql` gayet uygundur. Gerçek projelerde kullanılan araç, veri miktarına ve iş akışının karmaşıklığına göre değişir:

- Basit sunucu görevleri: Bash, `psql`, `cron`
- Veri yükleme ve dönüşüm: Python, SQL, Pandas, Polars
- Büyük veri: Spark, dbt, Airflow, Dagster
- Bulut veri ambarları: ELT araçları ve orkestrasyon platformları
- Tekrarlanan üretim işleri: Docker, CI/CD ve zamanlayıcılar

Kurumsal ortamda genellikle tek büyük Bash scripti yerine, işi parçalara ayıran ve loglama, yeniden deneme, yapılandırma, test ve izleme sağlayan araçlar kullanılır. Fakat Bash'in temellerini bilmek yine önemlidir; Docker, CI/CD, Linux sunucuları ve veri pipeline'larının çevresinde çok sık kullanılır.

---

## 2. Bash nedir?

Bash, Unix ve Linux sistemlerinde yaygın kullanılan bir **komut yorumlayıcısıdır**. Bash hem terminalde komutları etkileşimli olarak çalıştırabilir hem de komutları bir dosyada saklayıp script olarak çalıştırabilir.

Bash'in açılımı **Bourne Again Shell**'dir. Bash, Python veya Java gibi genel amaçlı bir programlama dilinden farklı olarak özellikle şu işler için tasarlanmıştır:

- Komut çalıştırmak
- Dosya ve klasörlerle çalışmak
- Programları birbirine bağlamak
- Ortam değişkenlerini yönetmek
- İşletim sistemi görevlerini otomatikleştirmek

Bash'te her komutun bir **çıkış kodu** vardır:

- `0`: Başarılı
- `0` dışındaki değerler: Hata veya başarısızlık

Bu özellik scriptlerin hata kontrolünün temelidir.

---

## 3. İlk Bash scripti

Bir dosya oluştur:

```bash
#!/usr/bin/env bash

echo "Merhaba Bash"
```

İlk satıra **shebang** denir:

```bash
#!/usr/bin/env bash
```

Bu satır işletim sistemine dosyanın Bash ile çalıştırılacağını söyler. `env`, Bash programını sistemin `PATH` değişkeninde arar.

Çalıştırılabilir izin ver:

```bash
chmod +x hello.sh
```

Çalıştır:

```bash
./hello.sh
```

İzin vermeden de Bash'e dosyayı vererek çalıştırabilirsin:

```bash
bash hello.sh
```

### Yorum satırı

```bash
# Bu bir yorumdur.
echo "Bu komut çalışır"
```

`#` işaretinden satır sonuna kadar olan bölüm Bash tarafından çalıştırılmaz.

---

## 4. Değişkenler

### Değişken tanımlama

Bash'te atama yapılırken `=` işaretinin iki tarafında boşluk bırakılmaz:

```bash
name="Ayhan"
count=5
```

Yanlış kullanım:

```bash
name = "Ayhan"
```

Bash bunu atama olarak değil, `name` isimli bir komut çalıştırma denemesi olarak yorumlar.

### Değişken kullanma

Değişkenin başına `$` konur:

```bash
name="Ayhan"
echo "$name"
```

Süslü parantez karmaşayı önler:

```bash
prefix="data"
echo "${prefix}_2022_oct"
```

Değişkenleri çoğu zaman çift tırnak içine al:

```bash
file_name="my file.csv"
echo "$file_name"
```

Çift tırnak kullanılmazsa boşluklar kelimeleri ayırabilir ve beklenmeyen davranış oluşabilir.

### Ortam değişkenleri

Bash'in ve işletim sisteminin hazır değişkenleri vardır:

```bash
echo "$HOME"
echo "$PATH"
echo "$PWD"
```

Bir komutu çalıştırırken geçici değişken verebilirsin:

```bash
PGPASSWORD=mysecretpassword psql -h localhost -U acosgun -d piscineds
```

Bu değişken yalnızca o komutun ortamında bulunur.

### Özel parametreler

- `$0`: Scriptin adı
- `$1`, `$2`: Birinci ve ikinci komut satırı argümanı
- `$#`: Argüman sayısı
- `"$@"`: Tüm argümanlar, ayrı ayrı korunarak
- `$?`: Son komutun çıkış kodu
- `$$`: Çalışan Bash process'inin ID'si
- `${BASH_SOURCE[0]}`: İçinde bulunulan Bash dosyasının yolu

Örnek:

```bash
#!/usr/bin/env bash

echo "Script: $0"
echo "Argüman sayısı: $#"
echo "İlk argüman: ${1:-verilmedi}"
```

Çalıştırma:

```bash
bash args.sh birinci ikinci
```

### Mevcut `automatic_table.sh` hakkında

Dosyanın şu anki içeriği:

```bash
#!/usr/bin/env bash
echo "selam"
$A = $5
echo $A
```

Buradaki `$A = $5` Bash'te doğru değişken ataması değildir. Doğru biçim şöyledir:

```bash
A="$5"
echo "$A"
```

Fakat `$5`, scriptin beşinci komut satırı argümanıdır. Script beşinci argüman verilmeden çalıştırılırsa beklenen değer gelmez. Ayrıca bu üç satır Ex03'ün CSV dosyalarını bulup PostgreSQL tablolarına aktarma işini yapmaz. Bu nedenle bu dosya şu anda bir Bash denemesi olarak görülmeli; Ex03 çözümü için otomatik tablo scriptiyle değiştirilmelidir.

---

## 5. Bash'teki veri türleri

Bash, Python gibi güçlü ve katı tipli bir dil değildir. Temel olarak değişkenlerin çoğu **metin** gibi davranır. Sayısal aritmetik gerektiğinde Bash bunu ayrıca değerlendirir.

### String

```bash
city="Istanbul"
message='Merhaba dünya'
```

Tek tırnak içindeki metin değişken genişletmez:

```bash
name="Ayhan"
echo 'Merhaba $name'   # Kelimesi kelimesine yazdırır
echo "Merhaba $name"   # Ayhan değerini kullanır
```

### Integer

```bash
first=10
second=3
result=$((first + second))
echo "$result"
```

Bash'in yerleşik aritmetik desteği esas olarak tam sayılar içindir.

### Ondalıklı sayılar

Bash'in normal aritmetik yapısı ondalıklı sayıları güvenilir biçimde işlemez. Bunun için `bc`, `awk` veya Python kullanılabilir:

```bash
result="$(awk 'BEGIN { printf "%.2f", 10.5 / 3 }')"
echo "$result"
```

### Array

```bash
files=("oct.csv" "nov.csv" "dec.csv")
echo "${files[0]}"

for file in "${files[@]}"; do
    echo "$file"
done
```

### Associative array

Anahtar-değer yapısı için Bash 4+ gerekir:

```bash
declare -A settings
settings[host]="localhost"
settings[database]="piscineds"
echo "${settings[database]}"
```

### Boolean

Bash'te klasik `true` ve `false` tipleri yoktur. `true` ve `false` komutları vardır:

```bash
if true; then
    echo "Basarili"
fi
```

Genellikle koşullar komutların çıkış kodlarıyla değerlendirilir.

---

## 6. Komut çıktısını değişkene alma

Bir komutun çıktısını `$()` ile değişkene alabilirsin:

```bash
current_directory="$(pwd)"
echo "$current_directory"
```

Eski backtick yazımı da vardır ama `$()` daha okunaklıdır:

```bash
# Eski biçim
current_directory="`pwd`"

# Önerilen biçim
current_directory="$(pwd)"
```

Ex03'te:

```bash
table_name="$(basename "$csv_file" .csv)"
```

`basename`, dosya yolunun son parçasını alır ve `.csv` uzantısını çıkarır.

---

## 7. Koşullar

### `if`

```bash
if [[ "$name" == "Ayhan" ]]; then
    echo "Isim dogru"
else
    echo "Farkli isim"
fi
```

Bash'te modern koşul yazımı için `[[ ... ]]` tercih edilir.

### Dosya kontrolleri

```bash
if [[ -f "$file" ]]; then
    echo "Normal bir dosya"
fi

if [[ -d "$directory" ]]; then
    echo "Bir klasor"
fi

if [[ -e "$path" ]]; then
    echo "Yol mevcut"
fi
```

Yaygın testler:

- `-e`: Yol mevcut mu?
- `-f`: Normal dosya mı?
- `-d`: Klasör mü?
- `-r`: Okunabilir mi?
- `-w`: Yazılabilir mi?
- `-x`: Çalıştırılabilir mi?

Ex03'te kullanılan ifade:

```bash
[ -e "$csv_file" ] || continue
```

Bu, dosya mevcut değilse döngünün sonraki turuna geçer. `[ ... ]`, Bash'in eski test komut biçimidir. Aynı kontrol modern biçimde şöyle yazılabilir:

```bash
if [[ ! -e "$csv_file" ]]; then
    continue
fi
```

### Sayısal karşılaştırmalar

```bash
if (( count > 0 )); then
    echo "Kayit var"
fi
```

Alternatif operatörler:

- `-eq`: Eşit
- `-ne`: Eşit değil
- `-lt`: Küçük
- `-le`: Küçük veya eşit
- `-gt`: Büyük
- `-ge`: Büyük veya eşit

Metin karşılaştırmalarında:

- `==`: Eşit
- `!=`: Farklı
- `-z`: Boş metin
- `-n`: Boş olmayan metin

---

## 8. Döngüler

### `for`

```bash
for item in one two three; do
    echo "$item"
done
```

Dosyalar üzerinde:

```bash
for csv_file in subject/customer/*.csv; do
    echo "$csv_file"
done
```

Değişkenli klasör yolu kullanırken tırnaklamaya dikkat et. Dosya glob'unu (`*.csv`) tırnak içine almak istemezsin; aksi halde Bash dosya listesini genişletmeyebilir.

### `while`

```bash
count=1
while (( count <= 3 )); do
    echo "$count"
    ((count++))
done
```

### `until`

```bash
count=1
until (( count > 3 )); do
    echo "$count"
    ((count++))
done
```

### `break` ve `continue`

```bash
for file in *.csv; do
    [[ -e "$file" ]] || continue
    [[ "$file" == "skip.csv" ]] && continue
    echo "$file"
done
```

- `continue`: Döngünün sonraki turuna geçer.
- `break`: Döngüyü tamamen bitirir.

---

## 9. Fonksiyonlar

Tekrar eden kodu fonksiyona alabilirsin:

```bash
log_message() {
    printf '[INFO] %s\n' "$1"
}

log_message "Import basladi"
```

Fonksiyon argümanları da `$1`, `$2` şeklinde kullanılır. Fonksiyonun dönüş değeri çıkış kodudur:

```bash
check_file() {
    [[ -f "$1" ]]
}

if check_file "data.csv"; then
    echo "Dosya var"
fi
```

Bash fonksiyonları normalde değer döndürmez; sonuç üretmek gerekiyorsa `printf` ile çıktı verip `$(...)` ile yakalamak veya global değişken kullanmak mümkündür. Basit scriptlerde gereksiz karmaşıklık oluşturmamak önemlidir.

---

## 10. `set`, `pipefail` ve hata yönetimi

### `set -e`

```bash
set -e
```

Bir komut başarısız olduğunda scriptin durmasını ister. Ex03 gibi veri aktarımında bu önemlidir; bir CSV aktarımı başarısız olursa sonraki tabloların sessizce işlenmesine devam edilmesi istenmeyebilir.

`set -e` her özel durumda kusursuz değildir. Örneğin `if`, `while` ve `||` içindeki bazı komut hataları istisna olarak değerlendirilir. Bu nedenle kritik komutlarda açık kontrol de yazılabilir.

### `set -u`

```bash
set -u
```

Tanımlanmamış değişken kullanılırsa hata üretir. Örneğin:

```bash
set -u
printf '%s\n' "$undefined_variable"
```

hata verir. İsteğe bağlı değerler için varsayılan kullanılabilir:

```bash
value="${OPTIONAL_VALUE:-default}"
```

### `set -o pipefail`

Pipe, bir komutun çıktısını diğerine aktarır:

```bash
cat file.txt | grep error
```

Normalde pipe'ın sonucu çoğunlukla son komutun çıkış kodudur. İlk komut başarısız olsa bile son komut başarılı görünürse hata gizlenebilir.

```bash
set -o pipefail
```

Pipe içindeki herhangi bir komut hata verirse zincirin başarısız sayılmasını sağlar.

### `set -euo pipefail`

Ex03 scriptindeki:

```bash
set -euo pipefail
```

şu üç ayarı birlikte etkinleştirir:

- `-e`: Hata sonrası dur.
- `-u`: Tanımsız değişkene izin verme.
- `pipefail`: Pipe içindeki hataları gizleme.

Bu, scriptler için iyi bir başlangıçtır ancak her hatayı tek başına ele almaz. Dış komutların çıktısını ve loglarını da kontrol etmek gerekir.

### Çıkış kodunu kontrol etme

```bash
some_command
status=$?

if (( status != 0 )); then
    echo "Komut basarisiz: $status" >&2
    exit "$status"
fi
```

Daha kısa biçim:

```bash
if ! some_command; then
    echo "Komut basarisiz" >&2
    exit 1
fi
```

- `exit 0`: Başarılı bitir.
- `exit 1`: Genel hata ile bitir.
- `>&2`: Mesajı standart hata kanalına gönderir.

### `trap`

Script biterken veya sinyal aldığında işlem yapmak için:

```bash
cleanup() {
    echo "Temizlik yapiliyor"
}

trap cleanup EXIT
```

Geçici dosyaları silmek veya bağlantıyı kapatmak gibi işler için kullanılır.

---

## 11. `BASH_SOURCE[0]` ve script yolunu bulma

Ex03 scriptindeki ifade:

```bash
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
```

biraz yoğun görünür, parçalara ayıralım.

### `${BASH_SOURCE[0]}`

`BASH_SOURCE`, Bash'in özel bir dizisidir. İçinde çalışan script veya fonksiyon dosyalarının yollarını tutar. `[0]`, mevcut script dosyasını belirtir.

Örneğin script şu konumdaysa:

```text
/home/ayhan/.../ds_0/ex03/automatic_table.sh
```

`${BASH_SOURCE[0]}` bu dosya yolunu verir.

Bu, `$0` ile benzer görünür; ancak dosya başka bir Bash dosyası tarafından `source` edilirse `BASH_SOURCE[0]` kaynak dosyasının konumunu daha güvenilir biçimde korur.

### `dirname`

```bash
dirname "/home/project/ex03/automatic_table.sh"
```

çıktı:

```text
/home/project/ex03
```

Yani dosyanın bulunduğu klasörü verir.

### `cd --`

```bash
cd -- "$directory"
```

Belirtilen klasöre geçer. `--`, klasör adı `-` ile başlasa bile bunun seçenek olarak yorumlanmasını engeller.

### `pwd`

```bash
pwd
```

Geçerli klasörün mutlak yolunu yazdırır.

### Tam ifade

```bash
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
```

şu anlama gelir:

1. Script dosyasının yolunu al.
2. `dirname` ile scriptin klasörünü bul.
3. O klasöre geç.
4. Mutlak yolu `pwd` ile al.
5. Sonucu `SCRIPT_DIR` değişkenine koy.

Böyle yazınca scripti hangi klasörden çağırdığın önemli olmaz:

```bash
cd /tmp
/home/project/ex03/automatic_table.sh
```

Script yine kendi bulunduğu yeri referans alabilir.

---

## 12. `<<'SQL'`: heredoc kullanımı

Ex03 scriptinde Bash komutunun sonunda şu yapı vardır:

```bash
psql ... <<'SQL'
SQL komutlari buraya gelir
SQL
```

Buna **here document**, kısaca **heredoc** denir. Çok satırlı metni bir komutun standart girdisine verir.

Burada:

```bash
<<'SQL'
```

- `<<`: Heredoc başlangıcıdır.
- `SQL`: Sınır etiketi, yani delimiter'dır.
- Tek tırnak: İçerideki Bash değişkenlerinin Bash tarafından genişletilmesini engeller.

Bitişteki tek başına:

```bash
SQL
```

aynı delimiter'dır. Başında boşluk bulunmamalıdır.

### Neden `SQL` yazılıyor?

`SQL` özel bir Bash anahtar kelimesi değildir. İstediğin başka bir kelimeyi kullanabilirsin:

```bash
cat <<'TEXT'
Bu metin
TEXT
```

SQL gönderildiği için `SQL` adı okunabilirlik sağlar.

### Tırnaklı ve tırnaksız heredoc farkı

Tırnaksız biçimde Bash değişkenleri genişletilir:

```bash
name="Ayhan"
cat <<TEXT
Merhaba $name
TEXT
```

çıktı:

```text
Merhaba Ayhan
```

Tırnaklı biçimde genişletme yapılmaz:

```bash
name="Ayhan"
cat <<'TEXT'
Merhaba $name
TEXT
```

çıktı:

```text
Merhaba $name
```

Ex03 scriptinde `<<'SQL'` kullanımı, SQL metninin Bash tarafından bozulmamasını sağlar. `psql` değişkenleri ise ayrıca şu seçeneklerle verilir:

```bash
-v table_name="$table_name"
-v csv_file="$csv_file"
```

PostgreSQL `psql` bu değişkenleri SQL içinde şöyle değiştirir:

```sql
DROP TABLE IF EXISTS :"table_name";
\copy :"table_name" FROM :'csv_file' WITH (FORMAT csv, HEADER true)
```

Bu iki farklı genişletme mekanizmasını ayırmak önemlidir:

- Bash değişkenleri: `$name`
- `psql` değişkenleri: `:"table_name"` veya `:'csv_file'`

---

## 13. Pipe, yönlendirme ve standart kanallar

Bash programlarla üç temel kanal üzerinden konuşur:

- Standart girdi: `stdin`
- Standart çıktı: `stdout`
- Standart hata: `stderr`

### Pipe

```bash
cat file.txt | grep "error"
```

İlk komutun çıktısı ikinci komutun girdisi olur.

### Çıktıyı dosyaya yazma

```bash
echo "merhaba" > output.txt
```

`>` dosyanın içeriğini silip yeniden yazar.

```bash
echo "yeni satir" >> output.txt
```

`>>` dosyanın sonuna ekler.

### Hata çıktısı

```bash
echo "Hata olustu" >&2
```

Mesajı standart hata kanalına gönderir.

### Hem çıktı hem log

```bash
./automatic_table.sh > import.log 2>&1
```

Normal çıktıyı ve hata çıktısını aynı log dosyasına yönlendirir.

---

## 14. Ex03 scriptinin mantığı

Ex03 için önerilen scriptin ana iskeleti şöyledir:

```bash
#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd -- "$SCRIPT_DIR/.." && pwd)"
CUSTOMER_DIR="$PROJECT_DIR/subject/customer"

for csv_file in "$CUSTOMER_DIR"/*.csv; do
    [ -e "$csv_file" ] || continue
    table_name="$(basename "$csv_file" .csv)"

    psql -h localhost -U acosgun -d piscineds \
        -v ON_ERROR_STOP=1 \
        -v table_name="$table_name" \
        -v csv_file="$csv_file" <<'SQL'
DROP TABLE IF EXISTS :"table_name";

CREATE TABLE :"table_name" (
    event_time TIMESTAMPTZ,
    event_type VARCHAR(32),
    product_id INTEGER,
    price NUMERIC(10, 2),
    user_id BIGINT,
    user_session UUID
);

\copy :"table_name" FROM :'csv_file' WITH (FORMAT csv, HEADER true)
SQL
done
```

Akış:

1. Bash çalışır.
2. Hata seçenekleri etkinleşir.
3. Scriptin bulunduğu klasör hesaplanır.
4. `subject/customer` klasörü bulunur.
5. Her `.csv` dosyası için döngü çalışır.
6. Dosya adından tablo adı üretilir.
7. `psql`, SQL metnini PostgreSQL'e gönderir.
8. Mevcut tablo varsa silinir.
9. Tablo yeniden oluşturulur.
10. CSV kayıtları `\copy` ile yüklenir.
11. Bir hata olursa `ON_ERROR_STOP=1` ve `set -e` sayesinde işlem durur.

### `ON_ERROR_STOP=1`

Bu, Bash değil `psql` seçeneğidir:

```bash
-v ON_ERROR_STOP=1
```

SQL komutlarından biri hata verirse `psql` sonraki komutları çalıştırmadan başarısız çıkış koduyla biter. Bash'teki `set -e` de bu başarısız çıkış kodunu görerek scripti durdurur.

---

## 15. Güvenli Bash alışkanlıkları

- Değişkenleri çoğu zaman çift tırnak içine al: `"$file"`.
- Atamalarda boşluk kullanma: `name="value"`.
- Dosya yollarını elle birleştirmek yerine `dirname`, `basename` ve mutlak yolları kullan.
- Kritik scriptlerde `set -euo pipefail` düşün.
- Kullanıcı girdisini doğrudan SQL veya shell komutuna ekleme.
- Hataları `stderr` üzerinden raporla.
- Büyük ve kritik işlemlerde önce küçük bir dosyayla test et.
- Tekrar çalıştırılabilir scriptler yaz; Ex03'te `DROP TABLE IF EXISTS` bu amaca hizmet eder.
- Sadece çıkış koduna değil, etkilenen satır sayılarına ve tablo kayıtlarına da bak.

---

## 16. Öğrenme sırası

Bash'i öğrenirken şu sırayla küçük denemeler yapabilirsin:

1. `echo` ve yorumlar
2. Değişken tanımlama ve `"$variable"`
3. Komut satırı argümanları
4. `if` ve dosya testleri
5. `for` ile dosya listesi üzerinde gezinme
6. Komut çıktısını `$()` ile alma
7. Fonksiyonlar
8. Çıkış kodları ve `set -euo pipefail`
9. Pipe ve yönlendirmeler
10. Heredoc
11. `psql` ile SQL çalıştırma

Her konuyu küçük bir scriptle test edip sonra Ex03 scriptine bağlamak, uzun bir scripti ezberlemekten daha öğreticidir.

---

## 17. Ek sorular (detayli cevaplar)

### 1) Ondalikli sayilar: `bc`, `awk`, `BEGIN` ve Bash icinde Python kullanimi

Bash'in kendi aritmetik yapisi (`$((...))`) tam sayi odaklidir. Ondalikli islemlerde ya hata alirsin ya da beklenmeyen yuvarlama gorursun. Bu nedenle dis araclar kullanilir.

#### `bc` nedir?

- `bc` bir hesap makinesi dilidir (command-line calculator).
- Ondalikli hesap, hassasiyet (`scale`) ve kuvvet gibi islemler yapar.

Ornek:

```bash
result="$(echo 'scale=4; 10.5 / 3' | bc)"
echo "$result"   # 3.5000
```

`scale=4` ondalik basamak sayisini belirler.

#### `awk` nedir?

- `awk` metin satirlarini ve kolonlarini islemek icin yazilmis guclu bir arac/dildir.
- Sayisal islemler de yapabilir.

Ornek:

```bash
result="$(awk 'BEGIN { printf "%.2f", 10.5 / 3 }')"
echo "$result"   # 3.50
```

#### `BEGIN` nedir?

`awk` tarafinda `BEGIN` blogu, girdi satirlari okunmadan once bir kez calisir.

- Dosya okumadan sadece hesap yapmak istiyorsan idealdir.
- `printf` formatlamayi kontrol eder (`%.2f` = 2 ondalik).

#### Bash scriptinde Python nasil kullanilir?

Python'u iki sekilde cagirabilirsin.

Tek satir:

```bash
result="$(python3 -c 'print(round(10.5/3, 2))')"
echo "$result"
```

Heredoc ile:

```bash
result="$(python3 - <<'PY'
value = 10.5 / 3
print(f"{value:.4f}")
PY
)"
echo "$result"
```

Pratik secim:

- Basit matematik: `bc`
- Metin + matematik: `awk`
- Daha karmasik hesap/mantik: `python3`

### 2) `PGPASSWORD=mysecretpassword ...` satirinda gecici degisken

Evet, burada gecici ortam degiskeni `PGPASSWORD`'dur.

```bash
PGPASSWORD=mysecretpassword psql -h localhost -U acosgun -d piscineds
```

Bu ifade sadece o tek komut icin `PGPASSWORD` degeri verir.

- `PGPASSWORD` PostgreSQL istemcilerinin tanidigi ozel bir ortam degiskenidir.
- `psql`, parola sorarken bu degiskene bakabilir.

Kalici tanimlamak istersen:

```bash
export PGPASSWORD=mysecretpassword
psql -h localhost -U acosgun -d piscineds
```

Gecici kullanim genelde daha guvenlidir; shell oturumuna kalici parola birakmaz.

Not: Uretimde parola icin `.pgpass` veya secret yonetimi daha iyi yaklasimdir.

### 3) `$?` tam olarak hangi komutun sonucu?

`$?`, **hemen once calisan komutun** cikis kodudur.

Ornek:

```bash
ls /var >/dev/null
echo "$?"   # genelde 0

ls /olmayan_klasor >/dev/null 2>&1
echo "$?"   # genelde 2
```

Script icinde de ayni kural gecerli: `$?` yazdigindan hemen once ne calistiysa onun sonucu gelir.

Tum scriptin cikis kodu ise script bittikten sonra terminalde okunur:

```bash
./my_script.sh
echo "$?"   # bu kez scriptin genel cikis kodu
```

Yani baglama gore degisir:

- Scriptin icinde: son komut
- Script disinda: script komutunun kendisi

### 4) Bash array yaziminda virgul ve `[]` kullanimi

Su yazim dogrudur:

```bash
files=("oct.csv" "nov.csv" "dec.csv")
```

- Bash'te elemanlar virgul ile ayrilmaz, bosluk ile ayrilir.
- Kose parantezle liste kurma (`["a", "b"]`) Bash'te yoktur; bu Python/JSON tarzi bir gosterdir.

Eleman ekleme:

```bash
files+=("jan.csv")
```

Index ile atama:

```bash
files[0]="oct.csv"
files[1]="nov.csv"
```

Tum elemanlar:

```bash
printf '%s\n' "${files[@]}"
```

### 5) `declare -A settings` ve associative array

Evet, `-A` bu degiskenin associative array (anahtar-deger dizisi) oldugunu belirtir.

```bash
declare -A settings
settings[host]="localhost"
settings[db]="piscineds"
echo "${settings[host]}"
```

Associative array:

- Sayisal index yerine metinsel anahtar kullanir.
- C++ `std::map` mantigina benzer.
- JSON objesine de yuzeysel olarak benzer (key-value), ama JSON degildir; sadece shell degisken yapisidir.

### 6) `basename "$csv_file" .csv` uzantiyi nasil cikariyor?

`basename` bir dosya yolunun son parcasini alir.

```bash
basename "/tmp/a/b/data_2022_oct.csv"
# data_2022_oct.csv
```

Ikinci arguman (`.csv`) verilirse, sondaki bu ek varsa cikarir:

```bash
basename "/tmp/a/b/data_2022_oct.csv" .csv
# data_2022_oct
```

Dolayisiyla:

```bash
table_name="$(basename "$csv_file" .csv)"
```

dosya yolundan tablo adini turetir.

Alternatif sadece Bash ile:

```bash
file_name="${csv_file##*/}"   # yolu at, sadece dosya adi
table_name="${file_name%.csv}" # sondaki .csv'yi at
```

### 7) `fi` ne ise yarar?

Evet, Bash'e ozeldir. `if` blogunun bittigini belirtir.

```bash
if [[ "$name" == "Ayhan" ]]; then
    echo "Isim dogru"
else
    echo "Farkli isim"
fi
```

`fi`, `if`'in tersten yazimi gibi dusunulebilir ve blogu kapatir.

Benzer kapanislar:

- `do ... done` (dongu)
- `case ... esac`

### 8) `[ -e "$csv_file" ] || continue` ifadesi

Evet, `||` mantiksal OR operatorudur.

Mantik:

1. Sol taraf calisir: `[ -e "$csv_file" ]`
2. Sol taraf basarisizsa (`false`), sag taraf calisir: `continue`
3. Sol taraf basariliysa (`true`), sag taraf calismaz

Yani pratikte:

- Dosya yoksa: `continue`
- Dosya varsa: asagiya devam

Bu bir satirlik "guard" kalibidir.

### 9) `done` ne ise yarar?

`done`, `for`, `while`, `until` dongu blogunu kapatir.

```bash
for item in one two three; do
    echo "$item"
done
```

`do` ile baslayan dongu govdesi `done` ile biter. Evet, bu da Bash/shell ailesine ozgudur.

### 10) Fonksiyon icin baska format var mi?

Bash'te iki yaygin tanim vardir:

```bash
my_func() {
    echo "hello"
}
```

ve

```bash
function my_func {
    echo "hello"
}
```

Birlesik kullanim da gorulebilir:

```bash
function my_func() {
    echo "hello"
}
```

En tasinabilir ve yaygin stil `my_func() { ... }` kalibidir.

"Fonksiyon deger dondurmez" ifadesinin anlami:

- `return` sadece 0-255 araliginda cikis kodu dondurur.
- Metinsel/sayisal sonuc icin stdout kullanilir.

Ornek:

```bash
sum() {
    local a="$1" b="$2"
    echo $((a + b))
}

result="$(sum 3 5)"
echo "$result"   # 8
```

### 11) `set -euo pipefail` disinda hata yakalama var mi?

Var. Bunlar en yaygin temel set ama tek yol degil.

Yontemler:

- Acik kontrol: `if ! command; then ... fi`
- Kisa devre: `command || { echo "hata"; exit 1; }`
- `trap '...' ERR` ile hata aninda yakalama
- `set -E` ile fonksiyon/subshell'lerde `ERR` davranisini genisletme
- `psql -v ON_ERROR_STOP=1` gibi arac-ozel bayraklar

Sifira bolme ornegi:

```bash
echo $((1/0))
```

Bu komut Bash'te "division by 0" hatasi verir ve komut basarisiz olur.

- `set -e` aciksa script genelde burada durur.
- `set -e` kapaliysa script devam edebilir.

Ama her hata turu aritmetik degil. Ornegin pipe, alt komutlar, kosul bloglari gibi durumlarda ek kontrol yazmak gerekir. Bu nedenle uretim scriptlerinde sadece `set` bayraklarina guvenmek yerine acik hata mesaji ve `exit` kullanmak daha saglamdir.

### 12) `trap ... EXIT` Python `finally` gibi mi?

Cok benzer bir amaca hizmet eder: script nasil biterse bitsin (normal bitis, `exit`, bircok hata durumu) temizlik kodunu calistirirsin.

```bash
cleanup() {
    echo "Temizlik yapiliyor"
}

trap cleanup EXIT
```

Benzerlik:

- Python `finally`: bloktan cikarken garanti calisir
- Bash `trap ... EXIT`: shell prosesi cikarken garanti calistirmayi hedefler

Fark:

- `finally` dilin kontrol yapisinin parcasi
- `trap` sinyal/olay tabanli shell mekanizmasi

Ek olarak `INT`, `TERM` gibi sinyaller icin de trap koyabilirsin:

```bash
trap cleanup EXIT INT TERM
```

Bu sayede Ctrl+C gibi kesmelerde de temizlik yapabilirsin.

---

### 13) `shopt`, `-s`, `-u` ve `nullglob` Nedir?

`shopt` ("Shell Options"), Bash kabugunun yerlesik ozelliklerini ve dosya arama/eslestirme (globbing) davranislarini yoneten dahili bir komuttur.

#### Parametrelerin Anlami:
- **`-s` (Set):** Belirtilen kabuk secenegini **aktif eder (acar)**.
- **`-u` (Unset):** Belirtilen kabuk secenegini **deaktif eder (kapatir)**.
- **`shopt <secenek>`:** Secenegin o an acik (`on`) mi kapali (`off`) mi oldugunu gosterir.
- **`shopt -p`:** Tum acik/kapali kabuk ayarlarini listeler.

---

#### `nullglob` Nedir ve Neden Kullanilir?

Varsayilan Bash davranisinda, bir dosya deseni (ornek: `*.csv`) hicbir dosya ile eslesmezse, Bash bu deseni **oldugu gibi duz metin** olarak birakir.

##### 1. Varsayilan Durum (`nullglob` kapali):
Klasorde hic CSV yoksa:
```bash
for file in /bos_klasor/*.csv; do
    echo "$file"
done
```
**Cikti:** `/bos_klasor/*.csv` (Boyle bir dosya olmamasina ragmen dongu 1 kez doner ve duz metin basar!).

##### 2. `nullglob` Acikken (`shopt -s nullglob`):
Eger eslesen hicbir dosya yoksa, Bash o deseni **tamamen bosluga (hicbir seye / null)** donusturur:
```bash
shopt -s nullglob
files=(/bos_klasor/*.csv)
shopt -u nullglob

echo "Bulunan dosya sayisi: ${#files[@]}"  # 0 basar!
```

> [!TIP]
> **Neden `shopt -u nullglob` ile kapatiriz?**
> Scriptin sadece dosya arama kisminda bu davranisi kullanip, sonrasinda Bash'i standart haline geri dondurmek (yan etkileri onlemek) en iyi muhendislik pratigidir.

---

#### Diger Cok Kullanisli `shopt` Secenekleri

| Secenek | Komut | Ne Ise Yarar? | Ornek |
| :--- | :--- | :--- | :--- |
| **`globstar`** | `shopt -s globstar` | `**` ile tum alt klasorleri ozyinelemeli (recursive) arar. | `ls **/*.sql` (Tum alt klasorlerdeki SQL'leri bulur) |
| **`nocaseglob`** | `shopt -s nocaseglob` | Dosya ararken buyuk/kucuk harf duyarsizligini acar. | `*.csv` hem `a.csv` hem `B.CSV` ile eslesir |
| **`dotglob`** | `shopt -s dotglob` | `*` deseninin gizli dosyalari (`.gitignore`, `.env`) da bulmasini saglar. | `rm *` (Gizli dosyalar dahil siler) |
| **`extglob`** | `shopt -s extglob` | Gelismis regex benzeri desen eslestirmeyi acar. | `rm !(*.csv)` (CSV haric her seyi sil) |
| **`failglob`** | `shopt -s failglob` | Eslesmeyen desen olursa komutu calistirmayip hata firlatir. | `ls *.xyz` -> `no match found` hatasi verir |

---

### 14) Bash'te Array (Dizi) Yapisi, Gezinme ve Ozel Isaretler

Bash'te diziler (arrays), birden fazla degeri tek bir degiskende saklamanin en guvenli yoludur.

#### 1. Dizi Tanimlama Yontemleri

```bash
# 1. Dogrudan elemanlarla tanimlama
meyveler=("elma" "armut" "muz")

# 2. Bos dizi olusturma
dosyalar=()

# 3. Dosyalari diziye toplama (nullglob ile)
shopt -s nullglob
csv_dosyalari=("$CUSTOMER_DIR"/*.csv)
shopt -u nullglob

# 4. Var olan diziye yeni eleman ekleme (+=)
meyveler+=("cilek" "karpuz")

# 5. Belirli bir indekse eleman atama
meyveler[10]="portakal"
```

---

#### 2. Elemanlara Erisme ve Ozel Isaretlerin Anlami

Bash'te dizilerle calisirken kullanilan sembollerin gorevleri:

| Isaret / Kalip | Anlami / Gorevi | Ornek | Aciklama |
| :--- | :--- | :--- | :--- |
| **`${dizi[i]}`** | Belirli bir indisteki eleman | `${meyveler[0]}` | Ilk elemani (`elma`) getirir. |
| **`${dizi[-1]}`** | Dizinin son elemani | `${meyveler[-1]}` | En sondaki elemani getirir. |
| **`${dizi[@]}`** | Dizideki **tum elemanlar** (Ayrilmis) | `"${meyveler[@]}"` | Her elemani tirnak icinde ayri kelime olarak korur (En guvenli yol). |
| **`${dizi[*]}`** | Dizideki tum elemanlar (Birlestirilmis) | `"${meyveler[*]}"` | Tum elemanlari tek bir metin dizesi (`"elma armut muz"`) yapar. |
| **`#` (Sayi/Uzunluk)** | **Eleman Sayisi** veya **Karakter Uzunlugu** | `${#meyveler[@]}` | Dizinin **toplam eleman sayisini** verir (Orn: `3`). |
| **`${#degisken}`** | Metin Karakter Sayisi | `${#meyveler[0]}` | `elma` kelimesinin uzunlugunu (`4`) verir. |
| **`$#`** | Girdi Parametre Sayisi | `$#` | Script'e gelen arguman sayisini verir. |
| **`!` (Indeksler)** | Dizinin **indeks numaralarini** listeler | `${!meyveler[@]}` | `0 1 2` seklinde mevcut indisleri doner. |

---

#### 3. Dizi Icinde Gezinme (Donguler)

##### Yontem A: Elemanlar Uzerinde Donme (En Yaygin)
```bash
for meyve in "${meyveler[@]}"; do
    echo "Meyve: $meyve"
done
```

##### Yontem B: Indeksler Uzerinde Donme (`!` ile)
Elemanin kacinci sirada oldugunu bilmek istediginizde:
```bash
for i in "${!meyveler[@]}"; do
    echo "Sira $i -> ${meyveler[$i]}"
done
```

##### Yontem C: C-Tipi Klasik Sayacli Dongu
```bash
for ((i=0; i<${#meyveler[@]}; i++)); do
    echo "Indeks $i: ${meyveler[$i]}"
done
```

---

#### 4. Dizi Dilimleme (Slicing) ve Eleman Silme

```bash
sayilar=(0 1 2 3 4 5 6 7 8 9)

# 2. indeksten basla, 3 eleman al (2 3 4):
echo "${sayilar[@]:2:3}"

# 1. indisteki elemani sil (Dizinin boyutu kuculur ama indeksler kaymaz):
unset sayilar[1]
```

---

#### 5. Iliskili Diziler (Associative Arrays / Key-Value Sozluk)

Python'daki `dict` yapisi gibi anahtar-deger cifti saklamak icin `declare -A` kullanilir:

```bash
# Iliskili dizi tanimla:
declare -A db_config

db_config["host"]="localhost"
db_config["port"]="5432"
db_config["user"]="acosgun"

# Degere erisme:
echo "Baglanti adresi: ${db_config["host"]}:${db_config["port"]}"

# Tum anahtarlari (keys) listeleme (! ile):
for key in "${!db_config[@]}"; do
    echo "$key = ${db_config[$key]}"
done
```

