from sqlalchemy import create_engine
import pandas as pd
import matplotlib.pyplot as plt

engine = create_engine("postgresql+psycopg2://acosgun:mysecretpassword@localhost:5432/piscineds")

query = """SELECT
    event_type,
    COUNT(*) AS event_count
    FROM customers
    GROUP BY event_type
    ORDER BY event_count DESC;"""

try:
    with engine.connect() as connection:
        df = pd.read_sql(query, connection)

    print("DataFrame created successfully.")

    event_types = df["event_type"]
    counts = df["event_count"]

    print("Event event_types and counts:")
    print(df[["event_type", "event_count"]])

    plt.figure(figsize=(8, 8))
    plt.pie(
        counts,
        labels=event_types,
        autopct="%1.1f%%",
        explode=[0.003] * len(event_types),
        textprops={"fontsize": 18}
    )
    plt.title("Distribution of Customer Events", fontsize=20)
    plt.tight_layout()
    plt.show()

except Exception as e:
    print(f"An error occurred connecting to the database: {e}")
