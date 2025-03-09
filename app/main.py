from fastapi import FastAPI
from routes import users, transactions
from db import create_all_tables

app = FastAPI(lifespan=create_all_tables)

app.include_router(users.router)
app.include_router(transactions.router)