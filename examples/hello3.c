#include <uapi/linux/ptrace.h>


BPF_TABLE("array",int,u64,dist,1024);

int kprobe___do_fork(struct pt_regs *ctx, unsigned long clone_flags) {
	int lowbit = clone_flags & 1023;
	u64 zero = 0;
	u64* tmp = dist.lookup_or_init(&lowbit, &zero);
	if(tmp)
	{
		(*tmp)++;
	}
	return 0;
}

