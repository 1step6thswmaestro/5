/*
 * Event : fs.read_ahead
 * Data to crawl : total count, total size
 * Used Kernel-function : __do_page_cache_readahead
 */

#include <uapi/linux/ptrace.h>
#include <linux/mm_types.h>
#include <asm/page.h>

#define NUM_ARRAY_MAP_SIZE 1
#define NUM_MAP_INDEX 0

struct fs_read_ahead_value
{
    u64 count;
    u64 size;
};

BPF_TABLE("array", int, struct fs_read_ahead_value, fs_read_ahead_map, NUM_ARRAY_MAP_SIZE);

int fs_read_ahead_begin(struct pt_regs *ctx)
{
    struct fs_read_ahead_value *val, val_temp;
    int map_index = NUM_MAP_INDEX;
    u64 cnt, siz, look_ahead_size;
    val_temp.count = 0;
    val_temp.size = 0;
    look_ahead_size = ctx->r8;

    val = fs_read_ahead_map.lookup_or_init(&map_index, &val_temp);
    ++(val->count);
    val->size += look_ahead_size * PAGE_SIZE;

    cnt = val->count;
    siz = val->size;
    if (EXPRESSION)
        return 1;

    return 0;
}
