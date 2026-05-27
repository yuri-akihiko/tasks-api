from sqlalchemy import Column, Integer
from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    __tablename__ = "app_user"

    id: int | None = Field(
        default=None,
        sa_column=Column(Integer, primary_key=True, autoincrement=True),
    )
    username: str = Field(index=True, unique=True)
    full_name: str | None = None
    email: str | None = Field(default=None, index=True)
    hashed_password: str
    disabled: bool = False
