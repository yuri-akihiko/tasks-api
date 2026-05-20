import json
from pathlib import Path
from fastapi import HTTPException
from sqlmodel import Session, select

from models.task_model import Task

try:
    from ..schemas.task_schema import TaskCreate, TaskUpdate
except ImportError:
    from schemas.task_schema import TaskCreate, TaskUpdate


TASKS_FILE = Path(__file__).resolve().parents[1] / "tasks.json"

class TaskServices:
    @staticmethod
    async def get_tasks(session: Session,
                        owner: str | None = None,
                        status: str | None = None,
                        skip: int = 0,
                        limit: int | None = None):
        declaracao = select(Task)
        if owner is not None:
            declaracao = declaracao.where(Task.owner.contains(owner))
        if status is not None:
            declaracao = declaracao.where(Task.status == status.lower())

        declaracao = declaracao.offset(skip)
        if limit is not None:
            declaracao = declaracao.limit(limit)

        return session.exec(declaracao).all()

    # use essa doc como exemplo para fazer a criação no banco(https://fastapi.tiangolo.com/tutorial/sql-databases/#read-one-hero) 
    @staticmethod
    async def get_tasks_by_id(session: Session, id: int):
        task = session.get(Task, id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        return task
        
        

    # use essa doc como exemplo para fazer a criação no banco(https://fastapi.tiangolo.com/tutorial/sql-databases/#create-a-hero) 
    @staticmethod
    async def create_task(session: Session, task: TaskCreate)-> Task:
        new_task = Task(**task.model_dump(mode="json")) 
        session.add(new_task)
        session.commit()
        session.refresh(new_task)
        return new_task

    # use essa doc como exemplo para fazer a criação no banco(https://fastapi.tiangolo.com/tutorial/sql-databases/#delete-a-hero) 
    @staticmethod
    async def delete_task(session: Session, id: int):
        task = session.get(task,_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        session.delete(task)
        session.commit()
        return {"ok": True}

    #use essa doc como exemplo para fazer a criação no banco(https://fastapi.tiangolo.com/tutorial/sql-databases/#update-a-hero-with-heroupdate)
    @staticmethod
    async def update_task(session: Session, Task: TaskUpdate )-> Task:
        task_db = session.get(Task, task_db)
        if not task_db:
            raise HTTPException(status_code=404, detail="Task not found")
        task_data = Task.model_dump(exclude_unset=True)
        task_db.sqlmodel_update(task_data)
        session.add(task_db)
        session.commit()
        session.refresh(task_db)
        return task_db
        
        
    
    @staticmethod
    async def ler_arquivo_json():
        with TASKS_FILE.open(encoding="utf-8") as f:
            dados = json.load(f)
        return dados