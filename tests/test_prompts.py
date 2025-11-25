import pytest
import json
import os

# Load prompts for testing
def load_prompts():
    with open(os.path.join("data", "prompt_templates.json"), "r") as f:
        return json.load(f)

def test_prompts_are_valid_json():
    """Ensures the prompt file itself isn't broken."""
    prompts = load_prompts()
    assert "categorize_email" in prompts
    assert "extract_action_items" in prompts

def test_critical_instructions_exist():
    """Ensures the prompts contain the safety instructions."""
    prompts = load_prompts()
    
    # The Categorization prompt must ask for JSON
    assert "Output strictly valid JSON" in prompts["categorize_email"]["template"]
    
    # The Reply prompt must use context (RAG)
    assert "{context}" in prompts["generate_reply"]["template"]

def test_mock_inbox_integrity():
    """Ensures the mock data has the required fields."""
    with open(os.path.join("data", "mock_inbox.json"), "r") as f:
        emails = json.load(f)
    
    assert len(emails) >= 10  # Requirement check
    for email in emails:
        assert "id" in email
        assert "body" in email