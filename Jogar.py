import tkinter as tk
from tkinter import messagebox

# ===========================
# TAD posicao (mantem idêntico)
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
# Funções de movimento e IA
# ===========================

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
# Interface gráfica com Tkinter
# ===========================

class JogoMoinhoApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Jogo do Moinho")
        self.geometry("400x450")
        self.resizable(False, False)

        self.tabuleiro = cria_tabuleiro()
        self.jogador_humano = None
        self.peca_humano = None
        self.peca_computador = None
        self.dificuldade = None
        self.turno_atual = 'X'
        self.fase_colocacao = True
        self.botao_selecionado = None

        self.criar_widgets()
        self.pedir_configuracao()

    def criar_widgets(self):
        self.info_label = tk.Label(self, text="Bem-vindo ao Jogo do Moinho", font=("Arial", 14))
        self.info_label.pack(pady=10)

        self.buttons_frame = tk.Frame(self)
        self.buttons_frame.pack()

        # Mapa de posições para acesso rápido  buttons[(c,l)]
        self.buttons = {}
        posicoes = [('a', '1'), ('b', '1'), ('c', '1'),
                    ('a', '2'), ('b', '2'), ('c', '2'),
                    ('a', '3'), ('b', '3'), ('c', '3')]
        for i, pos in enumerate(posicoes):
            btn = tk.Button(self.buttons_frame, text='', font=("Arial", 18), width=4, height=2,
                            command=lambda p=pos: self.botao_clicado(p))
            # grid com 3 colunas e 3 linhas
            btn.grid(row=i//3, column=i%3, padx=5, pady=5)
            self.buttons[pos] = btn

        self.status_label = tk.Label(self, text="A aguardar configuração...", font=("Arial", 12))
        self.status_label.pack(pady=10)

    def pedir_configuracao(self):
        self.info_label.config(text="Escolha o seu jogador (X começa)")
        self.botao_jx = tk.Button(self, text="Jogador X", command=lambda: self.iniciar_jogo('[X]'))
        self.botao_jo = tk.Button(self, text="Jogador O", command=lambda: self.iniciar_jogo('[O]'))
        self.botao_jx.pack(pady=5)
        self.botao_jo.pack(pady=5)

    def iniciar_jogo(self, jogador):
        self.jogador_humano = jogador
        self.peca_humano = jogador[1]
        self.peca_computador = 'O' if self.peca_humano == 'X' else 'X'
        self.botao_jx.pack_forget()
        self.botao_jo.pack_forget()
        self.info_label.config(text=f"Jogador: {self.jogador_humano}")
        self.pedir_dificuldade()

    def pedir_dificuldade(self):
        self.info_label.config(text="Escolha a dificuldade")
        self.botao_facil = tk.Button(self, text="Fácil", command=lambda: self.set_dificuldade('facil'))
        self.botao_normal = tk.Button(self, text="Normal", command=lambda: self.set_dificuldade('normal'))
        self.botao_dificil = tk.Button(self, text="Difícil", command=lambda: self.set_dificuldade('dificil'))
        self.botao_facil.pack(pady=3)
        self.botao_normal.pack(pady=3)
        self.botao_dificil.pack(pady=3)

    def set_dificuldade(self, nivel):
        self.dificuldade = nivel
        self.botao_facil.pack_forget()
        self.botao_normal.pack_forget()
        self.botao_dificil.pack_forget()
        self.status_label.config(text=f"Dificuldade: {self.dificuldade}")
        self.info_label.config(text="Comece a jogar! Coloque peças no tabuleiro.")
        self.atualizar_tabuleiro()

        if self.peca_computador == 'X':
            self.jogada_computador()

    def atualizar_tabuleiro(self):
        for pos, btn in self.buttons.items():
            peca = obter_peca(self.tabuleiro, pos)
            if peca == ' ':
                btn.config(text='', state=tk.NORMAL, bg='SystemButtonFace')
            elif peca == 'X':
                btn.config(text='X', fg='blue', state=tk.DISABLED, bg='white')
            else:
                btn.config(text='O', fg='red', state=tk.DISABLED, bg='white')

    def botao_clicado(self, pos):
        if self.fase_colocacao:
            if not eh_posicao_livre(self.tabuleiro, pos):
                messagebox.showwarning("Posição ocupada", "Esta posição já está ocupada!")
                return
            if self.peca_humano != self.turno_atual:
                messagebox.showinfo("Aguarde", "Não é o seu turno!")
                return
            coloca_peca(self.tabuleiro, self.peca_humano, pos)
            self.atualizar_tabuleiro()
            vencedor = obter_ganhador(self.tabuleiro)
            if vencedor != ' ':
                messagebox.showinfo("Fim de Jogo", f"Jogador {vencedor} venceu!")
                self.desativar_tabuleiro()
                return
            self.mudar_turno()
            self.jogada_computador()
        else:
            if self.botao_selecionado is None:
                if obter_peca(self.tabuleiro, pos) == self.peca_humano:
                    self.botao_selecionado = pos
                    self.buttons[pos].config(bg='yellow')
                else:
                    messagebox.showwarning("Peça inválida", "Selecione uma das suas peças primeiro!")
            else:
                if pos == self.botao_selecionado:
                    # Deseleciona a peça
                    self.buttons[self.botao_selecionado].config(bg='SystemButtonFace')
                    self.botao_selecionado = None
                else:
                    if pos in obter_posicoes_adjacentes(self.botao_selecionado) and eh_posicao_livre(self.tabuleiro, pos):
                        move_peca(self.tabuleiro, self.botao_selecionado, pos)
                        self.atualizar_tabuleiro()
                        vencedor = obter_ganhador(self.tabuleiro)
                        if vencedor != ' ':
                            messagebox.showinfo("Fim de Jogo", f"Jogador {vencedor} venceu!")
                            self.desativar_tabuleiro()
                            return
                        self.botao_selecionado = None
                        self.mudar_turno()
                        self.jogada_computador()
                    else:
                        messagebox.showwarning("Movimento inválido", "Movimento inválido para essa peça.")
                        self.buttons[self.botao_selecionado].config(bg='SystemButtonFace')
                        self.botao_selecionado = None

    def mudar_turno(self):
        self.turno_atual = 'O' if self.turno_atual == 'X' else 'X'
        if self.turno_atual == 'X':
            self.status_label.config(text="Turno do jogador X")
        else:
            self.status_label.config(text="Turno do jogador O")
        self.fase_colocacao = (len(obter_posicoes_jogador(self.tabuleiro, 'X')) < 3 or
                              len(obter_posicoes_jogador(self.tabuleiro, 'O')) < 3)

    def jogada_computador(self):
        if self.turno_atual != self.peca_computador:
            return
        movimento = obter_movimento_auto(self.tabuleiro, self.peca_computador, self.dificuldade)
        if movimento is None:
            messagebox.showinfo("Fim de Jogo", "Empate!")
            self.desativar_tabuleiro()
            return
        if len(movimento) == 1:
            coloca_peca(self.tabuleiro, self.peca_computador, movimento[0])
        else:
            move_peca(self.tabuleiro, movimento[0], movimento[1])
        self.atualizar_tabuleiro()
        vencedor = obter_ganhador(self.tabuleiro)
        if vencedor != ' ':
            messagebox.showinfo("Fim de Jogo", f"Jogador {vencedor} venceu!")
            self.desativar_tabuleiro()
            return
        self.mudar_turno()

    def desativar_tabuleiro(self):
        for btn in self.buttons.values():
            btn.config(state=tk.DISABLED)


if __name__ == '__main__':
    app = JogoMoinhoApp()
    app.mainloop()
