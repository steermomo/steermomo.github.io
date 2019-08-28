Title: 决策树, 回归树, CART决策树, bootstrap, bagging, boosting, adaboost, GBDT, XGboost
Date: 2019-08-26 18:10
Modified: 2019-08-26 18:10
Category: Machine Learning,
Tags: decision-tree, 
Slug: misc-about-decision-tree
Summary: 

虽然有跑过XGboost, 但是十分惭愧的是, 并不知道XGboost到底是怎么回事. 也只是在kaggle上fork别人的kernel, 然后修修改改. 做一个discussion miner.

决策树的概念还是比较清晰的, 对分类问题, 使用信息增益或者增益率去做划分选择.

对于回归树, 最开始我直观的疑问是, 一个树模型怎么能做回归呢? 树模型有限的输出并不能映射到无限的输出空间.

直接看了统计学习方法中关于CART算法的部分.
> 回归树是对应着输入空间(特征空间)的一个划分以及在划分的单元上的输出值.

假设回归树将输出空间划分为M个单元, 那么回归树在每个单元上都会有一个固定的输出值c. 也就是说, 回归树的输出值也是有限的, 而不是像线性回归模型那样, 训练完成后可以将$\R^m$的特征空间映射到实值域.

 
集成通过构建并结合多个模型, 可以获得比单一学习器显著优越的泛化性能, 对弱分类器尤其明显.

集成分为两大类:
- 个体学习器间存在强依赖关系, 需要串行生成的序列化方法
    -   如Boosting
- 个体学习器间不存在强依赖关系, 可同时生成的并行化方法
    -   如Bagging和随机森林



bootstrap sampling: 有放回采样相同大小的数据集.

Bagging: 使用bootstrap sampling采样m次, 可并行获得m个模型, 再将m个模型进行组合. 每个模型的权重相同.

Boosting: 改变训练样本的权重, 学习多个分类器, 并将分类器进行线性组合, 提高分类性能.

AdaBoost: 代表性的Boosting算法, 每一轮提高前一轮弱分类器分错样本的权值, 训练一系列分类器. 加大分类误差率小的弱分类器的权值, 使其在表决中起较大作用. 

AdaBoost的加法模型解释中, 每一步训练的分类器相当于在学习之前所有分类器的结果与目标的残差.


GBDT: 梯度提升方法, 利用损失函数的负梯度在当前模型的值, 作为回归问题中残差的近似值, 拟合回归树.
为什么这里可以说模型的负梯度是残差的近似值? [^1]

XGboost: 

机器学习算法中 GBDT 和 XGBOOST 的区别有哪些?[^2]



- https://homes.cs.washington.edu/~tqchen/pdf/BoostedTree.pdf

[^1]:[梯度提升树中为什么说目标函数关于当前模型的负梯度是残差的近似值?](https://www.zhihu.com/question/60625492)
[^2]:[机器学习算法中 GBDT 和 XGBOOST 的区别有哪些?](https://www.zhihu.com/question/41354392)
