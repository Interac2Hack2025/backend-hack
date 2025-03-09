from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import users, transactions, qr_payment
from db import create_all_tables


app = FastAPI(lifespan=create_all_tables)

# Agregar middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir orígenes de todos los dominios
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos HTTP
    allow_headers=["*"],  # Permitir todos los encabezados
)

app.include_router(users.router)
app.include_router(transactions.router)
app.include_router(qr_payment.router)
