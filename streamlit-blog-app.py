import streamlit as st
import pandas as pd
import io
import math
from datetime import datetime

### 初期処理 ###
# ページ設定
st.set_page_config(
    page_title="まとめブログ",
    page_icon="📰"
)

# アプリケーションタイトル
st.title("まとめブログ")

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


### サイドバー ###
# サイドバーでフィルターオプションを提供
st.sidebar.header("フィルターオプション")

# 日付フィルター
st.sidebar.subheader("日付で絞り込み")
min_date = df['date'].min().date()
max_date = df['date'].max().date()
selected_date_range = st.sidebar.date_input(
    "日付範囲を選択",
    [min_date, max_date],
    min_value=min_date,
    max_value=max_date
)

# ソース（サイト）フィルター
sources = df['source'].unique()
selected_sources = st.sidebar.multiselect("表示するソースを選択", options=sources, default=list(sources))

# キーワード検索
st.sidebar.subheader("キーワード検索")
search_term = st.sidebar.text_input("キーワードを入力")

# 更新情報
st.sidebar.markdown("---")
st.sidebar.info(f"最終更新: {datetime.now().strftime('%Y年%m月%d日 %H:%M')}")


### メインコンテンツ ###
## データのフィルタリング ##
# 日付フィルター適用
if len(selected_date_range) == 2:
    start_date, end_date = selected_date_range
    df = df[
        (df['date'].dt.date >= start_date) & 
        (df['date'].dt.date <= end_date)
    ]

# 選択されたソースに基づいてデータをフィルタリング
if selected_sources:
    df = df[df['source'].isin(selected_sources)]
else:
    st.warning("少なくとも1つのソースを選択してください。")

# キーワード検索適用
if search_term:
    df = df[
        df['title'].str.contains(search_term, case=False) | 
        df['source'].str.contains(search_term, case=False)
    ]

# ページネーションの設定（1ページあたり50件）
items_per_page = 50
total_items = len(df)
total_pages = math.ceil(total_items / items_per_page)

# ページ番号の選択（Streamlitのnumber_inputを利用）
page = st.number_input("ページ番号を選択", min_value=1, max_value=total_pages, step=1, value=1)

start_index = (page - 1) * items_per_page
end_index = start_index + items_per_page
df_page = df.iloc[start_index:end_index]

# 最新の記事を上に表示するために日付でソート
df = df.sort_values(by='date', ascending=False)

# 各記事の情報を表示
for index, row in df_page.iterrows():
    # タイトルをリンク付きで表示（クリックすると元記事へ飛びます）
    st.markdown(f"##### [{row['title']}]({row['url']})")
    # 日付とソース情報のキャプション表示
    st.caption(f"{row['date'].strftime('%Y-%m-%d')} | {row['source']}")
    st.write("---")
