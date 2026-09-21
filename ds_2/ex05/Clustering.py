import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from pathlib import Path

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
print(cluster_check.round(2),file=open("asd.txt", "w"))


# Üretilecek PNG dosyalarının doğru klasöre yazılacağı yolu saklar.
output_dir = Path(__file__).resolve().parent

# K-Means numaralarını iş açısından okunabilir isimlere dönüştürür.
segment_names = {
    0: "Inactive / reactivation",        # Ortalama R çok yüksek olan eski müşteriler.
    1: "Recent low-value / potential",   # Yeni olduğu kanıtlanmayan, düşük değerli yakın müşteri.
    3: "Loyal - Silver",                 # Düzenli ve orta-yüksek değerli müşteri.
    2: "Loyal - Gold/Platinum",          # En sık ve en yüksek harcamalı müşteri.
}

# Tüm tablolarda ve grafiklerde kullanılacak bilinçli sunum sırası.
segment_order = list(segment_names.values())

# Her segmentin bütün grafiklerde aynı kalacak rengi.
# palette = {
#     "Inactive / reactivation": "#D55E00",       # Turuncu-kırmızı: dikkat / risk.
#     "Recent low-value / potential": "#56B4E9",  # Mavi: gelişim potansiyeli.
#     "Loyal - Silver": "#7A7A7A",                # Gri: Silver.
#     "Loyal - Gold/Platinum": "#E69F00",         # Altın: yüksek değer.
# }

# Her müşterinin cluster numarasından iş adı üretir.
df_rfm["segment"] = df_rfm["cluster"].map(segment_names)

from sklearn.metrics import silhouette_score

print("k=5 silhouette:", round(silhouette_score(X_scaled, df_rfm["cluster"]), 3))

# # K-Means centroidleri X_scaled uzayındadır; grafikte ham R/F birimleri için geri dönüştürülür.
# centroids_raw = pd.DataFrame(
#     scaler.inverse_transform(kmeans.cluster_centers_),
#     columns=["recency", "frequency", "monetary"],
# )

# # Centroid satırına doğru iş adını da bağlar.
# centroids_raw["cluster"] = range(kmeans.n_clusters)
# centroids_raw["segment"] = centroids_raw["cluster"].map(segment_names)


# Bar değerleri ve segment adları doğrudan df_rfm'deki her müşteri satırından sayılacak.
fig, ax = plt.subplots(figsize=(11, 5))

# Her segment için müşteri sayısını yatay bar olarak çizer.
sns.countplot(
    data=df_rfm,                   # İçinde her müşteri ve segment sütunu bulunan tablo.
    y="segment",                   # Kategorik eksen dikey; uzun segment isimleri okunur.
    order=segment_order,            # Bar sırasını iş mantığına göre sabitler.
    hue="segment",                 # Her segmentin palette'teki rengini seçmesini sağlar.
    legend=False,                   # y ekseninde isim zaten olduğu için tekrarlı legend'ı gizler.
    ax=ax,                          # Grafiği bu Matplotlib eksenine çizer.
)

# Her barın ucuna tam müşteri sayısını yazdırır.
for container in ax.containers:
    ax.bar_label(container, padding=3, fmt="%d")

# Başlık ve eksen etiketleri grafiğin iş sorusunu açıklar.
ax.set(title="Customer count by RFM segment", xlabel="Number of customers", ylabel="")

# Kesilmiş label olmaması için boşlukları otomatik ayarlar.
fig.tight_layout()

# PNG çıktısını script'in olduğu ex05 klasörüne subject'e uygun bir adla kaydeder.
fig.savefig(output_dir / "Clustering_segment_sizes.png", dpi=200, bbox_inches="tight")
plt.show()











# Her segmenti tek satıra indirger; medyan aykırı değerlerden daha dayanıklıdır.
bubble_summary = (
    df_rfm.groupby("segment", observed=True)
    .agg(
        customers=("user_id", "size"),                         # Bubble yanına yazılacak segment büyüklüğü.
        recency_months=("recency", lambda s: s.median() / 30.44),# Median R'yi gün yerine aya çevirir.
        median_frequency=("frequency", "median"),              # y eksenindeki tipik sipariş sayısı.
        median_monetary=("monetary", "median"),                # Bubble alanını belirleyecek tipik harcama.
    )
    .reindex(segment_order)                                      # Satır sırasını grafiklerle eşitler.
    .reset_index()                                               # segment'i yeniden normal sütun yapar.
)

# Orta boy bir figür ve tek eksen oluşturur.
fig, ax = plt.subplots(figsize=(11, 7))

# Her segment için tek bir bubble çizer.
sns.scatterplot(
    data=bubble_summary,             # Dört satırlık özet tablosu.
    x="recency_months",              # Solda yakın zamanlı, sağda eski alışveriş.
    y="median_frequency",            # Yukarı doğru daha sık satın alma.
    hue="segment",                   # Segmenti renk ile kodlar.
    size="median_monetary",          # Median harcamayı bubble alanı ile kodlar.
    sizes=(250, 1800),                # En küçük/en büyük marker alanını okunabilir sınırlar.
    legend="brief",                  # Legend'da segment ve anlamlı boyut örneklerini gösterir.
    ax=ax,                            # Çizimi seçilen eksene yapar.
)

# Her bubble'ın yanına iş adı ve kaç müşteri içerdiğini koyar.
for row in bubble_summary.itertuples():
    ax.annotate(
        f"{row.segment}\nn={row.customers:,}",
        (row.recency_months, row.median_frequency),
        xytext=(8, 8), textcoords="offset points", fontsize=9,
    )

# Frequency aralığı geniş olduğunda küçük değerleri de görünür kılmak için log ölçek kullanır.
ax.set_yscale("log")

# Eksenlerin neyi ölçtüğünü ve bubble alanının anlamını açıkça yazar.
ax.set(
    title="RFM segment profile: recency, frequency and monetary value",
    xlabel="Median recency (months since last purchase; lower is more recent)",
    ylabel="Median frequency (orders; log scale)",
)

# Düzeni düzeltir, dosyayı üretir ve gösterir.
fig.tight_layout()
fig.savefig(output_dir / "Clustering_rfm_bubbles.png", dpi=200, bbox_inches="tight")
plt.show()
