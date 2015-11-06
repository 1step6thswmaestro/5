from bcc import BPF
from time import sleep

b = BPF(src_file = "kmalloc.c")

b.attach_kprobe(event = "__kmalloc", fn_name = "kmal")
b.attach_kprobe(event = "kfree", fn_name = "kfre")



do_exit = 0
while 1:
    sleep(5)

    try:
        for k, v in b["info"].items():
            print "pid : %5s, total alloc size %8d, max allo_size %8d, free_count %5d " %(k.value,v.total_allocate_size,v.max_allocate_size,  v.free_count)
    except KeyboardInterrupt:
        do_exit = 1
    
    if do_exit:
        exit()
