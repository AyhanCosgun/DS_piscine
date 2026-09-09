import matplotlib.pyplot as plt
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
import seaborn as sns
import matplotlib.dates as mdates
from matplotlib import font_manager
from matplotlib.font_manager import FontProperties

font_path = font_manager.findfont("Lato")
currency_font = FontProperties(fname=font_path)

engine: Engine = create_engine(
    "postgresql+psycopg2://acosgun:mysecretpassword@localhost:5432/piscineds")

query = """
    SELECT price FROM customers WHERE event_type = 'purchase';
    """
try:
    with engine.connect() as connection:
        df = pd.read_sql(query, connection)

    print("DataFrames created successfully.")
    print(df[["price"]].describe())

except Exception as e:
    print(f"An error occurred connecting to the database: {e}")
    exit(1)

# sns.set_theme()

# # First chart: Daily Customer Count
# plt.figure(figsize=(10, 8))
# plt.title("Daily Customer Count", fontsize=18)
# sns.lineplot(
#     data=df_daily,
#     x="day_date",
#     y="customer_count"
#     )
# plt.xlim(df_daily["day_date"].min(), df_daily["day_date"].max())
# plt.xlabel("")
# plt.ylabel("Number of customers", fontsize=16)
# plt.xticks(fontsize=14)
# plt.yticks(fontsize=14)
# plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
# plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%b"))
# plt.tight_layout()
# plt.show()

# # Second chart: Monthly Sales
# plt.figure(figsize=(10, 8))
# plt.title("Monthly Sales", fontsize=18)
# sns.barplot(
#     data=df_monthly,
#     x="month",
#     y="total_sales_mil",
#     color="lightsteelblue"
#     )
# plt.xticks(fontsize=14)
# plt.yticks(fontsize=14)
# plt.xlabel("month", fontsize=16)
# plt.ylabel("total sales in million of ₳",
#            fontsize=16, fontproperties=currency_font)
# plt.tight_layout()
# plt.show()

# # Third chart: Daily Average Spend per Customer
# plt.figure(figsize=(10, 8))
# plt.title("Daily Average Spend per Customer", fontsize=18)
# sns.lineplot(
#     data=df_daily,
#     x="day_date",
#     y="avg_spend_per_customer",
#     color="lightsteelblue"
#     )
# plt.xlim(df_daily["day_date"].min(), df_daily["day_date"].max())
# plt.xlabel("")
# plt.ylabel("average spend / customers in ₳",
#            fontsize=16, fontproperties=currency_font)
# plt.xticks(fontsize=14)
# plt.yticks(fontsize=14)
# plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
# plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%b"))
# plt.fill_between(
#     "day_date",
#     "avg_spend_per_customer",
#     data=df_daily,
#     color="lightsteelblue",
# )
# plt.tight_layout()
# plt.show()


fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# 1. Item Price Box Plot
sns.boxplot(ax=axes[0], x=df["price"], color="skyblue")
axes[0].set_title("Purchased Item Prices")
axes[0].set_xlabel("Price (Altairian Dollars)")

# 2. User Average Basket Price Box Plot
basket_df = pd.read_sql("""
    SELECT user_id, AVG(session_total) as avg_basket
    FROM (
        SELECT user_id, user_session, SUM(price) as session_total
        FROM customers
        WHERE event_type = 'purchase'
        GROUP BY user_id, user_session
    ) t
    GROUP BY user_id;
""", engine)

sns.boxplot(ax=axes[1], x=basket_df["avg_basket"], color="lightgreen")
axes[1].set_title("Average Basket Price per User")
axes[1].set_xlabel("Basket Price (Altairian Dollars)")

plt.tight_layout()
plt.show()
