from bcc import BPF
import time
import sys
import argparse

parser = argparse.ArgumentParser(description = "Notifier usage")
parser.add_argument("--event", type=str, default=None, help = "the kind of event that you want notify")
parser.add_argument("--condition", type=str, default=None, help = "the condition expression you want to notify that moment")
parser.add_argument("--time", type=int, default=5, help = "timeout second")
args = parser.parse_args()

if args.event:
    event = args.event
    print ("event: %s" % (event))
if args.condition:
    expr = args.condition
    print ("expr: %s" % (expr))
if args.time:
    interval = args.time
    print ("timeout: %u" % (interval))

def call_back (pid, call_chain):
    print "The event happens"

if len(sys.argv) == 1:
    print " "
    exit()

EVENT_LIST = {
        "task.create" : ["task/task_create.c", "_do_fork", "task_create_begin", "task_create"],
        "task.exit" : ["task/task_exit.c", "do_exit", "task_exit_begin", "task_exit"]
        }

with open(EVENT_LIST[event][0], 'r') as f:
    cfile = f.read()

rep = "EXPRESSION"
bpf_code = cfile.replace(rep, expr)

b = BPF(text = bpf_code, cb = call_back, debug=6)
b.attach_kprobe(event = EVENT_LIST[event][1], fn_name = EVENT_LIST[event][2])

interval = interval * 1000
b.kprobe_poll(timeout = interval)

map_name = EVENT_LIST[event][3] + "_map"
for k,v in b[map_name].items():
    print ("%u" % (v.count))

exit()
