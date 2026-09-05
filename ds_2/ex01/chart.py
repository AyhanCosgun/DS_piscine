import string

from sqlalchemy import create_engine
import pandas as pd
import matplotlib.pyplot as plt

engine = create_engine("postgresql+psycopg2://acosgun:mysecretpassword@localhost:5432/piscineds")

query = """
    WITH monthly_sales AS (
        SELECT
            DATE_TRUNC('month', event_time) AS month_date,
            SUM(price) AS total_sales
        FROM customers
        WHERE event_type = 'purchase'
        GROUP BY DATE_TRUNC('month', event_time)
    )
    SELECT
        TO_CHAR(month_date, 'Mon') AS month,
        total_sales
    FROM monthly_sales
    ORDER BY month_date;
"""

try:
    with engine.connect() as connection:
        df = pd.read_sql(query, connection)

    print("DataFrame created successfully.")

    event_types = df["event_type"].tosequence(string.ascii_letters)
    counts = df["event_count"]

    print("Event counts:")
    print(counts)
    print("Event types:")
    print(event_types)

    plt.figure(figsize=(7, 7))
    plt.pie(
        counts,
        labels=event_types,
        autopct="%1.1f%%"
    )
    plt.title("Site Event Distribution")
    plt.show()

except Exception as e:
    print(f"An error occurred connecting to the database: {e}")
