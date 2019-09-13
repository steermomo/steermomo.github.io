Title: Categorical Feature Encoding Challenge
Date: 2019-09-10 18:19
Modified: 2019-09-19 18:19
Category: Python, Kaggle, ML
Tags: ML, 
Slug: Categorical-Feature-Encoding-Challenge
Summary: 


这是一个PlayGround的比赛, 所以数据很简单, 目的应该就是练习. 

<img src="{static}/images/cat-header.png" style="max-width: 80%">

我是在做IEEE-CIS Fraud Detection的时候, 觉得自己连特征工程都不会做.  那种啥How win a Kaggle Competition的, 听了好几个了,啥也不会.

Categorical Feature Encoding Challenge 的数据介绍是这样的.

>A common task in machine learning pipelines is encoding categorical variables for a given algorithm in a format that allows as much useful signal as possible to be captured.
>
>Because this is such a common task and important skill to master, we've put together a dataset that contains only categorical features, and includes:
>binary features  
>low- and high-cardinality nominal features  
>low- and high-cardinality ordinal features  
>(potentially) cyclical features  

这里的特征就是二元属性bin_0-4, 类别属性nom_0-9, 序列属性ord_0-5, 在加上两个属性`day`和`month`. 


做这个Categorical Feature Encoding Challenge更是绝望啊,  因为我一通操作, 将所有的categorical feature都编码好了, 扔进`Catboost`一跑, 比别人的baseline还低三个点. 我这里的local cv只有0.777 

只能排查是不是我哪里编码不合适, 模型参数是不是不太好. 折腾完还是不知道问题在哪, 索性看别人baseline的notebook, 除了序列属性处理了之外, 其他都保持不动.  emmm🙄, 把除了序列属性的处理部分之前的全部注释掉, 直接扔到Catboost里.

Local CV 0.800827  &  LB 0.80508

😤这还有什么好处理的

<img src="{static}/images/what.jfif" style="max-width: 80%">

