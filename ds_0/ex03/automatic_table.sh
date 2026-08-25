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
pwd
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
echo "BASH_SOURCE[0]: ${BASH_SOURCE[0]}"
dirname -- "${BASH_SOURCE[0]}"
echo "Script directory: $(dirname -- "${BASH_SOURCE[0]}")"
echo "Script directory (absolute path): $SCRIPT_DIR"
cd -- "$(dirname -- "${BASH_SOURCE[0]}")"
pwd