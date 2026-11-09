"""Version 2: deterministic engine plus optional Gemini narration."""
import sys
from pathlib import Path
import streamlit as st
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
load_dotenv(ROOT / ".env")
from game_state import GameState
from game_engine import act, CONFIG
from narrator import narrate

st.set_page_config(page_title="Midnight Library — V2", page_icon="🔐", layout="wide")
st.title("🔐 The Midnight Library — Version 2")
st.caption("Reliable Python-validated gameplay, with optional Gemini narration.")
st.info(CONFIG["starting_description"] + " Examine objects, collect items, and unlock the exit. Type 'hint' if stuck.")
if "v2_state" not in st.session_state:
    st.session_state.v2_state = GameState()
if "v2_chat" not in st.session_state:
    st.session_state.v2_chat = []
with st.sidebar:
    st.header("Game progress")
    st.write("**Inventory:**", ", ".join(sorted(st.session_state.v2_state.inventory)) or "Empty")
    st.write("**Clues discovered:**", sum(x in st.session_state.v2_state.solved for x in ("bookshelf_clue", "desk_clue", "painting_clue")), "/ 3")
    st.write("**Drawer:**", "Open" if st.session_state.v2_state.drawer_open else "Locked")
    st.write("**Exit:**", "Escaped!" if st.session_state.v2_state.door_open else "Locked")
    st.write("**Turns:**", st.session_state.v2_state.turns)
    if st.button("🔄 Restart game"):
        st.session_state.v2_state = GameState()
        st.session_state.v2_chat = []
        st.rerun()
    with st.expander("Debug: public game state"):
        st.json(st.session_state.v2_state.snapshot())
for message in st.session_state.v2_chat:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
if prompt := st.chat_input("e.g. examine bookshelf, open drawer with MOON"):
    st.session_state.v2_chat.append({"role":"user", "content":prompt})
    result = act(st.session_state.v2_state, prompt)
    # Always show the authoritative result before optional prose.
    narrative = narrate(prompt, result.message, st.session_state.v2_state.snapshot())
    response = f"**Game result:** {result.message}\n\n*Game Master:* {narrative}"
    st.session_state.v2_chat.append({"role":"assistant", "content":response})
    st.rerun()
if st.session_state.v2_state.door_open:
    st.success("🏆 ESCAPED! You solved The Midnight Library.")
    st.balloons()
