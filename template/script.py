from bcc import BPF
import time
import sys


def call_back (pid, call_chain):
    print "evnet happen"

if len(sys.argv) == 1:
    print " "
    exit()

FUNC_NAME = ["sys_clone", "finish_task_switch"]

#default
event_num = 5 
interval = 5
event = 0
if "-n" in sys.argv:
    event_num = int(sys.argv[sys.argv.index("-n")+1])

if "-t" in sys.argv:
    interval = int(sys.argv[sys.argv.index("-t")+1])

with open("sys_fork.c", 'r') as f:
    cfile = f.read()

rep = "NUM"
bpf_code = cfile.replace(rep, str(event_num))

b = BPF(text = bpf_code, cb = call_back)
b.attach_kprobe(event = "sys_clone", fn_name = "count_sys_fork")
interval = interval*1000
b.kprobe_poll(timeout = interval)



exit()

