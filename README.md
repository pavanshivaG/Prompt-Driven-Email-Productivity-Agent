# 📬 MailPilot AI: Prompt-Driven Email Productivity Agent

> **Course Assignment Submission**
> **Objective:** A secure, prompt-driven agent to categorize emails, extract actions, and draft context-aware replies.

## 📖 Project Overview
MailPilot is an intelligent email assistant that transforms a standard inbox into a **Kanban-style productivity board**. It utilizes a **Prompt-Driven Architecture** where all AI behaviors (categorization rules, drafting tones, extraction logic) are controlled by user-editable prompts stored in a dedicated Knowledge Base.

### 🌟 Key Differentiators ("Rank 1" Features)
* [cite_start]**Context-Aware RAG Engine:** Unlike standard drafters, this agent searches the inbox for related threads (e.g., "Project Delta" history) to write factually accurate replies[cite: 144].
* **Safety & Confidence Scoring:** The AI assigns a "Confidence Score" to every classification. [cite_start]Low-confidence predictions are flagged with a ⚠️ warning to the user.
* [cite_start]**Kanban Visualization:** Emails are visually sorted into "Urgent", "Work", and "Spam" columns for immediate prioritization[cite: 45].

---

## [cite_start]🛠️ Setup Instructions [cite: 16]

### Prerequisites
* Python 3.8+
* An API Key for **OpenAI** (Recommended) or Google Gemini.

### Installation
1.  **Clone the Repository**
    ```bash
    git clone <repository-url>
    cd email-productivity-agent
    ```

2.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Environment Configuration**
    Create a file named `.env` in the root directory and add your API key:
    ```env
    OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxxxxx
    # OR
    GEMINI_API_KEY=AIzaSy-xxxxxxxxxxxxxxxxxxxxxxxx
    ```

---

## [cite_start]🚀 How to Run the Application [cite: 17]

To launch both the Backend Processor and the Streamlit UI, run the following command from the root directory:

```bash
streamlit run main.py
```

UI VISUALIZATION OF PROJECT 
<img width="1919" height="875" alt="image" src="https://github.com/user-attachments/assets/95208111-151b-42e7-a3ed-6a328fafc1b3" />
<img width="1892" height="858" alt="image" src="https://github.com/user-attachments/assets/278c0b38-c07c-45f0-bef7-f24bc7e91e8e" />
<img width="1900" height="856" alt="image" src="https://github.com/user-attachments/assets/440852a7-f02a-4b7a-865c-a2969ed7934c" />

