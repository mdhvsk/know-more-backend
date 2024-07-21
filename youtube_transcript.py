from youtube_transcript_api import YouTubeTranscriptApi
from groqFunctions import chatWithGroq
from prompts import flashcard_prompt, bullet_point_prompt, quick_read_prompt


def getTranscript(url):
    start_pos = url.find("v=") + 2
    video_id = url[start_pos:]
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    audio = []
    for i in range(len(transcript)):
        text = transcript[i]['text']
        modified_text = text.replace("\n", " ")
        audio.append(modified_text)

    audio_context = " ".join(audio)

    return audio_context


def getResponse(output, final_transcript):
    if output == "flashcard":
        response = chatWithGroq(flashcard_prompt, final_transcript)
    elif output == "bullet_point":
        response = chatWithGroq(bullet_point_prompt, final_transcript)
    else:
        response = chatWithGroq(quick_read_prompt, final_transcript)
    return response