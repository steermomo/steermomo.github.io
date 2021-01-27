Title: Deformable-DETR中的MultiScaleDeformableAttention
Date: 2021-01-14 18:20
Modified: 2021-01-14 18:20
Category: Coding
Tags: Python,Pytorch
Slug: MSAttn-in-Deformable-DETR
Status: draft

最近一个任务需要用到Deformable-DETR，其中比较关键的一步是Multi-scale Deformable Attention Module （MSDeformAttn），这个模块能够实现在multi-scale的feature map上的deformable convolution操作。

## Deformable-DETR的大致结构
Deformable-DETR具体算法可以去看原文章[^1]，这里说一下大概的结构。

下图是D-DETR的框架图，MSDeformAttn是希望将deformable convolution扩展到Multi-scale Feature Maps上。原来的deformable convolution可以当成是在一个二维平面上对采样点进行偏移，这里对同一个采样位置，需要同时在多个尺度的feature map上做不同程度的偏移。
<img style="width:95%" src="/images/2021/ddetr_arch_tiny_png.png" />

## Multi-Scale-Deformable-Attention

#### 函数定义

reference_points
#### 代码实现

```python
import torch
import torch.nn.functional as F
from torch.autograd import Function
from torch.autograd.function import once_differentiable

import MultiScaleDeformableAttention as MSDA


class MSDeformAttnFunction(Function):
    @staticmethod
    def forward(ctx, value, value_spatial_shapes, value_level_start_index, sampling_locations, attention_weights, im2col_step):
        ctx.im2col_step = im2col_step
        output = MSDA.ms_deform_attn_forward(
            value, value_spatial_shapes, value_level_start_index, sampling_locations, attention_weights, ctx.im2col_step)
        ctx.save_for_backward(value, value_spatial_shapes, value_level_start_index, sampling_locations, attention_weights)
        return output

    @staticmethod
    @once_differentiable
    def backward(ctx, grad_output):
        value, value_spatial_shapes, value_level_start_index, sampling_locations, attention_weights = ctx.saved_tensors
        grad_value, grad_sampling_loc, grad_attn_weight = \
            MSDA.ms_deform_attn_backward(
                value, value_spatial_shapes, value_level_start_index, sampling_locations, attention_weights, grad_output, ctx.im2col_step)

        return grad_value, None, None, grad_sampling_loc, grad_attn_weight, None
```

这里forward函数的几个参数



| Parameter               | Shape                                    | Comment                     |
| ----------------------- | :--------------------------------------- | :-------------------------- |
| value                   | N,HW,C                                   | 多个尺度拉平后的Feature Map |
| value_spatial_shapes    | S,2                                      | 每个尺度的Feature Map的大小 |
| value_level_start_index | S,1                                      |                             |
| sampling_locations      | N, Len_q, n_heads, n_levels, n_points, 2 |                             |
| attention_weights       | n_heads \* n_levels \* n_points          |                             |
| im2col_step             |                                          |                             |


#### CPP接口
MSDeformAttn的CPP接口是在models/src/下，实际上只实现了CUDA版本。

在vision.cpp内，使用pybind11将Python和C++的方法绑定在一起。
```cpp
#include "ms_deform_attn.h"

PYBIND11_MODULE(TORCH_EXTENSION_NAME, m) {
  m.def("ms_deform_attn_forward", &ms_deform_attn_forward, "ms_deform_attn_forward");
  m.def("ms_deform_attn_backward", &ms_deform_attn_backward, "ms_deform_attn_backward");
}
```
在models/src/cuda下，则是具体的实现.



```cpp
#include <vector>
#include "cuda/ms_deform_im2col_cuda.cuh"

#include <ATen/ATen.h>
#include <ATen/cuda/CUDAContext.h>
#include <cuda.h>
#include <cuda_runtime.h>


at::Tensor ms_deform_attn_cuda_forward(
    const at::Tensor &value, 
    const at::Tensor &spatial_shapes,
    const at::Tensor &level_start_index,
    const at::Tensor &sampling_loc,
    const at::Tensor &attn_weight,
    const int im2col_step)
{
    AT_ASSERTM(value.is_contiguous(), "value tensor has to be contiguous");
    AT_ASSERTM(spatial_shapes.is_contiguous(), "spatial_shapes tensor has to be contiguous");
    AT_ASSERTM(level_start_index.is_contiguous(), "level_start_index tensor has to be contiguous");
    AT_ASSERTM(sampling_loc.is_contiguous(), "sampling_loc tensor has to be contiguous");
    AT_ASSERTM(attn_weight.is_contiguous(), "attn_weight tensor has to be contiguous");

    AT_ASSERTM(value.type().is_cuda(), "value must be a CUDA tensor");
    AT_ASSERTM(spatial_shapes.type().is_cuda(), "spatial_shapes must be a CUDA tensor");
    AT_ASSERTM(level_start_index.type().is_cuda(), "level_start_index must be a CUDA tensor");
    AT_ASSERTM(sampling_loc.type().is_cuda(), "sampling_loc must be a CUDA tensor");
    AT_ASSERTM(attn_weight.type().is_cuda(), "attn_weight must be a CUDA tensor");

    const int batch = value.size(0);
    const int spatial_size = value.size(1);
    const int num_heads = value.size(2);
    const int channels = value.size(3);

    const int num_levels = spatial_shapes.size(0);

    const int num_query = sampling_loc.size(1);
    const int num_point = sampling_loc.size(4);

    const int im2col_step_ = std::min(batch, im2col_step);

    AT_ASSERTM(batch % im2col_step_ == 0, "batch(%d) must divide im2col_step(%d)", batch, im2col_step_);
    
    auto output = at::zeros({batch, num_query, num_heads, channels}, value.options());

    const int batch_n = im2col_step_;
    auto output_n = output.view({batch/im2col_step_, batch_n, num_query, num_heads, channels});
    auto per_value_size = spatial_size * num_heads * channels;
    auto per_sample_loc_size = num_query * num_heads * num_levels * num_point * 2;
    auto per_attn_weight_size = num_query * num_heads * num_levels * num_point;
    for (int n = 0; n < batch/im2col_step_; ++n)
    {
        auto columns = output_n.select(0, n);
        AT_DISPATCH_FLOATING_TYPES(value.type(), "ms_deform_attn_forward_cuda", ([&] {
            ms_deformable_im2col_cuda(at::cuda::getCurrentCUDAStream(),
                value.data<scalar_t>() + n * im2col_step_ * per_value_size,
                spatial_shapes.data<int64_t>(),
                level_start_index.data<int64_t>(),
                sampling_loc.data<scalar_t>() + n * im2col_step_ * per_sample_loc_size,
                attn_weight.data<scalar_t>() + n * im2col_step_ * per_attn_weight_size,
                batch_n, spatial_size, num_heads, channels, num_levels, num_query, num_point,
                columns.data<scalar_t>());

        }));
    }

    output = output.view({batch, num_query, num_heads*channels});

    return output;
}
```

[^1]: https://arxiv.org/abs/2010.04159
