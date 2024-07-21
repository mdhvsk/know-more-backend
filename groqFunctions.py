import os
from groq import Groq
import json
import time


client = Groq(
    api_key=os.environ.get("GROQ_API_KEY")
)


def getKeywordsWithGroq(content):

    
    prompt = '''
        You are going to be give an overview from a conversation. Give a five word sentence descibing the overarching topic of this conversation based on the overview. 
        Make sure the sentence does not go over 5 words.
        The output should follow the following pattern: 
        {
            words: sentence
        }
        Do not return back any text besides the json output

    '''
    chat_completion = client.chat.completions.create(
        messages=[
            {

                "role": "user",
                "content":  prompt + str(content),
            },
        ],
        model="llama3-8b-8192",
    )
    chat_output = chat_completion.choices[0].message.content
    print(chat_output)
    return chat_output


def chatWithGroq(prompt, content):
    while True:
        try:
            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt + content,
                    },
                ],
                model="llama3-8b-8192",
            )
            chat_output = chat_completion.choices[0].message.content
            start_pos = chat_output.find("{")
            response = json.loads(chat_output[start_pos:])

            return response

        except (json.JSONDecodeError, KeyError) as e:
            print(f"Error occurred: {e}")
            time.sleep(2)
