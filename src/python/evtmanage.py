# coding=utf-8


class EventManager:
    """
    LDEN에서 다루는 이벤트들을 관리하는 클래스이다.
    기본적으로 general.c 코드를 선택된 이벤트에 맞게 변환한 뒤 필요한 데이터를 리턴하는 작업을 한다.
    """

    def __init__(self):
        self.source = self.read_file("./src/c/general.c")
        self.EVENT_LIST = {
            "sys.open": self.sys_open(),
            "sys.kill": self.sys_kill(),
            "task.create": self.task_create(),
            "task.exec": self.task_exec(),
            "task.exit": self.task_exit(),
            "task.switch": self.task_switch(),
            "memory.alloc": self.memory_alloc(),
            "memory.free": self.memory_free(),
            "memory.alloc_page": self.memory_alloc_page(),
            "memory.free_page": self.memory_free_page(),
            "memory.reclaim": self.memory_reclaim(),
            "memory.oom_kill": self.memory_oom_kill(),
            "fs.pagecache_access": self.fs_pagecache_access(),
            "fs.pagecache_miss": self.fs_pagecache_miss(),
            "fs.read_ahead": self.fs_read_ahead(),
            "fs.page_writeback_per_inode": self.fs_page_writeback_per_inode(),
            "network.tcp_send": self.network_tcp_send(),
            "network.tcp_recv": self.network_tcp_recv(),
            "network.udp_send": self.network_udp_send(),
            "network.udp_recv": self.network_udp_recv(),
            "disk.read": self.disk_read(),
            "disk.write": self.disk_write(),
            "irq.hard" : self.irq_hard(),
        }

    def user_custom(self, kfunc):
        return self.source\
                   .replace("HEADER", '')\
                   .replace("PARAMETER", '')\
                   .replace("SIZE", '0')\
                   .replace("CHECK", ""),\
               kfunc

    def read_file(self, path):
        with open(path, 'r') as f:
            return f.read()

    def sys_open(self):
        return self.source\
                   .replace("HEADER", '')\
                   .replace("PARAMETER", '')\
                   .replace("SIZE", '0')\
                   .replace("CHECK", ""),\
               "sys_open"

    def sys_kill(self):
        return self.source\
                   .replace("HEADER", '')\
                   .replace("PARAMETER", '')\
                   .replace("SIZE", '0')\
                   .replace("CHECK", ""),\
               "sys_kill"

    def task_create(self):
        return self.source\
                   .replace("HEADER", '')\
                   .replace("PARAMETER", '')\
                   .replace("SIZE", '0')\
                   .replace("CHECK", ""),\
               "_do_fork"

    def task_exec(self):
        return self.source\
                   .replace("HEADER", '')\
                   .replace("PARAMETER", '')\
                   .replace("SIZE", '0')\
                   .replace("CHECK", ""),\
               "sys_execve"

    def task_exit(self):
        return self.source\
                   .replace("HEADER", '')\
                   .replace("PARAMETER", '')\
                   .replace("SIZE", '0')\
                   .replace("CHECK", ""),\
               "do_exit"

    def task_switch(self):
        return self.source\
                   .replace("HEADER", '')\
                   .replace("PARAMETER", '')\
                   .replace("SIZE", '0')\
                   .replace("CHECK", ""),\
               "finish_task_switch"

    def memory_alloc(self):
        return self.source\
                   .replace("HEADER", '')\
                   .replace("PARAMETER", ', size_t size')\
                   .replace("SIZE", '(u64)size')\
                   .replace("CHECK", ""),\
               "__kmalloc"

    def memory_free(self):
        return self.source\
                   .replace("HEADER", '')\
                   .replace("PARAMETER", '')\
                   .replace("SIZE", '0')\
                   .replace("CHECK", ""),\
               "kfree"

    def memory_alloc_page(self):
        return self.source\
                   .replace("HEADER", '#include<asm/page.h>')\
                   .replace("PARAMETER", ', gfp_t gfp_mask, unsigned int order')\
                   .replace("SIZE", '(1<<(u64)order)*PAGE_SIZE')\
                   .replace("CHECK", ""),\
               "__alloc_pages_nodemask"

    def memory_free_page(self):
        return self.source\
                   .replace("HEADER", '#include <linux/pagevec.h>\n#include<asm/page.h>')\
                   .replace("PARAMETER", ', struct page *page, unsigned int order')\
                   .replace("SIZE", '(1 << (u64)order) * PAGE_SIZE')\
                   .replace("CHECK", "")\
                   .replace("0;\n}", """0;\n}
int func2(struct pt_regs *ctx)
{
    struct value *val, *val_spd, val_temp;
    int map_index = NUM_MAP_VAL_INDEX;
    int map_spd_index = NUM_MAP_SPD_INDEX;
    u64 tim = bpf_ktime_get_ns();
    val_temp.count = 0;
    val_temp.size = 0;

    val_spd = map.lookup_or_init(&map_spd_index, &val_temp);
    val = map.lookup_or_init(&map_index, &val_temp);
    val->size += PAGE_SIZE;
    ++(val->count);

    if (val_spd->count == 0 || tim - (val_spd->size) > NUM_SEC)
    {
        val_spd->size = tim;
        val_spd->count = 1;
    }
    else
        val_spd->count += 1;

    return 0;
}
"""),\
                "__free_pages_ok",\
                "func",\
                "free_hot_cold_page",\
                "func2"

    def memory_reclaim(self):
        return self.source\
                   .replace("HEADER", '#include <linux/mmzone.h>\n#include<asm/page.h>')\
                   .replace("PARAMETER", ', struct zonelist *zonelist, int order, gfp_t gfp_mask')\
                   .replace("SIZE", '(1<<order) * PAGE_SIZE')\
                   .replace("CHECK", ""),\
               "try_to_free_pages"

    def memory_oom_kill(self):
        return self.source\
                   .replace("HEADER", "")\
                   .replace("PARAMETER", '')\
                   .replace("SIZE", '0')\
                   .replace("CHECK", ""),\
               "oom_kill_process"

    def fs_pagecache_access(self):
        return self.source\
                   .replace("HEADER", '')\
                   .replace("PARAMETER", '')\
                   .replace("SIZE", '0')\
                   .replace("CHECK", ""),\
               "pagecache_get_page"

    def fs_pagecache_miss(self):
        return self.source\
                   .replace("HEADER", '')\
                   .replace("PARAMETER", '')\
                   .replace("SIZE", '0')\
                   .replace("CHECK", ""),\
               "page_cache_sync_readahead"
               #    "do_generic_file_read"

    def fs_read_ahead(self):
        return self.source\
                   .replace("HEADER", "#include <linux/mm_types.h>\n#include<asm/page.h>")\
                   .replace("PARAMETER", '')\
                   .replace("SIZE", '(ctx->r8) * PAGE_SIZE')\
                   .replace("CHECK", ""),\
               "__do_page_cache_readahead"

    def fs_page_writeback_per_inode(self):
        return self.source\
                   .replace("HEADER", "#include <linux/writeback.h>")\
                   .replace("PARAMETER", ',struct inode *inode, struct writeback_control *wbc')\
                   .replace("SIZE", 'wbc->nr_to_write')\
                   .replace("CHECK", ""),\
               "__writeback_single_inode"

    def network_tcp_recv(self):
        return self.source\
                   .replace("HEADER", "#include <net/tcp.h>")\
                   .replace("PARAMETER", ',struct sock *sk, struct msghdr *msg, size_t len')\
                   .replace("SIZE", '(u64)len')\
                   .replace("CHECK", ""),\
               "tcp_recvmsg"

    def network_tcp_send(self):
        return self.source\
                   .replace("HEADER", "#include <net/tcp.h>\n #include <net/inet_common.h>")\
                   .replace("PARAMETER", ',struct sock *sk, struct msghdr *msg, size_t size')\
                   .replace("SIZE", '(u64)size')\
                   .replace("CHECK", ""),\
               "tcp_sendmsg"

    def network_udp_send(self):
        return self.source\
                   .replace("HEADER", "#include <net/udp.h>")\
                   .replace("PARAMETER", ',struct sock *sk, struct msghdr *msg, size_t len')\
                   .replace("SIZE", '(u64)len')\
                   .replace("CHECK", ""),\
               "udp_sendmsg"

    def network_udp_recv(self):
        return self.source\
                   .replace("HEADER", "#include <net/udp.h>")\
                   .replace("PARAMETER", ',struct sock *sk, struct msghdr *msg, size_t len')\
                   .replace("SIZE", '(u64)len')\
                   .replace("CHECK", ""),\
               "udp_recvmsg"

    def disk_read(self):
        return self.source\
                   .replace("HEADER", "#include <linux/blkdev.h>")\
                   .replace("PARAMETER", ', struct request *req')\
                   .replace("SIZE", '(u64)req->__data_len')\
                   .replace("CHECK", "if(req->cmd_flags & REQ_WRITE)return 0;"),\
               "blk_account_io_completion"
    def disk_write(self):
        return self.source\
                   .replace("HEADER", "#include <linux/blkdev.h>")\
                   .replace("PARAMETER", ', struct request *req')\
                   .replace("SIZE", '(u64)req->__data_len')\
                   .replace("CHECK", "if((req->cmd_flags & REQ_WRITE) == 0 )return 0;"),\
               "blk_account_io_start"

    def irq_hard(self):
        return self.source\
                .replace("HEADER", '#include <linux/irq.h>\n #include <linux/irqdesc.h>\n #include<linux/interrupt.h>')\
                .replace("PARAMETER", ', struct irq_desc *desc')\
                .replace("SIZE", '0')\
                .replace("CHECK", ""),\
            "handle_irq_event_percpu"

