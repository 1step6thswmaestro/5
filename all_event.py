from bcc import BPF
import time
import sys
import os
from multiprocessing import Process
from event_function import *


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
        #"memory.reclaim_direct" : memory_reclaim_direct(),
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
def run_event_tracing(event):
    (cfile, event_name) = EVENT_LIST[event]
    bpf_code = cfile.replace("EXPRESSION", "0")
    b = BPF(text = bpf_code)
    b.attach_kprobe(event=event_name, fn_name='func')
    while 1:
        time.sleep(1)
        for k,v in b["map"].items():
            print event, v.count, v.size


if __name__ == "__main__":
    task_list = []
    for k in EVENT_LIST.keys():
        task_list.append(Process(target=run_event_tracing, args=(k,)))
    for p in task_list:
        p.start()


    while 1:
        time.sleep(1)

