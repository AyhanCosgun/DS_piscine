#!/usr/bin/env bash


# $0: Scriptin adı
# $1, $2: Birinci ve ikinci komut satırı argümanı
# $#: Argüman sayısı
# "$@": Tüm argümanlar, ayrı ayrı korunarak
# $?: Son komutun çıkış kodu
# $$: Çalışan Bash process'inin ID'si
# ${BASH_SOURCE[0]}: İçinde bulunulan Bash dosyasının yolu

# echo "Script: $0"
# echo "Argüman sayısı: $#"
# echo "İlk argüman: ${1:-verilmedi}"
# echo "İkinci argüman: ${2:-verilmedi}"
# echo "Tüm argümanlar: $@"
# echo "Son komutun çıkış kodu: $?"
# echo "Çalışan Bash process'inin ID'si: $$"
# echo "İçinde bulunulan Bash dosyasının yolu: ${BASH_SOURCE[0]}"

# name="Ayhan"
# echo 'Merhaba $name'   # Kelimesi kelimesine yazdırır
# echo "Merhaba $name"   # Ayhan değerini kullanır


# # Bash'in yerleşik aritmetik desteği esas olarak tam sayılar içindir.
# first=10
# second=3
# result=$((first + second))
# echo "$result"

# files=("oct.csv" "nov.csv" "dec.csv")
# echo "${files[0]}"

# for file in "${files[@]}"; do
#     echo "$file"
# done

# declare -A settings
# settings[host]="localhost"
# settings[database]="piscineds"
# echo "${settings[database]}"

# for csv_file in ../subject/customer/*.csv; do
#     echo "$csv_file"
# done
# pwd
 SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
# echo "BASH_SOURCE[0]: ${BASH_SOURCE[0]}"
# dirname -- "${BASH_SOURCE[0]}"
# echo "Script directory: $(dirname -- "${BASH_SOURCE[0]}")"
# echo "Script directory (absolute path): $SCRIPT_DIR"
# cd -- "$(dirname -- "${BASH_SOURCE[0]}")"
# pwd

#### set -euo pipefail kullanımı

# set -e  #errexit bayrağı: herhangi bir komut başarısız olursa, script hemen durur.
# echo "1"
# false
# echo "2"

#set -u  #nounset bayrağı: tanımsız değişkenlere erişmeye çalışıldığında hata verir.
#echo "$NAME"

#set -o pipefail  #pipefail bayrağı: bir pipeline'daki herhangi bir komut başarısız olursa, pipeline'ın tamamı başarısız sayılır.

# set -e
# set -o pipefail

# false | echo "Merhaba"

# echo "Script devam etti"

##VEYA

#set -eo pipefail
# cat $SCRIPT_DIR/ornek.txt | grep "Ayhan" | sort
# echo $?


# | Kısa | Uzun         |
# | ---- | ------------ |
# | `-e` | `-o errexit` |
# | `-u` | `-o nounset` |
# | `-f` | `-o noglob`  |
# | `-x` | `-o xtrace`  |


# shopt -s nullglob

# for csv_file in $SCRIPT_DIR/*.csv; do
#     echo "csv_file = $csv_file"

#     if [ -e "$csv_file" ]; then
#         echo "Dosya gerçekten var."
#     else
#         echo "Bu gerçek bir dosya değil."
#     fi
# done


   ### dirname ve basename kullanımı
# SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
# echo "Script directory: $SCRIPT_DIR"
# echo "dirname of script directory: $(dirname $SCRIPT_DIR)"
# echo "basename of script directory: $(basename $SCRIPT_DIR)"

   ### -v ile değişkenleri psql'e aktarma nın önemi

# isim="O'Reilly"

# psql -h localhost -U postgres -p 5432  -d postgres\
#     -v isim="$isim" \
# <<SQL
# INSERT INTO author (name)
# VALUES (:'isim');
# SQL

# isim="O'Reilly2"

# psql -h localhost -U postgres -p 5432  -d postgres\
# <<SQL
# INSERT INTO author (name)
# VALUES ($isim);
# SQL

      ###### nullglob kullanımı ######
shopt -s nullglob
for file in /bos_klasor/*.csv; do
    echo "$file"
done

files=(/bos_klasor/*.csv)

echo "Bulunan dosya sayisi: ${#files[@]}"
echo "Bulunan dosyalar: ${files[@]}"

shopt -u nullglob