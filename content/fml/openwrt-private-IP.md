Title: OpenWrt不能解析内网地址
Date: 2020-04-10
Modified: 2020-04-10
Category: Linux
Tags: Linux, DNS, OpenWrt
Slug: openwrt-resolve-private-IP

目前在不同的网络环境下有多台设备，我是用zerotier-one把他们组到一个虚拟局域网内，并用子域名管理这些内网地址。

前几天将家里光猫改成桥接，拨号放到了一台OpenWrt设备上，发现在这个网络下无法解析内网地址.

```bash
$ nslookup whatever.steer.space
Server:		2409:8a30:ac5b:64f0::1
Address:	2409:8a30:ac5b:64f0::1#53

Non-authoritative answer:
*** Can't find whatever.steer.space: No answer
```

在指定解析服务器时，结果是正常的

```bash
$ nslookup whatever.steer.space 208.67.222.222
Server:		208.67.222.222
Address:	208.67.222.222#53

Non-authoritative answer:
Name:	whatever.steer.space
Address: 172.26.48.92
```



<img src="{static}/images/what.jfif" style="max-width: 80%">



Update...

