Title: Deformable-Conv编译后运行报错及解决
Date: 2021-01-27 18:20
Modified: 2021-01-27 18:20
Category: Coding
Tags: Python,Pytorch
Slug: Build-MSAttn-in-Deformable-DETR
<!-- Status: draft -->

最近一个任务需要用到Deformable-DETR，其中比较关键的一步是Multi-scale Deformable Attention Module （MSDeformAttn），这个模块能够实现在multi-scale的feature map上的deformable convolution操作。


所用的代码是Deformable DETR的官方实现[^1]，其中需要先对CUDA的算子进行编译
```bash
cd ./models/ops
sh ./make.sh
# unit test (should see all checking is True)
python test.py
```
我这里编译完之后，在集群上的M40 GPU上是可以正常训练的，但是切换到P40之后，运行就一直刷错误
```bash
error in ms_deformable_im2col_cuda: no kernel image is available for execution on the device
```

集群上的环境是:
```bash
CUDA                10.2
torch               1.7.0+cu101
torchvision         0.8.1+cu101
OS                  4.14.105-1-tlinux3-0013
```

```bash
+-----------------------------------------------------------------------------+
| NVIDIA-SMI 440.64.00    Driver Version: 440.64.00    CUDA Version: 10.2     |
|-------------------------------+----------------------+----------------------+
| GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
| Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
|===============================+======================+======================|
|   0  Tesla P40           On   | 00000000:04:00.0 Off |                  Off |
| N/A   43C    P0    57W / 250W |  20653MiB / 24451MiB |    100%      Default |
+-------------------------------+----------------------+----------------------+
+-------------------------------+----------------------+----------------------+
|   7  Tesla P40           On   | 00000000:0F:00.0 Off |                  Off |
| N/A   47C    P0   142W / 250W |  20653MiB / 24451MiB |     40%      Default |
+-------------------------------+----------------------+----------------------+
```

找到这段错误代码来自models/ops/src/cuda/ms_deform_im2col_cuda.cuh 
```cpp
void ms_deformable_im2col_cuda(cudaStream_t stream,
                              const scalar_t* data_value,
                              const int64_t* data_spatial_shapes, 
                              const int64_t* data_level_start_index, 
                              const scalar_t* data_sampling_loc,
                              const scalar_t* data_attn_weight,
                              const int batch_size,
                              const int spatial_size, 
                              const int num_heads, 
                              const int channels, 
                              const int num_levels, 
                              const int num_query,
                              const int num_point,
                              scalar_t* data_col)
{
  const int num_kernels = batch_size * num_query * num_heads * channels;
  const int num_actual_kernels = batch_size * num_query * num_heads * channels;
  const int num_threads = CUDA_NUM_THREADS;
  ms_deformable_im2col_gpu_kernel<scalar_t>
      <<<GET_BLOCKS(num_actual_kernels, num_threads), num_threads,
          0, stream>>>(
      num_kernels, data_value, data_spatial_shapes, data_level_start_index, data_sampling_loc, data_attn_weight, 
      batch_size, spatial_size, num_heads, channels, num_levels, num_query, num_point, data_col);
  
  cudaError_t err = cudaGetLastError();
  if (err != cudaSuccess)
  {
    printf("error in ms_deformable_im2col_cuda: %s\n", cudaGetErrorString(err));
  }

}
```
在调用ms_deformable_im2col_gpu_kernel之后出现了问题，网上搜了一下也没发现解决方案。

只能自己看了一下`setup.py`, 发现里面与编译相关配置为
```python
    if torch.cuda.is_available() and CUDA_HOME is not None:
        extension = CUDAExtension
        sources += source_cuda
        define_macros += [("WITH_CUDA", None)]
        extra_compile_args["nvcc"] = [
            "-DCUDA_HAS_FP16=1",
            "-D__CUDA_NO_HALF_OPERATORS__",
            "-D__CUDA_NO_HALF_CONVERSIONS__",
            "-D__CUDA_NO_HALF2_OPERATORS__",

        ]
    else:
        raise NotImplementedError('Cuda is not availabel')
```

P40上也没有FP16的支持，遂将`-DCUDA_HAS_FP16=1`改成了`-DCUDA_HAS_FP16=0`。
然后删除build文件重新编译一遍，运行就都正常了。





[^1]: https://github.com/fundamentalvision/Deformable-DETR
