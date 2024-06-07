from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base

class FingersActionsModel(Base):
    __tablename__ = 'devices'

    __table_args__ = {'extend_existing': True}

    id: Mapped[int] = mapped_column(primary_key=True)
    finger_id: Mapped[int] = mapped_column(
        ForeignKey('fingers.id', ondelete='CASCADE'))
    action_id: Mapped[int] = mapped_column(
        ForeignKey('actions.id', ondelete='CASCADE'))
