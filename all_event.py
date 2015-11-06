from bcc import BPF
import time
import sys
import os
import httplib
from multiprocessing import Process
from event_function import *


ES_URL = 'localhost:9200'
conn = None


def trace_begin():
    global conn, ES_INDEX
    conn = httplib.HTTPConnection(ES_URL)
    now = time.time()
    mapping = '''{
    "mappings" : {
        "events" : {
            "properties":{
                "event" : { "type" : "string" , "index" : "not_analyzed"} ,
                "count" : { "type" : "long"},
                "size" : { "type" : "long"},
                "time" : { "type" : "date", "format": "dateOptionalTime"}
            }
        }
    }
    }
    '''

    conn.request("PUT", "/lden", mapping)
    resp= conn.getresponse()
    data = resp.read()
    if resp.status != 200:
        print data

def trace_end():
    global conn
    conn.close()

def process_event(event, count, size, timestamp):
    global conn, now, now_sec
    body = '''
    {
    "event" : "%s",
    "count" : %d,
    "size" : %d,
    "time" : "%s"
    }''' %(event, count, size, timestamp)

    conn.request('POST', '/lden/events', body)
    resp = conn.getresponse()
    data = resp.read()
    if resp.status != 201:
        print "post document: ", resp.status, ":", resp.reason
        print data


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
    count = 0
    size = 0
    while 1:
        time.sleep(1)
        for k,v in b["map"].items():
            count = v.count
            size = v.size
            break
        timestamp = time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime())
        process_event(event.replace('.','_'), count, size, timestamp)




if __name__ == "__main__":
    task_list = []
    trace_begin()
    for k in EVENT_LIST.keys():
        task_list.append(Process(target=run_event_tracing, args=(k,)))
    for p in task_list:
        p.start()


    while 1:
        time.sleep(1)

