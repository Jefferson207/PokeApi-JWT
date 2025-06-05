from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from datetime import datetime, timezone
from app.models import PokemonRequest
from app.services import fetch_pokemon_info

router = APIRouter()

oauth2_scheme = HTTPBearer()
SECRET_KEY = "secreto-super-seguro"
ALGORITHM = "HS256"

async def verificar_token(credentials: HTTPAuthorizationCredentials = Depends(oauth2_scheme)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if datetime.fromtimestamp(payload["exp"], tz=timezone.utc) < datetime.now(timezone.utc):
            raise HTTPException(status_code=401, detail="Token expirado")
        return payload  
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")


@router.post("/pokemon")
async def obtener_pokemon(data: PokemonRequest, token: dict = Depends(verificar_token)):
    return await fetch_pokemon_info(data.pokemons)

