import streamlit as st
import pandas as pd
import io

# CSVファイルからデータを読み込む
@st.cache_data
def load_data():
    try:
        # CSVファイルのパスを指定（必要に応じて変更してください）
        file_path = "blog_data.csv"
        return pd.read_csv(file_path)
    except Exception as e:
        st.error(f"CSVファイルの読み込みに失敗しました: {e}")
        # エラー発生時はサンプルデータを利用する
        data = """date,url,title,source
2025-03-05,https://hamusoku.com/archives/10858699.html,スタバのキラキラ女性店員さん　あまりにも勝ち組陽キャ感が凄い,ハムスター速報
2025-03-05,https://hamusoku.com/archives/10857168.html,東京に来たんやが臭くて草,ハムスター速報
2025-03-05,https://hamusoku.com/archives/10858443.html,アメリカのカードショップ　日本と同じく臭いことが判明,ハムスター速報
2025-03-05,https://hamusoku.com/archives/10858392.html,ワイ、福井県立大学恐竜学部に合格,ハムスター速報"""
        return pd.read_csv(io.StringIO(data))

# データの読み込みと前処理
df = load_data()
df['date'] = pd.to_datetime(df['date'])

# ページタイトルの表示
st.title("まとめブログサイト")

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
for index, row in df[:50].iterrows():
    # タイトルをリンク付きで表示（クリックすると元記事へ飛びます）
    st.markdown(f"##### [{row['title']}]({row['url']})")
    # 日付とソース情報のキャプション表示
    st.caption(f"{row['date'].strftime('%Y-%m-%d')} | {row['source']}")
    st.write("---")
