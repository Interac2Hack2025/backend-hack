from sqlmodel import Relationship, SQLModel, Field
from typing import Optional
from models.tipos_users import TipoUsuario

class User(SQLModel, table=True):
    id: str = Field(primary_key=True)
    email: str
    password: str
    tipo_user_id: Optional[int] = Field(default=None, foreign_key="tipousuario.tipoId")
    tipoUser: Optional[TipoUsuario] = Relationship()