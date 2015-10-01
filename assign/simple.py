#!/usr/bin/python
from bcc import BPF
from time import sleep
import sys

b = BPF(src_file = "simple.c", debug=6)

FUNC_NAME = "__kmalloc"
FLAG_NUM = 25

b.attach_kprobe(event = FUNC_NAME, fn_name = "malloc_call")
sleep(5)

for k,v in b["simple_map"].items():
	print("pid(%5d) malloced %5d" % (k, v.size))
	for i in range(0, FLAG_NUM):
		print("No mean print, %u" % (v.flag[i]))

