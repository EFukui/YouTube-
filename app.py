import streamlit as st
from newspaper import Article
from transformers import pipeline

st.set_page_config(page_title="記事要約アプリ")

st.title("📰 Web記事要約アプリ")
url = st.text_input("記事のURLを入力してください")

if url:
    try:
        # 記事抽出
        article = Article(url)
        article.download()
        article.parse()
        article_text = article.text

        st.subheader("📄 記事本文（抽出結果）")
        st.write(article_text)

        # 要約処理
        summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
        summary = summarizer(article_text, max_length=200, min_length=30, do_sample=False)

        st.subheader("✂ 要約結果")
        st.write(summary[0]['summary_text'])

    except Exception as e:
        st.error(f"記事の取得または要約に失敗しました：{str(e)}")
