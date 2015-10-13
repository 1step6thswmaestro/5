from bcc import BPF
from time import sleep

b = BPF(src_file = "page_fault.c")

b.attach_kprobe(event = "finish_task_switch", fn_name = "count_page_fault")

do_exit = 0
while 1:
    sleep(3)

    try:
        for k, v in b["info"].items():
            print "pid %5s, minor : %8d, major : %8d"%(k.value, v.min_flt, v.maj_flt)

    except KeyboardInterrupt:
        do_exit = 1
    if do_exit:
        break

