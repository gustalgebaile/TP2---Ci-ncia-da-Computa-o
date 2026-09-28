import sys
import os

sys.setrecursionlimit(50000)

def imprimir_labirinto(labirinto):
    for linha in labirinto:
        print("".join(linha))
    print()

def resolver_labirinto(labirinto, x, y, visitados):
    # Condição de parada 1: Fora dos limites do labirinto
    if x < 0 or x >= len(labirinto) or y < 0 or y >= len(labirinto[0]):
        return False

    # Condição de parada 2: Bateu na parede ('#') ou já visitou essa célula
    if labirinto[x][y] == '#' or (x, y) in visitados:
        return False

    # Sucesso: Encontrou a saída ('E')
    if labirinto[x][y] == 'E':
        return True

    # Registra a posição como visitada para não voltar nela
    visitados.add((x, y))
    
    eh_inicio = (labirinto[x][y] == 'S')
    
    # Marca visualmente o caminho atual com um ponto (exceto no 'S')
    if not eh_inicio:
        labirinto[x][y] = '.'

    # Passo Recursivo: Tentar as 4 direções (Baixo, Cima, Direita, Esquerda)
    direcoes = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    for dx, dy in direcoes:
        if resolver_labirinto(labirinto, x + dx, y + dy, visitados):
            return True # Se o caminho deu certo, propaga o sucesso de volta

    # Backtracking: Se todas as 4 direções falharam, retrocede.
    # Desfazemos a marcação visual do caminho (apagando o ponto).
    if not eh_inicio:
        labirinto[x][y] = ' '
    
    return False

def main():
    filepath = '/dados/labirinto.txt'
    
    # Gera um labirinto de fallback caso o professor não tenha especificado o nome do arquivo
    if not os.path.exists(filepath):
        print("Arquivo padrão não encontrado. Utilizando labirinto de teste...")
        filepath = 'labirinto_teste.txt'
        with open(filepath, 'w') as f:
            f.write("###############\n#S   #        #\n# ### # ##### #\n#  ##   ##    #\n### # ##### # #\n#   #       # #\n# ##### # # # #\n#     # #   # #\n##### # ##### #\n#     #       #\n# ########### #\n#           #E#\n###############\n")

    labirinto = []
    start_x, start_y = -1, -1
    
    # Leitura do arquivo
    with open(filepath, 'r') as f:
        for i, linha in enumerate(f):
            linha_lista = list(linha.strip('\n'))
            if not linha_lista: continue
            labirinto.append(linha_lista)
            if 'S' in linha_lista:
                start_x = i
                start_y = linha_lista.index('S')

    if start_x == -1:
        print("Erro: Ponto de início 'S' não encontrado no labirinto.")
        return

    visitados = set()
    
    print("Labirinto Inicial:")
    imprimir_labirinto(labirinto)
    
    if resolver_labirinto(labirinto, start_x, start_y, visitados):
        print("Caminho encontrado!")
        imprimir_labirinto(labirinto)
    else:
        print("Não há saída para este labirinto.")

if __name__ == '__main__':
    main()
