#include <uapi/linux/ptrace.h>
#include <linux/gfp.h>

BPF_HASH(simple_map, u32);
BPF_TABLE("array", int, u64, flag, 5);


int malloc_call(struct pt_regs *ctx, size_t size, gfp_t flags)
{
    u32 pid = bpf_get_current_pid_tgid();
    u64* sizes = simple_map.lookup(&pid);
    int index;
    u64 * value;
    u64 zero = 0;

    if (sizes)
    {
        (*sizes) += size;
    }
    else
    {
        u64 one = size;
        simple_map.update(&pid, &one);
    }
    if((flags & GFP_USER)== GFP_USER){
        index = 1;
        value =flag.lookup_or_init(&index, &zero);
        (*value)++;
    }
    else if((flags & GFP_KERNEL)== GFP_KERNEL){
        index = 2;
        value =flag.lookup_or_init(&index, &zero);
        (*value)++;
        if ((*value)>100)
            return 1;
    }
    else if((flags & GFP_ATOMIC)== GFP_ATOMIC){
        index = 3;
        value =flag.lookup_or_init(&index, &zero);
        (*value)++;
    }
    else {
        index = 4 ;
        value =flag.lookup_or_init(&index, &zero);
        (*value)++;
    }

return 0;
}
