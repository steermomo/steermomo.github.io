Title: 为Pelican编写插件
Date: 2020-03-31
Category: Pelican
Tags: Pelican, Python

🐧

这里为[Pelican][2]移植了一个静态的相册[Sigal][1]，使得相册程序也能托管在Github Page上。





很久之前就有打算过给Pelican写个插件实现这样的功能，一直没有仔细看过Pelican的实现逻辑是怎么样的，今天刚好看到了这样一个静态相册，花了一晚上的时间将其以插件的形式集成到Pelican中。

Pelican中关于插件的文档并不是很多，文档中给的样例很短

```python
from pelican import signals

def test(sender):
    print "%s initialized !!" % sender

def register():
    signals.initialized.connect(test)
```

看起来是自己实现一个处理函数，然后将这个函数注册到Pelican内部的信号量上，这样Pelican会将自定义函数插入到处理的流程中，类似于在水管中多加了一段。

关于信号量的说明也是看得我一脸懵逼，我在整个都实现完之后才看明白不同的阶段及参数是什么意思。



Signal是可以直接从文件夹生成相册，还会有其他的一些自定义修饰。我觉得这个特性拿来配置在静态博客下也是很方便的，更重要的是不用再担心图床什么时候挂掉了。



在Pelican中，如果要生成新的页面而不是在已有的内容上添加的话，需要自定义`generator`， 文档中给了比较短的一段示例

```python
def get_generators(pelican_object):
    # define a new generator here if you need to
    return MyGenerator

signals.get_generators.connect(get_generators)
```

这个也是说的不太明白，文档中还有一段`How to implement a new generator?`提到了，`generator`需要实现两个方法，这两个方法将会被依次调用

- `generate_context` 这个方法就是要生成所需要的信息，用于传递给jinja2模板。
- `generate_output` 这个方法用来生成页面，将会传入一个`writer`的参数，用于控制jinja2的一些参数，以及写入内容的字典。



实际上这两个方法要怎么生成，内部该有怎样的结构，只能看源码了。 我按照Pelican中`generator.py`的代码，模仿着写了一个`gallery_generator`类。这个类的内部代码则是从Signal移植过来的。



Signal的代码是没有办法直接拿来用的，它本来就是一个独立的项目，实现了自己的`writer`用于控制页面生成。 需要把其中相关的代码抽出来，调整成与Pelican适配的形式。

其中模板文件跟CSS比较好改写，需要将jinja2模板中的路径改成带参数的。 比较费时的是Signal中`url`的生成，与Pelican的规则完全不搭配。 Signal本身的`url`生成都是基于根目录的，而在Pelican中需要将`content`中的内容搬到`output`下的子目录中，作为静态博客的一个子部分，原来的相对路径都不对。

在这样一个项目中调试比较难(或者说我压根不会加断点调试)，全靠`logger`提供信息，最后所有的`URL`生成都被我改成用绝对路径了(带参数自动配置)。 Debug不如重写来得快。



陆续花了7小时左右的时间，静态博客也用上相册了🐧




[1]: Sigal	"http://sigal.saimon.org/en/latest/"
[2]: Pelican "https://blog.getpelican.com/"

