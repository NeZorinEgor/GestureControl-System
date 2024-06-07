from typing import List

from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base, str_50


class ActionsModel(Base):
    __tablename__ = 'actions'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str_50]
    path_to_file: Mapped[str_50]   # 0000 0001 ...
    descriptions: Mapped[str_50]