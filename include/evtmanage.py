# coding=utf-8


class EventManager:
    """
    LDEN에서 다루는 이벤트들을 관리하는 클래스이다.
    기본적으로 general.c 코드를 선택된 이벤트에 맞게 변환한 뒤 필요한 데이터를 리턴하는 작업을 한다.
    """

    def __init__(self):
        self.EVENT_LIST = {
            "task.create": task_create(),
            "task.exec": task_exec(),
            "task.exit": task_exit(),
            "task.switch": task_switch(),
            "memory.alloc": memory_alloc(),
            "memory.free": memory_free(),
            "memory.alloc_page": memory_alloc_page(),
            # "memory.free_page": ["memory/memory_free_page.c", "__free_pages_ok", "memory_free_page_begin", "memory_free_page", "free_hot_cold_page", "memory_free_page_order_zero_begin"],
            "memory.reclaim": memroy_reclaim(),
            "fs.pagecache_access": fs_pagecache_access(),
            "fs.pagecache_miss": fs_pagecache_miss(),
            "fs.read_ahead": fs_read_ahead(),
            # "fs.page_writeback_bg": fs_page_writeback_bg(),
            "fs.page_writeback_per_inode": fs_page_writeback_per_inode(),
            "network.tcp_send": network_tcp_send(),
            "network.tcp_recv": network_tcp_recv(),
            "network.udp_send": network_udp_send(),
            "network.udp_recv": network_udp_recv(),
        }

    @staticmethod
    def read_file(path):
        with open(path, 'r') as f:
            read_text = f.read()
        return read_text

    @staticmethod
    def task_exec():
        read_text = read_file("general/general.c")
        source = read_text.replace("HEADER", '')
        source = source.replace("PARAMETER", '')
        source = source.replace("SIZE", '0')
        return source, "sys_execve"

    @staticmethod
    def task_exit():
        read_text = read_file("general/general.c")
        source = read_text.replace("HEADER", '')
        source = source.replace("PARAMETER", '')
        source = source.replace("SIZE", '0')
        return source, "do_exit"

    @staticmethod
    def task_switch():
        read_text = read_file("general/general.c")
        source = read_text.replace("HEADER", '')
        source = source.replace("PARAMETER", '')
        source = source.replace("SIZE", '0')
        return source, "finish_task_switch"

    @staticmethod
    def memory_alloc():
        read_text = read_file("general/general.c")
        source = read_text.replace("HEADER", '')
        source = source.replace("PARAMETER", ', size_t size')
        source = source.replace("SIZE", '(u64)size')
        return source, "__kmalloc"

    @staticmethod
    def memory_free():
        read_text = read_file("general/general.c")
        source = read_text.replace("HEADER", '')
        source = source.replace("PARAMETER", '')
        source = source.replace("SIZE", '0')
        return source, "kfree"

    @staticmethod
    def memory_alloc_page():
        read_text = read_file("general/general.c")
        source = read_text.replace("HEADER", '#include<asm/page.h>')
        source = source.replace("PARAMETER", ', gfp_t gfp_mask, unsigned int order')
        source = source.replace("SIZE", '(1<<(u64)order)*PAGE_SIZE')
        return source, "__alloc_pages_nodemask"

    @staticmethod
    def memory_free_page():
        read_text = read_file("general/general.c")
        source = read_text.replace("HEADER", '#include <linux/pagevec.h>\n#include<asm/page.h>')
        source = source.replace("PARAMETER", ', struct page *page, unsinged int order')
        source = source.replace("SIZE", '(1 << (u64)order) * PAGE_SIZE')
        return source, "__free_pages_ok"

    @staticmethod
    def memroy_reclaim():
        read_text = read_file("general/general.c")
        source = read_text.replace("HEADER", '#include <linux/mmzone.h>\n#include<asm/page.h>')
        source = source.replace("PARAMETER", ', struct zonelist *zonelist, int order, gfp_t gfp_mask')
        source = source.replace("SIZE", '(1<<order) * PAGE_SIZE')
        return source, "try_to_free_pages"

    @staticmethod
    def fs_pagecache_access():
        read_text = read_file("general/general.c")
        source = read_text.replace("HEADER", '')
        source = source.replace("PARAMETER", '')
        source = source.replace("SIZE", '0')
        return source, "pagecache_get_page"

    @staticmethod
    def fs_pagecache_miss():
        read_text = read_file("general/general.c")
        source = read_text.replace("HEADER", '')
        source = source.replace("PARAMETER", '')
        source = source.replace("SIZE", '0')
        return source, "page_cache_sync_readahead"

    @staticmethod
    def fs_read_ahead():
        read_text = read_file("general/general.c")
        source = read_text.replace("HEADER", "#include <linux/mm_types.h>\n#include<asm/page.h>")
        source = source.replace("PARAMETER", '')
        source = source.replace("SIZE", '(ctx->r8) * PAGE_SIZE')
        return source, "__do_page_cache_readahead"

    @staticmethod
    def fs_page_writeback_bg():
        read_text = read_file("general/general.c")
        source = read_text.replace("HEADER", "#include <linux/backing-dev-defs.h>")
        source = source.replace("PARAMETER", ',struct bdi_writeback * wb')
        source = source.replace("SIZE", '0')
        return source, "wb_start_background_writeback"

    @staticmethod
    def fs_page_writeback_per_inode():
        read_text = read_file("general/general.c")
        source = read_text.replace("HEADER", "#include <linux/writeback.h>")
        source = source.replace("PARAMETER", ',struct inode *inode, struct writeback_control *wbc')
        source = source.replace("SIZE", 'wbc->nr_to_write')
        return source, "wb_start_background_writeback"

    @staticmethod
    def network_tcp_recv():
        read_text = read_file("general/general.c")
        source = read_text.replace("HEADER", "#include <net/tcp.h>")
        source = source.replace("PARAMETER", ',struct sock *sk, struct msghdr *msg, size_t len')
        source = source.replace("SIZE", '(u64)len')
        return source, "tcp_recvmsg"

    @staticmethod
    def network_tcp_send():
        read_text = read_file("general/general.c")
        source = read_text.replace("HEADER", "#include <net/tcp.h>\n #include <net/inet_common.h>")
        source = source.replace("PARAMETER", ',struct sock *sk, struct msghdr *msg, size_t size')
        source = source.replace("SIZE", '(u64)size')
        return source, "tcp_sendmsg"

    @staticmethod
    def network_udp_send():
        read_text = read_file("general/general.c")
        source = read_text.replace("HEADER", "#include <net/udp.h>")
        source = source.replace("PARAMETER", ',struct sock *sk, struct msghdr *msg, size_t len')
        source = source.replace("SIZE", '(u64)len')
        return source, "udp_sendmsg"

    @staticmethod
    def network_udp_recv():
        read_text = read_file("general/general.c")
        source = read_text.replace("HEADER", "#include <net/udp.h>")
        source = source.replace("PARAMETER", ',struct sock *sk, struct msghdr *msg, size_t len')
        source = source.replace("SIZE", '(u64)len')
        return source, "udp_recvmsg"
