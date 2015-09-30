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
    print("count of GFP_DMA : %u" % (v.flags.flag[0]))
    print("count of GFP_HIGHMEM : %u" % (v.flags.flag[1]))
    print("count of GFP_DMA32 : %u" % (v.flags.flag[2]))
    print("count of GFP_MOVABLE : %u" % (v.flags.flag[3]))
    print("count of GFP_WAIT : %u" % (v.flags.flag[4]))
    print("count of GFP_HIGH : %u" % (v.flags.flag[5]))
    print("count of GFP_IO : %u" % (v.flags.flag[6]))
    print("count of GFP_FS : %u" % (v.flags.flag[7]))
    print("count of GFP_COLD : %u" % (v.flags.flag[8]))
    print("count of GFP_NORWARN : %u" % (v.flags.flag[9]))
    print("count of GFP_REPEAT : %u" % (v.flags.flag[10]))
    print("count of GFP_NOFAIL : %u" % (v.flags.flag[11]))
    print("count of GFP_NORETRY : %u" % (v.flags.flag[12]))
    print("count of GFP_MEMALLOC : %u" % (v.flags.flag[13]))
    print("count of GFP_COMP : %u" % (v.flags.flag[14]))
    print("count of GFP_ZERO : %u" % (v.flags.flag[15]))
    print("count of GFP_NOMEMALLOC : %u" % (v.flags.flag[16]))
    print("count of GFP_HARDWALL : %u" % (v.flags.flag[17]))
    print("count of GFP_THISNODE : %u" % (v.flags.flag[18]))
    print("count of GFP_RECLAIMABLE : %u" % (v.flags.flag[19]))
    print("count of GFP_NOACCOUNT : %u" % (v.flags.flag[20]))
    print("count of GFP_NOTRACK : %u" % (v.flags.flag[21]))
    print("count of GFP_NO_KSWAPD : %u" % (v.flags.flag[22]))
    print("count of GFP_OTHER_NODE : %u" % (v.flags.flag[23]))
    print("count of GFP_WRITE : %u" % (v.flags.flag[24]))
      

