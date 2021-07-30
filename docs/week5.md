# Week 5: Beyond OpenMP and MPI: GPU parallelisation 

## 5.1 V: Introduction

In this week we will go beyond classical parallelisation paradigms (like OpenMP and MPI) which are generally associated with CPUs. We will talk about Graphics Processing Units (GPUs) that were originally developed for executing graphical tasks (including rendering in computer games) but can also be used for general purpose computing in many fields. So, in the context of general purpose computing GPUs are referred to as accelerators for intensive computational tasks. The main advantage of GPUs over CPUs is greater computational capability and high-bandwidth memory, but on the other hand GPUs are known for latency problems. Thus, efficient computing algorithms make use of the "best of both worlds" approach:

- GPUs are used for parallel tasks, while CPUs for serial tasks;
- GPUs are used to achieve throughput performance, while CPUs for low-latency access.

Computing acceleration can be achieved with:

- existing GPU applications
- GPU libraries
- directive based methods: OpenMP, OpenACC...
- special programming languages or extensions: CUDA, OpenCL...

In this week we shall briefly present OpenMP as a means for "off-loading" parallel tasks to GPUs and more thoroughly deal with two extensions to C for programming GPUs: CUDA and OpenCL. On one hand, GPU off-loading is simple to use, but it's quite limited, contrary to GPU programming which requires more effort, but offers more flexibility.

## 5.2 GPU Architecture

In order to understand better the capabilities of GPUs in terms of computing acceleration we will have a look at a typical architecture of a modern GPU.

As we already pointed out, GPUs were originally designed to accelerate graphics. They excel at operations (such as shading and rendering) on graphical primitives which constitute a 3D graphical object. The main characteristic of these primitives is that they are independent or, in other words, they can be processed independently in a parallel fashion. Thus, GPU acceleration of graphics was designed for the execution of inherently parallel tasks. On the other hand, CPUs are designed to execute the workflow of any general-purpose program, where many parallel tasks may not be involved. These different design principles reflect the fact that GPUs have many more processing units and higher memory bandwidth, while CPUs are characterized by more specialized processing of instructions and faster clock speed rates.

On the figure (source: nvidia.com) below you can observe schematics of both CPU and GPU hardware architectures. From the schematics it is evident that:

- a GPU has many more arithmetic logic units or ALUs (green rectangles) than a CPU;
- a GPU can control simple, highly parallel workloads well (there's a yellow rectangle for every row of green rectangles), contrary to a CPU which can control more complex workloads;
- a core (green rectangle) in a CPU is different than a "core" or ALU (green rectangle) in a GPU: the former is comprised by ALUs and FPUs which are more specialized than ALUs in a GPU;
- a CPU has more cache memory than a GPU.

![](images/CPU_vs_GPU_architecture.png?raw=true)

It has to be noted that the term "GPU core" is more or less a marketing term. The equivalent of a CPU core in a GPU is a streaming multiprocessor (SM) with many ALUs or "cores" (typically more than 100). Each SM has a lot of (L1 cache) registers (32-64 KB), instruction scheduler dispatchers and a very fast shared memory. In the next step we will put everything explained so far into perspective by showing some numbers.

## 5.3 E: GPUs by numbers

Nowadays, desktop PCs or laptops are standardly equipped with a GPU, either integrated or as a standalone card. But how such GPUs differ from GPUs dedicated to computing, e.g., on supercomputers (HPC clusters)?

First, let's have a look at the GPUs that are installed on the Marconi-100 cluster (currently #14 on the [Top500 list](https://www.top500.org/lists/top500/list/2021/06/) of supercomputers in the world). By invoking the diagnostic utilities ```deviceQuery``` and ```bandwidthTest``` in the terminal of the login node we can get:

Output (excerpt) from ```deviceQuery```:

```
Detected 4 CUDA Capable device(s)

Device 0: "Tesla V100-SXM2-16GB"
  CUDA Driver Version / Runtime Version          11.0 / 10.2
  CUDA Capability Major/Minor version number:    7.0
  Total amount of global memory:                 16128 MBytes (16911433728 bytes)
  (80) Multiprocessors, ( 64) CUDA Cores/MP:     5120 CUDA Cores
  GPU Max Clock rate:                            1530 MHz (1.53 GHz)
  Memory Clock rate:                             877 Mhz
  Memory Bus Width:                              4096-bit
  L2 Cache Size:                                 6291456 bytes
  Maximum Texture Dimension Size (x,y,z)         1D=(131072), 2D=(131072, 65536), 3D=(16384, 16384, 16384)
  Maximum Layered 1D Texture Size, (num) layers  1D=(32768), 2048 layers
  Maximum Layered 2D Texture Size, (num) layers  2D=(32768, 32768), 2048 layers
  Total amount of constant memory:               65536 bytes
  Total amount of shared memory per block:       49152 bytes
  Total number of registers available per block: 65536
  Warp size:                                     32
  Maximum number of threads per multiprocessor:  2048
  Maximum number of threads per block:           1024
  Max dimension size of a thread block (x,y,z): (1024, 1024, 64)
  Max dimension size of a grid size    (x,y,z): (2147483647, 65535, 65535)
  Maximum memory pitch:                          2147483647 bytes
  Texture alignment:                             512 bytes
  Concurrent copy and kernel execution:          Yes with 4 copy engine(s)
  Run time limit on kernels:                     No
  Integrated GPU sharing Host Memory:            No
  Support host page-locked memory mapping:       Yes
  Alignment requirement for Surfaces:            Yes
  Device has ECC support:                        Enabled
  Device supports Unified Addressing (UVA):      Yes
  Device supports Compute Preemption:            Yes
  Supports Cooperative Kernel Launch:            Yes
  Supports MultiDevice Co-op Kernel Launch:      Yes
  Device PCI Domain ID / Bus ID / location ID:   4 / 4 / 0
```
Output (excerpt) from ```bandwidthTest```:

```
 Device 0: Tesla V100-SXM2-16GB
 Quick Mode

 Host to Device Bandwidth, 1 Device(s)
 PINNED Memory Transfers
   Transfer Size (Bytes)        Bandwidth(GB/s)
   32000000                     67.1

 Device to Host Bandwidth, 1 Device(s)
 PINNED Memory Transfers
   Transfer Size (Bytes)        Bandwidth(GB/s)
   32000000                     65.8

 Device to Device Bandwidth, 1 Device(s)
 PINNED Memory Transfers
   Transfer Size (Bytes)        Bandwidth(GB/s)
   32000000                     712.9

Result = PASS
```

There were 4 NVIDIA Tesla V100-SXM2-16GB GPUs detected on the login node of the cluster. Every compute node of the cluster is also equipped with 4 GPUs of the same type, on 980 compute nodes + 8 login nodes there are 3952 GPU accelerators in total. Combined the GPUs account for 97.5% of the total theoretical peak performance of the Marconi-100 supercomputer: 30.83 out of 31.6 PFlops. Really a huge compute power!

If we do the same on a consumer grade laptop (assuming it is equipped with a standalone GPU by NVIDIA), we get, e.g.:

Output (excerpt) from ```deviceQuery```:

```
Detected 1 CUDA Capable device(s)

Device 0: "GeForce 930MX"
  CUDA Driver Version / Runtime Version          11.2 / 10.1
  CUDA Capability Major/Minor version number:    5.0
  Total amount of global memory:                 2004 MBytes (2101870592 bytes)
  ( 3) Multiprocessors, (128) CUDA Cores/MP:     384 CUDA Cores
  GPU Max Clock rate:                            1020 MHz (1.02 GHz)
  Memory Clock rate:                             1001 Mhz
  Memory Bus Width:                              64-bit
  L2 Cache Size:                                 1048576 bytes
  Maximum Texture Dimension Size (x,y,z)         1D=(65536), 2D=(65536, 65536), 3D=(4096, 4096, 4096)
  Maximum Layered 1D Texture Size, (num) layers  1D=(16384), 2048 layers
  Maximum Layered 2D Texture Size, (num) layers  2D=(16384, 16384), 2048 layers
  Total amount of constant memory:               65536 bytes
  Total amount of shared memory per block:       49152 bytes
  Total number of registers available per block: 65536
  Warp size:                                     32
  Maximum number of threads per multiprocessor:  2048
  Maximum number of threads per block:           1024
  Max dimension size of a thread block (x,y,z): (1024, 1024, 64)
  Max dimension size of a grid size    (x,y,z): (2147483647, 65535, 65535)
  Maximum memory pitch:                          2147483647 bytes
  Texture alignment:                             512 bytes
  Concurrent copy and kernel execution:          Yes with 1 copy engine(s)
  Run time limit on kernels:                     Yes
  Integrated GPU sharing Host Memory:            No
  Support host page-locked memory mapping:       Yes
  Alignment requirement for Surfaces:            Yes
  Device has ECC support:                        Disabled
  Device supports Unified Addressing (UVA):      Yes
  Device supports Compute Preemption:            No
  Supports Cooperative Kernel Launch:            No
  Supports MultiDevice Co-op Kernel Launch:      No
  Device PCI Domain ID / Bus ID / location ID:   0 / 1 / 0
```

Output (excerpt) from ```bandwidthTest```:

```
 Device 0: GeForce 930MX
 Quick Mode

 Host to Device Bandwidth, 1 Device(s)
 PINNED Memory Transfers
   Transfer Size (Bytes)	Bandwidth(MB/s)
   33554432			2934.4

 Device to Host Bandwidth, 1 Device(s)
 PINNED Memory Transfers
   Transfer Size (Bytes)	Bandwidth(MB/s)
   33554432			2973.9

 Device to Device Bandwidth, 1 Device(s)
 PINNED Memory Transfers
   Transfer Size (Bytes)	Bandwidth(MB/s)
   33554432			13520.2

Result = PASS
```

There was 1 NVIDIA GeForce 930MX GPU detected on the laptop.

The outputs show that a professional high-end card has much more global memory, streaming multiprocessors (SMs) and "cores" available and also a much higher memory bandwidth than a consumer grade card: 16 GB, 80 SMs, 5120 CUDA cores, 712.9 GB/s and 2 GB, 3 SMs, 384 CUDA cores, 13520.2 MB/s, respectively. The V100 has also a much higher theoretical throughput of 15.7 TFlops (for FP32) than the GeForce 930MX with throughput of 0.765 TFlops (for FP32).

In short, both cards share the same technology but consumer grade ones are quite inferior in terms of hardware resources. Of course, there are some other differences (like the underlying microarchitecture), but both can be used for GPU computing albeit with a big difference in performance. To be completely frank there also exist gaming cards with better performance, even somewhat comparable to professional cards, but we won't go into details of why they are not used in HPC systems or data centers.

Here we have compared only GPUs of one manufacturer (NVIDIA). Similar characteristics apply also for consumer grade and professional cards of other manufacturers, e.g., AMD.

## 5.4 Exer.: Information and compute capabilities of a GPU

In this exercise you will check the information and compute capabilities of the GPU available for you in the current sesion of Colab.

Login to Colab and first check if your runtime type is set to ```GPU``` by:

```
Runtime -> Change runtime type
```

If not change it to ```GPU``` in the ```Hardware accelerator``` dropdown menu.

Now you can complete the following tasks:

- find general info on the GPU by:

```
!nvidia-smi
```

- find the diagnostic programs ```deviceQuery``` and ```bandwidthTest``` by:

```
!ls -l /usr/local/cuda-11.0/extras/demo_suite

```

- execute the diagnostic utilities to determine the main characteristics of the GPU (No. of SMs,
No. of CUDA cores, global memory available, memory bandwidth) by:

```
!/usr/local/cuda-11.0/extras/demo_suite/deviceQuery
```

and

```
!/usr/local/cuda-11.0/extras/demo_suite/bandwidthTest
```

How the characteristics of the GPU in your login session compare to those of the GPUs in the previous step? Leave a comment with your findings.

## 5.5 Quiz: GPU basics and architecture

## 5.6 GPU programming solutions

As already mentioned, GPUs serve as accelerators to CPUs, i.e., computationally intensive tasks are off-loaded from CPUs to GPUs. Standard programming languages such as Fortran and C/C++ do not permit such off-loading because of their lack of addressing distinct memory spaces and of knowing the GPU architecture. For that purpose special language extensions are needed which basically allow GPU programming.

Many solutions exist for programming GPUs, we will talk about the two mostly used, i.e., CUDA and OpenCL. CUDA (Compute Unified Device Architecture) is a set of extensions to higher level programming languages (C, C++ and Fortran) developed by NVIDIA for its GPUs. CUDA comes with a developer toolkit for compiling, debugging and profiling programs. It's the first solution for GPU programming (the current version is 11.x) but unfortunately it's only supported by GPUs manufactured by NVIDIA.

Another solution is OpenCL (Open Computing Language), which is a standard open-source programming model initially developed by major manufacturers (Apple, Intel, ATI/AMD, NVIDIA), now maintained by Khronos. It also provides extensions to C, while C++ is supported in SYCL (a similar but independent solution by Khronos). Although its programming model is similar to CUDA, it's more low-level. It can also come with a developer toolkit, depending on the hardware, but its main advantage over CUDA is that it's supported by many types of Processing Units (CPUs, GPUs, FPGAs, MICs...) and is de facto oriented to heterogeneous computing. In principle that means an OpenCL program can run either on a GPU (not depending on the manufacturer) or on a CPU (or any other PU). OpenCL's standard is currently at 2.x. Unfortunately, the NVIDIA GPUs does not support it (contrary to Intel and AMD GPUs), the support is offered only for OpenCL 1.2.

![](images/CUDA_OpenCL.png?raw=true)

## 5.7 E: Hello world on GPU

Before explaining CUDA and OpenCL programming models in detail we will introduce GPU programming with a Hello World example.

Let's first have a look at the following C code:

```
#define N 4
for(int i = 0; i < N; ++i){
    printf("Hello world! I'm Iteration %d\n", i);
}
```

What do you think this code will do if executed as a program? If you are familiar with the concept of a ```for``` loop then you know that in it every iteration of the code is run sequentially (on a CPU) and that the above code will print ''Hello world'' messages in order from iteration 0 to 3. Try to execute it in the notebook to see the expected results:

![Hello_World_C.ipynb](https://github.com/kosl/ihipp-examples/blob/master/GPU/Hello_World_C.ipynb)

By now we already know that GPUs are really good at executing independent parallel tasks, hence the above ```for``` loop is a good candidate for that. How can we do it in CUDA? Let's give the solution:

```
#define NUM_BLOCKS 4
#define BLOCK_SIZE 1

__global__ void hello(){
    int idx = blockIdx.x;
    printf("Hello world! I'm a thread in block %d\n", idx);
}

hello<<<NUM_BLOCKS, BLOCK_SIZE>>>();
```

A ```for``` loop that is executed sequentially on a CPU is replaced by a kernel on a GPU which is run in parallel by independent threads organized into blocks. In CUDA a kernel is defined by the ```__global__``` prefix and it's called by the CPU as a regular function by the triple chevron syntax ```<<<...>>>```. In the above code there's a kernel ```hello``` which doesn't take any input parameters. Still, it's called with:

```
hello<<<NUM_BLOCKS, BLOCK_SIZE>>>();
```

The triple chevron launch syntax ```<<<NUM_BLOCKS, BLOCK_SIZE>>>``` contains the ''kernel launch parameters'':

- ```NUM_BLOCKS```: defines the number of blocks to use (in the above example 4);
- ```BLOCK_WIDTH```: defines the number of threads per block (in the above example 1);

Of course, the same parameters can be called in the following way:

```
hello<<<4, 1>>>();
```

What is crucial about the kernel execution on a GPU is that the blocks with threads are executed *in parallel*. So, what does the above kernel do in parallel? For every block index ```idx``` it tries to print the ''Hello world'' message in parallel, where the block index is taken from the built-in variable ```blockIdx.x```. Of course, the messages can't be printed in parallel but the blocks still run in parallel and which ever is faster it's printed before the slower ones. Try to execute the CUDA Hello world in the notebook for a couple of times to see which block indices are printed first. Is the order of block indices always the same or does it change with any new execution of the code?

![Hello_World_CUDA.ipynb](https://github.com/kosl/ihipp-examples/blob/master/GPU/Hello_World_CUDA.ipynb)

We can also run the ''Hello world'' example on a GPU in OpenCL. Let's give the solution straight again:

```
#define GLOBAl_SIZE 4
#define LOCAL_SIZE 1

__kernel void hello() {
    int gid = get_global_id(0);
    printf("Hello world! I'm a thread in block %d\n", gid);
}

size_t globalItemSize = GLOBAl_SIZE;
size_t localItemSize = LOCAL_SIZE;
cl_kernel kernel = clCreateKernel(program, "hello", &ret);
ret = clEnqueueNDRangeKernel(commandQueue, kernel, 1, NULL, &globalItemSize, &localItemSize, 0, NULL, NULL);
```

In the case of OpenCL a ```for``` loop (that is executed sequentially on a CPU) is replaced by a kernel on a GPU which is run in parallel by independent work–items organized into work–groups. This is just different terminology: in OpenCL the equivalent of a block is called a work–group, while the equivalent of a thread is a  work–item.  In OpenCL a kernel is defined by the ```__kernel ``` prefix and it's called by the CPU with the ```clEnqueueNDRangeKernel()``` function of the OpenCL API. In the above code there's also a kernel ```hello``` which doesn't take any input parameters, but it's still called with:

```
clEnqueueNDRangeKernel(commandQueue, kernel, 1, NULL, &globalItemSize, &localItemSize, 0, NULL, NULL);
```

This function of the OpenCL API contains the ''kernel launch parameters'':

- ```&globalItemSize```: defines the number of work–items times work–groups (in the above example 1 x 4 = 4);
- ```&localItemSize```: defines the number of work–items (in the above example 1);

So, the launch parameters of a kernel in OpenCL are a bit different than in CUDA. What one needs to pay attention to is that the ```globalItemSize``` must be divisible with the ```localItemSize```, otherwise the kernel execution will go into error. As in CUDA the kernel execution on a GPU in OpenCL means that the work-groups with work-items are executed *in parallel*. Try to figure out, what does the kernel in OpenCL
 do in parallel and if there's an equivalent of the block index ```idx``` for the work-group index in the OpenCL code. Try to execute the OpenCL Hello world in the notebook for a couple of times to see which indices are printed first. Is the order of indices always the same or does it change with any new execution of the code?

![Hello_World_OpenCL.ipynb](https://github.com/kosl/ihipp-examples/blob/master/GPU/Hello_World_OpenCL.ipynb)

Don't worry if you don't understand completely the codes above. We will explain everything in detail (including compiling of the codes) in the following steps.

## 5.8 Exer: Hello world extended on GPU


Modify the Hello world CUDA example from the previous step to complete the following tasks:

- define 2 blocks with 4 threads each;
- print the "Hello World" message to reflect also information on the thread number from each block (hint: use the built-in variable ```threadIdx.x```).

![Hello_World_CUDA_extended.ipynb](https://github.com/kosl/ihipp-examples/blob/master/GPU/Hello_World_CUDA_extended.ipynb)

Similarly, modify the Hello world OpenCL example from the previous step to complete the following tasks:

- define 2 blocks (work-groups) with 4 threads (work-items) each;
- print the "Hello World" message to reflect also information on the thread (work-item) number from each block (work-group) (hint: use the built-in variables ```get_group_id(0)``` for work-groups and ```get_local_id(0)``` for work-items).

![Hello_World_OpenCL_extended.ipynb](https://github.com/kosl/ihipp-examples/blob/master/GPU/Hello_World_OpenCL_extended.ipynb)

## 5.9 CUDA and OpenCL execution model

After exploring the GPU architecture and getting to know the principles of GPU programming we can abstract everything into a GPU execution model. Let's see how a GPU hardware architecture corresponds to the GPU programming paradigm. We will talk in terms of CUDA terminology but the same applies to OpenCL. We will present the equivalent OpenCL terminology at the end.

The GPU execution model uses the concept of a grid of thread blocks, where the multiple blocks in a grid map onto the multiple SMs, and each block contains multiple threads, mapping onto the cores in an SM. We can see this concept on the picture (source: NVIDIA) below.

![](images/Execution_Model.png?raw=true)

The term "device" is a general reference to the GPU, whereas the term "host" is reserved for the CPU. A scalar processor is often referred to a GPU "core".

So, when a GPU  kernel  is executed each thread block is assigned  to a SM. A maximum number of thread blocks can be assigned to a SM, depending  on GPU hardware resources. The  runtime  system  maintains  a  list  of  active blocks and  assigns new blocks to SMs when resources are freed or in other words: once a thread block is assigned to a SM the resources on it are reserved until the execution of all threads in the block is not finished. Each thread block execution is independent from another (no synchronization can be done among blocks). Threads in each block are divided into warps of consecutive threads (generally 32 on modern GPU architectures) and the scheduler selects warps for execution from the residing blocks in a SM. A warp executes one common set of instructions at a time and a GPU "core" (scalar processor) executes one thread in the warp.

Let's recap everything about the GPU CUDA threads hierarchy with some details:

- threads are organized into blocks: blocks can be 1D, 2D, 3D
- blocks are organized into a grid: grids can also be 1D, 2D, 3D
- each block or thread has a unique ID: ```.x```, ```.y```, ```.z``` are components in every dimension
- built-in variables for the CUDA threads hierarchy:
    - ```threadIdx```: thread coordinate inside the block
    - ```blockIdx```: block coordinate inside the grid
    - ```blockDim```: block dimension in thread units
    - ```gridDim```: grid dimension in block units

The picture below (source: nvidia.com) shows an example of a CUDA threads hierarchy with 2D blocks.

![](images/grid-of-thread-blocks.png?raw=true)

Using built-in variables we can define global thread indices that run in a kernel. For a 1D kernel we can define a global thread index ```idx``` in the following way:

```
int idx = blockIdx.x * blockDim.x + threadIdx.x;
```
Similarly, we can define global thread indices ```i``` and  ```j``` for a 2D kernel:

```
int i = blockDim.x * blockIdx.x + threadIdx.x;
int j = blockDim.y * blockIdx.y + threadIdx.y;
```

These indices are defined in a kernel as internal variables and can be used for thread related computing. We have already seen such an index in the Hello World CUDA example where the index was defined to just identify blocks:

```
int idx = blockIdx.x;
```

and later used to print the block ID number:

```
printf("Hello world! I'm a thread in block %d\n", idx);
```

You could instead define a global thread index ```gid```:

```
int gid = blockIdx.x * blockDim.x + threadIdx.x;
```

and print it with:

```
printf("Hello world! I'm a global thread index %d in hierarchy\n", gid);
```

Of course, the global thread index would run from 0 to ```NUM_BLOCKS * BLOCK_SIZE - 1``` if the ```hello``` kernel is invoked with:

```
hello<<<NUM_BLOCKS, BLOCK_SIZE>>>();
```

One should remember that the kernel on the GPU is run with all the threads defined by the launch parameters in the triple chevron synthax ```<<<...>>>``` but the calculation could be limited, e.g., with an ```if``` clause:

```
__global__ void hello(){
    int gid = blockIdx.x * blockDim.x + threadIdx.x;
    if(gid < N)
        printf("Hello world! I'm a global thread index %d in hierarchy\n", gid);
}
```

For example, if one sets ```N = 7``` the kernel invoked by:


```
hello<<<4, 2>>>();
```
would print global thread indices from 0 to 6 instead of the total 0 to 7 deployed by invoking the kernel. You can experiment yourself by changing the launch parameters and ```N```.

The GPU OpenCL work-items hierarchy is equivalent to the CUDA threads hierarchy except for terminology and some minor details:

- work-items are organized into work-groups
- the number of work-items can be specified in a work-group – this is called the local (work-group) size
- both work-items and work-groups can be 1D, 2D, 3D
- each work-item and work-group has a unique ID: ```(0)```, ```(1)```, ```(2)``` are components in every dimension
- built-in variables for the OpenCL work-items hierarchy:
    - ```get_local_id``` equivalent to ```threadIdx```
    - ```get_group_id``` equivalent to ```blockIdx```
    - ```get_local_size``` equivalent to ```blockDim```
    - ```get_global_id``` equivalent to ```blockIdx * blockDim + threadIdx```

The picture below (source: khronos.org) shows an example of an OpenCL work-items hierarchy with 2D work-groups (note that the equivalent of "grid" in OpenCL is called NDRange).

![](images/ndrange-work-items.png?raw=true)

As in CUDA we can use built-in variables in OpenCL to define global work-item indices that run in a kernel. For a 1D kernel we can define a global work-item index ```idx``` in the following way:

```
int idx = get_group_id(0) * get_local_size(0) + get_local_id(0)
```

This is of course unnecessary since OpenCL offers the ```get_global_id``` variable which returns a global work-item index:

```
int idx = get_global_id(0);
```

As in CUDA, we can define global work-item indices ```i``` and  ```j``` for a 2D kernel in OpenCL with:

```
int i = get_group_id(0) * get_local_size(0) + get_local_id(0)
int j = get_group_id(1) * get_local_size(1) + get_local_id(1)
```

or equivalently with:

```
int i = get_global_id(0);
int j = get_global_id(1);
```

As in CUDA, these indices are defined in a kernel as internal variables and can be used for work-items related computing in OpenCL. You can modify the Hello World OpenCL example to print the global work-item index and experiment with launch parameters along with an ```if``` clause in the kernel to limit the print out of indices.