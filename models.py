from sqlmodel import SQLModel, Field
from typing import Optional
from database import id_field, DATABASE_URL


class Todo(SQLModel, table=True, extend_existing=True):
    id: Optional[int] = id_field("todo", DATABASE_URL)
    title: str = Field(min_length=3, max_length=100)
    description: str = Field(min_length=3, max_length=100)
    completed: bool = Field(default=False)
    priority: int = Field(ge=0, le=6, default=1)
    date: Optional[str] = Field(default=None)
