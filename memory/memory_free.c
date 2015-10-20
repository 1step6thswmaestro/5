/*
 * Author : Dr.Zix
 * Event : memory.free
 * Data to crawl : total count, total size
 * Used Kernel-function : kfree
 */

#include <uapi/linux/ptrace.h>

#define NUM_ARRAY_MAP_SIZE 1
#define NUM_MAP_INDEX 0

struct memory_free_value
{
    u64 count;
};

    // map where we save total count
BPF_TABLE("array", int, struct memory_free_value, memory_free_map, NUM_ARRAY_MAP_SIZE);

    // add memory_free_value.count one when kfree is called
int memory_free_begin(struct pt_regs *ctx)
{
    struct memory_free_value *val, val_temp;
    int count, map_index = NUM_MAP_INDEX;
    val_temp.count = 0;
    
    val = memory_free_map.lookup_or_init(&map_index, &val_temp);
    ++(val->count);
    
    count = val->count;
    if (EXPRESSION)
        return 1;

    return 0;
}
