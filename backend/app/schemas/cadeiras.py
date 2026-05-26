from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# --- Schemas para Cadeiras ---

class CadeiraBase(BaseModel):
    nome: str
    descricao: Optional[str] = None
    cor_quadro: str = "#004d00"

class CadeiraCreate(CadeiraBase):
    professor_id: Optional[str] = None

class Cadeira(CadeiraBase):
    id: int
    professor_id: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True

# --- Schemas para Perguntas ---

class PerguntaBase(BaseModel):
    enunciado: str
    opcao_a: str
    opcao_b: str
    opcao_c: str
    opcao_d: str
    resposta_correta: str # 'a', 'b', 'c', 'd'

class PerguntaCreate(PerguntaBase):
    cadeira_id: int

class Pergunta(PerguntaBase):
    id: int
    cadeira_id: int
    ativa: bool
    created_at: datetime

    class Config:
        from_attributes = True

class PerguntaUpdate(BaseModel):
    enunciado: Optional[str] = None
    opcao_a: Optional[str] = None
    opcao_b: Optional[str] = None
    opcao_c: Optional[str] = None
    opcao_d: Optional[str] = None
    resposta_correta: Optional[str] = None
    ativa: Optional[bool] = None
