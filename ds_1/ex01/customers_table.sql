\echo '================================================================================'
\echo 'Processing: customers_old_table.sql'
\echo '================================================================================'

\set ON_ERROR_STOP on

BEGIN;

DROP TABLE IF EXISTS customers_old;

DO $$
DECLARE
    v_merge_sql_command TEXT;
    v_control_sql_command TEXT;
    v_table_count INT;
    v_expected_total BIGINT;
    v_observed_total BIGINT;
BEGIN

    SELECT count(*), 
           'CREATE TABLE customers_old AS ' || 
           string_agg('SELECT * FROM ' || quote_ident(tablename), ' UNION ALL ' ORDER BY tablename),
           'SELECT ' ||
           string_agg('(SELECT count(*) FROM ' || quote_ident(tablename) || ')', ' + ')
    INTO v_table_count, v_merge_sql_command, v_control_sql_command
    FROM pg_tables
    WHERE schemaname = 'public'
      AND tablename ~ '^data_202[0-9]_[a-z]{3}$';

    IF v_table_count = 0 OR v_merge_sql_command IS NULL THEN
        RAISE EXCEPTION 'ERROR: could not found any matching tables with the specified pattern "data_202*_***"!';
    END IF;

    RAISE NOTICE '% tables found. Starting the merge process...', v_table_count;

    EXECUTE v_merge_sql_command;

    RAISE NOTICE '% tables merged into the "customers_old" table successfully.', v_table_count;

  
    RAISE NOTICE 'Calculating expected total record count from source tables...';

    EXECUTE v_control_sql_command INTO v_expected_total;

    RAISE NOTICE 'Calculating observed total record count in the "customers_old" table...';

    SELECT count(*)
    INTO v_observed_total 
    FROM customers_old;

    RAISE NOTICE 'Expected total: %, Observed total: %',
      v_expected_total,
      v_observed_total;

    IF v_expected_total <> v_observed_total THEN
      RAISE EXCEPTION
        'Record count mismatch! Expected: %, Observed: % . Aborting the process.',
        v_expected_total,
        v_observed_total;
    END IF;

    RAISE NOTICE 'Record count verification successful.';
  END $$;

  \echo 'Transaction is being committed...'

COMMIT;