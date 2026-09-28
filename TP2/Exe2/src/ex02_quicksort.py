import time
import sys
import os

# Aumenta o limite de recursão do Python (útil caso o QuickSort caia no pior caso)
sys.setrecursionlimit(50000)

def partition(arr, low, high, stats):
    # Escolhemos o último elemento como pivô
    pivot = arr[high]
    i = low - 1
    
    for j in range(low, high):
        stats['comparisons'] += 1
        # Se o elemento atual for menor ou igual ao pivô, trocamos
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
            
    # Coloca o pivô na sua posição final correta
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1

def quicksort(arr, low, high, stats):
    stats['recursions'] += 1
    
    if low < high:
        # pi é o índice de particionamento (posição correta do pivô)
        pi = partition(arr, low, high, stats)
        
        # Ordena os elementos antes e depois da partição recursivamente
        quicksort(arr, low, pi - 1, stats)
        quicksort(arr, pi + 1, high, stats)

def main():
    filepath = '/dados/numeros.txt'
    
    if not os.path.exists(filepath):
        print(f"Erro: Arquivo {filepath} não encontrado.")
        return

    # Lendo o arquivo e convertendo as linhas em uma lista de inteiros
    print("Lendo o arquivo de números...")
    with open(filepath, 'r') as f:
        arr = [int(line.strip()) for line in f if line.strip()]

    # Dicionário para rastrear os contadores por referência
    stats = {
        'comparisons': 0,
        'recursions': 0
    }
    
    print(f"Iniciando ordenação de {len(arr)} números com QuickSort...")
    
    # Inicia a contagem de tempo com alta precisão
    start_time = time.perf_counter()
    
    # Chama o algoritmo
    quicksort(arr, 0, len(arr) - 1, stats)
    
    # Finaliza a contagem de tempo
    end_time = time.perf_counter()
    
    print("\n--- Resultados ---")
    print(f"Quantidade de comparações: {stats['comparisons']}")
    print(f"Quantidade de chamadas recursivas: {stats['recursions']}")
    print(f"Tempo de execução: {end_time - start_time:.4f} segundos")
    
    # Salvar o resultado ordenado para comprovação
    output_path = 'outputs/numeros_ordenados_quicksort.txt'
    with open(output_path, 'w') as f:
        for num in arr:
            f.write(f"{num}\n")
    print(f"\nLista ordenada salva em: {output_path}")

if __name__ == '__main__':
    main()
