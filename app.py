import streamlit as st
import requests
from bs4 import BeautifulSoup
from gensim.summarization import summarize

st.title("📰 記事要約アプリ")

url = st.text_input("記事のURLを入力してください")

if url:
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.content, "html.parser")

        # 本文抽出：pタグの内容を連結
        paragraphs = soup.find_all("p")
        text = "\n".join(p.get_text() for p in paragraphs if p.get_text())

        if len(text) < 500:
            st.warning("本文が短すぎて要約できません。")
        else:
            st.subheader("📄 本文の一部")
            st.write(text[:1000] + "...")

            summary = summarize(text, ratio=0.2)
            st.subheader("✂️ 要約")
            st.write(summary)

    except Exception as e:
        st.error(f"エラーが発生しました: {e}")
