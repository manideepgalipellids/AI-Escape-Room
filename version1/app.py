"""Version 1: LLM-only baseline. Requires a Gemini API key."""
import os
from pathlib import Path
import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types
from game_prompt import SYSTEM_PROMPT

load_dotenv(Path(__file__).resolve().parents[1] / ".env")
st.set_page_config(page_title="Midnight Library — V1", page_icon="📚")
st.title("📚 The Midnight Library — Version 1")
st.caption("LLM-managed baseline: the model tracks the game using chat history.")
st.info("Explore the bookshelf, desk, painting, drawer and door. Type actions in ordinary English. Find the clues, then escape.")
if st.button("🔄 Restart game"):
    st.session_state.pop("v1_messages", None)
    st.rerun()
if "v1_messages" not in st.session_state:
    st.session_state.v1_messages = [{"role":"assistant", "content":"You wake in a moonlit library. A bookshelf, desk, painting, locked drawer and coded exit door await. What do you do?"}]
for message in st.session_state.v1_messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
if prompt := st.chat_input("What do you do next?"):
    st.session_state.v1_messages.append({"role":"user", "content":prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        api_key = os.getenv("GEMINI_API_KEY", "").strip()
        if not api_key or api_key == "replace_with_your_google_ai_studio_key":
            reply = "⚠️ Add GEMINI_API_KEY to your .env file to use the Version 1 Game Master."
        else:
            try:
                client = genai.Client(api_key=api_key)
                history = [{"role": "user" if m["role"] == "user" else "model", "parts": [{"text":m["content"]}]} for m in st.session_state.v1_messages]
                result = client.models.generate_content(model=os.getenv("GEMINI_MODEL", "gemini-2.5-flash"), contents=history, config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT, temperature=0.6))
                reply = result.text or "The library falls silent. Please try again."
            except Exception as exc:
                reply = f"⚠️ Gemini request failed ({type(exc).__name__}). Check your key, model, network and quota."
        st.markdown(reply)
        st.session_state.v1_messages.append({"role":"assistant", "content":reply})
