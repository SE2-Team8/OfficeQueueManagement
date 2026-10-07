from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# from app.core.database import engine, Base # currently makes the program crash

# Importa i router delle feature
from app.features.tickets.router import router as tickets_router

# Crea le tabelle nel database
# Base.metadata.create_all(bind=engine)

app = FastAPI(title="Office Queue Management API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrazione dei router delle singole feature
app.include_router(tickets_router)