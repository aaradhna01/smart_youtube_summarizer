from youtube_transcript_api import YouTubeTranscriptApi

def extract_video_id(url):
    if "watch?v=" in url:
        return url.split("watch?v=")[-1].split("&")[0]
    elif "youtu.be/" in url:
        return url.split("youtu.be/")[-1].split("?")[0]
    return None

def get_transcript(video_url):
    video_id = extract_video_id(video_url)
    try:
        # Try Hindi first, then English if available
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=["hi", "en"])
        full_text = " ".join([item["text"] for item in transcript])
        return full_text
    except Exception as e:
        return f"❌ Error: {str(e)}"
