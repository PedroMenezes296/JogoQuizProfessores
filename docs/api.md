# Documentação da API - Quiz dos Professores

## Autenticação
- `POST /auth/cadastro`: Cria novo usuário.
- `POST /auth/login`: Autentica e retorna token JWT.
- `GET /auth/perfil`: Retorna dados do usuário logado.

## Cadeiras e Perguntas
- `GET /cadeiras/`: Lista todas as cadeiras.
- `GET /cadeiras/{id}/perguntas`: Lista perguntas ativas (jogo) ou todas (professor).
- `POST /cadeiras/{id}/perguntas`: Adiciona nova pergunta.
- `PUT /cadeiras/perguntas/{id}`: Edita pergunta.
- `DELETE /cadeiras/perguntas/{id}`: Desativa pergunta.

## Admin
- `GET /admin/usuarios`: Lista todos os usuários.
- `PATCH /admin/usuarios/{id}/role`: Altera permissões.
- `PATCH /admin/usuarios/{id}/cadeira`: Associa professor a cadeira.

## Partidas
- `POST /partidas/`: Registra resultado da partida.
- `GET /partidas/ranking/{cadeira_id}`: Retorna Top 10.
