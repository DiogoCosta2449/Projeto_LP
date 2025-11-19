import tkinter as tk
from tkinter import messagebox

# ========== TADs e Funções Base ==========

def cria_posicao(c, l):
    if not isinstance(c, str) or not isinstance(l, str) or c not in ['a', 'b', 'c'] or l not in ['1', '2', '3']:
        raise ValueError('cria_posicao: argumentos invalidos')
    return (c, l)
def obter_pos_c(p): return p[0]
def obter_pos_l(p): return p[1]
def eh_posicao(arg): return isinstance(arg, tuple) and len(arg) == 2 and isinstance(arg[0], str) and isinstance(arg[1], str) and arg[0] in ['a', 'b', 'c'] and arg[1] in ['1', '2', '3']
def posicoes_iguais(p1, p2): return eh_posicao(p1) and eh_posicao(p2) and p1 == p2
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

def cria_peca(s):
    if not isinstance(s, str) or s not in ['X', 'O', ' ']:
        raise ValueError('cria_peca: argumento invalido')
    return s
def eh_peca(arg): return isinstance(arg, str) and arg in ['X', 'O', ' ']
def pecas_iguais(j1, j2): return eh_peca(j1) and eh_peca(j2) and j1 == j2
def peca_para_str(j): return f'[{j}]'

def cria_tabuleiro():
    tabuleiro = {}
    for c in ['a', 'b', 'c']:
        for l in ['1', '2', '3']:
            tabuleiro[(c, l)] = ' '
    return tabuleiro

def cria_copia_tabuleiro(t): return t.copy()
def obter_peca(t, p): return t[p]
def coloca_peca(t, j, p): t[p] = j; return t
def move_peca(t, p1, p2): peca = t[p1]; t[p1] = ' '; t[p2] = peca; return t
def eh_posicao_livre(t, p): return t[p] == ' '
def obter_posicoes_livres(t): return tuple([k for k,v in t.items() if v == ' '])
def obter_posicoes_jogador(t, j): return tuple([k for k,v in t.items() if v == j])

def _verificar_ganhador(t, jogador):
    for l in ['1', '2', '3']:
        if all(t[(c, l)] == jogador for c in ['a', 'b', 'c']): return True
    for c in ['a', 'b', 'c']:
        if all(t[(c, l)] == jogador for l in ['1', '2', '3']): return True
    return False

def obter_ganhador(t):
    if _verificar_ganhador(t, 'X'): return 'X'
    elif _verificar_ganhador(t, 'O'): return 'O'
    else: return ' '

# ========== Algoritmo de IA Completo com dificuldades ==========

def obter_movimento_auto(t, j, dificuldade):
    pecas_jogador = len(obter_posicoes_jogador(t, j))
    if pecas_jogador < 3:
        return _movimento_colocacao_auto(t, j)
    else:
        return _movimento_movimento_auto(t, j, dificuldade)

def _movimento_colocacao_auto(t, j):
    adversario = 'O' if j == 'X' else 'X'
    movimento_vitoria = _buscar_movimento_vitoria(t, j)
    if movimento_vitoria: return (movimento_vitoria,)
    movimento_bloqueio = _buscar_movimento_vitoria(t, adversario)
    if movimento_bloqueio: return (movimento_bloqueio,)
    pos_centro = cria_posicao('b', '2')
    if eh_posicao_livre(t, pos_centro): return (pos_centro,)
    cantos = [cria_posicao('a', '1'), cria_posicao('c', '1'), cria_posicao('a', '3'), cria_posicao('c', '3')]
    for canto in cantos:
        if eh_posicao_livre(t, canto): return (canto,)
    laterais = [cria_posicao('b', '1'), cria_posicao('a', '2'), cria_posicao('c', '2'), cria_posicao('b', '3')]
    for lateral in laterais:
        if eh_posicao_livre(t, lateral): return (lateral,)
    posicoes_livres = obter_posicoes_livres(t)
    if posicoes_livres: return (posicoes_livres[0],)
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
    if posicoes_jogador: return (posicoes_jogador[0], posicoes_jogador[0])
    return None

def _movimento_normal(t, j):
    movimento_vitoria = _buscar_movimento_vitoria_movimento(t, j)
    if movimento_vitoria: return movimento_vitoria
    adversario = 'O' if j == 'X' else 'X'
    movimento_bloqueio = _buscar_movimento_bloqueio_movimento(t, adversario)
    if movimento_bloqueio: return movimento_bloqueio
    return _movimento_facil(t, j)

def _movimento_dificil(t, j):
    melhor_movimento = _minimax_profundidade_5(t, j)
    if melhor_movimento: return melhor_movimento
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
# INTERFACE TKINTER
# ===========================

class MoinhoGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Jogo do Moinho")
        self.configure(background='black')
        self.tabuleiro = cria_tabuleiro()
        self.peca_humano = None
        self.peca_computador = None
        self.dificuldade = None
        self.turno_atual = None
        self.botao_selecionado = None
        self.fase_colocacao = True
        self.start_screen()

    def start_screen(self):
        self.clear_widgets()
        self.label = tk.Label(self, text="Escolha o seu jogador", font=("Arial", 18), bg="black", fg="white")
        self.label.pack(pady=26)
        self.x_btn = tk.Button(self, text="X (começa)", width=16, height=2, command=lambda: self.choose_player('X'))
        self.x_btn.pack(pady=6)
        self.o_btn = tk.Button(self, text="O", width=16, height=2, command=lambda: self.choose_player('O'))
        self.o_btn.pack(pady=6)

    def choose_player(self, jogador):
        self.peca_humano = jogador
        self.peca_computador = 'O' if jogador == 'X' else 'X'
        self.difficulty_screen()

    def difficulty_screen(self):
        self.clear_widgets()
        self.label = tk.Label(self, text="Escolha a dificuldade", font=("Arial", 18), bg="black", fg="white")
        self.label.pack(pady=26)
        self.btns = []
        for label, diff in [("Fácil", "facil"), ("Normal", "normal"), ("Difícil", "dificil")]:
            btn = tk.Button(self, text=label, width=16, height=2, command=lambda d=diff: self.start_game(d))
            btn.pack(pady=6)
            self.btns.append(btn)

    def start_game(self, dificultad):
        self.dificuldade = dificultad
        self.turno_atual = 'X'
        self.tabuleiro = cria_tabuleiro()
        self.fase_colocacao = True
        self.setup_board()

    def clear_widgets(self):
        for widget in self.winfo_children():
            widget.destroy()

    def setup_board(self):
        self.clear_widgets()
        self.info = tk.Label(self, text=f"Turno: {self.turno_atual} | Dif: {self.dificuldade}", font=("Arial", 14), bg="black", fg="white")
        self.info.pack(pady=2)
        self.canvas = tk.Canvas(self, width=420, height=420, bg="black", highlightthickness=0)
        self.canvas.pack()
        self.draw_board_lines()
        self.buttons = {}
        pos_btn_xy = {('a','1'):(60,60), ('b','1'):(210,60), ('c','1'):(360,60),
                      ('a','2'):(60,210), ('b','2'):(210,210), ('c','2'):(360,210),
                      ('a','3'):(60,360), ('b','3'):(210,360), ('c','3'):(360,360)}
        for (c, l), (x, y) in pos_btn_xy.items():
            btn = tk.Button(self, text="", font=("Arial", 18,"bold"), width=2, height=1, bg="white",
                            command=lambda p=(c,l): self.cell_click(p))
            btn_window = self.canvas.create_window(x, y, window=btn, width=53, height=53)
            self.buttons[(c,l)] = btn
        self.status = tk.Label(self, text="", font=("Arial", 12), fg="yellow", bg="black")
        self.status.pack(pady=8)
        self.update_board()
        if self.turno_atual == self.peca_computador:
            self.after(700, self.computer_move)

    def draw_board_lines(self):
        c = self.canvas
        # Linhas horizontais
        c.create_line(60,60, 360,60, fill='grey', width=5)
        c.create_line(60,210, 360,210, fill='grey', width=5)
        c.create_line(60,360, 360,360, fill='grey', width=5)
        # Linhas verticais
        c.create_line(60,60, 60,360, fill='grey', width=5)
        c.create_line(210,60, 210,360, fill='grey', width=5)
        c.create_line(360,60, 360,360, fill='grey', width=5)
        # Diagonais (para o efeito visual do moinho)
        c.create_line(60,60, 210,210, fill='grey', dash=(5,4), width=2)
        c.create_line(360,60, 210,210, fill='grey', dash=(5,4), width=2)
        c.create_line(60,360, 210,210, fill='grey', dash=(5,4), width=2)
        c.create_line(360,360, 210,210, fill='grey', dash=(5,4), width=2)

    def cell_click(self, pos):
        if self.turno_atual != self.peca_humano:
            return
        if self.fase_colocacao:
            if not eh_posicao_livre(self.tabuleiro, pos):
                self.status['text'] = "Casa ocupada! Escolha livre."
                return
            coloca_peca(self.tabuleiro, self.peca_humano, pos)
            self.update_board()
            if obter_ganhador(self.tabuleiro) != ' ':
                self.end_game(f"Jogador {obter_ganhador(self.tabuleiro)} venceu!")
                return
            self.switch_turn()
            self.after(700, self.computer_move)
        else:
            if self.botao_selecionado is None:
                if obter_peca(self.tabuleiro, pos) == self.peca_humano:
                    self.botao_selecionado = pos
                    self.buttons[pos].configure(bg="lightblue")
                else:
                    self.status['text'] = "Clique numa peça sua para mover."
            else:
                if pos == self.botao_selecionado:
                    self.buttons[self.botao_selecionado].configure(bg="white")
                    self.botao_selecionado = None
                elif pos in obter_posicoes_adjacentes(self.botao_selecionado) and eh_posicao_livre(self.tabuleiro, pos):
                    move_peca(self.tabuleiro, self.botao_selecionado, pos)
                    self.botao_selecionado = None
                    self.update_board()
                    if obter_ganhador(self.tabuleiro) != ' ':
                        self.end_game(f"Jogador {obter_ganhador(self.tabuleiro)} venceu!")
                        return
                    self.switch_turn()
                    self.after(700, self.computer_move)
                else:
                    self.status['text'] = "Movimento inválido!"
                    self.buttons[self.botao_selecionado].configure(bg="white")
                    self.botao_selecionado = None

    def computer_move(self):
        mov = obter_movimento_auto(self.tabuleiro, self.peca_computador, self.dificuldade)
        if mov is None:
            self.end_game("Empate!")
            return
        if len(mov) == 1:
            coloca_peca(self.tabuleiro, self.peca_computador, mov[0])
        else:
            move_peca(self.tabuleiro, mov[0], mov[1])
        self.update_board()
        if obter_ganhador(self.tabuleiro) != ' ':
            self.end_game(f"Jogador {obter_ganhador(self.tabuleiro)} venceu!")
            return
        self.switch_turn()

    def update_board(self):
        for p, btn in self.buttons.items():
            v = obter_peca(self.tabuleiro, p)
            btn.configure(text=v, bg="white" if v in [' ',''] else ("#51a0ff" if v=='X' else "#ff5151"))
            btn.config(state=tk.NORMAL if v == ' ' or v == self.peca_humano else tk.DISABLED)
        self.fase_colocacao = (len(obter_posicoes_jogador(self.tabuleiro, 'X')) < 3 or len(obter_posicoes_jogador(self.tabuleiro, 'O')) < 3)
        if self.fase_colocacao:
            self.status['text'] = "Coloque as peças no tabuleiro."
        else:
            self.status['text'] = "Clique na sua peça e mova para casa adjacente."

    def switch_turn(self):
        self.turno_atual = 'O' if self.turno_atual == 'X' else 'X'
        self.info['text'] = f"Turno: {self.turno_atual} | Dif: {self.dificuldade}"

    def end_game(self, msg):
        for b in self.buttons.values():
            b.config(state=tk.DISABLED)
        self.status['text'] = msg
        self.after(3500, self.reset_all)

    def reset_all(self):
        self.tabuleiro = cria_tabuleiro()
        self.peca_humano = None
        self.peca_computador = None
        self.dificuldade = None
        self.turno_atual = None
        self.botao_selecionado = None
        self.fase_colocacao = True
        self.start_screen()

if __name__ == "__main__":
    app = MoinhoGUI()
    app.mainloop()
