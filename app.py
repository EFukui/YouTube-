import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
from transformers import pipeline
import re

st.title("🎬 YouTube字幕要約アプリ")
st.write("YouTubeのURLを入力してください（例： https://www.youtube.com/watch?v=xxxxxxxxxxx）")

# 入力欄
url = st.text_input("")

def extract_video_id(url):
    match = re.search(r"v=([\w-]+)", url)
    if match:
        return match.group(1)
    return None

if url:
    try:
        video_id = extract_video_id(url)
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['ja', 'en'])

        # 字幕を結合
        text = " ".join([entry['text'] for entry in transcript])

        # 要約処理
        summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
        summary = summarizer(text, max_length=200, min_length=60, do_sample=False)

        st.subheader("📝 要約")
        st.write(summary[0]['summary_text'])

    except Exception as e:
        st.error(f"エラーが発生しました: {str(e)}")
