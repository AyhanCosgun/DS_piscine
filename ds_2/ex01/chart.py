from sqlalchemy import create_engine
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

# ── Veritabanı bağlantısı ──────────────────────────────────────────────────
engine = create_engine(
    "postgresql+psycopg2://acosgun:mysecretpassword@localhost:5432/piscineds"
)

# ─ ─ Sorgu 1: Günlük tekil müşteri sayısı (Grafik 1) ───────────────────────
# Granülarite: gün → Y ekseni 500-2000 civarı (aylık olsaydı çok daha yüksek olurdu)
query_daily = """
    SELECT
        DATE_TRUNC('day', event_time)::date AS day_date,
        COUNT(DISTINCT user_id)             AS customer_count
    FROM customers
    WHERE event_type = 'purchase'
      AND event_time >= '2022-10-01'
      AND event_time <  '2023-03-01'
    GROUP BY DATE_TRUNC('day', event_time)
    ORDER BY day_date;
"""

# ── Sorgu 2: Aylık toplam satış + aylık ortalama harcama (Grafik 2 & 3) ───
# avg_spend = o ayın TOPLAM satışı / o ayın TEKİL müşteri sayısı
# Bunu günlük sorguda hesaplasaydık: o GÜNÜN ortalamasını alırdık (yanlış olurdu!)
query_monthly = """
    SELECT
        DATE_TRUNC('month', event_time)                  AS month_date,
        TO_CHAR(DATE_TRUNC('month', event_time), 'Mon')  AS month_name,
        SUM(price)                                       AS total_sales,
        COUNT(DISTINCT user_id)                          AS customer_count,
        SUM(price) / COUNT(DISTINCT user_id)             AS avg_spend_per_customer
    FROM customers
    WHERE event_type = 'purchase'
      AND event_time >= '2022-10-01'
      AND event_time <  '2023-03-01'
    GROUP BY DATE_TRUNC('month', event_time)
    ORDER BY month_date;
"""

try:
    with engine.connect() as conn:
        df_daily   = pd.read_sql(query_daily,   conn)
        df_monthly = pd.read_sql(query_monthly, conn)

    print("Günlük veri:")
    print(df_daily.head())
    print("\nAylık veri:")
    print(df_monthly)

    # ── 3 Grafik yan yana ─────────────────────────────────────────────────
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    fig.suptitle("Customer Purchase Analysis (Oct 2022 – Feb 2023)", fontsize=14)

    # ── Grafik 1: Number of customers (günlük) ────────────────────────────
    ax1 = axes[0]
    ax1.plot(
        df_daily["day_date"],
        df_daily["customer_count"],
        color="steelblue",
        linewidth=1.2
    )
    ax1.set_title("Number of customers")
    ax1.set_xlabel("Date")
    ax1.set_ylabel("Number of customers")
    ax1.tick_params(axis="x", rotation=45)
    ax1.set_ylim(bottom=0)

    # ── Grafik 2: Total sales (aylık) ─────────────────────────────────────
    ax2 = axes[1]
    ax2.bar(
        df_monthly["month_name"],
        df_monthly["total_sales"],
        color="steelblue",
        width=0.5
    )
    ax2.set_title("Total sales")
    ax2.set_xlabel("Month")
    ax2.set_ylabel("Total sales in A")
    # Milyonları kısalt: 1500000 → "1.5M"
    ax2.yaxis.set_major_formatter(
        mticker.FuncFormatter(lambda x, _: f"{x/1_000_000:.1f}M")
    )

    # ── Grafik 3: Average spend per customer (aylık) ──────────────────────
    ax3 = axes[2]
    ax3.bar(
        df_monthly["month_name"],
        df_monthly["avg_spend_per_customer"],
        color="steelblue",
        width=0.5
    )
    ax3.set_title("Average spend per customer")
    ax3.set_xlabel("Month")
    ax3.set_ylabel("Average spend in A")

    plt.tight_layout()
    plt.show()

except Exception as e:
    print(f"Hata oluştu: {e}")
    raise
