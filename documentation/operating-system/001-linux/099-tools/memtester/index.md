# memtester


**本文介绍了如何使用 memtester**

&lt;!--more--&gt;

[pyropus.ca]: https://pyropus.ca./software/memtester/
[v4.6.0]: https://pyropus.ca./software/memtester/old-versions/memtester-4.6.0.tar.gz

## 下载源码

仓库地址：[pyropus.ca], 最新版本是 [V4.6.0]

### 下载

```bash
wget https://pyropus.ca./software/memtester/old-versions/memtester-4.6.0.tar.gz
```

### 解压

```bash
tar -zxvf memtester-4.6.0.tar.gz -C . &amp;&amp; cd memtester-4.6.0
```



## 编译源码

### 编译 x86

```bash
make clean &amp;&amp; make

# 查看生成文件
ls memtester
```

### 编译 aarch64

```bash
# 指定 对应平台的 GCC 路径
MY_CC=/opt/toolchain/aarch64/bin/aarch64-cros-linux-gnu-gcc
```

```bash
# 修改编译脚本
sed -i s@cc@\$MY_CC@g ./conf-cc ./conf-ld

make clean &amp;&amp; make MY_CC=$MY_CC

# 查看生成文件
ls memtester
```



## 工具使用

### 命令行参数

```bash
/data # memtester --help
Usage: memtester [-p physaddrbase [-d device]] &lt;mem&gt;[B|K|M|G] [loops]
 
- mem 申请测试内存的数量，单位默认是megabytes(兆)，也可以是B K M G。
- loops 测试的次数，默认是无限
```



### 用途

#### 测试内存

```
# 指定
# - 起始地址 0x38000000
# - 内存大小 16M
# - 循环次数 2
memtester -p 0x38000000 16M 2

# 循环测试
memtester 16M
```

日志

```txt
/data # memtester 16M 1
memtester version 4.6.0 (64-bit)
Copyright (C) 2001-2020 Charles Cazabon.
Licensed under the GNU General Public License version 2 (only).

pagesize is 4096
pagesizemask is 0xfffffffffffff000
want 16MB (16777216 bytes)
got  16MB (16777216 bytes), trying mlock ...locked.
Loop 1/1:
  Stuck Address       : ok         
  Random Value        : ok
  Compare XOR         : ok
  Compare SUB         : ok
  Compare MUL         : ok
  Compare DIV         : ok
  Compare OR          : ok
  Compare AND         : ok
  Sequential Increment: ok
  Solid Bits          : ok         
  Block Sequential    : ok         
  Checkerboard        : ok         
  Bit Spread          : ok         
  Bit Flip            : ok         
  Walking Ones        : ok         
  Walking Zeroes      : ok         
  8-bit Writes        : ok
  16-bit Writes       : ok

Done.
```



---

> 作者: Somebody  
> URL: https://zack4396.github.io/documentation/operating-system/001-linux/099-tools/memtester/  

