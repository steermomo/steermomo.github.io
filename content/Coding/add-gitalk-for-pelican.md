Title: 在Pelican中添加Gitalk
Date: 2020-12-29
Modified: 2020-12-29
Category: Coding
Tags: Pelican
Slug: add-gitalk-for-pelican

静态博客因为是静态的，所以评论系统啥的都得靠第三方的服务。

最开始用过多说，后来没了，煎蛋有段时间就是要从多说迁移出来，colt一直在说“快了”。
多说挂了之后就转到Disqus，现在又被墙了。

所以现在又开始白嫖Github的服务，加上[Gitalk](https://github.com/gitalk/gitalk)之后整个网站都挂在Github上了（编译、托管、评论服务）。

> Gitalk is a modern comment component based on GitHub Issue and Preact.

要在Pelican的系统上加上Gitalk也十分简单，Pelican的页面生成本来就是使用Jinja2模块化的，我目前的主题也是在Pelican原始的模板文件上魔改过来的。

下面的过程基本上都是参考Gitalk的文档指引完成的，添加了部分css用于跟正文部分的风格进行匹配。

## 申请GitHub Application
申请GitHub Application用于读写Github Issue，所有的评论内容都是写入到issue内。

## 修改base.html
根据Gitalk的文档，首先需要在页面内引入资源。 在Pelican中就是需要修改base.html文件，保证所有的页面都能引用到资源文件。
在base.html的head中加入

```html
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/gitalk@1/dist/gitalk.css">
  <script src="https://cdn.jsdelivr.net/npm/gitalk@1/dist/gitalk.min.js"></script>
```

## 修改日志页面，加入评论框

只需要在文章详情页加入评论系统，在Pelican内是修改article.html，在正文的后方加入
```html
<div id="comments">
  <h2 style="margin-top: 0.1rem;">Comments !</h2>
  <div id="gitalk-container"></div>
</div>
<script>
  var gitalk = new Gitalk({
    clientID: '4df********634',
    clientSecret: '4c7*****',
    repo: 'steermomo.github.io',
    owner: 'steermomo',
    admin: ['steermomo'],
    id: location.pathname,      // Ensure uniqueness and length less than 50
    distractionFreeMode: true,  // Facebook-like distraction free mode
    createIssueManually: true,
  })
  gitalk.render('gitalk-container')
</script>
```

上面的代码直接在文章的末尾添加了评论框容器，外层的comments容器用于控制评论框的风格。script内的配置字段参考Gitalk的文档说明填写就好。

## 修改main.css，风格适配
刚加入评论框的时候，视觉效果还是十分惨烈的，这里用我主文档部分的css进行了一下修饰，完工后就毫无违和感了。
```css
#comments {
    background: #fff;
    margin: 0 auto;
    margin-bottom: 1rem;
    overflow: hidden;
    padding: 20px 20px;
    width: 80%;
    max-width: 50rem;
    margin-top: 2rem;
    /* width: 80%; */
    border-radius: 5px;
    -moz-border-radius: 5px;
    -webkit-border-radius: 5px;
}
```


## Dang! 生成评论框 ↓↓↓↓↓