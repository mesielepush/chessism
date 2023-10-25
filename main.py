import os
from dotenv import load_dotenv

load_dotenv()
CONN_STRING = os.getenv("CONN_STRING")
print(CONN_STRING)
from fastapi import FastAPI
from database.database.engine import init_db
from database.routers import players, games

app = FastAPI() 

@app.on_event("startup")
async def startup_event():
    init_db(CONN_STRING)

@app.get("/")
def read_root():
    return "Download server running."

app.include_router(players.router)
app.include_router(games.router)