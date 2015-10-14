#include <uapi/linux/ptrace.h>
#include <linux/sched.h>

BPF_TABLE("array", int, int, dist2, 1);

int count_sys_fork(struct pt_regs *ctx){
    int index = 0;
    int zero = 0;
    int * leaf;
    leaf = dist2.lookup_or_init(&index, &zero);
    
    (*leaf)++;

    if ((*leaf) > NUM )
        return 1;

    return 0;
}
