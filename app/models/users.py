from sqlmodel import Relationship, SQLModel, Field
from typing import Optional
from models.tipos_users import TipoUsuario

class User(SQLModel, table=True):
    id: str = Field(primary_key=True)
    name: str
    email: str
    password: str
    role: Optional[int] = Field(default=None, foreign_key="tipousuario.tipoId")
    tipoUser: Optional[TipoUsuario] = Relationship()