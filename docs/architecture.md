# Arquitetura do Projeto - Quiz dos Professores

O sistema é dividido em três componentes principais:
1. **Cliente (Godot 4):** Interface do jogo, lógica de gameplay e consumo de API.
2. **Backend (FastAPI):** Middleware de regras de negócio, validação e persistência.
3. **Persistência/Auth (Supabase):** Banco de Dados PostgreSQL e serviço de autenticação JWT.

## Fluxo de Dados
`Godot` <--(JSON/REST)--> `FastAPI` <--(PostgreSQL/Auth)--> `Supabase`

## Estrutura do Jogo (Godot)
- **Autoloads:**
    - `AuthManager`: Gerencia o estado da sessão.
    - `HTTPManager`: Wrapper para requisições assíncronas.
    - `SceneManager`: Transições entre cenas.
    - `GameManager`: Lógica de estado da partida atual.
- **Cenas:** Organizadas em `scenes/` com scripts correspondentes em `scripts/`.

## Estrutura do Backend (FastAPI)
- `app/core/`: Configurações e segurança.
- `app/routers/`: Definição dos endpoints REST.
- `app/schemas/`: Modelos Pydantic para validação.
- `app/models/`: (Opcional) Modelos de dados para o Supabase.
