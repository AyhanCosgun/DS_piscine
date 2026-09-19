import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

engine: Engine = create_engine(
    "postgresql+psycopg2://acosgun:mysecretpassword@localhost:5432/piscineds")

query_rfm = """
    SELECT user_id,
        DATE_PART('day', '2023-03-01 00:00:00+00'::timestamp - MAX(event_time))
        AS recency,
        count (*) AS frequency,
        sum(price) AS monetary
    FROM customers
    WHERE event_type = 'purchase'
    AND event_time >= TIMESTAMPTZ '2022-10-01 00:00:00+00'
    AND event_time <  TIMESTAMPTZ '2023-03-01 00:00:00+00'
    GROUP BY user_id;
    """

try:
    with engine.connect() as connection:

        df_rfm = pd.read_sql(query_rfm, connection)

    print("DataFrames created successfully.")

except Exception as e:
    print(f"An error occurred connecting to the database: {e}")
    exit(1)

sns.set_theme()

scaler = StandardScaler()
X_scaled = scaler.fit_transform(df_rfm[["recency", "frequency", "monetary"]])

kmeans = KMeans(n_clusters=5, random_state=42, n_init=10)
df_rfm["cluster"] = kmeans.fit_predict(X_scaled)

cluster_check = df_rfm.groupby("cluster").agg(
    customers=("user_id", "size"),
    recency_mean=("recency", "mean"),
    recency_median=("recency", "median"),
    frequency_mean=("frequency", "mean"),
    frequency_median=("frequency", "median"),
    monetary_mean=("monetary", "mean"),
    monetary_median=("monetary", "median"),
)
print(cluster_check.round(2))

segments = {
    0: "inactive",
    1: "Cluster 1",
    2: "Cluster 2",
    3: "Cluster 3",
}
