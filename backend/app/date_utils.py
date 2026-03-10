"""Date Utility functions for PromptLab"""

from datetime import datetime


def update_timestamp(entity, field_name="updated_at"):
    setattr(entity, field_name, get_current_time())


def get_current_time() -> datetime:
    return datetime.utcnow()