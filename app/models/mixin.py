from datetime import datetime, timezone
from sqlalchemy import Column, DateTime

class TimestampMixin:
    registered_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
