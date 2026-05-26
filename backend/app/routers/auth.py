from fastapi import APIRouter, Depends, HTTPException, status, Header, Request
from app.schemas.auth import UserCreate, UserLogin, Token, UserProfile
from app.core.supabase import supabase
from app.core.config import get_settings
from slowapi import Limiter
from slowapi.util import get_remote_address
import jose.jwt as jwt
from typing import Optional

from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

router = APIRouter(prefix="/auth", tags=["auth"])
settings = get_settings()

async def get_current_user(authorization: Optional[str] = Header(None)) -> UserProfile:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token de autenticação ausente ou inválido",
        )
    
    token = authorization.split(" ")[1]
    try:
        # No Supabase, validamos o token JWT usando o segredo do projeto
        payload = jwt.decode(token, settings.SUPABASE_JWT_SECRET, algorithms=["HS256"], audience="authenticated")
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")
        
        # Busca perfil complementar no banco
        response = supabase.table("profiles").select("*").eq("id", user_id).single().execute()
        if not response.data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Perfil não encontrado")
            
        return UserProfile(**response.data)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Erro na autenticação: {str(e)}")

@router.post("/cadastro", response_model=UserProfile, status_code=status.HTTP_201_CREATED)
@limiter.limit("5/minute")
async def cadastro(request: Request, user_data: UserCreate):
    try:
        # 1. Criar usuário no Auth do Supabase
        auth_response = supabase.auth.sign_up({
            "email": user_data.email_institucional,
            "password": user_data.senha,
            "options": {
                "data": {
                    "nome_completo": user_data.nome_completo
                }
            }
        })
        
        if not auth_response.user:
            raise HTTPException(status_code=400, detail="Erro ao criar usuário no Auth")

        # 2. Criar perfil na tabela profiles (via trigger no banco seria melhor, mas aqui faremos via código para controle)
        profile_data = {
            "id": auth_response.user.id,
            "nome_completo": user_data.nome_completo,
            "email_institucional": user_data.email_institucional,
            "matricula": user_data.matricula,
            "role": "aluno" # Default
        }
        
        profile_response = supabase.table("profiles").insert(profile_data).execute()
        
        return UserProfile(**profile_response.data[0])
    except Exception as e:
        # No caso de erro, o ideal seria fazer rollback do auth.user, mas o SDK simplificado não facilita isso.
        # Por isso em produção usamos Triggers de SQL no Supabase.
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login", response_model=Token)
@limiter.limit("10/minute")
async def login(request: Request, credentials: UserLogin):
    try:
        auth_response = supabase.auth.sign_in_with_password({
            "email": credentials.email_institucional,
            "password": credentials.senha
        })
        
        if not auth_response.session:
            raise HTTPException(status_code=401, detail="Credenciais inválidas")

        # Busca perfil para retornar junto com o token
        profile_response = supabase.table("profiles").select("*").eq("id", auth_response.user.id).single().execute()
        
        return {
            "access_token": auth_response.session.access_token,
            "token_type": "bearer",
            "user": UserProfile(**profile_response.data)
        }
    except Exception as e:
        raise HTTPException(status_code=401, detail="Email ou senha incorretos")

@router.get("/perfil", response_model=UserProfile)
async def get_perfil(current_user: UserProfile = Depends(get_current_user)):
    return current_user
