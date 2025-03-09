from fastapi import APIRouter, Depends
from sqlmodel import select
from schemas.users import UserMe
from db import SessionDep
from models.users import User
from models.tipos_users import TipoUsuario

router = APIRouter(prefix="/user", tags=["users"])

@router.get("/me", response_model=User)
async def read_users_me(current_user: UserMe = Depends()):
    return current_user

@router.post("/auth")
async def auth_user(user_auth: UserAuth, session: SessionDep):
    user = session.exec(select(User).where(User.email == user_auth.email)).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return user

@router.post("/create")
async def create_user(user_create: UserCreate, session: SessionDep):
    user = User(email=user_create.email, password=user_create.password)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

@router.get("/types")
async def get_user_types(session: SessionDep):
    return session.exec(select(TipoUsuario)).all()

@router.post("/types")
async def create_user_type(tipo_usuario: TipoUsuario, session: SessionDep):
    session.add(tipo_usuario)
    session.commit()
    session.refresh(tipo_usuario)
    return tipo_usuario