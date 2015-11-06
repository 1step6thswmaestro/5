/*
 * Event : task.switch
 * Data to crawl : total count
 * Used Kernel-function : finish_task_switch
 */

#include <uapi/linux/ptrace.h>

#define NUM_ARRAY_MAP_SIZE 3
#define NUM_MAP_INDEX 0
#define NUM_MAP_INDEX2 1
#define NUM_MAP_INDEX3 2
#define NUM_SEC 1000000000

struct task_switch_value
{
    u64 count;
};

    // map where we save total count
BPF_TABLE("array", int, struct task_switch_value, task_switch_map, NUM_ARRAY_MAP_SIZE);

    // add task_switch_value.count one when finish_task_switch is called
int task_switch_begin(struct pt_regs *ctx)
{
    struct task_switch_value *val, val_temp, *val_time, *val_sec;
    int map_index = NUM_MAP_INDEX;
    int map_time_index = NUM_MAP_INDEX2;
    int map_sec_index = NUM_MAP_INDEX3;
    u64 cnt, spd;
    u64 tim = bpf_ktime_get_ns();
    val_temp.count = 0;

    val = task_switch_map.lookup_or_init(&map_index, &val_temp);
    val_time = task_switch_map.lookup_or_init(&map_time_index, &val_temp);
    val_sec = task_switch_map.lookup_or_init(&map_sec_index, &val_temp);
    //store base time
    if (val_time->count == 0 || tim - (val_time->count) > NUM_SEC){
        val_time->count = tim;
        val_sec->count = 1;
    }
    else{
        val_sec->count += 1;
    }
    spd = val_sec->count;

    ++(val->count);

    cnt = val->count;
    if (EXPRESSION)
        return 1;

    return 0;
}
