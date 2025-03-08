from sqlmodel import Field, SQLModel
from typing import Optional

class TipoUsuario(SQLModel, table=True):
    tipoId: Optional[int] = Field(default=None, primary_key=True)
    descripcion: str
    abbrev: str
    status: bool