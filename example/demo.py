import sys
import os

if __name__ == "__main__":
    if sys.argv[1] == "pagecache":
        os.system("./fileio_test.sh")
    elif sys.argv[1] == "oom":
        os.system("./oom")

