from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime
from models.users import User

class TransactionStatus(SQLModel, table=True):
    id: str = Field(primary_key=True)
    status: str
    created_at: datetime = Field(default=datetime.now())

class TransactionType(SQLModel, table=True):
    id: str = Field(primary_key=True)
    description: str
    created_at: datetime = Field(default=datetime.now())

class Transaction(SQLModel, table=True):
    idTrx: str = Field(default=None, primary_key=True)
    idUser: str = Field(foreign_key="user.id")
    user: User = Relationship()
    detailsTrx: str
    amount: float
    idType: str = Field(foreign_key="transactiontype.id")
    type: TransactionType = Relationship()
    idStatus: str = Field(foreign_key="transactionstatus.id")
    transaction_status: TransactionStatus = Relationship()
    created_at: datetime = Field(default=datetime.now())
    updated_at: datetime = Field(default=datetime.now())
