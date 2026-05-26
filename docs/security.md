# Segurança e Qualidade - Quiz dos Professores

## Segurança
- **JWT:** Todos os endpoints protegidos validam o token assinado pelo Supabase.
- **RBAC (Role-Based Access Control):** Validação rigorosa de roles no backend para cada ação sensível.
- **Rate Limiting:** Limite de requisições em endpoints críticos (cadastro/login) via SlowAPI.
- **CORS:** Configurado para restringir origens (ajustar conforme ambiente).
- **Anti-Cheat:** Validação de tempo mínimo por partida para evitar registros falsos.

## Qualidade
- **CCN:** Complexidade ciclomática mantida baixa em scripts e rotas.
- **SZ:** Arquivos modulares e focados em uma única responsabilidade.
- **Docker:** Ambiente reprodutível para o backend.
