/*
 * Event : network.send
 * Data to crawl : total count, total size
 * Used Kernel-function : tcp_v4_send_check
 */

#include <uapi/linux/ptrace.h>
#include <net/tcp.h>

#define NUM_ARRAY_MAP_SIZE 1
#define NUM_MAP_INDEX 0

struct network_send_value
{
    u64 count;
    u64 size;
};

    // map where we save total count and size
BPF_TABLE("array", int, struct network_send_value, network_send_map, NUM_ARRAY_MAP_SIZE);

    // add network_send_value.count one
    // add network_send_value.size sent packet size
    // when tcp_v4_send_check is called
int network_send_begin(struct pt_regs *ctx, struct sk_buff *skb)
{
    //struct sk_buff *skb_ptr;
    struct network_send_value *val, val_temp;
    int map_index = NUM_MAP_INDEX;
    u64 cnt, siz;
    val_temp.count = 0;
    val_temp.size = 0;
    
    val = network_send_map.lookup_or_init(&map_index, &val_temp);
    ++(val->count);
    val->size += (u64)skb->len;
    //skb_ptr = skb;
    //val->size += (u64)skb_ptr->len;    
    //skb_ptr = skb_ptr->next;
    //val->size += (u64)skb_ptr->len;
    //skb_ptr = skb_ptr->next;
    //val->size += (u64)skb_ptr->len;
    cnt = val->count;
    siz = val->size;
    if (EXPRESSION)
        return 1;

    return 0;
}
