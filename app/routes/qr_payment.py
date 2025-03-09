# 1. Consume API DeUna
# 2. store in db (QR, transaction_id, payment_url)
# 3. return payment_url
# {
#   "pointOfSale": "4121565",      // Point of sale identifier
#   "qrType": "dynamic",           // Type of QR code (dynamic in this case)
#   "amount": 5.19,                // Transaction amount
#   "detail": "test postman GEO",  // Description of the transaction
#   "internalTransactionReference": "IXWAHROMYSCEZWQ", // Your internal reference ID
#   "format": "2"                  // QR format version
# }

from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from models.qr_model import QR
import requests
from typing import Dict, Any
from enum import Enum
from db import SessionDep
from models.transactions import Transaction


router = APIRouter(prefix="/qr-payment", tags=["qr-payment"])
class PaymentStatus(Enum):
    # We'll define the states here once you confirm them
    PENDING = "1"
    COMPLETED = "2"
    REJECTED = "3"
    # Your custom state here

async def request_payment(amount: float, detail: str) -> Dict[str, Any]:
    API_URL = "https://apis-merchant.qa.deunalab.com/merchant/v1/payment/request"
    HEADERS = {
        "x-api-key": "9fd4ac9c11b6455fa7270dba42a135ff",
        "x-api-secret": "70aa3a0caa6341f88b67ebb167ef7a50",
        "Content-Type": "application/json"
    }
    payload = {
        "pointOfSale": "4121565",
        "qrType": "dynamic",
        "amount": amount,
        "detail": detail,
        "internalTransactionReference": "IXWAHROMYSCEZWQ",  # This should be generated uniquely
        "format": "2"
    }

    response = requests.post(API_URL, headers=HEADERS, json=payload)
    response.raise_for_status()
    return response.json()


@router.post("/create-payment")
async def create_payment(amount: float, detail: str, session: SessionDep):
    try:
        data = await request_payment(amount, detail)
        transaction = session.exec(select(Transaction).where(Transaction.idTrx == data["transactionId"])).first()
        
        # Check if the transaction is None
        if transaction is not None:
            raise HTTPException(status_code=400, detail="Transaction already exists")
        else:
            qr_generated = QR(
                qr=data["qr"],
                transaction_id=data["transactionId"],
                payment_url=data.get("deeplink"),
                status=PaymentStatus.PENDING.value
            )
            # transaction = Transaction(
            #     idTrx=data["transactionId"],
            #     idUser=transaction_data.id,
            #     detailsTrx=data["detail"],
            #     amount=data["amount"],
            #     idStatus=PaymentStatus.PENDING.value,
            #     created_at=datetime.now(),
            #     updated_at=datetime.now()
            # )
            
        
        # Store the transaction in the database
        session.add(qr_generated)
        session.commit()
        session.refresh(qr_generated)

        return {
            "transaction_id": data["transactionId"],
            "status": PaymentStatus.PENDING.value,
            "payment_url": data.get("deeplink"),
            "qr_code": data["qr"]
        }

    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/check-transaction")
async def check_transaction(transaction_id: int, session: SessionDep):
    exists = check_transaction_exists(session, transaction_id)
    return {"exists": exists}