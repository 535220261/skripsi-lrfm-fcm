import pandas as pd
import re

# CLEAN CURRENCY
def clean_currency(value):

    if pd.isna(value):
        return None

    # Kalau sudah numeric → aman
    if isinstance(value, (int, float)):
        return float(value)

    value = str(value)

    # Hapus semua karakter selain angka
    value = re.sub(r"[^\d]", "", value)

    try:
        return float(value)
    except:
        return None

# CLEAN COMMON DATA
def clean_common(df):

    # Konversi tanggal
    df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")

    # Bersihkan monetary
    df["total_amount"] = df["total_amount"].apply(clean_currency)

    # Hapus data invalid
    df = df.dropna(subset=["order_date", "total_amount"])

    return df

# DEDUPLICATE ORDER
def deduplicate_order(df, sum_amount=False):

    agg_method = "sum" if sum_amount else "first"

    df = df.groupby("order_id").agg({
        "username": "first",
        "order_date": "first",
        "total_amount": agg_method
    }).reset_index()

    return df

# SHOPEE LOADER
def load_shopee(file):

    df = pd.read_excel(file)

    df = df[[
        "Username (Pembeli)",
        "No. Pesanan",
        "Waktu Pesanan Dibuat",
        "Total Pembayaran",
        "Status Pesanan",
        "Status Pembatalan/ Pengembalian"
    ]]

    df = df.rename(columns={
        "Username (Pembeli)": "username",
        "No. Pesanan": "order_id",
        "Waktu Pesanan Dibuat": "order_date",
        "Total Pembayaran": "total_amount",
        "Status Pesanan": "status",
        "Status Pembatalan/ Pengembalian": "cancel_return_status"
    })

    # CLEAN FORMAT
    df = clean_common(df)

    # FILTER STATUS BATAL
    df = df[~df["status"].str.lower().isin([
        "batal",
        "dibatalkan",
        "cancelled",
        "canceled"
    ])]

    # FILTER RETUR
    return_mask = ~(
        (df["cancel_return_status"].isna()) |
        (df["cancel_return_status"].str.lower() == "masalah diselesaikan")
    )

    removed_return_count = return_mask.sum()
    df = df[~return_mask]

    # FILTER NILAI 0
    df = df[df["total_amount"] > 0]

    # DEDUP
    df = deduplicate_order(df, sum_amount=False)

    df["marketplace"] = "Shopee"

    return df, removed_return_count

# TIKTOK LOADER
def load_tiktok(file):

    df = pd.read_excel(file)

    df = df[[
        "Buyer Username",
        "Order ID",
        "Created Time",
        "Order Amount",
        "Order Status",
        "Cancelation/Return Type"
    ]]

    df = df.rename(columns={
        "Buyer Username": "username",
        "Order ID": "order_id",
        "Created Time": "order_date",
        "Order Amount": "total_amount",
        "Order Status": "status",
        "Cancelation/Return Type": "cancel_return_type"
    })

    # CLEAN
    df = clean_common(df)

    # FILTER STATUS
    df = df[~df["status"].str.lower().isin([
        "cancelled",
        "canceled",
        "returned",
        "refund",
        "failed"
    ])]

    # FILTER RETUR
    return_mask = df["cancel_return_type"].notna()

    removed_return_count = return_mask.sum()
    df = df[~return_mask]

    # FILTER NILAI 0
    df = df[df["total_amount"] > 0]

    # DEDUP
    df = deduplicate_order(df, sum_amount=False)

    df["marketplace"] = "TikTok"

    return df, removed_return_count

# LAZADA LOADER
def load_lazada(file):

    df = pd.read_excel(file, skiprows=[1])

    df = df[[
        "customerName",
        "orderNumber",
        "createTime",
        "paidPrice",
        "status",
        "buyerFailedDeliveryReturnInitiator"
    ]]

    df = df.rename(columns={
        "customerName": "username",
        "orderNumber": "order_id",
        "createTime": "order_date",
        "paidPrice": "total_amount",
        "buyerFailedDeliveryReturnInitiator": "failed_return_initiator"
    })

    # CLEAN
    df = clean_common(df)

    # FILTER STATUS
    df = df[~df["status"].str.lower().isin([
        "canceled",
        "cancelled",
        "returned",
        "refund",
        "failed"
    ])]

    # FILTER RETUR
    return_mask = df["failed_return_initiator"].notna()

    removed_return_count = return_mask.sum()
    df = df[~return_mask]

    # FILTER NILAI 0
    df = df[df["total_amount"] > 0]

    # DEDUP (LAZADA SUM)
    df = deduplicate_order(df, sum_amount=True)

    df["marketplace"] = "Lazada"

    return df, removed_return_count