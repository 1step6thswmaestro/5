/*
 * Event : fs.page_writeback_bg
 * Data to crawl : total count, total size
 * Used Kernel-function : wb_start_background_writeback
 */

#include <uapi/linux/ptrace.h>
#include <linux/backing-dev-defs.h>

#define NUM_ARRAY_MAP_SIZE 1
#define NUM_MAP_INDEX 0

struct fs_page_writeback_bg_value
{
    u64 count;
    u64 size;
};

BPF_TABLE("array", int, struct fs_page_writeback_bg_value, fs_page_writeback_bg_map, NUM_ARRAY_MAP_SIZE);

int fs_page_writeback_bg_begin(struct pt_regs *ctx, struct bdi_writeback * wb){
    struct fs_page_writeback_bg_value *val, val_temp;
    int map_index = NUM_MAP_INDEX;
    u64 cnt, siz;
    val_temp.count = 0;
    val_temp.size = 0;

    val = fs_page_writeback_bg_map.lookup_or_init(&map_index, &val_temp);
    ++(val->count);
    //val->size +=
    //need to find size variable in struct bdi_writeback *wb

    cnt = val->count;
    siz = val->size;
    if(EXPRESSION)
        return 1;

    return 0;
}
