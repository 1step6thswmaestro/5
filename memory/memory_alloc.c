/*
 * Author : Dr.Zix
 * Event : memory.alloc
 * Data to crawl : total count, total size
 * Used Kernel-function : __kmalloc
 */

#include <uapi/linux/ptrace.h>

#define NUM_ARRAY_MAP_SIZE 1
#define NUM_MAP_INDEX 0

struct memory_alloc_value
{
    u64 count;
    u64 size;
};

    // map where we save total count
BPF_TABLE("array", int, struct memory_alloc_value, memory_alloc_map, NUM_ARRAY_MAP_SIZE);

    // add memory_alloc_value.count one when __kmalloc is called
int memory_alloc_begin(struct pt_regs *ctx, size_t size)
{
    struct memory_alloc_value *val, val_temp;
    int count, map_index = NUM_MAP_INDEX;
    val_temp.count = 0;
    val_temp.size = (u64)size;
    
    val = memory_alloc_map.lookup_or_init(&map_index, &val_temp);
    ++(val->count);
    val->size += (u64)size;
    
    count = val->count;
    size = val->size;
    if (EXPRESSION)
        return 1;

    return 0;
}
