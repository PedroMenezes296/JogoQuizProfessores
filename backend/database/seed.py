import os
from supabase import create_client

# Configurações do Supabase (ajustar conforme seu .env)
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    print("Erro: SUPABASE_URL e SUPABASE_KEY devem estar definidas.")
    exit(1)

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def seed():
    # 1. Inserir Cadeiras iniciais
    cadeiras = [
        {"nome": "Redes de Computadores", "descricao": "Fundamentos de redes, protocolos e topologias.", "cor_quadro": "#004d00"},
        {"nome": "Engenharia de Software", "descricao": "Processos, requisitos e modelagem de sistemas.", "cor_quadro": "#000080"}
    ]

    for c in cadeiras:
        # Verifica se já existe
        exists = supabase.table("cadeiras").select("id").eq("nome", c["nome"]).execute()
        if not exists.data:
            supabase.table("cadeiras").insert(c).execute()
            print(f"Cadeira '{c['nome']}' inserida.")
        else:
            print(f"Cadeira '{c['nome']}' já existe.")

if __name__ == "__main__":
    seed()
