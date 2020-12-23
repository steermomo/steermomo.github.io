Title: PyTorch DistributedSampler封装其他Sampler策略
Date: 2020-12-23 18:20
Modified: 2020-12-23 18:20
Category: Coding
Tags: Python, PyTorch
Slug: pytorch-ddp-sampler-warper

用了PyTorch的分布式训练后，我把所有的dataloader都加上了 DistributedSampler 。

现在遇到的一个问题是需要对不同类别的样本进行采样，而PytTorch自带的WeightedRandomSampler 又不是那么回事，不能直接对类别进行采样，索性自己造了个轮子解决这个问题。


## WeightedBalanceClassSampler
首先要解决的是对每个类别进行采样，这里用了catalyst的一部分代码[^1]。catalyst提供了一个 BalanceClassSampler 实现类别均衡采样，但在我的场景下，类别不均衡比较严重，BalanceClassSampler 里将所有类的数量直接填成一样的了，不满足我的要求。

在 BalanceClassSampler 的基础上，这里实现了 WeightedBalanceClassSampler 用于带权采样。
用 weight 指定每个类别的采样比例，用length指定采样后数据集的大小。

weight 归一化后，乘上length计算采样后每个的数目，使用 saferound 保证类型转换后sample的总数仍然是一样的。

在 \_\_iter\_\_ 方法中 使用 np.random.choice 对每个类别下的索引进行采样。

```python
class WeightedBalanceClassSampler(Sampler):
    """Allows you to create stratified sample on unbalanced classes with given probabilities (weights).
    Args:
        labels: list of class label for each elem in the dataset
        weight: A sequence of weights to balance classes, not necessary summing up to one.
        length: the length of the sample dataset.
    """

    def __init__(
        self, labels: List[int], weight: List, length: int,
    ):
        """Sampler initialisation."""
        super().__init__(labels)

        labels = np.array(labels).astype(np.int)

        self.lbl2idx = {
            label: np.arange(len(labels))[labels == label].tolist()
            for label in set(labels)
        }

        weight = np.array(weight)
        weight = weight / weight.sum()

        samples_per_class = weight * length

        samples_per_class = np.array(saferound(samples_per_class, places=0)).astype(np.int)

        self.labels = labels
        self.samples_per_class = samples_per_class
        self.length = length

    def __iter__(self) -> Iterator[int]:
        """
        Yields:
            indices of stratified sample
        """
        indices = []
        for key in sorted(self.lbl2idx):
            replace_flag = self.samples_per_class[key] > len(self.lbl2idx[key])
            indices += np.random.choice(
                self.lbl2idx[key], self.samples_per_class[key], replace=replace_flag
            ).tolist()
        assert len(indices) == self.length
        np.random.shuffle(indices)

        return iter(indices)

    def __len__(self) -> int:
        """
        Returns:
             length of result sample
        """
        return self.length
```

## DistributedSamplerWrapper

PyTorch的DistributedSampler是直接对dataset进行封装，这里在已经封装了一层 WeightedBalanceClassSampler 后，需要将内部的 sampler 再放到DistributedSampler 内。

这里仍然是用了catalyst的两个类：DatasetFromSampler和DistributedSamplerWrapper。

其中 DatasetFromSampler 将内部的sampler包装成dataset的接口。

```python
class DatasetFromSampler(torch.utils.data.Dataset):
    """Dataset to create indexes from `Sampler`.
    Args:
        sampler: PyTorch sampler
    """

    def __init__(self, sampler: Sampler):
        """Initialisation for DatasetFromSampler."""
        self.sampler = sampler
        self.sampler_list = None

    def __getitem__(self, index: int):
        """Gets element of the dataset.
        Args:
            index: index of the element in the dataset
        Returns:
            Single element by index
        """
        if self.sampler_list is None:
            self.sampler_list = list(self.sampler)
        return self.sampler_list[index]

    def __len__(self) -> int:
        """
        Returns:
            int: length of the dataset
        """
        return len(self.sampler)
```

而DistributedSamplerWrapper是继承自PyTorch自带的DistributedSampler。

看 PyTorch DistributedSampler的源码[^2]可以知道，继承后需要覆写它的 \_\_iter\_\_ 方法，实现自己的迭代过程。

父类 DistributedSampler的 \_\_iter\_\_ 方法会返回当前rank下的dataset 索引，即已经处理好了分布式下的sampler，那在这里可以使用父类返回的索引值，对内部的 WeightedBalanceClassSampler 再进行一次索引，实现对 WeightedBalanceClassSampler 的封装。

```python
class DistributedSamplerWrapper(DistributedSampler):
    """
    Wrapper over `Sampler` for distributed training.
    Allows you to use any sampler in distributed mode.
    It is especially useful in conjunction with
    `torch.nn.parallel.DistributedDataParallel`. In such case, each
    process can pass a DistributedSamplerWrapper instance as a DataLoader
    sampler, and load a subset of subsampled data of the original dataset
    that is exclusive to it.
    .. note::
        Sampler is assumed to be of constant size.
    """

    def __init__(
        self,
        sampler,
        num_replicas: Optional[int] = None,
        rank: Optional[int] = None,
        shuffle: bool = True,
    ):
        """
        Args:
            sampler: Sampler used for subsampling
            num_replicas (int, optional): Number of processes participating in
              distributed training
            rank (int, optional): Rank of the current process
              within ``num_replicas``
            shuffle (bool, optional): If true (default),
              sampler will shuffle the indices
        """
        super(DistributedSamplerWrapper, self).__init__(
            DatasetFromSampler(sampler),
            num_replicas=num_replicas,
            rank=rank,
            shuffle=shuffle,
        )
        self.sampler = sampler

    def __iter__(self):
        """@TODO: Docs. Contribution is welcome."""
        self.dataset = DatasetFromSampler(self.sampler)
        indexes_of_indexes = super().__iter__()
        subsampler_indexes = self.dataset
        return iter(itemgetter(*indexes_of_indexes)(subsampler_indexes))
```

[^1]: https://github.com/catalyst-team/catalyst/blob/master/catalyst/data/sampler.py
[^2]: https://github.com/pytorch/pytorch/blob/master/torch/utils/data/distributed.py