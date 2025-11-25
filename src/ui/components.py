import streamlit as st

def render_email_card(email, on_click_key):
    """
    Renders a single email card for the Kanban board.
    """
    with st.container(border=True):
        # 1. Confidence Warning (Safety Feature)
        confidence = email.get("confidence_score", 1.0)
        if confidence < 0.7:
            st.warning(f"⚠️ Low Confidence ({int(confidence*100)}%)")
        
        # 2. Sender & Subject
        st.markdown(f"**{email['sender'].split('@')[0]}**")
        st.caption(f"{email['subject']}")
        
        # 3. Tags
        if email.get("category") == "Urgent":
            st.markdown("🔴 **Urgent**")
        
        # 4. Action Items Badge
        action_count = len(email.get("action_items", []))
        if action_count > 0:
            st.info(f"✅ {action_count} Tasks")
        
        # 5. Open Button
        if st.button("Open", key=on_click_key, use_container_width=True):
            return True
    return False