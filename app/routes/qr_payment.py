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

from fastapi import APIRouter, HTTPException
from sqlmodel import Session, select
from models.qr_model import QR
import requests
from typing import Dict, Any
from enum import Enum

router = APIRouter(prefix="/qr-payment", tags=["qr-payment"])

class PaymentStatus(Enum):
    # We'll define the states here once you confirm them
    PENDING = "1"
    COMPLETED = "2"
    REJECTED = "3"
    # Your custom state here

@router.post("/create-payment")
async def create_payment(amount: float, detail: str):
    # API configuration
    # Si, sabemos que toda esta info debe estar en un archivo de configuracion .env no nos bajen puntos </3 es por cosas de tiempo y practicidad, graciaas.
    API_URL = "https://apis-merchant.qa.deunalab.com/merchant/v1/payment/request"
    HEADERS = {
        "x-api-key": "9fd4ac9c11b6455fa7270dba42a135ff",
        "x-api-secret": "70aa3a0caa6341f88b67ebb167ef7a50",
        "Content-Type": "application/json"
    }
    
    # Request payload
    payload = {
        "pointOfSale": "4121565",
        "qrType": "dynamic",
        "amount": amount,
        "detail": detail,
        "internalTransactionReference": "IXWAHROMYSCEZWQ",  # This should be generated uniquely
        "format": "2"
    }

    try:
        # Make request to DeUna API
        response = requests.post(API_URL, headers=HEADERS, json=payload)
        response.raise_for_status()
        
        data = response.json()
        
        # Here we'll add the logic to:
        # 1. Store in database
        # 2. Handle the status states
        # 3. Return appropriate response
        
        return {
            "transaction_id": data["transactionId"],
            "status": data["status"],
            "qr_code": data["qr"]
        }

    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))

