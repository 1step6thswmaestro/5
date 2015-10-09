#include <uapi/linux/ptrace.h>
#include <linux/sched.h>

BPF_TABLE("array",int,u64,dist,1024);

int kprobe___do_fork(struct pt_regs *ctx, unsigned long clone_flags) {
	int lowbit = clone_flags & 1023;
    int n=0;
    bpf_probe_read(&n, sizeof(int), (void*)0xffffffff81ef2f24); 
    bpf_trace_printk("===%d", n);
	u64 zero = 0;
	u64* tmp = dist.lookup_or_init(&lowbit, &zero);
	if(tmp)
	{
		(*tmp)++;
	}
	return 0;
}

