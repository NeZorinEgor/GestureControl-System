from typing import List

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ARRAY, Boolean

from src.database import Base, str_50


class FingerModel(Base):
    __tablename__ = 'fingers'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str_50]
    fingers: Mapped[str_50]   # 0000 0001 ...
