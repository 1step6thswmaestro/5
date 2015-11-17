# Requirements

## Kernel

In general, to use these features, the Linux kernel version 4.1 or newer is
required. In addition, the following flags should be set:

```
CONFIG_BPF=y
CONFIG_BPF_SYSCALL=y
# [optional, for tc filters]
CONFIG_NET_CLS_BPF=m
# [optional, for tc actions]
CONFIG_NET_ACT_BPF=m
CONFIG_BPF_JIT=y
CONFIG_HAVE_BPF_JIT=y
# [optional, for kprobes]
CONFIG_BPF_EVENTS=y
```

## BCC (BPF Compiler Collection)

Visit [BCC main repository](https://github.com/iovisor/bcc) and install BCC.  
See [INSTALL.md](https://github.com/iovisor/bcc/blob/master/INSTALL.md) of BCC for installation steps on your platform.

## Elasticsearch & Kibana

Download Elasticsearch in [here](https://www.elastic.co/products/elasticsearch) and install it.  
Download Kibana in [here](https://www.elastic.co/products/kibana) and install it.
