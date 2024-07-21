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
    video_ids = search_youtube_videos(keyword, max_results=1)
    if video_ids:
        video_id = video_ids[0]
        return get_transcript(video_id)
    return ""

def process_keywords(keywords, output_type):
    all_responses = []
    for keyword in keywords:
        transcript = get_transcript_for_keyword(keyword)
        response = getResponse(output_type, transcript)
        all_responses.append({"keyword": keyword, "response": response})
    return all_responses

def get_transcript_for_keyword(keyword):
    video_ids = search_youtube_videos(keyword, max_results=1)
    if video_ids:
        video_id = video_ids[0]
        return get_transcript(video_id)
    return ""

def getResponse(output, transcript):
    if output == "flashcard":
        response = chatWithGroq(flashcard_prompt, transcript)
    elif output == "bullet_point":
        response = chatWithGroq(bullet_point_prompt, transcript)
    else:
        response = chatWithGroq(quick_read_prompt, transcript)
    return response

if __name__ == "__main__":
    # Accept JSON input
    input_json = input("Enter JSON input: ")
    input_data = json.loads(input_json)
    
    keywords = input_data["words"]
    output_type = input_data["output_type"]
    
    results = process_keywords(keywords, output_type)
    
    
    
