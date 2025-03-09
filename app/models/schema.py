from sqlalchemy import Column, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db import Base
import datetime
import uuid

def generate_uuid():
    return str(uuid.uuid4())

class User(Base):
    __tablename__ = 'users'

    idCli = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    createdAt = Column(DateTime, default=datetime.datetime.utcnow)

    transactions = relationship("Transaction", back_populates="user", cascade="all, delete-orphan")

class Transaction(Base):
    __tablename__ = 'transactions'

    idTrx = Column(String, primary_key=True, default=generate_uuid)
    idCli = Column(String, ForeignKey('users.idCli'), nullable=False)
    dateTrx = Column(String, nullable=False)
    detailsTrx = Column(String, nullable=True)
    amount = Column(Float, nullable=False)
    pointOfSale = Column(String, nullable=True)
    state = Column(String, nullable=False)
    QRcode = Column(String, nullable=True)
    internalReference = Column(String, nullable=True)

    user = relationship("User", back_populates="transactions")
    payment_statuses = relationship("PaymentStatus", back_populates="transaction", cascade="all, delete-orphan")

class PaymentStatus(Base):
    __tablename__ = 'payment_status'

    statusId = Column(String, primary_key=True, default=generate_uuid)
    idTrx = Column(String, ForeignKey('transactions.idTrx'), nullable=False)
    status = Column(String, nullable=False)
    lastUpdated = Column(DateTime, default=datetime.datetime.utcnow)

    transaction = relationship("Transaction", back_populates="payment_statuses") 