Title: SIFT算法及Python实现
Date: 2019-06-28
Summary: 用Python实现了一遍SIFT算法

#### 空间极值检测

SIFT算法需要在尺度空间中寻找关键点.

首先需要对相同物体在不同尺度下进行定位, 因此使用特征金字塔完成这一目的.

对尺度空间的搜索得到的特征能够满足尺缩不变性.

##### 空间金字塔

###### 高斯核

实现尺缩变换的唯一变换核是高斯核.

对于输入图像$I(x,y )$, 使用高斯核$G(x, y, \sigma)$做卷积, 形式如下.
$$
L(x, y, \sigma)=G(x, y, \sigma) \ast I(x, y)
$$
通过使用不同的$\sigma$, 相当于对图像做不同程度的高斯模糊, 即得到不同尺度的图像.

###### 高斯差分近似归一化拉普拉斯

Mikolajczyk(2002) 发现尺度归一化的拉普拉斯高斯函数$\sigma^2\nabla^2G$的极大极小值, 相比于其他特征方法, 能够产生最稳定的图像特征.

同时, 为了有效地检测稳定关键点的位置, 本文作者(Lowe, 1999)使用差分高斯DOG的尺度空间极值作为特征.   差分高斯是相邻尺度的差值, 尺度差距有常数因子$k$决定.
$$
D(x, y, \sigma)=\left(G(x, y, k\sigma)-G(x, y, \sigma) \right)\ast I(x, y)\\
=L(x, y, k\sigma)-L(x, y, \sigma)
$$
而Lindeberg(1994)发现这两种方式是近似的, 通过对$G$对$\sigma$求偏导可得,
$$
\frac{\partial G}{\partial \sigma}=\sigma\nabla^2G
$$
用差分近似微分, 可得
$$
\sigma\nabla^2G=\frac{\partial G}{\partial \sigma}\simeq \frac{G(x, y, k\sigma)-G(x, y,\sigma)}{k\sigma-\sigma}
$$

变换分母位置可得
$$
G(x, y, k\sigma)-G(x, y, \sigma)\simeq(k-1)\sigma^2\nabla^2G
$$
当$k$趋向于1时, 误差趋向于0.

因此本文作者使用高斯差分代替归一化拉普拉斯函数进行检测.

###### 差分高斯的构造

下图表示了如何有效地构建差分拉普拉斯.

![](https://img-my.csdn.net/uploads/201204/28/1335626876_5968.jpg)

高斯金字塔有$n$层, 当高斯核的$\sigma$翻倍时, 将图像归为一组(Octave), 下一张图像将下采样一次.

初始的图像使用高斯核进行卷积, 令第一张图像的高斯核参数为$\sigma_0$, 后续每张图像的高斯核参数为$k\sigma_0$, $k$为图像索引(从1开始).

如果每组内有$s$张图像, 则有
$$
k^s=2
$$
因此$k=2^{1/s}$. 

为了在每组检测$s$个尺度的极值点(每个极值点需要跟上下层比较), 则DOG 需要$s+2$层, 高斯金字塔每组需要$s+3$层.

###### 高斯金字塔的生成过程

之前构造差分高斯金字塔需要先构造高斯金字塔.  

- 对于一幅输入图像, 首先构造高斯金字塔的第1组, 因为高斯金字塔每组需要$s+3$层, 令第一层的高斯核尺度为$\sigma_0$, 则依次使用$k^0\sigma, k\sigma, k^2\sigma, \cdots, k^s\sigma, k^{s+1}\sigma, k^{s+2}\sigma$的尺度, 生成对应尺度的图像. 其中$k=2^{1/s}$.
- 接着构造第2组的图像, 因为第2组的第1张图像的尺度$\sigma$应该是第1组的2倍, 因为$k^s=2$, 因此选择第1组的倒数第3张, 并下采样一次, 作为第2组的第1张图像.
- 依次构建接下来的各组, 直到打到组数要求或者下采样到指定大小.



##### 局部极值检测

得到差分高斯金字塔后, 需要检测极值点. 

如下图所示, 每个点需要与8个临界点进行比较, 如果该点是这9个点中最大或最小的点, 则作为极值点.

![](https://img-my.csdn.net/uploads/201204/28/1335626904_5751.jpg)

这种方法的一个问题是, 尺度的采样频率会影响到极值点的检测, 当然越小的采样间隔会得到越多的极值点. 如果要检测到所有的极值点, 需要无限小的采样间隔(极值点间的距离可能十分小). 

无限小的采样间距是不实际的, 这里需要在检测效果和采样频率之间做平衡.

###### 尺度采样频率

对于高斯金字塔, 已经明确了, 相邻组间的尺度差距是2倍, 但是组内的图片数量并没有确定.

论文通过实验确定组内的图片数量, 通过比较$s=1,2,3,\cdots,8$ 的结果, 结果显示检测效果在$s=3$时达到最佳, 随后会略微下降. 

虽然更大的$s$会检测出更多的极值点, 但这些点可能会不稳定, 因此导致了检测效果的下降.

###### 空间采样频率

高斯金字塔中另一个未确定的参数是第1张图像的尺度$\sigma_0$,  通过类似的实验, 选择$\sigma_0$为1.6.

但是这样相当于直接丢掉了最高空域的采样率.  原始图像的$\sigma_{-1}$为0.5,  对其使用双线性插值将尺寸扩大一倍, 相当于$\sigma_{-1}=1.0$, 通过扩大原始图片尺寸的方式生成第-1组.

将尺寸扩大一倍, 可使得关键点的数量变为原来的4倍. 但是扩大更大的倍数不再能显著增加关键点的数量.



#### 关键点精确定位

局部极值检测中, 是对离散值的检测. 下一步需要做定位, 确定尺度和主曲率, 用于剔除低对比度(噪声敏感)或者是不稳定边缘响应.

##### 泰勒展开拟合

(Brown and Lowe, 2002) 提出了3D二次函数对极值点位置进行插值, 实验表明这种方法提升了匹配效果和稳定性.

使用DOG函数在尺度空间的泰勒展开式, 令样本点为原点, 有
$$
D(x)=D+\frac{\partial D^T}{\partial x}X + \frac{1}{2}X^T\frac{\partial^2D}{\partial x^2}X
$$
其中$X=(x, y, \sigma)^T$是离样本点的偏移. 将上式对X求偏导, 令结果为0, 可得极值点的位置偏移量.
$$
\hat{X}=-\frac{\partial^2D^{-1}}{\partial X^2}\frac{\partial D}{\partial X}
$$
如果$\hat{X}$大于0.5, 则极值点偏移到临近点上, 需要改变样本点的位置, 并在新的位置上重复这一计算, 直到收敛. 当超过迭代次数或超出图像范围时, 需要删除该点.

##### 消除低对比度点

对于上一步中求得的$\hat{X}$, 带入原式可得
$$
D(\hat{X})=D+\frac{1}{2}\frac{\partial D^T}{\partial X} \hat{X}
$$
为了消除低对比度的点, 文中剔除了$|D(\hat{X}|$小于0.03的点.

##### 消除边缘响应

为了稳定性, 只剔除低对比度点是不够的. DOG算子对边缘有较强的响应, 即使该边缘并不显著.

有些极值点的位置是在图像的边缘位置的，因为图像的边缘点很难定位，同时也容易受到噪声的干扰.

 物体边缘位置的一个方向的主曲率会比较高, 而良好的边缘(比如泡泡), 两个方向的曲率都比较高. 



论文中使用海森矩阵对曲率进行判断.对于二维图像的某点的hessian矩阵，其最大特征值和其对应的特征向量对应其邻域二维曲线最大曲率的强度和方向，即山坡陡的那面；最小特征值对应的特征向量对应与其垂直的方向，即平缓的方向。
$$
H=\left[\begin{array}{2}D_{xx} & D_{xy} \\ D_{xy} & D_{yy} \end{array}\right]
$$
令$\alpha$和$\beta$分别为$H$的最大最小特征值, 即x和y方向的梯度, 则
$$
Tr(H)=\alpha + \beta \\
Det(H)=\alpha\beta
$$
令$\alpha=r\beta$, 则
$$
\frac{Tr(H)^2}{Det(H)}=\frac{(\alpha+\beta)^2}{\alpha\beta}=\frac{(r+1)^2}{r}
$$
上式越大, 说明一个方向的梯度越大, 另一个方向的梯度越小, 对于这样的点需要进行剔除. 

在文中, 取阈值$r=10$. 

#### 方向匹配

为使得提取的特征对旋转具有不变性, 需要为每个关键点分配一个基准方向. 

该方向是根据关键点的局部特征计算出来的. 

对于关键的邻域, 使用如下方法计算每个点的梯度模值和方向.
$$
m(x,y) =\sqrt{(L(x+1,y)-L(x-1, y))^2 + (L(x, y+1)-L(x, y-1))^2}\\
\theta(x,y)=\tan^{-1}\frac{L(x, y+1)-L(x, y-1)}{L(x+1, y)-L(x-1, y)}
$$
其中邻域大小为$r=3\times1.5\sigma_c$, $\sigma_c$为当前层的图像尺度.



计算后, 需要先对模值进行加权, 权值为$\sigma_m=1.5\sigma_c$的高斯函数,

对加权后的模值, 使用直方图统计邻域内的像素梯度和方向. 直方图将360度分为36个bin, 每个bin的值为该方向加权后模值的和.

取直方图最高柱作为该关键点的主方向, 满足最高值的80%作为辅助方向.

#### 关键点特征描述

上一步获取了SIFT关键点, 及其尺度和方向. 接下来为每个关键点建立描述符. 用一组向量描述关键点.



- 将关键点的邻域划分为$d\times d$个区域, 文章中取$d=4$. 计算8个方向的梯度信息, 共$4\times 4\times 8=128$维.
  - 每个区域的边长为$\sigma_c$, 实际计算时使用双线性插值, 取边长为$3\sigma_c\times(d+1)$.
  - 为了保证关键点的方向不变性,需要对特征点邻域进行旋转, 旋转角度为特征点角度. 为使得旋转区域包含正方形, 实际上得边长为$\frac{3\sigma_c(d+1)\sqrt2}{2}$.

- 然后需要将关键点及其邻域的坐标轴(x)旋转到关键点的主方向
  - 旋转后的采样点坐标为$$\left(\begin{array}{1}x' \\ y'\end{array}\right)=\left(\begin{array}{2} \cos\theta & -\sin\theta \\\sin\theta & \cos\theta \end{array}\right)$$
- 将邻域分配到对于的子区域内
  - 计算梯度值和角度, 生成直方图
  - 类似方向匹配, 也需要模值的加权
    - 第一次加权, 根据像素点与关键点的距离, 使用$\sigma=\frac{d^2}{2}$的高斯核加权
    - 第二次加权, 根据像素点与子区域中心的距离, 使用高斯加权
  - 将加权后的模值分配到8个方向上, 获取直方图
- 对直方图进行归一化处理
  - 消除均匀光照的影响
- 使用阈值(0.2)对归一化后的直方图,设定上限
  - 消除非均匀光照的影响



### 代码实现

```python
# -*- coding: utf-8 -*-
r'''
File: c:\Users\lomom\Documents\DL2019\Assignment\code\sift.py
Project: c:\Users\lomom\Documents\DL2019\Assignment\code
Created Date: Monday June 24th 2019
Author: Hang Li (hangli@stu.xmu.edu.cn)
-----
Last Modified: Monday, 24th June 2019 2:56:06 pm
Modified By:  Hang Li (hangli@stu.xmu.edu.cn)
-----
Copyright (c) 2019 Wormhole
'''

from scipy import ndimage as ndi 
import scipy 
from scipy.ndimage import filters
import numpy as np 
from os import path
from copy import deepcopy
from multiprocessing.pool import ThreadPool, Pool
from itertools import repeat
from typing import List, Tuple
from PIL import Image, ImageDraw
from skimage import transform, io, color
import cv2 # 用于对比结果


class ScaleSpace:
    """图像金字塔类
    """
    def __init__(self, n_oct:int, n_spo:int, img_w:int, img_h:int, sigma_min:int, delta_min=0.5):
        """[summary]
        
        :param n_oct: 图像金字塔层数
        :type n_oct: int
        :param n_spo: 图像金字塔每层的图像数(指最终每层的极值点层数)
        :type n_spo: int
        :param img_w: 图像宽度
        :type img_w: int
        :param img_h: 图像高度
        :type img_h: int
        :param sigma_min: 最低层的sigma
        :type sigma_min: int
        :param delta_min: 最底层(放大2倍的)图像的像素间距(相对于输入图像), defaults to 0.5
        :type delta_min: float, optional
        """
        self.n_oct = n_oct
        self.n_spo = n_spo
        self.n_sca = n_spo + 3
        self.img_w = img_w
        self.img_h = img_h
        self.sigma_min = sigma_min

        self.ws = []
        self.hs = []
        self.deltas = [delta_min]
        self.ws.append(img_w * 2)
        self.hs.append(img_h * 2)
        
        #记录每层的长宽， 以及像素间距， 用于定位特征在原图的位置
        for o_idx in range(1, n_oct):
            self.ws.append(self.ws[-1] // 2)
            self.hs.append(self.hs[-1] // 2)
            self.deltas.append(self.deltas[-1] * 2)

        # 计算每层的sigma
        self.sigmas = np.zeros((n_oct, self.n_sca))
        for o_idx in range(n_oct):
            for s_idx in range(self.n_sca):
                self.sigmas[o_idx, s_idx] = sigma_min * 2 **(o_idx + s_idx /(self.n_sca))

        # 创建金字塔存储空间
        self.octave = []
        for o_idx in range(n_oct):
            current_layer = np.zeros((self.n_sca, self.hs[o_idx], self.ws[o_idx]))
            self.octave.append(current_layer)


        
    def add_img_to_octave(self, img: np.ndarray, oct_idx: int, s_idx:int, ):
        """向图像金字塔中加入图片
        
        :param oct_idx: 层索引
        :type oct_idx: int
        :param s_idx: 层内索引
        :type s_idx: int
        :param img: 加入的图像
        :type img: np.ndarray
        """
        self.octave[oct_idx][s_idx, :, :] = img
    
    def get_prev_octave_img(self, current_oct: int):
        """获取上一层的倒数第三张图像, 用于计算下一层
        
        :param current_oct: 当前层索引
        :type current_oct: int
        :return: [description]
        :rtype: [type]
        """
        ret = self.octave[current_oct - 1][-3, :, :]
        return ret
        
    def get_sigma(self, o_idx, s_idx):
        return self.sigmas[o_idx, s_idx]

    def get_current_octave(self, o_idx):
        return self.octave[o_idx]


class DogSpace:
    """差分高斯金字塔
    """
    def __init__(self, gauss_spcae: ScaleSpace):
        """从高斯金字塔构建差分高斯金字塔的结构
        
        :param gauss_spcae: 高斯金字塔对象
        :type gauss_spcae: ScaleSpace
        """
        self.n_oct = gauss_spcae.n_oct
        self.n_sca = gauss_spcae.n_sca - 1
        self.hs = deepcopy(gauss_spcae.hs)
        self.ws = deepcopy(gauss_spcae.ws)
        self.deltas = deepcopy(gauss_spcae.deltas)
        self.octave = [np.zeros((self.n_sca, h, w)) for h, w in zip(self.hs, self.ws)]
        
        self.sigmas = np.zeros((self.n_oct, self.n_sca))
        for o_idx in range(self.n_oct):
            current_layer = np.zeros((self.n_sca, gauss_spcae.hs[o_idx], gauss_spcae.ws[o_idx]))
            for s_idx in range(self.n_sca):
                self.sigmas[o_idx, s_idx] = gauss_spcae.get_sigma(o_idx, s_idx)
        
    def set_current_layer(self, layer: np.ndarray,  o_idx:int):
        self.octave[o_idx][:, :, :] = layer

class KeyPoint:
    """关键点
    """
    def __init__(self, o, s, h, w, x, y, sigma, value):
        """        
        :param o: 层索引
        :param s: 层内索引
        :param h: 尺度空间行索引
        :type h: [type]
        :param w: 尺度空间列索引
        :param x: 关键点在原图中的x
        :param y: 关键点在原图中的y
        :param sigma: 关键点所在尺度的sigma
        :param value: 关键点的值
        """
        self.o = o
        self.s = s
        self.h = h
        self.w = w
        self.x = x
        self.y = y
        self.sigma = sigma
        self.value = value
    
    def init_hist(self, n_bins):
        # self.hist = [0 for _ in range(n_bins)]
        self.hist = np.zeros(n_bins)
        self.theta = 0

    def init_descr(self, n_descr):
        self.descr = np.zeros(n_descr)
        

def imread(img_path: str):
    """读取图片, 如果是彩色图像将其转为灰度图
    
    :param img_path: 图片路径
    :type img_path: str
    :raises ValueError: [description]
    :return: [description]
    :rtype: [type]
    """
    if not path.exists(img_path):
        raise ValueError(f'image path not exist:{img_path}')
    # img = ndi.imread(img_path)
    img = io.imread(img_path)
    if len(img.shape) == 3:
        # 将彩色图像转为灰度图像
        img = np.dot(img[...,:3], [0.2989, 0.5870, 0.1140])

    img = img / 255.
    return img

def subsample_by2(img_in: np.ndarray):
    """对图像下采样， 根据论文中的描述-every second pixel in each row and column
    这里选取从第二个像素开始
    
    :param img_in: 待下采样图像
    :type img_in: np.ndarray
    :return: 下采样后的图像
    :rtype: [type]
    """
    ret = img_in[1::2, 1::2]
    return ret

#-------------- 特征金字塔-------------
def gaussian_scale_space(img: np.ndarray, sigma_in=0.5, sigma_min=0.8, n_oct=8, n_spo=3):
    """构建高斯金字塔
    
    :param img: 输入图像
    :type img: np.ndarray
    :param sigma_in: 输入图像的sigma, defaults to 0.5
    :type sigma_in: float, optional
    :param sigma_min: 最底层图像的sigma, defaults to 0.8
    :type sigma_min: float, optional
    :param n_oct: 金字塔层数, defaults to 8
    :type n_oct: int, optional
    :param n_spo: 金字塔每层的图像数, defaults to 3
    :type n_spo: int, optional
    :return: [description]
    :rtype: [type]
    """
    delta_min = 0.5
    h, w = img.shape
    g_scale = ScaleSpace(n_oct=n_oct, n_spo=n_spo, img_w=w, img_h=h, sigma_min=sigma_min)
    # k = 2 ** (1 / (n_spo + 3))
    nSca = n_spo + 3
    sigmas = np.zeros((n_oct, nSca))
    
    for o in range(n_oct):
        for s in range(nSca):
            sigmas[o,s] = sigma_min * 2 **(o + s /(nSca))
    
    for oct_idx in range(n_oct):# 构建每一层
       
        if oct_idx == 0: # 构建第一层
            sigma_extra = np.sqrt(sigma_in**2 - sigma_in**2) / delta_min 
            image_shape = img.shape   
            resize_shape = [x * 2 for x in image_shape]
            # 尺寸扩大2倍
            # seed_image = scipy.misc.imresize(img, resize_shape, interp='bilinear')
            #0: Nearest-neighbor
            #1: Bi-linear (default)
            #2: Bi-quadratic
            #3: Bi-cubic
            #4: Bi-quartic
            #5: Bi-quintic
            seed_image = transform.resize(img, resize_shape, order=1)
            image_add_blur = filters.gaussian_filter(seed_image, sigma=sigma_extra)
            current_image = image_add_blur
        else: # 构建其余层的第一张
            img_prev = g_scale.get_prev_octave_img(oct_idx)
            current_image = subsample_by2(img_prev)
            
        # 添加每层的第一张图像
        g_scale.add_img_to_octave(img=current_image, oct_idx=oct_idx, s_idx=0)
        
        prev_img = current_image
        for s_idx in range(1, nSca): # 构建每一层的剩余图像
            prev_sigma = g_scale.get_sigma(oct_idx, s_idx-1)
            next_sigma = g_scale.get_sigma(oct_idx, s_idx)

            sigma_extra = np.sqrt(next_sigma**2 - prev_sigma**2)
            
            current_image = filters.gaussian_filter(prev_img, sigma=sigma_extra)
            g_scale.add_img_to_octave(current_image, oct_idx=oct_idx, s_idx=s_idx)
            prev_img = current_image
    return g_scale

#-------------- 差分高斯金字塔-------------
def scale_space_dog(g_scale_space: ScaleSpace):
    """从高斯金字塔构建差分高斯金字塔
    
    :param g_scale_space: 高斯金字塔对象
    :type g_scale_space: ScaleSpace
    :return: 差分高斯金字塔
    :rtype: [type]
    """
    # 从高斯金字塔对象构建差分高斯金字塔
    d_space = DogSpace(g_scale_space)
    for o_idx in range(g_scale_space.n_oct):
        c_octave = g_scale_space.get_current_octave(o_idx)
        dif = np.diff(c_octave, axis=0) # 计算差分
        d_space.set_current_layer(dif, o_idx)
    
    return d_space

#-------------- 差分高斯金字塔 空间极值-------------
def is_local_maxmin(c_octave: np.array, loc, nei_offset,):
    """查找3D数组中的局部极大极小值
    
    :param c_octave: 3D数组
    :type c_octave: np.array
    :param loc: 当前查找位置
    :type loc: [type]
    :param nei_offset: 相邻像素点的偏移量
    :type nei_offset: [type]
    :return: 是否为极大极小值
    :rtype: bool
    """
    s_idx,h_idx,w_idx = loc
    center_value = c_octave[s_idx,h_idx,w_idx] # 当前值
    is_local_min = True
    # 查找是否为极小值
    for each_offset in nei_offset:
        if c_octave[
            s_idx+each_offset[0], h_idx+each_offset[1], w_idx+each_offset[2]
            ] <= center_value:
            is_local_min = False
            break
    # 查找是否为极大值
    is_local_max = True
    if is_local_min:
        is_local_max = False
    else:
        for each_offset in nei_offset:
            if c_octave[
                s_idx+each_offset[0], h_idx+each_offset[1], w_idx+each_offset[2]
                ] >= center_value:
                is_local_max = False
                break
    return is_local_max or is_local_min

def keypoints_find_3d_discrete_extrema(dog_space: DogSpace):
    """从差分高斯金字塔中查找关键点
    
    :param dog_space: 高斯金字塔对象
    :type dog_space: DogSpace
    :return: 关键点
    :rtype: [type]
    """
    n_oct = dog_space.n_oct
    n_sca = dog_space.n_sca
    # 创建偏移数组， 方便下一步计算
    nei_offset = []
    for s_idx in range(-1, 1+1):
        for h_idx in range(-1, 1+1):
            for w_idx in range(-1, 1+1):
                if s_idx != 0 or h_idx !=0 or w_idx != 0:
                    nei_offset.append((s_idx, h_idx, w_idx))

    key_points = []
    for o_idx in range(n_oct): # 遍历金字塔的每一层
        w, h = dog_space.ws[o_idx], dog_space.hs[o_idx]
        delta = dog_space.deltas[o_idx]
        c_octave = dog_space.octave[o_idx]
        locs = []
        for s_idx in range(1, n_sca-1):
            for h_idx in range(1, h-1):
                for w_idx in range(1, w-1):
                    locs.append((s_idx,h_idx,w_idx))
        # 使用进程池计算
        with Pool(16) as tp:
        # with ThreadPool(16) as tp:
            ret_flag = tp.starmap(is_local_maxmin, zip(repeat(c_octave), locs, repeat(nei_offset)))
        for loc, flag in zip(locs, ret_flag):
            if flag:
                s_idx, h_idx, w_idx = loc
                key_p = KeyPoint( o_idx, s_idx, h_idx, w_idx,
                    delta * h_idx, delta * w_idx,
                    dog_space.sigmas[o_idx],
                    c_octave[s_idx, h_idx, w_idx])
                key_points.append(key_p)
    return key_points
        

#-------------- 差分高斯金字塔 空间极值 精确定位-------------
def keypoints_discard_with_low_response(keys: list, thresh: float):
    """移除低对比度的点
    
    :param keys: 关键点列表
    :type keys: list
    :param thresh: 阈值
    :type thresh: float
    :return: 处理后的关键点列表
    :rtype: list
    """
    ret = []
    for each_key in keys:
        if each_key.value > thresh:
            ret.append(each_key)
    return ret


def inverse_3D_Taylor(octave:np.ndarray, s, i, j):
    """泰勒展开拟合,求解(s,i,j)位置附近极值点的偏移量
    计算过程由泰勒展开对X求导并令其为0,获得偏移量
    需要计算一阶导数, 二阶导数及二阶导数的逆
    使用有限差分法求导的方式计算该导数
    有限差分法参考https://blog.csdn.net/zddblog/article/details/7521424 4.3有限差分法求导
    
    :param octave: 差分高斯金字塔的一层
    :type octave: np.ndarray
    :param s: 层内索引
    :type s: [type]
    :param i: 层内行索引
    :type i: [type]
    :param j: 层内列索引
    :type j: [type]
    """
    # 在差分近似中， 分母包含h， 因为这里h=1，所以直接省略
    # 计算一阶偏导
    gx = 0.5 * (octave[s, i+1, j] - octave[s, i-1, j])
    gy = 0.5 * (octave[s, i, j+1] - octave[s, i, j - 1])
    gs = 0.5 * (octave[s+1, i, j] - octave[s-1, i, j])

    # 计算二阶偏导
    hxx = octave[s, i-1, j] + octave[s, i+1, j] - 2 * octave[s, i, j]
    hyy = octave[s, i, j-1] + octave[s, i, j+1] - 2 * octave[s, i, j]
    hss = octave[s-1, i, j] + octave[s+1, i, j] - 2 * octave[s, i, j]

    hxy = 0.25 * (octave[s, i+1, j+1] + octave[s, i-1, j-1] - octave[s, i+1, j-1] - octave[s, i-1, j+1])
    hxs = 0.25 * (octave[s+1, i+1, j] + octave[s-1, i-1, j] - octave[s+1, i-1, j] - octave[s-1, i+1, j])
    hys = 0.25 * (octave[s+1, i, j+1] + octave[s-1, i, j-1] - octave[s+1, i, j-1] - octave[s-1, i, j+1])


    # 对二阶矩阵求逆
    # 海森矩阵的形式如下(只写分母)
    # | xx xy xs |
    # | yx yy ys |
    # | sx sy ss |
    det = hxx*hyy*hss - hxx*hys*hys - hxy*hxy*hss + 2 * hxy*hxs*hys - hxs*hxs*hyy
    # if det == 0:
    #     return 5., 5., 5., 1
    aa = (hyy*hss - hys*hys) / det
    ab = (hxs*hys - hxy*hss) / det
    ac = (hxy*hys - hxs*hyy) / det
    bb = (hxx*hss - hxs*hxs) / det
    bc = (hxy*hxs - hxx*hys) / det
    cc = (hxx*hyy - hxy*hxy) / det

    # 偏移量
    # 根据解出的公式，偏移量为3*3的逆矩阵乘以3*1的一阶偏导列向量
    # 拆解矩阵相乘运算
    ofst_x = -(aa * gx + ab * gy + ac * gs)
    ofst_y = -(ab * gx + bb * gy + bc * gs)
    ofst_s = -(ac * gx + bc * gy + cc * gs)

    # 插值后的极值的偏移量
    ofst_val = 0.5 * (gx * ofst_x + gy * ofst_y + gs * ofst_s)

    val = octave[s, i, j] + ofst_val
    
    return ofst_s, ofst_x, ofst_y, val


def keypoints_interpolate_position(dog_space: DogSpace, keys: List[KeyPoint], iter_max:int):
    """对关键点位置进行插值，获取更精确的位置
    
    :param dog_space: 差分高斯金字塔
    :type dog_space: DogSpace
    :param keys: 关键点列表
    :type keys: List[KeyPoint]
    :param iter_max: 最大迭代次数
    :type iter_max: int
    :return: 筛选后的关键点
    :rtype: [type]
    """
    max_inter = iter_max # 最大插值次数
    ofst_max = 0.6
    ret = []
    sigma_ratio = dog_space.sigmas[0, 1] / dog_space.sigmas[0, 0]
    for key in keys: # 迭代所有的关键点
        o,s,i,j = key.o, key.s, key.h, key.w

        octave = dog_space.octave[o]
        w = dog_space.ws[o]
        h = dog_space.hs[o]
        ns = dog_space.n_sca
        delta = dog_space.deltas[o]
        val = key.value

        # 开始插值
        c_i, c_j, c_s = i, j, s
        n_intrp = 0
        is_conv = False

        ofst_x, ofst_y, ofst_s = 0, 0, 0

        while n_intrp < max_inter:
            if 0 < c_i < (h-1) and 0 < c_j < (w-1):
                ofst_s, ofst_y, ofst_s, val = inverse_3D_Taylor(octave, c_s, c_i, c_j)
            else:
                is_conv = False
                ofst_x=5.0
                ofst_y=5.0
                ofst_s=5.0
            
            if abs(ofst_x) < ofst_max and abs(ofst_y) < ofst_max and abs(ofst_s) < ofst_max:
                is_conv = True
                break
            else:
                if (ofst_x > ofst_max) and ((c_i + 1) < (h - 1)):
                    c_i += 1
                if (ofst_x < -ofst_max) and ((c_i - 1) > 0):
                    c_i -= 1
                if (ofst_y > ofst_max) and ((c_j + 1) < (w - 1)):
                    c_j += 1
                if (ofst_y < -ofst_max) and ((c_j - 1) > 0):
                    c_j -= 1

                if (ofst_s > ofst_max) and ((c_s + 1) < (ns - 1)):
                    c_s += 1
                if (ofst_s < -ofst_max) and ((c_s-1) > 0):
                    c_s -= 1

            n_intrp += 1

        if is_conv:
            if dog_space.sigmas[o, c_s] * sigma_ratio**ofst_s == 0:
                print('sigma is zero')
            k = KeyPoint(
                o=o, s=c_s, h=c_i, w=c_j, 
                x=(c_i+ofst_x)*delta, y=(c_j+ofst_max)*delta,
                sigma=dog_space.sigmas[o, c_s] * sigma_ratio**ofst_s,
                value=val
                )
            ret.append(k)
    return ret


def keypoints_edge_response(dog_sp: DogSpace, keys: List[KeyPoint]):
    """计算关键点的边缘响应
    
    :param dog_sp: 差分高斯金字塔
    :type dog_sp: DogSpace
    :param keys: 关键点列表
    :type keys: List[KeyPoint]
    """
    for key in keys:
        o, s, i, j = key.o, key.s, key.h, key.w
        c_img = dog_sp.octave[o][s, :, :]
        w, h = dog_sp.ws[o], dog_sp.hs[o]

        # 计算二阶海森矩阵
        hxx = c_img[i+1, j] + c_img[i-1, j] - 2*c_img[i, j]
        hyy = c_img[i, j+1] + c_img[i, j-1] - 2*c_img[i, j]
        hxy = 0.25 * (c_img[i+1, j+1] + c_img[i-1, j-1] - c_img[i-1, j+1] - c_img[i+1, j-1])

        edge_response = (hxx + hyy) ** 2 / (hxx*hyy - hxy**2)
        key.edge_resp =  edge_response


def keypoints_discard_with_edge_resp(keys: List[KeyPoint], thresh: float):
    """根据关键点的边缘响应剔除响应较弱的点
    
    :param keys: 关键点列表
    :type keys: List[KeyPoint]
    :param thresh: 响应阈值
    :type thresh: float
    """
    ret = []
    for key in keys:
        if key.edge_resp <= thresh:
            ret.append(deepcopy(key))
    return ret




#--------------方向匹配-------------
def compute_gradient(im: np.ndarray, w, h):
    dx = np.zeros((h, w))
    dy = np.zeros((h, w))

    # 计算dy
    for i in range(h):
        for j in range(1, w - 1):
            dy[i, j] = (im[i, j+1] - im[i, j-1]) * 0.5
        # 处理边界
        dy[i, 0] = im[i, 1] - im[i, 0]
        dy[i, w-1] = im[i, w-1] - im[i, w-2]

    # 计算dx
    for i in range(1, h-1):
        for j in range(w):
            dx[i, j] = (im[i+1, j] - im[i-1, j]) * 0.5
        
    for j in range(w):
        dx[0, j] = im[1, j] - im[0, j]
        dx[h-1, j] = im[h-1, j] - im[h-2, j]
    
    return dx, dy

def scale_compute_gradient(g_scale_space: ScaleSpace, dx_space: ScaleSpace, dy_space: ScaleSpace):
    """预先计算两个方向的差分， 避免在后续计算中重复计算差分
    
    :param g_scale_space: 高斯金字塔
    :type g_scale_space: ScaleSpace
    :param dx_space: x方向差分金字塔
    :type dx_space: ScaleSpace
    :param dy_space: y方向差分金字塔
    :type dy_space: ScaleSpace
    """
    n_oct = g_scale_space.n_oct
    n_sca = g_scale_space.n_sca
    for o in range(n_oct):
        w, h = g_scale_space.ws[o], g_scale_space.hs[o]
        for s in range(n_sca):
            im = g_scale_space.octave[o][s,:,:]
            dx, dy = compute_gradient(im, w, h)
            dx_space.octave[o][s, :, :] = dx
            dy_space.octave[o][s, :, :] = dy

def accumulate_orientation_hist(x, y, sigma, im_dx: np.ndarray, im_dy:np.ndarray, n_bins, lambda_ori:float, key: KeyPoint):
    """计算关键点的方向直方图
    
    :param x: 当前尺度的x
    :type x: [type]
    :param y: 当前尺度的y
    :type y: [type]
    :param sigma: 原图尺度的sigma
    :type sigma: [type]
    :param im_dx: x方向的差分图像
    :type im_dx: np.ndarray
    :param im_dy: y方向的差分图像
    :type im_dy: np.ndarray
    :param n_bins: 方向直方图的bins数量
    :type n_bins: [type]
    :param lambda_ori: 用于计算取样区域大小的系数
    :type lambda_ori: float
    :param key: 关键点
    :type key: KeyPoint
    """
    h, w = im_dx.shape
    R = 3 * lambda_ori * sigma # 计算取样半径

    # 计算取样区域
    si_min = max(0, int(x-R + 0.5))
    sj_min = max(0, int(y-R + 0.5))

    si_max = min(int(x+R+0.5), h-1)
    sj_max = min(int(y+R+0.5), w-1)

    for si in range(si_min, si_max+1):
        for sj in range(sj_min, sj_max+1):
            sx = (si - x) / sigma
            sy = (sj - y) / sigma

            dx = im_dx[si, sj]
            dy = im_dy[si, sj]

            # 计算角度
            ori = np.arctan2(dy, dx) % (2 * np.pi)

            # 计算加权权值
            r2 = sx ** 2 + sy ** 2
            weight = np.hypot(dx, dy) * np.exp(-r2 / (2*lambda_ori*lambda_ori))
            bin_idx = int(ori / (2 * np.pi) * n_bins + 0.5) % n_bins

            key.hist[bin_idx] += weight
    
    # max_hist_idx = np.argmax(key.hist)

    # # 对梯度方向直方图进行插值， 获取更精确的方向
    # idx_prev = (max_hist_idx - 1 + n_bins) % n_bins
    # idx_next = (max_hist_idx + 1) % n_bins

    # h1 = key.hist[idx_prev]
    # h2 = key.hist[max_hist_idx]
    # h3 = key.hist[idx_next]
    # offset = (h3 - h1) / (2 * (h1 + h3 - 2*h2))

    # # 计算插值后的角度， 保存到关键点中
    # new_ori = (max_hist_idx + 0.5 + offset) * (2 * np.pi / n_bins)
    
    # new_ori = new_ori - 2*np.pi if new_ori > 2*np.pi else new_ori # 处理越界情况
    # key.theta = new_ori

def smooth_hist(hist: np.ndarray, n_inter):
    """对角度直方图进行平滑
    
    :param hist: 直方图
    :type hist: np.ndarray
    :param n_inter: 平滑次数
    :type n_inter: [type]
    :return: 平滑后的直方图
    :rtype: [type]
    """
    bins = len(hist)
    
    for _ in range(n_inter):
        tmp = hist.copy()
        for i in range(bins):
            i_prev = (i-1+bins) % bins
            i_next = (i+1) % bins
            hist[i] = (tmp[i_prev]+tmp[i]+tmp[i_next])/3.
    return hist

def interp_peak(h1, h2, h3):
    """对直方图方向进行插值
    
    :param h1: [description]
    :type h1: [type]
    :param h2: [description]
    :type h2: [type]
    :param h3: [description]
    :type h3: [type]
    :return: [description]
    :rtype: [type]
    """
    offset = (h3 - h1) / (2 * (h1 + h3 - 2*h2))
    return offset

def extract_principal_ori(hist: np.ndarray, thresh):
    """从直方图中提取主要方向和辅助方向
    
    :param hist: 角度直方图
    :type hist: np.ndarray
    :param thresh: 辅助方向的阈值:0~1
    :type thresh: [type]
    :return: 提取后的方向
    :rtype: [type]
    """
    principal_ori = []
    n_bins = len(hist)
    smoothed_hist = smooth_hist(hist, 6)

    max_val = np.max(smoothed_hist)

    for i in range(n_bins):
        i_prev = (i-1+n_bins) % n_bins
        i_next = (i+1) % n_bins
        if (smoothed_hist[i] > thresh * max_val) and (smoothed_hist[i] > smoothed_hist[i_prev]) and (smoothed_hist[i] > smoothed_hist[i_next]):
            # is peak
            # 插值
            offset = interp_peak(smoothed_hist[i_prev], smoothed_hist[i], smoothed_hist[i_next])
            # 计算插值后的角度， 保存到关键点中
            new_ori = (i + 0.5 + offset) * (2*np.pi / n_bins)
            new_ori = new_ori - 2*np.pi if new_ori > 2*np.pi else new_ori # 处理越界情况
            principal_ori.append(new_ori)
    return principal_ori


def keypoints_attribute_orientations(sx: ScaleSpace, sy: ScaleSpace, keys: List[KeyPoint], n_bins=36, lambda_ori=3, t=0.8):
    """提取关键点主方向信息
    
    :param sx: x方向差分高斯金字塔
    :type sx: ScaleSpace
    :param sy: y方向差分高斯金字塔
    :type sy: ScaleSpace
    :param keys: 关键点列表
    :type keys: List[KeyPoint]
    :param n_bins: 保存的方向数目, defaults to 36
    :type n_bins: int, optional
    :param lambda_ori: 对模值加权时高斯函数sigma的系数, defaults to 3
    :type lambda_ori: int, optional
    :param t: 辅助方向的直方图阈值, defaults to 0.8
    :type t: int, optional
    """
    ret = []
    for key in keys:
        x, y = key.x, key.y
        sigma = key.sigma
        o, s = key.o, key.s

        w, h = sx.ws[o], sx.hs[o]

        delta = sx.deltas[o]

        dx = sx.octave[o][s, :, :]
        dy = sx.octave[o][s, :, :]

        # 将坐标转为特征金字塔对应层的坐标
        x = x / delta
        y = y / delta
        

        # 原图对应层的sigma
        sigma = sigma / delta 

        key.init_hist(n_bins) # 初始化关键点的直方图
        # 计算关键点的方向直方图
        accumulate_orientation_hist(x, y, sigma, dx, dy, n_bins, lambda_ori, key)

        # 提取关键点的多个方向
        prin_ori = extract_principal_ori(key.hist, t)

        # 把该关键点复制成多份关键点，并将方向值分别赋给这些复制后的关键点
        for ori in prin_ori:
            new_key = deepcopy(key)
            new_key.theta = ori
            ret.append(new_key)
    
    # 返回分配了方向的关键点
    return ret

        
#--------------关键点特征描述-------------
def rotate(x, y, theta):
    """将x y 点旋转theta
    """
    c = np.cos(theta)
    s = np.sin(theta)
    rx = c * x - s * y
    ry = s * x + c * y
    return rx, ry

def extract_sift_feature_vector(x, y, sigma, theta, im_dx, im_dy, n_hist, n_ori, lambda_descr, key:KeyPoint):
    h, w = im_dx.shape
    R = (1 + 1 / n_hist) * lambda_descr * sigma
    # 考虑旋转因素， 实际半径需要再乘根号2
    Rp = np.sqrt(2) * R

    si_min = max(0, int(x - Rp + 0.5))
    sj_min = max(0, int(y - Rp + 0.5))

    si_max = min(int(x + Rp + 0.5), h-1)
    sj_max = min(int(y + Rp + 0.5), w-1)

    # 遍历关键点的邻域
    for si in range(si_min, si_max+1):
        for sj in range(sj_min , sj_max):
            # 当前点相对于关键点的坐标
            sx = si - x
            sy = sj - y
            sx, sy = rotate(sx, sy, -theta) # 将关键点方向与坐标轴对齐

            if max(abs(sx), abs(sy)) < R: # 只处理区域内的点
                dx, dy = im_dx[si, sj], im_dy[si, sj]

                ori = np.arctan2(dy, dx) - theta # si sj点在旋转后的角度
                ori = (ori + 2*np.pi) % (2*np.pi)

                # 计算梯度幅值的加权
                t = lambda_descr * sigma
                M = np.hypot(dx, dy) * np.exp(-(sx*sx+sy*sy)/2*t*t)

                # alpha beta 指向当前的计算是哪个bin的中心
                alpha = sx / (2 * lambda_descr * sigma/n_hist) + (n_hist - 1) / 2
                beta  = sy / (2 * lambda_descr * sigma/n_hist) + (n_hist - 1) / 2
                gamma = ori / (2 * np.pi) * n_ori

                i0 = int(np.floor(alpha))
                j0 = int(np.floor(beta))

                for i in range(max(0, i0), min(i0+1, n_hist-1) + 1):
                    for j in range(max(0, j0), min(j0+1, n_hist-1) + 1):
                        # 当前指向的方向bin
                        k = (int(gamma) + n_ori) % n_ori

                        # 插值处理
                        # 方向指向是连续的，对相邻的两个bin都有贡献，通过权值平衡
                        # 靠近子区域中心的权值应该更大

                        # 对当前方向的贡献度
                        key.descr[i*n_hist*n_ori+j*n_ori+k] += M * (1 - (gamma - np.floor(gamma))) * (1 - abs(i - alpha)) * (1 - abs(j - beta))

                        # 对相邻方向的贡献度
                        k = (int(gamma) + 1 + n_ori) % n_ori
                        key.descr[i*n_hist*n_ori+j*n_ori+k] += M * (1 - (np.floor(gamma) + 1 - gamma)) * (1 - abs(i - alpha)) * (1 - abs(j - beta))



def threshold_quantize_feature_vector(key:KeyPoint, n_descr, thresh):
    l2_norm = np.linalg.norm(key.descr)
    t_descr = np.minimum(key.descr, thresh * l2_norm)

    l2_norm = np.linalg.norm(t_descr)
    t_descr = np.minimum(t_descr * 512 / l2_norm, 255)
    key.descr = t_descr

def keypoints_attribute_descriptors(
    im_dx: ScaleSpace, im_dy: ScaleSpace,
    keys: List[KeyPoint],
    n_hist:int, n_ori:int,
    lambda_descr: float):
    """生成SIFT描述子
    
    :param im_dx: x方向差分金字塔
    :type im_dx: ScaleSpace
    :param im_dy: y方向差分金字塔
    :type im_dy: ScaleSpace
    :param keys: 关键点列表
    :type keys: List[KeyPoint]
    :param n_hist: 直方图划分区域数目
    :type n_hist: int
    :param n_ori: 方向取样数目
    :type n_ori: int
    :param lambda_descr: 描述区域半径系数
    :type lambda_descr: float
    """
    n_descr = n_hist * n_hist * n_ori # 描述子向量的大小

    for key in keys:

        # 获取关键点的尺度信息
        x, y = key.x, key.y 
        o, s = key.o, key.s 
        sigma, theta = key.sigma, key.theta

        # 获取尺度空间梯度
        w, h = im_dx.ws[o], im_dx.hs[o]
        delta = im_dx.deltas[o]

        dx = im_dx.octave[o][s, :, :]
        dy = im_dy.octave[o][s, :, :]

        # 转换到原图尺度
        x /= delta
        y /= delta
        sigma /= delta

        key.init_descr(n_descr)
        extract_sift_feature_vector(x, y, sigma, theta, dx, dy, n_hist, n_ori, lambda_descr,  key)
        threshold_quantize_feature_vector(key, n_descr, 0.2)



#--------------sift算法调用-------------
def num_of_octave(w, h, delta_min):
    """计算图像金字塔的层数
    """
    hmin = 12 # 最顶层的图像大小
    h0 = min(w, h) / delta_min # 最底层图像大小
    n_oct = int(np.log2(h0/hmin)) + 1
    return n_oct

def get_thresh(n_spo, c_dog):
    k_nspo =  np.exp( np.log(2)/n_spo)
    k_3 =  np.exp( np.log(2) / 3)
    thresh = (k_nspo - 1) / (k_3 - 1) * c_dog
    return thresh
    

def sift_algorithm(
        img: np.ndarray, 
        n_oct=8, n_spo=3, # 图像金字塔参数
        c_dog=0.013333333, #0.04/3
        delta_min=0.5,
        sigma_min=0.8, sigma_in=0.5,
        n_bins=36, lambda_ori=1.5, # 方向匹配参数
        c_edge=10, # 边缘响应阈值
        t=0.8, n_hist=4, n_ori=8, lambda_descr=6, # sift描述算子参数
        iter_max=5): # 求极值点插值迭代次数

    h, w = img.shape

    n_oct = min(num_of_octave(w, h, 0.5), n_oct)

    #-------------生成图像金字塔-------------
    # 高斯金字塔
    g_scale = gaussian_scale_space(img, sigma_in=sigma_in, sigma_min=sigma_min, n_oct=n_oct, n_spo=n_spo)
    # 差分高斯
    dog_scale = scale_space_dog(g_scale)


    # 辅助过程，用于可视化图像金字塔
    for o in range(g_scale.n_oct):
        for s in range(g_scale.n_sca):
            img = g_scale.octave[o][s, :, :]
            img = (img * 255).astype('uint8')
            save_name = f'./sift_result/g_{o}_{s}.jpg'
            io.imsave(save_name, img) 
    
    def pseudocolor(arr):
        h = (arr - arr.min()) / (arr.max()-arr.min()) * 120
        hsv = np.stack([h, np.ones(h.shape), np.ones(h.shape)], axis=-1)
        # Convert hsv color (h,1,1) to its rgb equivalent.
        return color.hsv2rgb(hsv)

    for o in range(dog_scale.n_oct):
        for s in range(dog_scale.n_sca):
            img = dog_scale.octave[o][s, :, :]
            pseudo = pseudocolor(img)
            img = pseudo
            img = (img * 255).astype('uint8')
            save_name = f'./sift_result/d_{o}_{s}.jpg'
            io.imsave(save_name, img) 


    #--------------关键点检测-------------
    keypoints = keypoints_find_3d_discrete_extrema(dog_scale)

    # 计算关键点阈值
    thresh = get_thresh(n_spo, c_dog)
    keypoints_rm_low = keypoints_discard_with_low_response(keypoints, 0.8 * thresh)
    # 对关键点进行插值，获取更精确的位置
    keypoints_interp = keypoints_interpolate_position(dog_scale, keypoints_rm_low, iter_max)

    keyp_rm_low_again = keypoints_discard_with_low_response(keypoints_interp, thresh)

    # j计算边缘响应
    keypoints_edge_response(dog_scale, keyp_rm_low_again)
    # 移除不良边缘响应
    keys_rm_edge_rep = keypoints_discard_with_edge_resp(keyp_rm_low_again, (c_edge+1)**2 / c_edge)

    #--------------关键点描述-------------
    dx = deepcopy(g_scale)
    dy = deepcopy(g_scale)
    scale_compute_gradient(g_scale, dx, dy)  # 预计算两个方向的差分

    # 计算关键点的主要方向和辅助方向
    keys_attr_ori = keypoints_attribute_orientations(dx, dy, keys_rm_edge_rep, n_bins=n_bins, lambda_ori=lambda_ori, t=t)

    # 生成关键点描述
    keypoints_attribute_descriptors(dx, dy, keys_attr_ori, n_hist=n_hist, n_ori=n_ori, lambda_descr=lambda_descr)

    print(f'number of keypoints: {len(keys_attr_ori)}')

    return keys_attr_ori

def draw_sift_result(img_path, keys:List[KeyPoint], save_path, factor=3.5):
    """在图像上绘制检测出的SIFT关键点
    """
    img = Image.open(img_path)
    draw = ImageDraw.Draw(img)
    for key in keys:
        
        x, y, sigma, theta = key.x, key.y, key.sigma, key.theta
        # print(theta)
        sigma *= factor # 放大倍数,
        end_x, end_y = x + np.cos(theta) * sigma, y+np.sin(theta) * sigma
        draw.line([(y,x), (end_y, end_x)], fill=(255,0,0, 255))
        
        draw.ellipse((y-sigma, x-sigma, y+sigma, x+sigma), width=1, outline='red')

    img.save(save_path)

def sift_match():
    pass

if __name__ == "__main__":
    img_path = './img/sift/download.png'
    
    # img_path = './img/sift/jobs.jfif'
    img_path = './img/sift/images.jfif'
    
    base = path.basename(img_path)

    img = cv2.imread(img_path)
    img_RGB= cv2.cvtColor(img,cv2.COLOR_BGR2RGB)

    siftDetector=cv2.xfeatures2d.SIFT_create()
    kp = siftDetector.detect(img_RGB,None)
    kp,des = siftDetector.compute(img_RGB,kp)
    # 关键点列表
    print(f'cv2 检测数量:{len(kp)}')
    # des是一个大小为关键点数目*128的数组
    # print type(des),des.shape
    im=cv2.drawKeypoints(img_RGB,kp, np.array([]), (255,0,0), flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    
    save_path = f'./sift_result/cv2_{base}.png'
    io.imsave(save_path, im)


    img = imread(img_path)
    keys = sift_algorithm(img)
    
    save_path = f'./sift_result/{base}.png'
    draw_sift_result(img_path, keys, save_path)

    




```

🐧