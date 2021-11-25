# Introduction to parallel programming

## A->V:Intro to parallel programming
### V: Intro to Week 1, Serial vs Parallel

In this week we will introduce you to the basic principles and paradigms of parallel programming. We will not go deeply into each topic, the next weeks will be dedicated to that, even to some advanced topics in parallel programming. But even with the advanced topics we will briefly describe just what it is important to know and to give you a starting point where to learn more so that at some point you will be able to do your own coding.

There are many scientific and engineering challenges that can be tackled by the area of computing. In general we have two views on it. One is distributed serial computing, which means that you have many problems to solve and you don't care about time. The other is parallel computing where the problem needs to be divided into many compute cores or nodes, essentially many computers, because it is too big to fit into one computer or one computer would be too slow to solve it. The first approach is often called grid computing, while the opposite of it or the second approach is generally referred to supercomputing where you need a supercomputer to solve your problem. You probably also heard of cloud computing and similar, which is a commercial version of grid or supercomputing resources.

If you are a serious user, you will quickly find out that, if we use an analogy, buying a car is cheaper than renting it on the long term, so there will never be a commercial offering that will match individual purchases for the machine that is usually 90 or 100 percent utilized. So it's not like buying a car for fun and you have spent for it a lot. Supercomputers are usually very heavily utilized, meaning that during its lifetime, the computer operates near peak performance.

Parallel computing cannot be done better on a single machine or many single machines, since the program is usually written for serial execution on one processor. You have to divide the problem into separate commands (with one command at a time executed on one CPU) that are done in parallel or in other words: a serial execution in parallel.

![](https://raw.githubusercontent.com/kosl/ihipp-examples/master/docs/images/W1_parallelization.png)

There are different approaches or programming models that were developed during the years and they are still being developed. Along with the languages that might help you to resolve some of the issues of the hardware, for parallel computing is also essential the underlying hardware topology that we see usually as a combination of memory and CPUs. In the past, there were just a single processor and memory per node, and many of those nodes were combined together to make a cluster. In the recent years a cluster of compute nodes, so called "Beowulf", is being upgraded with many cores per node and shared memory. The cores share a memory, there can also be many sockets. The programming model for such a hardware architecture is a combination of languages. We have, e.g., OpenMP, a parallelization that can be easily done on a single computer, whether this is your PC laptop or a remote computer. This is quite an easy approach to do "automatic" parallelization. It means that you will start with a serial program and upgrade it with the command directives. The result is multi-threaded code that runs faster. We will introduce OpenMP in this week, while in Week 2 we will present it in detail.

### D: What team are you on?

We will introduce you to parallel programming with the use of some programming languages. Tell us which programming language(s) you use or know about or what language are you planning to learn.

###  E: Hello World!

As already mentioned, the simplest approach to parallelization is Open Multi-Processing (OpenMP). We will show you this paradigm through a "Hello World!" example in two programming languages: **C and Fortran**.

Let's assume, we want to parallelize the "Hello World!" print statement in C:

~~~c
printf("Hello World!\n");
~~~

and in Fortran:

~~~fortran
PRINT *, "Hello World!"
~~~

We can do that with the **parallel** construct which forms a team of threads and starts parallel execution. In C the construct looks like:

~~~c
#pragma omp parallel num_threads(2)
  {
    printf("Hello World!\n");
  }
~~~

Here `#pragma omp` indicates the OpenMP executable directive, `parallel` the construct and `num_threads(2)` the number of threads to be used. This directive is applied to the succeeding structured block of executable statements between `{...}`. In our case the executable statement is the "Hello World!" print statement.

In Fortran the construct looks like:

~~~fortran
!$OMP PARALLEL num_threads(2)

    PRINT *, "Hello World!"

!$OMP END PARALLEL
~~~

Similarly to C, `!$OMP` indicates the OpenMP executable directive, `PARALLEL` the construct and `num_threads(2)` the number of threads to be used. This directive is applied to the succeeding structured block of executable statements with a single entry at the top and a single exit at the bottom. As before, the executable statement is the "Hello World!" print statement.

First, have a look at the notebook with both codes in C and Fortran. Notice the C headers that must be included and the `USE OMP_LIB` line of code in Fortran to provide OpenMP functionality. Compilation of the codes will be explained later, so don't worry about this detail for now.

Run both codes in the notebook:

[Hello_world_OpenMP.ipynb](https://github.com/kosl/ihipp-examples/blob/master/OpenMP/Hello_world_OpenMP.ipynb)

Are the outputs as you expected?

### A->V: Architectures and memory models

Over the years there were different multi node approaches to parallelization. The only really interesting system was Message Passing Interface (MPI), which we will introduce in this week and present in detail in Week 3. Contrary to "automatic" parallelization in OpenMP, in MPI manual parallelization is needed. A combination of both approaches (hybrid model with OpenMP and MPI) can actually be done in a very simple way to gain a bit of performance regarding memory or CPU utilisation. Latest hardware architectures have non-uniform memory access (NUMA), hence memory regarding the cores is not symmetric but mostly asymmetric.

![](https://raw.githubusercontent.com/kosl/ihipp-examples/master/docs/images/W1_hybrid_OpenMP_MPI.png)

The parallel computing approach tends to use as many computing cores as possible for parallel code execution. The ideal is 100% parallel utilisation which can be achieved only for embarassingly simple parallel problems, i.e, parallel processing of the same subproblems on multiple processors.

![](https://raw.githubusercontent.com/kosl/ihipp-examples/master/docs/images/W1_embarassingly_simple.png)

Such kind of computing is actually not considered High Performance Computing (HPC). You have many other solutions, e.g., grid computing that is usually distributed and cloud computing that you can rent. Such problems that are being solved are not actually interdependent, so the parallelization here is 100% and no communication is needed among the processes. Running such a problem on HPC would mean underutilization of a supercomputer since the main point of HPC is having closely coupled compute cores on multiple nodes. In such cases you have quite good scaling, i.e., your program can run equally well on one core as on one million cores because there is no interdependence. Such problems are, e.g., searching for an optimum of some function for which you do not know its location, so you greedily search the domain. There can be also some intelligence behind, like a genetic algorithm, but this is just actually complicating the problem since there can be overlap of the search domains. And such algorithms are just maybe empirically describing the theory behind those. That's what supercomputing actually is not, although we are very fine with such kind of computing problems. There are also other problems that can be highly parallel, e.g., some kind of direct numerical computing or kinetic simulations could be very close to what embarrassingly simple computing is.

For efficient parallellization you need to know the computer architecture on which programs will run. Let's have a look at a computing node found in modern supercomputers. On the picture below you can observe that the compute node is a standalone Von Neumann computer.

![](https://raw.githubusercontent.com/kosl/ihipp-examples/master/docs/images/W1_compute_node.png)

The schematic below shows the logical view of a compute node.

![](https://raw.githubusercontent.com/kosl/ihipp-examples/master/docs/images/W1_logical_view_compute_node.png)

We have two or maybe four CPU sockets with shared memory that are interconnected by a bus or fast bus. The nodes are also connected with fast internet or Infiniband, by a network that has small latency. Such an architecture was a standard for computers 10 years ago. In the recent years main-stream computers besides CPU sockets also have accelerators, i.e., general-purpose graphical processing units (GPU) for speed up of computing. Therefore, the non-uniform memory is even more non-uniform. Coding or porting old codes with MPI and accelerating parts of it has become increasingly difficult to achieve. We will introduce you to accelerated programming with CUDA and OpenCL in Week 5, i.e., how to off-load parts of the code to the accelerators. Combining everything to run on a large cluster requires quite a lot of experience, also with the trial and error approach to identify, e.g., the bottlenecks. In order to resolve interconnection problems of nodes in the Infiniband network, as well as among the processor sockets and accelerators (GPUs) in the node some newer languages or upgrades to the existing programming languages were developed. To utilize these new paradigms some new tricks with the old code are needed, although rethinking or rewriting the code is usually the best approach. The new code approaches can be used even without the intervention of the programmer or any thinking, e.g., Coarray Fortran has some of intelligence behind how to do non-uniform memory operations on matrices and so on, but actually one will need to understand a few things.

Let's also discuss how nodes in a supercomputer are interconnected.

![](https://raw.githubusercontent.com/kosl/ihipp-examples/master/docs/images/W1_nodes_interconnect.png)

The figure on the left shows the nodes architecture that was typical in the past, while the figure on the right shows the present standard: also accelerators can be attached to memory from the other side. The distributed computing in such a sense means that the nodes are interconnected with some kind of topology. The many nodes message exchange, with message passing interface (MPI), is done through a high speed and low latency network, meaning usually Infiniband or some kind of similar technology, like Tofu Interconnect or RES, which are actually dependent on the vendor, is used. Infiniband is quite common and a de facto standard among many vendors. That means you can build a cluster with different vendors, which will still work for you, what was actually the initial idea to use commodity hardware and interconnect it by a high speed network. This is the basic idea of a supercomputer: a single fast machine that shares memory and processors, which can act well with any code. A typical test, still used to measure the performanceo of such machines, is the LINPACK test. Usually, the result is given in TFlops or teraFLops. 1 TFlops means the capability of a trillion floating-point operations per second. Currently, the TOP10 supercomputers in the world exceed the 30 thousand TFlops mark with the fastest at about 442 thousand TFlops.

So, for the development of parallel codes, you need to have quite a good overview of the architecture that you are using. Usually, many computing centers provide different machines, depending on the type of users. General purpose codes are usually not best suited for parallel computing. You need to understand the bottlenecks or which parts of the code consume most of the time. These parts must be optimized and that is the usual approach for the parallelization of the code.

On HPC, optimal communication is crucial for overcoming the bottlenecks. The main reason for bottlenecks can be generally found in communication among many parts of the code(s). To understand communication one should generally do profiling of the codes. Based on the profiling results one could, e.g., distribute the overhead of communication evenly to get rid of the peaks of it. Of course, this depends on the specific problem. Communication overall is important to be understood, but for embarassingly simple programs or those that do not have, have little or infrequent communication (for such problems communication is basically not interdependent), any communication network could be just fine, even the plain old ethernet. On the other hand, for solving large problems with coupled systems of equations, it's important not having large delays among coupled parts. The main difference between plain internet/ethernet and Infiniband, is in the latency time or how much time is needed to establish communication from one processor to another and to transfer the data between them, whether the data is small or large. Networks like Infiniband offer low-latency transfer among hardware resources connected to it. If you have such kind of problems with communication you probably would like to group the bunch of messages into a single message in order to have some useful workload.

We can recap what was already said regarding the development of parallel codes with the following points:

- good understanding of the problem being solved in parallel
- identifying how much of the problem can be run in parallel
- bottleneck analysis and profiling gives good picture on scalability of the problem
- optimization and parallelization of parts that consume most of the computing time
- the problem needs to be dissected into parts functionally and logically

### A->V: Amdahl's and Gustafson's laws explained

When you consider the execution of the code on a number of processors, the speed up achieved with such scaling is typically described by Amdahl's law.

![](https://raw.githubusercontent.com/kosl/ihipp-examples/master/docs/images/W1_Amdahl.png)

The speed up depends on the parallel portion of the code, the ideal speed up for a code that has, e.g., a parallel portion of 50% or in other words: 50% of it is serial and 50% is parallel, and is executed on an infinite number of processors, is just equal to 2, not more. So, for 50% of the parallel portion of the code, the maximum that you can obtain is two times faster or half of the time that is usually needed for execution on 1 processor (left figure). The figure on the right shows speed up depending on the number of processors for parallel portion of the code of 25, 50, 90 and 95%, respectively. For the cyan curve (95% parallel portion of the code), one can observe the maximum speed up of 20x for a large number of processors. A nearly 20x speed up is already achieved with about 500 processors, hence using more than 500 processors will not result in much gain of the speed up.

The latter rises the question, why would one invest in one million of processors if we see that even the best or one of the best programs, that are running 95% in parallel, are just going 20x faster? The answer can be given by Gustafson's law that actually interprets the currently available hardware, e.g., if 100, 1000 or a million of processors are available to the user.

![](https://raw.githubusercontent.com/kosl/ihipp-examples/master/docs/images/W1_Amdahl_vs_Gustafson.png)

Such a user can usually tailor the problem to her/his expectations and the hardware available. In other words, Gustafson's law fixes the time available to the user. By fixing the time, the problem can be scaled to the size that will give you the most accurate result for a chosen run time. Instead of looking how the code can get faster one can look how to get better results in the available run time. Of course, for some codes the expected time for the results to converge can take a week or month, so we can tailor a problem size to the currently available hardware and get the job done in the specified run time.

### A, D: Languages for parallel programming

When speaking of languages for parallel programming we actually mean parallelization paradigms in host languages. Such paradigms are generally available in the form of Application Programming Interfaces (APIs) that are installed on the user system and can be used as directives or extensions for compiling the parallelized code into executables.

Historically, the first host languages for parallel programming were C/C++ and Fortran. These languages are still a standard for using classical paradigms like OpenMP and MPI and also for accelerated programming, e.g., with CUDA and OpenCL. While Python as an interpreted language is not a common choice for parallel programming, some of its libraries, e.g., Cython, make use of parallelization paradigms, such as OpenMP, to speed up Python programs or scripts. Also, a Python library for MPI support exist (mpi4py), although it is not much used in HPC. On the other hand specialized Python libraries for Machine Learning and Deep Learning in the area of Artificial Intelligence heavily use parallel paradigms for accelerators (GPUs).

On the following list some parallelization paradigms available as APIs are given:

* **Open Multi-Processing (OpenMP)**:
  - supports multi-platform shared-memory parallel programming in C/C++ and Fortran
  - defines a portable, scalable model with a simple and flexible interface for developing parallel applications on several platforms
  - annotation of source code to identify the areas that should be accelerated using compiler directives and additional functions
  - targets both the CPU and GPU architectures and off-loads computational code on them
* **Message Passing Interface (MPI)**:
  - a standardized and portable message-passing standard designed to function on parallel computing architectures
  - defines the syntax and semantics of library routines that are useful to a wide range of users writing portable message-passing programs in C, C++, and Fortran.
* **Open Accelerators (OpenACC)**:
  - a programming standard for parallel computing designed to simplify parallel programming of heterogeneous CPU/GPU systems
  - annotation of C, C++ and Fortran source code to identify the areas that should be accelerated using compiler directives and additional functions
  - targets both the CPU and GPU architectures and off-loads computational code on them
* **Compute Unified Device Architecture (CUDA)**:
  - a parallel computing platform for general-purpose computing GPUs (GPGPU)
  - designed specifically for NVIDIA GPUs
  - a software layer for direct access to the GPU's virtual instruction set and parallel computational elements and for the execution of compute kernels
  - designed to work with programming languages such as C, C++, and Fortran.
* **Open Computing Language (OpenCL)**:
  - a framework for writing programs that execute across heterogeneous platforms (CPUs, GPUs, DSPs, FPGAs and other processors or hardware accelerators)
  - specifies programming languages (based on C99, C++14 and C++17) for programming these devices to control the platform and execute programs on the compute devices
  - provides a standard interface for parallel computing using task-based and data-based parallelism
  - an open standard maintained by the non-profit technology consortium Khronos Group
* **SYCL**:
  - a higher-level programming model to improve programming productivity on various hardware accelerators
  - a single-source domain-specific embedded language (DSEL) based on pure C++17
  - a standard developed by Khronos Group
* **Open Hybrid Multicore Parallel Programming (OpenHMPP)**:
  - programming standard for heterogeneous computing
  - based on a set of compiler directives, a programming model designed to handle hardware accelerators without the complexity associated with GPU programming

### Q: Performance, Easy to use

## OpenMP overview
### A: Brief intro to OpenMP

OpenMP (Open specifications for Multi Processing) is an API for shared-memory parallel computing. It was developed as an open standard for portable and scalable parallel programming, primarly designed for Fortran and C/C++. It is a flexible and easy to implement solution, which offers a specification for a set of compiler directives, library routines and environment variables.

As of 2021, the latest version of OpenMP API is 5.2. The OpenMP API is comprised of three components:

- Compiler Directives
- Runtime Library Routines
- Environment Variables 

**Compiler Directives**

Compiler directives are in the form of comments in the source code and are taken into account at compile time only if an appropriate compiler flag is specified. OpenMP compiler directives are used for:

- spawning a parallel region
- dividing blocks of code among threads
- distributing loop iterations between threads
- serializing sections of code
- synchronization of work among threads 

The syntax of the compiler directives is as follows:

```
sentinel  directive-name  [clause, ...]
```

In step [E: Hello World!] you have already learned the syntax of the OpenMP compiler directive in C and Fortran, i.e., for the directive name *parallel*.

**Run-time Library Routines**

These routines can be used for:

* setting and querying:
  - number of threads
  - dynamic threads feature
  - nested parallelism
* querying:
  - thread ID
  - thread ancestor's identifier
  - thread team size
  - wall clock time and resolution
  - a parallel region and its level
* setting, initializing and terminating:
  - locks
  - nested locks

All the run-time library routines in C/C++ are subroutines, while in Fortran some are functions, e.g., the run-time library routine for querying the number of threads in C:

~~~c
int omp_get_num_threads(void)
~~~

is a subroutine, while in Fortran:

~~~fortran
INTEGER FUNCTION OMP_GET_NUM_THREADS()
~~~

is a function.

Also note, that in C/C++ a specific header:

~~~c
#include <omp.h>
~~~

has to be generally included and that, contrary to Fortran, C/C++ routines are case sensitive.

**Environment Variables**

OpenMP environment variables can be used to control the execution of parallel code at run-time by:

* setting:
  - number of threads
  - thread stack size
  - thread wait policy
  - maximum levels of nested parallelism
* specifying how loop interations are divided
* binding threads to processors
* enabling/disabling:
  - nested parallelism
  - dynamic threads

The OpenMP environment variables are set as any other environment variables, depending on the shell used, e.g., you can set the number of OpenMP threads in *bash* with:

~~~bash
export OMP_NUM_THREADS=2
~~~

and in *csh* with:

~~~bash
setenv OMP_NUM_THREADS 2
~~~

### V: OpenMP memory, programming and execution model

OpenMP is based on the *shared memory model* of multi-processor/core machines. The shared memory type can be either Uniform Memory Access (UMA) or Non-Uniform Memory Access (NUMA). In OpenMP programs accomplish parallelism exclusively with the use of threads (thread based parallelism).

A thread is the smallest unit of processing that can be scheduled. Threads can exist only within the resources of a single process. When the process is finished, also the threads vanish. The maximum number of threads is equal to the number of processors/cores available. The actual number of threads used is defined by the user or application used.

While we referred OpenMP in the introduction to an easy approach for doing "automatic" parallelization, in reality OpenMP is an explicit *programming model*, that offers the user full control over parallelization. Although not automatic in a strict sense, parallelization is simply achieved by inserting compiler directives in a serial program and hence "automatically" transform it into a parallel program. Of course, OpenMP offers also complex programming approaches such as inserting subroutines to set multiple levels of parallelism, locks and nested locks, etc.

The basis of OpenMP's *execution model* is the the **fork-join model** of parallel execution. OpenMP programs begin as a *master thread*, that is executed sequentially until the first parallel region construct is encountered. The master thread then creates a team of parallel threads - a *fork*. The executable statements that are inside the parallel region construct are executed in parallel by the team threads. After the team threads finish execution of the statements in the parallel region construct, synchronization among them occurs and finally their termination results in a *join*, with the master thread as the only thread left.

![](https://raw.githubusercontent.com/kosl/ihipp-examples/master/docs/images/W1_OpenMP_fork-join.png)

Let's recap the OpenMP terminology discussed so far with descriptions:

| Term | Description |
| :--------------: | :-------------------------------------------: |
| OpenMP thread | a running process specified by OpenMP |
| thread team | a set of threads which cooperate on a task |
| master thread | main thread which coordinates the thread |
| thread safety | correct execution of multiple threads |
| OpenMP directive | OpenMP line of code for compilers with OpenMP |
| construct | an OpenMP executable directive |
| clause | controls the scoping of the variables during execution |

### E: For loop

In this example you will learn how to use a `for` OpenMP directive in C and a `DO` OpenMP directive in Fortran for vector addition.

Let's assume we want to add arrays `a` and `b` into the sum (array) `c`. In C we can do that by using the `parallel` and `for` OpenMP directives:

~~~c
#pragma omp parallel shared(a,b,c,chunk) private(i)
  {

  #pragma omp for schedule(dynamic,chunk) nowait
  for (i=1; i <= N; i++)
    c[i] = a[i] + b[i];

  }  /* end of parallel section */
~~~

Let's explain the code in detail:

- the clause `shared(a,b,c,chunk)` in the `parallel` directive indicates that arrays `a`, `b`, `c` and the variable `chunk` will be shared by all threads
- the clause `private(i)` in the `parallel` directive indicates that the variable `i` will be private to each thread and that each thread will have its own unique copy
- the clause `schedule(dynamic,chunk)` in the `for` directive indicates that the iterations of the for loop will be distributed dynamically in `chunk` sizes
- the clause `nowait` in the `for` directive indicates that the threads will not synchronize after completing their individual pieces of work

Explore the whole C code in the notebook and run it. Are the results as you expected?

Now, compare the OpenMP code in Fortran:

~~~fortran
!$OMP PARALLEL SHARED(A,B,C,CHUNK) PRIVATE(I)

!$OMP DO SCHEDULE(DYNAMIC,CHUNK)
      DO I = 1, N
         C(I) = A(I) + B(I)
      ENDDO
!$OMP END DO NOWAIT

!$OMP END PARALLEL
~~~

with the code in C and identify the differences in the syntax of OpenMP directives and clauses.

Explore also the whole Fortran code in the notebook and run it. Are the results the same as in C?

[for_DO_OpenMP.ipynb](https://github.com/kosl/ihipp-examples/blob/master/OpenMP/for_DO_OpenMP.ipynb)

## MPI overview
### A/V: Brief intro to MPI
### A: Different types of communication
### Programming point of view
### E: MPI hello world

## Accelerators overview?
### A: graphic accelerators
### V: GPGPU programming/Thread hierarchy


## Resources:
### Further reading
### List of top 500
### Where to search for a help

## Test:

###### tags: ipp, HPCFS
