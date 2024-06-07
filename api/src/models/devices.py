from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base, str_50


class DevicesModel(Base):
    __tablename__ = 'devices'

    id: Mapped[int] = mapped_column(primary_key=True)
    mac_addr: Mapped[str_50]
    descriptions: Mapped[str_50]   # 0000 0001 ...
