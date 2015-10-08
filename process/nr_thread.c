#include <uapi/linux/ptrace.h>
#include <linux/sched.h>

struct thread_count{
    int nr_curr;
    int max;
    int min;
};

BPF_TABLE("array", int, struct thread_count, dist, 1);

int read_nr_thread(struct pt_regs *ctx, unsigned long flags){

    int n  = 0;
    bpf_probe_read(&n, sizeof(int), (void*) ADRVAR );
    int index = 0;
    struct thread_count * count_info;
    struct thread_count  init_info = {0, 0, 0};

    count_info = dist.lookup_or_init(&index, &init_info);
    count_info -> nr_curr = n;


    if (n > count_info->max){
        count_info->max = n;
    }
    else if( n <count_info->min || count_info->min== 0){
        count_info->min = n;
    }
    
    return 0;
}

    
