/*
 * Event : network.recv
 * Data to crawl : total count, total size
 * Used Kernel-function : tcp_recvmsg
 */

#include <uapi/linux/ptrace.h>
#include <net/tcp.h>

#define NUM_ARRAY_MAP_SIZE 1
#define NUM_MAP_INDEX 0

struct network_recv_value
{
    u64 count;
    u64 size;
};

    // map where we save total count and size
BPF_TABLE("array", int, struct network_recv_value, network_recv_map, NUM_ARRAY_MAP_SIZE);

    // add network_recv_value.count one
    // add network_recv_value.size recv packet's data size
    // when tcp_recvmsg is called
int network_recv_begin(struct pt_regs *ctx, struct sock *sk, struct msghdr *msg, size_t len)
{
    struct network_recv_value *val, val_temp;
    int map_index = NUM_MAP_INDEX;
    u64 cnt, siz;
    val_temp.count = 0;
    val_temp.size = 0;

    val = network_recv_map.lookup_or_init(&map_index, &val_temp);
    ++(val->count);
    val->size += (u64)len;

    cnt = val->count;
    siz = val->size;
    if (EXPRESSION)
        return 1;

    return 0;
}
