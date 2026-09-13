import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

engine: Engine = create_engine(
    "postgresql+psycopg2://acosgun:mysecretpassword@localhost:5432/piscineds")

query_prices = """
    SELECT price 
    FROM customers 
    WHERE event_type = 'purchase';
    """
query_av_basket = """
    SELECT user_id, AVG(session_total) AS avg_basket
    FROM (
        SELECT user_id, user_session, SUM(price) AS session_total
        FROM customers
        WHERE event_type = 'purchase'
        GROUP BY user_id, user_session
    ) AS session_totals
    GROUP BY user_id;
        """

try:
    with engine.connect() as connection:
        df_prices = pd.read_sql(query_prices, connection)
        df_basket = pd.read_sql(query_av_basket, connection)

    print("DataFrames created successfully.")

    print(df_prices.head())
    print(df_basket.head())

except Exception as e:
    print(f"An error occurred connecting to the database: {e}")
    exit(1)

sns.set_theme()

# First chart: Raw Product Prices (All Outliers / Fliers Included)
plt.figure(figsize=(10, 8))
plt.title("Raw Product Prices", fontsize=18)
sns.boxplot(x=df_prices["price"], color="#7285A5", fliersize=10, linewidth=3)
plt.xlabel("price", fontsize=20)
plt.xticks(fontsize=20)
plt.tight_layout()
plt.show()

# Second chart: Adjusted Product Prices (Outliers Hidden)
plt.figure(figsize=(10, 8))
plt.title("Adjusted Product Prices", fontsize=18)
sns.boxplot(x=df_prices["price"], color="#68B478", showfliers=False, linewidth=3)
plt.xlabel("price", fontsize=20)
plt.xticks(fontsize=20)
plt.tight_layout()
plt.show()

# Third chart: Average Basket Price per User
plt.figure(figsize=(10, 8))
plt.title("Average Basket Price per User", fontsize=18)
sns.boxplot(x=df_basket["avg_basket"], color="#64A0C8", fliersize=10, linewidth=3)
plt.xlabel("")
plt.xlim(-20, 150)
plt.xticks(fontsize=20)
plt.tight_layout()
plt.show()
