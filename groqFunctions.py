import os
from groq import Groq
import json
import time
from openai import OpenAI
import agentops

agentops.init(os.environ.get("AGENT_OPS_API_KEY"))


client = Groq(
    api_key=os.environ.get("GROQ_API_KEY")
)

open_ai_client = OpenAI(
    api_key = os.environ.get("OPEN_AI_API_KEY")
)
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


@agentops.record_function('sample function being record')
def getKeywordsWithOpenAi(content):

    
    prompt = '''
        You are going to be give an overview from a conversation. Give up to five words descibing the specific topic of this conversation based on the overview. 
        If there are multiple topics, seperate each topic with a comma.Make sure the sentence does not go over 5 words and use very technical words
        The output should follow the following pattern: 
        {
            keyword: sentence
        }
        Do not return back any text besides the json output

    '''
    chat_completion = open_ai_client.chat.completions.create(
        messages=[
            {

                "role": "user",
                "content":  prompt + str(content),
            },
        ],
        model="gpt-4o-mini",
    )
    chat_output = chat_completion.choices[0].message.content
    print(chat_output)
    return chat_output