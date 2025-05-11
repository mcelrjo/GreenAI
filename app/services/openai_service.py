import openai
import os
from app.services.conversation_service import get_session_messages, add_message
from app.services.retrieval_service import retrieve_relevant_context

openai.api_key = os.getenv("OPENAI_API_KEY")

def get_turf_response(user_input: str, session_id: str = "default") -> str:
    # Retrieve relevant context from your knowledge base
    context = retrieve_relevant_context(user_input)

    # Format the prompt with retrieved context
    context_prompt = f"Use the following information to answer accurately:\n\n{context}\n\nUser Question: {user_input}"

    # Add user input with context to session memory
    add_message(session_id, "user", context_prompt)

    # Retrieve the full conversation history
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