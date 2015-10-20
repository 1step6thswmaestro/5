#include <uapi/linux/ptrace.h>
#include <linux/sched.h>

struct task_page_info{
    unsigned long min_flt;
    unsigned long maj_flt;

};

BPF_HASH( info, u32, struct task_page_info);

int count_page_fault(struct pt_regs *ctx, struct task_struct *prev){
    struct task_page_info init_info ={0,0};
    struct task_page_info *leaf;
    u32 pid = prev->pid;
    leaf = info.lookup_or_init(&pid, &init_info);
    leaf -> min_flt = prev->min_flt;
    leaf -> maj_flt = prev->maj_flt;
    return 0;
}
