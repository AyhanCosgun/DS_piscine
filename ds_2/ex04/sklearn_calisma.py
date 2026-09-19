import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer

# StandardScaler: sayısal ölçekleme
# Ne zaman? K-Means, lojistik regresyon, SVM, k-NN, PCA gibi mesafe veya katsayı cezası kullanan yöntemlerde.

# Sütunlar: [recency, frequency, monetary]
X = np.array([[2, 12, 1200], [30, 5, 520], [100, 1, 70]], dtype=float)

scaler = StandardScaler(with_mean=True, with_std=True)
X_scaled = scaler.fit_transform(X)

print(X_scaled.round(3))
print("Öğrenilen ortalamalar:", scaler.mean_)
print("Öğrenilen ölçekler:", scaler.scale_)

# Yeni müşteri için YENİDEN fit etme: aynı eski ölçeği uygula.
new_customer = np.array([[10, 7, 700]], dtype=float)
print(scaler.transform(new_customer).round(3))




# Eksik değer: SimpleImputer
# Ne zaman? NaN içeren sayısal/kategorik sütunlarınız varsa.
# Sayısal sütunda medyan, kategorik sütunda en sık değer çoğu zaman güvenli temel seçimdir.
# Eksikliği sıfırla doldurmak ancak sıfırın gerçekten anlamlı olduğu durumda doğrudur.


X = np.array([[2.0, 1200.0], [np.nan, 550.0], [40.0, np.nan]])
imputer = SimpleImputer(strategy="median")
X_filled = imputer.fit_transform(X)

print(X_filled)
print("Sütun medyanları:", imputer.statistics_)