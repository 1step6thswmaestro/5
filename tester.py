from bcc import BPF
import time
import sys
import argparse
import os
import multiprocessing

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
    map_name = EVENT_LIST[event][3] + "_map"
    for k,v in b[map_name].items():
        print ("total count : %u" % (v.count))
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

def read_file(path):
    with open(path, 'r') as f:
        read_text = f.read()
    return read_text

def task_create():
    read_text = read_file("general/general.c")
    source = read_text.replace("HEADER", '')
    source = source.replace("PARAMETER", ' ' )
    source = source.replace("SIZE", '0')
    return (source, "_do_fork")

def task_exec():
    read_text = read_file("general/general.c")
    source = read_text.replace("HEADER", '')
    source = source.replace("PARAMETER", ' ' )
    source = source.replace("SIZE", '0')
    return (source, "do_execveat_common.isra.34")

def task_exit():
    read_text = read_file("general/general.c")
    source = read_text.replace("HEADER", '')
    source = source.replace("PARAMETER", ' ' )
    source = source.replace("SIZE", '0')
    return (source, "do_exit")

def task_switch():
    read_text = read_file("general/general.c")
    source = read_text.replace("HEADER", '')
    source = source.replace("PARAMETER", ' ' )
    source = source.replace("SIZE", '0')
    return (source, "finish_task_switch")

def memory_alloc():
    read_text = read_file("general/general.c")
    source = read_text.replace("HEADER", '')
    source = source.replace("PARAMETER", ', size_t size' )
    source = source.replace("SIZE", '(u64)size')
    return (source, "__kmalloc")

def memory_free():
    read_text = read_file("general/general.c")
    source = read_text.replace("HEADER", '')
    source = source.replace("PARAMETER", '' )
    source = source.replace("SIZE", '0')
    return (source, "kfree")

def memory_alloc_page():
    read_text = read_file("general/general.c")
    source = read_text.replace("HEADER", '')
    source = source.replace("PARAMETER", ', gfp_t gfp_mask, unsigned int order' )
    source = source.replace("SIZE", '1<<(u64)order')
    return (source, "__alloc_pages_nodemask")

def memory_free_page():
    read_text = read_file("general/general.c")
    source = read_text.replace("HEADER", '#include <linux/pagevec.h>')
    source = source.replace("PARAMETER", ', struct page *page, unsinged int order' )
    source = source.replace("SIZE", '1 << (u64)order')
    return (source, "__free_pages_ok")

def memroy_reclaim_bc():
    read_text = read_file("general/general.c")
    source = read_text.replace("HEADER", '#include <linux/mmzone.h>\n#include<asm>page.h>')
    source = source.replace("PARAMETER", ', pg_data_t *pgdat, int order')
    source = source.replace("SIZE", '(2<<order) * PAGE_SIZE')
    return (source, "balance_pgdat")


EVENT_LIST = {
        "task.create" : ["task/task_create.c", "_do_fork", "task_create_begin", "task_create"],
        "task.exec" : ["task/task_exec.c", "do_execveat_common.isra.34", "task_exec_begin", "task_exec"],
        "task.exit" : ["task/task_exit.c", "do_exit", "task_exit_begin", "task_exit"],
        "task.switch" : ["task/task_switch.c", "finish_task_switch", "task_switch_begin", "task_switch"],
        "memory.alloc" : ["memory/memory_alloc.c", "__kmalloc", "memory_alloc_begin", "memory_alloc"],
        "memory.free" : ["memory/memory_free.c", "kfree", "memory_free_begin", "memory_free"],
        "memory.alloc_page" : ["memory/memory_alloc_page.c", "__alloc_pages_nodemask", "memory_alloc_page_begin", "memory_alloc_page"],
        "memory.free_page" : ["memory/memory_free_page.c", "__free_pages_ok", "memory_free_page_begin", "memory_free_page", "free_hot_cold_page", "memory_free_page_order_zero_begin"],
        "memory.reclaim" : ["memory/memory_reclaim_bc.c", "balance_pgdat", "memory_reclaim_begin", "memory_reclaim"],
        "fs.pagecache_access" : ["fs/fs_pagecache_access.c", "pagecache_get_page", "fs_pagecache_access_begin", "fs_pagecache_access"],
        "fs.pagecache_miss" : ["fs/fs_pagecache_miss.c", "page_cache_sync_readahead", "fs_pagecache_miss_begin", "fs_pagecache_miss"],
        "fs.read_ahead" : ["fs/fs_read_ahead.c", "__do_page_cache_readahead", "fs_read_ahead_begin", "fs_read_ahead"],
        "fs.page_writeback_bg" : ["fs/fs_page_writeback_bg.c", "wb_start_background_writeback", "fs_page_writeback_bg_begin", "fs_page_writeback_bg"],
        "fs.page_writeback_per_inode" : ["fs/fs_page_writeback_per_inode.c", "__writeback_single_inode", "fs_page_writeback_per_inode_begin", "fs_page_writeback_per_inode"],
        "network.tcp_send" : ["network/network_tcp_send.c", "tcp_sendmsg", "network_tcp_send_begin", "network_tcp_send"],
        "network.tcp_recv" : ["network/network_tcp_recv.c", "tcp_recvmsg", "network_tcp_recv_begin", "network_tcp_recv"],
        "network.udp_send" : ["network/network_udp_send.c", "udp_sendmsg", "network_udp_send_begin", "network_udp_send"],
        "network.udp_recv" : ["network/network_udp_recv.c", "udp_recvmsg", "network_udp_recv_begin", "network_udp_recv"],
        "general.printk" : ["general/general_printk.c", "printk", "general_printk_begin", "general_printk"],
        "test.speed" : ["speedtest/task_switch.c", "finish_task_switch", "task_switch_begin", "task_switch"]
        }

#with open(EVENT_LIST[event][0], 'r') as f:
#    cfile = f.read()


rep = "EXPRESSION"
cfile = task_create()[0]
bpf_code = cfile.replace(rep, expr)

b = BPF(text = bpf_code, cb = call_back, debug=0)
b.attach_kprobe(event = task_create()[1], fn_name='func')

#for i in range(0, multiprocessing.cpu_count()):
#    b.attach_kprobe(event = EVENT_LIST[event][1], fn_name = EVENT_LIST[event][2], cpu=i)
#    if event == "memory.free_page":
#        b.attach_kprobe(event = EVENT_LIST[event][4], fn_name = EVENT_LIST[event][5], cpu=i)

interval = interval * 1000
b.kprobe_poll(timeout = interval)


#if (event == "test.speed"):
#    map_name = EVENT_LIST[event][3] + "_map"
#    for k,v in b[map_name].items():
#        print ("value : %d" %(v.count))


#print_map()

exit()
