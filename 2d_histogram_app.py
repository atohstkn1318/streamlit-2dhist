import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import io

st.title("2Dヒストグラム可視化アプリ")

uploaded_file = st.file_uploader("CSVまたはExcelをアップロード", type=["csv", "xlsx"])
if uploaded_file is None:
    st.stop()

# --- データ読み込み ---
if uploaded_file.name.endswith(".csv"):
    df = pd.read_csv(uploaded_file, skiprows=45)
else:
    df = pd.read_excel(uploaded_file, skiprows=45)

if not {"CH1(ch)", "CH2(ch)", "Counts"}.issubset(df.columns):
    st.error("必要なカラム（CH1(ch), CH2(ch), Counts）が見つかりません。")
    st.stop()

x = df["CH1(ch)"]
y = df["CH2(ch)"]
z = df["Counts"]

# --- レイアウト：左・中央・右 ---
col_y, col_center, col_z = st.columns([1, 6, 1])

# 左側：Y軸レンジ
with col_y:
    y_min, y_max = st.slider(
        "Y軸 範囲",
        0,
        int(y.max()),
        (0, int(y.max())),
        key="y_range"
    )

# 右側：Countsレンジ
with col_z:
    counts_min, counts_max = st.slider(
        "Counts 範囲",
        0,
        int(z.max()),
        (0, int(z.max())),
        key="z_range"
    )

# 中央：まずプロット用プレースホルダを作成しておき、その下にX軸レンジスライダー
with col_center:
    plot_placeholder = st.empty()

    x_min, x_max = st.slider(
        "X軸 範囲",
        0,
        int(x.max()),
        (0, int(x.max())),
        key="x_range"
    )

# --- フィルタリング & プロット ---
mask = (
    (x >= x_min) & (x <= x_max) &
    (y >= y_min) & (y <= y_max) &
    (z >= counts_min) & (z <= counts_max)
)
x_f, y_f, z_f = x[mask], y[mask], z[mask]

x_bins = np.arange(x_min, x_max + 1)
y_bins = np.arange(y_min, y_max + 1)

fig, ax = plt.subplots(figsize=(6, 6))
hist = ax.hist2d(
    x_f, y_f,
    bins=[x_bins, y_bins],
    weights=z_f,
    cmap='turbo',
    vmin=counts_min,
    vmax=counts_max
)
ax.set_xlim(x_min, x_max)
ax.set_ylim(y_min, y_max)
ax.set_xlabel("CH1 (ch)")
ax.set_ylabel("CH2 (ch)")
plt.colorbar(hist[3], ax=ax, label="Counts")

# プロットをプレースホルダに差し込む
plot_placeholder.pyplot(fig)

# ダウンロードボタンも中央カラムに置く
with col_center:
    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    st.download_button(
        label="このヒストグラム画像を保存",
        data=buf.getvalue(),
        file_name="histogram.png",
        mime="image/png"
    )
