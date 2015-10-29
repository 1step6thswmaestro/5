/*
 * Event : custom
 * Data to crawl : total count
 * Used Kernel-function : Everything in /proc/kallsyms
 */

#include <uapi/linux/ptrace.h>

#define NUM_ARRAY_MAP_SIZE 1
#define NUM_MAP_INDEX 0

struct custom_value
{
    u64 count;
};

    // map where we save total count
BPF_TABLE("array", int, struct custom_value, custom_map, NUM_ARRAY_MAP_SIZE);

    // add custom_value.count one when selected function is called
int custom_begin(struct pt_regs *ctx)
{
    struct custom_value *val, val_temp;
    int map_index = NUM_MAP_INDEX;
    u64 cnt;
    val_temp.count = 0;
    
    val = custom_map.lookup_or_init(&map_index, &val_temp);
    ++(val->count);
    
    cnt = val->count;
    if (EXPRESSION)
        return 1;

    return 0;
}
