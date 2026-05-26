from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.core.supabase import supabase
from app.schemas.auth import UserProfile
from app.schemas.admin import UserRoleUpdate, UserCadeiraUpdate
from app.routers.auth import get_current_user

router = APIRouter(prefix="/admin", tags=["admin"])

async def check_admin_role(current_user: UserProfile = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso restrito a administradores"
        )
    return current_user

@router.get("/usuarios", response_model=List[UserProfile])
async def listar_usuarios(admin: UserProfile = Depends(check_admin_role)):
    response = supabase.table("profiles").select("*").execute()
    return response.data

@router.patch("/usuarios/{usuario_id}/role", response_model=UserProfile)
async def alterar_role_usuario(
    usuario_id: str,
    role_update: UserRoleUpdate,
    admin: UserProfile = Depends(check_admin_role)
):
    if role_update.role not in ["aluno", "professor", "admin"]:
        raise HTTPException(status_code=400, detail="Role inválida")
    
    response = supabase.table("profiles").update({"role": role_update.role}).eq("id", usuario_id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    return response.data[0]

@router.patch("/usuarios/{usuario_id}/cadeira", status_code=status.HTTP_200_OK)
async def associar_professor_cadeira(
    usuario_id: str,
    cadeira_update: UserCadeiraUpdate,
    admin: UserProfile = Depends(check_admin_role)
):
    # Verifica se o usuário é um professor
    user_res = supabase.table("profiles").select("role").eq("id", usuario_id).single().execute()
    if not user_res.data or user_res.data["role"] != "professor":
        raise HTTPException(status_code=400, detail="O usuário deve ter o role 'professor' para ser associado a uma cadeira")

    # Verifica se a cadeira existe
    cadeira_res = supabase.table("cadeiras").select("id").eq("id", cadeira_update.cadeira_id).execute()
    if not cadeira_res.data:
        raise HTTPException(status_code=404, detail="Cadeira não encontrada")

    # Atualiza a cadeira com o ID do professor
    response = supabase.table("cadeiras").update({"professor_id": usuario_id}).eq("id", cadeira_update.cadeira_id).execute()
    
    return {"message": "Professor associado à cadeira com sucesso"}
