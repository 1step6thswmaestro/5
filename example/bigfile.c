#include <fcntl.h>
#include <unistd.h>
#include <stdio.h>


int main (int argc, char* argv[])
{
    int fd;
    fd = open("bigfile", O_WRONLY | O_CREAT, 0666);
    size_t size = 1024*1024;
    char buf[size];
    int i = 0;
    long index = 1024 * 4;
    for (i =0 ; i<index; i++){
        write(fd, buf, size);
    }
    fsync(fd);
    posix_fadvise(fd, 0, size * 4096*2, POSIX_FADV_DONTNEED);

    close(fd);

    fd = open("/proc/sys/vm/drop_caches", O_WRONLY);
    write(fd, "3\n", 3);
    close(fd);

    sleep(1);
    fd = open("bigfile", O_RDONLY);
    posix_fadvise(fd, 0, size * index, POSIX_FADV_RANDOM);
    long offset = 0;
    int count = 0;
    for (offset= 0 ; offset < size*index ; offset=offset+1024*64){
        count++;
        pread(fd, buf, 1, offset);
    }
    close(fd);
    unlink("bigfile");
    return 0;

}
