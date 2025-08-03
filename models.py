from sqlalchemy import Column, Integer, String, Boolean, Text
from pydantic import BaseModel, Field
from typing import Optional
from database import Base


# SQLAlchemyモデル
class TodoModel(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    completed = Column(Boolean, default=False, nullable=False)
    priority = Column(Integer, default=1, nullable=False)
    date = Column(String, nullable=True)


# Pydanticモデル
class Todo(BaseModel):
    id: Optional[int] = Field(default=None)
    title: str = Field(min_length=3, max_length=100)
    description: str = Field(min_length=3, max_length=100)
    completed: bool = Field(default=False)
    priority: int = Field(ge=0, le=6)
    date: Optional[str] = Field(default=None)

    model_config = {"from_attributes": True}
