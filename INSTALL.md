# Requirements

## Kernel

In general, to use these features, a Linux kernel version 4.1 or newer is
required. In addition, the following flags should be set:

- `CONFIG_BPF=y`
- `CONFIG_BPF_SYSCALL=y`
- `CONFIG_NET_CLS_BPF=m` [optional, for tc filters]
- `CONFIG_NET_ACT_BPF=m` [optional, for tc actions]
- `CONFIG_BPF_JIT=y`
- `CONFIG_HAVE_BPF_JIT=y`
- `CONFIG_BPF_EVENTS=y` [optional, for kprobes]

## BPF Compiler Collection

BCC 설치하라는 이야기가 들어갈 곳

## Elastic Search & Kibana

키바나 설치하라는 이야기가 들어갈 곳
