from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class PartidaCreate(BaseModel):
    cadeira_id: int
    total_perguntas: int
    acertos: int
    tempo_segundos: int

class Partida(PartidaCreate):
    id: int
    usuario_id: str
    pontuacao_total: int
    data_partida: datetime

    class Config:
        from_attributes = True

class RankingEntry(BaseModel):
    nome_completo: str
    acertos: int
    total_perguntas: int
    tempo_segundos: int
    pontuacao_total: int
    data_partida: datetime
