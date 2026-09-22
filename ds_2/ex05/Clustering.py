import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from pathlib import Path
from matplotlib.ticker import MultipleLocator, FuncFormatter

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

print(cluster_check.round(2),file=open("cluster_check.txt", "w"))


output_dir = Path(__file__).resolve().parent

segment_names = {
    0: "Inactive / reactivation",      
    1: "Recent low-value / potential",
    3: "Loyal - Gold",
    2: "Loyal - Platinum",
}

df_rfm["segment"] = df_rfm["cluster"].map(segment_names)

segment_order = list(segment_names.values())

sns.set_theme(style="white", font="DejaVu Sans")

# First chart: The number of customers in each RFM segment
plt.figure(figsize=(20, 10))
plt.title("Customer count by RFM segment", fontsize=18)
sns.countplot(
    data=df_rfm,
    y="segment",
    order=segment_order,
    hue="segment",
    legend=False,
    palette="Set2"
)
sns.despine(right=True, top=True)
plt.xlabel("number of customers", fontsize=18)
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)
plt.ylabel("")

ax = plt.gca()
for container in ax.containers:
    ax.bar_label(container, padding=3, fmt="%d", fontsize=18)

plt.tight_layout()
plt.savefig(output_dir / "Clustering_segment_sizes.png", dpi=200, bbox_inches="tight")
plt.show()




bubble_summary = (
    df_rfm.groupby("segment", observed=True)
    .agg(
        recency_median_months=(
            "recency",
            "median"
        ),
        frequency_median=("frequency", "median"),
        monetary_mean=("monetary", "mean"),
    )
    .reindex(segment_order)
    .reset_index()
)

# Second chart: Bubble plot of RFM segments
plt.figure(figsize=(20, 15))
plt.title("Bubble plot of RFM segments", fontsize=18)
sns.scatterplot(
    data=bubble_summary,
    x="recency_median_months",
    y="frequency_median",
    hue="segment",
    size="monetary_mean",
    palette="Set2",
    sizes=(500, 5000),
    size_norm=(0, bubble_summary["monetary_mean"].max()),
    legend=False
)

sns.despine(right=True, top=True)
plt.xlabel("Median Recency (months)", fontsize=18)
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)
plt.ylabel("Median Frequency", fontsize=18)

ax = plt.gca()
for row in bubble_summary.itertuples():
    ax.annotate(
        f'Average "{row.segment}": {row.monetary_mean:,.2f} ₳',
        xy=(row.recency_median_months, row.frequency_median),
        xytext=(10, 10),
        textcoords="offset points",
        fontsize=14,
    )

ax.xaxis.set_major_locator(MultipleLocator(30.44))
ax.xaxis.set_major_formatter(
    FuncFormatter(lambda days, position: f"{days / 30.44:.0f}")
)

plt.tight_layout()
plt.savefig(output_dir / "Clustering_rfm_bubbles.png", dpi=200, bbox_inches="tight")
plt.show()






# # Orta boy bir figür ve tek eksen oluşturur.
# fig, ax = plt.subplots(figsize=(20, 10))

# sns.scatterplot(
#     data=bubble_summary,
#     x="recency_median_months",
#     y="frequency_median",
#     hue="segment",
#     size="monetary_mean",              # Bubble ALANI ortalama Monetary'ye bağlı.
#     palette="Set2",
#     sizes=(180, 1800),                 # Görsel alan aralığı; birimi point².
#     size_norm=(0, bubble_summary["monetary_mean"].max()),
#     legend=False,                      # Subjectteki gibi legend yok.
#     ax=ax,
# )

# for row in bubble_summary.itertuples():
#     ax.annotate(
#         f'Average "{row.segment}": {row.monetary_mean:,.2f} ₳',
#         xy=(row.recency_median_months, row.frequency_median),
#         xytext=(10, 10),
#         textcoords="offset points",
#         fontsize=11,
#     )


# ax.xaxis.set_major_locator(MultipleLocator(30.44))
# ax.xaxis.set_major_formatter(
#     FuncFormatter(lambda days, position: f"{days / 30.44:.0f}")
# )

# ax.set(
#     title="Customer segments",
#     xlabel="Median Recency (month)",
#     ylabel="Median Frequency",
# )
# # Düzeni düzeltir, dosyayı üretir ve gösterir.
# fig.tight_layout()
# fig.savefig(output_dir / "Clustering_rfm_bubbles.png", dpi=200, bbox_inches="tight")
# plt.show()


# GRAFİK 2: Kümeler ve Centroidler (Scatter Plot: Recency vs Frequency)
# plt.figure(figsize=(9, 6))
# sns.scatterplot(data=df_rfm, x="recency", y="frequency", hue="segment", alpha=0.6, palette="Set1")

# # Centroidleri orijinal ölçeğe geri çevirip çizelim
# centroids = scaler.inverse_transform(kmeans.cluster_centers_)
# plt.scatter(centroids[:, 0], centroids[:, 1], s=250, c="yellow", edgecolor="black", marker="X", label="Centroids")

# plt.title("Customer Clusters with Centroids")
# plt.xlabel("Recency (Days)")
# plt.ylabel("Frequency (Orders)")
# plt.legend()
# plt.tight_layout()
# plt.show()
