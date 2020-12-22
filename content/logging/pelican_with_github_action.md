Title: 使用Github Action自动构建Pelican
Date: 2020-12-22 18:20
Modified: 2020-12-22 18:20
Category: Python
Tags: pelican, publishing

我自己在博客的部署上，大致经历了三个阶段：

+ Wordpress
+ Hexo
+ Pelican + Travis
+ Pelican + Github Action

对我来说，Pelican + Github Action是静态页面部署的最佳实践。

Wordpress的功能对我来说有些太多了，有些繁重，我只需要一个静态的页面托管一些想法就够了。在WP之后使用了Hexo，本地生成页面后推送到Github Pages分支上去，Hexo令人烦恼的是`node_modules`，而且一旦本地丢了文件或者换环境部署就特别麻烦。在折腾Hexo的过程中也看到有人想办法构建了绿色版的node环境放在移动存储设备中，实现环境的简单迁移。

这种将数据与环境封在一起的做法还是不够简洁，在那之后我开始用Pelican。只要有对应的Python包环境，就能一键编译出静态页面，只需要持续保留原文档即可。
为了将原始的文档将生成的页面分离，又用了Travis去做持续集成。Travis监控并拉去github上的分支，将编译后的文件推送到另外一个分支内，以此实现原文档与生成文件的分离。

Travis的一个不太完美的地方就是，它还是一个第三方的网站。在Github Action推出之后我就一直想将持续集成迁移到Github自带的服务上。

## 创建Workflow
在项目的选项卡中选择`Action`，然后使用`New workflow`，创建新的CI流程，这一步会在项目的`.github/workflows`下创建`.yml`格式的配置文件。

## Workflow配置
下面贴上我的CI配置，关于Github Actions的说明可以直接看[GitHub Actions文档](https://docs.github.com/cn/free-pro-team@latest/actions)或者[阮一峰的GitHub Actions 入门教程](http://www.ruanyifeng.com/blog/2019/09/getting-started-with-github-actions.html)。

在项目的根目录下需要有`requirements.txt`配置相关的包依赖，配置中的 __Install dependencies__ 这一步会安装相应的依赖，__Generate pages__ 这一步会调用pelican的命令行将静态页面生成到`output`目录下，__Push content__ 会在`output`路径下创建初始化git， 并将该路径下的所有文件推送到gh-pages分支下。对gh-pages这一分支，并没有必要保存历史的commit，使用force命令强制覆盖这一分支。

> --force
> 
> Usually, the command refuses to update a remote ref that is not an ancestor of the local ref used to overwrite it. Also, when --force-with-lease option is used, the command refuses to update a remote ref whose current value does not match what is expected.


```yml
# This workflow will install Python dependencies, run tests and lint with a single version of Python
# For more information see: https://help.github.com/actions/language-and-framework-guides/using-python-with-github-actions

name: Python application

on:
  push:
    branches: [ origin ]
  pull_request:
    branches: [ origin ]

jobs:
  build:

    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v2
    - name: Set up Python 3.8
      uses: actions/setup-python@v2
      with:
        python-version: 3.8
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
    - name: Generate pages
      run: |
        pelican content -o output -s ${PELICAN_CONFIG_FILE:=pelicanconf.py}
    - name: Push content
      run: |
        remote_repo="https://x-access-token:${{secrets.GITHUB_TOKEN}}@github.com/${GITHUB_REPOSITORY}.git"
        remote_branch=${GH_PAGES_BRANCH:=gh-pages}
        
        cd output
        git init
        git add -A
        git config user.name "${GITHUB_ACTOR}"
        git config user.email "${GITHUB_ACTOR}@users.noreply.github.com"
        git remote add deploy "$remote_repo"
        git checkout $remote_branch || git checkout --orphan $remote_branch
        echo -n 'Files to Commit:' && ls -l | wc -l
        timestamp=$(date +%s%3N)
        git commit -m "[ci skip] Automated deployment to GitHub Pages on $timestamp"
        git push deploy $remote_branch --force
        rm -fr .git
        cd ../
        echo '=================== Done  ==================='
```

## 自动持续集成
在配置完Github Action后，只需要操心原文档存放的分支。每次更新原文档后，推送到GitHub上，GitHub Actions会自动编译改动，将结果更新到gh-pages，从而实现了原文档与环境、编译输出文件的分离。