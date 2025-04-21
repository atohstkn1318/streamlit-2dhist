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

    # 必要カラムがあるかチェック
    if {"CH1(ch)", "CH2(ch)", "Counts"}.issubset(df.columns):
        x = df["CH1(ch)"]
        y = df["CH2(ch)"]
        z = df["Counts"]

        # ——— カウント範囲を１本のスライダーで指定 ———
        counts_min, counts_max = st.slider(
            "Counts 範囲を選択",
            0,
            int(z.max()),
            (0, int(z.max()))
        )

        # ——— X軸レンジを１本のスライダーで指定 ———
        x_min, x_max = st.slider(
            "X軸 範囲を選択",
            0,
            int(x.max()),
            (0, int(x.max()))
        )

        # ——— Y軸レンジを１本のスライダーで指定 ———
        y_min, y_max = st.slider(
            "Y軸 範囲を選択",
            0,
            int(y.max()),
            (0, int(y.max()))
        )

        # フィルタリング
        mask = (
            (x >= x_min) & (x <= x_max) &
            (y >= y_min) & (y <= y_max) &
            (z >= counts_min) & (z <= counts_max)
        )
        x_f = x[mask]
        y_f = y[mask]
        z_f = z[mask]

        # ビンを 1 チャンネル刻みで作成
        x_bins = np.arange(x_min, x_max + 1)
        y_bins = np.arange(y_min, y_max + 1)

        # 描画
        fig, ax = plt.subplots(figsize=(8, 6))
        hist = ax.hist2d(
            x_f, y_f,
            bins=[x_bins, y_bins],
            weights=z_f,
            cmap='turbo',
            vmin=counts_min,
            vmax=counts_max,
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
