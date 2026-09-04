\echo '================================================================================'
\echo 'Processing: create_duplicates.sql'
\echo '================================================================================'

\set ON_ERROR_STOP on

BEGIN;

    DROP TABLE IF EXISTS duplicate_groups;

    CREATE TABLE duplicate_groups AS
    WITH ranked_events AS (
        SELECT *,
            LAG(event_time) OVER (
                PARTITION BY user_id, user_session, event_type, product_id, price
                ORDER BY event_time
            ) AS prev_event_time,
            LEAD(event_time) OVER (
                PARTITION BY user_id, user_session, event_type, product_id, price
                ORDER BY event_time
            ) AS next_event_time
        FROM customers
    )
    SELECT
        event_time,
        event_type,
        product_id,
        price,
        user_id,
        user_session,
        prev_event_time,
        next_event_time
    FROM ranked_events
    WHERE
        event_time - prev_event_time <= INTERVAL '1 second'
        OR
        next_event_time - event_time <= INTERVAL '1 second';

    DO $$
    DECLARE
        duplicate_count BIGINT;
    BEGIN
        SELECT COUNT(*) INTO duplicate_count FROM duplicate_groups;
        RAISE NOTICE 'Duplicate records found: %', duplicate_count;

    END $$;

\echo '================================================================================'
\echo 'Creating duplicates table completed successfully.'
\echo '================================================================================'

COMMIT;