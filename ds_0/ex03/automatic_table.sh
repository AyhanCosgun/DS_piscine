#!/usr/bin/env bash

set -euo pipefail

# SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
# PROJECT_DIR="$(cd -- "$SCRIPT_DIR/.." && pwd)"
CUSTOMER_DIR="/home/acosgun/sgoinfre/subject/customer"

 for csv_file in "$CUSTOMER_DIR"/*.csv; do
	if [[ -f "$csv_file" ]]; then
		echo "Found CSV file: $csv_file"
		
	else
		echo "No CSV files found in $CUSTOMER_DIR"
		continue
	fi

done