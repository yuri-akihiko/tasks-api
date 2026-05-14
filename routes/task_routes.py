from fastapi import APIRouter, Depends
from sqlmodel import Session

from database import get_session

try:
    from ..controllers.task_controller import TaskController
    from ..schemas.task_schema import TaskCreate, TaskUpdate
except ImportError:
    from controllers.task_controller import TaskController
    from schemas.task_schema import TaskCreate, TaskUpdate

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"]
)

@router.get("/")
async def tasks(owner: str | None = None, 
                status: str | None = None, 
                skip: int = 0, limit: int | None = None,
                session: Session = Depends(get_session)):
    return await TaskController.get_tasks(session, owner, status, skip, limit)

@router.get("/{id}")
async def tasks_id(id: int, session: Session = Depends(get_session)):
    return await TaskController.get_tasks_by_id(session,id)

@router.post("/")
async def create_task(task: TaskCreate, session: Session = Depends(get_session)):
    return await TaskController.create_task(session, task)

@router.delete("/{id}")
async def delete_task(id: int):
    return await TaskController.delete_task(id)

@router.put("/{id}")
async def update_task(id: int, task: TaskUpdate):
    return await TaskController.update_task(id, task)
