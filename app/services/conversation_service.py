from typing import Dict, List

# In-memory session storage
sessions: Dict[str, List[Dict[str, str]]] = {}

def get_or_create_session(session_id: str) -> List[Dict[str, str]]:
    if session_id not in sessions:
        sessions[session_id] = [
            {
                "role": "system",
                "content": (
                    "You are a highly specialized AI assistant focused on turfgrass, lawncare, landscaping, and related topics. "
                    "You specialize in helping with turfgrass species, mowing, irrigation, fertilization, weed control, insect control, "
                    "disease management, and environmental conditions affecting turfgrass and landscapes. "
                    "You are also knowledgeable about commercial product names, chemical active ingredients, and brand names used in these industries. "
                    "If you are unsure whether a question is related, ask for clarification. "
                    "Do not answer unrelated questions about politics, history, science, or general advice outside of turfgrass, lawncare, or landscaping."
                )
            }
        ]
    return sessions[session_id]

def add_message(session_id: str, role: str, content: str):
    session = get_or_create_session(session_id)
    session.append({"role": role, "content": content})

def get_session_messages(session_id: str) -> List[Dict[str, str]]:
    return get_or_create_session(session_id)

def clear_session(session_id: str):
    if session_id in sessions:
        del sessions[session_id]

