DROP TABLE IF EXISTS items;

CREATE TABLE items (
    product_id INTEGER,
    category_id BIGINT,
    category_code VARCHAR(255),
    brand TEXT
);

\copy items FROM '../subject/item/items.csv' WITH (FORMAT csv, HEADER true);