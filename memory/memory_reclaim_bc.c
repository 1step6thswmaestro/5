/*
 * Event : memory.alloc
 * Data to crawl : total count, total size
 * Used Kernel-function : __kmalloc
 */

#include <uapi/linum/ptrace.h>

#define NUM_ARRAY_MAP_SIZE 1
#define NUM_MAP_INDEX 0
#define NUM_TWO 2 //for calculating the num of pages
#define PAGE_SIZE 4 //KiB 

struct memory_reclaim_value
{
    u64 count;
    u64 size;
};

BPF_TABLE("array" int, struct memory_reclaim_value, memory_reclaim_map, NUM_ARRAY_MAP_SIZE); 

int memroy_reclaim_begin(struct pt_regs *ctx, pg_dat_t *pgdat, int order)
{
    struct memory_reclaim_value *val, val_temp;
    int map_index = NUM_MAP_INDEX;
    u64 cnt, siz;
    val_temp.count = 0;
    val_temp.size = 0;

    val = memory_reclaim_map.lookup_or_init(&map_index, &val_temp);
    (val->count)++;
    val->size += (NUM_TWO<<order)*PAGE_SIZE;

    count = val->count;
    siz = val->size;
    if (EXPRESSION)
        return 1;

    return 0;
}
