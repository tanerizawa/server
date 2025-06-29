from sqlalchemy.orm import Session
from app import crud, models
import logging
from typing import Dict
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ProfileAnalyzerService:
    def analyze_and_update_profile(self, db: Session, user: models.User):
        try:
            logger.info(f"[PROFILE] Starting analysis for user_id: {user.id}")

            all_journals = crud.journal.get_multi_by_owner(db=db, owner_id=user.id, limit=1000)

            if not all_journals:
                logger.info(f"[PROFILE] No journals found for user_id: {user.id}. Skipping.")
                return

            mood_counts: Dict[str, int] = {}
            for journal in all_journals:
                if journal.mood:
                    mood_counts[journal.mood] = mood_counts.get(journal.mood, 0) + 1

            if not mood_counts:
                logger.info(f"[PROFILE] No valid mood data for user_id: {user.id}.")
                return

            total = sum(mood_counts.values())
            themes = {mood: count / total for mood, count in mood_counts.items()}
            logger.info(f"[PROFILE] Computed themes for user_id {user.id}: {themes}")

            sorted_journals = sorted(all_journals, key=lambda j: j.created_at, reverse=True)
            recent_mood = sorted_journals[0].mood.lower() if sorted_journals[0].mood else ""

            sentiment_trend = "stabil"
            if recent_mood in {"happy", "good", "great"}:
                sentiment_trend = "meningkat"
            elif recent_mood in {"sad", "bad", "angry"}:
                sentiment_trend = "menurun"

            profile = crud.user_profile.get_by_user_id(db, user_id=user.id)
            update_data = {
                "emerging_themes": themes,  # or json.dumps(themes) if not using JSONField
                "sentiment_trend": sentiment_trend,
            }

            if profile:
                logger.info(f"[PROFILE] Updating profile for user_id: {user.id}")
                crud.user_profile.update(db, db_obj=profile, obj_in=update_data)
            else:
                logger.info(f"[PROFILE] Creating new profile for user_id: {user.id}")
                new_profile = models.UserProfile(user_id=user.id, **update_data)
                db.add(new_profile)
                db.commit()
                db.refresh(new_profile)

            logger.info(f"[PROFILE] Analysis complete for user_id: {user.id}")

        except Exception as e:
            logger.error(f"[PROFILE] Error during analysis for user_id: {user.id} - {str(e)}")


profile_analyzer = ProfileAnalyzerService()
