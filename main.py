import streamlit as st
from openai import OpenAI
# from dotenv import load_dotenv
import os

# Load API key from .env file
# load_dotenv()
api_key = st.secrets["OPENAI_API_KEY"]

# Load system prompt once
@st.cache_resource
def load_system_prompt():
    with open("UK_LPA.txt", "r", encoding="utf-8") as f:
        system_prompt = f.read()
    return system_prompt

system_prompt = load_system_prompt()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": system_prompt}
    ]

# --- UI Tabs ---
tab1, tab2 = st.tabs(["💬 Chat", "📄 About"])

# --- CHAT TAB ---
with tab1:
    st.title("🏛️ UK LPA Planning Chatbot")
    user_input = st.text_input("Ask a planning question (e.g., 'Do I need permission for a loft extension?')", key="input")

    if st.button("Send", use_container_width=True) and user_input.strip():
        # Append user prompt
        st.session_state.messages.append({"role": "user", "content": user_input})

        # Call OpenAI
        with st.spinner("Thinking..."):
            client = OpenAI(api_key=api_key)
            response = client.chat.completions.create(
                model="gpt-4.1-nano",  # GPT-4.1-nano
                messages=st.session_state.messages,
                temperature=0.3
            )

            reply = response.choices[0].message.content.strip()
            st.session_state.messages.append({"role": "assistant", "content": reply})

    # Display messages
    for msg in st.session_state.messages[1:]:  # skip system
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# --- ABOUT TAB ---
with tab2:
    st.title("📄 About This Chatbot")
    st.markdown("""
    **UK LPA Chatbot** is a demo assistant for answering house planning queries in England using GPT-4.1-nano.

    ### ⚙️ How it works
    - **Model**: OpenAI GPT-4.1-nano
    - **Prompt**: A detailed planning policy document is loaded once as the system message.
    - **RAG-Free**: This demo does not use vector databases or retrieval; all logic is contained in the system prompt.
    - **Persistence**: Session history is retained using `st.session_state`.
    - **Frontend**: Built with [Streamlit](https://streamlit.io/) and deployed as a web demo.

    ### 🧠 Guardrails
    - Does **not cite sources**
    - Stays strictly within the planning domain
    - Advises users to consult LPAs when needed

    ### 📦 Tech Stack
    - Python 3.10+
    - `openai`, `streamlit`

    ---

    © 2025 — Internal demo use only
    """)

