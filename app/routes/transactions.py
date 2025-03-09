from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select
from schemas.users import UserMe
from datetime import datetime
from db import SessionDep, get_session
from models.users import User
from models.transactions import Transaction, TransactionType, TransactionStatus
from routes.users import get_current_user


router = APIRouter(prefix="/transactions", tags=["transactions"])

@router.get("/")
def get_transactions(session: SessionDep):
    return session.exec(select(Transaction)).all()

@router.post("/")
def create_transaction(transaction: Transaction, session: SessionDep):
    if isinstance(transaction.created_at, str):
        transaction.created_at = datetime.fromisoformat(transaction.created_at)
        print(type(transaction.created_at), transaction.created_at)
        print("-------------------------")
    if isinstance(transaction.updated_at, str):
        transaction.updated_at = datetime.fromisoformat(transaction.updated_at)
    session.add(transaction)
    session.commit()
    session.refresh(transaction)
    return transaction

@router.get("/{transaction_id}")
def get_transaction(transaction_id: str, session: SessionDep):
    transaction = session.get(Transaction, transaction_id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction

@router.put("/{transaction_id}")
def update_transaction(transaction_id: str, session: SessionDep, transaction_data: Transaction = Depends(get_current_user)):
    transaction = session.get(Transaction, transaction_id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    for key, value in transaction_data.dict(exclude_unset=True).items():
        setattr(transaction, key, value)
    session.add(transaction)
    session.commit()
    session.refresh(transaction)
    return transaction

@router.delete("/{transaction_id}")
def delete_transaction(transaction_id: str, session: SessionDep):
    transaction = session.get(Transaction, transaction_id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    session.delete(transaction)
    session.commit()
    return {"message": "Transaction deleted successfully"}