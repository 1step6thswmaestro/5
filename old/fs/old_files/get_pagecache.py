#!/usr/bin/python

from bcc import BPF
from time import sleep

b = BPF(src_file="get_pagecache.c")
KERN_FUNC = "pagecache_write_end"
sleep_time = 3

b.attach_kprobe(event = KERN_FUNC, fn_name = "myGet_pagecache")

sleep(sleep_time)

for k,v in b["cache_map"].items():
    print ("--------------------------------------------------------------")
    print ("%s, %d" % (v.name, v.size))

