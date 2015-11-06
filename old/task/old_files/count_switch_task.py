#!/usr/bin/python

from bcc import BPF
from time import sleep

b = BPF(src_file="count_switch_task.c")
KERN_FUNC = "finish_task_switch"
sleep_time = 1

b.attach_kprobe(event = KERN_FUNC, fn_name = "myCount_switch_task")

sleep(sleep_time)

#sorted(b["count_map"])
for k,v in b["count_map"].items():
    print ("---------------------------------")
    print ("task_id[%5d]'s nvcsw : %u" % (k.value, v.myNvcsw))
    print ("task_id[%5d]'s nivcsw : %u" % (k.value, v.myNivcsw))
