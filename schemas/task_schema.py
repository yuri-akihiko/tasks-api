from pydantic import BaseModel, ConfigDict, Field
class TaskBase(BaseModel):
    title: str = Field(..., example="Fazer compras")
    description: str = Field(..., example="Comprar leite, pão e ovos")
    owner: str = Field(..., example="João")
    status: str = Field(..., example="Pendente")
    comments: list[str] = Field(default_factory=list, example=["Comentário 1", "Comentário 2"])

class TaskCreate(TaskBase):
    pass

class TaskUpdate(TaskBase):
    pass

class Task(TaskBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
