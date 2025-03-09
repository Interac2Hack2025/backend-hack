from sqlmodel import Field, SQLModel
from typing import Optional


# {
#   "pointOfSale": "4121565",      // Point of sale identifier
#   "qrType": "dynamic",           // Type of QR code (dynamic in this case)
#   "amount": 5.19,                // Transaction amount
#   "detail": "test postman GEO",  // Description of the transaction
#   "internalTransactionReference": "IXWAHROMYSCEZWQ", // Your internal reference ID
#   "format": "2"                  // QR format version
# }

class QR(SQLModel, table=True):
    qr: str = Field(default=None, primary_key=True)
    transaction_id: int = Field(default=None, primary_key=True)
    payment_url: str = Field(default=None)
    status: int = Field(default=None, ge=1, le=3) 