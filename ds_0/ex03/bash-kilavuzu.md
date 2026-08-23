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
