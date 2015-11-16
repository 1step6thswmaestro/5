from bcc import BPF


class MapReader:

    def __init__(self, BPF, MAP_NAME):
        self.bpf_object = BPF
        self.map_name = MAP_NAME
        self.map_data = {
                "count" : 0,
                "size" : 0,
                "speed" : 0
                }

    def read_map(self):
        i = 0
        for k, v in self.bpf_object[self.map_name].items():
            if i == 0:
                self.map_data["count"] = v.count
                self.map_data["size"] = v.size
                i += 1
            else:
                self.map_data["speed"] = v.count
                return self.map_data
