import streamlit as st
import json
import os

# Define path relative to where main.py is run
PROMPTS_PATH = os.path.join("data", "prompt_templates.json")

def load_prompts():
    if not os.path.exists(PROMPTS_PATH):
        return {}
    with open(PROMPTS_PATH, "r") as f:
        return json.load(f)

def save_prompts(data):
    with open(PROMPTS_PATH, "w") as f:
        json.dump(data, f, indent=2)

def render_prompt_editor():
    st.title("🧠 Agent Brain (Prompt Engineering)")
    st.markdown("Configure how the AI thinks. Changes here affect the Inbox and Chat immediately.")
    
    prompts = load_prompts()
    
    if not prompts:
        st.error("⚠️ No prompts found in data/prompt_templates.json")
        return

    # Create tabs for each prompt type
    tabs = st.tabs(list(prompts.keys()))
    
    for i, (key, data) in enumerate(prompts.items()):
        with tabs[i]:
            st.subheader(f"Editing: {data.get('name', key)}")
            st.info(data.get('description', ''))
            
            # The Editor Area
            # We use key=... to ensure Streamlit treats each text area uniquely
            new_template = st.text_area(
                "Prompt Template", 
                value=data.get('template', ''), 
                height=300,
                key=f"editor_{key}"
            )
            
            col1, col2 = st.columns([1, 5])
            with col1:
                if st.button("💾 Save", key=f"save_{key}"):
                    prompts[key]['template'] = new_template
                    save_prompts(prompts)
                    st.success("Prompt updated!")
            
            with col2:
                if st.button("✨ Auto-Optimize (AI)", key=f"opt_{key}"):
                    st.toast("AI Optimization Engine would run here... (Demo Mode)")