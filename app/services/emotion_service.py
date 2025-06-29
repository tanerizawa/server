from typing import Set

class EmotionService:
    """Simple rule-based emotion classifier."""

    POSITIVE_WORDS: Set[str] = {
        "happy", "glad", "good", "great", "excited", "love", "wonderful", "awesome",
    }
    NEGATIVE_WORDS: Set[str] = {
        "sad", "unhappy", "bad", "terrible", "angry", "upset", "hate", "depressing",
    }

    def detect_emotion(self, text: str) -> str:
        """Return 'positive', 'negative' or 'neutral' based on keywords."""
        text_lower = text.lower()
        if any(word in text_lower for word in self.POSITIVE_WORDS):
            return "positive"
        if any(word in text_lower for word in self.NEGATIVE_WORDS):
            return "negative"
        return "neutral"
