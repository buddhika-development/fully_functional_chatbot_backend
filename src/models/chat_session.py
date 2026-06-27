from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from src.models.BaseMixing import BaseMixing
from src.models.conversation import Conversation
from typing import Optional

class ChatSession(BaseMixing):
    __tablename__ = "chat_session"

    user_id: Mapped[str] = mapped_column(
        String
    )
    session_title: Mapped[Optional[str]] = mapped_column(
        String(60),
        default=None
    )
    session_summary: Mapped[Optional[str]] = mapped_column(
        String,
        default= None
    )
    conversations: Mapped[list["Conversation"]] = relationship(
        back_populates="chat_session",
        cascade="all, delete-orphan"
    )
