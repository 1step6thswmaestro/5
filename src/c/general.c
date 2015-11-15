#define pr_fmt(fmt) "BPF:"fmt
#define KBUILD_MODNAME ""
#include <uapi/linux/ptrace.h>
HEADER

#define NUM_ARRAY_MAP_SIZ 2
#define NUM_MAP_VAL_INDEX 0
#define NUM_MAP_SPD_INDEX 1
#define NUM_SEC 1000000000

struct value
{
    u64 count;
    u64 size;
};

BPF_TABLE("array", int, struct value, map, NUM_ARRAY_MAP_SIZ);

int func(struct pt_regs * ctx PARAMETER)
{
    struct value *val, *val_spd, val_temp;
    int map_index = NUM_MAP_VAL_INDEX;
    int map_spd_index = NUM_MAP_SPD_INDEX;
    u64 cnt, siz, spd, tim = bpf_ktime_get_ns();
    val_temp.count = 0;
    val_temp.size = 0;
    CHECK

    val_spd = map.lookup_or_init(&map_spd_index, &val_temp);
    val = map.lookup_or_init(&map_index, &val_temp);
    val->size += SIZE;
    ++(val->count);

    if (val_spd->count == 0 || tim - (val_spd->size) > NUM_SEC)
    {
        val_spd->size = tim;
        val_spd->count = 1;
    }
    else
        val_spd->count += 1;

    spd = val_spd->count;
    cnt = val->count;
    siz = val->size;

    return 0;
}
