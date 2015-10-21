/*
 * Event : memory.alloc_page
 * Data to crawl : total count, total size
 * Used Kernel-function : __alloc_pages_nodemask
 */

#include <uapi/linux/ptrace.h>

#define NUM_ARRAY_MAP_SIZE 1
#define NUM_MAP_INDEX 0

struct memory_alloc_page_value
{
    u64 count;
    u64 size;
};

    // map where we save total count and size
BPF_TABLE("array", int, struct memory_alloc_page_value, memory_alloc_page_map, NUM_ARRAY_MAP_SIZE);

    // add memory_alloc_page_value.count one
    // add memory_alloc_page_value.size allocated page size, 'order'
    // when __alloc_pages_nodemask is called
int memory_alloc_page_begin(struct pt_regs *ctx, unsigned int order)
{
    struct memory_alloc_page_value *val, val_temp;
    int map_index = NUM_MAP_INDEX;
    u64 cnt, siz;
    val_temp.count = 0;
    val_temp.size = 0;
    
    val = memory_alloc_page_map.lookup_or_init(&map_index, &val_temp);
    ++(val->count);
    val->size += (u64)order;
    
    cnt = val->count;
    siz = val->size;
    if (EXPRESSION)
        return 1;

    return 0;
}
