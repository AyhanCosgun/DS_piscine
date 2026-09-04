#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd -- "$SCRIPT_DIR/.." && pwd)"
CUSTOMER_DIR="$PROJECT_DIR/subject/customer"

DB_HOST="localhost"
DB_PORT="5432"
DB_USER="acosgun"
DB_NAME="piscineds"

if [ ! -d "$CUSTOMER_DIR" ]; then
	echo "Customer directory not found in path: $CUSTOMER_DIR" >&2
	echo "Exiting the script." >&2
	exit 1
fi

shopt -s nullglob
csv_files=("$CUSTOMER_DIR"/*.csv)
if [ ${#csv_files[@]} -eq 0 ]; then
	echo "No CSV files found in $CUSTOMER_DIR" >&2
	echo "Exiting the script." >&2
	exit 1
fi
shopt -u nullglob

echo "Found ${#csv_files[@]} CSV files in $CUSTOMER_DIR" >&2
echo "Connecting to database..." >&2


for csv_file in "${csv_files[@]}"; do
    echo "creating SQL code for '$csv_file'" >&2
done