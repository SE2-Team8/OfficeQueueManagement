from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# from app.core.database import engine, Base # currently makes the program crash

# import feature's routers
from app.features.tickets.router import router as tickets_router
from app.features.counters.router import router as counters_router

# create db tab
# Base.metadata.create_all(bind=engine)

app = FastAPI(title="Office Queue Management API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# register single feature's router
app.include_router(tickets_router)
app.include_router(counters_router)