from bcc import BPF
import time
import sys
import os
import httplib
from multiprocessing import Process
from evtmanage import EventManager


class AllEvent:
    def __init__(self, ipaddress, port):
        self.ES_URL = ""

        if ipaddress is None:
            self.ES_URL += "192.168.225.1"
        else:
            self.ES_URL += ipaddress

        self.ES_URL += ":"

        if port is None:
            self.ES_URL += "9200"
        else:
            self.ES_URL += port

        self.conn = None

        self.bulk = ''
        self.header = '{"create":{"_index":"lden", "_type":"events"}}\n'
        self.EVENT_LIST_data = {}

    def trace_begin(self,):
        self.conn = httplib.HTTPConnection(self.ES_URL)
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

        self.conn.request("PUT", "/lden", mapping)
        resp= self.conn.getresponse()
        data = resp.read()
        if resp.status != 200:
            print data

    def trace_end(self):
        self.conn.close()

    def process_event(self,event, count, size, timestamp):
        body = '''
        {
        "event" : "%s",
        "count" : %d,
        "size" : %d,
        "time" : "%s"
        }''' %(event, count, size, timestamp)

        self.conn.request('POST', '/lden/events', body)
        resp = self.conn.getresponse()
        data = resp.read()
        if resp.status != 201:
            print "post document: ", resp.status, ":", resp.reason
            print data

    def run_event_tracing(self, b, event):
        count = 0
        size = 0
        for k, v in b["map"].items():
            count = v.count - self.EVENT_LIST_data[event]["count"]
            size = v.size - self.EVENT_LIST_data[event]["size"]
            self.EVENT_LIST_data[event]["count"] = v.count
            self.EVENT_LIST_data[event]["size"] = v.size
            break
        timestamp = time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime())
        self.bulk += self.header
        self.bulk += '{ "event" : "%s", "count" : %d, "size" : %d, "time" : "%s"}\n' %(event.replace('.','_'), count, size, timestamp)

    def main_run(self):
        manager = EventManager()
        task_list = []
        self.trace_begin()
        for k in manager.EVENT_LIST.keys():
            self.EVENT_LIST_data[k] ={"count" : 0, "size" : 0}
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
            task_list.append((b, k))

        current_time = time.time()
        sleep_time = int(current_time)+1 - current_time

        while 1:
            self.bulk = ''
            time.sleep(sleep_time)
            for i, v in task_list:
                self.run_event_tracing(i, v)  # i is bpf object, v is eventname

            self.bulk += '\n'
            self.conn.request('POST', '/_bulk', self.bulk)
            resp = self.conn.getresponse()
            data = resp.read()
            if resp.status != 200 and resp.status != 201:
                print "post document: ", resp.status, ":", resp.reason
                print data
            start = time.time()
            sleep_time = int(start) + 1 - start



if __name__ == "__main__":
    a = AllEvent()
    a.main_run()
