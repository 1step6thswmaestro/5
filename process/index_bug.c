#include <uapi/linux/ptrace.h>

BPF_TABLE("array", u64, u64, dist, 5);

int kprobe___do_fork (struct pt_regs *ctx, unsigned long flags){

    int index =0;
    u64  leaf =  0;
    u64* val = dist.lookup_or_init(&index, &leaf);//0, 0
    index++;leaf++;
    val = dist.lookup_or_init(&index, &leaf);//1, 1
    index++;leaf++;
    val = dist.lookup_or_init(&index,&leaf);//2, 2
    index++;leaf++;
    val = dist.lookup_or_init(&index,&leaf);//3, 3
    index++;leaf++;
    val = dist.lookup_or_init(&index,&leaf);//4, 4
    
    return 0;
}
