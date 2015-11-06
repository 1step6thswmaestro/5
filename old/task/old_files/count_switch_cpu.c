#include <uapi/linux/ptrace.h>
#include <linux/sched.h>

    // key of the map
struct cpu_and_pid
{
    u32 cpu;
    u32 pid;
};

    // counting map generate
BPF_HASH(count_map, struct cpu_and_pid, u64);

int myCount_switch_cpu(struct pt_regs *ctx, struct task_struct *prev)
{
        // counting previous task's
    u64 *_cnt, _cnt_temp;
    struct cpu_and_pid _cpu_pid;
    _cpu_pid.cpu = bpf_get_smp_processor_id();
    _cpu_pid.pid = prev->pid;
    _cnt_temp = 0;

    _cnt = count_map.lookup_or_init(&_cpu_pid, &_cnt_temp);
    ++(*_cnt);
    
    return 0;
}
