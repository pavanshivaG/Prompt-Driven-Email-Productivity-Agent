import json
import os

class RagEngine:
    def __init__(self, emails):
        self.emails = emails

    def find_related_context(self, current_email, limit=3):
        """
        Searches for related emails based on Subject threading and Sender.
        Returns a formatted string ready for the LLM.
        """
        context_hits = []
        
        # normalize subject (remove Re:, Fwd:)
        base_subject = current_email['subject'].replace("Re:", "").replace("Fwd:", "").strip()
        
        for email in self.emails:
            # 1. Don't include the email itself
            if email['id'] == current_email['id']:
                continue
                
            # 2. Check for Thread Match (Strongest Signal)
            if base_subject in email['subject']:
                context_hits.append(email)
                continue
                
            # 3. Check for Sender Match (Secondary Signal)
            # Only if we don't have enough hits yet
            if len(context_hits) < limit and email['sender'] == current_email['sender']:
                context_hits.append(email)

        # Format the top results
        formatted_context = []
        for hit in context_hits[:limit]:
            formatted_context.append(
                f"[Date: {hit['timestamp']}] From: {hit['sender']}\nSubject: {hit['subject']}\nBody: {hit['body']}\n---"
            )
            
        return "\n".join(formatted_context) if formatted_context else "No prior context found."