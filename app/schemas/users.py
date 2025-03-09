from sqlmodel import SQLModel


class UserMe(SQLModel):
    id: str
    name: str
    role: int

class UserSearch(SQLModel):
    id: str

class UserAuth(SQLModel):
    email: str
    password: str

class UserCreate(SQLModel):
    email: str
    password: str

