import streamlit as st
from newspaper import Article
import openai

# OpenAI APIキー設定（安全な保存が必要です）
openai.api_key = st.secrets["OPENAI_API_KEY"]  # Streamlit Secretから読み込みを推奨

st.set_page_config(page_title="News Digest - 記事要約アプリ")

st.title("📰 News Digest - 記事要約アプリ")
st.write("ニュース記事のURLを入力してください（例：https://www.bbc.com/news/...）")

url = st.text_input("記事URL")

if url:
    with st.spinner("記事を読み込んで要約中..."):
        try:
            # 記事を抽出
            article = Article(url)
            article.download()
            article.parse()
            content = article.text
            title = article.title

            # GPTに要約させる
            prompt = f"以下の記事を日本語で簡潔に3行で要約してください：\n\n{content}"
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=500
            )
            summary = response['choices'][0]['message']['content']

            st.success(f"📰 タイトル：{title}")
            st.markdown("### ✅ 要約結果")
            st.markdown(summary)

        except Exception as e:
            st.error(f"要約に失敗しました: {e}")
