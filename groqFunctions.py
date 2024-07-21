import os
from groq import Groq
import json
import time



client = Groq(
    api_key=GROQ_API_KEY
)



# def chatWithGroq(prompt, content):
#     while True:
#         try:
#             chat_completion = client.chat.completions.create(
#                 messages=[
#                     {
                
#                         "role": "user",
#                         "content": prompt + content,
#                     },
            
#                 ],
#                 model="llama3-8b-8192",
#             )
#             chat_output = chat_completion.choices[0].message.content
#             start_pos = chat_output.find("{")
#             response = json.loads(chat_output[start_pos:])
            
#             return response
        
#         except (json.JSONDecodeError, KeyError) as e:
#             print(f"Error occurred: {e}")
#             time.sleep(2)


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
            
            # Find the first occurrence of '{' and the last occurrence of '}'
            start_pos = chat_output.find("{")
            end_pos = chat_output.rfind("}") + 1
            
            if start_pos != -1 and end_pos != -1:
                json_str = chat_output[start_pos:end_pos]
                response = json.loads(json_str)
                return response
            else:
                raise ValueError("No valid JSON object found in the response")
        
        except (json.JSONDecodeError, ValueError) as e:
            print(f"Error occurred: {e}")
            print("Raw output:", chat_output)
            time.sleep(2)