from src.models.BaseMixing import BaseMixing
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, JSON, ForeignKey
from typing import Any

class Conversation(BaseMixing):
    __tablename__ = "conversation"

    session_id : Mapped[str] = mapped_column(
        ForeignKey("chat_session.id")
    )

    role: Mapped[str] = mapped_column(
        String
    )

    content : Mapped[str] = mapped_column(
        String,
        default= None
    )

    additional_information : Mapped[dict[str, Any]] = mapped_column(
        JSON,
        default= None
    )

