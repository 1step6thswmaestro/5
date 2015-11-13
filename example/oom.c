#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <unistd.h>
#include <fcntl.h>
int main (int argc, char * argv[])
{
    int i = 0;
    size_t size  = 1024*1024*1024;
    void * mem;
    int fd;
    mem = malloc(size);
    if (mem == NULL){
        printf("dead\n");
        return 0;
    }
    fd = open("/proc/self/oom_score_adj", O_WRONLY);
    write(fd, "1000\n", 5);
    close(fd);
    if (fork() <0 ){
        printf("error\n");
        return 0;
    }
    if (fork() <0 ){
        printf("error\n");
        return 0;
    }
    i = 10;
    while(i--){
        memset(mem, 0xff, size);
    }
    return 0;
}

