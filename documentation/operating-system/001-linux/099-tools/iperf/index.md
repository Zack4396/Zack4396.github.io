# iperf


**本文介绍了如何使用 iperf**

&lt;!--more--&gt;

[Github]: https://github.com/esnet/iperf
[V3.16]: https://github.com/esnet/iperf/releases/download/3.16/iperf-3.16.tar.gz

## 获取源码

仓库地址：[Github], 最新版本是 [V3.16]

### 下载

```bash
wget https://github.com/esnet/iperf/releases/download/3.16/iperf-3.16.tar.gz 
```

### 解压

```bash
tar -zxvf iperf-3.16.tar.gz &amp;&amp; cd iperf-3.16
```

## 编译源码

### 编译 x86

- 静态编译

  ```bash
  ./configure --enable-static-bin &amp;&amp; make clean &amp;&amp; make

  # 查看生成文件
  ls src/iperf3
  ```

- 动态编译

  ```bash
  ./configure &amp;&amp; make clean &amp;&amp; make

  # 动态编译生成的 src/ipef3 只是一个封装脚本
  # 最终调用的程序还是 src/.libs/iperf3 及其 src/.libs 下的 动态库文件
  ls src/iperf3
  ```

### 编译 aarch64

- 静态编译

  ```bash
  # 指定 对应平台的 GCC 路径
  MY_CC=/opt/toolchain/aarch64/bin/aarch64-cros-linux-gnu-gcc
  ```

  ```bash
  MY_HOST=&#34;$(echo $(basename $MY_CC) | sed &#39;s/-gcc$//&#39;)&#34;

  ./configure --enable-static-bin \
    --host=$MY_HOST \
    CC=$MY_CC

  make clean &amp;&amp; make

  # 查看生成文件
  ls src/iperf3
  ```

## 工具使用

### 命令行参数

- 服务端设置

  ```bash
  iperf3 [options]
  -s 作为 server 运行
  -i 报告的时间间隔
  ```

- 客户端设置

  ```bash
  iperf3 [options]
  -c 要连接的服务端的 ip
  -p 要连接的服务端的 port
  -t 测试时长
  -i 报告的时间间隔
  -b 每秒的数据量 (默认值为 0 等效于 无限制)  e.g. -b 0 或 -b 1G
  -R 以逆向模式运行 (服务器发送数据 T，客户端接收数据 R)
  ```

### 用途

#### 测试设备 RX/TX 性能

1. 准备测试环境

   &gt; 配置网络方式 1

   ```bash
   setup_wifi.sh ssid &lt;none|wpa|wpa2|wpa3&gt; [psk]
   ```

   &gt; 配置网络方式 2

   ```bash
   wpa_cli -i wlan0 scan
   wpa_cli -i wlan0 scan_results
   wpa_cli -i wlan0 add_network
   wpa_cli -i wlan0 set_network 0 ssid &#39;SSID&#39;
   wpa_cli -i wlan0 set_network 0 psk &#39;PASSWD&#39;
   wpa_cli -i wlan0 enable_network 0
   udhcpc -i wlan0
   wpa_cli save_config
   ```

   &gt; 查看设备 IP

   ```bash
   ifconfig
   ```

   &gt; 清除网络限制

   ```bash
   # 设备端
   iptables -F
   ```

   ```bash
   # 电脑端
   sudo ufw disable
   ```

2. 测试设备 RX 性能

{{&lt; admonition type=note title=&#34;测试时，设备与电脑需要使用同一个网络&#34; open=false &gt;}}

{{&lt; /admonition &gt;}}

- 设备作为 server, 接受数据包

  ```bash
  # 作为 server, 报告间隔为 1s
  /data # ./iperf3 -s -i 1
  -----------------------------------------------------------
  Server listening on 5201 (test #1)
  -----------------------------------------------------------
  Accepted connection from 192.168.2.175, port 52766
  [  5] local 192.168.2.128 port 5201 connected to 192.168.2.175 port 52774
  [ ID] Interval           Transfer     Bitrate
  [  5]   0.00-1.00   sec  5.88 MBytes  49.2 Mbits/sec
  ...
  ```

- 电脑作为 client, 发送数据包

  ```bash
  # 一个持续 60 秒的 iperf3 测试，向 IP 地址为 192.168.2.128、端口为 5201 的目标服务器发送到 1Gbps 速率的数据包
  xx@xx:~/linux$ ./iperf3-x86 -c 192.168.2.128 -p 5201 -t 60 -i 1 -b 1G
  Connecting to host 192.168.2.128, port 5201
  [  5] local 192.168.2.175 port 52774 connected to 192.168.2.128 port 5201
  [ ID] Interval           Transfer     Bitrate         Retr  Cwnd
  [  5]   0.00-1.00   sec  8.75 MBytes  73.4 Mbits/sec    0    481 KBytes
  [  5]   1.00-2.00   sec  7.50 MBytes  62.9 Mbits/sec  197    351 KBytes
  ```

3. 测试设备 TX 性能

{{&lt; admonition type=note title=&#34;测试时，设备与电脑需要使用同一个网络&#34; open=false &gt;}}

{{&lt; /admonition &gt;}}

- 设备作为 server, 发送数据包

  ```bash
  # 作为 server, 报告间隔为 1s
  /data # ./iperf3 -s -i 1
  -----------------------------------------------------------
  Server listening on 5201 (test #1)
  -----------------------------------------------------------

  Accepted connection from 192.168.2.175, port 60134
  [  5] local 192.168.2.128 port 5201 connected to 192.168.2.175 port 60140
  [ ID] Interval           Transfer     Bitrate         Retr  Cwnd
  [  5]   0.00-1.00   sec  6.12 MBytes  51.4 Mbits/sec    0    232 KBytes
  ...
  ```

- 电脑作为 client, 接受数据包

  ```bash
  # 一个持续 60 秒的 iperf3 测试，从 IP 地址为 192.168.2.128、端口为 5201 的目标服务器接收 1Gbps 速率的数据包
  xx@xx:~/linux$ ./iperf3-x86 -c 192.168.2.128 -p 5201 -t 60 -i 1 -b 1G -R
  Connecting to host 192.168.2.128, port 5201
  Reverse mode, remote host 192.168.2.128 is sending
  [  5] local 192.168.2.175 port 60140 connected to 192.168.2.128 port 5201
  [ ID] Interval           Transfer     Bitrate
  [  5]   0.00-1.00   sec  5.88 MBytes  49.2 Mbits/sec
  ```


---

> 作者: Somebody  
> URL: https://zack4396.github.io/documentation/operating-system/001-linux/099-tools/iperf/  

