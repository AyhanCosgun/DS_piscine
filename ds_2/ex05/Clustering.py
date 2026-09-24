import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from matplotlib.ticker import MultipleLocator, FuncFormatter
from pathlib import Path

output_dir = Path(__file__).resolve().parent

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


scaler = StandardScaler()
X_scaled = scaler.fit_transform(df_rfm[["recency", "frequency", "monetary"]])

kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
df_rfm["cluster"] = kmeans.fit_predict(X_scaled)

cluster_check = df_rfm.groupby("cluster").agg(
    customers=("user_id", "size"),
    recency_median=("recency", "median"),
    frequency_median=("frequency", "median"),
    monetary_median=("monetary", "median"),
    revenue=("monetary", "sum"),
    revenue_per_customer=("monetary", "mean"),
    median_revenue=("monetary", "median"),
)

cluster_check["customer_share_pct"] = (
    100 * cluster_check["customers"] / cluster_check["customers"].sum()
)
cluster_check["revenue_share_pct"] = (
    100 * cluster_check["revenue"] / cluster_check["revenue"].sum()
)
cluster_check["revenue_index"] = (
    cluster_check["revenue_per_customer"] / df_rfm["monetary"].mean()
)

pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)

print(cluster_check.round(2), file=open(f"{output_dir}/cluster_check.txt", "w"))

segment_names = {
    0: "Inactive",
    1: "Potential",
    3: "Loyal - Gold",
    2: "Loyal - Platinum",
}

df_rfm["segment"] = df_rfm["cluster"].map(segment_names)

segment_order = list(segment_names.values())

sns.set_theme(style="white")

# First chart: The number of customers in each RFM segment
plt.figure(figsize=(12, 7))
plt.title("Customer count by RFM segment")
sns.countplot(
    data=df_rfm,
    y="segment",
    order=segment_order,
    hue="segment",
    hue_order=segment_order,
    legend=False,
    palette="Set2"
)
sns.despine(right=True, top=True)
plt.xlabel("number of customers")
plt.ylabel("")

ax = plt.gca()
for container in ax.containers:
    ax.bar_label(container, padding=3, fmt="%d")

plt.tight_layout()
plt.savefig(
    output_dir / "Customer_count_by_RFM_segment.png",
    dpi=200,
    bbox_inches="tight")
plt.show()


# Second chart: Bubble plot of RFM segments

bubble_summary = (
    df_rfm.groupby("segment", observed=True).agg(
        recency_median_months=("recency", "median"),
        frequency_median=("frequency", "median"),
        monetary_mean=("monetary", "mean"),
    )
    .reindex(segment_order)
    .reset_index()
)

plt.figure(figsize=(12, 10))
plt.title("Bubble plot of RFM segments")
sns.scatterplot(
    data=bubble_summary,
    x="recency_median_months",
    y="frequency_median",
    hue="segment",
    hue_order=segment_order,
    size="monetary_mean",
    palette="Set2",
    sizes=(300, 3500),
    alpha=0.8,
    size_norm=(0, bubble_summary["monetary_mean"].max()),
    legend=False,
)

sns.despine(right=True, top=True)
plt.xlabel("Median Recency (month)")
plt.ylabel("Median Frequency")

ax = plt.gca()
for row in bubble_summary.itertuples():
    ax.annotate(
        f'Average "{row.segment}": {row.monetary_mean:,.2f} ₳',
        xy=(row.recency_median_months, row.frequency_median),
        xytext=(10, 10),
        textcoords="offset points",
    )

ax.xaxis.set_major_locator(MultipleLocator(30.44))
ax.xaxis.set_major_formatter(
    FuncFormatter(lambda days, position: f"{days / 30.44:.0f}")
)

plt.tight_layout()
plt.savefig(
    output_dir / "Bubble_plot_of_RFM_segments.png",
    dpi=200,
    bbox_inches="tight")
plt.show()


# Third chart: Scatter plot of customers with centroids (Recency vs Frequency)

plt.figure(figsize=(12, 7))
plt.title("Customer Clusters with Centroids")
sns.scatterplot(
    data=df_rfm,
    x="recency",
    y="frequency",
    hue="segment",
    hue_order=segment_order,
    alpha=0.6,
    palette="Set2",
    linewidth=0,
    s=70
)

centroids_raw = scaler.inverse_transform(kmeans.cluster_centers_)
plt.scatter(
    centroids_raw[:, 0],
    centroids_raw[:, 1],
    s=250,
    c="yellow",
    label="Centroids",
    alpha=0.9,
)

plt.xlabel("Recency (Days)")
plt.ylabel("Frequency (Orders)")
plt.legend(title="Segments", bbox_to_anchor=(1.02, 1), loc="upper left")
plt.tight_layout()
plt.savefig(
    output_dir / "Clusters_with_Centroids.png",
    dpi=200,
    bbox_inches="tight"
)
plt.show()


# Fourth chart: Standardized 2D Cluster Scatter Plot with centroids (Frequency vs Monetary)
sns.set_theme()

Scaled_rfm = df_rfm[["segment"]].reset_index(drop=True).join(
    pd.DataFrame(X_scaled, columns=["recency", "frequency", "monetary"])
)
plt.figure(figsize=(12, 7))
plt.title("Standardized 2D Cluster Scatter Plot (FM plane)")
sns.scatterplot(
    data=Scaled_rfm,
    x="frequency",
    y="monetary",
    hue="segment",
    hue_order=segment_order,
    s=600,
    palette="Set2",
    linewidth=0
)

plt.scatter(
    kmeans.cluster_centers_[:, 1],
    kmeans.cluster_centers_[:, 2],
    s=900,
    c="yellow",
    label="Centroids",
    edgecolors="black",
    zorder=5
)

plt.xlim(-1, 7)
plt.ylim(-2, 7)
plt.xlabel("Frequency (z-score)")
plt.ylabel("Monetary (z-score)")
plt.legend(
    title="Segments",
    bbox_to_anchor=(1.02, 1),
    loc="upper left",
    labelspacing=1.7
    )
plt.tight_layout()
plt.savefig(
    output_dir / "Scaled_Clusters_with_Centroids_FM_plane.png",
    dpi=200,
    bbox_inches="tight"
    )
plt.show()
