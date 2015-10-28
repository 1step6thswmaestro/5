from bcc import BPF
import time
import sys
import argparse

#default
event_num = 5 
interval = 5
event = 0

parser = argparse.ArgumentParser(description = "parsing arguemnt")
parser.add_argument("-n", type=int, help="the number of events for notify")
parser.add_argument("-t", type=int, help="timeout second")
parser.add_argument("-e", help = "kind of event that you want notify")
args = parser.parse_args()

if args.n:
    event_num = args.n
    print event_num

if args.t:
    interval = args.t
    print interval

if args.e:
    event = args.e
    print event



def call_back (pid, call_chain):
    print "evnet happen"

if len(sys.argv) == 1:
    print " "
    exit()

FUNC_NAME = ["sys_clone", "finish_task_switch"]

with open("sys_fork.c", 'r') as f:
    cfile = f.read()

rep = "NUM"
bpf_code = cfile.replace(rep, str(event_num))

b = BPF(text = bpf_code, cb = call_back)
b.attach_kprobe(event = "sys_clone", fn_name = "count_sys_fork")
interval = interval*1000
b.kprobe_poll(timeout = interval)



exit()

