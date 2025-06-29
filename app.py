import streamlit as st
import re

# 字幕取得
from youtube_transcript_api import YouTubeTranscriptApi

# 要約モデル
from transformers import pipeline

st.set_page_config(page_title="YouTube字幕要約アプリ", page_icon="🎬")
st.title("🎬 YouTube字幕要約アプリ")
st.markdown("YouTubeのURLを入力してください（例：[https://www.youtube.com/watch?v=xxxxxxxxxxx](https://www.youtube.com/watch?v=xxxxxxxxxxx)）")

# 入力
url = st.text_input("")

# video_id 抽出関数
def extract_video_id(url):
    match = re.search(r"(?:v=|youtu\.be/)([a-zA-Z0-9_-]{11})", url)
    return match.group(1) if match else None

if url:
    video_id = extract_video_id(url)
    if not video_id:
        st.error("❌ video_id を抽出できませんでした。URLを確認してください。")
    else:
        st.success(f"✅ 抽出された video_id: {video_id}")
        
        # 字幕取得
        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=["ja", "en"])
            full_text = " ".join([item["text"] for item in transcript])
            st.subheader("📄 字幕（全文）")
            st.write(full_text)
        except Exception as e:
            st.error(f"字幕取得に失敗しました：{e}")
            full_text = None

        # 要約
        if full_text:
            st.subheader("🧠 要約中...")
            try:
                summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
                summary = summarizer(full_text, max_length=120, min_length=30, do_sample=False)
                st.success("✅ 要約完了")
                st.subheader("📝 要約結果")
                st.write(summary[0]["summary_text"])
            except Exception as e:
                st.error(f"要約に失敗しました：{e}")
