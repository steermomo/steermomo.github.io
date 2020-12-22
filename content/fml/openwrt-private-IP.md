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

### 2020-12-22更新
忘记有这么个事情了。
这个问题是DNSmasq中的rebind_protection造成的，在[Openwrt的文档](https://openwrt.org/docs/guide-user/base-system/dhcp)中可以看到关于rebind_protection的说明。
> rebind_protection
> 
> --stop-dns-rebind
> 
> Enables DNS rebind attack protection by discarding upstream RFC1918 responses

而RFC1918指的是私有网络地址分配，这里遇到的问题就是zerotier-one分配的地址是私有IP，而我把一个域名解析到这个私有IP上了，在DNSmasq这一层会把它当作DNS重新绑定攻击，直接把这个请求给抛弃掉了，导致在内网中解析出现问题。
解决方法就是关闭rebind_protection。

