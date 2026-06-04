from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from src.models.BaseMixing import BaseMixing
from src.models.conversation import Conversation

class ChatSession(BaseMixing):
    __tablename__ = "chat_session"

    user_id: Mapped[str] = mapped_column(
        String
    )
    session_title: Mapped[str] = mapped_column(
        String(60)
    )
    session_summary: Mapped[str] = mapped_column(
        String
    )
    conversations : Mapped[list[Conversation]] = relationship(
        back_populates= "chat_session",
        cascade="all, delete-orphan"
    )