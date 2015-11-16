from bcc import BPF


class MapReader:

    def __init__(self, BPF, MAP_NAME):
        self.bpf_object = BPF
        self.map_name = MAP_NAME
        '''
        map_data[0]: count of event
        map_data[1]: size of event
        map_data[2]: speed of event
        '''
        self.map_data = [0, 0, 0]

    def read_map(self):
        i = 0
        for k, v in self.bpf_object[self.map_name].items():
            if i == 0:
                self.map_data[0] = v.count
                self.map_data[1] = v.size
                i += 1
            else:
                self.map_data[2] = v.count
                return self.map_data
