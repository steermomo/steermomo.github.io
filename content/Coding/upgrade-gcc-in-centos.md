Title: CentOS中更新GCC
Date: 2021-01-28 18:20
Modified: 2021-01-28 18:20
Category: Coding
Tags: CentOS,GCC,SCL
Slug: upgrade-gcc-in-centos
<!-- Status: draft -->

厂里的系统都是基于CentOS 的，就是那个
> One centOS 倒下了，Ten centOS 起来了

的CentOS 。

这玩意的问题就是它实在是太老了，我要装一下xgboost编译都不成功。

看了一下目前GCC的版本还是`4.8.5`, 而GCC都出到`10.2`了[^1], 真心穿越千年的爱恋。

```bash
$ gcc -v
Using built-in specs.
COLLECT_GCC=gcc
COLLECT_LTO_WRAPPER=/usr/libexec/gcc/x86_64-redhat-linux/4.8.5/lto-wrapper
Target: x86_64-redhat-linux
Configured with: ../configure --prefix=/usr --mandir=/usr/share/man --infodir=/usr/share/info --with-bugurl=http://bugzilla.redhat.com/bugzilla --enable-bootstrap --enable-shared --enable-threads=posix --enable-checking=release --with-system-zlib --enable-__cxa_atexit --disable-libunwind-exceptions --enable-gnu-unique-object --enable-linker-build-id --with-linker-hash-style=gnu --enable-languages=c,c++,objc,obj-c++,java,fortran,ada,go,lto --enable-plugin --enable-initfini-array --disable-libgcj --with-isl=/root/rpmbuild/BUILD/gcc-4.8.5-20150702/obj-x86_64-redhat-linux/isl-install --with-cloog=/root/rpmbuild/BUILD/gcc-4.8.5-20150702/obj-x86_64-redhat-linux/cloog-install --enable-gnu-indirect-function --with-tune=generic --with-arch_32=x86-64 --build=x86_64-redhat-linux
Thread model: posix
gcc version 4.8.5 20150623 (Red Hat 4.8.5-5) (GCC)
```

这个直接upgrade也是不成功滴，压根没有新版本可以升，系统的版本都太老了。
```bash
$ cat /etc/centos-release
CentOS Linux release 7.2 (Final)
```

本着遇事不决上stackoverflow的原则，在SO上也找到了一个例子[^2]，可惜的是第二个命令运行不起来。
根据发本文时的软件状况以及本机环境，这里需要先安装Software Collections (SCL)，再安装devtoolset-8。
```bash
sudo yum install -y centos-release-scl
sudo yum install -y devtoolset-8
scl enable devtoolset-8 bash
which gcc
gcc --version
```

这样装完之后就能生效了，可以看到GCC的版本已经变了
```bash
gcc (GCC) 8.3.1 20190311 (Red Hat 8.3.1-3)
Copyright (C) 2018 Free Software Foundation, Inc.
This is free software; see the source for copying conditions.  There is NO
warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
```

再安装XGBoost，终于成功了。


### 小结
根据CentOS的wiki[^3], SCL是指软件选集(Software Collections, SCL), SCL的目的就是为老旧的CentOS提供新版的软件集, 
安装完SCL和需要的软件集后，启动环境的命令是
```bash
$ scl enable <scl-package-name> <command>
```
在前面的例子中, 要在多个命令下都启动GCC的环境, 使用的就是调起bash, 在新的shell内执行.
```bash
$ scl enable devtoolset-8 bash
```

 要检查已经安装的SCL集合，可以用
```bash
$ scl --list
```

更多的信息可以看SCL的QuickStart指引[^4]以及Xmodulo的介绍[^5]。


[^1]: https://gcc.gnu.org/
[^2]: https://stackoverflow.com/questions/36327805/how-to-install-gcc-5-3-with-yum-on-centos-7-2
[^3]: https://wiki.centos.org/zh/AdditionalResources/Repositories/SCL
[^4]: https://www.softwarecollections.org/en/docs/
[^5]: https://www.xmodulo.com/enable-software-collections-centos.html