### HEP-CNN on Nurion trouble shooting  

1. 가장 최근 torch, conda 셋팅시 문제점  
 - epoch 이 끝나고 libgcc_s.so.1 must be installed for pthread_cancel to work 에러 발생  
 - 보다 근본적으로, import horovod.torch as hvd 시 다음과 같은 에러발생 
```bash
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/scratch/hpc22a03/conda/nurion_torch/lib/python3.8/site-packages/horovod/torch/__init__.py", line 44, in <module>
    from horovod.torch.mpi_ops import allreduce, allreduce_async, allreduce_, allreduce_async_
  File "/scratch/hpc22a03/conda/nurion_torch/lib/python3.8/site-packages/horovod/torch/mpi_ops.py", line 31, in <module>
    from horovod.torch import mpi_lib_v2 as mpi_lib
ImportError: /scratch/hpc22a03/conda/nurion_torch/lib/python3.8/site-packages/horovod/torch/mpi_lib_v2.cpython-38-x86_64-linux-gnu.so: undefined symbol: _ZNK2at6Tensor6deviceEv
```  
 - 해결책:  torch 1.6.0버전으로 설치  

 
