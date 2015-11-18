TARGET := oom pagecache_miss

all: $(TARGET)

$(TARGET): % : ./src/%.c
	$(CC) -o $@ $^

clean:
	rm -f $(TARGET)
