#include <uapi/linux/ptrace.h>
#include <linux/fs.h>

struct file_info
{
    //unsigned char name[512];
    unsigned size;
};

BPF_HASH(cache_map, u32, struct file_info);

int myGet_pagecache(struct pt_regs *ctx, struct file *file, unsigned len)
{
    u32 key = 1;
    //struct file *key = file;
    struct file_info *val, val_temp;
    //strcpy(val_temp.name, file->f_path.dentry->d_name.name);
    val_temp.size = len;

    val = cache_map.lookup_or_init(&key, &val_temp);
    //strcpy(val->name, file->f_path.dentry->d_name.name);
    val->size = len;
    return 0;
}
