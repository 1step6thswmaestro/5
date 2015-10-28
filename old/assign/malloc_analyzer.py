#!/usr/bin/python
from bcc import BPF
from time import sleep
import sys

b = BPF(src_file = "malloc_analyzer.c", debug=6)

FUNC_NAME = "__kmalloc"
FLAG_NUM = 25

b.attach_kprobe(event = FUNC_NAME, fn_name = "malloc_call")

sleep(5)

for k,v in b["pid_size"].items():
    print("size(%5d) malloc_call from pid(%5d): count->%u" % (k.size, k.pid, v.value))

for k,v in b["pid_total"].items():
    print("----------------------------------------------")
    print("pid(%5d) malloced total size of (%5d)" % (k, v.size))
    print("count of GFP_DMA : %u" % (v.flag[0]))
    print("count of GFP_HIGHMEM : %u" % (v.flag[1]))
    print("count of GFP_DMA32 : %u" % (v.flag[2]))
    print("count of GFP_MOVABLE : %u" % (v.flag[3]))
    print("count of GFP_WAIT : %u" % (v.flag[4]))
    print("count of GFP_HIGH : %u" % (v.flag[5]))
    print("count of GFP_IO : %u" % (v.flag[6]))
    print("count of GFP_FS : %u" % (v.flag[7]))
    print("count of GFP_COLD : %u" % (v.flag[8]))
    print("count of GFP_NORWARN : %u" % (v.flag[9]))
    print("count of GFP_REPEAT : %u" % (v.flag[10]))
    print("count of GFP_NOFAIL : %u" % (v.flag[11]))
    print("count of GFP_NORETRY : %u" % (v.flag[12]))
    print("count of GFP_MEMALLOC : %u" % (v.flag[13]))
    print("count of GFP_COMP : %u" % (v.flag[14]))
    print("count of GFP_ZERO : %u" % (v.flag[15]))
    print("count of GFP_NOMEMALLOC : %u" % (v.flag[16]))
    print("count of GFP_HARDWALL : %u" % (v.flag[17]))
    print("count of GFP_THISNODE : %u" % (v.flag[18]))
    print("count of GFP_RECLAIMABLE : %u" % (v.flag[19]))
    print("count of GFP_NOACCOUNT : %u" % (v.flag[20]))
    print("count of GFP_NOTRACK : %u" % (v.flag[21]))
    print("count of GFP_NO_KSWAPD : %u" % (v.flag[22]))
    print("count of GFP_OTHER_NODE : %u" % (v.flag[23]))
    print("count of GFP_WRITE : %u" % (v.flag[24]))
      

