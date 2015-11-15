#!/usr/bin/python

from src.python.all_event import AllEvent
from src.python.ldenparse import LdenParser
from src.python.mapread import MapReader
from bcc import BPF
from time import sleep
from sys import argv
import os

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
