#!/usr/bin/python

import sys_address
from bcc import BPF
from time import sleep

with open("nr_thread.c", 'r') as f:
    cfile = f.read()
    print cfile
    
bpf_code = cfile.replace("ADRVAR", ("0x"+sys_address.get_variable_address("nr_threads" )))

b = BPF(text = bpf_code)
event = "sys_clone"

b.attach_kprobe(event = "sys_clone", fn_name = "read_nr_thread" )

interval = 5
do_exit = 0

while 1:
    for k,v in b["dist"].items():
        print (k.value, v.value)
    
    try:
        sleep(interval)
    except KeyboardInterrupt:
        pass; do_exit = 1

    if do_exit:
        exit()


