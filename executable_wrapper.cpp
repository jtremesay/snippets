// Includes cstd
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <unistd.h>

// Includes c++std
#include <iostream>

// Includes divers
#include <sys/types.h>


#define safe_free(__PTR__) do { free(__PTR__); __PTR__ = 0; } while (false)
#define safe_delete(__PTR__) do { delete __PTR__; __PTR__ = 0; } while (false)
#define safe_delete_array(__PTR__) do { delete[] __PTR__; __PTR__ = 0; } while (false)


static const char LOG_PATH[] = "/mnt/HDA_ROOT/.logs/file_log/";
static const char EXE_PATH[] = "/opt/bin/file";



void log_parents_callstack(pid_t pid)
{

}

void __find_parents(pid_t pid, FILE * log_handler)
{

}



char ** duplicate_argv_for_exec(const char * executable_name, const int argc, const char ** argv)
{
    // Create the array
    char ** argv_for_exec = (char **) calloc(argc + 1, sizeof(char *));

    // Copy executable name
    argv_for_exec[0] = (char *) calloc(strlen(executable_name) + 1, sizeof(char));
    strcpy(argv_for_exec[0], executable_name);

    // Copy arguments
    for (int i = 1; i < argc; ++i) {
        argv_for_exec[i] = (char *) calloc(strlen(argv[i]) + 1, sizeof(char));
        strcpy(argv_for_exec[i], argv[i]);
    }

    // argv is NULL terminated
    argv_for_exec[argc] = NULL;

    return argv_for_exec;
}

void free_duplicated_argv(int argc, char ** argv)
{
    for (int i = 0; i < argc; ++i) {
        safe_free(argv[i]);
    }
    safe_free(argv);
}


int main(const int argc, const char * argv[], const char * env[])
{
    // L'executable
    // Création du tableau des arguments
    char ** exe_argv = duplicate_argv_for_exec(EXE_PATH, argc, argv);


    // Récupère le PID de l'appli
    pid_t pid = getpid();
    log_parents_callstack(pid);


    // Appel de l'executable
    //execv(EXE_PATH, exe_argv);


    //ménage
    free_duplicated_argv(argc, exe_argv);



    return EXIT_SUCCESS;
}
