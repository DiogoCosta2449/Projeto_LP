
def criar_tabuleiro():
    tabuleiro = {
        'a': {1: '[ ]', 2: '[ ]', 3: '[ ]'},
        'b': {1: '[ ]', 2: '[ ]', 3: '[ ]'},
        'c': {1: '[ ]', 2: '[ ]', 3: '[ ]'},
    }
    return tabuleiro

def imprimir_tabuleiro(tabuleiro_local):
    print('    a   b   c')
    print(f"1  {tabuleiro_local['a'][1]}-{tabuleiro_local['b'][1]}-{tabuleiro_local['c'][1]}")
    print("    | \\ | / |")
    print(f"2  {tabuleiro_local['a'][2]}-{tabuleiro_local['b'][2]}-{tabuleiro_local['c'][2]}")
    print("    | / | \\ |")
    print(f"3  {tabuleiro_local['a'][3]}-{tabuleiro_local['b'][3]}-{tabuleiro_local['c'][3]}")

def colocar_peca(tabuleiro_local, coluna, linha, jogada):
    # Verifica se a posição existe no tabuleiro
    if coluna not in tabuleiro_local or linha not in tabuleiro_local[coluna]:
        return False, "Posição inexistente"
    # Verifica se a posição está livre
    if tabuleiro_local[coluna][linha] == '[ ]':
        tabuleiro_local[coluna][linha] = f'[{jogada}]'
        return True, "Peça colocada com sucesso"
    else:
        return False, "Posição já ocupada"


tabuleiro = criar_tabuleiro()
# Jogador tenta colocar uma peça na posição b2 com o símbolo X
sucesso, mensagem = colocar_peca(tabuleiro, 'b', 2, 'X')
print(mensagem)
imprimir_tabuleiro(tabuleiro)
# qualquer coisa