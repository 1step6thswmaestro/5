#!/usr/bin/python
from bcc import BPF
from time import sleep
import sys
def call_back(pid, callchain):
    print (pid)
    for i in callchain:
        print (BPF.ksym(i))


b = BPF(src_file = "simple.c",cb = call_back)

FUNC_NAME = "__kmalloc"
FLAG_NUM = 25

b.attach_kprobe(event = FUNC_NAME, fn_name = "malloc_call")
b.kprobe_poll()


for k,v in b["simple_map"].items():
    print ("pid : %5d, size = %d" %(k.value, v.value))

for k,v in b["flag"].items():
    print (" %d, %d" %(k.value, v.value))


