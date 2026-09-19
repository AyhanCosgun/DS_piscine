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
import numpy as np

np.set_printoptions(
    precision=2,
    suppress=True,
    floatmode="fixed"
)

pd.options.display.float_format = "{:.2f}".format

data = {
    "Customer": ["M01", "M02", "M03", "M04", "M05", "M06", "M07", "M08", "M09", "M10"],
    "R": [2, 5, 9, 18, 27, 42, 58, 75, 91, 120],
    "F": [12, 10, 8, 7, 5, 4, 3, 2, 1, 1],
    "M": [1200, 1050, 900, 720, 550, 380, 260, 150, 95, 60]
}

df = pd.DataFrame(data)
print("############################## Customer RFM DataFrame ##############################")
print(df)
print("####################################################################################\n")

scalar = StandardScaler()
X_scaled_np_array = scalar.fit_transform(df[["R", "F", "M"]])
print("########################### Scaled Customer RFM Numpy Array #########################")
print(X_scaled_np_array)
print("####################################################################################\n")

print("########################### Inverse transformed Customer RFM Numpy Array ##########################")
print(f"Inverse transformed:\n{scalar.inverse_transform(X_scaled_np_array)}")
print("####################################################################################\n")

print("-"*50)

kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
df["cluster"] = kmeans.fit_predict(X_scaled_np_array)
cluster_summary = df.groupby("cluster")[["R", "F", "M"]].mean()
print("Kümelerin Ortalama Değerleri:")
print(cluster_summary)

segment_names = {
    2: "Loyal Customers",
    1: "New Customers",
    0: "Inactive Customers",
    3: "Platinum VIP"
}
df["segment"] = df["cluster"].map(segment_names)
print(df)

print("-"*50)


X_scaled = df[["Customer"]].join(pd.DataFrame(X_scaled_np_array, columns=["R", "F", "M"]))
print("########################### Scaled Customer RFM DataFrame ##########################")
print(X_scaled)
print("####################################################################################\n")

print("########################### X_scaled metrics #######################################")
print(X_scaled.describe().head(3))
print("####################################################################################\n")

print("########################### KMeans Labels and Inertia ##############################")
inertias = []
K_range = range(4, 5)
for k in K_range:
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    kmeans.fit(X_scaled_np_array)
    inertias.append(kmeans.inertia_)
    print(f"K: {k}, Labels: ", kmeans.labels_)
    print(f"K: {k}, Inertia: {kmeans.inertia_:.2f}")
    #print(f"inertia change (abs): \33[92m{abs(inertias[-1] - inertias[-2]):.2f}\33[0m" if k > 1 else '\33[92m inertia change (abs): N/A \33[0m')
print("####################################################################################\n")

print("########################### KMeans Clusters #########################################")
for i in set(kmeans.labels_):
    mask = kmeans.labels_ == i
    print(f"Cluster {i}: ", X_scaled[mask]["Customer"].values)
print("####################################################################################\n")

print("########################### KMeans Cluster Centers ##################################")
print(pd.DataFrame(scalar.inverse_transform(kmeans.cluster_centers_), columns=["R", "F", "M"]))
print("####################################################################################\n")
