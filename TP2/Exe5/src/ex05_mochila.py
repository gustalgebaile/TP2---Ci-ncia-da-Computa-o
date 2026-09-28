import time
import os
import sys

sys.setrecursionlimit(50000)

# --- Parte A: Solução Recursiva ---
def mochila_recursiva(W, pesos, valores, n, stats):
    stats['chamadas'] += 1
    if n == 0 or W == 0:
        return 0
    if pesos[n-1] > W:
        return mochila_recursiva(W, pesos, valores, n-1, stats)
    else:
        incluir = valores[n-1] + mochila_recursiva(W - pesos[n-1], pesos, valores, n-1, stats)
        excluir = mochila_recursiva(W, pesos, valores, n-1, stats)
        return max(incluir, excluir)

# --- Parte B: Programação Dinâmica (Memorização) ---
def mochila_pd(W, pesos, valores, n, memo, stats):
    if n == 0 or W == 0:
        return 0
    if memo[n][W] != -1:
        return memo[n][W]
        
    stats['estados'] += 1
    
    if pesos[n-1] > W:
        memo[n][W] = mochila_pd(W, pesos, valores, n-1, memo, stats)
    else:
        incluir = valores[n-1] + mochila_pd(W - pesos[n-1], pesos, valores, n-1, memo, stats)
        excluir = mochila_pd(W, pesos, valores, n-1, memo, stats)
        memo[n][W] = max(incluir, excluir)
        
    return memo[n][W]

def main():
    filepath = '/dados/itens.txt'
    
    # Gera arquivo de teste se o do professor não existir
    if not os.path.exists(filepath):
        print("Arquivo de itens não encontrado. Criando um de teste (25 itens)...")
        filepath = 'itens_teste.txt'
        with open(filepath, 'w') as f:
            import random
            random.seed(42)
            for _ in range(25):
                f.write(f"{random.randint(1, 15)} {random.randint(10, 100)}\n")

    pesos = []
    valores = []
    
    # Lê os itens assumindo o formato: peso valor
    with open(filepath, 'r') as f:
        for linha in f:
            partes = linha.strip().split()
            if len(partes) == 2:
                pesos.append(int(partes[0]))
                valores.append(int(partes[1]))

    W = 50
    n = len(pesos)
    
    print(f"Mochila - Capacidade: {W} | Total de Itens: {n}\n")

    # --- Execução da Parte A ---
    stats_rec = {'chamadas': 0}
    start_rec = time.perf_counter()
    max_val_rec = mochila_recursiva(W, pesos, valores, n, stats_rec)
    end_rec = time.perf_counter()
    tempo_rec = end_rec - start_rec

    print("--- Parte A: Recursividade ---")
    print(f"Valor máximo: {max_val_rec}")
    print(f"Chamadas recursivas: {stats_rec['chamadas']}")
    print(f"Tempo: {tempo_rec:.6f} segundos\n")

    # --- Execução da Parte B ---
    stats_pd = {'estados': 0}
    memo = [[-1 for _ in range(W + 1)] for _ in range(n + 1)]
    
    start_pd = time.perf_counter()
    max_val_pd = mochila_pd(W, pesos, valores, n, memo, stats_pd)
    end_pd = time.perf_counter()
    tempo_pd = end_pd - start_pd

    print("--- Parte B: Programação Dinâmica ---")
    print(f"Valor máximo: {max_val_pd}")
    print(f"Estados calculados: {stats_pd['estados']}")
    print(f"Tempo: {tempo_pd:.6f} segundos\n")
    
    print(f"Conclusão: PD foi {tempo_rec / tempo_pd:.2f}x mais rápida.")

if __name__ == '__main__':
    main()
