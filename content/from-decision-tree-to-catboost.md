Title: 决策树, CART, GBDT, XGBoost, LightGBM, CatBoost
Date: 2019-09-13 18:10
Modified: 2019-09-13 18:10
Category: Machine Learning,
Tags: decision-tree, 
Slug: from-decision-tree-to-catboost
Summary: 

[TOC]

曾经我认为树模型很弱鸡, 毕竟有点像小朋友画的分支决策树, 选择题有啥好玩的. 🐱‍🐉 还是我太弱鸡了, 一群学渣互相交流, 也能将选择题做得很好.



这里我想整理一下从决策树到`CatBoost`相关的概念, 以及一些推导. `XGBoost`, `LightGBM`和`CatBoost`是在Kaggle表数据竞赛中, 必然会出现的三种模型. 想知道他们是怎么工作的, 应该要从决策树开始讲起, 因为后面的内容都是在决策树的基础上一步步构建出来的, 从决策树到提升方法, 到`GBDT的`一些概念, `XGBoost`又是在GBDT的基础上改进.  知道了前面的内容才会理解`LightGBM`是要解决什么问题, `CatBoost`又跟`LightGBM`有什么不同.



对于`GBDT`, 很多的文章或讲解都在说"拟合残差", "拟合梯度", 但是就不提为什么拟合残差, 为什么拟合梯度可行. 这里也按照GBDT的那篇文章, 整理了一下整个思考过程, 为什么会去拟合梯度, 以及是如何推导出拟合残差的.



这里主要看了几篇论文

1. Classification and regression trees[^1]

2. Greedy Function Approximation: A Gradient Boosting Machine[^2]
3. XGBoost: A Scalable Tree Boosting System[^3]
4. LightGBM: A Highly Efficient Gradient Boosting Decision Tree[^4]
5. CatBoost: gradient boosting with categorical features support[^5]

以及陈天奇的Slide: Introduction to Boosted Trees [^6], 西瓜书决策树章节和统计学习方法的决策树,提升方法部分. 

主要以论文为主, 书本对照一些基本的知识. 因为文章中的故事性比较好:  问题背景, 引入问题, 这部分设计是为了解决什么问题, 很有承接关系, 讲得比较清楚. 而国内的书一般是直接定义一个问题, 解决一个问题, 而很少讲为什么.







<br>

## 集成方法

首先要说一下集成方法,  因为后面的方法都是对树模型的集成.



集成方法可以分为两大类, 一种是基学习器之间不存在强依赖关系, 可以同时并行生成, 另外一种是基学习器之间有强依赖关系, 必须串行生成.



前者主要是**Bagging**和**随机森林**, 后者的代表是**Boosting方法**.



- **Bagging**是对数据做行抽样, 使用bootstrap sampling采样m次, 可并行获得m个模型, 再将m个模型进行组合. 每个模型的权重相同.

- **随机森林**是对数据做列抽样,  在训练决策树时随机选择属性.



**Boosting**是改变数据的分布, 有AdaBoost和Gradient Boosting.  

- **AdaBoost**是多轮训练, 在每一轮中,提升前一轮被错误分类的样本的权值, 具体的内容这里不提.

- **Gradient Boosting**是直接改变弱分类器的学习目标, 学习当前组合模型的梯度值. 具体的算法内容后面会讲到.



<br>

## 决策树

后面的方法用的都是树模型, 需要简单讲一下决策树是在干嘛.

<br>

### 决策树的直观概念

对于一个分类问题, 假设数据集$\{X_i\}$有$n$个样本, $p$个特征, 类别值$Y_i$有$k$个取值.   想要建立一个模型对这样的数据进行分类,  理论上只要将样本空间划分为$k$个不相交的区域就可以了,  简单的做法有LDA和kNN.  LDA的决策边界是线性的, 而kNN的决策边界是非线性的.  然而这样的作法太简单了:前者的线性决策边界太弱鸡了, 后者是惰性学习, 遇到大规模数据就炸了.



决策树每次选择一个特征, 在这个特征上对样本空间进行划分. 在划分的子样本空间上, 选择未被使用的离散特征(或已被使用的连续特征), 继续划分子空间. 这样递归地下去, 直至无法划分或者满足某个准则.  这些划分组合起来就是决策树的决策边界.

下图是`sklearn`的决策树边界示意图, 其特点是平行于特征轴.

<img src="http://ww1.sinaimg.cn/large/dd456925ly1g6y5fudu8bj20hs0dc762.jpg" style="max-witdh: 50%">

<br>

### 决策树的生成算法

有多种方法去生成一棵决策树.  

一个及其简单的决策树伪码可以这样描述

```
1. 从根结点开始

2. 对每个属性, 找到最佳的划分方法, 使得划分后的子树纯度最高

3. 如果满足停止准则, 则停止划分, 否则对每个子树递归调用第2步.
```



这个伪码的描述及其简单, 不过其本质就是这样. 如何构建树, 如何选择最优属性就是不同的算法实现. 



ID3算法使用信息增益作为准则选择特征, 但是偏向于选择可取值较多的属性, 在此基础上改进的C4.5算法使用信息增益率作为选择准则.   这两种方法生成的都是多叉树. 知道有这两种方法应该就行.



使用最广泛的决策树方法是CART(分类与回归树). CART使用基尼指数选择最优划分属性, CART内部是二叉树, 结点的特征取值为"是"和"否",  左分支为"是", 右分支为"否".  

CART既能用于分类, 也能用于回归.  在构建决策树时, 一个叶子节点可以满足数据集中的多个样本$D_k$, 在**分类**的情况下, 叶子节点的类别就是$D_k$中大部分样本的类别, 在**回归**的情况下, 叶子节点的值是$D_k$标签值的均值.



所以CART在处理回归问题时并不是像线性回归那样, 能够将样本空间映射到无穷的实域, 而是有限的点集.



如下是`sklearn`示例中的一棵决策树. 

<img src="http://ww1.sinaimg.cn/large/dd456925ly1g6y6gz7iv6j20u30nhdl2.jpg" style="max-witdh: 50%">









## Gradient Boosting到底是什么

梯度提升是在函数空间进行优化. 经常会看到梯度提升是在用每一轮的基学习器去拟合当前模型的梯度.  



将集成模型看作是一系列模型的累加, 用第一个模型学习样本目标, 那么第二个模型可以学习第一个模型与样本目标的差值, 这样他们累加起来仍然是逼近样本目标的.以此类推, 可以设置一系列的基学习器, 每一个都学习当前模型与目标的差值,  这样可以称为对残差的学习.



上面这个例子十分直观, 理解起来也完全没有问题, 介绍起来一点套路都没, 反正加起来就是最终要预测的目标嘛! 但是梯度提升去拟合当前模型的梯度, 直观上是很难理解的,  很多地方说梯度是残差的近似, 但是并没有说为什么梯度可以当作残存的近似. 



这一部分根据Gradient Boosting的那篇文章, 先介绍参数空间的优化, 再引入函数空间的优化,  最后导出为什么可以用基模型拟合梯度值, 而且所有模型加起来还是正确的.





### 问题引入

假设要在数据集$\{(x_i, y_i)\}$上训练一个函数$F(X)$, 使得损失函数$L(y, F(x))$在$(x,y)$的联合分布上最小化. 

那么有
$$
F^*=\arg \min_{F}E_{y, x}L(y, F(x))=\arg \min_F E_x[L(y, F(X))|x] \tag{GBM 1}
$$
可以定义参数化的函数簇, 来约束这样的$F(X)$, 即$F(x;P)$.

将该函数定义为加法模型, 则函数形式可写为
$$
F(x;\{\beta_m,a_m\}^M_1) = \sum_{m=1}^M\beta_mh(x;a_m) \tag{GBM 2}
$$
其中$h$为基函数, $a_m$为基函数的参数, $\beta_m$为加法模型权重.



这里只是介绍加法模型这样一个概念.





### 参数空间数值优化



对于上面定义的可以, 找到最优的参数$P*$,就找到了最优函数.可以通过数值优化的方法求解最优参数$P^*$
$$
P^*=\arg \min_{P} \Phi(P) \\
\Phi(P) = E_{y, x}L(y, F(x;P))
$$


数值优化的求解过程是一个迭代的过程, 因此可以将$P^*$写为
$$
P^*=\sum_{m=0}^Mp_{m} \tag{GBM 4}
$$
其中$p_0$是初始值, $\{p_m\}_1^M$ 是迭代过程中的增量(步长). 可以理解为从$p_0$开始, 迭代$M-1$次, 每次都会获得一个增量, 最终$P*$的值是初始值与迭代中增量的和.



每一步的增量$p_m$可以用数值优化方法求解.



### 最速梯度下降法

梯度下降没啥说的,  根据参数空间当前的梯度值, 可以迭代地对参数进行优化. 在上一步定义了一个由参数约束的函数, 用最速梯度下降法去优化参数.

在迭代的每一步中,  $p_m$处的梯度为
$$
g_m={g_{jm}}=\left\{ \left[\frac{\partial\Phi(P)}{\partial P_j}\right]_{P=P_{m-1}}\right\}
$$


其中，
$$
P_{m-1}=\sum_{i=0}^{m-1}p_i
$$
这个也很直观, 就是当前P的值. 接下来要去求, 当前的迭代步长应该是多少

取
$$
p_m = -\rho_mg_m
$$


这里$\rho_m$的求解如下
$$
-\rho_m=\arg \min_{\rho}\Phi(P_{m-1}-\rho g_m) \tag{GBM 5}
$$
上面这个式子的含义是, 在当前梯度方向上, 取使得目标函数最小的最大步长, 即用最快的速度下降(最速梯度).就是在当前的$P_{m-1}$处, 取沿着梯度方向尽可能地下降, 取最大的步长为$p_m$. 这里的$\rho_m$可以通过线性搜索求出.

这样一直迭代下去, 直到满足条件就能求出一个$P^*$出来.



### 函数空间的优化

上面的优化过程中, 固定了基函数的形式, 以及参数的数量, 优化过程是在参数空间完成的. 如果基函数是非参数化形式, 就引入了函数空间的优化.



将$F(X)$在每个$x$点处的值当作一个"参数",  优化目标为
$$
\Phi(F)=E_{y, x}L(y, F(X)) = E_x[E_y(L(y, F(X)))|X]
$$


等价于在每个$x$点处定义
$$
\phi(F(X))=E_y[L(y, F(X))|x]
$$
函数空间有无数个点, 但是我们的数据集只有有限个点.



类似于在参数空间的优化过程, 这里也将函数写成加法形式.
$$
F^*(X)=\sum_{m=1}^{M}f_m(x)
$$
同样的, 有$f_0(x)$是初始的猜测, $\{f_m(x)\}_1^M$是函数增量.



同样地用最速下降法, 有
$$
f_m(x)=-\rho_mg_m(x) \tag{GBM 6}
$$
同样地有
$$
F_{m-1}(x)=\sum_{i=0}^{m-1}f_i(x)
$$
这里导数为
$$
g_m(x)=\left[\frac{\partial\phi(F(x))}{\partial F(x)}\right]_{F(x)=F_{m-1}(x)}=\left[\frac{\partial E_y[L(y, F(X))|x]}{\partial F(x)}\right]_{F(x)=F_{m-1}(x)}\tag{GBM 7}
$$



#### 交换积分求导顺序

式(GBM 7)中涉及到对一个期望的偏导,  这应该是个棘手的事情. 

在GBM论文原文[^2]中说

> Assuming sufficient regularity that one can interchange differentiation and integration, this becomes

我这里的解释可能不太规范, **Assuming sufficient regularity**就是说:以面神的旨意, 你可以套大定理了. 👻



假设各种规律性都非常好, 接下来我们可以做积分求导交换顺序了. 我查了一下, 这个应该是叫[Leibniz integral rule, **莱布尼茨积分法则**](https://en.wikipedia.org/wiki/Leibniz_integral_rule)



期望的定义就是积分, 在概率空间上做积分.
$$
E[X] = \int_{\Omega}X dP
$$


(GBM 7)中是对一个期望做偏导, 在**sufficient regularity**的旨意下, 那就可以去交换求导积分的顺序, 得到

$$
g_m(x) = E_y\left[\frac{\partial L(y, F(x))}{\partial F(x)}|x\right]_{F(x)=F_{m-1}(x)}
$$


因此, 对照参数空间的优化过程, 这里的$\rho_m$也可以通过线性搜索得到.
$$
\rho_m = \arg \min_{\rho} E_{y,x}L(y, F_{m-1}(x) - \rho g_m(x)) \tag{GBM 8}
$$





### 数据有限的情况

上面在求解梯度的时候用到了期望的计算, 然而在实际上有限的数据集中, 对$E_y[\cdot|X]$是不准确的. 那该怎么办呢? 原文中说

> Strength must be borrowed from nearby data points by imposing smoothness on the solution. One way to do this is to assume a parameterized form such as (2) and do parameter optimization as discussed in Sec 1.1 to minimize the corresponding data based estimate of expected loss.

对我来说, 这段话的前半段有些玄乎, Borrowing strength是个啥感觉只可意会不可言传. 反正就是说, 既然解决不了上面那个问题, 那就带一些先验进去, 假设函数的形式是如(GBM 2)的参数形式. 然后用参数优化的方式最小化损失.



根据(GBM 2)的定义形式, 最优参数为
$$
 \{\beta_m, a_m\}_1^M= \arg \min_{\{\beta'_m, a'_m\}_1^M}\sum_{i=1}^L(y_i, \sum_{m=1}^M\beta'_mh(x_i;a'_m))
$$





在没有可行解的情况下, 可以使用**greedy-stagewise**去优化参数, 对$m=1, 2, \dots, M$
$$
(\beta_m, a_m)=\arg \min_{\beta, a}\sum_{i=1}^NL(y_i, F_{m-1}(x_i)+\beta h(x_i;a)) \tag{GBM 9}
$$


在求完每个**stage**的参数后, 更新函数形式.
$$
F_m(x) = F_{m-1}(x)+\beta_m h(x;a_m) \tag{GBM 10}
$$





但是有时候，对于特定的损失函数或是基学习器，(GBM 9) 式**很难求解.**



这时候需要换一个角度去看之前设置的(GBM 10)式,  类比于梯度下降法, (GBM 10)式可以看作是在当前位置$F_{m-1}(x)$沿着方向$h(x;a_m)$前进了$\beta_m$. 但是因为已经假定了$h(x)$的函数簇, 相当于是在限制了函数簇的有约束最速下降.



类似地, 基于数据的无约束下的梯度形式为
$$
-g_m(x_i)=-\left[\frac{\partial L(y_i, F(x_i))}{\partial F(x)}\right]_{F(x)=F_{m-1}(x)}
$$

在$F_{m-1}(x)$的N为数据空间中, 获得的$-g_m(x_i)=\{-g_m(x_i)\}_1^N$.  这里的梯度都是定义在数据点上的, 并不能推广到其他位置,  为了让这个信息能够**泛化**,  既然已经定义了$h(x)$的函数簇, 那就用$h(x)$去生成$h_m=\{h(x_i;a_m\}_1^N$, 尽可能平行于$-g_m$.(在数据点上尽可能接近,  这里还是在函数空间内优化)



**拟合梯度在这里出现了!!**, 因此有
$$
a_m = \arg\min_{a, \beta}\sum_{i=1}^N[-g_m(x_i)-\beta h(x_i;a)]^2 \tag{GBM 11}
$$


用有约束下的$h(x;a_m)$替换(GBM 8)式中的$g_m$, 可以得到
$$
\rho_m = \arg\min_{\rho}\sum_{i=1}^NL(y_i, F_{m-1}(x_i)+\rho h(x_i;a_m)) \tag{GBM 12}
$$



这一步完成后, 就可以进一步更新$F(x)$.
$$
F_m(x)=F_{m-1}(x) + \rho_mh(x;a_m)
$$



这里就讲完了, 为什么会去做拟合梯度这样一个事情.



由此导出了广义的最速下降求解方式

```
Algorithm: Gradient_Boost
```


$$
\begin{eqnarray}
&&F_0(x)=\arg\min_{\rho}\sum_{i=1}^NL(y_i, p) \\
&&For \quad  m =1 \, to \,M \, do:\\
&& \quad\quad\quad \widetilde{y}=-\left[\frac{\partial L}{\partial F(x_i)}\right] \\
&& \quad\quad\quad a_m = \arg \min_{a, \beta} \sum_{i=1}^{N}\left[\widetilde{y}_i-\beta h(x_i;a)\right]^2 \\
&& \quad\quad\quad \rho_m=\arg\min_\rho  \sum_{i=1}^{N}L\left(y_i, F_{m-1}(x_i)+\rho h(x_i;a_m)\right)\\
&& \quad\quad\quad F_m(x) = F_{m-1}(x) + \rho_m h(x;a_m)
\end{eqnarray}
$$





### 那拟合残差是什么

GBDT的方法里讲了梯度是怎么来的,  那拟合残差又是什么情况? 

对于回归树来说, 损失函数为
$$
L(y, F) = (y-F)^2/2
$$
$L$对$F$求偏导, 得到的就是$\widetilde{y}_i=y_i - F_{m-1}(x_i)$, 也就是残差.




<br>
### GBDT白话总结
在参数空间中的梯度优化很好理解, 那个累加的形式就是从起始点加上每一步的偏移量. 梯度下降的图这年头到处都是.

同样的类比, 在函数空间优化也是可以这样理解. 不严谨的说法是, 在函数空间中, 起始点是一个函数, 同样是梯度下降法, 这里的增量是函数.所以$F_m(x)=F_{m-1}(X) + h(x;a_m)$就是每次在当前的点, 偏移$h(x;a_m)$, 即函数空间的梯度下降. 



<br>
## XGBoost

XGBoost是在GBDT的基础上进行改进， 基学习器是CART.


<br>
### XGB的目标函数

XGBoost在损失函数中引入了正则项
$$
L(\phi)=\sum_il(\hat{y}_i, y_i)+\sum_k\Omega(f_k) \tag{XGB 2}
$$
这里k下标指代基学习器, 正则项定义为
$$
\Omega(f)=\gamma T+1/2\lambda ||w||^2
$$


T是叶子节点的数量, w是叶子节点的值. 由此对树模型进行一个约束.



### XGB目标函数的泰勒展开

在XGB中, 第$t$个基学习器的目标函数定义为
$$
L^{(t)}=\sum_{i=1}^nl(y_i, \hat{y}_i^{(t-1)}+f_t(x_i))+\Omega(f_t)
$$
由泰勒展式, 将损失函数展开到二阶, 可有
$$
L^{(t)}\simeq\sum_{i=1}^n[l(y_i, \hat{y}_i^{(t-1)})+g_if_t(x_i) + 1/2h_if^2_t(x_i)]+\Omega(f_t)
$$
移除常数项, 则在第$t$步的简化优化目标为
$$
L^{(t)}=\sum_{i=1}^n[g_if_t(x_i) + 1/2h_if^2_t(x_i)]+\Omega(f_t)
$$


定义符号$I_j=\{i|q(x_i)=j\}$表示样本属于叶子节点$j$的样本下标, 将上式展开为按叶子节点表示的方式
$$
\begin{aligned}
L^{(t)}&=\sum_{i=1}^n[g_if_t(x_i) + 1/2h_if^2_t(x_i)]+\Omega(f_t) \\
&=\sum_{i=1}^n[g_if_t(x_i) + 1/2h_if^2_t(x_i)] + \gamma T + 1/2\lambda \sum_{j=1}^Tw_j^2 \\
&= \sum_{j=1}^T\left[ (\sum_{i\in I_j}g_i)w_j+1/2(\sum_{i \in I_j}h_i+\lambda)w_j^2
\right]+\gamma T 
\end{aligned}
\tag{XGB 4}
$$
在式(XGB 4)中, 目标函数被写成了对叶结点求和的方式, 对于每个叶结点, 要最小化
$$
(\sum_{i\in I_j}g_i)w_j+1/2(\sum_{i \in I_j}h_i+\lambda)w_j^2
$$
这个式子是关于$w$的二次形式, 该函数有最小值点, 由此对于每个叶结点, 有最优的$w^*_j$为
$$
W^*_j=-\frac{\sum_{i \in I_j}g_i}{\sum_{i \in I_j}h_i+\lambda}
$$
带回(XGB 4), 得到最优的目标函数形式
$$
\widetilde{L}^{(t)}(q)=-1/2\frac{\sum_{i \in I_j}g_i}{\sum_{i \in I_j}h_i+\lambda}+\gamma T \tag{XGB 6}
$$


XGBoost中使用(XGB 6)式对树结构进行打分, 计算节点分裂后的分数增益, 用来确定最佳的节点分裂位置. 类似于决策树算法中的信息增益率.



### Shrinkage和列抽样



shrinkage在学得每个基学习器后, 将其乘以一个因子$\eta$后再加入集成中,  $\eta$也就是学习率的意思. 列抽样是随机森林中的概念,  随着学习器的数量增加, 随机森林可以收敛到更低的泛化误差.



### XGB中的节点分裂近似贪心算法

在决策树中对节点进行分裂时, 原始的贪心算法遍历每一个可能的值, 进行节点分裂, 计算得分.  但是当数据量太大, 或是在分布式计算的场景下, 数据无法全部放入内存进行贪心搜索. XGBoost设置了一个近似贪心搜索方式.



原始贪心遍历特征的每一个值,  近似算法将特征的所有取值进行排序, 然后按照数据的分位数(分位点, quantile)进行分割, 通俗地来说类似于将数据放入n个桶中.



### 分位数加权

在近似算法的设定基础上,  并不是直接按照特征的取值进行分位点划分, XGBoost中设置了使用样本点的二阶梯度信息进行加权, 用 $D_k={(x_{1k}, h_1),(x_{2k}, h_2),...,(x_{nk}, h_n)}$表示样本的第k个特征及其对于的二阶梯度, 使用下面的公式计算特征值小于z的样本在总体中的排位
$$
r(z)=\frac{1}{\sum_{(x, h)\in D_k}} \sum_{(x, h)\in D_k, x<z}h
$$

### 缺失值处理

在C4.5和CART算法中， 出现缺失值后将样本划分到每个子结点中， 同时调整它的权值.

在XGBoost中, 对每个特征会学到一个最优的划分方向, 在该特征上出现缺失值时, 就把样本划分到学到的最优方向上.



### 系统中的并行设计

预先对数据进行了排序，然后保存为 block结构，后面的迭代中重复地使用这个结构，大大减小计算量。block结构也使得可并行计算，在进行节点的分裂时，需要计算每个特征的增益，最终选增益最大的那个特征去做分裂，那么各个特征的增益计算就可以开多线程进行。







## LightGBM

XGBoost在GBDT的基础上改进了很多, LightGBM也是基于GBDT的方法, 目的也是为了加快训练的速度.



GBDT中查找最佳分裂点需要遍历特征的取值, XGBoost中对特征按照二阶梯度进行排序, 创建桶去降低特征的取值数量, 加快查找速度. LightGBM使用histogram-based方法, 将查找分裂点的时间复杂度从(#data $\times$ #feature)降低到(#bin $\times$ #feature).



LightGBM提出了两种方法, 分别用于降低训练时的样本数量和训练的特征数量.



### Gradient-based One-Side Sampling(GOSS)

AdaBoost方法中, 每个样本都有对应的权重, 但是在GBDT中没有, 不过GBDT中的样本梯度也可以表示样本的重要性.

GOSS方法保留梯度值大的样本, 同时对梯度值小的样本进行采样, 用来降低训练时样本的数量.



### Exclusive Feature Bundling(EFB)

EFB的设想是, 样本的特征是稀疏的,  通过对特征进行聚合, 可以将时间复杂度从(#data $\times$ #features) 降低到(#data $\times$ #bundle).



有些特征值不会同时为零, 那么这些特征便可以合并到一起.







## CatBoost

CatBoost为了更好的处理 GBDT 特征中的categorical features. 该库中的学习算法基于GPU实现，打分算法基于CPU实现。



在一般的特征工程中, 都会提前将categorical feature进行编码, 对于low-cardinality的特征, 可以直接用one-hot编码, 对于high-cardinality的特征, 可以用target-encoding编码处理.



CatBoost使用的是对称树, 自由度更小, 但是速度更快, 每个叶结点都可以被编码为一串二元数组, 可以快速进行打分.



在GBDT的模型训练阶段，同样会因为训练数据与测试数据分布不同的问题产生预测偏移(Prediction Shift)和残差偏移(Residual Shift)的问题。CatBoost采用了排序提升（Ordered Boosting）的方式, 首先对所有的数据进行随机排列, 然后在计算第 i 步残差时候的模型只利用了随机排列中前 i-1个样本。







[^1]: Classification and regression trees, http://pages.stat.wisc.edu/~loh/treeprogs/guide/wires11.pdf
[^2]: Greedy Function Approximation: A Gradient Boosting Machine,  https://statweb.stanford.edu/~jhf/ftp/trebst.pdf
[^3]:XGBoost: A Scalable Tree Boosting System, https://arxiv.org/abs/1603.02754
[^4]: LightGBM: A Highly Efficient Gradient Boosting Decision Tree,  https://papers.nips.cc/paper/6907-lightgbm-a-highly-efficient-gradient-boosting-decision-tree.pdf
[^5]: CatBoost: gradient boosting with categorical features support, http://learningsys.org/nips17/assets/papers/paper_11.pdf
[^6]: Introduction to Boosted Trees, https://homes.cs.washington.edu/~tqchen/pdf/BoostedTree.pdf