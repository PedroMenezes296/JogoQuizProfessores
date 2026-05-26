from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.core.supabase import supabase
from app.schemas.cadeiras import Cadeira, Pergunta, PerguntaBase, PerguntaUpdate
from app.schemas.auth import UserProfile
from app.routers.auth import get_current_user

router = APIRouter(prefix="/cadeiras", tags=["cadeiras"])

# --- Endpoints de Cadeiras ---

@router.get("/", response_model=List[Cadeira])
async def listar_cadeiras():
    response = supabase.table("cadeiras").select("*").execute()
    return response.data

@router.get("/{cadeira_id}/perguntas", response_model=List[Pergunta])
async def listar_perguntas_cadeira(cadeira_id: int):
    # Retorna apenas perguntas ativas para o jogo
    response = supabase.table("perguntas")\
        .select("*")\
        .eq("cadeira_id", cadeira_id)\
        .eq("ativa", True)\
        .execute()
    return response.data

# --- Endpoints de Gestão de Perguntas (Professor/Admin) ---

@router.post("/{cadeira_id}/perguntas", response_model=Pergunta, status_code=status.HTTP_201_CREATED)
async def criar_pergunta(
    cadeira_id: int, 
    pergunta: PerguntaBase,
    current_user: UserProfile = Depends(get_current_user)
):
    if current_user.role not in ["admin", "professor"]:
        raise HTTPException(status_code=403, detail="Acesso negado")
    
    if current_user.role == "professor":
        cadeira_res = supabase.table("cadeiras").select("professor_id").eq("id", cadeira_id).single().execute()
        if not cadeira_res.data or cadeira_res.data["professor_id"] != current_user.id:
            raise HTTPException(status_code=403, detail="Você não é o professor desta cadeira")

    data = pergunta.dict()
    data["cadeira_id"] = cadeira_id
    
    response = supabase.table("perguntas").insert(data).execute()
    return response.data[0]

@router.put("/perguntas/{pergunta_id}", response_model=Pergunta)
async def editar_pergunta(
    pergunta_id: int,
    pergunta_update: PerguntaUpdate,
    current_user: UserProfile = Depends(get_current_user)
):
    # Busca a pergunta para saber a qual cadeira pertence
    pergunta_res = supabase.table("perguntas").select("cadeira_id").eq("id", pergunta_id).single().execute()
    if not pergunta_res.data:
        raise HTTPException(status_code=404, detail="Pergunta não encontrada")
    
    cadeira_id = pergunta_res.data["cadeira_id"]

    if current_user.role not in ["admin", "professor"]:
        raise HTTPException(status_code=403, detail="Acesso negado")
    
    if current_user.role == "professor":
        cadeira_res = supabase.table("cadeiras").select("professor_id").eq("id", cadeira_id).single().execute()
        if not cadeira_res.data or cadeira_res.data["professor_id"] != current_user.id:
            raise HTTPException(status_code=403, detail="Você não é o professor desta cadeira")

    update_data = {k: v for k, v in pergunta_update.dict().items() if v is not None}
    response = supabase.table("perguntas").update(update_data).eq("id", pergunta_id).execute()
    return response.data[0]

@router.delete("/perguntas/{pergunta_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remover_pergunta(
    pergunta_id: int,
    current_user: UserProfile = Depends(get_current_user)
):
    pergunta_res = supabase.table("perguntas").select("cadeira_id").eq("id", pergunta_id).single().execute()
    if not pergunta_res.data:
        raise HTTPException(status_code=404, detail="Pergunta não encontrada")
    
    cadeira_id = pergunta_res.data["cadeira_id"]

    if current_user.role not in ["admin", "professor"]:
        raise HTTPException(status_code=403, detail="Acesso negado")
    
    if current_user.role == "professor":
        cadeira_res = supabase.table("cadeiras").select("professor_id").eq("id", cadeira_id).single().execute()
        if not cadeira_res.data or cadeira_res.data["professor_id"] != current_user.id:
            raise HTTPException(status_code=403, detail="Você não é o professor desta cadeira")

    # Soft delete (apenas marca como inativa) conforme GEMINI.md ou delete real?
    # O GEMINI.md diz "Perguntas podem ser marcadas como inativas (soft delete) sem serem removidas do banco"
    # Mas a rota DELETE sugere remoção. Vamos seguir o soft delete para segurança.
    supabase.table("perguntas").update({"ativa": False}).eq("id", pergunta_id).execute()
    return None
