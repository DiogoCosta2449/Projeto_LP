# 🎮 Jogo do Moinho - Projeto de Programação

Um jogo clássico de tabuleiro implementado em Python, onde o jogador humano enfrenta o computador com diferentes níveis de dificuldade!

## 📋 Descrição do Projeto

O **Jogo do Moinho** (Nine Men's Morris) é um jogo tradicional de tabuleiro para dois jogadores em um tabuleiro 3×3. O objetivo é alinhar três das suas peças em linha (horizontal ou vertical) antes do adversário.

### Fases do Jogo:
1. **Fase de Colocação**: Cada jogador coloca 3 peças no tabuleiro (6 turnos no total)
2. **Fase de Movimento**: Os jogadores movem as suas peças para posições adjacentes até que um consiga fazer um alinhamento de 3

## 🎯 Características

✅ **Implementação completa com TADs (Tipos de Dados Abstratos)**:
- **TAD Posição** - Gestão de coordenadas do tabuleiro (a-c, 1-3)
- **TAD Peça** - Representação das peças (X, O, espaço)
- **TAD Tabuleiro** - Matriz 3×3 com operações completas

✅ **3 Níveis de Dificuldade**:
- **Fácil**: Computador faz movimentos aleatórios simples
- **Normal**: Computador tenta vitória e bloqueia ameaças
- **Difícil**: Algoritmo Minimax com profundidade 5 e poda alpha-beta

✅ **Interface Interativa**:
- Menu de escolha de jogador e dificuldade
- Validação de movimentos
- Visualização clara do tabuleiro após cada jogada

✅ **100% de Testes Passados**:
- 25/25 testes públicos ✔️
- Cobertura completa de todas as funcionalidades

## 📦 Estrutura do Projeto

```
ProjetoCompletoPerplexity.py
├── TAD Posição (7 funções)
├── TAD Peça (5 funções)
├── TAD Tabuleiro (15 funções)
├── Funções de Movimento (8 funções)
├── Algoritmo Minimax (4 funções)
└── Função Principal: moinho()
```

## 🚀 Como Usar

### Executar o Jogo Interativo:

```bash
python3 ProjetoCompletoPerplexity.py
```

Depois segue o menu:
1. Escolhe o teu jogador (X ou O)
2. Escolhe a dificuldade (Fácil, Normal, Difícil)
3. Joga!

### Executar os Testes:

```bash
python3 public_tests.py
```

Resultado esperado: `25 / 25 (100.00% )`

## 🎮 Como Jogar

### Movimento de Colocação (Fases 1-3)
Digite a posição desejada:
```
Turno do jogador. Escolha uma posicao: b2
```

### Movimento de Movimento (Fases 4+)
Digite origem e destino juntos:
```
Turno do jogador. Escolha um movimento: a1b1
```

**Posições válidas**: a1, a2, a3, b1, b2, b3, c1, c2, c3

**Movimentos válidos**: Apenas para posições adjacentes ao tabuleiro

### Tabuleiro Visual

```
   a   b   c
1 [X]-[O]-[ ]
   | \ | / |
2 [ ]-[X]-[ ]
   | / | \ |
3 [O]-[ ]-[X]
```

## 🧠 Algoritmos Implementados

### Nível Fácil
- Escolhe o primeiro movimento possível disponível

### Nível Normal
- Verifica se pode ganhar (vitória imediata)
- Verifica se precisa bloquear (ameaça do adversário)
- Caso contrário, faz movimento aleatório simples

### Nível Difícil - Minimax
```
Análise de até 5 jogadas à frente
Uso de poda alpha-beta para otimização
Função de avaliação de posições:
  - Penaliza ameaças do adversário (-15)
  - Premia oportunidades de vitória (+10)
  - Premia vitória (+100)
  - Penaliza derrota (-100)
```

## 📊 Testes

O projeto passa todos os **25 testes públicos** incluindo:
- ✅ Validação de TADs
- ✅ Operações de tabuleiro
- ✅ Movimentos válidos
- ✅ Detecção de vitória
- ✅ Funções automáticas em 3 níveis
- ✅ Jogo completo interativo

## 📝 Exemplo de Jogo

```
===== JOGO DO MOINHO =====

Escolha o seu jogador:
1 - X (começa primeiro)
2 - O (computador começa)
Digite 1 ou 2: 1

Escolha a dificuldade:
1 - Fácil
2 - Normal
3 - Difícil
Digite 1, 2 ou 3: 2

Bem-vindo ao JOGO DO MOINHO. Nivel de dificuldade normal.
   a   b   c
1 [ ]-[ ]-[ ]
   | \ | / |
2 [ ]-[ ]-[ ]
   | / | \ |
3 [ ]-[ ]-[ ]

Turno do jogador. Escolha uma posicao: b2
   a   b   c
1 [ ]-[ ]-[ ]
   | \ | / |
2 [ ]-[X]-[ ]
   | / | \ |
3 [ ]-[ ]-[ ]

Turno do computador (normal):
   a   b   c
1 [ ]-[ ]-[ ]
   | \ | / |
2 [ ]-[X]-[O]
   | / | \ |
3 [ ]-[ ]-[ ]

... (jogo continua) ...

========== JOGO TERMINADO ==========
O vencedor foi: [X]
```

## 🔧 Funções Principais

### TAD Posição
- `cria_posicao(c, l)` - Cria uma posição
- `obter_pos_c(p)`, `obter_pos_l(p)` - Obtém coordenadas
- `posicoes_iguais(p1, p2)` - Compara posições
- `posicao_para_str(p)` - Converte para string
- `obter_posicoes_adjacentes(p)` - Retorna vizinhos

### TAD Peça
- `cria_peca(s)` - Cria uma peça (X, O ou espaço)
- `peca_para_str(j)` - Converte para string
- `peca_para_inteiro(j)` - Converte para número

### TAD Tabuleiro
- `cria_tabuleiro()` - Cria tabuleiro vazio
- `obter_peca(t, p)` - Obtém peça em posição
- `coloca_peca(t, j, p)` - Coloca peça
- `move_peca(t, p1, p2)` - Move peça
- `obter_ganhador(t)` - Detecta vencedor
- `tabuleiro_para_str(t)` - Visualiza tabuleiro

### Movimento Automático
- `obter_movimento_auto(t, j, dif)` - Escolhe movimento com base na dificuldade
- `_movimento_facil(t, j)` - Estratégia fácil
- `_movimento_normal(t, j)` - Estratégia normal
- `_movimento_dificil(t, j)` - Estratégia difícil (Minimax)

### Jogo Principal
- `moinho(jogador_humano, dificuldade)` - Loop principal do jogo

## 💾 Ficheiros

- **ProjetoCompletoPerplexity.py** - Código completo do jogo
- **public_tests.py** - Testes automáticos (25 testes)
- **README.md** - Este ficheiro

## 📚 Conceitos Implementados

- **Abstração com TADs**: Separação clara entre interface e implementação
- **Validação**: Verificação rigorosa de entradas
- **Algoritmos de Busca**: Minimax com poda alpha-beta
- **Programação Defensiva**: Tratamento de erros e exceções
- **Interface Amigável**: Menu interativo e visualização clara

## 🎓 Linguagem e Tecnologias

- **Linguagem**: Python 3
- **Paradigma**: Programação Funcional com TADs
- **Algoritmo de IA**: Minimax com poda alpha-beta
- **Estrutura de Dados**: Dicionários Python

## 👨‍💻 Autor

Projeto desenvolvido para disciplina de Programação.

**Nota**: O projeto foi testado e validado com 100% de sucesso em todos os testes públicos! 🎉