from sqlmodel import SQLModel


class UserMe(SQLModel):
    email: str
    name: str
    role: int

class UserSearch(SQLModel):
    id: str

class UserAuth(SQLModel):
    username: str
    password: str

class UserCreate(SQLModel):
    email: str
    password: str
    role: str
    name: str