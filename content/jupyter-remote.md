Title: Jupyter Notebook 允许远程访问
Date: 2019-08-10 10:20
Modified: 2019-08-10 19:30
Category: Python
Tags: jupyter notebook,
Slug: jupyter-notebook-server
Summary: Short version for index and feeds


jupyter notebook中关于这部分的文档[Here](https://jupyter-notebook.readthedocs.io/en/stable/public_server.html)

首先需要生成jupyter notebook的配置文件
```bash
$ jupyter notebook --generate-config
Writing default config to: /home/unnamed/.jupyter/jupyter_notebook_config.py
```

然后设置访问密码
```bash
$ jupyter notebook password
Enter password:
Verify password:
[NotebookPasswordApp] Wrote hashed password to /home/unnamed/.jupyter/jupyter_notebook_config.json
```

编辑配置文件
```bash
$ vim ~/.jupyter/jupyter_notebook_config.py 
```

搜索配置ip的位置
```
# vim 中键入 /
# 然后输入 c.NotebookApp.ip

# 修改如下
## The IP address the notebook server will listen on.
#c.NotebookApp.ip = 'localhost'

# 为

c.NotebookApp.ip = '*'
```
                      
