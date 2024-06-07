from typing import List

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ARRAY, Boolean

from src.database import Base, str_50


class ScenariosModel(Base):
    __tablename__ = 'scenarios'

    yandex_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str_50]
