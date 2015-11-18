# LDEN (Linux Dynamic Event Notifier)
##Original repository
[https://github.com/SomaLDEN/lden](https://github.com/SomaLDEN/lden)

##INSTALL & RUN
To execute 'LDEN', please read INSTALL.md and implement those instructions.

## Provided data

- count : it means how many the kprobe-attached function(s) related with chosen event has called  
- size : it means the size of memory that the event handled  
- speed : it means the velocity of count per sec

## Provided event

"*" doesn't support size data.

- sys.open *
- sys.kill *
- task.create *
- task.exec *
- task.exit *
- task.switch *
- memory.alloc
- memory.free *
- memory.alloc_page
- memory.free_page
- memory.reclaim
- memory.oom_kill *
- fs.pagecache_access *
- fs.pagecache_miss *
- fs.read_ahead
- fs.page_writeback_per_inode
- network.tcp_send
- network.tcp_recv
- network.udp_send
- network.udp_recv
- disk.read
- disk.write
- irq.hard *

## Usage

### Commands

There are two commands provided by LDEN.  
To make all data in the event list visual, `sudo lden visualize [<options>]`.  
To get notification when a special event that you set happens, `sudo lden notify <expression> [<options>]`.  
You can see help with `lden --help`

#### 1. visualize

(You can see help with `lden visual --help`)
- Option **'address'** requires an ip address you want to send data to Elasticsearch. The default value is "localhost".
- Option **'port'** requires a port number of Elasticsearch. The default value is "9200".

Executing visual command, you can see accumulated data on port 5601 which is default port number of Kibana.

#### 2. notify

(You can see help with `lden notify --help`)  
This command helps you get notification. See below, that's an example command when we want to know when if the number of tasks created is over 100 while the size of memory freed by the kernel is over 500 bytes:

    $ sudo lden notify "count(task.create) > 100 and size(memory.free) > 500"
    
It's so simple, isn't it?

##### 2.1 grammar

- Just write **"ProvidedData(ProvidedEvent)"** to choose event and data.
- Comparison operators **">, >=, <, <=, =, <>"** are supported. These operators must be included in your expression.
- Boolean operators **"&, and, |, or"** are supported.
- Custom function is supported. If you make a kernel function and want to trace that function, write `custom(yourfunction)`. Custom function doesn't support size data.

See example:

    $ sudo lden notify "count(custom(foo)) < 10 and (count(sys.kill) > 5 or speed(disk.read) > 30)"
    
is same as

    $ sudo lden notify "count(custom(foo)) < 10 & (count(sys.kill) > 5 | speed(disk.read) > 30)"
    
and also same as

    $ sudo lden notify "count(custom(foo)) < 10 and count(sys.kill) > 5
      or count(custom(foo)) < 10 and speed(disk.read) > 30"
    
##### 2.2 options

- Option **'time'** requires the number of time. You want to turn off this program after that time spends. The default set is "infinity" mode.
- Option **'script'** requires shell script that would be executed when the expressed event happens. It's recommended to use it like `--script "bash yourscript.sh"`

