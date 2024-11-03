+++
title = "Starship配置命令行提示符"
date = "2021-05-11T00:00:38+08:00"

#
# description is optional
#
# description = "An optional description for SEO. If not provided, an automatically created summary will be used."

tags = []
+++



最近尝试了一下Starship，其官方声称是一个CROSS-SHELL PROMPT，用RUST实现，看起来蛮高级迅速。
整了一下配置过程，发现中文网络上对其的配置过程介绍的比较少。

## 移除oh-my-zsh
之前一直用的是oh-my-zsh，有了新玩具，旧的先移除了。直接在终端中使用移除命令即可。
```bash
uninstall_oh_my_zsh
```

## 安装Starship
在这篇文章写作的时候，brew中还没有针对M1芯片的包，安装过程直接使用了shell脚本

```bash
sh -c "$(curl -fsSL https://starship.rs/install.sh)"
```

## 安装Nerd字体

从 www.nerdfonts.com 上下载字体，我使用的是Fira Mono Nerd Font
并在终端中启用字体

## 配置启动

在 ~/.zshrc 文件的最末端加上如下命令用于自动启动starhip。
```
# ~/.zshrc

eval "$(starship init zsh)"
```

## ys主题配置格式
在使用starship之前，一直用的是oh-my-zsh，ys主题，
<img style="width: 70%;" src="https://user-images.githubusercontent.com/49100982/108255792-be1ede00-716d-11eb-8c26-f7ad7ab3c4f2.jpg">
</img>


而Starship默认的提示格式也太简陋了，上一条线就给了目录，下一条线给了个箭头完事

<div style="margin: auto;">
<video style="width: 70%;display: block;margin: 0 auto;" muted="muted" autoplay="autoplay" loop="loop" playsinline="" class="demo-video"><source src="https://starship.rs/demo.webm" type="video/webm"> <source src="https://starship.rs/demo.mp4" type="video/mp4"></video>
</div>

这里想把它改成ys主题的形式，ys的配置文件[^1]中给出了配置格式
```bash
# Prompt format:
#
# PRIVILEGES USER @ MACHINE in DIRECTORY on git:BRANCH STATE [TIME] C:LAST_EXIT_CODE
# $ COMMAND
#
# For example:
#
# % ys @ ys-mbp in ~/.oh-my-zsh on git:master x [21:47:42] C:0
# $
PROMPT="
%{$terminfo[bold]$fg[blue]%}#%{$reset_color%} \
%(#,%{$bg[yellow]%}%{$fg[black]%}%n%{$reset_color%},%{$fg[cyan]%}%n) \
%{$fg[white]%}@ \
%{$fg[green]%}%m \
%{$fg[white]%}in \
%{$terminfo[bold]$fg[yellow]%}%~%{$reset_color%}\
${hg_info}\
${git_info}\
${venv_info}\
 \
%{$fg[white]%}[%*] $exit_code
%{$terminfo[bold]$fg[red]%}$ %{$reset_color%}"
```

## 配置Starship
在Starship中，直接使用 starship config 命令可以打开配置文件。

配置过程看起来有点复杂，Starship中对prompt的配置[^2]给出了一个示例
```bash
# Use custom format
format = """
[┌───────────────────>](bold green)
[│](bold green)$directory$rust$package
[└─>](bold green) """
```

这个例子看起来还要手写format， 其中format所有可用的配置项目如下
```bash
format = "$all"

# Which is equivalent to
format = """
$username\
$hostname\
$shlvl\
$kubernetes\
$directory\
$vcsh\
$git_branch\
$git_commit\
$git_state\
$git_status\
$hg_branch\
$docker_context\
$package\
$cmake\
$dart\
$deno\
$dotnet\
$elixir\
$elm\
$erlang\
$golang\
$helm\
$java\
$julia\
$kotlin\
$nim\
$nodejs\
$ocaml\
$perl\
$php\
$purescript\
$python\
$red\
$ruby\
$rust\
$scala\
$swift\
$terraform\
$vagrant\
$zig\
$nix_shell\
$conda\
$memory_usage\
$aws\
$gcloud\
$openstack\
$env_var\
$crystal\
$custom\
$cmd_duration\
$line_break\
$lua\
$jobs\
$battery\
$time\
$status\
$shell\
$character"""
```

对比oh my zsh中ys主题的配置，大概的格式如下
```bash
ys @ ys-mbp in ~/.oh-my-zsh on git:master x [21:47:42] C:0
用户名 @ 主机名 in 路径 on git分支提示 时间 状态码
```

倒腾了一小会，发现不需要自己再手动写配置格式，在Starship的Configuration部分已经预置了很多场景下的配置项，
只是默认情况下没有打开。

比如需要添加Username项目，在starship.toml文件内添加
```
[username]
disabled = false
show_always = true
```
就能在提示符中显示Username了。

若设置成类似于ys主题的效果，其完整的配置内容如下

```bash
# Use custom format

[username]
style_user = "white bold"
style_root = "black bold"
format = "[$user]($style) "
disabled = false
show_always = true

[directory]
truncation_length = 8
truncation_symbol = "…/"

[hostname]
ssh_only = false
format =  "on [$hostname](bold red) "
trim_at = ".companyname.com"
disabled = false

[status]
style = "bg:blue"
symbol = "🔴"
format = '[\[$symbol $common_meaning$signal_name$maybe_int\]]($style) '
map_symbol = true
disabled = false

[time]
disabled = false
format = '[\[ $time \]]($style) '
time_format = "%T"
utc_time_offset = "+8"
```

## 小结
在Startship中，可以通过starship config 命令直接打开toml格式的配置文件。
如果要自定义prompt格式，可以通过手写format字串的方式实现灵活的自定义过程，
更简单的是使用其预设的配置，基本是如下的定义格式
```bash
[预设项名称]
配置1=值1
配置2=值2
```
详细的预设内容在Starship的Configuration[^3]内有文档说明，
通过该配置文档可以避免手写format。

[^1]:https://github.com/ohmyzsh/ohmyzsh/blob/master/themes/ys.zsh-theme
[^2]:https://starship.rs/config/#prompt
[^3]: https://starship.rs/config/#configuration