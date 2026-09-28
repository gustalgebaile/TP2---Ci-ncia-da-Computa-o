import time
import sys
import os

sys.setrecursionlimit(50000)

def partition(arr, low, high):
    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1

def quickselect(arr, low, high, k):
    # Se o array contém apenas um elemento, retornamos ele
    if low == high:
        return arr[low]
    
    # Particiona o array e obtém o índice do pivô
    pi = partition(arr, low, high)
    
    # Se o pivô for exatamente o k-ésimo elemento procurado
    if k == pi:
        return arr[k]
    # Se k for menor, procuramos apenas na metade esquerda
    elif k < pi:
        return quickselect(arr, low, pi - 1, k)
    # Se k for maior, procuramos apenas na metade direita
    else:
        return quickselect(arr, pi + 1, high, k)

def main():
    filepath = '/dados/numeros.txt'
    
    if not os.path.exists(filepath):
        print(f"Erro: Arquivo {filepath} não encontrado.")
        return

    # Lendo o arquivo para duas listas separadas (para comparar os métodos)
    with open(filepath, 'r') as f:
        arr_select = [int(line.strip()) for line in f if line.strip()]
    arr_sort = list(arr_select) # Cópia para o teste do QuickSort

    # Queremos o 1000º menor número. Como os índices começam em 0, k = 999
    k_index = 999 

    print(f"Buscando o {k_index + 1}º menor número em {len(arr_select)} elementos...")

    # --- TESTE 1: QuickSelect ---
    start_select = time.perf_counter()
    resultado_select = quickselect(arr_select, 0, len(arr_select) - 1, k_index)
    end_select = time.perf_counter()
    tempo_select = end_select - start_select

    print("\n--- QuickSelect ---")
    print(f"Resultado: {resultado_select}")
    print(f"Tempo: {tempo_select:.6f} segundos")

    # --- TESTE 2: QuickSort (aproveitando o código da Parte A adaptado) ---
    def quicksort(arr, low, high):
        if low < high:
            pi = partition(arr, low, high)
            quicksort(arr, low, pi - 1)
            quicksort(arr, pi + 1, high)

    start_sort = time.perf_counter()
    quicksort(arr_sort, 0, len(arr_sort) - 1)
    resultado_sort = arr_sort[k_index]
    end_sort = time.perf_counter()
    tempo_sort = end_sort - start_sort

    print("\n--- QuickSort + Acesso à posição ---")
    print(f"Resultado: {resultado_sort}")
    print(f"Tempo: {tempo_sort:.6f} segundos")
    print(f"\nConclusão: QuickSelect foi {tempo_sort / tempo_select:.2f}x mais rápido.")

if __name__ == '__main__':
    main()
