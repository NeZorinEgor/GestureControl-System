from typing import Annotated

from sqlalchemy.orm import DeclarativeBase

from src.config import settings
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import String
from sqlalchemy.orm import registry

async_engine = create_async_engine(
    url=settings.get_async_mysql_url,
    echo=True
)

async_session_factory = async_sessionmaker(
    async_engine,
    expire_on_commit=False
)


# Dependency
# db_session: AsyncSession = Depends(get_session)
async def get_session():
    async with async_session_factory() as session:
        yield session


# mysql varchar length
str_30 = Annotated[str, 30]
str_50 = Annotated[str, 50]


class Base(DeclarativeBase):
    registry = registry(
        type_annotation_map={
            str_30: String(30),
            str_50: String(50),
        }
    )