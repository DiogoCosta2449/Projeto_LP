# --- TAD posicao ---
def cria_posicao(c, l):
    if c not in ('a', 'b', 'c') or l not in ('1', '2', '3'):
        raise ValueError('cria_posicao: argumentos invalidos')
    return {'c': c, 'l': l}

def cria_copia_posicao(p):
    if not eh_posicao(p):
        raise ValueError('cria_copia_posicao: argumento invalido')
    return {'c': p['c'], 'l': p['l']}

def obter_pos_c(p):
    if not eh_posicao(p):
        raise ValueError('obter_pos_c: argumento invalido')
    return p['c']

def obter_pos_l(p):
    if not eh_posicao(p):
        raise ValueError('obter_pos_l: argumento invalido')
    return p['l']

def eh_posicao(arg):
    return isinstance(arg, dict) and 'c' in arg and 'l' in arg and arg['c'] in ('a','b','c') and arg['l'] in ('1','2','3')

def posicoes_iguais(p1, p2):
    if not (eh_posicao(p1) and eh_posicao(p2)):
        return False
    return p1['c'] == p2['c'] and p1['l'] == p2['l']

def posicao_para_str(p):
    if not eh_posicao(p):
        raise ValueError('posicao_para_str: argumento invalido')
    return p['c'] + p['l']

def obter_posicoes_adjacentes(p):
    if not eh_posicao(p):
        raise ValueError('obter_posicoes_adjacentes: argumento invalido')
    mapa_adjacentes = {
        'a1': ['a2', 'b1'],
        'a2': ['a1', 'a3', 'b2'],
        'a3': ['a2', 'b3'],
        'b1': ['a1', 'b2', 'c1'],
        'b2': ['a2', 'b1', 'b3', 'c2', 'a2', 'c2', 'a3', 'c1', 'c3', 'a1', 'a3', 'c1', 'c3'],
        # b2 deve ligar a todas as diagonais e meios (mas SEM duplicações!)
        'b2': ['a2', 'b1', 'b3', 'c2', 'a1', 'a3', 'c1', 'c3'],
        'b3': ['a3', 'b2', 'c3'],
        'c1': ['b1', 'c2'],
        'c2': ['c1', 'b2', 'c3'],
        'c3': ['b3', 'c2']
    }

    # Ajuste para garantir que não há repetição na lista
    pos_str = posicao_para_str(p)
    adj_raw = list(dict.fromkeys(mapa_adjacentes.get(pos_str, [])))
    adj_posicoes = tuple(cria_posicao(x[0], x[1]) for x in adj_raw)
    return adj_posicoes


# --- TAD peca ---
def cria_peca(s):
    if s not in ('X','O',' '):
        raise ValueError('cria_peca: argumento invalido')
    return s

def cria_copia_peca(j):
    if not eh_peca(j):
        raise ValueError('cria_copia_peca: argumento invalido')
    return j

def eh_peca(arg):
    return isinstance(arg, str) and arg in ('X','O',' ')

def pecas_iguais(j1, j2):
    if not (eh_peca(j1) and eh_peca(j2)):
        return False
    return j1 == j2

def peca_para_str(j):
    if not eh_peca(j):
        raise ValueError('peca_para_str: argumento invalido')
    return '[' + j + ']'

def peca_para_inteiro(j):
    if not eh_peca(j):
        raise ValueError('peca_para_inteiro: argumento invalido')
    if j == 'X':
        return 1
    elif j == 'O':
        return -1
    else:
        return 0

# --- TAD tabuleiro ---
def cria_tabuleiro():
    return [[' ' for _ in range(3)] for _ in range(3)]

def cria_copia_tabuleiro(t):
    if not eh_tabuleiro(t):
        raise ValueError('cria_copia_tabuleiro: argumento invalido')
    return [linha[:] for linha in t]

def eh_tabuleiro(arg):
    if not (isinstance(arg, list) and len(arg) == 3):
        return False
    for linha in arg:
        if not (isinstance(linha, list) and len(linha) == 3):
            return False
        for peca in linha:
            if not eh_peca(peca):
                return False
    x_count = sum(peca_para_inteiro(p) == 1 for linha in arg for p in linha)
    o_count = sum(peca_para_inteiro(p) == -1 for linha in arg for p in linha)
    if x_count > 3 or o_count > 3:
        return False
    ganhador = obter_ganhador(arg)
    if ganhador not in (' ', 'X', 'O'):
        return False
    return True

def obter_peca(t, p):
    if not (eh_tabuleiro(t) and eh_posicao(p)):
        raise ValueError('obter_peca: argumento invalido')
    c = obter_pos_c(p)
    l = obter_pos_l(p)
    col_idx = ord(c) - ord('a')
    row_idx = int(l) - 1
    return t[row_idx][col_idx]

def obter_vetor(t, s):
    if not (eh_tabuleiro(t) and isinstance(s, str)):
        raise ValueError('obter_vetor: argumentos invalidos')
    if s in ('a','b','c'):
        col_idx = ord(s) - ord('a')
        return tuple(t[i][col_idx] for i in range(3))
    elif s in ('1','2','3'):
        row_idx = int(s) - 1
        return tuple(t[row_idx][i] for i in range(3))
    else:
        raise ValueError('obter_vetor: argumento invalido')

def coloca_peca(t, j, p):
    if not (eh_tabuleiro(t) and eh_peca(j) and eh_posicao(p)):
        raise ValueError('coloca_peca: argumentos invalidos')
    if not eh_posicao_livre(t, p):
        raise ValueError('coloca_peca: posicao ocupada')
    c = obter_pos_c(p)
    l = obter_pos_l(p)
    col_idx = ord(c) - ord('a')
    row_idx = int(l) - 1
    t[row_idx][col_idx] = j
    return t

def remove_peca(t, p):
    if not (eh_tabuleiro(t) and eh_posicao(p)):
        raise ValueError('remove_peca: argumentos invalidos')
    if eh_posicao_livre(t, p):
        raise ValueError('remove_peca: posicao livre')
    c = obter_pos_c(p)
    l = obter_pos_l(p)
    col_idx = ord(c) - ord('a')
    row_idx = int(l) - 1
    t[row_idx][col_idx] = ' '
    return t

def move_peca(t, p1, p2):
    if not (eh_tabuleiro(t) and eh_posicao(p1) and eh_posicao(p2)):
        raise ValueError('move_peca: argumentos invalidos')
    if eh_posicao_livre(t, p1):
        raise ValueError('move_peca: posicao origem livre')
    if not eh_posicao_livre(t, p2):
        raise ValueError('move_peca: posicao destino ocupada')
    peca = obter_peca(t, p1)
    t = remove_peca(t, p1)
    t = coloca_peca(t, peca, p2)
    return t

def eh_posicao_livre(t, p):
    if not eh_tabuleiro(t) or not eh_posicao(p):
        raise ValueError('eh_posicao_livre: argumento invalido')
    return obter_peca(t, p) == ' '

def tabuleiros_iguais(t1, t2):
    if not (eh_tabuleiro(t1) and eh_tabuleiro(t2)):
        return False
    for i in range(3):
        for j in range(3):
            if t1[i][j] != t2[i][j]:
                return False
    return True

def tabuleiro_para_str(t):
    if not eh_tabuleiro(t):
        raise ValueError('tabuleiro_para_str: argumento invalido')
    linha_0 = '   a   b   c'
    linhas = []
    for i in range(3):
        linha_pecas = []
        for j in range(3):
            linha_pecas.append(peca_para_str(t[i][j]))
        linha_str = str(i+1) + ' ' + '-'.join(linha_pecas)
        linhas.append(linha_str)
    linhas_conexao = [
        '  | \\ | / |',
        '  | / | \\ |',
        '  | \\ | / |'
    ]
    resultado = linha_0 + '\n'
    for i in range(3):
        resultado += linhas[i] + '\n'
        if i < 2:
            resultado += linhas_conexao[i] + '\n'
    return resultado.rstrip()

# --- Funções de jogo ---
def obter_ganhador(t):
    for i in range(3):
        if t[i][0] == t[i][1] == t[i][2] != ' ':
            return t[i][0]
    for j in range(3):
        if t[0][j] == t[1][j] == t[2][j] != ' ':
            return t[0][j]
    return ' '

def obter_posicoes_livres(t):
    pos_livres = []
    for l in ('1','2','3'):
        for c in ('a','b','c'):
            p = cria_posicao(c,l)
            if eh_posicao_livre(t,p):
                pos_livres.append(p)
    return tuple(pos_livres)

def obter_posicoes_jogador(t, j):
    pos_ocup = []
    for l in ('1','2','3'):
        for c in ('a','b','c'):
            p = cria_posicao(c,l)
            if pecas_iguais(obter_peca(t,p), j):
                pos_ocup.append(p)
    return tuple(pos_ocup)

def jogador_ganhou(t, j):
    ganhador = obter_ganhador(t)
    return pecas_iguais(ganhador, j)

def obter_posicoes_adjacentes_livres(t, p):
    adj = obter_posicoes_adjacentes(p)
    adj_livres = [pos for pos in adj if eh_posicao_livre(t, pos)]
    return tuple(adj_livres)

def movimento_valido(t, j, p1, p2):
    if not (eh_tabuleiro(t) and eh_peca(j) and eh_posicao(p1) and eh_posicao(p2)):
        return False
    if not pecas_iguais(obter_peca(t, p1), j):
        return False
    if not eh_posicao_livre(t, p2):
        return False
    adj = obter_posicoes_adjacentes(p1)
    return any(posicoes_iguais(p2, adj_pos) for adj_pos in adj)

def todos_movimentos_possiveis(t, j):
    posicoes = obter_posicoes_jogador(t, j)
    movimentos = []
    for p1 in posicoes:
        adjacentes = obter_posicoes_adjacentes_livres(t, p1)
        for p2 in adjacentes:
            if movimento_valido(t,j,p1,p2):
                movimentos.append((p1,p2))
    return movimentos

def obter_movimento_manual(t,j):
    fase_colocacao = len(obter_posicoes_jogador(t, j)) < 3
    while True:
        try:
            if fase_colocacao:
                jogada = input('Turno do jogador. Escolha uma posicao: ')
                if len(jogada) != 2:
                    raise ValueError
                p = cria_posicao(jogada[0], jogada[1])
                if not eh_posicao_livre(t,p):
                    raise ValueError
                return (p,)
            else:
                jogada = input('Turno do jogador. Escolha um movimento (p1p2): ')
                if len(jogada) != 4:
                    raise ValueError
                p1 = cria_posicao(jogada[0], jogada[1])
                p2 = cria_posicao(jogada[2], jogada[3])
                if not movimento_valido(t,j,p1,p2):
                    raise ValueError
                return (p1,p2)
        except ValueError:
            print('obter_movimento_manual: escolha invalida')

def heuristica(t, j):
    ganhador = obter_ganhador(t)
    if pecas_iguais(ganhador, j):
        return 100
    elif ganhador != ' ' and ganhador != j:
        return -100
    else:
        return 0

def maxmin(t, j, profundidade, max_prof):
    if profundidade == max_prof or obter_ganhador(t) != ' ':
        return heuristica(t, j), None
    melhor_valor = -float('inf')
    melhor_movimento = None
    movimentos = todos_movimentos_possiveis(t, j)
    if not movimentos:
        return heuristica(t,j), None
    for mov in movimentos:
        t_copia = cria_copia_tabuleiro(t)
        t_copia = move_peca(t_copia, mov[0], mov[1])
        val, _ = minmax(t_copia, adversario(j), profundidade+1, max_prof)
        if val > melhor_valor:
            melhor_valor = val
            melhor_movimento = mov
    return melhor_valor, melhor_movimento

def minmax(t, j, profundidade, max_prof):
    if profundidade == max_prof or obter_ganhador(t) != ' ':
        return heuristica(t, j), None
    melhor_valor = float('inf')
    melhor_movimento = None
    movimentos = todos_movimentos_possiveis(t, j)
    if not movimentos:
        return heuristica(t,j), None
    for mov in movimentos:
        t_copia = cria_copia_tabuleiro(t)
        t_copia = move_peca(t_copia, mov[0], mov[1])
        val, _ = maxmin(t_copia, adversario(j), profundidade+1, max_prof)
        if val < melhor_valor:
            melhor_valor = val
            melhor_movimento = mov
    return melhor_valor, melhor_movimento

def adversario(j):
    return 'O' if j == 'X' else 'X'

def ha_vitoria_ou_bloqueio(t, j):
    pos_livres = obter_posicoes_livres(t)
    for p in pos_livres:
        t_copia = cria_copia_tabuleiro(t)
        coloca_peca(t_copia, j, p)
        if jogador_ganhou(t_copia, j):
            return p
    return None

def obter_movimento_auto_colocacao(t, j):
    advers = adversario(j)
    p = ha_vitoria_ou_bloqueio(t, j)
    if p is not None:
        return (p,)
    p = ha_vitoria_ou_bloqueio(t, advers)
    if p is not None:
        return (p,)
    centro = cria_posicao('b','2')
    if eh_posicao_livre(t, centro):
        return (centro,)
    cantos = [cria_posicao(c,l) for c,l in [('a','1'),('a','3'),('c','1'),('c','3')]]
    for pos in cantos:
        if eh_posicao_livre(t,pos):
            return (pos,)
    laterais = [cria_posicao(c,l) for c,l in [('a','2'),('b','1'),('b','3'),('c','2')]]
    for pos in laterais:
        if eh_posicao_livre(t,pos):
            return (pos,)
    return None

def obter_movimento_auto_movimento(t, j, nivel):
    if nivel == 'facil':
        movimentos = todos_movimentos_possiveis(t,j)
        if movimentos:
            return movimentos[0]
        return None
    elif nivel in ('medio', 'dificil'):
        _, mov = maxmin(t, j, 0, 2 if nivel == 'medio' else 4)
        return mov
    else:
        return None

def moinho():
    print('Bem-vindo ao Jogo do Moinho')
    t = cria_tabuleiro()
    jogador_humano = 'X'
    jogador_computador = 'O'
    nivel = ''

    while nivel not in ('facil', 'medio', 'dificil'):
        nivel = input('Escolha nivel de dificuldade (facil, medio, dificil): ').lower()

    turno = 'X'
    fase_colocacao_jog_humano = True
    fase_colocacao_pc = True

    for i in range(6):
        print(tabuleiro_para_str(t))
        if turno == jogador_humano:
            p = None
            while p is None:
                try:
                    jogada = obter_movimento_manual(t, turno)
                    p = jogada[0]
                    if not eh_posicao_livre(t,p):
                        print('Posicao ocupada, tente outra.')
                        p = None
                except ValueError:
                    print('Entrada invalida, tente novamente')
            coloca_peca(t, turno, p)
            if i == 2:
                fase_colocacao_jog_humano = False
        else:
            p = obter_movimento_auto_colocacao(t, turno)
            if p is not None:
                coloca_peca(t, turno, p[0])
            if i == 3:
                fase_colocacao_pc = False
        if jogador_ganhou(t, turno):
            print(tabuleiro_para_str(t))
            print(f'Ganhador: {turno}')
            return
        turno = adversario(turno)

    while True:
        print(tabuleiro_para_str(t))
        if turno == jogador_humano:
            movimentos = todos_movimentos_possiveis(t, turno)
            if not movimentos:
                print('Sem movimentos possiveis. Ganhador: O computador')
                return
            mov = None
            while mov is None:
                try:
                    jogada = obter_movimento_manual(t, turno)
                    if len(jogada) != 2:
                        print('Movimento invalido, deve ter 2 posicoes')
                        continue
                    p1, p2 = jogada
                    if movimento_valido(t, turno, p1, p2):
                        mov = (p1, p2)
                    else:
                        print('Movimento invalido, tente novamente')
                except ValueError:
                    print('Entrada invalida, tente novamente')
            t = move_peca(t, mov[0], mov[1])
        else:
            movimentos = todos_movimentos_possiveis(t, turno)
            if not movimentos:
                print('Sem movimentos possiveis. Ganhador: Jogador humano')
                return
            mov = obter_movimento_auto_movimento(t, turno, nivel)
            if mov is None:
                print('Sem movimentos possiveis para computador. Ganhador: Jogador humano')
                return
            t = move_peca(t, mov[0], mov[1])

        if jogador_ganhou(t, turno):
            print(tabuleiro_para_str(t))
            print(f'Ganhador: {turno}')
            return
        turno = adversario(turno)

if __name__ == "__main__":
    moinho()
