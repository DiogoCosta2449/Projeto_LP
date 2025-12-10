# Jogo do Moinho

Implementação completa em Python do **Jogo do Moinho** para a disciplina de **Linguagens de Programação - IPBeja**.

## 🎮 O Jogo

Jogo de tabuleiro 3x3 para 2 jogadores (**X** e **O**). Cada jogador tem **3 peças**.

### Fases do Jogo
1. **Fase de Colocação** (6 turnos): Jogadores alternam colocando 1 peça por vez.
2. **Fase de Movimento**: Jogadores movem peças para posições **adjacentes** (horizontal/vertical/diagonal).

### Como Ganhar
Primeiro jogador a alinhar **3 peças em linha** (horizontal ou vertical).

### Dificuldades da IA

| Nível | Estratégia |
|-------|------------|
| **facil** | Primeiro movimento disponível |
| **normal** | Minimax profundidade 1 (procura vitória imediata) |
| **dificil** | Minimax profundidade 5 + Alpha-Beta (analisa vários lances à frente) |
