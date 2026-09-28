#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <dirent.h>
#include <omp.h>
#include <ctype.h>

#define MAX_FILES 1000
#define MAX_PATH 512

void process_file(const char* filepath, const char* filename) {
    FILE* file = fopen(filepath, "r");
    if (!file) return;

    int lines = 0;
    int words = 0;
    int in_word = 0;
    char buffer[4096];

    while (fgets(buffer, sizeof(buffer), file)) {
        lines++;
        for (int i = 0; buffer[i] != '\0'; i++) {
            if (isspace(buffer[i])) {
                in_word = 0;
            } else if (in_word == 0) {
                in_word = 1;
                words++;
            }
        }
    }
    fclose(file);

    // Evita que as threads misturem os textos na tela na hora de imprimir
    #pragma omp critical
    {
        printf("%s\nLinhas: %d\nPalavras: %d\n", filename, lines, words);
    }
}

int main() {
    DIR *dir;
    struct dirent *ent;
    char filepaths[MAX_FILES][MAX_PATH];
    char filenames[MAX_FILES][MAX_PATH];
    int file_count = 0;

    const char* dir_path = "/dados/arquivos";

    // Lê todos os arquivos do diretório
    if ((dir = opendir(dir_path)) != NULL) {
        while ((ent = readdir(dir)) != NULL) {
            if (ent->d_name[0] != '.') { // Ignora pastas ocultas . e ..
                snprintf(filepaths[file_count], MAX_PATH, "%s/%s", dir_path, ent->d_name);
                snprintf(filenames[file_count], MAX_PATH, "%s", ent->d_name);
                file_count++;
            }
        }
        closedir(dir);
    } else {
        perror("Erro ao abrir o diretório");
        return EXIT_FAILURE;
    }

    // Inicia a contagem do tempo
    double start_time = omp_get_wtime();

    // Distribui os arquivos dinamicamente entre as threads
    #pragma omp parallel for schedule(dynamic)
    for (int i = 0; i < file_count; i++) {
        process_file(filepaths[i], filenames[i]);
    }

    // Finaliza a contagem do tempo
    double end_time = omp_get_wtime();
    printf("Tempo total: %.2f segundos\n", end_time - start_time);

    return 0;
}
