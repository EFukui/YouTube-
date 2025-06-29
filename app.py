import streamlit as st
import requests
from bs4 import BeautifulSoup
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer

st.title("📰 記事要約アプリ")

url = st.text_input("🔗 記事URLを入力してください")

if st.button("要約する") and url:
    try:
        # 記事を取得
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        paragraphs = soup.find_all("p")
        content = "\n".join([p.get_text() for p in paragraphs if len(p.get_text()) > 40])

        st.subheader("📄 抽出された本文")
        st.write(content[:1000] + "..." if len(content) > 1000 else content)

        parser = PlaintextParser.from_string(content, Tokenizer("english"))  # ← 修正ポイント
        summarizer = LexRankSummarizer()
        summary = summarizer(parser.document, sentences_count=5)

        st.subheader("✂️ 要約（5文）")
        for sentence in summary:
            st.write("・", sentence)

    except Exception as e:
        st.error(f"エラーが発生しました：{e}")
