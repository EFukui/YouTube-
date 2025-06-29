import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
from transformers import pipeline

st.set_page_config(page_title="YouTube概要アプリ", layout="wide")
st.title("🎬 YouTube字幕要約アプリ")

# URL入力
video_url = st.text_input("YouTubeのURLを入力してください（例：https://www.youtube.com/watch?v=xxxxxxxxxxx）")

# 要約処理
if video_url:
    try:
        video_id = video_url.split("v=")[-1][:11]
        st.info("🎥 字幕を取得中…")

        # 字幕取得（日本語優先）
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=["ja", "en"])
        full_text = " ".join([entry["text"] for entry in transcript])

        st.success("✅ 字幕の取得に成功しました！")
        st.subheader("🎧 字幕（全文）")
        st.write(full_text)

        # 要約処理
        st.info("✏️ 要約を生成中…")
        summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
        summary = summarizer(full_text, max_length=180, min_length=30, do_sample=False)

        st.subheader("📌 要約結果")
        st.write(summary[0]["summary_text"])

    except Exception as e:
        st.error(f"⚠️ エラーが発生しました: {e}")
