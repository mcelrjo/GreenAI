from typing import Dict, List

# In-memory session storage
sessions: Dict[str, List[Dict[str, str]]] = {}

def get_or_create_session(session_id: str) -> List[Dict[str, str]]:
    if session_id not in sessions:
        sessions[session_id] = [
            {
                "role": "system",
                "content": (
                    "You are a highly specialized AI assistant trained only to answer questions related to turfgrass, "
                    "lawncare, mowing, fertilization, weed control, irrigation, disease diagnostics, grass types, and "
                    "related turf management practices. If someone asks anything outside this domain—including topics like politics, history, science, or general advice—"
                    "respond with: 'I'm sorry, but I can only help with lawncare and turfgrass-related questions.'"
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

