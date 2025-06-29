import streamlit as st
from newspaper import Article
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer

st.set_page_config(page_title="記事要約アプリ", layout="centered")

st.title("📰 記事要約アプリ")
st.markdown("ニュースやブログの記事URLを入力してください。本文を取得して、自動的に要約します。")

url = st.text_input("🔗 記事のURLを入力", placeholder="https://example.com/news")

if st.button("要約する") and url:
    try:
        # 記事をダウンロードして解析
        article = Article(url, language="ja")
        article.download()
        article.parse()

        st.subheader("📝 記事タイトル")
        st.write(article.title)

        # 本文を表示（任意）
        with st.expander("📄 記事の全文を表示"):
            st.write(article.text)

        # 要約を生成
        parser = PlaintextParser.from_string(article.text, Tokenizer("japanese"))
        summarizer = LexRankSummarizer()
        summary = summarizer(parser.document, sentences_count=5)

        st.subheader("✂️ 要約（5文）")
        for sentence in summary:
            st.write("・", sentence)

    except Exception as e:
        st.error(f"記事の取得または要約に失敗しました：{e}")
