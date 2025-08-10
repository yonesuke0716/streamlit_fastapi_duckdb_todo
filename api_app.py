from fastapi import FastAPI, HTTPException, Depends
from sqlmodel import Session, select
from typing import List
import uvicorn
from models import Todo
from database import create_tables, get_session

app = FastAPI()

create_tables()


# CRUDエンドポイント
@app.get("/todos", response_model=List[Todo])
def read_todos(session: Session = Depends(get_session)):
    todos = session.exec(select(Todo)).all()
    return todos


@app.get("/todos/{todo_id}", response_model=Todo)
def read_todo(todo_id: int, session: Session = Depends(get_session)):
    todo = session.get(Todo, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


@app.post("/todos", response_model=Todo)
def create_todo(todo: Todo, session: Session = Depends(get_session)):
    session.add(todo)
    session.commit()
    session.refresh(todo)
    return todo


@app.put("/todos/{todo_id}", response_model=Todo)
def update_todo(
    todo_id: int, todo_update: Todo, session: Session = Depends(get_session)
):
    db_todo = session.get(Todo, todo_id)
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    # 更新データを適用（idは除外）
    todo_data = todo_update.model_dump(exclude={"id"}, exclude_unset=True)
    for key, value in todo_data.items():
        setattr(db_todo, key, value)

    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)
    return db_todo


@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int, session: Session = Depends(get_session)):
    db_todo = session.get(Todo, todo_id)
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    session.delete(db_todo)
    session.commit()
    return {"result": "success"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
