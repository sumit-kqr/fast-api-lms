from datetime import datetime
from sqlmodel import SQLModel, Field

class Timestamp(SQLModel):
    """Mixin for timestamp fields with created_at and updated_at."""
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)