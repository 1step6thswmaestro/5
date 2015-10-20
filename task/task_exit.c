/*
 * Event : task.exit
 * Data to crawl : total count
 * Used Kernel-function : do_exit
 */

#include <uapi/linux/ptrace.h>

#define NUM_ARRAY_MAP_SIZE 1
#define NUM_MAP_INDEX 0

struct task_exit_value
{
    u64 count;
};

    // map where we save total count
BPF_TABLE("array", int, struct task_exit_value, task_exit_map, NUM_ARRAY_MAP_SIZE);

    // add task_exit_value.count one when do_exit is called
int task_exit_begin(struct pt_regs *ctx)
{
    struct task_exit_value *val, val_temp;
    int map_index = NUM_MAP_INDEX;
    u64 cnt;
    val_temp.count = 0;
    
    val = task_exit_map.lookup_or_init(&map_index, &val_temp);
    ++(val->count);

    cnt = val->count;
    if (EXPRESSION)
        return 1;

    return 0;
}
