import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression

# Örnek: Basit bir Regresyon Modeli
X = [[1], [2], [3]]  # Girdiler
y = [2, 4, 6]  # Hedefler

model = LinearRegression()
model.fit(X, y)
print(model.predict([[4]]))  # Çıktı: [8.]


# Örnek Veri: [Recency (gün), Monetary (₳)]
data = np.array([[10, 1000], [20, 2000], [30, 3000]])

scaler = StandardScaler()

# Hem parametreleri öğrenir (fit) hem dönüştürür (transform)
data_scaled = scaler.fit_transform(data)

print(data_scaled)
# Çıktı:
# [[-1.22474487 -1.22474487]
#  [ 0.          0.        ]
#  [ 1.22474487  1.22474487]]