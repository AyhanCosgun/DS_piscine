\echo '================================================================================'
\echo 'Processing: fusion.sql'
\echo '================================================================================'

\set ON_ERROR_STOP on

BEGIN;

    DROP TABLE IF EXISTS customers_fusion;

    CREATE TABLE customers_fusion AS
        WITH unique_items AS (
            SELECT DISTINCT ON (product_id)
                product_id,
                category_id,
                category_code,
                brand
            FROM items
            ORDER BY product_id,
                (category_code IS NOT NULL AND category_code <> '') DESC,
                (brand IS NOT NULL AND brand <> '') DESC,
                category_id DESC NULLS LAST
        )
        SELECT
            c.*,
            u.category_id,
            u.category_code,
            u.brand
        FROM customers c
        LEFT JOIN unique_items u
        ON c.product_id = u.product_id;

    DO $$
    DECLARE
        customers_count BIGINT;
        fusion_count BIGINT;

    BEGIN
        SELECT COUNT(*) INTO customers_count FROM customers;
        SELECT COUNT(*) INTO fusion_count FROM customers_fusion;

        RAISE NOTICE 'Original customer table rows: %', customers_count;
        RAISE NOTICE 'Fusion table rows: %', fusion_count;
        IF customers_count <> fusion_count THEN
            RAISE EXCEPTION 'row count mismatch, aborting !';
        END IF;

    END $$;

    DROP TABLE customers;

    ALTER TABLE customers_fusion RENAME TO customers;

    \echo '================================================================================'
    \echo 'Combining "customers" with "items" is completed successfully.'
    \echo '================================================================================'

COMMIT;