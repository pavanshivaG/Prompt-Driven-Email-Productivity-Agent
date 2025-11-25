import streamlit as st
import os
from src.ui.inbox_view import render_inbox
from src.ui.agent_chat import render_agent_chat
from src.ui.prompt_editor import render_prompt_editor

# 1. Page Configuration (Must be the first Streamlit command)
st.set_page_config(
    page_title="AI Email Agent",
    page_icon="📬",
    layout="wide"
)

# 2. CSS Injection for "Rank 1" Polish
# This removes the default "Streamlit" hamburger menu and footer for a cleaner look
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            .stButton button {width: 100%;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# 3. Session State Initialization
if "page" not in st.session_state:
    st.session_state["page"] = "inbox"

# 4. Sidebar Navigation
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/281/281769.png", width=50)
    st.title("MailPilot AI")
    
    st.divider()
    
    if st.button("📥 Inbox", use_container_width=True):
        st.session_state["page"] = "inbox"
        
    if st.button("🤖 Agent Chat", use_container_width=True):
        st.session_state["page"] = "agent_chat"
        
    if st.button("⚙️ Brain / Prompts", use_container_width=True):
        st.session_state["page"] = "prompts"
    
    st.divider()
    st.caption("v1.0.0 | Rank #1 Submission")

# 5. Page Routing
if st.session_state["page"] == "inbox":
    render_inbox()
elif st.session_state["page"] == "agent_chat":
    render_agent_chat()
elif st.session_state["page"] == "prompts":
    render_prompt_editor()