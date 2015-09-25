#!/usr/bin/python
from bcc import BPF
from time import sleep
import sys

b = BPF(src_file = "function_analyzer.c",debug = 6)

func_name = "sys_clone"
if len(sys.argv)>1:   
    func_name = sys.argv[1]


b.attach_kprobe(event = func_name, fn_name="function_start")

b.attach_kretprobe(event = func_name, fn_name="function_exit")

sleep(10)

fun_data = {
        "count" : 0,
        "total_time" : 0,
        "min_time" : None,
        "max_time" : 0
        }



for k,v in b["result"].items():
    if v.count == 0:
        continue
    fun_data["count"] += v.count
    fun_data["total_time"] += v.total_time
    if fun_data["min_time"] is None or fun_data["min_time"]> v.min_time:
        fun_data["min_time"] = v.min_time

    print type(v.min_time)
    if fun_data["max_time"]< v.max_time:
        fun_data["max_time"] = v.max_time


for k, v in fun_data.items():
    if v is None:
        print "no process exec"
        continue
    print (k, v)









    

