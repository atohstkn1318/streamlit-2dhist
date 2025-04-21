import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import io  

# タイトル
st.title("2Dヒストグラム可視化アプリ")

# ファイルアップロード
uploaded_file = st.file_uploader("CSVファイルをアップロードしてください", type=["csv", "xlsx"])

if uploaded_file is not None:
    # ファイル読み込み
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file, skiprows=45)
    else:
        df = pd.read_excel(uploaded_file, skiprows=45)

    if {"CH1(ch)", "CH2(ch)", "Counts"}.issubset(df.columns):
        x = df["CH1(ch)"]
        y = df["CH2(ch)"]
        z = df["Counts"]

        # カラースケール用スライダー
        vmin = st.slider("最小カウント (vmin)", min_value=0, max_value=int(z.max()), value=0)
        vmax = st.slider("最大カウント (vmax)", min_value=1, max_value=int(z.max()), value=int(z.max()))

        # x軸レンジ用スライダー
        x_min = st.slider("X軸 最小値", int(x.min()), int(x.max()), int(x.min()))
        x_max = st.slider("X軸 最大値", int(x.min()), int(x.max()), int(x.max()))

        # y軸レンジ用スライダー
        y_min = st.slider("Y軸 最小値", int(y.min()), int(y.max()), int(y.min()))
        y_max = st.slider("Y軸 最大値", int(y.min()), int(y.max()), int(y.max()))

        # 指定範囲でフィルタリング
        mask = (x >= x_min) & (x <= x_max) & (y >= y_min) & (y <= y_max)
        x_f = x[mask]
        y_f = y[mask]
        z_f = z[mask]

        # ヒストグラム用ビン
        x_bins = np.arange(x_min, x_max + 1)
        y_bins = np.arange(y_min, y_max + 1)

        # 描画
        fig, ax = plt.subplots(figsize=(8, 6))
        hist = ax.hist2d(
            x_f, y_f,
            bins=[x_bins, y_bins],
            weights=z_f,
            cmap='turbo',
            vmin=vmin,
            vmax=vmax,
        )
        ax.set_xlabel("CH1 (ch)")
        ax.set_ylabel("CH2 (ch)")
        ax.set_xlim(x_min, x_max)
        ax.set_ylim(y_min, y_max)
        plt.colorbar(hist[3], ax=ax, label="Counts")
        st.pyplot(fig)

        # 画像ダウンロード
        buf = io.BytesIO()
        fig.savefig(buf, format="png")
        st.download_button(
            label="このヒストグラム画像を保存",
            data=buf.getvalue(),
            file_name="histogram.png",
            mime="image/png"
        )
    else:
        st.error("必要なカラム（CH1(ch), CH2(ch), Counts）が見つかりません。")
