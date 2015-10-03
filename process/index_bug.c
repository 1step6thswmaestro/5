#include <uapi/linux/ptrace.h>

BPF_TABLE("array", int, int, dist, 5);

int index_sys_clone (struct pt_regs *ctx, unsigned long flags){

    int index =0;
    int zero = 0;
    int  leaf =  0;
    //u64* val = dist.lookup_or_init(&index, &leaf);//0, 0
    //index++;leaf++;
    int *val;
    val = dist.lookup_or_init(&index, &zero);//0,0
    (*val) = leaf;
    index++;leaf++;

    val = dist.lookup_or_init(&index, &zero);//1, 1
    (*val) = leaf;
    index++;leaf++;

    val = dist.lookup_or_init(&index,&zero);//2, 2
    (*val) = leaf;
    index++;leaf++;

    val = dist.lookup_or_init(&index,&zero);//3, 3
    (*val) = leaf;
    index++;leaf++;

    val = dist.lookup_or_init(&index,&zero);//4, 4
    (*val) = leaf;
    index++;leaf++;

    val = dist.lookup_or_init(&index,&zero);//5, 5
    (*val) = leaf;
    
    
    return 0;
}
