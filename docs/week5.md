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

On the figure below you can observe schematics of both CPU and GPU hardware architectures. From the schematics it is evident that:

- a GPU has many more arithmetic logic units or ALUs (green rectangles) than a CPU;
- a GPU can control simple, highly parallel workloads well (there's a yellow rectangle for every row of green rectangles), contrary to a CPU which can control more complex workloads;
- a core (green rectangle) in a CPU is different than a "core" or ALU (green rectangle) in a GPU: the former is comprised by ALUs and FPUs which are more specialized than ALUs in a GPU;
- a CPU has more cache memory than a GPU.

[Figure: CPU vs GPU architecture]

It has to be noted that the term "GPU core" is more or less a marketing term. The equivalent of a CPU core in a GPU is a streaming multiprocessor (SM) with many ALUs or "cores".

## 5.3 E: Consumer grade vs. high-end GPUs

Nowadays, desktop PCs or laptops are standardly equipped with a GPU, either integrated or as a standalone card. But how such GPUs differ from GPUs dedicated to computing, e.g., on supercomputers (HPC clusters)?

First, let's have a look at the GPUs (NVIDIA Tesla V100-SXM2-16GB) that are installed on the Marconi-100 cluster (currently #14 on the Top500 list of supercomputers in the world). By invoking the utilities ```deviceQuery``` and ```bandwidthTest``` in the terminal of the login node we can get:

Output (excerpt) from ```deviceQuery```:

```
Total amount of global memory:
16128 MBytes (16911433728 bytes)
(80) Multiprocessors, (64) CUDA Cores/MP:
5120 CUDA Cores
GPU Max Clock rate: 1530 MHz (1.53 GHz)
Memory Bus Width: 4096-bit
L2 Cache Size: 6291456 bytes
```
Output (excerpt) from ```bandwidthTest```:

```
Device to Device Bandwidth, 1 Device(s)
Transfer Size (Bytes) Bandwidth(GB/s)
32000000              713.5
```

If we do the same on a consumer grade laptop (assuming it is equipped with a standalone GPU by NVIDIA), we get, e.g.:

Output (excerpt) from ```deviceQuery```:

```
Total amount of global memory:
2004 MBytes (2101870592 bytes)
(3) Multiprocessors, (128) CUDA Cores/MP:
384 CUDA Cores
GPU Max Clock rate: 1020 MHz (1.02 GHz)
Memory Bus Width: 64-bit
L2 Cache Size: 1048576 bytes
```

Output (excerpt) from ```bandwidthTest```:

```
Device to Device Bandwidth, 1 Device(s)
Transfer Size (Bytes) Bandwidth(MB/s)
33554432              13193.8
```

We can see that a professional high-end card has much more global memory, Streaming Multiprocessors (SMs) and "cores" available and also much higher memory bandwidth than a consumer grade card (in the example above: NVIDIA GeForce 930MX). The V100 has also a much higher theoretical throughput of 15.7 TFlops (for FP32) than the GeForce 930MX with throughput of 0.765 TFlops (for FP32). In short, both cards share the same technology but consumer grade ones are quite inferior in terms of hardware resources. Of course, there are some other differences (like the underlying microarchitecture), but both can be used for GPU computing albeit with a big difference in performance. To be completely frank there also exist gaming cards with better performance, even somewhat comparable to professional cards, but we won't go into details of why they are not used in HPC systems or data centers.

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

- execute the diagnostic programs to determine the main characteristics of the GPU (No. of SMs,
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