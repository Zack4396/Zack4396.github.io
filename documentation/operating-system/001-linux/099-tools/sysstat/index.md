# sysstat


**本文介绍了如何使用 sysstat**

&lt;!--more--&gt;

[Github]: https://github.com/sysstat/sysstat
[V12.7.5]: https://github.com/sysstat/sysstat/archive/refs/tags/v12.7.5.tar.gz

## 获取源码

仓库地址：[Github], 最新版本是 [V12.7.5]

### 下载

```bash
wget https://github.com/sysstat/sysstat/archive/refs/tags/v12.7.5.tar.gz 
```

### 解压

```bash
tar -zxvf v12.7.5.tar.gz -C . &amp;&amp; cd sysstat-12.7.5
```

## 编译源码

### 编译 x86

略

### 编译 aarch64

```bash
# 指定 对应平台的 GCC 路径
MY_CC=/opt/toolchain/aarch64/bin/aarch64-cros-linux-gnu-gcc
```

```bash
MY_HOST=&#34;$(echo $(basename $MY_CC) | sed &#39;s/-gcc$//&#39;)&#34;
MY_CXX=&#34;$(dirname $MY_CC)/$MY_HOST-g&#43;&#43;&#34;

export PATH=$PATH:&#34;$(dirname $MY_CC)&#34;

mkdir output
export SA_DIR=`pwd`/output/var/log/sa
export conf_dir=`pwd`/output/etc/kksysconfig

# NOTE
# v11.1.2 之前 (2015年), 使用 --disable-man-group
# v11.1.3 之后 (最新版), 使用 --disable-file-attr
./configure \
  CC=$MY_HOST_CC \
  --prefix=`pwd`/output --host=$MY_HOST \
  --disable-file-attr \
  --disable-documentation

# 更正路径为设备端的路径 &#34;/data/output&#34;
sed -i &#39;/-DSA_DIR=\\\&#34;$(SA_DIR)\\\&#34; -DSADC_PATH=\\\&#34;$(SADC_PATH)\\\&#34;/i\MY_TEMP = /data/output&#39; Makefile
sed -i &#39;s/-DSA_DIR=\\\&#34;$(SA_DIR)\\\&#34; -DSADC_PATH=\\\&#34;$(SADC_PATH)\\\&#34;/-DSA_DIR=\\\&#34;$(MY_TEMP)\\\&#34; -DSADC_PATH=\\\&#34;$(MY_TEMP)\/lib\/sa\/sadc\\\&#34;/&#39; Makefile

make clean &amp;&amp; make &amp;&amp; make install
unset SA_DIR
unset conf_dir
```

编译生成文件

```bash
xx@xx:~/linux-tools/sysstat-12.7.5$ tree output
output/
├── bin
│   ├── cifsiostat
│   ├── iostat
│   ├── mpstat
│   ├── pidstat
│   ├── sadf
│   ├── sar
│   └── tapestat
├── etc
│   └── kksysconfig
│       ├── sysstat
│       └── sysstat.ioconf
├── lib
│   └── sa
│       ├── sa1
│       ├── sa2
│       └── sadc
├── share
│   └── doc
│       └── sysstat-12.7.5
└── var
    └── log
        └── sa

11 directories, 12 files
```

使用方法

```bash
# 推送工具到设备
adb push output /data/
# 修改权限
chmod -R 755 /data/output
```

## 工具使用

### 命令行参数

- **iostat**

```bash
# 基本用法
iostat [ 选项 ] [ &lt;时间间隔&gt; ] [ &lt;次数&gt; ]

-c：显示 CPU 使用情况。
-d：显示磁盘 I/O 使用情况。
-k：以 KB/s 为单位显示数据传输速率。
-m：以 MB/s 为单位显示数据传输速率。
-t：显示时间戳。

tps 表示每秒完成的传输数量（Transactions Per Second）
MB_read/s 表示每秒读取的数据量（Megabytes Read Per Second）
MB_wrtn/s 表示每秒写入的数据量（Megabytes Written Per Second）
MB_dscd/s 表示每秒丢弃（或丢失）的数据量（Megabytes Discarded Per Second）
MB_read、MB_wrtn 和 MB_dscd 分别表示自系统启动以来的总读取、写入和丢弃的数据量（Megabytes Read/Written/Discarded）

# 查看 CPU 使用情况
iostat -c

# 查看 磁盘使用I/O使用情况
iostat -d
```

- **pidstat**

```bash
# 基本用法
pidstat [ 选项 ] [ &lt;时间间隔&gt; ] [ &lt;次数&gt; ]

# 查看所有进程的  CPU 使用情况（ -u -p ALL）
pidstat -u -p ALL

# 统计CPU使用情况
pidstat -u

# 统计内存使用情况
pidstat -r
```

- **sar**

```bash
# 基本用法
sar [ 选项 ] [ &lt;时间间隔&gt; ] [ -o &lt;次数&gt; ]

# 统计CPU利用率 -u [ ALL ]
# 例如: (间隔1s, 抓6次)
sar -u ALL 1 -o 6

# 统计内存利用率 -r [ ALL ]
# 例如: (间隔1s, 抓6次)
sar -r ALL 1 -o 6
```

### 用途

#### 分析系统

- iostat 监视系统的磁盘 I/O 使用情况

  &gt; 它提供了有关磁盘读写操作、吞吐量、延迟和使用率等方面的信息。iostat 还可以帮助识别磁盘瓶颈和性能问题。

- mpstat 监视系统的 CPU 使用情况

  &gt; 它提供了有关每个 CPU 核心的使用率、上下文切换、中断和软中断等信息。mpstat 还可以显示平均负载、用户态和内核态 CPU 时间等指标。

- pidstat 监视进程的 CPU 使用情况

  &gt; 它可以显示每个进程的 CPU 使用率、上下文切换、内存使用情况和其他性能指标。pidstat 还可以按照进程名称、用户、PID 等进行过滤和排序。

- sar 用于收集、报告和分析系统性能数据 (System Activity Reporter )

  &gt; 它可以提供有关 CPU、内存、磁盘、网络和其他子系统的统计信息

iostat 日志

```bash
# 模拟读写磁盘操作
/data # stressapptest -s 86400 -M 32 -f /cache/temp1 -f /cache/temp2 -m 0 -l /data/testfile &amp;

# 每隔1秒打印磁盘I/O使用情况 (单位为 MB)
/data/output/bin # ./iostat -d -m 1
Device             tps    MB_read/s    MB_wrtn/s    MB_dscd/s    MB_read    MB_wrtn    MB_dscd
mmcblk0          27.62         2.38         2.41         0.00      12938      13072          0
...
Device             tps    MB_read/s    MB_wrtn/s    MB_dscd/s    MB_read    MB_wrtn    MB_dscd
mmcblk0         185.00        16.00        17.12         0.00         16         17          0
```

mpstat 日志

```bash
/data/output/bin # ./mpstat
Linux 4.19.69-gc3a2d66af7e9 (Chromecast) 	01/01/70 	_aarch64_	(2 CPU)

01:02:21     CPU    %usr   %nice    %sys %iowait    %irq   %soft  %steal  %guest  %gnice   %idle
01:02:21     all    7.41    0.01    8.71    0.01    0.58    0.61    0.00    0.00    0.00   82.67
```

pidstat 日志

```bash
/data/output/bin # ./pidstat
Linux 4.19.69-gc3a2d66af7e9 (Chromecast) 	01/01/70 	_aarch64_	(2 CPU)

00:11:22      UID       PID    %usr %system  %guest   %wait    %CPU   CPU  Command
00:11:22        0         1    0.01    0.54    0.00    0.04    0.55     1  init
00:11:22        0         2    0.00    0.00    0.00    0.00    0.00     1  kthreadd
00:11:22        0         7    0.00    0.00    0.00    0.00    0.00     1  kworker/u4:0-events_unbound
00:11:22        0         9    0.00    0.02    0.00    0.03    0.02     0  ksoftirqd/0
00:11:22        0        10    0.01    0.12    0.00    0.22    0.13     1  rcu_preempt
00:11:22        0        11    0.01    0.06    0.00    0.24    0.08     1  rcu_sched
```

sar 日志

```bash
/data/output/bin # ./sar -u ALL 1 -o 6
Linux 4.19.69-gc3a2d66af7e9 (Chromecast) 	01/01/70 	_aarch64_	(2 CPU)

00:13:49        CPU      %usr     %nice      %sys   %iowait    %steal      %irq     %soft    %guest    %gnice     %idle
00:13:50        all     10.95      0.00     12.94      0.00      0.00      0.50      1.00      0.00      0.00     74.63
00:13:51        all     10.05      0.00     10.55      0.00      0.00      1.01      1.01      0.00      0.00     77.39
00:13:52        all      9.09      0.00     11.62      0.00      0.00      0.51      0.51      0.00      0.00     78.28
00:13:53        all      1.01      0.00      1.01      0.00      0.00      0.00      0.50      0.00      0.00     97.49
00:13:54        all      9.00      0.00     10.50      0.00      0.00      1.00      0.50      0.00      0.00     79.00
00:13:55        all     10.20      0.00     13.27      0.00      0.00      1.02      0.51      0.00      0.00     75.00
Average:        all      8.38      0.00      9.97      0.00      0.00      0.67      0.67      0.00      0.00     80.30
```


---

> 作者: Somebody  
> URL: https://zack4396.github.io/documentation/operating-system/001-linux/099-tools/sysstat/  

