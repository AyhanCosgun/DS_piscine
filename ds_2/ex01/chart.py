import matplotlib.pyplot as plt
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
import seaborn as sns
import matplotlib.dates as mdates

engine: Engine = create_engine(
    "postgresql+psycopg2://acosgun:mysecretpassword@localhost:5432/piscineds")

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
        TO_CHAR(DATE_TRUNC('month', event_time), 'Mon') as month,
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

except Exception as e:
    print(f"An error occurred connecting to the database: {e}")
    exit(1)

sns.set_theme()

# First chart: Daily Customer Count
plt.figure(figsize=(10, 8))
plt.title("Daily Customer Count", fontsize=18)
sns.lineplot(
    data=df_daily,
    x="day_date",
    y="customer_count"
    )
plt.xlim(df_daily["day_date"].min(), df_daily["day_date"].max())
plt.xlabel("")
plt.ylabel("Number of customers", fontsize=18)
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)
plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%b"))
plt.tight_layout()
plt.show()

# Second chart: Monthly Sales
plt.figure(figsize=(10, 8))
plt.title("Monthly Sales", fontsize=18)
sns.barplot(
    data=df_monthly,
    x="month",
    y="total_sales_mil",
    color="lightsteelblue"
    )
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)
plt.xlabel("month", fontsize=18)
plt.ylabel("total sales in million of ₳", fontsize=18)
plt.tight_layout()
plt.show()

# Third chart: Daily Average Spend per Customer
plt.figure(figsize=(10, 8))
plt.title("Daily Average Spend per Customer", fontsize=18)
sns.lineplot(
    data=df_daily,
    x="day_date",
    y="avg_spend_per_customer",
    color="lightsteelblue"
    )
plt.xlim(df_daily["day_date"].min(), df_daily["day_date"].max())
plt.xlabel("")
plt.ylabel("average spend / customers in ₳", fontsize=18)
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)
plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%b"))
plt.fill_between(
    "day_date",
    "avg_spend_per_customer",
    data=df_daily,
    color="lightsteelblue",
)
plt.tight_layout()
plt.show()
