import os
from groq import Groq
import json
import time


client = Groq(
    api_key=os.environ.get("GROQ_API_KEY")
)


# def chatWithGroq(prompt, content):


#     chat_completion = client.chat.completions.create(
#         messages=[
#             {
#                 "role": "user",
#                 "content": prompt + content,
#             }
#         ],
#         model="llama3-8b-8192",
#     )
#     chat_output = chat_completion.choices[0].message.content
#     print(type(chat_output))

#     print(chat_output)

#     start_pos = chat_output.find("{")
#     response = json.loads(chat_output[start_pos:])
#     print(type(response))
#     print(response)
    


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
