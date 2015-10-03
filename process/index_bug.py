from bcc import BPF
from time import sleep


b = BPF(src_file = "index_bug.c")
b.attach_kprobe(event = "sys_clone", fn_name = "index_sys_clone")

interval = 5
do_exit = 0

while 1:
    for k,v in b["dist"].items():
        print (k.value, v.value)
    try:
        sleep(interval)
    except KeyboardInterrupt:
        pass; do_exit = 1

    if do_exit:
        exit()



