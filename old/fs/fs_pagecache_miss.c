/*
 * Event : fs.pagecache_miss
 * Data to crawl : total count
 * Used Kernel-function : page_cache_sync_readahead
 */

#include <uapi/linux/ptrace.h>

#define NUM_ARRAY_MAP_SIZE 1
#define NUM_MAP_INDEX 0

struct fs_pagecache_miss_value
{
    u64 count;
};

    // map where we save total count
BPF_TABLE("array", int, struct fs_pagecache_miss_value, fs_pagecache_miss_map, NUM_ARRAY_MAP_SIZE);

    // add fs_pagecache_miss_value.count one
    // when page_cache_sync_readahead is called
int fs_pagecache_miss_begin(struct pt_regs *ctx)
{
    struct fs_pagecache_miss_value *val, val_temp;
    int map_index = NUM_MAP_INDEX;
    u64 cnt;
    val_temp.count = 0;
    
    val = fs_pagecache_miss_map.lookup_or_init(&map_index, &val_temp);
    ++(val->count);
    
    cnt = val->count;
    if (EXPRESSION)
        return 1;

    return 0;
}
