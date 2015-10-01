#include <uapi/linux/ptrace.h>
#include <linux/gfp.h>

#define NUM_GFP_FLAG 25

struct malloc_data{
	size_t size;
	u64 flag[NUM_GFP_FLAG];
};

BPF_HASH(simple_map, u32, struct malloc_data);

int malloc_call(struct pt_regs *ctx, size_t size, gfp_t flags)
{
	u32 pid = bpf_get_current_pid_tgid();
	struct malloc_data* leaf = simple_map.lookup(&pid);
	
	if (leaf)
	{
		leaf->size += size;
		leaf->flag[flags % NUM_GFP_FLAG]++;
	}
	else
	{
		struct malloc_data new_data;
		new_data.size = size;
		for (int i = 0; i < NUM_GFP_FLAG; ++i)
			new_data.flag[i] = 0;
		new_data.flag[flags % NUM_GFP_FLAG]++;
		simple_map.update(&pid, &new_data);
	}

	return 0;
}
