import openai
import os
from app.services.conversation_service import get_session_messages, add_message

openai.api_key = os.getenv("OPENAI_API_KEY")

def get_turf_response(user_input: str, session_id: str = "default") -> str:
    # Add user input to session memory
    add_message(session_id, "user", user_input)

    # Retrieve the full conversation
    messages = get_session_messages(session_id)

    # Make OpenAI API call with the full history
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    # Extract the assistant's reply
    result = response.choices[0].message["content"]

    # Add the assistant's reply to session memory
    add_message(session_id, "assistant", result)

    return result
