from bcc import BPF
import time
import sys
import argparse
import os
import multiprocessing
from event_function import *

parser = argparse.ArgumentParser(description = "Notifier usage\nex) sudo python tester.py --event task.create --condition \"count > 1\" --time 10 --script \"bash script.sh\"")
parser.add_argument("--event", type=str, default=None, help = "the kind of event that you want notify")
parser.add_argument("--condition", type=str, default=None, help = "the condition expression you want to notify that moment")
parser.add_argument("--time", type=int, default=5, help = "timeout second")
parser.add_argument("--script", type=str, default=None, help = "the script to be executed after event happens")
args = parser.parse_args()

if args.event:
    event = args.event
    print ("event: %s" % (event))
if args.condition:
    expr = args.condition
    print ("condition expression: %s" % (expr))
if args.time:
    interval = args.time
    print ("timeout: %u" % (interval))
if args.script:
    shscript = args.script
    print ("script: %s" % (shscript))

def print_map():
    print ("-------------------")
    map_name = 'map'
    i = 0;
    for k,v in b[map_name].items():
        if i == 1:
            print("speed per sec : %u" %(v.count))
            return

        print ("total count : %u" % (v.count))
        i= i+1
        try:
            print ("total size : %u" % (v.size))
        except:
            pass

flag = False
def call_back (pid, call_chain):
    global flag
    if flag is False:
        flag = True
        print ("-------------------")
        os.system(shscript)
    #for idx in call_chain:
    #    print(b.ksym(idx))
    #b.trace_print()

if len(sys.argv) == 1:
    print " "
    exit()


EVENT_LIST = {
        "task.create" : task_create(),
        "task.exec" : task_exec(),
        "task.exit" : task_exit(),
        "task.switch" : task_switch(),
        "memory.alloc" : memory_alloc(),
        "memory.free" : memory_free(),
        "memory.alloc_page" : memory_alloc_page(),
        #"memory.free_page" : ["memory/memory_free_page.c", "__free_pages_ok", "memory_free_page_begin", "memory_free_page", "free_hot_cold_page", "memory_free_page_order_zero_begin"],
        "memory.reclaim" : memroy_reclaim(),
        "memory.reclaim_direct" : memory_reclaim_direct(),
        "fs.pagecache_access" : fs_pagecache_access(),
        "fs.pagecache_miss" : fs_pagecache_miss(),
        "fs.read_ahead" : fs_read_ahead(),
        "fs.page_writeback_bg" : fs_page_writeback_bg(),
        "fs.page_writeback_per_inode" : fs_page_writeback_per_inode(),
        "network.tcp_send" : network_tcp_send(),
        "network.tcp_recv" : network_tcp_recv(),
        "network.udp_send" : network_udp_send(),
        "network.udp_recv" : network_udp_recv(),
        }



rep = "EXPRESSION"
(cfile, event_name) = EVENT_LIST[event]
bpf_code = cfile.replace(rep, expr)

b = BPF(text = bpf_code, cb = call_back, debug=0)

b.attach_kprobe(event_re="(__free_pages_ok|free_hot_cold_page)", fn_name=memory_free_page_order_zero )

#for i in range(0, multiprocessing.cpu_count()):
#    b.attach_kprobe(event = event_name, fn_name = 'func', cpu=i)

interval = interval * 1000
b.kprobe_poll(timeout = interval)



print_map()

exit()
