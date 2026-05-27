# routes/task_routes.py — versão protegida
from fastapi import APIRouter, Depends
from sqlmodel import Session
from database import get_session
from controllers.task_controller import TaskController
from schemas.task_schema import TaskCreate, TaskUpdate
from security import get_current_user
from models.user_model import User

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.get("/")
async def tasks(
    owner: str | None = None,
    status: str | None = None,
    skip: int = 0,
    limit: int | None = None,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    return await TaskController.get_tasks(session, owner, status, skip, limit)

@router.get("/{id}")
async def tasks_id(id: int, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    return await TaskController.get_tasks_by_id(session, id)

@router.post("/", status_code=201)
async def create_task(
    task: TaskCreate, 
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    task.owner = current_user.username
    return await TaskController.create_task(session, task)

@router.put("/{id}")
async def update_task(id: int, task: TaskUpdate, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    return await TaskController.update_task(session, id, task)

@router.delete("/{id}")
async def delete_task(id: int, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    return await TaskController.delete_task(session, id)
