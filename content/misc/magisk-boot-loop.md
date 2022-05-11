Title: Magisk Patch boot.img 后无法启动(循环卡米)
Date: 2021-09-05 12:20
Tags:  Android, Magisk
Category: MISC
Slug: magisk-boot-loop

记录一下MIUI12 刷入Magisk后关闭校验。

## Magisk Patch boot.img 并刷入修改后的boot.img
从卡刷包内提取boot.img，放到手机的目录内，使用 Magisk 对其打补丁[^1]

1. 点击Magisk卡片上的安装按钮
2. 选择 “选择并修补一个文件”，点击开始后选择提取的boot.img
3. Magisk会对boot.img打补丁后存储到[Internal Storage]/Download/magisk_patched_[random_strings].img
4. 让设备进入到fastboot状态，在PC端刷入修改后的 boot.img

```
fastboot flash boot /path/to/magisk_patched.img
```


## 关闭 avb2.0校验

部分设备在刷入修改的boot.img后，会卡在无限重启，需要关闭avb2.0校验。

从卡刷包内提取vbmeta.img，直接刷入即可。
```
fastboot --disable-verity --disable-verification flash vbmeta vbmeta.img
```


[^1]: https://topjohnwu.github.io/Magisk/install.html