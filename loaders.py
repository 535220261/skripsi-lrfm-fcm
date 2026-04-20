import pandas as pd

# FUNGSI UMUM MEMBERSIHKAN FORMAT
def clean_common(df):

    # Konversi tanggal
    df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")

    # BERSIHKAN FORMAT UANG LEBIH AMAN
    df["total_amount"] = (
        df["total_amount"]
        .astype(str)
        .str.replace(".", "", regex=False)
        .str.replace(",", ".", regex=False)
    )

    df["total_amount"] = pd.to_numeric(df["total_amount"], errors="coerce")

    # Konversi ke numeric SEKALI LAGI secara paksa
    df["total_amount"] = pd.to_numeric(df["total_amount"], errors="coerce")

    # Hapus yang gagal konversi
    df = df.dropna(subset=["order_date", "total_amount"])

    # Pastikan benar-benar float
    df["total_amount"] = df["total_amount"].astype(float)

    return df


# DEDUPLICATE PER ORDER
def deduplicate_order(df, sum_amount=False):
    agg_method = "sum" if sum_amount else "first"

    df = df.groupby("order_id").agg({
        "username": "first",
        "order_date": "first",
        "total_amount": agg_method
    }).reset_index()

    return df


# SHOPEE
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

    # BUANG STATUS CANCEL / BATAL UMUM
    df = df[~df["status"].str.lower().isin([
        "batal",
        "dibatalkan",
        "cancelled",
        "canceled"
    ])]

    # FILTER KHUSUS SHOPEE (Retur/Refund)
    # Hitung dulu jumlah yang akan dihapus
    return_mask = ~(
        (df["cancel_return_status"].isna()) |
        (df["cancel_return_status"].str.lower() == "masalah diselesaikan")
    )

    removed_return_count = return_mask.sum()

    # Simpan hanya yang valid
    df = df[~return_mask]

    # HAPUS MONETARY 0

    # Pastikan numeric sebelum filter
    df["total_amount"] = pd.to_numeric(df["total_amount"], errors="coerce")
    df = df[df["total_amount"] > 0]

    df = deduplicate_order(df, sum_amount=False)

    df["marketplace"] = "Shopee"

    return df, removed_return_count


# TIKTOK
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

    # BUANG STATUS CANCEL UMUM
    df = df[~df["status"].str.lower().isin([
        "cancelled",
        "canceled",
        "returned",
        "refund",
        "failed"
    ])]

    # FILTER KHUSUS TIKTOK (Retur/Refund)

    return_mask = df["cancel_return_type"].notna()

    removed_return_count = return_mask.sum()

    df = df[~return_mask]

    # Hapus monetary 0
    # Pastikan numeric sebelum filter
    df["total_amount"] = pd.to_numeric(df["total_amount"], errors="coerce")
    df = df[df["total_amount"] > 0]

    df = deduplicate_order(df, sum_amount=False)

    df["marketplace"] = "TikTok"

    return df, removed_return_count

# LAZADA
def load_lazada(file):

    df = pd.read_excel(file)

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

    # BUANG STATUS CANCEL UMUM
    df = df[~df["status"].str.lower().isin([
        "canceled",
        "cancelled",
        "returned",
        "refund",
        "failed"
    ])]

    # FILTER KHUSUS LAZADA (Retur/Refund)
    return_mask = df["failed_return_initiator"].notna()

    removed_return_count = return_mask.sum()

    df = df[~return_mask]

    # Hapus monetary 0
    # Pastikan numeric sebelum filter
    df["total_amount"] = pd.to_numeric(df["total_amount"], errors="coerce")
    df = df[df["total_amount"] > 0]

    df = deduplicate_order(df, sum_amount=True)

    df["marketplace"] = "Lazada"

    return df, removed_return_count