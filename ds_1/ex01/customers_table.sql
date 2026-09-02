\echo '================================================================================'
\echo 'Processing: customers_table.sql (Dynamic Metadata Approach)'
\echo '================================================================================'

\set ON_ERROR_STOP on

BEGIN;

DROP TABLE IF EXISTS customers;

DO $$
DECLARE
    v_sql TEXT;
    v_table_count INT;
BEGIN
    -- 1. Kriterlere uyan kaç tablo olduğunu say ve dinamik sorguyu oluştur
    SELECT count(*), 
           'CREATE TABLE customers AS ' || 
           string_agg('SELECT * FROM ' || quote_ident(tablename), ' UNION ALL ' ORDER BY tablename)
    INTO v_table_count, v_sql
    FROM pg_tables
    WHERE schemaname = 'public'
      AND tablename ~ '^data_202[0-9]_[a-z]{3}$';

    -- 2. Tablo varlık kontrolü (Tablo yoksa hata fırlat ki ON_ERROR_STOP devreye girsin)
    IF v_table_count = 0 OR v_sql IS NULL THEN
        RAISE EXCEPTION 'HATA: "data_202*_***" desenine uyan hiçbir tablo bulunamadı!';
    END IF;

    RAISE NOTICE 'Toplam % adet tablo bulundu. Birleştirme işlemi başlatılıyor...', v_table_count;

    -- 3. Dinamik sorguyu tek seferde yürüt
    EXECUTE v_sql;

    RAISE NOTICE 'customers tablosu başarıyla oluşturuldu.';
END $$;

\echo '================================================================================'
COMMIT;