import re
from typing import Dict, Any

class MultilingualAssistant:
    # Keyword dictionaries for basic multilingual intent/category routing
    KEYWORD_MAP = {
        "food": ["khana", "bhojan", "ration", "meal", "hunger", "bhookh", "உணவு", "খাবার"],
        "healthcare": ["dawai", "medicine", "doctor", "hospital", "ill", "bimar", "மருத்துவம்", "மருந்து", "স্বাস্থ্য"],
        "shelter": ["ghar", "flood", "rain", "shelter", "stay", "house", "முகாம்", "বাসস্থান"],
        "education": ["book", "school", "padhai", "student", "class", "பள்ளி", "বই"]
    }

    URGENCY_MAP = {
        "CRITICAL": ["emergency", "turant", "jaan", "critical", "severe", "உயிர்", "জরুরি"],
        "HIGH": ["jaldi", "fast", "urgent", "important", "விரைவு"],
        "MEDIUM": ["need", "help", " chahiye"]
    }

    @staticmethod
    def parse_regional_input(text: str, language_hint: str = "en") -> Dict[str, Any]:
        text_lower = text.lower()

        detected_category = "General Assistance"
        for cat, keywords in MultilingualAssistant.KEYWORD_MAP.items():
            if any(kw in text_lower for kw in keywords):
                detected_category = cat.capitalize()
                break

        detected_urgency = "MEDIUM"
        for urg, keywords in MultilingualAssistant.URGENCY_MAP.items():
            if any(kw in text_lower for kw in keywords):
                detected_urgency = urg
                break

        return {
            "original_text": text,
            "language": language_hint,
            "structured_category": detected_category,
            "structured_urgency": detected_urgency,
            "translated_summary": f"[{detected_urgency}] Request regarding {detected_category}: {text}"
        }