import re
from typing import Dict, Any, List
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class DataCleaningPipeline:
    @staticmethod
    def normalize_phone(phone: str) -> str:
        if not phone:
            return ""
        digits = re.sub(r'\D', '', phone)
        if len(digits) == 10:
            return f"+91{digits}" # Defaulting to India (+91) region or custom format
        return f"+{digits}" if not phone.startswith('+') else phone

    @staticmethod
    def normalize_location(location: str) -> str:
        if not location:
            return "Unknown"
        # Title case and strip extra whitespaces
        return " ".join(location.strip().title().split())

    @staticmethod
    def calculate_quality_score(data: Dict[str, Any]) -> float:
        score = 1.0
        required_fields = ["title", "description", "category", "location_name"]
        for field in required_fields:
            if not data.get(field):
                score -= 0.2
        if not data.get("latitude") or not data.get("longitude"):
            score -= 0.1
        return max(score, 0.1)

    @staticmethod
    def detect_duplicates(new_text: str, existing_texts: List[str], threshold: float = 0.75) -> bool:
        if not existing_texts:
            return False
        documents = existing_texts + [new_text]
        vectorizer = TfidfVectorizer().fit_transform(documents)
        vectors = vectorizer.toarray()

        new_vector = vectors[-1]
        existing_vectors = vectors[:-1]

        similarities = cosine_similarity([new_vector], existing_vectors)[0]
        max_sim = np.max(similarities) if len(similarities) > 0 else 0.0

        return bool(max_sim >= threshold)