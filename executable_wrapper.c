#define _GNU_SOURCE 1

// Includes cstd
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <unistd.h>

// Includes divers
#include <sys/types.h>


// Libère et met à NULL un pointeur
#define safe_free(__PTR__) do { free(__PTR__); __PTR__ = NULL; } while (false)


// Dossier de log
static const char LOG_PATH[] = "/mnt/HDA_ROOT/.logs/file_log/";

// Executable à remplacers
static const char EXE_PATH[] = "/opt/bin/file";


/**
 * Retourne le nom d'un processus
 * La mémoire doit être libérée par l'utilisateur
 *
 * @param pid_t pid Le pid du processus
 * @return char * Le nom du processus ou NULL en cas d'erreur
 */
char * get_process_name(pid_t pid);


/**
 * Retourne le pid du processus parent
 *
 * @param pid_t pid Le pid du processus
 * @return pid_t Le pid du processus parent ou 0 en cas d'erreur
 */
pid_t get_parent_pid(pid_t pid);


/**
 * Écrit dans un un fichier la hierachie des parents du processus
 * @param pid_t pid Le pid
 * @param FILE * L'handler du fichier dans lequel écrire
 */
void log_parents_callstack(pid_t pid, FILE * log_handler);


/**
 * Crée une copie de argv destiné à être utilisé par les fonctions exec*
 * La copie doit être détruite avec free_duplicated_argv
 *
 * @param const char * executable_name Le nom de l'executable
 * @param const int argc La taille d'argv
 * @param const char ** argv L'argv à copier et à adapter
 * @return char ** Une copie modifiée de argv ou NULL en cas d'erreur
 */
char ** duplicate_argv_for_exec(const char * executable_name, const int argc, const char ** argv);


/**
 * Libère la mémoire alloué par duplicate_argv_for_exec
 *
 * @param const int argc La taille d'argv
 * @param const char ** argv L'argv à libérer
 */
void free_duplicated_argv(int argc, char ** argv);


/**
 * Génère le nom du fichier de log
 * La mémoire doit être libérée par l'utilisateur
 *
 * @return char * Le chemin vers le fichier de log ou NULL en cas d'erreur
 */
char * generate_log_file_path(pid_t pid);


int main(const int argc, const char * argv[], const char * env[])
{
    // Création du tableau des arguments
    char ** exe_argv = duplicate_argv_for_exec(EXE_PATH, argc, argv);


    // Récupère le pid courant
    pid_t pid = getpid();


    // Génère le chemin vers le fichier de log
    char * log_path = generate_log_file_path(pid);
    if (log_path != NULL) {
        // Ouvre le fichier de log
        FILE * log_handler = fopen(log_path, "w");
        if (log_handler != NULL) {
            // Génère la callstack
            log_parents_callstack(pid, log_handler);

            fclose(log_handler);
        }

        safe_free(log_path);
    }


    // Remplacement du processus courant
    execv(EXE_PATH, exe_argv);


    //ménage
    free_duplicated_argv(argc, exe_argv);

    return EXIT_SUCCESS;
}



char * get_process_name(pid_t pid)
{
    char * process_name = NULL;
    FILE * process_cmdline_handler;

    // Génération du chemin vers le cmdline du processus
    char * process_cmdline_path = NULL;
    if (asprintf(&process_cmdline_path, "/proc/%d/cmdline", pid) == -1) {
        goto error;
    }


    // Ouverture du fichier
    process_cmdline_handler = fopen(process_cmdline_path, "r");
    if (process_cmdline_handler == NULL) {
        goto error;
    }


    // Lecture du fichier
    char buffer[4096];
    if (fgets(buffer, sizeof(buffer), process_cmdline_handler) == NULL) {
        goto error;
    }


    // Création de de la chaine contenant le contenu utile
    const size_t process_name_length = strlen(buffer) + 1;
    process_name = calloc(process_name_length, sizeof(char));
    if (process_name == NULL) {
        goto error;
    }


    // Copie du contenue
    strcpy(process_name, buffer);


error:
    // Ménage
    if (process_cmdline_handler != NULL) {
        fclose(process_cmdline_handler);
    }

    safe_free(process_cmdline_path);

    return process_name;
}


pid_t get_parent_pid(pid_t pid)
{
    pid_t parent_pid = 0;
    FILE * process_stat_handler;

    // Génération du chemin vers le cmdline du processus
    char * process_stat_path = NULL;
    if (asprintf(&process_stat_path, "/proc/%d/stat", pid) == -1) {
        goto error;
    }


    // Ouverture du fichier
    process_stat_handler = fopen(process_stat_path, "r");
    if (process_stat_handler == NULL) {
        goto error;
    }


    // Lecture du fichier
    char buffer[4096];
    if (fgets(buffer, sizeof(buffer), process_stat_handler) == NULL) {
        goto error;
    }


    // Recherche du pid du parent,
    // C'est le 4ème champs du fichier stat
    char * tok = strtok(buffer, " ");
    for (int i = 0; i < 3 && tok; ++i) {
        tok = strtok(NULL, " ");
    }

    parent_pid = atoi(tok);

error:
    // Ménage
    if (process_stat_handler != NULL) {
        fclose(process_stat_handler);
    }

    safe_free(process_stat_path);

    return parent_pid;
}


void log_parents_callstack(pid_t pid, FILE * log_handler)
{
    pid_t parent_pid = get_parent_pid(pid);
    if (parent_pid == 0) { // Une erreur est survenue ou on a atteint la racine, on s'arrête
        return;
    }


    // Recherche les infos du parent
    log_parents_callstack(parent_pid, log_handler);


    // Log les infos du processus
    char * process_name = get_process_name(pid);
    fprintf(log_handler, "%d - %s\n", pid, process_name);


    // Ménage
    safe_free(process_name);
}


char ** duplicate_argv_for_exec(const char * executable_name, const int argc, const char ** argv)
{
    // Crée le argv
    char ** argv_for_exec = (char **) calloc(argc + 1, sizeof(char *));
    if (argv_for_exec == NULL) {
        goto error;
    }


    // Copie le nom de l'exécutable
    argv_for_exec[0] = (char *) calloc(strlen(executable_name) + 1, sizeof(char));
    if (argv_for_exec[0] == NULL) {
        goto error;
    }
    strcpy(argv_for_exec[0], executable_name);


    // Copie les arguments
    for (int i = 1; i < argc; ++i) {
        argv_for_exec[i] = (char *) calloc(strlen(argv[i]) + 1, sizeof(char));
        if (argv_for_exec[i] == NULL) {
            goto error;
        }
        strcpy(argv_for_exec[i], argv[i]);
    }

    // argv est terminé par NULL
    argv_for_exec[argc] = NULL;

    return argv_for_exec;

error:
    // Ménage
    free_duplicated_argv(argc, argv_for_exec);

    return NULL;
}

void free_duplicated_argv(int argc, char ** argv)
{
    if (argv != NULL) {
        for (int i = 0; i < argc; ++i) {
            safe_free(argv[i]);
        }
    }

    safe_free(argv);
}


char * generate_log_file_path(pid_t pid)
{
    char * log_path = NULL;
    time_t t = time(NULL);
    struct tm tm = * localtime(&t);
    asprintf(&log_path, "%s%d_%d%d%d_%d%d%d.log", LOG_PATH, pid, tm.tm_year + 1900, tm.tm_mon + 1, tm.tm_mday, tm.tm_hour, tm.tm_min, tm.tm_sec);

    return log_path;
}
