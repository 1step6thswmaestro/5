/*
 * Author : Dr.Zix
 * Event : task.switch
 * Data to crawl : total count
 * Used Kernel-function : finish_task_switch
 */

#include <uapi/linux/ptrace.h>

#define NUM_ARRAY_MAP_SIZE 1
#define NUM_MAP_INDEX 0

struct task_switch_value
{
    u64 count;
};

    // map where we save total count
BPF_TABLE("array", int, struct task_switch_value, task_switch_map, NUM_ARRAY_MAP_SIZE);

    // add task_switch_value.count one when finish_task_switch is called
int task_switch_begin(struct pt_regs *ctx)
{
    struct task_switch_value *val, val_temp;
    int count, map_index = NUM_MAP_INDEX;
    val_temp.count = 0;
    
    val = task_switch_map.lookup_or_init(&map_index, &val_temp);
    ++(val->count);

    count = val->count;
    if (EXPRESSION)
        return 1;

    return 0;
}
