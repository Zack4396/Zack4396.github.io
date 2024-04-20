# stream


**本文介绍了如何使用 stream**

&lt;!--more--&gt;



[Github]: https://github.com/jeffhammond/STREAM


## 获取源码

仓库地址：[Github]

### 下载

```bash
wget https://github.com/jeffhammond/STREAM/archive/refs/heads/master.zip
```



### 解压

```bash
unzip master.zip &amp;&amp; cd STREAM-master
```



## 编译源码

### 编译参数介绍

{{&lt; admonition type=note title=&#34;-mcmodel&#34; open=false &gt;}}

{{&lt; /admonition &gt;}}

| -mcmodel 参数    | 含义            |
| ---------------- | --------------- |
| `-mcmodel=large` | 无限制寻址      |
| `-mcmodel=small` | 不大于 4GB 寻址 |
| `-mcmodel=tiny`  | 不大于 1MB 寻址 |

{{&lt; admonition type=note title=&#34;-DSTREAM_ARRAY_SIZE&#34; open=false &gt;}}

{{&lt; /admonition &gt;}}

  | -DSTREAM_ARRAY_SIZE 参数       | 含义                                                         |
  | ------------------------------ | ------------------------------------------------------------ |
  | `-DSTREAM_ARRAY_SIZE=0xa00000` | 每个测试数组的成员个数为 `0xa00000`（表示 10MB），有`a[]`,`b[]`,`c[]`三个数组，&lt;br /&gt;它们的数据类型均为双精度浮点数 `double`（占用 8 字节）。&lt;br /&gt;因此，进行测试时，需要申请总共 10MB * 3 * 8 = 240MB 的内存空间 |

1. `STREAM_ARRAY_SIZE * 24` 需要小于系统可用内存 (可使用 free 查看)

2. STREAM_ARRAY_SIZE 需要大于 CPU L3 Cache 大小 (512KB ~ 4MB 不等)

3. 如果 Copy/Scale/Add/Triad 的测试时间 `Avg/Min/Max` 小于 20us, 可以适当增加 `STREAM_ARRAY_SIZE` 的大小

   ```txt
   -------------------------------------------------------------
   Function    Best Rate MB/s  Avg time     Min time     Max time
   Copy:          412316.9     0.000002     0.000001     0.000006
   Scale:         412316.9     0.000002     0.000001     0.000005
   Add:           618475.3     0.000002     0.000001     0.000003
   Triad:         618475.3     0.000002     0.000001     0.000003
   -------------------------------------------------------------
   ```

{{&lt; admonition type=note title=&#34;-DNTIMES&#34; open=false &gt;}}

{{&lt; /admonition &gt;}}

&gt; 测试的循环次数 (默认值是 10)

{{&lt; admonition type=note title=&#34;-DOFFSET&#34; open=false &gt;}}

{{&lt; /admonition &gt;}}

&gt; 数组的偏移 (默认值是 0)



### 编译 x86

{{&lt; admonition type=warning title=&#34;避免 OOM 或者 Segmentation fault, STREAM_ARRAY_SIZE 不能设置过大&#34; open=false &gt;}}

{{&lt; /admonition &gt;}}

```bash
# STREAM_ARRAY_SIZE 96MB (实际需要2304MB)
gcc \
  -O3 \
  -mcmodel=large \
  -fopenmp \
  -DSTREAM_ARRAY_SIZE=0x6000000 \
  -DNTIMES=30 \
  -DOFFSET=4096 \
  stream.c -o stream
```



### 编译 aarch64

```bash
# 指定 对应平台的 GCC 路径
MY_CC=/opt/toolchain/aarch64/bin/aarch64-cros-linux-gnu-gcc
```

{{&lt; admonition type=warning title=&#34;避免 OOM 或者 Segmentation fault, STREAM_ARRAY_SIZE 不能设置过大&#34; open=false &gt;}}

{{&lt; /admonition &gt;}}

```bash
# STREAM_ARRAY_SIZE 10MB (实际需要240MB)
$MY_CC -static \
  -O3 \
  -mcmodel=small \
  -fopenmp \
  -DSTREAM_ARRAY_SIZE=0xa00000 \
  -DNTIMES=30 \
  -DOFFSET=4096 \
  stream.c -o stream
```



## 工具使用

### 命令行参数

无



### 用途

#### 测试内存

{{&lt; admonition type=note open=open &gt;}}

关于测试日志，有几点我们可以关注一下

1. **内存读写速度 Copy/Scale/Add/Triad**

   ```
   Function    Best Rate MB/s  Avg time     Min time     Max time
   Copy:           62398.0     0.027506     0.025812     0.034243
   Scale:          51210.2     0.032904     0.031451     0.038471
   Add:            53945.9     0.046618     0.044784     0.052294
   Triad:          53983.6     0.046919     0.044753     0.054359
   ```

{{&lt; /admonition &gt;}}

```bash
# 查看处理器个数
grep -c ^processor /proc/cpuinfo

# [可选] 设定多线程个数 (有几个设置几个)
# 若不设置，则默认使用最大线程数。
export OMP_NUM_THREADS=2

/data # stream
```



日志

```txt
/data # stream
-------------------------------------------------------------
STREAM version $Revision: 5.10 $
-------------------------------------------------------------
This system uses 8 bytes per array element.
-------------------------------------------------------------
Array size = 100663296 (elements), Offset = 4096 (elements)
Memory per array = 768.0 MiB (= 0.8 GiB).
Total memory required = 2304.0 MiB (= 2.2 GiB).
Each kernel will be executed 30 times.
 The *best* time for each kernel (excluding the first iteration)
 will be used to compute the reported bandwidth.
-------------------------------------------------------------
Number of Threads requested = 20
Number of Threads counted = 20
-------------------------------------------------------------
Your clock granularity/precision appears to be 1 microseconds.
Each test below will take on the order of 26879 microseconds.
   (= 26879 clock ticks)
Increase the size of the arrays if this shows that
you are not getting at least 20 clock ticks per test.
-------------------------------------------------------------
WARNING -- The above is only a rough guideline.
For best results, please be sure you know the
precision of your system timer.
-------------------------------------------------------------
Function    Best Rate MB/s  Avg time     Min time     Max time
Copy:           62398.0     0.027506     0.025812     0.034243
Scale:          51210.2     0.032904     0.031451     0.038471
Add:            53945.9     0.046618     0.044784     0.052294
Triad:          53983.6     0.046919     0.044753     0.054359
-------------------------------------------------------------
Solution Validates: avg error less than 1.000000e-13 on all three arrays
-------------------------------------------------------------
```



---

> 作者: Somebody  
> URL: https://zack4396.github.io/documentation/operating-system/001-linux/099-tools/stream/  

