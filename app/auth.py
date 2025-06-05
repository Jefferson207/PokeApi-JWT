from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from datetime import datetime, timedelta

router = APIRouter()

SECRET_KEY = "secreto-super-seguro"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 5

users_db = {
    "usuario1": "password1",
    "usuario2": "password2"
}

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if form_data.username not in users_db or users_db[form_data.username] != form_data.password:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {
        "sub": form_data.username,
        "exp": int(expire.timestamp())
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": token, "token_type": "bearer"}
