import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

df = pd.DataFrame({
    "age": [20, 21, 22, 23, 24, 25],
    "salary": [20000, 22000, 25000, 28000, 30000, 35000]
})

plt.scatter(df["age"], df["salary"])
plt.xlabel("Age")
plt.ylabel("Salary")
plt.show()

sns.scatterplot(data=df, x="age", y="salary")
plt.show()
