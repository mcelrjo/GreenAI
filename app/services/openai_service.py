import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_turf_response(user_input):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a turfgrass diagnostic assistant."},
            {"role": "user", "content": user_input},
        ],
    )
    return response.choices[0].message.content


