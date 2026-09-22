import pandas as pd

# 1. Örnek Tablomuzu Oluşturalım
data = {
    "user_id":   [1001, 1002, 1003, 1004, 1005, 1006, 1007, 1008, 1009, 1010],
    "recency":   [   5,   12,    8,   85,  120,   90,   95,    3,    1,    4],
    "frequency": [  12,    8,   15,    2,    1,    1,    3,   35,   42,   28],
    "monetary":  [ 450,  320,  600,   45,   20,   30,   70, 2100, 2800, 1800],
    "cluster":   [   0,    0,    0,    1,    1,    1,    1,    2,    2,    2]
}
df_rfm = pd.DataFrame(data)

print("=== HAM VERİ SETİ (df_rfm) ===")
print(df_rfm)
print("\n" + "="*80 + "\n")

# 2. GROUPBY ve AGG (Named Aggregation)
# SQL: SELECT cluster, COUNT(*) AS customers, ... FROM df_rfm GROUP BY cluster;
cluster_check = df_rfm.groupby("cluster").agg(
    customers=("user_id", "size"),
    recency_median=("recency", "median"),
    frequency_median=("frequency", "median"),
    monetary_median=("monetary", "median"),
    revenue=("monetary", "sum"),
    revenue_per_customer=("monetary", "mean"),
    median_revenue=("monetary", "median"),
)

# 3. YÜZDELER VE ENDEKS HESABI (SQL Window Function mantığı)
# SQL: 100.0 * customers / SUM(customers) OVER ()
cluster_check["customer_share_pct"] = (
    100 * cluster_check["customers"] / cluster_check["customers"].sum()
)

# SQL: 100.0 * revenue / SUM(revenue) OVER ()
cluster_check["revenue_share_pct"] = (
    100 * cluster_check["revenue"] / cluster_check["revenue"].sum()
)

# SQL: revenue_per_customer / (SELECT AVG(monetary) FROM df_rfm)
cluster_check["revenue_index"] = (
    cluster_check["revenue_per_customer"] / df_rfm["monetary"].mean()
)

print("=== KÜMELEME ÖZET TABLOSU (cluster_check) ===")
print(cluster_check.round(2).to_string())
print("\n" + "="*80 + "\n")

# 4. İŞ ZEKASI YORUMU
print("=== METRİK OKUMA VE İŞ YORUMU ===")
for c_id, row in cluster_check.iterrows():
    print(f"Cluster {c_id}:")
    print(f"  - Müşterilerin %{row['customer_share_pct']:.1f}'ini oluşturuyor.")
    print(f"  - Toplam cironun %{row['revenue_share_pct']:.1f}'ini getiriyor.")
    print(f"  - Değer Endeksi: {row['revenue_index']:.2f}x (Ortalamanın {row['revenue_index']:.2f} katı harcıyor)\n")

