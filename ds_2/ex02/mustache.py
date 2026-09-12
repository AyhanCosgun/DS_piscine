import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sqlalchemy import create_engine

# ── 1. Veritabanı bağlantısı ────────────────────────────────────────────────
engine = create_engine(
    "postgresql+psycopg2://acosgun:mysecretpassword@localhost:5432/piscineds"
)

try:
    with engine.connect() as conn:
        # Sorgu A: Tekil satın alınan ürün fiyatları (Grafik 1 & 2 için)
        query_prices = """
            SELECT price 
            FROM customers 
            WHERE event_type = 'purchase';
        """
        df_prices = pd.read_sql(query_prices, conn)

        # Sorgu B: Kullanıcı bazında ortalama sepet tutarı (Grafik 3 için)
        query_basket = """
            SELECT user_id, AVG(session_total) AS avg_basket
            FROM (
                SELECT user_id, user_session, SUM(price) AS session_total
                FROM customers
                WHERE event_type = 'purchase'
                GROUP BY user_id, user_session
            ) session_baskets
            GROUP BY user_id;
        """
        df_basket = pd.read_sql(query_basket, conn)

    # ── 2. İstenen İstatistiksel Özeti Konsola Yazdır ──────────────────────
    print(df_prices["price"].describe())

    # ── 3. Grafik Stili (Subject ile tam uyumlu tema) ──────────────────────
    sns.set_theme(style="darkgrid")

    # ── 4. Subject PDF Sayfa 8'deki 3 Box Plot (Alt Alta) ─────────────────
    fig, axes = plt.subplots(3, 1, figsize=(8, 12))

    # Grafik 1: Ham Ürün Fiyatları (Tüm aykırı değerler / fliers dahil)
    sns.boxplot(ax=axes[0], x=df_prices["price"], color="#7285A5", fliersize=3)
    axes[0].set_xlabel("price")

    # Grafik 2: Odaklanmış Ürün Fiyatları (Aykırı değerler gizlenmiş)
    sns.boxplot(ax=axes[1], x=df_prices["price"], color="#68B478", showfliers=False)
    axes[1].set_xlabel("price")

    # Grafik 3: Kullanıcı Başına Ortalama Sepet Tutarı
    sns.boxplot(ax=axes[2], x=df_basket["avg_basket"], color="#64A0C8", fliersize=3)
    axes[2].set_xlabel("price")
    axes[2].set_title("average basket price per user", pad=15)

    plt.tight_layout()
    plt.show()

except Exception as e:
    print(f"Hata oluştu: {e}")
    raise
