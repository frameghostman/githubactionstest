import streamlit as st
import pandas as pd
import io
import math

# ページ設定
st.set_page_config(
    page_title="まとめブログサイト",
    page_icon="📰"
)

# CSVファイルからデータを読み込む
@st.cache_data
def load_data():
    try:
        # GitHub上のCSVファイルのRaw URLを指定
        url = "https://raw.githubusercontent.com/frameghostman/githubactionstest/refs/heads/main/blog_data.csv"
        return pd.read_csv(url)
    except Exception as e:
        st.error(f"CSVファイルの読み込みに失敗しました: {e}")
        # エラー時はサンプルデータを返す
        data = """date,url,title,source
2025-03-05,https://hamusoku.com/archives/10858699.html,スタバのキラキラ女性店員さん　あまりにも勝ち組陽キャ感が凄い,ハムスター速報
2025-03-05,https://hamusoku.com/archives/10857168.html,東京に来たんやが臭くて草,ハムスター速報
2025-03-05,https://hamusoku.com/archives/10858443.html,アメリカのカードショップ　日本と同じく臭いことが判明,ハムスター速報
2025-03-05,https://hamusoku.com/archives/10858392.html,ワイ、福井県立大学恐竜学部に合格,ハムスター速報"""
        return pd.read_csv(io.StringIO(data))

# データの読み込みと前処理
df = load_data()
df['date'] = pd.to_datetime(df['date'])

# ページネーションの設定（1ページあたり50件）
items_per_page = 50
total_items = len(df)
total_pages = math.ceil(total_items / items_per_page)

# アプリケーションタイトル
st.title("まとめブログサイト")

# ページ番号の選択（Streamlitのnumber_inputを利用）
page = st.number_input("ページ番号を選択", min_value=1, max_value=total_pages, step=1, value=1)

start_index = (page - 1) * items_per_page
end_index = start_index + items_per_page
df_page = df.iloc[start_index:end_index]

# サイドバーでフィルターオプションを提供（例：ソースによるフィルタリング）
st.sidebar.header("フィルターオプション")
sources = df['source'].unique()
selected_sources = st.sidebar.multiselect("表示するソースを選択", options=sources, default=list(sources))

# 選択されたソースに基づいてデータをフィルタリング
if selected_sources:
    df = df[df['source'].isin(selected_sources)]
else:
    st.warning("少なくとも1つのソースを選択してください。")

# 最新の記事を上に表示するために日付でソート
df = df.sort_values(by='date', ascending=False)

# 各記事の情報を表示
for index, row in df_page.iterrows():
    # タイトルをリンク付きで表示（クリックすると元記事へ飛びます）
    st.markdown(f"##### [{row['title']}]({row['url']})")
    # 日付とソース情報のキャプション表示
    st.caption(f"{row['date'].strftime('%Y-%m-%d')} | {row['source']}")
    st.write("---")
