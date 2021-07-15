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

As we already pointed out, GPUs were originally designed to accelerate graphics. They excel at texturing, shading and rendering graphical primitives which comprise a 3D graphical object. The main characteristic of these primitives is that they are independent or, in other words, they can be processed independently in a parallel fashion. Thus, GPU acceleration of graphics was designed as an execution of inherently parallel tasks. On the other hand, CPUs are designed to execute the logical flow of any general-purpose program, where many parallel tasks may not be involved. These different design principles reflect the fact that GPUs have many more processing units and higher memory bandwidth, while CPUs are characterized by more specialized processing of instructions and faster clock speed rates.

On the figure below you can observe schematics of both CPU and GPU hardware architectures. From the schematics it is evident that:

- a GPU has many more arithmetic logic units or ALUs (green boxes) than a CPU;
- a GPU can control simple, highly parallel workloads well (a yellow box for every row of green compute boxes), contrary to a CPU which can control more complex workloads;
- a core in a CPU is different than a "core" or ALU in a GPU: the former is comprised by ALUs and FPUs which are more specialized than ALUs in a GPU;
- a CPU has more cache memory than a GPU.

[Figure: CPU vs GPU architecture]

It has to be noted that the term "GPU core" is more or less a marketing term. The equivalent of a CPU core in a GPU is a streaming multiprocessor (SM) with many ALUs or "cores".