import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Mengatur tampilan
st.set_page_config(page_title="Product Analysis Dashboard", layout="wide")

# Judul dan deskripsi dashboard
st.title("Product Analysis Dashboard")
st.markdown(
    """
Dashboard ini memberikan analisis mengenai produk dengan rentang harga paling banyak dibeli 
dan kategori produk yang paling populer di kalangan pelanggan. 
Gunakan filter di sebelah kiri untuk menyaring data sesuai kebutuhan.
"""
)


# Fungsi untuk memuat data
@st.cache_data
def load_data():
    order_items_df = pd.read_csv("dashboard/order_items_dataset.csv")
    products_df = pd.read_csv("dashboard/products_dataset.csv")
    product_category_translation_df = pd.read_csv(
        "dashboard/product_category_name_translation.csv"
    )

    # Menggabungkan data order_items dengan products
    order_items_products_df = pd.merge(
        order_items_df, products_df, on="product_id", how="inner"
    )
    order_items_products_df = pd.merge(
        order_items_products_df,
        product_category_translation_df,
        on="product_category_name",
        how="left",
    )
    return order_items_products_df


# Memuat data
data = load_data()

# Sidebar untuk filter
st.sidebar.header("Filter Data")

# Filter rentang harga
price_min, price_max = st.sidebar.slider(
    "Rentang Harga Produk", int(data["price"].min()), int(data["price"].max()), (0, 500)
)

# Filter kategori produk
categories = st.sidebar.multiselect(
    "Pilih Kategori Produk",
    options=data["product_category_name_english"].unique(),
    default=data["product_category_name_english"].unique(),
)

# Filter data berdasarkan pilihan
filtered_data = data[
    (data["price"] >= price_min)
    & (data["price"] <= price_max)
    & (data["product_category_name_english"].isin(categories))
]

# Visualisasi 1: Distribusi Rentang Harga
st.subheader("Distribusi Rentang Harga Produk yang Dibeli")
price_range_count = (
    pd.cut(
        filtered_data["price"],
        bins=[0, 50, 100, 200, 300, 400, 500, 1000, 5000],
        labels=[
            "0-50",
            "50-100",
            "100-200",
            "200-300",
            "300-400",
            "400-500",
            "500-1000",
            "1000-5000",
        ],
    )
    .value_counts()
    .sort_index()
)

fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(
    x=price_range_count.index, y=price_range_count.values, palette="Blues_d", ax=ax
)
ax.set_title("Produk dengan Rentang Harga Paling Banyak Dibeli")
ax.set_xlabel("Rentang Harga (BRL)")
ax.set_ylabel("Jumlah Pembelian")
ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
st.pyplot(fig)

# Visualisasi 2: Kategori Produk Paling Populer
st.subheader("Kategori Produk Paling Populer")
category_count = filtered_data["product_category_name_english"].value_counts()

fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(
    x=category_count.head(10).index,
    y=category_count.head(10).values,
    palette="viridis",
    ax=ax,
)
ax.set_title("Kategori Produk Paling Populer di Kalangan Pelanggan")
ax.set_xlabel("Kategori Produk")
ax.set_ylabel("Jumlah Pembelian")
ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
st.pyplot(fig)

# Data Tabel
st.subheader("Data Produk Terfilter")
st.write(filtered_data)

# Informasi Ringkas
st.sidebar.header("Informasi Ringkas")
st.sidebar.write(f"Jumlah Data: {len(filtered_data)}")
st.sidebar.write(f"Rata-rata Harga: {filtered_data['price'].mean():,.2f} BRL")
st.sidebar.write(f"Total Pembelian: {filtered_data['order_item_id'].count()}")
