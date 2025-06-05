from fastapi import FastAPI
from app.routes import router as pokemon_router
from app.auth import router as auth_router

app = FastAPI(title="PokeAPI JWT")

app.include_router(auth_router)
app.include_router(pokemon_router)
