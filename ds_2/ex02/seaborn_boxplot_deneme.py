import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 1. Sentetik bir e-ticaret fiyat verisi üretelim (sağa çarpık)
np.random.seed(42)
prices = np.concatenate([
    np.random.gamma(shape=2, scale=2, size=500),  # Çoğunluk 2 - 10 TL arası
    [50, 75, 120, 200]                             # Birkaç büyük aykırı değer
])
df_demo = pd.DataFrame({"price": prices})

fig, axes = plt.subplots(1, 3, figsize=(15, 4))

# Örnek 1: Klasik Boxplot
sns.boxplot(x=df_demo["price"], ax=axes[0], color="skyblue")
axes[0].set_title("1. Standart Boxplot (Aykırılar Açık)")

# Örnek 2: showfliers=False Boxplot (Ex02 Grafik 2)
sns.boxplot(x=df_demo["price"], ax=axes[1], color="mediumseagreen", showfliers=False)
axes[1].set_title("2. Zoomed Boxplot (showfliers=False)")

# Örnek 3: Violin Plot (Keman Grafiği)
sns.violinplot(x=df_demo["price"], ax=axes[2], color="salmon")
axes[2].set_title("3. Violin Plot (Yoğunluk Dağılımı)")

plt.tight_layout()
plt.show()
