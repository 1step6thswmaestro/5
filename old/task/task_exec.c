/*
 * Event : task.exec
 * Data to crawl : total count
 * Used Kernel-function : do_execveat_common.isra.34
 */

#include <uapi/linux/ptrace.h>

#define NUM_ARRAY_MAP_SIZE 1
#define NUM_MAP_INDEX 0

struct task_exec_value
{
    u64 count;
};

    // map where we save total count
BPF_TABLE("array", int, struct task_exec_value, task_exec_map, NUM_ARRAY_MAP_SIZE);

    // add task_exec_value.count one when do_execveat_common.isra.34 is called
int task_exec_begin(struct pt_regs *ctx)
{
    struct task_exec_value *val, val_temp;
    int map_index = NUM_MAP_INDEX;
    u64 cnt;
    val_temp.count = 0;
    
    val = task_exec_map.lookup_or_init(&map_index, &val_temp);
    ++(val->count);
    
    cnt = val->count;
    if (EXPRESSION)
        return 1;

    return 0;
}
