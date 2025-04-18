import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import io  # これが重要！

# タイトル
st.title("2Dヒストグラム可視化アプリ")

# ファイルアップロード
uploaded_file = st.file_uploader("CSVファイルをアップロードしてください", type=["csv", "xlsx"])

if uploaded_file is not None:
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file, skiprows=45)
    else:
        df = pd.read_excel(uploaded_file, skiprows=45)

    if {"CH1(ch)", "CH2(ch)", "Counts"}.issubset(df.columns):
        x = df["CH1(ch)"]
        y = df["CH2(ch)"]
        z = df["Counts"]

        # スライダー
        vmin = st.slider("最小カウント (vmin)", min_value=0, max_value=int(z.max()), value=0)
        vmax = st.slider("最大カウント (vmax)", min_value=1, max_value=int(z.max()), value=int(z.max()))

        # 描画と保存
        fig, ax = plt.subplots(figsize=(8, 6))
        x_bins = np.arange(x.min(), x.max() + 1)
        y_bins = np.arange(y.min(), y.max() + 1)
        hist = ax.hist2d(x, y, bins=[x_bins, y_bins], weights=z, cmap='turbo', vmin=vmin, vmax=vmax)
        ax.set_xlabel("CH1 (ch)")
        ax.set_ylabel("CH2 (ch)")
        plt.colorbar(hist[3], ax=ax, label="Counts")
        st.pyplot(fig)

        # 画像をバッファに保存してダウンロードリンクを表示
        buf = io.BytesIO()
        fig.savefig(buf, format="png")
        st.download_button(
            label="📥 このヒストグラム画像を保存",
            data=buf.getvalue(),
            file_name="histogram.png",
            mime="image/png"
        )
