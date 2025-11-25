import json
import os
from src.llm.llm_client import LLMClient

class EmailProcessor:
    def __init__(self):
        # Paths
        self.inbox_path = os.path.join("data", "mock_inbox.json")
        self.prompts_path = os.path.join("data", "prompt_templates.json")
        self.processed_path = os.path.join("data", "processed_inbox.json")
        
        # Initialize AI
        self.llm = LLMClient()
        
        # Load Data
        self.emails = self._load_json(self.inbox_path)
        self.prompts = self._load_json(self.prompts_path)

    def _load_json(self, path):
        """Helper to safely load JSON data."""
        if not os.path.exists(path):
            return [] if "inbox" in path else {}
        with open(path, "r") as f:
            return json.load(f)

    def save_results(self):
        """Saves the enriched emails to a new file."""
        with open(self.processed_path, "w") as f:
            json.dump(self.emails, f, indent=2)
        print(f"✅ Saved processed data to {self.processed_path}")

    def process_inbox(self):
        """
        The Main Engine: Loops through emails and applies AI.
        """
        print(f"🚀 Starting Batch Processing for {len(self.emails)} emails...")
        
        for i, email in enumerate(self.emails):
            # OPTIMIZATION: Skip if already processed
            if "category" in email and "action_items" in email:
                print(f"⏩ Skipping Email {email['id']} (Already processed)")
                continue

            print(f"⚡ Processing Email {i+1}/{len(self.emails)}: {email['subject'][:30]}...")

            # 1. Run Categorization
            try:
                # FIX: Use .replace() instead of .format() to avoid crashing on JSON braces
                raw_template = self.prompts["categorize_email"]["template"]
                # Check if template is valid string
                if not isinstance(raw_template, str):
                    raw_template = str(raw_template)

                cat_prompt = raw_template.replace("{subject}", email["subject"])\
                                         .replace("{sender}", email["sender"])\
                                         .replace("{body}", email["body"])
                
                cat_result = self.llm.generate_structured_response(cat_prompt)
                
                # Merge results into the email object
                email["category"] = cat_result.get("category", "Uncategorized")
                email["confidence_score"] = cat_result.get("confidence_score", 0.0)
                email["reasoning"] = cat_result.get("reasoning", "No reasoning provided.")
                
            except Exception as e:
                print(f"❌ Error categorizing email {email['id']}: {e}")
                email["category"] = "Error"

            # 2. Run Action Item Extraction
            try:
                # FIX: Use .replace() here too
                raw_template = self.prompts["extract_action_items"]["template"]
                if not isinstance(raw_template, str):
                    raw_template = str(raw_template)
                    
                action_prompt = raw_template.replace("{body}", email["body"])
                
                action_result = self.llm.generate_structured_response(action_prompt)
                
                email["action_items"] = action_result.get("action_items", [])
                
            except Exception as e:
                print(f"❌ Error extracting actions for {email['id']}: {e}")
                email["action_items"] = []

        # Final Save
        self.save_results()
        print("🎉 Processing Complete!")

if __name__ == "__main__":
    processor = EmailProcessor()
    processor.process_inbox()