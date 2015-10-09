#include <uapi/linux/ptrace.h>
#include <linux/sched.h>

    // value of the map
struct switch_counter_task
{ // count nvcsw and nivcsw of task_struct
    unsigned long myNvcsw;
    unsigned long myNivcsw;
};

    // counting map generate
BPF_HASH(count_map, u32, struct switch_counter_task);

int myCount_switch_task(struct pt_regs *ctx, struct task_struct *prev)//, struct task_struct *next)
{
        // counting previous task's
    struct switch_counter_task *_cnt, _cnt_temp;//, _cnt_temp2;
    u32 _pid = prev->pid;
    _cnt_temp.myNvcsw = 0;
    _cnt_temp.myNivcsw = 0;
    _cnt = count_map.lookup_or_init(&_pid, &_cnt_temp);
    _cnt->myNvcsw = prev->nvcsw;
    _cnt->myNivcsw = prev->nivcsw;

        // counting next task's
    //_cnt = count_map.lookup_or_init((u32*)(next->pid), &_cnt_temp2);
    //_cnt->myNvcsw = next->nvcsw;
    //_cnt->myNivcsw = next->nivcsw;

    return 0;
}
