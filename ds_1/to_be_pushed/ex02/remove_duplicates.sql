\echo '================================================================================'
\echo 'Processing: remove_duplicates.sql'
\echo '================================================================================'

\set ON_ERROR_STOP on

BEGIN;

    DROP TABLE IF EXISTS customers_clean;

    CREATE TABLE customers_clean AS
        WITH ranked_events AS (
            SELECT *,
                LAG(event_time) OVER (
                    PARTITION BY user_id, user_session, event_type, product_id, price
                    ORDER BY event_time
                ) AS prev_event_time
            FROM customers
        )
        SELECT
            event_time,
            event_type,
            product_id,
            price,
            user_id,
            user_session
        FROM ranked_events
        WHERE prev_event_time IS NULL
        OR event_time - prev_event_time > INTERVAL '1 second';

    DO $$
    DECLARE
        original_count BIGINT;
        cleaned_count BIGINT;
        duplicate_count BIGINT;
    BEGIN
        SELECT COUNT(*) INTO original_count FROM customers;
        SELECT COUNT(*) INTO cleaned_count FROM customers_clean;
        duplicate_count := original_count - cleaned_count;

        RAISE NOTICE 'Original record count: %', original_count;
        RAISE NOTICE 'Cleaned record count: %', cleaned_count;
        RAISE NOTICE 'Duplicate records removed: %', duplicate_count;

    END $$;

    DROP TABLE customers;

    ALTER TABLE customers_clean RENAME TO customers;

\echo '================================================================================'
\echo 'Removing duplicates completed successfully.'
\echo '================================================================================'

COMMIT;