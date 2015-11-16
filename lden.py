#!/usr/bin/python
# coding=utf-8

from src.python.evtmanage import EventManager
from src.python.all_event import AllEvent
from src.python.ldenparse import LdenParser
from src.python.mapread import MapReader
from bcc import BPF
from time import sleep
from sys import argv, maxint
import os

## DEFINE CONSTANT ##
INTERVAL = 0.5
MAP = "map"
## ## ## ## ## ## ##

if __name__ == "__main__":
    argv_parser = LdenParser(argv)
    commander = argv_parser.result[0]
    user_args = argv_parser.result[1]


    ##############################
    # "all" command executed
    if commander == 0:
        visualizer = AllEvent(ipaddress=user_args["address"], port=user_args["port"])
        try:
            visualizer.main_run()
        except KeyboardInterrupt:
            print ""
            pass
    # "all" command ended
    ##############################


    ##############################
    # "notify" command executed
    else:
        manager = EventManager()
        task_dict = {}

        ## parsing expression
        event_parse_tree = [">", ["task.create", "count"], "100"]
        ## ## ## ## ## ## ##

        ## attach kprobe
        for k in manager.EVENT_LIST.keys():
            if k in task_dict:
                continue
            code_and_func = manager.EVENT_LIST[k]
            b = BPF(text=code_and_func[0])

            if len(code_and_func) > 2:
                for func_idx in range(1, len(code_and_func)):
                    if (func_idx & 1) == 0:
                        continue
                    b.attach_kprobe(event=code_and_func[func_idx],
                            fn_name=code_and_func[func_idx + 1])
            else:
                b.attach_kprobe(event=code_and_func[1], fn_name='func')

            task_dict[k] = (MapReader(b, MAP), [0, 0, 0])
        ## ## ## ## ## ## ##

        ## read maps until timeout
        if user_args["time"] is None:
            timeout = maxint
        else:
            try:
                timeout = float(user_args["time"])
            except:
                print "Invalid time \'",  str(timeout), "\'. Value of option \'time\' must be integer type or float type."
                exit()

        print "# Tracing selected events..."
        print "# Condition : ", user_args["expression"]
        print "# Timeout   : ", "infinity" if timeout is maxint else str(timeout) + " s"
        print "# Script    : ", user_args["script"]

        try:
            sleep_time = 0
            while True:
                if (sleep_time >= timeout):
                    print "timeout"
                    exit()
                sleep_time += INTERVAL
                sleep(INTERVAL)

        except KeyboardInterrupt:
            print ""
            exit()
        ## ## ## ## ## ## ##

    # "notify" command ended
    ##############################

