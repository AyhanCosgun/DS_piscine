import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

engine: Engine = create_engine(
    "postgresql+psycopg2://acosgun:mysecretpassword@localhost:5432/piscineds")

query_fm = """
    SELECT user_id,
    count (*) AS frequency,
    sum(price) AS monetary
    FROM customers
    WHERE event_type = 'purchase'
    AND event_time >= '2022-10-01' AND event_time < '2023-03-01'
    GROUP BY user_id;
    """

try:
    with engine.connect() as connection:
        df_fm = pd.read_sql(query_fm, connection)

    print("DataFrames created successfully.")

except Exception as e:
    print(f"An error occurred connecting to the database: {e}")
    exit(1)

sns.set_theme()

fig, axs = plt.subplots(1, 2, figsize=(25, 10))

# First chart: The number of orders according to the frequency
axs[0].set_title("The number of orders according to the frequency",
                 fontsize=20)
sns.histplot(ax=axs[0],
             data=df_fm,
             x="frequency",
             bins=5,
             binrange=(1, 38),
             color="lightsteelblue",
             linewidth=3)
axs[0].set_xlabel("frequency", fontsize=20)
axs[0].set_xticks(ticks=[0, 10, 20, 30])
axs[0].tick_params(axis='x', labelsize=20)
axs[0].set_ylabel("customers", fontsize=20)
axs[0].tick_params(axis='y', labelsize=20)

# Second chart: the Altairian Dollars spent on the site by customers
axs[1].set_title("the Altairian Dollars spent on the site by customers",
                 fontsize=20)
sns.histplot(ax=axs[1],
             data=df_fm,
             x="monetary",
             bins=5,
             binrange=(-25, 225),
             linewidth=3,
             color="lightsteelblue")
axs[1].set_xticks(ticks=[0, 50, 100, 150, 200])
axs[1].set_xlabel("monetary value in ₳", fontsize=20)
axs[1].tick_params(axis='x', labelsize=20)
axs[1].set_ylabel("customers", fontsize=20)
axs[1].tick_params(axis='y', labelsize=20)

# Kutu (Rectangle) nesnelerinden sınırları çekme
patches = axs[1].patches

print("--- KUTU SINIRLARI VE MÜŞTERİ SAYILARI ---")
for i, patch in enumerate(patches):
    x_start = patch.get_x()                  # Kutunun sol sınırı
    width = patch.get_width()                # Kutu genişliği
    x_end = x_start + width                  # Kutunun sağ sınırı
    count = patch.get_height()               # Kutunun içine düşen müşteri sayısı
    print(f"{i+1}. Kutu: [{x_start:.2f} ile {x_end:.2f}] aralığı -> Müşteri Sayısı: {int(count)}")

# Her sütunun üzerine müşteri sayısını yazma
# for p in axs[1].patches:
#     height = p.get_height()  # Müşteri sayısı
#     if height > 0:
#         axs[1].annotate(
#             f"{int(height)}",  # Yazılacak metin
#             (
#                 p.get_x() + p.get_width() / 2.0,
#                 height,
#             ),  # Metnin konumu (orta-üst)
#             ha="center",
#             va="bottom",
#             fontsize=14,
#         )

import numpy as np
counts, bin_edges = np.histogram(df_fm["monetary"], bins=5, range=(-25, 225))
print("Kutu Sınır Noktaları:", bin_edges)
print("Müşteri Sayıları:", counts)
print("toplam müşteri sayısı:", counts.sum())
print("toplam müşteri sayısı (df_fm):", df_fm["monetary"].count())
# Çıktı örneği: [-25.   25.   75.  125.  175.  225.]

plt.tight_layout()
plt.show()
