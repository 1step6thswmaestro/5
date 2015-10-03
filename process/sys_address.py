import platform

#use get_variable_address, we can get Kerenl global variable, and functions's address
class sys_address():
    path = "/lib/modules/%s/build/System.map"
    f = None #file object
    
    def __init__(self):
        self.path = (self.path % self.get_kernel_version())
        print self.path
        with open(self.path, 'r') as self.f:
            self.contents = self.f.readlines()


    def get_kernel_version(self):
        return platform.uname()[2]

    def get_path(self):
        return self.path
    
    def get_variable_address(self, va_name):
        for i in self.contents:
            j = i.split()
            if va_name == j[2]:
                return j[0]

def get_variable_address(va_name):
    path = "/lib/modules/%s/build/System.map" %platform.uname()[2]
    with open(path, 'r') as f:
        contents = f.readlines()
    for i in contents:
        j = i.split()
        if va_name == j[2]:
            return j[0]


if __name__ == "__main__":
    a = sys_address()
    print a.get_variable_address("nr_threads")
    print get_variable_address("nr_threads")
