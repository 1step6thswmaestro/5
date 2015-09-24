#include <uapi/linux/ptrace.h>
#include <linux/sched.h>

struct key_t{
    u32 pre_pid;
};

BPF_TABLE("hash", struct key_t, u64, stats, 1024);

int count_sched(struct pt_regs *ctx, struct task_struct *prev){

    u64 zero=0;
    struct key_t key = {};
    u64* val;
    key.pre_pid = prev->pid;
    val=stats.lookup_or_init(&key, &zero);
    (*val)++;

    return 0;
}
