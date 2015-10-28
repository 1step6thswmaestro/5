#!/usr/bin/python
from bcc import BPF
from time import sleep
import sys

b = BPF(src_file = "simple2.c", debug=6)

FUNC_NAME = "__kmalloc"

b.attach_kprobe(event = FUNC_NAME, fn_name = "malloc_call")
sleep(3)
for k,v in b["simple_map"].items():
    print ("cnt = %d" % (v.value))
