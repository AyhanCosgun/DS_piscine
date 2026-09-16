from sklearn.cluster import KMeans
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler

# Etiketli (supervised) örnek: metrekareden fiyat öğrenmek
# X = [[60], [80], [100]]
# y = [2_000_000, 2_600_000, 3_300_000]
# model = LinearRegression().fit(X, y)
# print(model.predict([[90]]))


# Etiketsiz (unsupervised) örnek: müşterileri RFM benzerliğine göre ayırmak

import pandas as pd

data = {
    "Customer": ["M01", "M02", "M03", "M04", "M05", "M06", "M07", "M08", "M09", "M10"],
    "R": [2, 5, 9, 18, 27, 42, 58, 75, 91, 120],
    "F": [12, 10, 8, 7, 5, 4, 3, 2, 1, 1],
    "M": [1200, 1050, 900, 720, 550, 380, 260, 150, 95, 60]
}

df = pd.DataFrame(data)
print(df)

scalar = StandardScaler()
X_scaled_np_array = scalar.fit_transform(df[["R", "F", "M"]])
X_scaled = df[["Customer"]].join(pd.DataFrame(X_scaled_np_array, columns=["R", "F", "M"]))
print(X_scaled)
print("X_scaled metrics:", X_scaled.describe().round(3))

inertias = []
K_range = range(4, 5)
for k in K_range:
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    kmeans.fit(X_scaled_np_array)
    inertias.append(kmeans.inertia_)
    print(f"K: {k}, Labels: ", kmeans.labels_)
    print(f"K: {k}, Inertia:", kmeans.inertia_)
    #print(f"inertia change (abs): \33[92m{abs(inertias[-1] - inertias[-2]):.2f}\33[0m" if k > 1 else '\33[92m inertia change (abs): N/A \33[0m')

for i in set(kmeans.labels_):
    print(f"Cluster {i}: ", X_scaled[kmeans.labels_ == i]["Customer"].values)

