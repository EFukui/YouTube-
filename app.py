import streamlit as st
from urllib.parse import urlparse, parse_qs

st.set_page_config(page_title="YouTube字幕要約アプリ")

st.title("🎬 YouTube字幕要約アプリ")
st.markdown("YouTubeのURLを入力してください（例：[https://www.youtube.com/watch?v=xxxxxxxxxxx](https://www.youtube.com/watch?v=xxxxxxxxxxx)）")

# 入力フォーム
url = st.text_input("")

# ▶️ 動画IDを抽出する関数
def extract_video_id(url):
    try:
        if "youtu.be" in url:
            return url.split("/")[-1].split("?")[0]
        elif "youtube.com" in url:
            query = parse_qs(urlparse(url).query)
            return query.get("v", [None])[0]
        else:
            return None
    except:
        return None

# 処理
if url:
    video_id = extract_video_id(url)
    if isinstance(video_id, str) and video_id:
        st.success(f"✅ 抽出された video_id: `{video_id}`")
        # ※ ここに字幕取得・要約処理を追加できます
    else:
        st.error("エラーが発生しました：`video_id` が取得できませんでした。URLを確認してください。")
