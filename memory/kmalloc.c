#include <uapi/linux/ptrace.h>
#include <linux/slab.h>

struct memory_info{
    size_t allocate_size;
    size_t free_size;
};

BPF_HASH(info, u32, struct memory_info);

int kmal(struct pt_regs *ctx, size_t size){
    
    struct memory_info * leaf;
    struct memory_info init;
    init.allocate_size = 0;
    init.free_size = 0;
    u32 pid =bpf_get_current_pid_tgid();
    leaf = info.lookup_or_init(&pid, &init);
    leaf -> allocate_size += size;
    return 0;
}
/*
 * how to find objp's size?
 * need to check this logic
 *
int kfre(struct pt_regs *ctx, void *objp){
    struct memory_info * leaf;
    struct memory_info init;
    init.allocate_size = 0;
    init.free_size = 0;
    u32 pid = bpf_get_current_pid_tgid();
    leaf = info.lookup_or_init(&pid, &init);
    leaf -> free_size += sizeof(*objp);
    return 0;
}
*/
