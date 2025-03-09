from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select
from functions.auth import create_access_token, verify_access_token
from schemas.users import UserMe, UserAuth, UserCreate
from db import SessionDep
from models.users import User
from models.tipos_users import TipoUsuario
from fastapi.security import OAuth2PasswordBearer

router = APIRouter(prefix="/user", tags=["users"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/auth")

def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = verify_access_token(token)
    user_email: str = payload.get("sub")
    if user_email is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return user_email

@router.get("/me", response_model=UserMe, dependencies=[Depends(get_current_user)])
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.post("/auth")
async def auth_user(user_auth: UserAuth, session: SessionDep):
    user = session.exec(select(User).where(User.email == user_auth.email)).first()
    print(user)
    if not user or user.password != user_auth.password: 
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/create")
async def create_user(user: UserCreate, session: SessionDep):
    db_user = User(name=user.name, email=user.email, password=user.password, role=user.role)
    session.add(db_user)
    session.commit()
    return db_user

@router.get("/types")
async def get_user_types(session: SessionDep):
    return session.exec(select(TipoUsuario)).all()

@router.post("/types")
async def create_user_type(tipo_usuario: TipoUsuario, session: SessionDep):
    session.add(tipo_usuario)
    session.commit()
    session.refresh(tipo_usuario)
    return tipo_usuario
