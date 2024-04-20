# stress-ng


**本文介绍了如何使用 stress-ng**

&lt;!--more--&gt;

[Github]: https://github.com/ColinIanKing/stress-ng.git
[V0.17.07]: https://github.com/ColinIanKing/stress-ng/archive/refs/tags/V0.17.07.tar.gz

## 获取源码

仓库地址：[Github], 最新版本是 [V0.17.07]

### 下载

```bash
wget https://github.com/ColinIanKing/stress-ng/archive/refs/tags/V0.17.07.tar.gz
```

### 解压

```bash
tar -zxvf V0.17.07.tar.gz -C . &amp;&amp; cd stress-ng-0.17.07
```

## 编译源码

### 编译 x86

```bash
make clean &amp;&amp; make

# 查看生成文件
ls stress-ng
```

### 编译 aarch64

```bash
# 指定 对应平台的 GCC 路径
MY_CC=/opt/toolchain/aarch64/bin/aarch64-cros-linux-gnu-gcc
```

```bash
MY_HOST=&#34;$(echo $(basename $MY_CC) | sed &#39;s/-gcc$//&#39;)&#34;
MY_CXX=&#34;$(dirname $MY_CC)/$MY_HOST-g&#43;&#43;&#34;

# 编译报错: error: redefinition of ‘struct rseq’
# 需添加 &#39;CFLAGS=-D__GLIBC_HAVE_KERNEL_RSEQ&#39;
make clean &amp;&amp; make CC=$MY_CC CXX=$MY_CXX CFLAGS=-D__GLIBC_HAVE_KERNEL_RSEQ

# 查看生成文件
ls stress-ng
```

## 工具使用

### 命令行参数

```bash
/data # stress-ng --help
Usage: stress-ng [options]

--matrix [?]     启动 ? 个 worker 进行矩阵运算
-t [?]           设置测试超时时长 [?] 秒
-l [?]           设置CPU Loading 百分比 [?]%
--metrics-brief  启用指标并仅显示非零结果
--tz             从 thermal zone 收集温度数据
-v               启用详细输出
```

### 用途

#### 测试 CPU

```bash
# --matrix         启动 0 个 worker 进行矩阵运算
# -t               设置测试超时时长为 1440m(24hrs) 或 720m(12hrs) 或 480m(8hrs)
# -l               设置 CPU 负载为 80%
# --metrics-brief  启用指标并仅显示非零结果
# --tz             从 thermal zone 收集温度数据
# -v               启用详细输出
stress-ng --matrix 0 -t 1440m -l 80 --metrics-brief --tz -v
```

日志

```txt
/data # stress-ng --matrix 0 -t 1m -l 80 --metrics-brief --tz -v
stress-ng: debug: [2851] 2 processors online, 2 processors configured
stress-ng: info:  [2851] dispatching hogs: 2 matrix
stress-ng: info:  [2851] cache allocate: using built-in defaults as unable to ds
stress-ng: info:  [2851] cache allocate: default cache size: 2048K
stress-ng: debug: [2851] starting stressors
stress-ng: debug: [2851] 2 stressors spawned
stress-ng: debug: [2852] stress-ng-matrix: started [2852] (instance 0)
stress-ng: debug: [2853] stress-ng-matrix: started [2853] (instance 1)
stress-ng: debug: [2852] stress-ng-matrix: exited [2852] (instance 0)
stress-ng: debug: [2853] stress-ng-matrix: exited [2853] (instance 1)
stress-ng: debug: [2851] process [2852] terminated
stress-ng: debug: [2851] process [2853] terminated
stress-ng: info:  [2851] successful run completed in 60.00s (1 min, 0.00 secs)
stress-ng: info:  [2851] stressor       bogo ops real time  usr time  sys time s
stress-ng: info:  [2851]                           (secs)    (secs)    (secs)  )
stress-ng: info:  [2851] matrix            46456     60.00    118.51      0.01 7
stress-ng: info:  [2851] matrix:
stress-ng: info:  [2851]              thermal   62.50 °C
```

#### 测试 Memory

```bash
# -vm              启动 N 个虚拟内存压力器
# -vm-bytes        设置 测试的内存大小
# --timeout        设置 测试时长
stress-ng --vm 1 --vm-bytes 1G --timeout 60s
```


---

> 作者: Somebody  
> URL: https://zack4396.github.io/documentation/operating-system/001-linux/099-tools/stress-ng/  

