from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.core.supabase import supabase
from app.schemas.auth import UserProfile
from app.schemas.partidas import PartidaCreate, Partida, RankingEntry
from app.routers.auth import get_current_user

router = APIRouter(prefix="/partidas", tags=["partidas"])

@router.post("/", response_model=Partida, status_code=status.HTTP_201_CREATED)
async def registrar_partida(
    partida_data: PartidaCreate,
    current_user: UserProfile = Depends(get_current_user)
):
    # Validação anti-cheat básica: tempo mínimo por pergunta (ex: 1.5 segundos)
    tempo_minimo_esperado = partida_data.total_perguntas * 1.5
    if partida_data.tempo_segundos < tempo_minimo_esperado:
        raise HTTPException(
            status_code=400, 
            detail="Tempo de partida inconsistente com o número de perguntas."
        )

    # Cálculo da pontuação (Regra de Negócio)
    # 10 pontos por acerto; bônus de velocidade: +5 pontos se responder em menos de 5 segundos (média)
    # Nota: No Godot o bônus é por pergunta, aqui faremos uma aproximação pela média de tempo 
    # ou confiaremos no cálculo enviado se mudarmos o schema. 
    # Para seguir o GEMINI.md rigorosamente, o cálculo é no cliente, mas validamos aqui.
    
    # Vamos calcular aqui para garantir integridade:
    pontos_base = partida_data.acertos * 10
    
    # Bônus simplificado no backend para validação (se tempo médio < 5s por pergunta)
    # Em uma implementação real, poderíamos receber a pontuação calculada e validar.
    tempo_medio = partida_data.tempo_segundos / partida_data.total_perguntas if partida_data.total_perguntas > 0 else 0
    bonus_velocidade = 0
    if tempo_medio < 5:
        bonus_velocidade = partida_data.acertos * 5
    
    pontuacao_total = pontos_base + bonus_velocidade

    data = {
        "usuario_id": current_user.id,
        "cadeira_id": partida_data.cadeira_id,
        "total_perguntas": partida_data.total_perguntas,
        "acertos": partida_data.acertos,
        "tempo_segundos": partida_data.tempo_segundos,
        "pontuacao_total": pontuacao_total
    }

    response = supabase.table("partidas").insert(data).execute()
    if not response.data:
        raise HTTPException(status_code=400, detail="Erro ao registrar partida")
        
    return response.data[0]

@router.get("/ranking/{cadeira_id}", response_model=List[RankingEntry])
async def obter_ranking(cadeira_id: int):
    # Busca top 10 por pontuação (maior primeiro) e tempo (menor primeiro)
    # Precisamos fazer um join com profiles para pegar o nome
    response = supabase.table("partidas")\
        .select("acertos, total_perguntas, tempo_segundos, pontuacao_total, data_partida, profiles(nome_completo)")\
        .eq("cadeira_id", cadeira_id)\
        .order("pontuacao_total", desc=True)\
        .order("tempo_segundos", desc=False)\
        .limit(10)\
        .execute()
    
    ranking = []
    for item in response.data:
        ranking.append({
            "nome_completo": item["profiles"]["nome_completo"],
            "acertos": item["acertos"],
            "total_perguntas": item["total_perguntas"],
            "tempo_segundos": item["tempo_segundos"],
            "pontuacao_total": item["pontuacao_total"],
            "data_partida": item["data_partida"]
        })
        
    return ranking
