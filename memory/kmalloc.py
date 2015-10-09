from bcc import BPF
from time import sleep

b = BPF(src_file = "kmalloc.c")

b.attach_kprobe(event = "__kmalloc", fn_name = "kmal")



do_exit = 0
while 1:
    sleep(5)

    try:
        for k, v in b["info"].items():
            print "pid : %s , allocate size %d" %(k.value,v.allocate_size)
    except KeyboardInterrupt:
        do_exit = 1
    
    if do_exit:
        exit()
