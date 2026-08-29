\echo '================================================================================'
\echo 'Processing: table.sql'

DROP TABLE IF EXISTS data_2022_oct;

CREATE TABLE data_2022_oct (
    event_time TIMESTAMPTZ,
    event_type VARCHAR(32),
    product_id INTEGER,
    price NUMERIC(10, 2),
    user_id BIGINT,
    user_session UUID
);

\echo 'Loading data in data_2022_oct.csv'
\copy data_2022_oct FROM '../subject/customer/data_2022_oct.csv' WITH (FORMAT csv, HEADER true);
\echo 'Data loaded successfully into data_2022_oct table.'
\echo '================================================================================'