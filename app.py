import streamlit as st
import requests
from bs4 import BeautifulSoup
from transformers import pipeline

st.set_page_config(page_title="Web記事要約アプリ", layout="centered")
st.title("📰 Web記事要約アプリ")

url = st.text_input("記事のURLを入力してください（例：https://example.com/article）")

if url:
    try:
        # 記事本文を取得
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # タイトル + 本文の取得（シンプル版）
        title = soup.title.string if soup.title else ""
        paragraphs = soup.find_all("p")
        article = "\n".join(p.get_text() for p in paragraphs)

        if len(article.strip()) < 200:
            st.error("記事の本文が十分に取得できませんでした。")
        else:
            st.success("記事本文を取得しました。要約中...")

            # 要約（HuggingFace Transformers）
            summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
            summary = summarizer(article, max_length=200, min_length=60, do_sample=False)[0]['summary_text']

            st.subheader("📝 要約結果")
            st.write(summary)

    except Exception as e:
        st.error(f"記事の取得または要約に失敗しました：{e}")
