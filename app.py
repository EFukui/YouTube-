import streamlit as st
from gensim.summarization import summarize
import requests
from bs4 import BeautifulSoup

st.title("📰 記事要約アプリ")
url = st.text_input("記事のURLを入力してください")

if url:
    try:
        res = requests.get(url)
        res.encoding = res.apparent_encoding
        soup = BeautifulSoup(res.text, "html.parser")
        text = soup.get_text()
        summary = summarize(text, ratio=0.05)
        st.subheader("🔍 要約結果")
        st.write(summary if summary else "要約できる十分な文章が見つかりませんでした。")
    except Exception as e:
        st.error(f"エラーが発生しました: {e}")
