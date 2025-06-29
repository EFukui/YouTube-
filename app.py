import streamlit as st
import requests
from bs4 import BeautifulSoup
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer

st.set_page_config(page_title="記事要約アプリ", layout="centered")

st.title("📰 記事要約アプリ")
st.markdown("記事URLを入力すると、本文を取得して要約します。")

url = st.text_input("🔗 記事のURLを入力", placeholder="https://example.com/news")

if st.button("要約する") and url:
    try:
        # HTML取得とパース
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        # タイトルと本文らしき段落取得
        title = soup.title.string if soup.title else "（タイトル不明）"
        paragraphs = soup.find_all("p")
        content = "\n".join([p.get_text() for p in paragraphs if len(p.get_text()) > 40])

        st.subheader("📝 記事タイトル")
        st.write(title)

        with st.expander("📄 本文を表示"):
            st.write(content)

        # 要約
        parser = PlaintextParser.from_string(content, Tokenizer("japanese"))
        summarizer = LexRankSummarizer()
        summary = summarizer(parser.document, sentences_count=5)

        st.subheader("✂️ 要約（5文）")
        for sentence in summary:
            st.write("・", sentence)

    except Exception as e:
        st.error(f"取得または要約に失敗しました：{e}")
