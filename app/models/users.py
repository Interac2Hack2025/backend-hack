import uuid
from sqlmodel import Relationship, SQLModel, Field
from typing import Optional
from models.tipos_users import TipoUsuario

class User(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str
    email: str
    password: str
    role: Optional[int] = Field(default=None, foreign_key="tipousuario.tipoId")
    tipoUser: Optional[TipoUsuario] = Relationship()