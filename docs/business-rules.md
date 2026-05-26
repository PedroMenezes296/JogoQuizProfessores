# Regras de Negócio - Quiz dos Professores

## Usuários e Roles
- **Aluno:** Pode jogar, ver regras e ranking.
- **Professor:** Além das funções de aluno, gerencia perguntas da cadeira associada.
- **Admin:** Possui acesso total, incluindo promoção de usuários e associação de professores a cadeiras.

## Partida e Pontuação
- Uma partida consiste em 10 perguntas aleatórias.
- **Tempo:** 15 segundos por pergunta.
- **Pontuação:**
    - Acerto: +10 pontos.
    - Bônus de Velocidade: +5 pontos se respondido em menos de 5 segundos.
- O ranking é ordenado por: 1º Pontuação (maior), 2º Tempo total (menor).

## Gestão de Perguntas
- Professores só podem gerenciar perguntas de sua própria cadeira.
- O sistema utiliza **Soft Delete** (as perguntas são marcadas como inativas mas permanecem no banco).
- Mínimo de 5 perguntas ativas para que uma cadeira seja jogável (flexibilizado para 1 em testes).
