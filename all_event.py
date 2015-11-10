from bcc import BPF
import time
import sys
import os
import httplib
from multiprocessing import Process
from include.evtmanage import EventManager


ES_URL = 'localhost:9200'
conn = None

bulk = ''
header = '{"create":{"_index":"lden", "_type":"events"}}\n'

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
EVENT_LIST_data = {
        "task.create" : {"count" : 0 , "size" : 0},
        "task.exec" :  {"count" : 0 , "size" : 0},
        "task.exit" :  {"count" : 0 , "size" : 0},
        "task.switch" :  {"count" : 0 , "size" : 0},
        "memory.alloc" :  {"count" : 0 , "size" : 0},
        "memory.free" :  {"count" : 0 , "size" : 0},
        "memory.alloc_page" :  {"count" : 0 , "size" : 0},
        #"memory.free_page" : ["memory/memory_free_page.c", "__free_pages_ok", "memory_free_page_begin", "memory_free_page", "free_hot_cold_page", "memory_free_page_order_zero_begin"],
        "memory.reclaim" :  {"count" : 0 , "size" : 0},
        #"memory.reclaim_direct" : memory_reclaim_direct(),
        "fs.pagecache_access" :  {"count" : 0 , "size" : 0},
        "fs.pagecache_miss" :  {"count" : 0 , "size" : 0},
        "fs.read_ahead" :  {"count" : 0 , "size" : 0},
        "fs.page_writeback_bg" :  {"count" : 0 , "size" : 0},
        "fs.page_writeback_per_inode" :  {"count" : 0 , "size" : 0},
        "network.tcp_send" :  {"count" : 0 , "size" : 0},
        "network.tcp_recv" :  {"count" : 0 , "size" : 0},
        "network.udp_send" :  {"count" : 0 , "size" : 0},
        "network.udp_recv" :  {"count" : 0 , "size" : 0}
        }

def run_event_tracing(b, event):
    global bulk, header

    count = 0
    size = 0
    for k, v in b["map"].items():
        count = v.count - EVENT_LIST_data[event]["count"]
        size = v.size - EVENT_LIST_data[event]["size"]
        EVENT_LIST_data[event]["count"] = v.count
        EVENT_LIST_data[event]["size"] = v.size
        break
    timestamp = time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime())
    bulk += header
    bulk += '{ "event" : "%s", "count" : %d, "size" : %d, "time" : "%s"}\n' %(event.replace('.','_'), count, size, timestamp)


if __name__ == "__main__":
    manager = EventManager()
    task_list = []
    trace_begin()
    for k in manager.EVENT_LIST.keys():
        (cfile, event_name) = manager.EVENT_LIST[k]
        bpf_code = cfile.replace("EXPRESSION", "0")
        b = BPF(text=bpf_code)
        b.attach_kprobe(event=event_name, fn_name='func')
        task_list.append((b, k))

    current_time = time.time()
    sleep_time = int(current_time)+1 - current_time

    while 1:
        bulk = ''
        time.sleep(sleep_time)
        for i, v in task_list:
            run_event_tracing(i, v)  # i is bpf object, v is eventname

        bulk += '\n'
        conn.request('POST', '/_bulk', bulk)
        resp = conn.getresponse()
        data = resp.read()
        if resp.status != 200 and resp.status != 201:
            print "post document: ", resp.status, ":", resp.reason
            print data
        start = time.time()
        sleep_time = int(start) + 1 - start
