from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# Pydantic model for Task
class Task(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    completed: bool = False

# In-memory storage for tasks
tasks = []

@app.post("/tasks/", response_model=Task)
async def create_task(task: Task):
    # Check if task with same ID already exists
    for existing_task in tasks:
        if existing_task.id == task.id:
            raise HTTPException(status_code=400, detail="Task ID already exists")
    tasks.append(task)
    return task

@app.get("/tasks/", response_model=List[Task])
async def get_tasks():
    return tasks

@app.get("/tasks/{task_id}", response_model=Task)
async def get_task(task_id: int):
    for task in tasks:
        if task.id == task_id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")

@app.put("/tasks/{task_id}", response_model=Task)
async def update_task(task_id: int, updated_task: Task):
    for index, task in enumerate(tasks):
        if task.id == task_id:
            tasks[index] = updated_task
            return updated_task
    raise HTTPException(status_code=404, detail="Task not found")

@app.delete("/tasks/{task_id}", response_model=Task)
async def delete_task(task_id: int):
    for index, task in enumerate(tasks):
        if task.id == task_id:
            deleted_task = tasks.pop(index)
            return deleted_task
    raise HTTPException(status_code=404, detail="Task not found")

