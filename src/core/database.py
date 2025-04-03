from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from common.config import get_db_settings

settings = get_db_settings()

engine = create_async_engine(settings.get_async_db_url())
session_ = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
