import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.services.emotion_service import EmotionService


def test_positive_detection():
    service = EmotionService()
    assert service.detect_emotion("I am very happy today!") == "positive"


def test_negative_detection():
    service = EmotionService()
    assert service.detect_emotion("This is so sad and depressing.") == "negative"


def test_neutral_detection():
    service = EmotionService()
    assert service.detect_emotion("I have a pen.") == "neutral"
