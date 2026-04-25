from datetime import datetime

from sqlalchemy import Date, DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Interaction(Base):
    __tablename__ = "interactions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    representative_name: Mapped[str] = mapped_column(String(120), nullable=False)
    hcp_name: Mapped[str] = mapped_column(String(120), nullable=False, index=True)
    specialty: Mapped[str] = mapped_column(String(120), nullable=False)
    interaction_type: Mapped[str] = mapped_column(String(60), nullable=False)
    channel: Mapped[str] = mapped_column(String(60), nullable=False)
    interaction_date: Mapped[datetime] = mapped_column(Date, nullable=False)
    notes_raw: Mapped[str] = mapped_column(Text, nullable=False)
    notes_summary: Mapped[str] = mapped_column(Text, nullable=False)
    key_entities: Mapped[str] = mapped_column(Text, nullable=False, default="{}")
    products_discussed: Mapped[str] = mapped_column(Text, nullable=False, default="")
    follow_up_action: Mapped[str] = mapped_column(Text, nullable=False, default="")
    follow_up_date: Mapped[datetime | None] = mapped_column(Date, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

