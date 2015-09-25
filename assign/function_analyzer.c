#include <uapi/linux/ptrace.h>

struct fun_data {

    u32 count;
    u64 total_time;
    u64 min_time;
    u64 max_time;
};

BPF_HASH(stats, u32);
BPF_TABLE("array", u32, struct fun_data, result, 8);

int function_start(struct pt_regs *ctx){
    u32 curr_pid = bpf_get_current_pid_tgid();
    u64 zero = 0;
    u64 time = bpf_ktime_get_ns();
    stats.lookup_or_init(&curr_pid, &time);
    //stats.update(&curr_pid, &time);
    return 0;

}

int function_exit(struct pt_regs *ctx){
    u32 pid = bpf_get_current_pid_tgid();
    u32 cpu = bpf_get_smp_processor_id();
    u64 *val, delta;
    val = stats.lookup(&pid);
    if(val != 0){
        delta = bpf_ktime_get_ns() - *val;
        struct fun_data *leaf = result.lookup(&cpu);
        if (leaf!=0){
            leaf->count++;
            leaf->total_time += delta;

            if(leaf->min_time > delta)
                leaf->min_time = delta;

            if(leaf->max_time < delta)
                leaf->max_time = delta;
            result.update(&cpu,leaf);
        }
        else{
            struct fun_data tp = {1, delta, delta, delta};
            result.update(&cpu, &tp);
        }   
        stats.delete(&pid);
    }
    return 0;
}
