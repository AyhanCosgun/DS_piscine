import matplotlib.pyplot as plt
import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("postgresql+psycopg2://acosgun:mysecretpassword@localhost:5432/piscineds")

query_daily = """
    SELECT
        DATE_TRUNC('day', event_time) AS day_date,
        COUNT(DISTINCT user_id) AS customer_count,
        (SUM(price) / COUNT(DISTINCT user_id)) AS avg_spend_per_customer
    FROM customers
    WHERE event_type = 'purchase'
    AND event_time >= '2022-10-01' AND event_time < '2023-03-01'
    GROUP BY day_date
    ORDER BY day_date;
    """
query_monthly = """
    SELECT 
        TO_CHAR(DATE_TRUNC('month', event_time), 'mon') as month,
        SUM(price) / 1000000 as total_sales_mil
    FROM customers
    WHERE event_type = 'purchase'
    AND event_time >= '2022-10-01' AND event_time < '2023-03-01'
    GROUP BY DATE_TRUNC('month', event_time)
    ORDER BY DATE_TRUNC('month', event_time);
    """
try:
    with engine.connect() as connection:
        df_daily = pd.read_sql(query_daily, connection)
        df_monthly = pd.read_sql(query_monthly, connection)

    print("DataFrames created successfully.")

    print(df_daily.head())
    print(df_monthly.head())

    fig1 = plt.figure(figsize=(10, 8))
    plt.plot(df_daily["day_date"], df_daily["customer_count"])
    plt.ylabel("Number of customers", fontsize=14)
    plt.grid()

    plt.tight_layout()
    plt.show()
except Exception as e:
    print(f"An error occurred connecting to the database: {e}")