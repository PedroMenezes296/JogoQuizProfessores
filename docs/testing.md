# Estratégia de Testes - Quiz dos Professores

## Backend (FastAPI)
- **Ferramentas:** `pytest`, `httpx`.
- **Estratégia:** Testes de integração por endpoint, validando sucesso e casos de erro (401, 403, 422).
- **Como rodar:**
  ```bash
  cd backend
  pytest
  ```

## Cliente (Godot)
- **Estratégia:** Testes manuais do fluxo de gameplay e validação visual de reações.
- **Ponto de Atenção:** Verificar conectividade com a API em diferentes condições de rede.
