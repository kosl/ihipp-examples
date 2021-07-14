# Week 5: Beyond OpenMP and MPI: GPU parallelisation 

## 5.1 V: Introduction

In this week we will go beyond classical parallelisation paradigms (like OpenMP and MPI) which are generally associated with CPUs. We will talk about Graphics Processing Units (GPUs) that were originally developed for executing graphical tasks (including rendering in computer games) but can also be used for general purpose computing in many fields. So, in the context of general purpose computing GPUs are referred to as accelerators for intensive computational tasks. The main advantage of GPUs over CPUs is greater computational capability and high-bandwidth memory, on the other hand GPUs are known for latency problems. Thus, efficient computing algorithms make use of the "best of both worlds" approach:

- GPUs are used for parallel tasks while CPUs for serial tasks;
- GPUs excel in throughput performance contrary to the CPUs which excel in low-latency access.

Computing acceleration can be achieved with:

- existing applications
- libraries
- directive based methods: OpenMP, OpenACC...
- special programming languages or extensions: CUDA, OpenCL...

In this week we shall briefly present OpenMP as a means for "off-loading" parallel tasks to GPUs and more thoroughly deal with two extensions to C for programming GPUs: CUDA and OpenCL. On one hand, GPU off-loading is simple to use, but on the other hand it's quite limited, contrary to GPU programming which requires more effort to use, but offers more flexibility.