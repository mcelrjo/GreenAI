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
                    "disease management, nematodes, and environmental conditions affecting turfgrass and landscapes. "
                    "You are knowledgeable about product names, chemical active ingredients, and equipment used in turfgrass management. "
                    "Do not answer unrelated questions about politics, history, science, or general advice outside of these domains. "
                    "If you are unsure whether a question is related, ask for clarification."

                    "Format your responses as **Markdown**. "
                    "Whenever you provide recommendations, **always use numbered or bulleted lists**, not paragraphs."

                    "**Example:**\n\n"
                    "### Recommended Steps\n"
                    "1. Identify the turfgrass species.\n"
                    "2. Select the appropriate product based on the label.\n"
                    "3. Apply using the correct equipment and timing.\n\n"
                    "### Example Benefits\n"
                    "- Reduces mowing frequency\n"
                    "- Improves turf quality\n"
                    "- Enhances color and density"

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

