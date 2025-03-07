import streamlit as st
import pandas as pd
from datetime import datetime
import io

# ページ設定
st.set_page_config(
    page_title="ブログまとめアプリ",
    page_icon="📰",
    layout="wide"
)

# アプリケーションタイトル
st.title("ブログまとめアプリ")
st.markdown("### 最新記事をチェックしよう 👀")

# CSSの追加
st.markdown("""
<style>
    .article-card {
        background-color: #f9f9f9;
        border-radius: 10px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        border-left: 5px solid #ff4b4b;
        transition: transform 0.2s;
    }
    .article-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 20px rgba(0,0,0,0.1);
    }
    .article-title {
        font-size: 1.3rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    .article-meta {
        font-size: 0.9rem;
        color: #666;
        margin-bottom: 0.5rem;
    }
    .article-source {
        display: inline-block;
        background-color: #e0e0e0;
        padding: 0.2rem 0.5rem;
        border-radius: 5px;
        font-size: 0.8rem;
    }
    .filter-container {
        background-color: #f0f0f0;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# CSVファイルからデータを読み込む
@st.cache_data
def load_data():
    try:
        # CSVファイルのパスを指定（ファイルパスは適宜変更してください）
        file_path = "blog_data.csv"
        
        # ファイルを読み込む
        return pd.read_csv(file_path)
    except Exception as e:
        st.error(f"CSVファイルの読み込みに失敗しました: {e}")
        # エラーが発生した場合はサンプルデータを返す
        data = """date,url,title,source
2025-03-05,https://hamusoku.com/archives/10858699.html,スタバのキラキラ女性店員さん　あまりにも勝ち組陽キャ感が凄い,ハムスター速報
2025-03-05,https://hamusoku.com/archives/10857168.html,東京に来たんやが臭くて草,ハムスター速報
2025-03-05,https://hamusoku.com/archives/10858443.html,アメリカのカードショップ　日本と同じく臭いことが判明,ハムスター速報
2025-03-05,https://hamusoku.com/archives/10858392.html,ワイ、福井県立大学恐竜学部に合格,ハムスター速報"""
        
        return pd.read_csv(io.StringIO(data))

# データの読み込み
df = load_data()

# 日付をdatetime型に変換
df['date'] = pd.to_datetime(df['date'])

# サイドバー - フィルター
st.sidebar.header("フィルター設定")

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
st.sidebar.subheader("サイトで絞り込み")
all_sources = df['source'].unique()
selected_sources = st.sidebar.multiselect(
    "サイトを選択",
    options=all_sources,
    default=all_sources
)

# キーワード検索
st.sidebar.subheader("キーワード検索")
search_term = st.sidebar.text_input("キーワードを入力")

# サイドバー - 表示設定
st.sidebar.header("表示設定")
sort_by = st.sidebar.selectbox(
    "並び替え",
    options=["新しい順", "古い順"],
    index=0
)

# フィルタリング
filtered_df = df.copy()

# 日付フィルター適用
if len(selected_date_range) == 2:
    start_date, end_date = selected_date_range
    filtered_df = filtered_df[
        (filtered_df['date'].dt.date >= start_date) & 
        (filtered_df['date'].dt.date <= end_date)
    ]

# ソースフィルター適用
if selected_sources:
    filtered_df = filtered_df[filtered_df['source'].isin(selected_sources)]

# キーワード検索適用
if search_term:
    filtered_df = filtered_df[
        filtered_df['title'].str.contains(search_term, case=False) | 
        filtered_df['source'].str.contains(search_term, case=False)
    ]

# 並び替え適用
if sort_by == "新しい順":
    filtered_df = filtered_df.sort_values("date", ascending=False)
else:
    filtered_df = filtered_df.sort_values("date", ascending=True)

# フィルター適用後の記事数
st.markdown(f"### 記事数: {len(filtered_df)}")

# 記事の表示
for _, row in filtered_df.iterrows():
    with st.container():
        st.markdown(f"""
        <div class="article-card">
            <div class="article-title">{row['title']}</div>
            <div class="article-meta">{row['date'].strftime('%Y年%m月%d日')} | <span class="article-source">{row['source']}</span></div>
            <a href="{row['url']}" target="_blank">記事を読む →</a>
        </div>
        """, unsafe_allow_html=True)

# 更新情報
st.sidebar.markdown("---")
st.sidebar.info(f"最終更新: {datetime.now().strftime('%Y年%m月%d日 %H:%M')}")

# ファイルアップロード機能（オプション）
st.sidebar.markdown("---")
st.sidebar.subheader("CSVファイルをアップロード")
uploaded_file = st.sidebar.file_uploader("ブログデータのCSVファイル", type=["csv"])

if uploaded_file is not None:
    # 新しいデータフレームを作成
    new_df = pd.read_csv(uploaded_file)
    st.sidebar.success("ファイルをアップロードしました！")
    
    # データのプレビューを表示
    st.sidebar.subheader("アップロードデータのプレビュー")
    st.sidebar.dataframe(new_df.head())
