import streamlit as st
import json
import os
from src.llm.llm_client import LLMClient
from src.backend.rag_engine import RagEngine

def render_agent_chat():
    st.title("🤖 AI Email Agent")
    
    # 1. Safety Check
    if "selected_email" not in st.session_state:
        st.info("👈 Please select an email from the Inbox first.")
        if st.button("Go to Inbox"):
            st.session_state["page"] = "inbox"
            st.rerun()
        return

    email = st.session_state["selected_email"]
    llm = LLMClient()
    
    # Load RAG Context
    with open(os.path.join("data", "processed_inbox.json"), "r") as f:
        all_emails = json.load(f)
    rag = RagEngine(all_emails)

    col_email, col_agent = st.columns([1, 1])
    
    with col_email:
        st.subheader("📧 Current Email")
        st.info(f"**From:** {email['sender']}\n\n**Subject:** {email['subject']}")
        st.write(email['body'])
        
        st.divider()

        # --- NEW: DISPLAY LLM SUGGESTIONS (ACTION ITEMS) ---
        # This satisfies "LLM generates suggestions"
        suggestions = email.get("action_items", [])
        if suggestions:
            st.success(f"⚡ **AI Suggestions ({len(suggestions)})**")
            for item in suggestions:
                # Handle cases where the LLM returns a simple string or a dict
                task_text = item.get('task', str(item)) if isinstance(item, dict) else str(item)
                st.markdown(f"- {task_text}")
        else:
            st.caption("No specific actions suggested by AI.")
        # ---------------------------------------------------
        
        st.divider()
        
        # RAG Context
        st.caption("🔍 **Related Context Found by Agent:**")
        context_text = rag.find_related_context(email)
        
        if context_text and "No prior context" not in context_text:
            with st.expander("View Previous Emails"):
                st.text(context_text)
        else:
            st.caption("No previous context found.")

    with col_agent:
        st.subheader("💬 Agent Assistant")
        
        action = st.selectbox("Choose Action", ["Chat / Ask Question", "Draft Reply", "Summarize"])
        
        if action == "Summarize":
            if st.button("Generate Summary"):
                with st.spinner("Reading..."):
                    prompt = f"Summarize this email in 2 bullet points:\n{email['body']}"
                    summary = llm.generate_response(prompt)
                    st.success(summary)

        elif action == "Draft Reply":
            user_instructions = st.text_area("Instructions (Optional)", placeholder="e.g., Tell them I'll be late")
            
            if st.button("✍️ Draft Reply"):
                with st.spinner("Consulting context & drafting..."):
                    with open(os.path.join("data", "prompt_templates.json"), "r") as f:
                        templates = json.load(f)
                    
                    prompt = templates["generate_reply"]["template"].format(
                        context=context_text, 
                        sender=email['sender'],
                        body=email['body'],
                        user_instructions=user_instructions,
                        tone="Professional"
                    )
                    
                    draft = llm.generate_response(prompt)
                    st.session_state["current_draft"] = draft

            if "current_draft" in st.session_state:
                st.markdown("### 📝 Review Draft")
                final_draft = st.text_area("Edit before saving:", value=st.session_state["current_draft"], height=200)
                
                c1, c2 = st.columns(2)
                with c1:
                    if st.button("💾 Save Draft"):
                        # Save to JSON (Safety Requirement)
                        draft_entry = {
                            "original_email_id": email['id'],
                            "recipient": email['sender'],
                            "subject": f"Re: {email['subject']}",
                            "body": final_draft,
                            "status": "draft"
                        }
                        
                        drafts_path = os.path.join("data", "drafts.json")
                        if os.path.exists(drafts_path):
                            with open(drafts_path, "r") as f:
                                current_drafts = json.load(f)
                        else:
                            current_drafts = []
                        current_drafts.append(draft_entry)
                        
                        with open(drafts_path, "w") as f:
                            json.dump(current_drafts, f, indent=2)
                            
                        st.success("✅ Draft saved to 'data/drafts.json'!")
                        st.session_state.pop("current_draft")
                        st.rerun()

                with c2:
                    st.button("🚫 Discard", on_click=lambda: st.session_state.pop("current_draft"))

        elif action == "Chat / Ask Question":
            user_query = st.text_input("Ask about this email:")
            if user_query:
                prompt = (
                    f"You are a helpful assistant. Answer the user's question using the current email and the related history.\n\n"
                    f"--- RELATED EMAIL HISTORY ---\n{context_text}\n"
                    f"--- CURRENT EMAIL ---\n{email['body']}\n\n"
                    f"User Question: {user_query}"
                )
                with st.spinner("Analyzing context..."):
                    response = llm.generate_response(prompt)
                    st.write(response)

    st.divider()
    if st.button("⬅️ Back to Inbox"):
        st.session_state["page"] = "inbox"
        st.rerun()