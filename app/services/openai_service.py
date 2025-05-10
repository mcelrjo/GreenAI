import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def get_turf_response(user_input: str) -> str:
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a highly specialized AI assistant trained only to answer questions related to turfgrass, "
                    "lawncare, mowing, fertilization, weed control, irrigation, disease diagnostics, grass types, and "
                    "related turf management practices. If someone asks anything outside this domain—including topics like politics, history, science, or general advice—"
                    "respond with: 'I'm sorry, but I can only help with lawncare and turfgrass-related questions.'"
                )
            },
            {"role": "user", "content": user_input}
        ]
    )
    return response.choices[0].message["content"]


