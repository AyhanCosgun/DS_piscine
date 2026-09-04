\echo '================================================================================'
\echo 'Processing: remove_duplicates_from_duplicates_group.sql'
\echo '================================================================================'

\set ON_ERROR_STOP on

BEGIN;

    DROP TABLE IF EXISTS duplicates_clean;

    CREATE TABLE duplicates_clean AS
        WITH ranked_events AS (
            SELECT 
                event_time,
                event_type,
                product_id,
                price,
                user_id,
                user_session,
                LAG(event_time) OVER (
                    PARTITION BY user_id, user_session, event_type, product_id, price
                    ORDER BY event_time
                ) AS prev_event_time
            FROM duplicate_groups
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
        SELECT COUNT(*) INTO original_count FROM duplicate_groups;
        SELECT COUNT(*) INTO cleaned_count FROM duplicates_clean;
        duplicate_count := original_count - cleaned_count;

        RAISE NOTICE 'Original record count: %', original_count;
        RAISE NOTICE 'Cleaned record count: %', cleaned_count;
        RAISE NOTICE 'Duplicate records removed: %', duplicate_count;

    END $$;

\echo '================================================================================'
\echo 'Removing duplicates from duplicates group completed successfully.'
\echo '================================================================================'

COMMIT;