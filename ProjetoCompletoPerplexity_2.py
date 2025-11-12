# ===========================
# TAD posicao
# ===========================

def cria_posicao(c, l):
    if not isinstance(c, str) or not isinstance(l, str) or \
       c not in ['a', 'b', 'c'] or l not in ['1', '2', '3']:
        raise ValueError('cria_posicao: argumentos invalidos')
    return (c, l)

def cria_copia_posicao(p):
    return (p[0], p[1])

def obter_pos_c(p):
    return p[0]

def obter_pos_l(p):
    return p[1]

def eh_posicao(arg):
    return isinstance(arg, tuple) and len(arg) == 2 and \
           isinstance(arg[0], str) and isinstance(arg[1], str) and \
           arg[0] in ['a', 'b', 'c'] and arg[1] in ['1', '2', '3']

def posicoes_iguais(p1, p2):
    return eh_posicao(p1) and eh_posicao(p2) and p1 == p2

def posicao_para_str(p):
    return p[0] + p[1]

def obter_posicoes_adjacentes(p):
    c, l = obter_pos_c(p), obter_pos_l(p)
    adjacencias_mapa = {
        ('a', '1'): [('b', '1'), ('a', '2'), ('b', '2')],
        ('b', '1'): [('a', '1'), ('c', '1'), ('b', '2')],
        ('c', '1'): [('b', '1'), ('c', '2'), ('b', '2')],
        ('a', '2'): [('a', '1'), ('b', '2'), ('a', '3')],
        ('b', '2'): [('b', '1'), ('a', '2'), ('c', '2'), ('b', '3'), ('a', '1'), ('c', '1'), ('a', '3'), ('c', '3')],
        ('c', '2'): [('c', '1'), ('b', '2'), ('c', '3')],
        ('a', '3'): [('a', '2'), ('b', '3'), ('b', '2')],
        ('b', '3'): [('b', '2'), ('a', '3'), ('c', '3')],
        ('c', '3'): [('c', '2'), ('b', '3'), ('b', '2')]
    }
    resultado = []
    for adj in adjacencias_mapa[(c, l)]:
        if adj not in resultado and eh_posicao(adj):
            resultado.append(adj)
    return tuple(resultado)

# ===========================
# TAD peca
# ===========================

def cria_peca(s):
    if not isinstance(s, str) or s not in ['X', 'O', ' ']:
        raise ValueError('cria_peca: argumento invalido')
    return s

def cria_copia_peca(j):
    return j

def eh_peca(arg):
    return isinstance(arg, str) and arg in ['X', 'O', ' ']

def pecas_iguais(j1, j2):
    return eh_peca(j1) and eh_peca(j2) and j1 == j2

def peca_para_str(j):
    return f'[{j}]'

def peca_para_inteiro(j):
    if j == 'X':
        return 1
    elif j == 'O':
        return -1
    else:
        return 0

# ===========================
# TAD tabuleiro
# ===========================

def cria_tabuleiro():
    tabuleiro = {}
    for c in ['a', 'b', 'c']:
        for l in ['1', '2', '3']:
            tabuleiro[(c, l)] = ' '
    return tabuleiro

def cria_copia_tabuleiro(t):
    return t.copy()

def obter_peca(t, p):
    return t[p]

def obter_vetor(t, s):
    pecas = []
    if s in ['1', '2', '3']:
        for c in ['a', 'b', 'c']:
            pecas.append(t[(c, s)])
    elif s in ['a', 'b', 'c']:
        for l in ['1', '2', '3']:
            pecas.append(t[(s, l)])
    return tuple(pecas)

def coloca_peca(t, j, p):
    t[p] = j
    return t

def remove_peca(t, p):
    t[p] = ' '
    return t

def move_peca(t, p1, p2):
    peca = t[p1]
    t[p1] = ' '
    t[p2] = peca
    return t

def eh_tabuleiro(arg):
    if not isinstance(arg, dict) or len(arg) != 9:
        return False
    for c in ['a', 'b', 'c']:
        for l in ['1', '2', '3']:
            if (c, l) not in arg or not eh_peca(arg[(c, l)]):
                return False
    pecas_x = sum(1 for peca in arg.values() if peca == 'X')
    pecas_o = sum(1 for peca in arg.values() if peca == 'O')
    if pecas_x > 3 or pecas_o > 3:
        return False
    if abs(pecas_x - pecas_o) > 1:
        return False
    ganhador_x = _verificar_ganhador(arg, 'X')
    ganhador_o = _verificar_ganhador(arg, 'O')
    if ganhador_x and ganhador_o:
        return False
    return True

def eh_posicao_livre(t, p):
    return t[p] == ' '

def tabuleiros_iguais(t1, t2):
    return eh_tabuleiro(t1) and eh_tabuleiro(t2) and t1 == t2

def tabuleiro_para_str(t):
    resultado = "   a   b   c\n"
    for i, l in enumerate(['1', '2', '3']):
        linha_peca = f"{l} "
        for j, c in enumerate(['a', 'b', 'c']):
            peca = peca_para_str(t[(c, l)])
            linha_peca += peca
            if j < 2:
                linha_peca += "-"
        resultado += linha_peca
        if i < 2:
            if i == 0:
                resultado += "\n   | \\ | / |\n"
            else:
                resultado += "\n   | / | \\ |\n"
    return resultado

def tuplo_para_tabuleiro(tuplo):
    tabuleiro = {}
    for i, linha in enumerate(tuplo):
        l = str(i + 1)
        for j, valor in enumerate(linha):
            c = ['a', 'b', 'c'][j]
            if valor == 1:
                tabuleiro[(c, l)] = 'X'
            elif valor == -1:
                tabuleiro[(c, l)] = 'O'
            else:
                tabuleiro[(c, l)] = ' '
    return tabuleiro

def _verificar_ganhador(t, jogador):
    for l in ['1', '2', '3']:
        if all(t[(c, l)] == jogador for c in ['a', 'b', 'c']):
            return True
    for c in ['a', 'b', 'c']:
        if all(t[(c, l)] == jogador for l in ['1', '2', '3']):
            return True
    return False

def obter_ganhador(t):
    if _verificar_ganhador(t, 'X'):
        return 'X'
    elif _verificar_ganhador(t, 'O'):
        return 'O'
    else:
        return ' '

def obter_posicoes_livres(t):
    posicoes_livres = []
    for l in ['1', '2', '3']:
        for c in ['a', 'b', 'c']:
            if t[(c, l)] == ' ':
                posicoes_livres.append((c, l))
    return tuple(posicoes_livres)

def obter_posicoes_jogador(t, j):
    posicoes_jogador = []
    for l in ['1', '2', '3']:
        for c in ['a', 'b', 'c']:
            if t[(c, l)] == j:
                posicoes_jogador.append((c, l))
    return tuple(posicoes_jogador)

# ===========================
# Funções Adicionais
# ===========================

def obter_movimento_manual(t, j):
    pecas_jogador = len(obter_posicoes_jogador(t, j))
    if pecas_jogador < 3:
        entrada = input("Turno do jogador. Escolha uma posicao: ")
        if len(entrada) != 2 or entrada[0] not in ['a', 'b', 'c'] or entrada[1] not in ['1', '2', '3']:
            raise ValueError('obter_movimento_manual: escolha invalida')
        pos = cria_posicao(entrada[0], entrada[1])
        if not eh_posicao_livre(t, pos):
            raise ValueError('obter_movimento_manual: escolha invalida')
        return (pos,)
    else:
        entrada = input("Turno do jogador. Escolha um movimento: ")
        if len(entrada) != 4:
            raise ValueError('obter_movimento_manual: escolha invalida')
        try:
            pos_origem = cria_posicao(entrada[0], entrada[1])
            pos_destino = cria_posicao(entrada[2], entrada[3])
        except:
            raise ValueError('obter_movimento_manual: escolha invalida')
        if obter_peca(t, pos_origem) != j:
            raise ValueError('obter_movimento_manual: escolha invalida')
        if not posicoes_iguais(pos_origem, pos_destino) and not eh_posicao_livre(t, pos_destino):
            raise ValueError('obter_movimento_manual: escolha invalida')
        if not posicoes_iguais(pos_origem, pos_destino):
            adjacentes = obter_posicoes_adjacentes(pos_origem)
            if pos_destino not in adjacentes:
                raise ValueError('obter_movimento_manual: escolha invalida')
        return (pos_origem, pos_destino)

def obter_movimento_auto(t, j, dificuldade):
    pecas_jogador = len(obter_posicoes_jogador(t, j))
    if pecas_jogador < 3:
        return _movimento_colocacao_auto(t, j)
    else:
        return _movimento_movimento_auto(t, j, dificuldade)

def _movimento_colocacao_auto(t, j):
    adversario = 'O' if j == 'X' else 'X'
    movimento_vitoria = _buscar_movimento_vitoria(t, j)
    if movimento_vitoria:
        return (movimento_vitoria,)
    movimento_bloqueio = _buscar_movimento_vitoria(t, adversario)
    if movimento_bloqueio:
        return (movimento_bloqueio,)
    pos_centro = cria_posicao('b', '2')
    if eh_posicao_livre(t, pos_centro):
        return (pos_centro,)
    cantos = [cria_posicao('a', '1'), cria_posicao('c', '1'), cria_posicao('a', '3'), cria_posicao('c', '3')]
    for canto in cantos:
        if eh_posicao_livre(t, canto):
            return (canto,)
    laterais = [cria_posicao('b', '1'), cria_posicao('a', '2'), cria_posicao('c', '2'), cria_posicao('b', '3')]
    for lateral in laterais:
        if eh_posicao_livre(t, lateral):
            return (lateral,)
    posicoes_livres = obter_posicoes_livres(t)
    if posicoes_livres:
        return (posicoes_livres[0],)
    return None

def _buscar_movimento_vitoria(t, j):
    for l in ['1', '2', '3']:
        pecas_linha = [obter_peca(t, cria_posicao(c, l)) for c in ['a', 'b', 'c']]
        if pecas_linha.count(j) == 2 and pecas_linha.count(' ') == 1:
            for i, c in enumerate(['a', 'b', 'c']):
                if pecas_linha[i] == ' ':
                    return cria_posicao(c, l)
    for c in ['a', 'b', 'c']:
        pecas_coluna = [obter_peca(t, cria_posicao(c, l)) for l in ['1', '2', '3']]
        if pecas_coluna.count(j) == 2 and pecas_coluna.count(' ') == 1:
            for i, l in enumerate(['1', '2', '3']):
                if pecas_coluna[i] == ' ':
                    return cria_posicao(c, l)
    return None

def _movimento_movimento_auto(t, j, dificuldade):
    if dificuldade == 'facil':
        return _movimento_facil(t, j)
    elif dificuldade == 'normal':
        return _movimento_normal(t, j)
    elif dificuldade == 'dificil':
        return _movimento_dificil(t, j)
    return _movimento_facil(t, j)

def _movimento_facil(t, j):
    posicoes_jogador = obter_posicoes_jogador(t, j)
    for pos_origem in posicoes_jogador:
        adjacentes = obter_posicoes_adjacentes(pos_origem)
        for pos_destino in adjacentes:
            if eh_posicao_livre(t, pos_destino):
                return (pos_origem, pos_destino)
    if posicoes_jogador:
        return (posicoes_jogador[0], posicoes_jogador[0])
    return None

def _movimento_normal(t, j):
    movimento_vitoria = _buscar_movimento_vitoria_movimento(t, j)
    if movimento_vitoria:
        return movimento_vitoria
    adversario = 'O' if j == 'X' else 'X'
    movimento_bloqueio = _buscar_movimento_bloqueio_movimento(t, adversario)
    if movimento_bloqueio:
        return movimento_bloqueio
    return _movimento_facil(t, j)

def _movimento_dificil(t, j):
    melhor_movimento = _minimax_profundidade_5(t, j)
    if melhor_movimento:
        return melhor_movimento
    return _movimento_normal(t, j)

def _buscar_movimento_vitoria_movimento(t, j):
    posicoes_jogador = obter_posicoes_jogador(t, j)
    for pos_origem in posicoes_jogador:
        adjacentes = obter_posicoes_adjacentes(pos_origem)
        for pos_destino in adjacentes:
            if eh_posicao_livre(t, pos_destino):
                t_copia = cria_copia_tabuleiro(t)
                move_peca(t_copia, pos_origem, pos_destino)
                if obter_ganhador(t_copia) == j:
                    return (pos_origem, pos_destino)
    return None

def _buscar_movimento_bloqueio_movimento(t, adversario):
    posicoes_adversario = obter_posicoes_jogador(t, adversario)
    j = 'O' if adversario == 'X' else 'X'
    for pos_orig_adv in posicoes_adversario:
        adj_adv = obter_posicoes_adjacentes(pos_orig_adv)
        for pos_dest_adv in adj_adv:
            if eh_posicao_livre(t, pos_dest_adv):
                t_copia = cria_copia_tabuleiro(t)
                move_peca(t_copia, pos_orig_adv, pos_dest_adv)
                if obter_ganhador(t_copia) == adversario:
                    posicoes_jogador = obter_posicoes_jogador(t, j)
                    for p_origem in posicoes_jogador:
                        adj = obter_posicoes_adjacentes(p_origem)
                        if pos_dest_adv in adj:
                            return (p_origem, pos_dest_adv)
    return None

def _minimax_profundidade_5(t, j):
    melhor_pontuacao = float('-inf')
    melhor_movimento = None
    posicoes_jogador = obter_posicoes_jogador(t, j)
    for pos_origem in posicoes_jogador:
        adjacentes = obter_posicoes_adjacentes(pos_origem)
        for pos_destino in adjacentes:
            if eh_posicao_livre(t, pos_destino):
                t_copia = cria_copia_tabuleiro(t)
                move_peca(t_copia, pos_origem, pos_destino)
                pontuacao = _minimax(t_copia, 5, False, j, float('-inf'), float('inf'))
                if pontuacao > melhor_pontuacao:
                    melhor_pontuacao = pontuacao
                    melhor_movimento = (pos_origem, pos_destino)
    return melhor_movimento

def _minimax(t, profundidade, maximizar, jogador_inicial, alpha, beta):
    ganhador = obter_ganhador(t)
    if ganhador == jogador_inicial:
        return 100 + profundidade
    elif ganhador != ' ':
        return -100 - profundidade
    if profundidade == 0:
        return _avaliar_tabuleiro(t, jogador_inicial)
    jogador_atual = jogador_inicial if maximizar else ('O' if jogador_inicial == 'X' else 'X')
    posicoes = obter_posicoes_jogador(t, jogador_atual)
    if maximizar:
        max_aval = float('-inf')
        for pos_origem in posicoes:
            adjacentes = obter_posicoes_adjacentes(pos_origem)
            for pos_destino in adjacentes:
                if eh_posicao_livre(t, pos_destino):
                    t_copia = cria_copia_tabuleiro(t)
                    move_peca(t_copia, pos_origem, pos_destino)
                    aval = _minimax(t_copia, profundidade - 1, False, jogador_inicial, alpha, beta)
                    max_aval = max(max_aval, aval)
                    alpha = max(alpha, aval)
                    if beta <= alpha:
                        return max_aval
        return max_aval if max_aval != float('-inf') else 0
    else:
        min_aval = float('inf')
        for pos_origem in posicoes:
            adjacentes = obter_posicoes_adjacentes(pos_origem)
            for pos_destino in adjacentes:
                if eh_posicao_livre(t, pos_destino):
                    t_copia = cria_copia_tabuleiro(t)
                    move_peca(t_copia, pos_origem, pos_destino)
                    aval = _minimax(t_copia, profundidade - 1, True, jogador_inicial, alpha, beta)
                    min_aval = min(min_aval, aval)
                    beta = min(beta, aval)
                    if beta <= alpha:
                        return min_aval
        return min_aval if min_aval != float('inf') else 0

def _avaliar_tabuleiro(t, jogador):
    pontuacao = 0
    adversario = 'O' if jogador == 'X' else 'X'
    for l in ['1', '2', '3']:
        linha = [obter_peca(t, cria_posicao(c, l)) for c in ['a', 'b', 'c']]
        pontuacao += _avaliar_sequencia(linha, jogador, adversario)
    for c in ['a', 'b', 'c']:
        coluna = [obter_peca(t, cria_posicao(c, l)) for l in ['1', '2', '3']]
        pontuacao += _avaliar_sequencia(coluna, jogador, adversario)
    return pontuacao

def _avaliar_sequencia(seq, jogador, adversario):
    pontuacao = 0
    if seq.count(jogador) == 2 and seq.count(' ') == 1:
        pontuacao += 10
    if seq.count(adversario) == 2 and seq.count(' ') == 1:
        pontuacao -= 15
    if seq.count(jogador) == 3:
        pontuacao += 100
    if seq.count(adversario) == 3:
        pontuacao -= 100
    return pontuacao

# ===========================
# Função Principal
# ===========================

def moinho(jogador_humano, dificuldade):
    if jogador_humano not in ['[X]', '[O]'] or dificuldade not in ['facil', 'normal', 'dificil']:
        raise ValueError('moinho: argumentos invalidos')
    peca_humano = jogador_humano[1]
    peca_computador = 'O' if peca_humano == 'X' else 'X'
    print(f"Bem-vindo ao JOGO DO MOINHO. Nivel de dificuldade {dificuldade}.")
    t = cria_tabuleiro()
    print(tabuleiro_para_str(t))
    turno_atual = 'X'
    while True:
        if turno_atual == peca_humano:
            movimento = obter_movimento_manual(t, peca_humano)
            if len(movimento) == 1:
                coloca_peca(t, peca_humano, movimento[0])
            else:
                move_peca(t, movimento[0], movimento[1])
            print(tabuleiro_para_str(t))
        else:
            print(f"Turno do computador ({dificuldade}):")
            movimento = obter_movimento_auto(t, peca_computador, dificuldade)
            if len(movimento) == 1:
                coloca_peca(t, peca_computador, movimento[0])
            else:
                move_peca(t, movimento[0], movimento[1])
            print(tabuleiro_para_str(t))
        ganhador = obter_ganhador(t)
        if ganhador != ' ':
            return peca_para_str(ganhador)
        turno_atual = 'O' if turno_atual == 'X' else 'X'

# ===========================
# Iniciar o jogo
# ===========================
if __name__ == "__main__":
    print("\n===== JOGO DO MOINHO =====\n")
    print("Escolha o seu jogador:")
    print("1 - X (começa primeiro)")
    print("2 - O (computador começa)")

    escolha_jogador = input("Digite 1 ou 2: ").strip()

    if escolha_jogador == "1":
        jogador_escolhido = '[X]'
    elif escolha_jogador == "2":
        jogador_escolhido = '[O]'
    else:
        print("Escolha inválida! Jogando como X por defeito.")
        jogador_escolhido = '[X]'

    print("\nEscolha a dificuldade:")
    print("1 - Fácil")
    print("2 - Normal")
    print("3 - Difícil")

    escolha_dificuldade = input("Digite 1, 2 ou 3: ").strip()

    if escolha_dificuldade == "1":
        dificuldade_escolhida = 'facil'
    elif escolha_dificuldade == "2":
        dificuldade_escolhida = 'normal'
    elif escolha_dificuldade == "3":
        dificuldade_escolhida = 'dificil'
    else:
        print("Escolha inválida! Dificuldade normal por defeito.")
        dificuldade_escolhida = 'normal'

    print()
    resultado = moinho(jogador_escolhido, dificuldade_escolhida)
    print(f"\n========== JOGO TERMINADO ==========")
    print(f"O vencedor foi: {resultado}")
