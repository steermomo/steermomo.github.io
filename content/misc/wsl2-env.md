Title: WSL2环境踩坑配置
Date: 2020-12-24 18:20
Modified: 2020-12-24 18:20
Category: MISC
Tags: WSL2, Linux
Slug: wsl2-env

这两天装了好几遍WSL2... 每次都是要重新配置环境，开个页面集中记录一下做了哪些配置，免得又得开很多页面去找配置项

![](/images/wsl2-neofetch.png)

## 解决WSL2 DNS解析问题
在公司的内网环境下，Windows的升级都是由内部管理的，之前一直没法升级到支持WSL2的版本。

在几次更新后，终于用上了WSL2，但是将WSL1转为WSL2之后，DNS解析出现了问题。在WSL2内是有网络的，ping其他的ip地址都没有问题，需要解析域名的时候就挂了，
这里应该是内网的一些网络配置与WSL2的网络配置有不一致的地方。

反反复复将WSL2重装了几次都没有搞定，最后终于在一个[gist](https://gist.github.com/coltenkrauter/608cfe02319ce60facd76373249b8ca6)的评论下面找到了解决方法。

下面的`$`命令指示在Linux下的命令, `^$`指示Windows下的命令.

```bash
$ cd /etc
$ echo "[network]" | sudo tee wsl.conf
$ echo "generateResolvConf = false" | sudo tee -a wsl.conf 

^$ wsl --terminate

$ cd /etc
$ sudo rm -Rf resolv.conf 


# 下面在Windows下查找主机所用的DNS解析IP
^$ ipconfig /all 

# 将上一步找到的DNS解析替换到下面的xxxx内
$ echo "nameserver X.X.X.X" | sudo tee resolv.conf
$ echo "nameserver X.X.X.X" | sudo tee -a resolv.conf

^$ wsl --terminate

$ cd /etc
$ sudo chattr +i resolv.conf
```

## SSH会话复用
在内网中会有各种跳板机，跳板机认证又是各种token，每次连新机器都需要重连一次跳板机，这个过程繁琐又无趣，免认证的内部工具又不是很好用。

会话复用能让在已有一个跳板机连接后，后续的连接无需再次认证。

```bash
# ~/.ssh/config
Host *
    ControlMaster auto
    ControlPath ~/.ssh/sockets/%r@%h-%p
    ControlPersist 600
```
记得创建文件夹
```bash
mkdir ~/.ssh/sockets
```

## 配置WSL2 & Clion

后面的开发中希望能用Clion连接到WSL2的环境里，这里用Clion给的WSL2的配置脚本。

```bash
wget https://raw.githubusercontent.com/JetBrains/clion-wsl/master/ubuntu_setup_env.sh && bash ubuntu_setup_env.sh

```

## 解决WSL2挂载Windows磁盘的git权限问题

因为一些内网的限制，这里需要将代码放到Windows的硬盘上才能方便与远程环境进行代码同步。
在WSL2挂载的Windows磁盘中执行git clone会有权限问题.

> NTFS partitions do not support chmod or similar Linux permissions commands

根据万能的StackOverflow，这里应该在挂载的时候指定meta选项, 向/etc/wsl.conf文件添加

```bash
# /etc/wsl.conf 
[automount]
options = "metadata"
```


## ZSH

### oh-my-zsh

```bash
sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
```

### zsh-autosuggestions
设置zsh自动补全
```bash
git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions
```

```bash
plugins=(zsh-autosuggestions)
```
### pip3 package command not found 

```bash
# .zshrc
export PATH=$HOME/.local/bin:$PATH
```

## TMUX
tmux设置默认shell

```bash
# ~/.tmux.conf
set-option -g default-shell /bin/zsh
```