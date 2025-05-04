import os
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_turf_response(user_input: str) -> str:
    prompt = f"""
You are a professional turfgrass management assistant. A user has described a turf problem. Analyze the input and provide a likely diagnosis and a management recommendation.
Be concise and professional. Turf type may be included. Always consider location-specific conditions and note uncertainties.

User Input: {user_input}
"""
    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=[{"role": "system", "content": "You assist with professional turfgrass management issues."},
                  {"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=500
    )
    return response['choices'][0]['message']['content'].strip()
