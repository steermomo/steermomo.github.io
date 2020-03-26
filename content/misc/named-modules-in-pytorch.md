Title: Pytorch中的named_modules是个啥-debug真难
Date: 2019-09-05 13:20
Modified: 2019-09-05 21:20
Category: Pytorch,
Tags: Python, Pytorch
Slug: named-modules-in-pytorch
Summary: 


Summary =>  在改写deeplabv3+时, 因为需要去掉ASPP和decoder部分, 仅保留mobilenet的backbone. 但是因为误对`nn.Module`内的所有权值进行初始化, 导致backbone中的预训练权值丢失. 同样的模型训练1000个epoch的效果依然很差.

<img src="{static}/images/file_3938986.jpg" style="max-width: 30%">

这几天遇到了一个十分奇怪的问题, 实验需要用到mobilenetv2作为backbone的deeplabv3+做分割, 在对比实验中需要丢掉ASPP和decoder部分, 即backbone后面直接接上两层卷积.  

最开始是直接在原来的deeplabv3+的代码上魔改, 即创建新的ASPP结构直接返回input, 再创建新的decoder部分只接受high level feature作为输出. 


但是这样修改的模型, 在测试速度时比原始的MobileNetV2要慢很多, 没法给出正确的性能数据. 但是原始的MobileNet又好像没有直接指定`out_stride`的地方. 我就按照修改后的ASPP跟decoder部分, 在deeplabv3+的backbone后面加了两层卷积. 测完速度, 效果达到, 十分开心.


在后续跑实验的过程中, 发现后面写的这个模型, 虽然能训练, 能收敛, 效果奇差.

后面的模型, 定义更加简单, 在结构上更是一模一样, 用torchsummary输出两个模型的结构, 更是一点没差, 作为对比, 使用了同一份训练代码, 完全相同的训练参数, 后者的效果仍然是无限逼近但永远达不到前者10个epoch的效果. 不是玄学就是Bug.


原始的deeplabv3+的代码定义是这样的
```python
class DeepLab(nn.Module):
    def __init__(self, backbone='resnet', output_stride=16, num_classes=21,
                 sync_bn=True, freeze_bn=False, deeplab_header=True):
        super(DeepLab, self).__init__()

        self.backbone = build_backbone(backbone, output_stride, BatchNorm)
        self.aspp = build_aspp(backbone, output_stride, BatchNorm, deeplab_header)
        self.decoder = build_decoder(num_classes, backbone, BatchNorm, deeplab_header)

        if freeze_bn:
            self.freeze_bn()

    def forward(self, input):
        x, low_level_feat = self.backbone(input)
        x = self.aspp(x)
        x = self.decoder(x, low_level_feat)
        x = F.interpolate(x, size=input.size()[2:], mode='bilinear', align_corners=True)
        return x

    def freeze_bn(self):
        for m in self.modules():
            if isinstance(m, SynchronizedBatchNorm2d):
                m.eval()
            elif isinstance(m, nn.BatchNorm2d):
                m.eval()

    def get_1x_lr_params(self):
        modules = [self.backbone]
        for i in range(len(modules)):
            for m in modules[i].named_modules():
                if isinstance(m[1], nn.Conv2d) or isinstance(m[1], SynchronizedBatchNorm2d) \
                        or isinstance(m[1], nn.BatchNorm2d):
                    for p in m[1].parameters():
                        if p.requires_grad:
                            yield p

    def get_10x_lr_params(self):
        modules = [self.aspp, self.decoder]
        for i in range(len(modules)):
            for m in modules[i].named_modules():
                if isinstance(m[1], nn.Conv2d) or isinstance(m[1], SynchronizedBatchNorm2d) \
                        or isinstance(m[1], nn.BatchNorm2d):
                    for p in m[1].parameters():
                        if p.requires_grad:
                            yield p
```

修改之后的代码直接将ASPP和decoder的内容拿了出来.

```python
class MobilenetV2(nn.Module):
    def __init__(self, output_stride=8, num_classes=2,sync_bn=True, freeze_bn=False):
        super(MobilenetV2, self).__init__()
        if sync_bn == True:
            BatchNorm = SynchronizedBatchNorm2d
        else:
            BatchNorm = nn.BatchNorm2d

        self.feat_conv = nn.Sequential(
            nn.Conv2d(320, 256, kernel_size=3, stride=1, padding=1, bias=False),
            BatchNorm(256),
            nn.ReLU()
        )
        self.prob_conv = nn.Sequential(
            nn.Dropout(0.1),
            nn.Conv2d(256, num_classes, kernel_size=1, stride=1, padding=0)
        )
        self._init_weight()

    def forward(self, x):
        mob_feat, low_level_feat = self.backbone(x)
        last_feat = self.feat_conv(mob_feat)
        prob_map = self.prob_conv(last_feat)
        ret = F.interpolate(prob_map, size=x.size()[2:], mode='bilinear', align_corners=True)
        return ret
    
    def get_1x_lr_params(self):
        modules = [self.backbone]
        for i in range(len(modules)):
            for m in modules[i].named_modules():
                if isinstance(m[1], nn.Conv2d) or isinstance(m[1], SynchronizedBatchNorm2d) \
                        or isinstance(m[1], nn.BatchNorm2d):
                    for p in m[1].parameters():
                        if p.requires_grad:
                            yield p

    def get_10x_lr_params(self):
        modules = [self.feat_conv, self.prob_conv]
        for i in range(len(modules)):
            for m in modules[i].named_modules():
                if isinstance(m[1], nn.Conv2d) or isinstance(m[1], SynchronizedBatchNorm2d) \
                        or isinstance(m[1], nn.BatchNorm2d):
                    for p in m[1].parameters():
                        if p.requires_grad:
                            yield p

    def _init_weight(self):
        for m in self.modules():
            if isinstance(m, nn.Conv2d):
                torch.nn.init.kaiming_normal_(m.weight)
            elif isinstance(m, SynchronizedBatchNorm2d):
                m.weight.data.fill_(1)
                m.bias.data.zero_()
            elif isinstance(m, nn.BatchNorm2d):
                m.weight.data.fill_(1)
                m.bias.data.zero_()
```


这里唯一显著的改变就是将ASPP和decoder的内容拿了出来.

<br>
### named_modules
> Returns an iterator over all modules in the network, yielding both the name of the module as well as the module itself.

在torch.nn.modules.module的源码中, named_modules的实现是这样的
```python
def named_modules(self, memo=None, prefix=''):
    if memo is None:
        memo = set()
    if self not in memo:
        memo.add(self)
        yield prefix, self
        for name, module in self._modules.items():
            if module is None:
                continue
            submodule_prefix = prefix + ('.' if prefix else '') + name
            for m in module.named_modules(memo, submodule_prefix):
                yield m
```
可以看出来这个调用过程是递归调用, 那我把decoder内的运算用`nn.Module`包装起来和拿到外面应该没有区别, 总会递归到所有的成员.


在Module类中, 可以看到_modules是一个有序字典.
```python
def _construct(self):
    """
    Initializes internal Module state, shared by both nn.Module and ScriptModule.
    """
    torch._C._log_api_usage_once("python.nn_module")
    self._backend = thnn_backend
    self._parameters = OrderedDict()
    self._buffers = OrderedDict()
    self._backward_hooks = OrderedDict()
    self._forward_hooks = OrderedDict()
    self._forward_pre_hooks = OrderedDict()
    self._state_dict_hooks = OrderedDict()
    self._load_state_dict_pre_hooks = OrderedDict()
    self._modules = OrderedDict()
```

emm...当我发现`named_modules()`是递归调用的时候, 我还没有意识到是哪里出了问题, 当我看到`modules()`实际上是调用了`named_modules()`的时候,🙄.  


所以问题是我在改写了原来deeplabv3+之后, 因为将ASPP和decoder的内容都直接显示地写在`forward()`方法中, 需要对`feat_conv`和`prob_conv`初始化, 初始化方法中调用了`modules()`遍历所有子`Conv2d`, 初始化其权重, 所以导致`backbone`中的所有权值都被初始化了😤. 丢了预训练权值, 效果自然差了一大截, 训练1000个epoch都抵不过训练10个epoch的效果.


把权重初始化的部分改为跳过backbone部分, 问题解决.
```python
def _init_weight(self):
    modules = [self.feat_conv, self.prob_conv]:
    for i in range(len(modules)):
        for m in modules[i].modules():
            if isinstance(m, nn.Conv2d):
                torch.nn.init.kaiming_normal_(m.weight)
            elif isinstance(m, SynchronizedBatchNorm2d):
                m.weight.data.fill_(1)
                m.bias.data.zero_()
            elif isinstance(m, nn.BatchNorm2d):
                m.weight.data.fill_(1)
                m.bias.data.zero_()
```

Slide note: 虽然罗里巴叽讲了一堆没用的东西, 不过是在啰嗦的过程中发现了Bug的位置, 我一直以为是因为套了一层`nn.Module`导致`get_10x_lr_params()`方法不能正确返回参数, 排除了几个问题之后才发现Bug这么明显. 

我决定save&push, 制造互联网垃圾.