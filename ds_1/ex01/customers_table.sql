\echo '================================================================================'
\echo 'Processing: customers_table.sql'

\set ON_ERROR_STOP on

BEGIN;

DROP TABLE IF EXISTS customers;

CREATE TABLE customers AS
SELECT * FROM data_2022_oct
UNION ALL
SELECT * FROM data_2022_nov
UNION ALL
SELECT * FROM data_2022_dec
UNION ALL
SELECT * FROM data_2023_jan;

\echo 'Customers table created successfully.'
\echo '================================================================================'
COMMIT;