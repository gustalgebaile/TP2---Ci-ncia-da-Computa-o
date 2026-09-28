import asyncio
import os
import time

def count_lines_words(filepath):
    lines = 0
    words = 0
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            lines += 1
            words += len(line.split())
    return os.path.basename(filepath), lines, words

async def process_file_async(filepath):
    # Executa a leitura do arquivo em uma thread separada para não bloquear o event loop
    return await asyncio.to_thread(count_lines_words, filepath)

async def main():
    directory = '/dados/arquivos'
    
    if not os.path.exists(directory):
        print(f"Diretório {directory} não encontrado.")
        return

    filepaths = [os.path.join(directory, f) for f in os.listdir(directory) 
                 if os.path.isfile(os.path.join(directory, f))]

    start_time = time.time()

    # Cria e aguarda todas as tarefas assíncronas rodarem concorrentemente
    tasks = [process_file_async(fp) for fp in filepaths]
    results = await asyncio.gather(*tasks)

    for filename, lines, words in results:
        print(f"{filename}")
        print(f"Linhas: {lines}")
        print(f"Palavras: {words}")

    end_time = time.time()
    print(f"Tempo total: {end_time - start_time:.2f} segundos")

if __name__ == '__main__':
    asyncio.run(main())
