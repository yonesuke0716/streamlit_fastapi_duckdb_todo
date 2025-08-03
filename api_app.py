from fastapi import FastAPI, HTTPException
from database import SessionLocal
from typing import List

from models import TodoModel, Todo

app = FastAPI()


# データベースセッション依存関係
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# CRUDエンドポイント
@app.get("/todos", response_model=List[Todo])
def read_todos():
    db = SessionLocal()
    try:
        todos = db.query(TodoModel).all()
        return [Todo.model_validate(todo) for todo in todos]
    finally:
        db.close()


@app.get("/todos/{todo_id}", response_model=Todo)
def read_todo(todo_id: int):
    db = SessionLocal()
    try:
        db_todo = db.query(TodoModel).filter(TodoModel.id == todo_id).first()
        if not db_todo:
            raise HTTPException(status_code=404, detail="Todo not found")
        return Todo.model_validate(db_todo)
    finally:
        db.close()


@app.post("/todos", response_model=Todo)
def create_todo(todo: Todo):
    db = SessionLocal()
    try:
        db_todo = TodoModel(
            title=todo.title,
            description=todo.description,
            completed=todo.completed,
            priority=todo.priority,
            date=todo.date,
        )
        db.add(db_todo)
        db.commit()
        db.refresh(db_todo)
        return Todo.model_validate(db_todo)
    finally:
        db.close()


@app.put("/todos/{todo_id}", response_model=Todo)
def update_todo(todo_id: int, todo: Todo):
    db = SessionLocal()
    try:
        db_todo = db.query(TodoModel).filter(TodoModel.id == todo_id).first()
        if not db_todo:
            raise HTTPException(status_code=404, detail="Todo not found")

        if todo.title is not None:
            db_todo.title = todo.title
        if todo.description is not None:
            db_todo.description = todo.description
        if todo.completed is not None:
            db_todo.completed = todo.completed
        if todo.priority is not None:
            db_todo.priority = todo.priority
        if todo.date is not None:
            db_todo.date = todo.date

        db.commit()
        db.refresh(db_todo)
        return Todo.model_validate(db_todo)
    finally:
        db.close()


@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    db = SessionLocal()
    try:
        db_todo = db.query(TodoModel).filter(TodoModel.id == todo_id).first()
        if not db_todo:
            raise HTTPException(status_code=404, detail="Todo not found")

        db.delete(db_todo)
        db.commit()
        return {"result": "success"}
    finally:
        db.close()
