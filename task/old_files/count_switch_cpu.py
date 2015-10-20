#!/usr/bin/python

from bcc import BPF
from time import sleep

b = BPF(src_file="count_switch_cpu.c")
KERN_FUNC = "finish_task_switch"
sleep_time = 2

b.attach_kprobe(event = KERN_FUNC, fn_name = "myCount_switch_cpu")

sleep(sleep_time)

switch_data_dict = {}

for k,v in b["count_map"].items():
    print ("--------------------------------------------------------------")
    print ("|  pid[%5d] was switched [%5u] times by core number[%2d]  |" % (k.pid, v.value, k.cpu))
    if (switch_data_dict.get(k.cpu) is None):
        switch_data_dict[k.cpu] = v.value
    else:
        switch_data_dict[k.cpu] += v.value

print ("--------------------------TOTAL-------------------------------")

for k,v in switch_data_dict.items():
    print ("*        core number[%2d] switched total [%5u] times        *" % (k, v))

print ("--------------------------------------------------------------")
