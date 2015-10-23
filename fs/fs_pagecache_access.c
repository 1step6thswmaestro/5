/*
 * Event : fs.pagecache_access
 * Data to crawl : total count
 * Used Kernel-function : pagecache_get_page
 */

#include <uapi/linux/ptrace.h>
//#include <linux/fs.h>

#define NUM_ARRAY_MAP_SIZE 1
#define NUM_MAP_INDEX 0

struct fs_pagecache_access_value
{
    u64 count;
};

    // map where we save total count
BPF_TABLE("array", int, struct fs_pagecache_access_value, fs_pagecache_access_map, NUM_ARRAY_MAP_SIZE);

    // add fs_pagecache_access_value.count one
    // when pagecached_get_page is called
int fs_pagecache_access_begin(struct pt_regs *ctx)//, struct address_space *mapping)
{
    struct fs_pagecache_access_value *val, val_temp;
    int map_index = NUM_MAP_INDEX;
    u64 cnt;
    val_temp.count = 0;
    //bpf_trace_printk("sb: %d, ino: %d\n", mapping->host->i_sb->s_dev, mapping->host->i_ino);
    val = fs_pagecache_access_map.lookup_or_init(&map_index, &val_temp);
    ++(val->count);
    
    cnt = val->count;
    //if (mapping->host->i_ino == 1601565)
    if (EXPRESSION)
        return 1;

    return 0;
}
