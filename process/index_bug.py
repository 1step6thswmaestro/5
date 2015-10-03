from bcc import BPF
from time import sleep


b = BPF(src_file = "index_bug")

interval = 5

while 1:
    for k,v in b["dist"].items():
        print (k.value, v.vlaue)
    try:
        sleep(interval)
    except KeyboardInterrupt:
        pass; do_exit = 1

    if do_exit:
        exit()



