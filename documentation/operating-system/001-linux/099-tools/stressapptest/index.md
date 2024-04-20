# stressapptest


**本文介绍了如何使用 stressapptest**

&lt;!--more--&gt;

[Github]: https://github.com/stressapptest/stressapptest
[V1.0.11]: https://github.com/stressapptest/stressapptest/archive/refs/tags/v1.0.11.tar.gz

## 获取源码

仓库地址：[Github], 最新版本是 [V1.0.11]

### 下载

```bash
wget https://github.com/stressapptest/stressapptest/archive/refs/tags/v1.0.11.tar.gz
```

### 解压

```bash
tar -zxvf v1.0.11.tar.gz -C . &amp;&amp; cd stressapptest-1.0.11
```

## 编译源码

### 编译 x86

```bash
./configure &amp;&amp; make clean &amp;&amp; make

# 查看生成文件
ls src/stressapptest
```

### 编译 aarch64

```bash
# 指定 对应平台的 GCC 路径
MY_CC=/opt/toolchain/aarch64/bin/aarch64-cros-linux-gnu-gcc
```

```bash
MY_HOST=&#34;$(echo $(basename $MY_CC) | sed &#39;s/-gcc$//&#39;)&#34;
MY_CXX=&#34;$(dirname $MY_CC)/$MY_HOST-g&#43;&#43;&#34;

./configure --build=aarch64 --host=&#34;$MY_HOST&#34; CC=&#34;$MY_CC&#34; CXX=&#34;$MY_CXX&#34;

make clean &amp;&amp; make

ls src/stressapptest
```

## 工具使用

### 命令行参数

```bash
/data # stressapptest --help
Usage: stressapptest [options]

-s [?] 指定测试时长 ? 秒
-M [?] 指定内存大小 ? MB

-m [?] 指定 copy 线程 ? 个
-i [?] 指定 invert 线程 ? 个
-C [?] 指定 cpu stress 线程 ? 个

-f [?] 新增 disk 线程测试文件 [?] (注: 可指定多个)
-l [?] 指定日志输出文件 [?]

-W 使用更多CPU压力去压测
```

### 用途

#### 测试内存

{{&lt; admonition type=note open=false &gt;}}

关于测试日志，有几点我们可以关注一下

1. **内存拷贝速度**

   不同压测环境，观察 DDR 读写速度是否有影响

   `xxxx/yy/zz-aa:bb:cc(PDT) Stats: Memory Copy: 130562.00M at 2946.00MB/s`

2. **测试是否通过**

   `Status: PASS - please verify no corrected errors`

{{&lt; /admonition &gt;}}

```bash
# -s 测试时长 86400(24hrs) 或 43200(12hrs) 或 28800(8hrs)
# -M 测试大小 256M
# -m copy 线程 8个
# -W 使用更多CPU压力去压测
stressapptest -s 28800 -M 256 -m 8 -W
```

日志

```txt
/ # stressapptest -s 28800 -M 256 -m 8 -W
2024/04/10-20:09:31(PDT) Log: Commandline - stressapptest -s 28800 -M 256 -m 8 -W
2024/04/10-20:09:31(PDT) Stats: SAT revision 1.0.4_autoconf, 64 bit binary
2024/04/10-20:09:31(PDT) Log: Android version from open source release
2024/04/10-20:09:31(PDT) Log: 1 nodes, 2 cpus.
2024/04/10-20:09:31(PDT) Log: Prefer plain malloc memory allocation.
2024/04/10-20:09:31(PDT) Log: Using mmap() allocation at 0x7f7c000000.
2024/04/10-20:09:31(PDT) Stats: Starting SAT, 256M, 28800 seconds
2024/04/10-20:09:32(PDT) Log: Region mask: 0x1
2024/04/10-20:09:42(PDT) Log: Seconds remaining: 28790
2024/04/10-20:09:52(PDT) Log: Seconds remaining: 28780
2024/04/10-20:10:02(PDT) Log: Seconds remaining: 28770
2024/04/10-20:10:12(PDT) Log: Seconds remaining: 28760
^C2024/04/10-20:10:16(PDT) Log: User exiting early (28756 seconds remaining)
2024/04/10-20:10:17(PDT) Stats: Found 0 hardware incidents
2024/04/10-20:10:17(PDT) Stats: Completed: 130562.00M in 45.01s 2900.81MB/s, with 0 hardware incidents, 0 errors
2024/04/10-20:10:17(PDT) Stats: Memory Copy: 130562.00M at 2946.00MB/s
2024/04/10-20:10:17(PDT) Stats: File Copy: 0.00M at 0.00MB/s
2024/04/10-20:10:17(PDT) Stats: Net Copy: 0.00M at 0.00MB/s
2024/04/10-20:10:17(PDT) Stats: Data Check: 0.00M at 0.00MB/s
2024/04/10-20:10:17(PDT) Stats: Invert Data: 0.00M at 0.00MB/s
2024/04/10-20:10:17(PDT) Stats: Disk: 0.00M at 0.00MB/s
2024/04/10-20:10:17(PDT)
2024/04/10-20:10:17(PDT) Status: PASS - please verify no corrected errors
2024/04/10-20:10:17(PDT)
```

#### 测试存储 (EMMC, Nand)

{{&lt; admonition type=note open=false &gt;}}

关于测试日志，有几点我们可以关注一下

1. **文件拷贝速度**

   不同压测环境，观察 EMMC 读写速度是否有影响

   `xxxx/yy/zz-aa:bb:cc(PDT) Stats: File Copy: 2016.00M at 34.50MB/s`

2. **测试是否通过**

   `Status: PASS - please verify no corrected errors`

{{&lt; /admonition &gt;}}

```bash
# -s 测试时长 86400(24hrs) 或 43200(12hrs) 或 28800(8hrs)
# -M 测试大小 128M
# -f 新增 disk 线程测试文件 /cache/temp1
# -f 新增 disk 线程测试文件 /cache/temp2
# -m copy 线程 0个
# -l 日志输出文件 /data/testfile
stressapptest -s 86400 -M 128 -f /cache/temp1 -f /cache/temp2 -m 0 -l /data/testfile
```

日志

```txt
/ # stressapptest -s 86400 -M 128 -f /cache/temp1 -f /cache/temp2 -m 0
2024/04/10-19:50:42(PDT) Log: Commandline - stressapptest -s 86400 -M 128 -f /cache/temp1 -f /cache/temp2 -m 0
2024/04/10-19:50:42(PDT) Stats: SAT revision 1.0.4_autoconf, 64 bit binary
2024/04/10-19:50:42(PDT) Log: Android version from open source release
2024/04/10-19:50:42(PDT) Log: 1 nodes, 2 cpus.
2024/04/10-19:50:42(PDT) Log: Prefer plain malloc memory allocation.
2024/04/10-19:50:42(PDT) Log: Using mmap() allocation at 0x7fa4000000.
2024/04/10-19:50:42(PDT) Stats: Starting SAT, 128M, 86400 seconds
2024/04/10-19:50:42(PDT) Log: Region mask: 0x1
2024/04/10-19:50:52(PDT) Log: Seconds remaining: 86390
2024/04/10-19:51:02(PDT) Log: Seconds remaining: 86380
2024/04/10-19:51:12(PDT) Log: Seconds remaining: 86370
2024/04/10-19:51:22(PDT) Log: Seconds remaining: 86360
2024/04/10-19:51:32(PDT) Log: Seconds remaining: 86350
^C2024/04/10-19:51:40(PDT) Log: User exiting early (86342 seconds remaining)
2024/04/10-19:51:41(PDT) Stats: Found 0 hardware incidents
2024/04/10-19:51:41(PDT) Stats: Completed: 2016.00M in 58.44s 34.50MB/s, with 0 hardware incidents, 0 errors
2024/04/10-19:51:41(PDT) Stats: Memory Copy: 0.00M at 0.00MB/s
2024/04/10-19:51:41(PDT) Stats: File Copy: 2016.00M at 34.50MB/s
2024/04/10-19:51:41(PDT) Stats: Net Copy: 0.00M at 0.00MB/s
2024/04/10-19:51:41(PDT) Stats: Data Check: 0.00M at 0.00MB/s
2024/04/10-19:51:41(PDT) Stats: Invert Data: 0.00M at 0.00MB/s
2024/04/10-19:51:41(PDT) Stats: Disk: 0.00M at 0.00MB/s
2024/04/10-19:51:41(PDT)
2024/04/10-19:51:41(PDT) Status: PASS - please verify no corrected errors
2024/04/10-19:51:41(PDT)
```


---

> 作者: Somebody  
> URL: https://zack4396.github.io/documentation/operating-system/001-linux/099-tools/stressapptest/  

