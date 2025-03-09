from sqlmodel import SQLModel


class UserMe(SQLModel):
    id: str

class UserAuth(SQLModel):
    email: str
    password: str

class UserCreate(SQLModel):
    email: str
    password: str
