from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base

#--config
SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./todo.db"

Base = declarative_base()

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

SessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)

#dependency
async def get_db():
    async with SessionLocal() as db:
        try:
            yield db
        finally:
            await db.close()

#--models
class Todo(Base):
    __tablename__ = "todos"
    id = Column(Integer, primary_key=True)
    title = Column(String, index=True)
    description = Column(String, nullable=True)
    tododate = Column(DateTime, nullable=True)
    completed = Column(Boolean, default=False)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)