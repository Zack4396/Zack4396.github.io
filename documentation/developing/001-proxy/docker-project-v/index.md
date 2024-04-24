# Project V (Docker 篇)


**本文介绍了如何使用 Docker 设置 Project V**

&lt;!--more--&gt;

[uninstall-old-versions]: https://docs.docker.com/engine/install/ubuntu/#uninstall-old-versions
[install-using-the-repository]: https://docs.docker.com/engine/install/ubuntu/#install-using-the-repository
[subconvert.py]: /scripts/subconvert.py
[v2builder.py]: /scripts/v2builder.py

## 安装 docker

{{&lt; admonition type=note title=&#34;以 Ubuntu 22.04 为例&#34; open=false &gt;}}

{{&lt; /admonition &gt;}}

&gt; 参考 [Docker 安装文档：移除旧版本][uninstall-old-versions]
&gt;
&gt; 参考 [Docker 安装文档：使用 APT 存储库安装][install-using-the-repository]

安装步骤如下

### **1. 移除旧版本**

```bash
for pkg in docker.io docker-doc docker-compose docker-compose-v2 podman-docker containerd runc; do sudo apt-get remove $pkg; done
```

### **2. 设置源**

```bash
# Add Docker&#39;s official GPG key:
sudo apt-get update
sudo apt-get install -fy ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a&#43;r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
echo \
  &#34;deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release &amp;&amp; echo &#34;$VERSION_CODENAME&#34;) stable&#34; | \
  sudo tee /etc/apt/sources.list.d/docker.list &gt; /dev/null
sudo apt-get update
```

### **3. 安装 docker**

```bash
sudo apt-get install -fy docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

### **4. 添加当前用户到 docker 权限组**

{{&lt; admonition type=warning title=&#34;如果是通过 `ssh` 执行 `docker`命令，仍需要`sudo`权限 &#34; open=false &gt;}}

{{&lt; /admonition &gt;}}

```bash
# 设置好后,需要注销并重新登录用户, 设置才能生效
sudo groupadd docker
sudo usermod -aG docker $USER

# 适用 Debian 12 的命令
# sudo gpasswd -a $USER docker
# newgrp docker
```

## 运行 docker

### 1. 拉取 docker image (Project V 旧版本)

```bash
sudo docker pull v2ray/official
```

### 2. 准备 config.json 文件

&gt; 这里提供了两个脚本 subconvert.py 和 v2builder.py, 请自行下载

{{&lt; link href=&#34;/scripts/subconvert.py&#34; content=&#34;subconvert.py&#34; title=&#34;subconvert.py&#34; download=&#34;subconvert.py&#34; card=true &gt;}}

{{&lt; link href=&#34;/scripts/v2builder.py&#34; content=&#34;v2builder.py&#34; title=&#34;v2builder.py&#34; download=&#34;v2builder.py&#34; card=true &gt;}}

- 生成 serverxx.conf 文件

  {{&lt; admonition type=note title=&#34;此处需要填写正确的订阅链接&#34; open=false &gt;}}

  {{&lt; /admonition &gt;}}

  ```bash
  # 需要安装一下 request 依赖库
  pip install requests
  ```

  ```bash
  # 使用 subconvert.py 脚本从订阅链接中获取服务器信息，并将其保存到指定文件夹
  # 调用 Python3 脚本 subconvert.py，传入以下参数：
  # --subscribe 指定订阅链接为 https://sub.xxx.com/api/v1/client/subscribe?token=xxxxx，
  #             其中 token=xxxxx 是订阅的令牌或者身份验证信息。
  # --outdir 指定服务器信息的保存文件夹为 ~/.cache，表示保存到当前用户的缓存文件夹中。
  python3 subconvert.py \
    --subscribe https://sub.xxx.com/api/v1/client/subscribe?token=xxxxx \
    --outdir $HOME/.cache
  ```

  ```bash
  # 查看保存的服务器信息
  ls $HOME/.cache/server* -l
  /home/xxx/.cache/server01.conf
  ...
  /home/xxx/.cache/server20.conf
  ```

- 生成 config.json 文件

  {{&lt; admonition type=tip title=&#34;根据需要，可使用不同的 server.conf 和 http_port &#34; open=false &gt;}}

  {{&lt; /admonition &gt;}}

  ```bash
  # 使用 server01.conf 中的服务器信息生成对应的 V2 配置文件
  # 调用 Python3 脚本 v2builder.py，传入以下参数：
  # --input 指定服务器信息文件的路径为 $HOME/cache/server01.conf
  # --output 指定生成的 V2 配置文件的保存路径为 /tmp/config.json
  # --http_port 指定 HTTP 代理端口为 10809（如果未指定，则使用默认值 10809）
  # --allow_lan 若需要多台电脑可用，需要指定 --allow_lan
  #            若限本机使用，无需指定
  python3 v2builder.py \
    --input $HOME/cache/server01.conf
    --output /tmp/config.json \
    --http_port 10809 --allow_lan
  ```

  {{&lt; admonition type=note title=&#34;手动修改 rules, 添加你要代理的 IP, 再重复上面的步骤&#34; open=false &gt;}}

  {{&lt; /admonition &gt;}}

  ```bash
  $ vi ~/.v2rules.json
  ...

  # 来自 direct_1st 分组下的所有域名  走直连
  # 来自 proxy_1st  分组下的所有域名  走代理
  ...
  # 来自 proxy_3rd  分组下的所有 IP   走代理
  ```

  {{&lt; image src=&#34;/documentation/developing/001-proxy/update-v2rules.png&#34; caption=&#34;新增两个要全局代理的 IP&#34; src_s=&#34;/documentation/developing/001-proxy/update-v2rules.png&#34; src_l=&#34;/documentation/developing/001-proxy/update-v2rules.png&#34; &gt;}}

### 3. 运行容器

- 启动容器

  {{&lt; admonition type=warning title=&#34;-p 10809:10809 与 前面的 http_port 端口号需要保持一致 &#34; open=false &gt;}}

  {{&lt; /admonition &gt;}}

  {{&lt; admonition type=warning title=&#34;如果要启动多个容器，避免端口冲突，请使用不同的端口&#34; open=false &gt;}}

  {{&lt; /admonition &gt;}}

  ```bash
  # 复制 config.json 到指定路径
  sudo cp /tmp/config.json /etc/v2ray-docker/config.json

  # 运行一个容器
  # 监听端口是 10809 -&gt; 10809
  sudo docker run -d --name proxy_box_01 \
    -v /etc/v2ray-docker:/etc/v2ray-docker \
    -p 10809:10809 \
    v2ray/official v2ray -config=/etc/v2ray-docker/config.json
  ```

- 查看容器状态

  ```bash
  $ sudo docker container ls
  CONTAINER ID   IMAGE            COMMAND                  CREATED       STATUS       PORTS                                           NAMES
  1f6d4cffcc23   v2ray/official   &#34;v2ray -config=/etc/…&#34;   2 hours ago   Up 2 hours   0.0.0.0:10809-&gt;10809/tcp, :::10809-&gt;10809/tcp   proxy_box_01
  ```

- 停止容器

  ```bash
  # 停止 proxy_box_01 容器
  sudo docker container stop proxy_box_01
  ```

- 删除容器

  ```bash
  # 删除 proxy_box_01 容器
  sudo docker container rm proxy_box_01
  ```

### 4. 一键运行脚本

{{&lt; admonition type=tip title=&#34;一个简单的启动脚本&#34; open=false &gt;}}

{{&lt; /admonition &gt;}}

```bash
#!/bin/bash
# 根据个人需要, 选择不同的端口和server.conf
proxy_port=10809
proxy_conf=$HOME/.cache/server02.conf
proxy_name=proxy_box_01

python3 ~/bin/v2builder.py --input $proxy_conf --output /tmp/config.json --http_port $proxy_port --allow_lan
sudo mv /tmp/config.json /etc/v2ray-docker/config.json

sudo docker container stop $proxy_name
sudo docker container rm $proxy_name
sudo docker run -d --name $proxy_name -v /etc/v2ray-docker:/etc/v2ray-docker -p $proxy_port:$proxy_port v2ray/official v2ray -config=/etc/v2ray-docker/config.json
```

- 测试 http proxy 连接

  ```bash
  # 注意此处的 local_ip 应为部署了该容器的机器 IP (使用 ifconfig 查看)
  local_ip=192.168.2.175

  # 若端口未指定，则默认的代理地址是 http://$local_ip:10809
  export http_proxy=&#34;http://$local_ip:10809&#34;
  export http_proxy=&#34;http://$local_ip:10809&#34;

  wget www.google.com.hk -O /dev/null
  ```


---

> 作者: Somebody  
> URL: https://zack4396.github.io/documentation/developing/001-proxy/docker-project-v/  

