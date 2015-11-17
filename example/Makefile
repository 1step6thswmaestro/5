CXX=gcc

TARGET := oom bigfile
OBJECTS := oom.o bigfile.o

all: $(TARGET)

oom : 
	$(CXX) -o $@ $@.c

bigfile:
	$(CXX) -o pagecache_miss $@.c


clean:
	rm -f oom pagecache_miss
