import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from pathlib import Path

output_dir = Path(__file__).resolve().parent

engine: Engine = create_engine(
    "postgresql+psycopg2://acosgun:mysecretpassword@localhost:5432/piscineds")

query_fm = """
    SELECT user_id,
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

        df_fm = pd.read_sql(query_fm, connection)

    print("DataFrames created successfully.")

except Exception as e:
    print(f"An error occurred connecting to the database: {e}")
    exit(1)

sns.set_theme()

fig, axs = plt.subplots(1, 2, figsize=(25, 10))

# First chart: The number of orders according to the frequency
axs[0].set_title("The number of orders according to the frequency")
sns.histplot(ax=axs[0],
             data=df_fm,
             x="frequency",
             bins=5,
             binrange=(1, 38),
             color="lightsteelblue",
             linewidth=3)
axs[0].set_xlabel("frequency")
axs[0].set_xticks(ticks=[0, 10, 20, 30])
axs[0].set_ylabel("customers")

# Second chart: the Altairian Dollars spent on the site by customers
axs[1].set_title("the Altairian Dollars spent on the site by customers")
sns.histplot(ax=axs[1],
             data=df_fm,
             x="monetary",
             bins=5,
             binrange=(-25, 225),
             linewidth=3,
             color="lightsteelblue")
axs[1].set_xticks(ticks=[0, 50, 100, 150, 200])
axs[1].set_xlabel("monetary value in ₳")
axs[1].set_ylabel("customers")

counts, bin_edges = np.histogram(df_fm["monetary"], bins=5, range=(-25, 225))
print("Box boundaries:", bin_edges)
print("Customer Counts:", counts)
print("Customer Count in the histogram:", counts.sum())
print("Total Customer Count (df_fm):", df_fm.shape[0])

plt.tight_layout(w_pad=10.0)
plt.savefig(
    output_dir / "frequency_monetary.png",
    dpi=200,
    bbox_inches="tight")
plt.show()
