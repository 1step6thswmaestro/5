#include <uapi/linux/ptrace.h>
#include <linux/gfp.h>

#define NUM_GFP_FLAG 25

struct malloc_data {
    size_t size;
    u64 flag[NUM_GFP_FLAG];
};

struct pid_and_size {
    u32 pid;
    size_t size;
};

BPF_HASH(pid_size, struct pid_and_size, u64);
BPF_HASH(pid_total, u32, struct malloc_data);

int malloc_call(struct pt_regs *ctx, size_t size, gfp_t flags)
{
    u32 pid = bpf_get_current_pid_tgid();
    struct malloc_data* leaf = pid_total.lookup(&pid);
    struct pid_and_size new_pid_size;
    u64 zero = 0;
    new_pid_size.pid = pid;
    new_pid_size.size = size;
    gfp_t shift_bit = 1;

    if (leaf)
    {
        leaf->size += size;
        for (int i = 0 ; i < NUM_GFP_FLAG; ++i)
        {
            if (shift_bit & flags)
                leaf->flag[i]++;
            shift_bit <<= 1;
        }
       
        u64 *val = pid_size.lookup_or_init(&new_pid_size, &zero);
        (*val)++;
    }
    else
    {
        struct malloc_data new_total;
        new_total.size = size;

        for(int i = 0 ; i < NUM_GFP_FLAG; ++i)
        {
            if (flags & shift_bit)
                new_total.flag[i] = 1;
            else
                new_total.flag[i] = 0;

            shift_bit <<= 1;
        }

        pid_total.update(&pid, &new_total);
        pid_size.update(&new_pid_size, &zero);
    }

    return 0;
}


