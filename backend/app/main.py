from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from app.routers import auth, cadeiras, admin, partidas

from app.routers.auth import limiter
app = FastAPI(title="Quiz dos Professores API")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Configuração de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Ajustar para o build final do Godot
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(cadeiras.router)
app.include_router(admin.router)
app.include_router(partidas.router)

@app.get("/")
async def root():
    return {"message": "Bem-vindo à API do Quiz dos Professores", "status": "online"}
