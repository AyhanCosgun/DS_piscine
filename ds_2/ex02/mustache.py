import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from pathlib import Path

output_dir = Path(__file__).resolve().parent

engine: Engine = create_engine(
    "postgresql+psycopg2://acosgun:mysecretpassword@localhost:5432/piscineds")

query_prices = """
    SELECT price
    FROM customers
    WHERE event_type = 'purchase'
    AND event_time >= TIMESTAMPTZ '2022-10-01 00:00:00+00'
    AND event_time <  TIMESTAMPTZ '2023-03-01 00:00:00+00'
    """
query_av_basket = """
    SELECT user_id, AVG(session_total) AS avg_basket
    FROM (
        SELECT user_id, user_session, SUM(price) AS session_total
        FROM customers
        WHERE event_type = 'purchase'
        AND event_time >= TIMESTAMPTZ '2022-10-01 00:00:00+00'
        AND event_time <  TIMESTAMPTZ '2023-03-01 00:00:00+00'
        GROUP BY user_id, user_session
    ) AS session_totals
    GROUP BY user_id;
        """
query_daily_av_spend = """
    SELECT
        DATE_TRUNC('day', event_time) AS day_date,
        (SUM(price) / COUNT(DISTINCT user_id)) AS avg_spend_per_customer
    FROM customers
    WHERE event_type = 'purchase'
    AND event_time >= TIMESTAMPTZ '2022-10-01 00:00:00+00'
    AND event_time <  TIMESTAMPTZ '2023-03-01 00:00:00+00'
    GROUP BY day_date
    ORDER BY day_date;
    """

try:
    with engine.connect() as connection:
        df_prices = pd.read_sql(query_prices, connection)
        df_basket = pd.read_sql(query_av_basket, connection)
        df_daily_av_spend = pd.read_sql(query_daily_av_spend, connection)

    print("DataFrames created successfully.")

    print(df_prices.describe().to_string(float_format="{:.6f}".format))

except Exception as e:
    print(f"An error occurred connecting to the database: {e}")
    exit(1)

sns.set_theme()

# First chart: Raw Product Prices (All Outliers / Fliers Included)
plt.figure(figsize=(10, 8))
plt.title("Raw Product Prices", fontsize=18)
sns.boxplot(x=df_prices["price"], color="#68B478", fliersize=10,
            linewidth=3,
            flierprops={"marker": "d",
                        "markerfacecolor": "#4c4c4c",
                        "markeredgecolor": "#4c4c4c"})
plt.xlabel("price", fontsize=20)
plt.xticks(fontsize=20)
plt.tight_layout()
plt.show()

# Second chart: Adjusted Product Prices (Outliers Hidden)
plt.figure(figsize=(10, 8))
plt.title("Adjusted Product Prices", fontsize=18)
sns.boxplot(x=df_prices["price"], color="#68B478", showfliers=False,
            linewidth=3)
plt.xlabel("price", fontsize=20)
plt.xticks(fontsize=20)
plt.tight_layout()
plt.show()

# Third chart: Average Basket Price per User
plt.figure(figsize=(10, 8))
plt.title("Average Basket Price per User (Outliers / Fliers Hidden)",
          fontsize=18)
sns.boxplot(x=df_basket["avg_basket"], color="#64A0C8", showfliers=False,
            linewidth=3)
plt.xlabel("")
plt.xticks(fontsize=20)
plt.tight_layout()
plt.show()

# Fourth chart: Average Basket Price per User (Outliers / Fliers Included)
plt.figure(figsize=(10, 8))
plt.title("Average Basket Price per User (Outliers / Fliers Included)",
          fontsize=18)
sns.boxplot(x=df_basket["avg_basket"], color="#64A0C8", fliersize=10,
            linewidth=3,
            flierprops={"marker": "d",
                        "markerfacecolor": "#4c4c4c",
                        "markeredgecolor": "#4c4c4c"})
plt.xlabel("")
plt.xticks(fontsize=20)
plt.tight_layout()
plt.show()

# Given Subject Box plot : Misunderstanding of "average basket price per user"
# Fifth chart: Daily Average Spend per Customer (Outliers / Fliers Included)
plt.figure(figsize=(10, 8))
plt.title("Daily Average Spend per Customer (Outliers / Fliers Included)",
          fontsize=18)
sns.boxplot(x=df_daily_av_spend["avg_spend_per_customer"], color="#64A0C8",
            fliersize=10,
            linewidth=3,
            flierprops={"marker": "d",
                        "markerfacecolor": "#4c4c4c",
                        "markeredgecolor": "#4c4c4c"})
plt.xlabel("")
plt.xticks(fontsize=20)
plt.tight_layout()
plt.show()
