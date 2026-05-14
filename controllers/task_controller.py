
from sqlmodel import Session


try:
    from ..services.task_services import TaskServices
except ImportError:
    from services.task_services import TaskServices

try:
    from ..schemas.task_schema import TaskCreate, TaskUpdate
except ImportError:
    from schemas.task_schema import TaskCreate, TaskUpdate
    
class TaskController:
    @staticmethod
    async def get_tasks(session: Session,
                        owner: str | None = None,
                        status: str | None = None,
                        skip: int = 0,
                        limit: int | None = None):
        return await TaskServices.get_tasks(session, owner, status, skip, limit)

    @staticmethod
    async def get_tasks_by_id(session: Session,id: int):
        return await TaskServices.get_tasks_by_id(session,id)

    @staticmethod
    async def create_task(task: TaskCreate):
        return await TaskServices.create_task(task)

    @staticmethod
    async def delete_task(id: int):
        return await TaskServices.delete_task(id)

    @staticmethod
    async def update_task(id: int, task: TaskUpdate):
        return await TaskServices.update_task(id, task)
