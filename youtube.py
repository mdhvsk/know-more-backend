import requests
from youtube_transcript_api import YouTubeTranscriptApi
from groqFunctions import chatWithGroq
from prompts import flashcard_prompt, bullet_point_prompt, quick_read_prompt

API_KEY = "AIzaSyAyDacalcyKd7P7XqrAMDQkefOTRTmeKHM"

def search_youtube_videos(keyword, max_results=3):
    youtube_search_url = f"https://www.googleapis.com/youtube/v3/search?key={API_KEY}&part=snippet&type=video&q={keyword}&maxResults={max_results}"
    response = requests.get(youtube_search_url)
    data = response.json()
    
    video_ids = [item['id']['videoId'] for item in data['items']]
    return video_ids

def get_transcript(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return " ".join([entry['text'] for entry in transcript])
    except Exception as e:
        print(f"Error getting transcript for video {video_id}: {str(e)}")
        return ""

def get_transcripts_for_keyword(keyword):
    video_ids = search_youtube_videos(keyword)
    if len(video_ids) > 1 : 
        video_ids.replace(" ", "+")
    transcripts = {}
#TDDO : Add a list a of keywords to search for instead of just one. 
    
    for video_id in video_ids:
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        transcript = get_transcript(video_id)
        transcripts[video_url] = transcript
    
    return transcripts

def getResponse(output, final_transcript):
    if output == "flashcard":
        response = chatWithGroq(flashcard_prompt, final_transcript)
    elif output == "bullet_point":
        response = chatWithGroq(bullet_point_prompt, final_transcript)
    else:
        response = chatWithGroq(quick_read_prompt, final_transcript)
    return response

def process_keyword(keyword, output_type):
    transcripts = get_transcripts_for_keyword(keyword)
    combined_transcript = " ".join(transcripts.values())
    response = getResponse(output_type, combined_transcript)
    return response

if __name__ == "__main__":
    keyword = input("Enter a keyword to search for: ")
    output_type = input("Enter output type (flashcard/bullet_point/quick_read): ")
    
    result = process_keyword(keyword, output_type)
    print(result)
