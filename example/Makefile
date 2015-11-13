CXX=gcc

all: oom bigfile
	echo 'compile'

oom:
	$(CXX) -o oom oom.c

bigfile:
	$(CXX) -o pagecache_miss bigfile.c

clean:
	rm -f oom pagecache_miss
