# Pythonの軽量な公式イメージをベースにする（バージョンは適宜調整してください）
FROM python:3.9-slim

# 作業ディレクトリを設定
WORKDIR /app

# 必要なパッケージのインストール
# requirements.txtに必要なライブラリ（streamlit, pandasなど）を記述しておく
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションのソースコードをコンテナにコピー
COPY . .

# Cloud Runで使用するポート番号（PORT環境変数はCloud Runから自動で設定される）
ENV PORT=8080
EXPOSE 8080

# StreamlitのCORS制限を無効化して、Cloud Run上での利用を許可
# また、PORT番号も指定
CMD streamlit run app.py --server.port $PORT --server.enableCORS false
