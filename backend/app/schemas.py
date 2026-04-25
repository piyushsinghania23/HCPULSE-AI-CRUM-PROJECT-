from datetime import date, datetime
from typing import Any

from pydantic import BaseModel, Field


class InteractionBase(BaseModel):
    representative_name: str = Field(min_length=2, max_length=120)
    hcp_name: str = Field(min_length=2, max_length=120)
    specialty: str = Field(min_length=2, max_length=120)
    interaction_type: str = Field(min_length=2, max_length=60)
    channel: str = Field(min_length=2, max_length=60)
    interaction_date: date
    notes_raw: str = Field(min_length=5)
    notes_summary: str = ""
    key_entities: dict[str, Any] = Field(default_factory=dict)
    products_discussed: str = ""
    follow_up_action: str = ""
    follow_up_date: date | None = None


class InteractionCreate(InteractionBase):
    pass


class InteractionUpdate(BaseModel):
    representative_name: str | None = None
    hcp_name: str | None = None
    specialty: str | None = None
    interaction_type: str | None = None
    channel: str | None = None
    interaction_date: date | None = None
    notes_raw: str | None = None
    notes_summary: str | None = None
    key_entities: dict[str, Any] | None = None
    products_discussed: str | None = None
    follow_up_action: str | None = None
    follow_up_date: date | None = None


class InteractionRead(InteractionBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class AgentChatRequest(BaseModel):
    message: str = Field(min_length=2)
    representative_name: str | None = None
    hcp_name: str | None = None


class AgentChatResponse(BaseModel):
    response: str
    trace: list[str] = Field(default_factory=list)

