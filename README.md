# Quiz dos Professores

Jogo de perguntas e respostas estilo quiz com visual pixel art, desenvolvido em Godot 4 e FastAPI.

## 🚀 Estrutura do Projeto

- `backend/`: API desenvolvida com FastAPI e integração ao Supabase.
- `jogo/`: Projeto Godot 4 (GDScript).
- `docs/`: Documentação detalhada do projeto.

## 🛠️ Como Executar o Backend Localmente

1. Entre na pasta `backend/`.
2. Configure o arquivo `.env` (use o `.env.example` como base):
   - `SUPABASE_URL`: URL do seu projeto Supabase.
   - `SUPABASE_KEY`: Anon Key do Supabase.
   - `SUPABASE_JWT_SECRET`: JWT Secret do projeto (necessário para validar tokens).
3. Certifique-se de ter o Docker e Docker Compose instalados.
4. Execute:
   ```bash
   docker compose up --build
   ```
5. A API estará disponível em `http://localhost:8000`.

## 🎮 Como Executar o Jogo (Desenvolvimento)

1. Abra o arquivo `jogo/project.godot` no Godot Editor (versão 4.2+).
2. Pressione **F5** para iniciar.

## 📦 Como fazer o Build do Executável (.exe)

1. No Godot, vá em `Project` -> `Export`.
2. Adicione uma configuração para `Windows Desktop`.
3. Certifique-se de ter os templates de exportação instalados.
4. Defina o arquivo de saída (ex: `QuizProfessores.exe`).
5. Clique em `Export Project`.

## 📄 Documentação

Consulte a pasta `docs/` para detalhes técnicos:
- [Arquitetura](docs/architecture.md)
- [Regras de Negócio](docs/business-rules.md)
- [API](docs/api.md)
- [Segurança](docs/security.md)
