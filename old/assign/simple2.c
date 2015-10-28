#include <uapi/linux/ptrace.h>

BPF_TABLE("array", int, int, simple_map, 5);

int malloc_call(struct pt_regs *ctx)
{
    int index = 0;
    int *val, val_temp;
    val_temp = 0;
    val = simple_map.lookup_or_init(&index, &val_temp);
    *val /= 3;

    return 0; 
}
