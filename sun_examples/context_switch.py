from bcc import BPF
from time import sleep

b =BPF(src_file= "context_switch.c")
b.attach_kprobe(event="finish_task_switch", fn_name="count_sched");

interval = 3;


while True:

    sleep(interval)
    
    for k,v in b["stats"].items():
        print ("%5d, %u") %(k.pre_pid, v)
    print ("ci")
