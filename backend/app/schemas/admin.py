from pydantic import BaseModel
from typing import Optional

class UserRoleUpdate(BaseModel):
    role: str # 'aluno', 'professor', 'admin'

class UserCadeiraUpdate(BaseModel):
    cadeira_id: int
