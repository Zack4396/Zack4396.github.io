# dhrystone


**本文介绍了如何使用 dhrystone**

&lt;!--more--&gt;

[fossies.org]: https://fossies.org/linux/privat/old/dhrystone-2.1.tar.gz/
[v2.1]: https://fossies.org/linux/privat/old/dhrystone-2.1.tar.gz/

## 获取源码

仓库地址：[fossies.org], 最新版本是 [V2.1]

### 下载

```bash
wget https://fossies.org/linux/privat/old/dhrystone-2.1.tar.gz
```

### 解压

```bash
mkdir dhrystone
tar -zxvf dhrystone-2.1.tar.gz -C dhrystone
cd dhrystone
```

## 编译源码

### 编译 x86

```bash
gcc -c -O2 -fno-inline dhry_1.c -o dhry_1.o -DTIME
gcc -c -O2 -fno-inline dhry_2.c -o dhry_2.o
gcc -o dhrystone dhry_1.o dhry_2.o

ls dhrystone
```

### 编译 aarch64

```bash
# 指定 对应平台的 GCC 路径
MY_CC=/opt/toolchain/aarch64/bin/aarch64-cros-linux-gnu-gcc
```

```bash
$MY_CC -c -O2 -fno-inline dhry_1.c -o dhry_1.o -DTIME
$MY_CC -c -O2 -fno-inline dhry_2.c -o dhry_2.o
$MY_CC -o dhrystone dhry_1.o dhry_2.o

ls dhrystone
```

## 工具使用

### 命令行参数

&gt; 无

### 用途

#### 测试 CPU 单核性能

{{&lt; admonition type=note open=false &gt;}}

关于测试日志，有几点我们可以关注一下

1. **Dhrystones per Second**

   &gt; 其数值表示每秒钟执行 Dhrystone 的次数

   `Dhrystones per Second:                      71332960.0`

2. **MIPS**

   &gt; 其数值表示每秒钟执行 Dhrystone 的次数除以一百万

   `MIPS: 71.33`

3. **DhrystoneMIPS**

   &gt; 其数值表示每秒钟执行 Dhrystone 的次数除以 1757
   &gt;
   &gt; 注：1757 (这一数值来自于 VAX 11/780机器，此机器在名义上为1MIPS机器，它每秒运行Dhrystone次数为1757次)

   `DMIPS: 40599.3`

{{&lt; /admonition &gt;}}

```bash
/data # ./dhrystone
...
Please give the number of runs through the benchmark: [***此处需要设置运行次数***]
...
```

日志

```txt
/data # ./dhrystone 500000000000

Dhrystone Benchmark, Version 2.1 (Language: C)

Program compiled without &#39;register&#39; attribute

Please give the number of runs through the benchmark: 50000000000000000

Execution starts, 784662528 runs through Dhrystone
Execution ends

Final values of the variables used in the benchmark:

Int_Glob:            5
        should be:   5
Bool_Glob:           1
        should be:   1
Ch_1_Glob:           A
        should be:   A
Ch_2_Glob:           B
        should be:   B
Arr_1_Glob[8]:       7
        should be:   7
Arr_2_Glob[8][7]:    784662538
        should be:   Number_Of_Runs &#43; 10
Ptr_Glob-&gt;
  Ptr_Comp:          -1262181728
        should be:   (implementation-dependent)
  Discr:             0
        should be:   0
  Enum_Comp:         2
        should be:   2
  Int_Comp:          17
        should be:   17
  Str_Comp:          DHRYSTONE PROGRAM, SOME STRING
        should be:   DHRYSTONE PROGRAM, SOME STRING
Next_Ptr_Glob-&gt;
  Ptr_Comp:          -1262181728
        should be:   (implementation-dependent), same as above
  Discr:             0
        should be:   0
  Enum_Comp:         1
        should be:   1
  Int_Comp:          18
        should be:   18
  Str_Comp:          DHRYSTONE PROGRAM, SOME STRING
        should be:   DHRYSTONE PROGRAM, SOME STRING
Int_1_Loc:           5
        should be:   5
Int_2_Loc:           13
        should be:   13
Int_3_Loc:           7
        should be:   7
Enum_Loc:            1
        should be:   1
Str_1_Loc:           DHRYSTONE PROGRAM, 1&#39;ST STRING
        should be:   DHRYSTONE PROGRAM, 1&#39;ST STRING
Str_2_Loc:           DHRYSTONE PROGRAM, 2&#39;ND STRING
        should be:   DHRYSTONE PROGRAM, 2&#39;ND STRING

Microseconds for one run through Dhrystone:    0.0
Dhrystones per Second:                      71332960.0
```


---

> 作者: Somebody  
> URL: https://zack4396.github.io/documentation/operating-system/001-linux/099-tools/dhrystone/  

