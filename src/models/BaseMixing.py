import datetime
import uuid

from src.models.Base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import func

class BaseMixing(Base):
    __abstract__ = True

    id: Mapped[str] = mapped_column(
        default=lambda : uuid.uuid4().hex,
        primary_key=True
    )

    created_at: Mapped[datetime.datetime] = mapped_column(
        server_default=func.now()
    )

    updated_at: Mapped[datetime.datetime] = mapped_column(
        server_default=func.now(),
        onupdate=func.now()
    )