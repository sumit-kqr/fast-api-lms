from datetime import datetime
from sqlmodel import SQLModel, Field

class Timestamp(SQLModel):
    """
    Mixin for timestamp fields. Adds created_at and updated_at fields to models.
    Automatically sets the current UTC time when a record is created or updated.
    """
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)