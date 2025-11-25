import streamlit as st
import json
import os
from src.backend.email_processor import EmailProcessor
from src.ui.components import render_email_card  # <--- NEW IMPORT

def load_data():
    """Loads processed emails. If not found, runs the processor first."""
    processed_path = os.path.join("data", "processed_inbox.json")
    
    if not os.path.exists(processed_path):
        st.warning("⚠️ Inbox not processed yet. Running AI Agent now...")
        processor = EmailProcessor()
        processor.process_inbox()
        st.rerun()
        
    with open(processed_path, "r") as f:
        return json.load(f)

def render_inbox():
    st.title("📬 Smart Inbox Agent")
    
    # 1. Top Controls
    col1, col2 = st.columns([3, 1])
    with col1:
        search_query = st.text_input("🔍 Search emails...", placeholder="Search subject or sender")
    with col2:
        if st.button("🔄 Refresh Inbox"):
            with st.spinner("Processing new emails..."):
                processor = EmailProcessor()
                processor.process_inbox()
            st.rerun()

    emails = load_data()
    
    # Filter logic
    if search_query:
        emails = [e for e in emails if search_query.lower() in e['subject'].lower() or search_query.lower() in e['body'].lower()]

    # 2. The "Rank 1" Kanban Board Layout
    tab1, tab2 = st.tabs(["📋 Kanban Board", "📝 List View"])
    
    with tab1:
        c_urgent, c_work, c_news, c_other = st.columns(4)
        
        categories = {
            "Urgent": c_urgent,
            "Work": c_work,
            "Newsletter": c_news,
            "Spam": c_other,
            "Finance": c_other,
            "Uncategorized": c_other
        }

        # Headers
        c_urgent.markdown("### 🚨 Urgent")
        c_work.markdown("### 🏢 Work")
        c_news.markdown("### 📰 News")
        c_other.markdown("### 📂 Other")

        for email in emails:
            category = email.get("category", "Uncategorized")
            target_col = categories.get(category, c_other)
            
            with target_col:
                # <--- REPLACED 20 LINES OF CODE WITH THIS CLEAN FUNCTION
                is_clicked = render_email_card(email, on_click_key=f"btn_{email['id']}")
                
                if is_clicked:
                    st.session_state["selected_email"] = email
                    st.session_state["page"] = "agent_chat" 
                    st.rerun()

    with tab2:
        for email in emails:
            with st.expander(f"{email['subject']} - {email['sender']}"):
                st.write(email['body'])
                st.json(email)