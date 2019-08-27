Title: plt.imshow自动scaling.
Date: 2019-05-23

## Matplotlib imshow 自动scaling mapping

在做`直方图归一化`的时候发现`imshow`显示的图像是一样的, 更进一步观察发现`imshow`显示的居然不是原始的图像!!!!

问题跟这个`issue` [Why does pyplot display wrong grayscale image?](https://github.com/matplotlib/matplotlib/issues/7221/)完全一致.

这种多做事的太烦了
```python
plt.imshow(img, cmap=cm.gray, vmin=0, vmax=255)
```


🐧

