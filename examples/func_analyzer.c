#include <uapi/linux/ptrace.h>

struct func_call_info
{
    int count;
    u64 total_time;
    u64 min_time;
    u64 max_time;
};

BPF_HASH(anal, u32);
BPF_TABLE("array", u32, struct func_call_info, result, 6);

int function_start(struct pr_regs *ctx){
    u64 zero = 0;
    u64 val = bpf_ktime_get_ns();
    u32 curr_pid = bpf_get_currend_pid_tgid();
    
    anal.update(&curr_pid, &val);
}

int function_exit(struct pr_regs *ctx){
    u32 pid = bpf_get_currend_pid_tgid();
    u64 time = bpf_ktime_get_ns();
    u32 cpu = bpf_get_smp_processor_id();
    u64* val = stats.lookup(&pid), delta;
    
    if(val)
    {
        delta = bpf_ktime_get_ns() - *val;
        u64 *leaf = result.lookup(&cpu);
        
        if(leaf)
        {
            leaf->count++;
            leaf->total_time += delta;
            
            if(leaf->min_time > delta)
                leaf->min_time = delta;

            if(leaf->max_time < delta)
                leaf->max_time = delta;
            
            result.update(&cpu, leaf);
        }
        else
        {
            struct func_call_info tp = {1, delta, delta, delta};
            result.update(&cpu, &tp);
        }
    }
}
