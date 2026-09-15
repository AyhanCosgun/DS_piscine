from sqlalchemy import create_engine
import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy.engine import Engine

engine: Engine = create_engine(
    "postgresql+psycopg2://acosgun:mysecretpassword@localhost:5432/piscineds")

query = """SELECT
    event_type,
    COUNT(*) AS event_count
    FROM customers
    where event_time >= '2022-10-01' AND event_time < '2023-03-01'
    GROUP BY event_type
    ORDER BY event_count DESC;"""

try:
    with engine.connect() as connection:
        df = pd.read_sql(query, connection)

    print("DataFrame created successfully.")

except Exception as e:
    print(f"An error occurred connecting to the database: {e}")
    exit(1)

print("Event event_types and counts:")
print(df[["event_type", "event_count"]])

plt.figure(figsize=(8, 8))
plt.pie(
    "event_count",
    labels="event_type",
    data=df,
    autopct="%1.1f%%",
    explode=[0.003] * len(df["event_type"]),
    textprops={"fontsize": 18}
)
plt.title("Distribution of Customer Events", fontsize=20)
plt.tight_layout()
plt.show()
