
def read_file(path):
    with open(path, 'r') as f:
        read_text = f.read()
    return read_text

def task_create():
    read_text = read_file("general/general.c")
    source = read_text.replace("HEADER", '')
    source = source.replace("PARAMETER", ' ' )
    source = source.replace("SIZE", '0')
    return (source, "_do_fork")

def task_exec():
    read_text = read_file("general/general.c")
    source = read_text.replace("HEADER", '')
    source = source.replace("PARAMETER", ' ' )
    source = source.replace("SIZE", '0')
    return (source, "sys_execve")

def task_exit():
    read_text = read_file("general/general.c")
    source = read_text.replace("HEADER", '')
    source = source.replace("PARAMETER", ' ' )
    source = source.replace("SIZE", '0')
    return (source, "do_exit")

def task_switch():
    read_text = read_file("general/general.c")
    source = read_text.replace("HEADER", '')
    source = source.replace("PARAMETER", ' ' )
    source = source.replace("SIZE", '0')
    return (source, "finish_task_switch")

def memory_alloc():
    read_text = read_file("general/general.c")
    source = read_text.replace("HEADER", '')
    source = source.replace("PARAMETER", ', size_t size' )
    source = source.replace("SIZE", '(u64)size')
    return (source, "__kmalloc")

def memory_free():
    read_text = read_file("general/general.c")
    source = read_text.replace("HEADER", '')
    source = source.replace("PARAMETER", '' )
    source = source.replace("SIZE", '0')
    return (source, "kfree")

def memory_alloc_page():
    read_text = read_file("general/general.c")
    source = read_text.replace("HEADER", '#include<asm/page.h>')
    source = source.replace("PARAMETER", ', gfp_t gfp_mask, unsigned int order' )
    source = source.replace("SIZE", '(1<<(u64)order)*PAGE_SIZE')
    return (source, "__alloc_pages_nodemask")

def memory_free_page():
    read_text = read_file("general/general.c")
    source = read_text.replace("HEADER", '#include <linux/pagevec.h>\n#include<asm/page.h>')
    source = source.replace("PARAMETER", ', struct page *page, unsinged int order' )
    source = source.replace("SIZE", '(1 << (u64)order) * PAGE_SIZE')
    return (source, "__free_pages_ok")

def memroy_reclaim():
    read_text = read_file("general/general.c")
    source = read_text.replace("HEADER", '#include <linux/mmzone.h>\n#include<asm/page.h>')
    source = source.replace("PARAMETER", ', struct zonelist *zonelist, int order, gfp_t gfp_mask')
    source = source.replace("SIZE", '(1<<order) * PAGE_SIZE')
    return (source, "try_to_free_pages")

def fs_pagecache_access():
    read_text = read_file("general/general.c")
    source = read_text.replace("HEADER", '')
    source = source.replace("PARAMETER", '')
    source = source.replace("SIZE", '0')
    return (source, "pagecache_get_page")

def fs_pagecache_miss():
    read_text = read_file("general/general.c")
    source = read_text.replace("HEADER", '')
    source = source.replace("PARAMETER", '')
    source = source.replace("SIZE", '0')
    return (source, "page_cache_sync_readahead")

def fs_read_ahead():
    read_text = read_file("general/general.c")
    source = read_text.replace("HEADER", "#include <linux/mm_types.h>\n#include<asm/page.h>")
    source = source.replace("PARAMETER", '')
    source = source.replace("SIZE", '(ctx->r8) * PAGE_SIZE')
    return (source, "__do_page_cache_readahead")

def fs_page_writeback_bg():
    read_text = read_file("general/general.c")
    source = read_text.replace("HEADER", "#include <linux/backing-dev-defs.h>")
    source = source.replace("PARAMETER", ',struct bdi_writeback * wb')
    source = source.replace("SIZE", '0')
    return (source, "wb_start_background_writeback")

def fs_page_writeback_per_inode():
    read_text = read_file("general/general.c")
    source = read_text.replace("HEADER", "#include <linux/writeback.h>")
    source = source.replace("PARAMETER", ',struct inode *inode, struct writeback_control *wbc')
    source = source.replace("SIZE", 'wbc->nr_to_write')
    return (source, "wb_start_background_writeback")

def network_tcp_recv():
    read_text = read_file("general/general.c")
    source = read_text.replace("HEADER", "#include <net/tcp.h>")
    source = source.replace("PARAMETER", ',struct sock *sk, struct msghdr *msg, size_t len')
    source = source.replace("SIZE", '(u64)len')
    return (source, "tcp_recvmsg")

def network_tcp_send():
    read_text = read_file("general/general.c")
    source = read_text.replace("HEADER", "#include <net/tcp.h>\n #include <net/inet_common.h>")
    source = source.replace("PARAMETER", ',struct sock *sk, struct msghdr *msg, size_t size')
    source = source.replace("SIZE", '(u64)size')
    return (source, "tcp_sendmsg")

def network_udp_send():
    read_text = read_file("general/general.c")
    source = read_text.replace("HEADER", "#include <net/udp.h>")
    source = source.replace("PARAMETER", ',struct sock *sk, struct msghdr *msg, size_t len')
    source = source.replace("SIZE", '(u64)len')
    return (source, "udp_sendmsg")

def network_udp_recv():
    read_text = read_file("general/general.c")
    source = read_text.replace("HEADER", "#include <net/udp.h>")
    source = source.replace("PARAMETER", ',struct sock *sk, struct msghdr *msg, size_t len')
    source = source.replace("SIZE", '(u64)len')
    return (source, "udp_recvmsg")
