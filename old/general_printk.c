/*
 * Event : general.printk
 * Data to crawl : total count
 * Used Kernel-function : printk
 */

#include <uapi/linux/ptrace.h>

#define NUM_ARRAY_MAP_SIZE 1
#define NUM_MAP_INDEX 0

struct general_printk_value
{
    u64 count;
};

    // map where we save total count and size
BPF_TABLE("array", int, struct general_printk_value, general_printk_map, NUM_ARRAY_MAP_SIZE);

    // add general_printk_value.count one
    // when printk is called
int general_printk_begin(struct pt_regs *ctx)
{
    struct general_printk_value *val, val_temp;
    int map_index = NUM_MAP_INDEX;
    u64 cnt;
    val_temp.count = 0;
    
    val = general_printk_map.lookup_or_init(&map_index, &val_temp);
    ++(val->count);
    
    cnt = val->count;
    if (EXPRESSION)
        return 1;

    return 0;
}
