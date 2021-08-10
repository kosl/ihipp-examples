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
__global__ void hello(int N){
    int gid = blockIdx.x * blockDim.x + threadIdx.x;
    if(gid < N)
        printf("Hello world! I'm a global thread index %d in hierarchy\n", gid);
}
```

For example, if one sets ```N = 7``` (note that ```N``` is an integer variable defined outside the kernel, hence it must be called as an input parameter in a function like manner) the kernel invoked by:


```
int N = 7;
hello<<<4, 2>>>(N);
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

## 5.10 E: Vector addition on GPU

A standard introductory example for GPU computing is vector addition. We will first show how it is done on a CPU and then on a GPU. In the next two steps we will use this example to present a step-by-step approach to GPU programming, both in CUDA and OpenCL.

Vector addition on a CPU can be done with a ```for``` loop. Each iteration computes the sum of one component of vectors ```a``` and  ```b```. The vector sum is stored in ```out```.

```
for(int i = 0; i < N; i++){
    out[i] = a[i] + b[i];
}
```

You can have a look at the program for vector addition in C and execute it:

![Vector_addition_C.ipynb](https://github.com/kosl/ihipp-examples/blob/master/GPU/Vector_addition_C.ipynb)

By now we should know how to transform this ```for``` loop into a GPU kernel. The only difference is that the kernel in this case will take some extra parameters, i.e., the vectors ```a```, ```b```, ```out``` and the vector size ```n```. Let's write down the CUDA kernel first:

```
__global__ void vector_add(double *out, double *a, double *b, int n)
{
    int i = blockIdx.x * blockDim.x + threadIdx.x;
    if(i < n)
        out[i] = a[i] + b[i];
}
```

You can see that the input parameters for the kernel ```vector_add``` are defined in a function like manner and that the index ```i``` defined inside the kernel represents the global thread index. In that way the kernel sums the vector components in parallel (keep in mind that this is true if enough resources on the GPU are available): for every component addition there's a thread which takes care of the computing task, while the ```if``` clause makes sure that the calculations are done only within the vector size. We will see in the next step how the kernel is called and the parameters or variables must be defined.

For the same task we can use an OpenCL kernel instead:

```
__kernel void vector_add(__global double *a, __global double *b, __global double *out, int n) {
    int i = get_global_id(0);
    if(i < n)
        out[i] = a[i] + b[i];
}
```

You can see that the kernel looks basically the same, except for variable type prefixes and built-in variables. In the next steps we will also see how the kernel in OpenCL is called and how the parameters or variables must be defined.

If you are curious how the codes for vector addition on GPU look like, you can have look, for the CUDA version:

![Vector_addition_CUDA.ipynb](https://github.com/kosl/ihipp-examples/blob/master/GPU/Vector_addition_CUDA.ipynb)

and the OpenCL version:

![Vector_addition_OpenCL.ipynb](https://github.com/kosl/ihipp-examples/blob/master/GPU/Vector_addition_OpenCL.ipynb)

Don't be afraid if you find them difficult to grasp, we will explore and explain them in a step-by-step fashion in the next steps.

## 5.11 CUDA step-by-step

In this step we will explain in detail the vector addition in CUDA, which is a typical GPU program in CUDA. A typical CUDA program flow consists of the following steps:

- Allocate GPU memory
- Populate GPU memory with inputs from the host (CPU)
- Execute a GPU kernel on those inputs
- Transfer outputs from the GPU back to the host (CPU)
- Free GPU memory

It has to be mentioned that recent NVIDIA GPUs (Pascal microarchitecture or newer) support unified memory (invoked with ```cudaMallocManaged()```) in a single-pointer-to-data model meaning CPUs and GPUs can use the same memory address space. Consequently, transfers from/to GPU memory are no longer needed or at least less important in a GPU accelerated code.

Let's analyze the CUDA vector addition code:

![Vector_addition_CUDA.ipynb](https://github.com/kosl/ihipp-examples/blob/master/GPU/Vector_addition_CUDA.ipynb)

step-by step and explain how to compile it into an executable program.

1. Initialize device

The first available CUDA device (GPU) is automatically initialized to ```0```, but you could still set it yourself by:

```
CudaSetDevice(0);
```

Such initialization is important in multi GPU systems where there's a need for switching from one device to another, e.g., switching to device ```1``` can be done with:

```
CudaSetDevice(1);
```

It's a good approach to initialize CUDA through the ```CUDA_ERROR()``` API call:

```
CUDA_ERROR(cudaSetDevice(0));
```

In this way a CUDA program will continue with execution only if a CUDA capable device is available. Sometimes it's useful to get the device properties through ```cudaGetDeviceProperties()``` by:

```
cudaDeviceProp prop;
CUDA_ERROR(cudaGetDeviceProperties(&prop,0));
printf("Found GPU '%s' with %g GB of global memory, max %d threads per
       block, and %d multiprocessors\n", prop.name,
       prop.totalGlobalMem/(1024.0*1024.0*1024.0),
       prop.maxThreadsPerBlock,prop.multiProcessorCount);
```

All the above calls are optional but it's a good approach to control CUDA initialization to avoid running GPU accelerated codes on unresponsive GPUs. Older CUDA versions also needed the inclusion of CUDA specific headers, e.g.:

```
#include <cuda.h>
#include <cuda_runtime.h>
#include <device_launch_parameters.h>
```

what is now redundant. Still, you can put this lines at the beginning of CUDA codes to no harm.

2. Allocate GPU memory

Memory allocation on the device is done with ```cudaMalloc()```:

```
cudaMalloc((void**)&d_a, sizeof(double) * N);
cudaMalloc((void**)&d_b, sizeof(double) * N);
cudaMalloc((void**)&d_out, sizeof(double) * N);
```

For every variable on the host (CPU) from which or to which GPU memory transfers will be done we must allocate memory on the GPU of the same size and type.

It's also a good approach to use "d" for the variables in GPU memory as a indication for device, e.g., ```d_a``` or ```a_d```. This naming convention is optional but quite useful in terms of code readability.

3. Transfer data from host to device memory

Data transfer from host (CPU) to device (GPU) is done with ```cudaMemcpy()``` and the option ```cudaMemcpyHostToDevice```. In the example of vector addition we have to transfer data from host variables ```a``` and ```b``` to device variables ```d_a``` and ```d_b```:

```
cudaMemcpy(d_a, a, sizeof(double) * N, cudaMemcpyHostToDevice);
cudaMemcpy(d_b, b, sizeof(double) * N, cudaMemcpyHostToDevice);
```

Basically, we transfer the values of the components of vectors ```a``` and ```b``` from host do device memory. Note, that host and device variables must be of same size and type.

4. Execute kernel on device variables as inputs

After transfering the components of vectors ```a``` and ```b``` from host do device memory we can sum the vector components in parallel on the GPU. In the previous step we have already shown how to do that, i.e., with the kernel ```vector_add```:

```
__global__ void vector_add(double *out, double *a, double *b, int n)
{
    int i = blockIdx.x * blockDim.x + threadIdx.x;
    if(i < n)
        out[i] = a[i] + b[i];
}
```

Before executing the kernel we have to define launch parameters, i.e., the number of threads per block and the number of blocks. We need at least 2020 threads in total. Choosing the 1024 as the number of threads per block we need 2020/1024 = 1.97 blocks or 2 blocks rounded. We can do this calculation with:

```
int threadsPerBlock = 1024;
int blocksPerGrid = N/threadsPerBlock + (N % threadsPerBlock == 0 ? 0:1);
```

or alternatively with:

```
int threadsPerBlock = 1024;
int blocksPerGrid =(N + threadsPerBlock - 1) / threadsPerBlock;
```

Now we can launch the kernel with these parameters:

```
vector_add<<<blocksPerGrid, threadsPerBlock>>>(d_out, d_a, d_b, N);
```

Note that we launched the kernel with the allocated device variables ```d_out```, ```d_a``` and ```d_b``` as is usuallly done with function calls. Note also that integers and constant type variables can be passed to the kernel without device memory allocation. In this case we passed the vector size ```N``` in this way.

5. Transfer data back from device to host

The kernel ```vector_add``` calculates the vector sum of ```d_a``` and ```d_b``` and puts it into the variable ```d_out```. This variable with the vector sum resides in GPU global memory and cannot be accessed by the CPU directly, hence it has to be transferred back to host memory to the variable ```out```. This is done again with ```cudaMemcpy()``` except that now the option used is ```cudaMemcpyDeviceToHost```:

```
cudaMemcpy(out, d_out, sizeof(double) * N, cudaMemcpyDeviceToHost);
```

Again, the counterpart host variable ```out``` must be of the same size and type as the device variable ```d_out```.

6. Deallocate (free) device memory

In the end (after the device variables are not needed any more) the allocated device memory can be freed:

```
cudaFree(d_a);
cudaFree(d_b);
cudaFree(d_out);
```

7. Compiling the code

CUDA codes reside in ```*.cu``` files and the NVIDIA CUDA (nvcc) compiler can be used to compile them, e.g., in the case of the vector addition CUDA code:

```
!nvcc -o vector_add_cuda vector_add_cuda.cu
```

The executable can be run with:

```
!./vector_add_cuda
```

Hardware design, number of cores, cache size, and supported arithmetic instructions are different for different GPU models. Every NVIDIA GPU supports a compute capability according to its microarchitecture, e.g., the Tesla V100 (Volta microarchitecture) supports CUDA compute capabilities up to 7.0 (see the output in Step 5.3). The above code can be compiled specifically for the V100 in the following way:

```
!nvcc -arch=sm_70 -gencode=arch=compute_70,code=sm_70 -o vector_add_cuda vector_add_cuda.cu
```

You can compile and run the CUDA vector addition code in the notebook. Check the output to see if the GPU calculates the vector sum correctly.

## 5.12 OpenCL step-by-step

In this step we will explain in detail the vector addition also in OpenCL. A typical OpenCL program flow basically consists of the same steps as a CUDA program flow, but you will notice that OpenCL is a more low level programming extension with many calls to the OpenCL API. OpenCL, like CUDA, can also offer shared memory (Shared Virtual Memory) for host and device kernels, thus eliminating costly data transfers between host and device, but this feature is supported only in OpenCL 2.0 and above. Unfortunately, as already mentioned, the NVIDIA GPUs support only OpenCL 1.2 and such features are not available. Also for that reason we will follow this standard to explain GPU accelerated programming in OpenCL.

Let's also analyze the OpenCL vector addition code:

![Vector_addition_OpenCL.ipynb](https://github.com/kosl/ihipp-examples/blob/master/GPU/Vector_addition_OpenCL.ipynb)

step-by step and explain how to compile it into an executable program.

1. Initialize device

As opposed to CUDA a specific OpenCL header must be included at the beginning of the code, depending on the operating system:

```
#ifdef __APPLE__
#include <OpenCL/opencl.h>
#else
#include <CL/cl.h>
#endif
```

Before initializing the device it's necessary to get platform and device information; this is more or less boiler-plate code that you can copy/paste it to every OpenCL code. Device initialization consists of the following steps:

- declare context:

cl_context context = clCreateContext(NULL, 1, &device_id, NULL, NULL, &ret);

- choose a device from context:

ret = clGetDeviceIDs(platform_id, CL_DEVICE_TYPE_ALL, 1, &device_id, &ret_num_devices);

- create a command queue with device and context:

cl_command_queue command_queue = clCreateCommandQueue(context, device_id, 0, &ret);

This is still more or less boiler-plate code which is basically the same for every OpenCL program.

2. Create buffers and memory transfer device

Next we create buffers which is essentialy memory allocation on the GPU:

```
cl_mem a_mem_obj = clCreateBuffer(context, CL_MEM_READ_ONLY, N * sizeof(double), NULL, &ret);
cl_mem b_mem_obj = clCreateBuffer(context, CL_MEM_READ_ONLY, N * sizeof(double), NULL, &ret);
cl_mem out_mem_obj = clCreateBuffer(context, CL_MEM_WRITE_ONLY, N * sizeof(double), NULL, &ret);
```

Notice, that we used the flag ```CL_MEM_READ_ONLY``` to create buffers for vectors ```a``` and ```b``` since the GPU kernel will only read these data. The vector sum will be stored in the buffer ```out_mem_obj``` and the GPU kernel will only write to it, hence the use of the ```CL_MEM_WRITE_ONLY``` flag. If there's the need of both reading from and writing to memory buffers one could use the flag ```CL_MEM_READ_WRITE```.

After buffer creation we can transfer host data to the device. Transfering the host variables ```a``` and ```b``` to GPU memory buffers ```a_mem_obj``` and ```b_mem_obj``` is done with the following calls:

```
ret = clEnqueueWriteBuffer(command_queue, a_mem_obj, CL_TRUE, 0, N * sizeof(double), a, 0, NULL, NULL);
ret = clEnqueueWriteBuffer(command_queue, b_mem_obj, CL_TRUE, 0, N * sizeof(double), b, 0, NULL, NULL);
```

As in CUDA the size and the type of the memory buffers of the device variables must be the same as for the host counterparts, in this case: ```N * sizeof(double)```.

3. Build program and select kernel

You have probably noticed that the kernel source was loaded in the beginning with:

```
FILE *fp;
char *source_str;
size_t source_size;

fp = fopen("vector_add.cl", "r");
if (!fp) {
    fprintf(stderr, "Failed to load kernel.\n");
    exit(1);
}
source_str = (char*)malloc(MAX_SOURCE_SIZE);
source_size = fread( source_str, 1, MAX_SOURCE_SIZE, fp);
fclose( fp );
```

These lines basically load the OpenCL kernel ```vector_add``` for vector addition (shown in Step 5.10):

```
__kernel void vector_add(__global double *a, __global double *b, __global double *out, int n) {
    int i = get_global_id(0);
    if(i < n)
        out[i] = a[i] + b[i];
}
```

as a string from the file ```vector_add.cl```. It's common practice in OpenCL programming to have kernels in ```*.cl``` files but one could also define them in the main code as plain strings.

With kernel source loaded we can create a program from it:

```
cl_program program = clCreateProgramWithSource(context, 1, (const char **)&source_str, (const size_t *)&source_size, &ret);
```

build the program:

```
ret = clBuildProgram(program, 1, &device_id, NULL, NULL, NULL);
```

and create the OpenCL kernel:

```
cl_kernel kernel = clCreateKernel(program, "vector_add", &ret);
```

Notice the constant use of the variable ```ret``` of the ```cl_int``` type defined at beginning. This variable accepts return values for the OpenCL API. As said before you can use many of the OpenCL API calls as boiler-plate code as long as you are consistent with the variables definitions in these calls.

4. Set arguments and enqueue kernel

After the creation of the OpenCL kernel we have first to set arguments for it, in the example of vector addition with:

```
ret = clSetKernelArg(kernel, 0, sizeof(cl_mem), (void *)&a_mem_obj);
ret = clSetKernelArg(kernel, 1, sizeof(cl_mem), (void *)&b_mem_obj);
ret = clSetKernelArg(kernel, 2, sizeof(cl_mem), (void *)&out_mem_obj);
ret = clSetKernelArg(kernel, 3, sizeof(cl_int), (void *)&n);
```

It's important that these arguments follow the same order (indices from 0 to 3) as in the kernel definition:

```
vector_add(__global double *a, __global double *b, __global double *out, int n)
```

Notice, that integer variable, e.g. ```n``` in this case, do not need the creation of a memory buffer but still need to be set as a kernel argument.

Next, we must set local and global work-group sizes:

```
size_t local_item_size = 1024;
int n_blocks = n/local_item_size + (n % local_item_size == 0 ? 0:1);
size_t global_item_size = n_blocks * local_item_size;
```

This is equivalent to setting the number of threads per block and the number of blocks per grid in CUDA.

Finally, we execute the kernel with:

```
ret = clEnqueueNDRangeKernel(command_queue, kernel, 1, NULL, &global_item_size, &local_item_size, 0, NULL, NULL);
```

You will notice that the execution of a kernel in OpenCL is different than in CUDA. The main difference is that the kernel in OpenCL is not called in a function-like manner, i.e., with passing arguments to it. In OpenCL the arguments of a kernel are set with the ```clSetKernelArg()``` API function before the kernel is executed. On the other hand, launch parameters for the kernel, i.e., ```global_item_size``` and ```local_item_size``` are set at kernel execution, as in CUDA.

5. Transfer back results

The kernel ```vector_add``` calculates the vector sum of ```a_mem_obj``` and ```b_mem_obj``` and puts it into the memory buffer ```out_mem_obj```. As in CUDA, this vector sum resides in GPU global memory and cannot be accessed by the CPU directly, hence it has to be transferred back to host memory to the variable ```out```. The transfer is done with:

```
ret = clEnqueueReadBuffer(command_queue, out_mem_obj, CL_TRUE, 0, N * sizeof(double), out, 0, NULL, NULL);
```
6. Free buffers and resources

In the end the memory buffers can be freed:

```
ret = clReleaseMemObject(a_mem_obj);
ret = clReleaseMemObject(b_mem_obj);
ret = clReleaseMemObject(out_mem_obj);
```

as well as other resources (this is again more or less boiler-plate code):

```
ret = clFlush(command_queue);
ret = clFinish(command_queue);
ret = clReleaseKernel(kernel);
ret = clReleaseProgram(program);
ret = clReleaseCommandQueue(command_queue);
ret = clReleaseContext(context);
```

7. Compiling the code

OpenCL codes reside in *.c files (main code) and *.cl files (kernels). Compilers that can link to the OpenCL library (generally with the flag ```-lOpenCL```) can be used, e.g., gcc or nvcc. One should be aware that for running OpenCL codes on a GPU a Software Developer Kit (SDK) for it must be installed. For NVIDIA GPUs the installation of the CUDA SDK is generally enough and compiling can be done with:

```
!nvcc -o vector_add_opencl vector_add_opencl.c -lOpenCL
```

For non-NVIDIA GPUs or CPUs one could compile the code with, e.g.:

```
!gcc -o vector_add_opencl vector_add_opencl.c -lOpenCL
```

Of course, OpenCL drivers for the hardware must be installed, generally as implementations for OpenCL called Installable Client Drivers (ICDs).

As before you can compile and run the OpenCL vector addition code in the notebook. Check again the output to see if the GPU calculates the vector sum correctly.

## 5.13 CUDA and OpenCL comparison

To sum up we will give a side by side comparison of both the GPU programming models discussed so far. We haven't presented everything of what you will find in the comparison tables, some things we will discuss in the final example in the following steps of this week, for other undiscussed things you can have a look at documentations for CUDA and OpenCL.

### Execution model terminology

| CUDA | OpenCL |
| :---------------------------: | :---------------: |
| SM (Streaming Multiprocessor) | CU (Compute Unit) |
| thread | work-item |
| block | work-group |
| global memory | global memory |
| constant memory | constant memory |
| shared memory | local memory |
| local memory | private memory |

### Function, variable and built-in variable types

| CUDA | OpenCL |
| :-----------------------------: | :---------------: |
| `__global__ function` | `__kernel function` |
| `__device__ function`   | `function` |
| `__constant__ variable` | `__constant variable` |
| `__device__ variable` | `__global variable` |
| `__shared__ variable` | `__local variable` |
| `gridDim` | `get_num_groups()` |
| `blockDim` | `get_local_size()` |
| `blockIdx` | `get_group_id()` |
| `threadIdx` | `get_local_id()` |
| `blockIdx * blockDim + threadIdx` | `get_global_id()` |
| `gridDim * blockDim` | `get_global_size()` |

### Kernel synchronization

| CUDA | OpenCL |
| :------------------: | :---------------: |
| `__syncthreads()` | `barrier()` |
| `__threadfence()` | / |
| `__threadfence_block()` | `mem_fence()` |
| / | `read_mem_fence()` |
| / | `write_mem_fence()` |

### API calls

| CUDA | OpenCL |
| :-----------------------: | :---------------: |
| `cudaGetDeviceProperties()` | `clGetDeviceInfo()` |
| `cudaMalloc()` | `clCreateBuffer()` |
| `cudaMemcpy()` | `clEnqueueReadBuffer()`, `clEnqueueWriteBuffer()` |
| `cudaFree()` | `clReleaseMemObj()` |
| `kernel<<<...>>>()` | `clEnqueueNDRangeKernel()` |

## 5.14 Quiz: CUDA and OpenCL programming and execution models

## 5.15 Numerical integration: Riemann sum with trapeziums

We are ready for a somewhat more complex, yet still a fairly school example in numerical computation, to show some extra features of GPU computing: Riemann sum for numerical integration. But first we will show how it's done on a CPU and after that think of how can we parallelize it on the GPU with CUDA and OpenCL. As an excursus in between we will also parallelize the CPU version with OpenMP and show how to off-load the computation on GPU with OpenMP, as well.

Approximation of a definite integral of a function can be done using the trapezium rule. The area under the function on the interval from a to b, which represents the definite integral, is divided into N trapeziums. The area of each trapezium is equal to the median of the trapezium `(f(x+h)+f(x))/2` multiplied with the sub-interval width `(b-a)/N`. The sum of all trapezium areas is an approximation of the definite integral of the function from a to b. For simplicity we choose `a = 0` and `b = 1` to calculate the normal distribution function from 0 to 1 which is equal to 0.341345.

How can we do this example on the CPU? The simplest approach is, of course, using a `for` loop to calculate trapezium medians and trapezium sums:

```
double riemann(int n)
{
    double sum = 0;
    for(int i = 0; i < n; ++i)
    {
        double x = (double) i / (double) n;

        double fx = (exp(-x * x / 2.0) + exp(-(x + 1 / (double)n) * (x + 1 / (double)n) / 2.0)) / 2.0;
        sum += fx;
    }

    sum *= (1.0 / sqrt(2.0 * M_PI)) / (double) n;
    return sum;
}
```

Notice, that in the code above we calculate trapezium medians for every sub-interval and add them to the `sum` variable at every iteration. In the end we multiply this sum of trapezium medians with `(1.0 / sqrt(2.0 * M_PI)) / (double) n` to obtain the Riemann sum. The term `1.0 / (double) n` is in fact the height of the trapezium `(b-a)/n` and is the same for every trapezium since the sub-interval width is the same and we have chosen `a = 0` and `b = 1`.

The whole Riemann sum CPU code can be found in this notebook:

![Riemann_sum_C.ipynb](https://github.com/kosl/ihipp-examples/blob/master/GPU/Riemann_sum_C.ipynb)

If you compile the code for `N` equal to 1 billion, i.e.:

```
#define N 1000000000
```

without optimization the calculation of the Riemann sum will take about 90 s. With the `-O3` optimization level flag the calculation with the compiled code will take less than half of the time, about 40 s.

But can we do better, e.g., with some parallelization approach like OpenMP? We shall see the answer in the next step.

## 5.16 Exer: Riemann sum with OpenMP

In Week 2 you have learned how to use OpenMP to parallelize parts of the code to gain speed up of execution. In this exercise you will use this knowledge and try to speed up the calculation of the Riemann sum C code from the previous step.

Complete the following tasks:

- use OpenMP to parallelize the `for` loop in the Riemann sum C code from the previous step
- execute the code for the maximum threads available on the CPU (hint: use `!lscpu` to get information on the CPU)

Did you succeed to gain any speed up with the use of OpenMP? Leave a comment with your findings.

If you have any troubles to modify the code or compile it you can have a look at the solution given in the notebook below:

![Riemann_sum_OpenMP.ipynb](https://github.com/kosl/ihipp-examples/blob/master/GPU/Riemann_sum_OpenMP.ipynb)

## 5.17 OpenMP off-loading to GPU for Riemann sum

OpenMP is an example of a directive based method which can be used to off-load computation intensive tasks to GPUs. From OpenMP 4.0 on new device constructs have been added to support this. As in CUDA or OpenCL the execution model relies on the host on which the OpenMP program begins execution and then off-loads tasks or data to a target
device, e.g., GPU.

The main OpenMP device constructs are:

- the `target` and
- the `teams` construct.

By defining a `target` construct a new target task is generated. When the latter starts, the enclosed target region is executed by an initial thread running sequentially on a target device if it's available and supported. If not all target regions associated with the device are executed on the host. The `teams` construct generates a league of thread teams where the master thread of each team executes the region sequentially as shown on the picture below (source: OpenMP Accelerator Model, IWOMP 2016).

![](images/OpenMP_execution_model.png?raw=true)

Some important OpenMP 4.x device constructs are listed in the following table:

| Device construct | Description |
| ------------------------- | -------------------------------------------------------------------------------- |
| `#pragma omp target` | Map variables to a device data environment and execute the construct on the device. |
| `#pragma omp target data` | Creates a data environment for the extent of the region. |
| `#pragma omp target` | Map variables to a device data environment and execute the construct on the device. |
| `#pragma omp declare target` |  A declarative directive that specifies that variables and functions are mapped to a device. |
| `#pragma omp teams` | Creates a league of thread teams where the master thread of each team executes the region. |
| `#pragma omp distribute` | Specifies loops which are executed by the thread teams. |
| `#pragma omp ... simd` | Specifies code that is executed concurrently using SIMD instructions. |
| `#pragma omp distribute parallel for` | Specifies a loop that can be executed in parallel by multiple threads that are members of multiple teams. |

So, how can we off-load the computation of the Riemann sum to the GPU using OpenMP? We start from the OpenMP directive in the previous exercise. If you have completed it successfully then you should have come to a solution something like:

```
double riemann(int n)
{
  double sum = 0;
  
  #pragma omp parallel for reduction(+:sum)
  for(int i = 0; i < n; ++i)
  {
    double x = (double) i / (double) n;
    sum += (exp(-x * x / 2.0) + exp(-(x + 1 / (double)n) * (x + 1 / (double)n) / 2.0)) / 2.0;
  }

  sum *= (1.0 / sqrt(2.0 * M_PI)) / (double) n;

  return sum;
}
```

We just have to add appropriate device constructs to enable off-loading to a GPU:

```
double riemann(int n)
{
  double sum = 0;
  
  #pragma omp target teams distribute parallel for simd map(tofrom: sum) map(to: n) reduction(+:sum)
  for(int i = 0; i < n; ++i)
  {
    double x = (double) i / (double) n;
    sum += (exp(-x * x / 2.0) + exp(-(x + 1 / (double)n) * (x + 1 / (double)n) / 2.0)) / 2.0;
  }
 
  sum *= (1.0 / sqrt(2.0 * M_PI)) / (double) n;
 
  return sum;
}
```

Here `map` is used to copy data from the host to the device and vice versa, e.g., `map(tofrom: sum)` copies the variable `sum` to the device (GPU) and after computation back to the host (CPU), while `map(to: n)` just copies the variable `n` to the device.

Such OpenMP off-loading to the GPU results in speed up greater than in typical many threads OpenMP execution on the host and is quite close to classical GPU acceleration with CUDA or OpenCL, provided the device (GPU) is supported and compilers can build programs with OpenMP off-load.