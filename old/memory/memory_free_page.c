/*
 * Event : memory.free_page
 * Data to crawl : total count, total size
 * Used Kernel-function : free_hot_cold_page, __free_pages_ok
 */

#include <uapi/linux/ptrace.h>
#include <linux/pagevec.h>

#define NUM_ARRAY_MAP_SIZE 1
#define NUM_MAP_INDEX 0

struct memory_free_page_value
{
    u64 count;
    u64 size;
};

    // map where we save total count and size
BPF_TABLE("array", int, struct memory_free_page_value, memory_free_page_map, NUM_ARRAY_MAP_SIZE);

    // add memory_free_page_value.count one
    // add memory_free_page_value.size freed page size, pow('order', 2)
    // when __free_pages_ok is called
int memory_free_page_begin(struct pt_regs *ctx, struct page *page, unsigned int order)
{
    struct memory_free_page_value *val, val_temp;
    int map_index = NUM_MAP_INDEX;
    u64 cnt, siz;
    val_temp.count = 0;
    val_temp.size = 0;
    
    val = memory_free_page_map.lookup_or_init(&map_index, &val_temp);
    ++(val->count);
    val->size += 1 << (u64)order;
    
    cnt = val->count;
    siz = val->size;
    if (EXPRESSION)
        return 1;

    return 0;
}

int memory_free_page_order_zero_begin(struct pt_regs *ctx)
{
    struct memory_free_page_value *val, val_temp;
    int map_index = NUM_MAP_INDEX;
    u64 cnt, siz;
    val_temp.count = 0;
    val_temp.size = 0;
                        
    val = memory_free_page_map.lookup_or_init(&map_index, &val_temp);
    ++(val->count);
    ++(val_temp.size);

    cnt = val->count;
    siz = val->size;
    if (EXPRESSION)
        return 1;

    return 0;
}
