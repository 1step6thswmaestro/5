#include <uapi/linux/ptrace.h>
#include <linux/sched.h>

BPF_TABLE("array", int, int, dist, 4);

int read_nr_thread(struct pt_regs *ctx, unsigned long flags){

    int n  = 0;
    bpf_probe_read(&n, sizeof(int), (void*) ADRVAR );
    int index = 0;
    int *nr_curr;
    int *max;
    int *min;
    int zero = 0;

    nr_curr = dist.lookup_or_init(&index, &zero);
    (*nr_curr) = n;
    index = 2;
    max = dist.lookup_or_init(&index, &zero);
    index = 3;
    min = dist.lookup_or_init(&index, &zero);
    if (n > (*max)){
        (*max) = n;
    }
    else if( n <(*min) || (*min)== 0){
        (*min) = n;
    }
    
    return 0;
}

    
