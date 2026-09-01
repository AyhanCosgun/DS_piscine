\echo '================================================================================'
\echo 'Processing: items_table.sql'

\set ON_ERROR_STOP on

BEGIN;

DROP TABLE IF EXISTS items;

CREATE TABLE items (
    product_id INTEGER,
    category_id BIGINT,
    category_code VARCHAR(255),
    brand TEXT
);

\echo 'Loading data in item.csv'
\copy items FROM '../subject/item/item.csv' WITH (FORMAT csv, HEADER true);

\echo 'Data loaded successfully into items table.'
\echo '================================================================================'
COMMIT;