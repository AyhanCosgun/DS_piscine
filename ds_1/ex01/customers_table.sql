\echo '================================================================================'
\echo 'Processing: customers_table.sql'
\echo '================================================================================'

\set ON_ERROR_STOP on

BEGIN;

DROP TABLE IF EXISTS customers;

DO $$
DECLARE
    v_sql TEXT;
    v_table_count INT;
BEGIN

    SELECT count(*), 
           'CREATE TABLE customers AS ' || 
           string_agg('SELECT * FROM ' || quote_ident(tablename), ' UNION ALL ' ORDER BY tablename)
    INTO v_table_count, v_sql
    FROM pg_tables
    WHERE schemaname = 'public'
      AND tablename ~ '^data_202[0-9]_[a-z]{3}$';

    IF v_table_count = 0 OR v_sql IS NULL THEN
        RAISE EXCEPTION 'ERROR: could not found any matching tables with the specified pattern "data_202*_***"!';
    END IF;

    RAISE NOTICE '% tables found. Starting the merge process...', v_table_count;

    EXECUTE v_sql;

    RAISE NOTICE '% tables merged into the "customers" table successfully.', v_table_count;
END $$;



\echo '================================================================================'
\echo 'Verifying expected and observed record counts...'
\echo '================================================================================'

DO $$
DECLARE
  v_expected_total BIGINT;
  v_observed_total BIGINT;
BEGIN
  RAISE NOTICE 'Calculating expected total record count from source tables...';

  SELECT
    (SELECT count(*) FROM data_2022_oct) +
    (SELECT count(*) FROM data_2022_nov) +
    (SELECT count(*) FROM data_2022_dec) +
    (SELECT count(*) FROM data_2023_jan)
  INTO v_expected_total;

  RAISE NOTICE 'Calculating observed total record count in the "customers" table...';

  SELECT count(*)
  INTO v_observed_total 
  FROM customers;

  RAISE NOTICE 'Expected total: %, Observed total: %',
    v_expected_total,
    v_observed_total;

  IF v_expected_total <> v_observed_total THEN
    RAISE EXCEPTION
      'Record count mismatch! Expected: %, Observed: % \n Rolling back the transaction, deleting the "customers" table, and aborting the process.',
      v_expected_total,
      v_observed_total;
  END IF;

  RAISE NOTICE 'Record count verification successful. The "customers" table contains the expected number of records.';
END $$;

\echo 'Transaction is being committed...'

COMMIT;