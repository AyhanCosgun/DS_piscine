#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd -- "$SCRIPT_DIR/.." && pwd)"
CUSTOMER_DIR="$PROJECT_DIR/subject/customer"

DB_HOST="localhost"
DB_PORT="5432"
DB_USER="acosgun"
DB_NAME="piscineds"

{
	for csv_file in "$CUSTOMER_DIR"/*.csv; do
		[ -e "$csv_file" ] || continue
			table_name=$(basename "$csv_file" .csv)
			file_name=$(basename "$csv_file")

			echo "creating SQL code for $table_name" >&2

			cat <<SQL
\echo '================================================================================'
\echo 'Processing: $file_name'

DROP TABLE IF EXISTS $table_name;

CREATE TABLE $table_name (
	event_time TIMESTAMPTZ,
	event_type VARCHAR(32),
	product_id INTEGER,
	price NUMERIC(10, 2),
	user_id BIGINT,
	user_session UUID
);

\echo 'Loading data in $file_name'
\copy $table_name FROM $csv_file WITH (FORMAT csv, HEADER true)
\echo 'Data loaded successfully into $table_name'
\echo '================================================================================'
SQL

	done

} | psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" -v ON_ERROR_STOP=1