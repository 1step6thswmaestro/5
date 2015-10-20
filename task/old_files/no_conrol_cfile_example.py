#!/usr/bin/python

from bcc import BPF
from time import sleep
import sys

b = BPF(src_file="count_switch_cpu.c")
KERN_FUNC = "finish_task_switch"

b.attach_kprobe(event = KERN_FUNC, fn_name = "myCount_switch_cpu")

if (sys.argv[1] is None or sys.argv[2] is None):
    print("argv err")

break_count = 0
play_time = 0

if "-n" in sys.argv:
    break_count = int(sys.argv[sys.argv.index("-n") + 1])
if "-t" in sys.argv:
    play_time = int(sys.argv[sys.argv.index("-t") + 1])

while (True):
    count_sum = 0
    for k,v in b["count_map"].items():
        count_sum += v.value
    
    if (count_sum >= break_count):
        print ("PUSH! %5d" % (count_sum))
        break
