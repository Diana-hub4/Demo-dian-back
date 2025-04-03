from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from ..schemas.auth_schemas import Token
from ..services.auth_service import authenticate_user
from ..utils.security import create_access_token
from datetime import timedelta

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login")
async def login(request: LoginRequest):
    if request.username == "admin" and request.password == "1234":
        return JSONResponse(content={"message": "Login exitoso", "redirect": "/portal-contador"}, status_code=200)
    raise HTTPException(status_code=401, detail="Credenciales inválidas")