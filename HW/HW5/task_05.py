import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Хранилище задач (замените на базу данных в реальном приложении)
tasks_db = []

# Модель данных для задачи
class Task(BaseModel):
    title: str
    description: str
    status: bool


# Получение списка всех задач
@app.get("/tasks", response_model=List[Task])
def get_tasks():
    return tasks_db

# Получение задачи по идентификатору
@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int):
    if task_id < len(tasks_db):
        return tasks_db[task_id]
    raise HTTPException(status_code=404, detail="Task not found")

# Добавление новой задачи
@app.post("/tasks", response_model=Task)
def create_task(task: Task):
    tasks_db.append(task)
    return task

# Обновление задачи по идентификатору
@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, task: Task):
    if task_id < len(tasks_db):
        tasks_db[task_id] = task
        return task
    raise HTTPException(status_code=404, detail="Task not found")

# Удаление задачи по идентификатору
@app.delete("/tasks/{task_id}", response_model=Task)
def delete_task(task_id: int):
    if task_id < len(tasks_db):
        deleted_task = tasks_db.pop(task_id)
        return deleted_task
    raise HTTPException(status_code=404, detail="Task not found")

if __name__ == '__main__':
    uvicorn.run(
        'task_05:app',
        host='127.0.0.1',
        port=8000,
        reload=True
    )
