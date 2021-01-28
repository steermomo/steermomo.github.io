Title: 在NCCL后端下Pytorch的distributed.all_gather卡死排查
Date: 2021-01-05 21:20
Modified: 2021-01-05 21:20
Category: Coding
Tags: PyTorch, Python
Slug: pytorch-dist-nccl-backend-allgather-stuck

用了Github上一个[SimCLR的PyTorch实现](https://github.com/Spijkervet/SimCLR)，但是在训练过程中遇到了一些问题。

原repo要用DDP训练的方式有点质朴，需要手动启动N的进程进行训练，那8张卡岂不是要操作八次！实验开多了要累死了。
```bash
CUDA_VISIBLE_DEVICES=0 python main.py --nodes 2 --nr 0
CUDA_VISIBLE_DEVICES=1 python main.py --nodes 2 --nr 1
CUDA_VISIBLE_DEVICES=2 python main.py --nodes 2 --nr 2
CUDA_VISIBLE_DEVICES=N python main.py --nodes 2 --nr 3
```

## 一行代码起

这肯定不能忍，不符合我的风格，我从陈年代码包里拿出了我的顺手工具，能一行做完的事情绝不用八行。
```bash

python3 -m torch.distributed.launch --nproc_per_node 2 --master_port=9495 main.py
```

一行代码起！完美！

后面还有一些把分布式通讯的配置修改的问题，比如移除
```python
# Master address for distributed data parallel
os.environ["MASTER_ADDR"] = "127.0.0.1"
os.environ["MASTER_PORT"] = "8000"
mp.spawn(main, args=(args,), nprocs=args.gpus, join=True)
```
加上
```python
dist.init_process_group(backend='nccl', rank=args.local_rank)
```

## Debug靠Google

完事了，Docker调起、磁盘挂载、程序启动...

然后就看见GPU0卡死100%，GPU1-N傻站着不动。

这不行，上工具定位，发现是多卡通讯中卡在dist.all_gather这一步。
这里有一步实现需要对所有卡上的特征进行聚合计算正负样本，但只希望保留当前卡内的梯度。
```python
class GatherLayer(torch.autograd.Function):
    '''Gather tensors from all process, supporting backward propagation.
    '''

    @staticmethod
    def forward(ctx, input):
        ctx.save_for_backward(input)
        output = [torch.zeros_like(input) \
            for _ in range(dist.get_world_size())]

        dist.all_gather(output, input)
        return tuple(output)

    @staticmethod
    def backward(ctx, *grads):
        input, = ctx.saved_tensors
        grad_out = torch.zeros_like(input)
        grad_out[:] = grads[dist.get_rank()]
        return grad_out
```


想下班回家了...不想写了，反正就是对着Google一顿猛搜，发现有跟我一样的倒霉蛋遇到了类似的问题[^1]，就是在NCCL初始化init_process_group之前，需要先为每个进程分配GPU，分配完事了就没任何问题了。
```python
torch.cuda.set_device(args.rank)
dist.init_process_group(backend='nccl', rank=local_rank)
```



AP:
🤣

之前还遇到过诡异的M40卡死在dist.all_gather，但是在P40上运行就十分正常，还找了机器学习平台的同事花了一下午时间debug。

现在回去检查当时出现诡异bug的代码，果然是我写错了，我给这两句写反了啊！😑🙄
```python
dist.init_process_group(backend='nccl', rank=local_rank)
torch.cuda.set_device(args.local_rank)
```


[^1]: [distributed.all_gather function stuck when using NCCL backend](https://github.com/pytorch/pytorch/issues/18689)