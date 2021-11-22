# Introduction to parallel programming

## A->V:Intro to parallel programming
### V: Intro to Week 1, Serial vs Parallel

In this week we will introduce you to the basic principles and paradigms of parallel programming. We will not go deeply into each topic, the next weeks will be dedicated to that, even to some advanced topics in parallel programming. But even with the adavanced topics we will briefly describe just what it is important to know and to give you a starting point where to learn more so that at some point you will be able to do your own coding.

There are many scientific and engineering challenges that can be tackled by the area of computing. In general we have two views on it. One is distributed serial computing, which means that you have many problems to solve and you don't care about time. The other is parallel computing where the problem needs to be divided into many compute cores or nodes, essentially many computers, because it is too big to fit into one computer or one computer would be too slow to solve it. The first approach is often called grid computing, while the opposite of it or the second approach is generally referred to supercomputing where you need a supercomputer to solve your problem. You probably also heard of cloud computing and similar, which is a commercial version of grid or supercomputing resources.

If you are a serious user, you will quickly find out that, if we use an analogy, buying a car is cheaper than renting it on the long term, so there will never be a commercial offering that will match individual purchases for the machine that is usually 90 or 100 percent utilized. So it's not like buying a car for fun and you have spent for it a lot. Supercomputers are usually very heavily utilized, meaning that during its lifetime, the computer operates near peak performance.

Parallel computing cannot be done better on a single machine or many single machines. You have to divide the problem into separate commands that are done in parallel or in other words: a serial execution in parallel. There are different approaches or programming models that were developed during the years and they are still being developed. Along with the languages that might help you to resolve some of the issues of the hardware, for parallel computing is also essential the underlying hardware topology that we see usually as a combination of memory and CPUs. In the past, there were just a single processor and memory per node, and many of those nodes were combined together to make a cluster. In the recent years a cluster of compute nodes, so called "Beowulf", is being upgraded with many cores per node and shared memory. The cores share a memory, there can also be many sockets. The programming model for such a hardware architecture is a combination of languages. We have, e.g., OpenMP, a parallelization that can be easily done on a single computer, whether this is your PC laptop or a remote computer. This is quite an easy approach to do automatic parallelization. It means that you will start with a serial program and upgrade it with the command directives and the result is multi-threaded code that runs faster.

### D: What team are you on?

We will introduce you to parallel programming with the use of some programming languages. Tell us which programming language(s) you use or know about or what language are you planning to learn.

###  E: Hello, World!

As already mentioned, the simplest approach to parallelization is Open Multiprocessing (OpenMP). We will show you this paradigm through a "Hello, World" example in two programming languages: C and Fortran.

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

Here `#pragma omp` indicates the OpenMP executable directive, `parallel` the construct and `num_threads(2)` the number of threads to be used. This directive is applied to the succeeding structured block of executable statements between `{...}`. In our case the executable statement is "Hello World!" print statement.

In Fortran the construct looks like:

~~~fortran
!$OMP PARALLEL num_threads(2)

    PRINT *, "Hello World!"

!$OMP END PARALLEL
~~~

Similarly to C, `!$OMP` indicates the OpenMP executable directive, `PARALLEL` the construct and `num_threads(2)` the number of threads to be used. This directive is applied to the succeeding structured block of executable statements with a single entry at the top and a single exit at the bottom. As before, the executable statement is "Hello World!" print statement.

Have a look at the notebook with both codes in C and Fortran. Notice the headers in C that must be included and the `USE OMP_LIB` line of code in Fortran to provide openmp functionality. Compilation of the codes will be explained later, so don't worry about this detail for now.

Run both codes in the following notebook:

[Hello_world_OpenMP.ipynb](https://github.com/kosl/ihipp-examples/blob/master/OpenMP/Hello_world_OpenMP.ipynb)

Are the outputs as you expected?

### A->V: Architectures, Memory models, Amdahl's and Gustafson's laws explained

Over the years there were different multi node approaches to parallelization. The only really interesting system was Message Passing Interface (MPI), which we will introduce in this week and present in detail in Week 3. A combination of both approaches (OpenMP and MPI) can actually be done in a very simple way to gain a bit of performance regarding memory utilisation or CPU utilisation. Latest hardware architectures have non-uniform memory access (NUMA), hence memory regarding the cores is not symmetric but mostly asymmetric.

The parallel computing approach tends to use as many computing cores as possible for parallel code execution. The ideal is 100% parallel utilisation which can be achieved only for embarassingly simple parallel problems. For such kind of computing you actually don't need High Performance Computing (HPC). You have many other solutions, e.g., grid computing that is usually distributed and cloud computing that you can rent. Such problems that are being solved are not actually interdependent, so the parallelization here is 100% and no communication is needed among the processes. Running such a problem on HPC would mean underutilizing a supercomputer since the main point of HPC is having closely coupled compute cores on multiple nodes. In such cases you have quite good scaling, i.e., your program can run equally well on one core as on one million cores because there is no interdependence. Such problems are, e.g., searching for an optimum of some function for which you do not know its location, so you greedily search the domain. There can be also some intelligence behind, like a genetic algorithm, but this is just actually complicating the problem since there can be overlap of the search domains. And such algorithms are just maybe empirically describing the theory behind those. That's what supercomputing actually is not, although we are very fine with such kind of computing problems. There are also other problems that can be highly parallel, e.g., some kind of direct numerical computing or kinetic simulations could be very close to what embarrassingly simple computing is. For the large racks of computers the setup is usually like this.

We have two or maybe four CPU sockets that are interconnected by a bus or fast bus. The nodes are also connected with fast internet or Infiniband, by a network that has small latency. Such an architecture was a standard for computers 10 years ago. In the recent years main-stream computers besides CPU sockets also have accelerators, i.e., general-purpose graphical processing units (GPU) for speed up of computing. Therefore, the non-uniform memory is even more non-uniform. Coding or porting old codes with MPI and accelerating parts of it has become increasingly difficult to achieve. We will introduce you to accelerated programming with CUDA and OpenCL in Week 5, i.e., how to off-load parts of the code to the accelerators. Combining everything to run on a large cluster requires quite a lot of experience, also with the trial and error approach to identify, e.g., the bottlenecks. In order to resolve interconnection problems of nodes in the Infiniband network, as well as among the processor sockets and accelerators (GPUs) in the node some newer languages or upgrades to the existing programming languages were developed. To utilize these new paradigms some new tricks with the old code are needed, although rethinking or rewriting the code is usually the best approach.

The new code approaches can be used even without the intervention of the programmer or any thinking, e.g., Coarray Fortran has some of intelligence behind how to do non-uniform memory operations on matrices and so on, but actually one will need to understand a few things. The top figure with four blocks shows the hardware architecture as was typical in the past, while the bottom figure the present standard: accelerators can be attached to memory from the other side. The distributed computing in such a sense means that the nodes are interconnected with some kind of topology. The many nodes message exchange, with message passing interface (MPI), is done through high speed and low latency access, meaning usually Infiniband or some kind of similar technology, like Tofu Interconnect or RES, which are actually dependent on the vendor, is used. Infiniband is quite common and a de facto standard among many vendors. That means you can build a cluster with different vendors, which will still work for you, what was actually the initial idea to use commodity hardware and interconnect it by a high speed network. This is the basic idea of a supercomputer: a single fast machine that shares memory and processors, which can act well with any code. A typical test, still used to measure the performanceo of such machines, is the LINPACK test. Usually, the result is given in TFlops or teraFLops. 1 TFlops means the capability of a trillion floating-point operations per second. Currently, the TOP10 supercomputers in the world exceed 30 thousand TFlops mark with the fastest at about 442 thousand TFlops.

To recap, for the development of parallel codes, you need to have quite a good overview of the architecture that you are using. Usually, many computing centers provide different machines, depending on the type of users. General purpose codes are usually not best suited for parallel computing. You need to understand the bottlenecks or which parts of the code consume most of the time. These parts must be optimized and that is the usual approach for the parallelization of the code.

On HPC, optimal communication is crucial for overcoming the bottlenecks. The main reason for bottlenecks can be generally found in communication among many parts of the code(s). To understand communication one should generally do profiling of the codes. Based on the profiling results one could, e.g., distribute the overhead of communication evenly to get rid of the peaks of it. Of course, this depends on the specific problem. Communication overall is important to be understood, but for embarassingly simple programs or those that do not have, have little or infrequent communication that is not interdependent, any communication network could be just fine, even the plain old ethernet. On the other hand, for solving large problems with coupled systems of equations, it's important not having large delays among coupled parts. The main difference between plain internet/ethernet and Infiniband, is the latency time or how much time is needed to establish communication from one processor to another and to transfer the data between them, whether the data is small or large. If you have such kind of problems with communication you probably would like to group the bunch of messages into a single message in order to have some useful workload.

When you consider the execution of the code on a number of processors, the speed up achieved with such scaling is typically described by Amdahl's law. The speed up depends on the parallel portion of the code, the ideal speed up for a code that has, e.g., a parallel portion of 50% or in other words: 50% of it is serial and 50% is parallel, and is executed on an infinite number of processors, is just equal to 2, not more. So, for 50% of the parallel portion of the code, the maximum that you can obtain is two times faster or half of the time that is usually needed for execution on 1 processor (left figure). The figure on the right shows speed up depending on the number of processors for parallel portion of the code of 25, 50, 90 and 95%, respectively. For the cyan curve (95% parallel portion of the code), one can observe the maximum speed up of 20x for a large number of processors. A nearly 20x speed up is already achieved with about 500 processors, hence using more than 500 processors will not result in much gain of the speed up.

The latter rises the question, why would one invest in one million of processors if we see that even the best or one of the best programs, that are running 95% in parallel, are just going 20x faster? The answer can be given by Gustafson's law that actually interprets the currently available hardware, e.g., if 100, 1000 or a million of processors are available to the user. Such a user can usually tailor the problem to her/his expectations and the hardware available. In other words, Gustafson's law fixes the time available to the user. By fixing the time, the problem can be scaled to the size that will give you the most accurate result for a chosen run time. Instead of looking how the code can get faster one can look how to get better results in the available run time. Of course, for some codes the expected time for the results to converge can take a week or month, so we can tailor a problem size to the currently available hardware and get the job done in the specified run time.

### A, D: Languages for parallel programming
### Q: Performance, Easy to use


## OpenMP overview:
### A: Brief intro to OpenMP
### What is shared memory
### V: OpenMP programming and execution models
### V: OpenMP memory models
### E: For loop


## MPI overview
### A/V:
### A: /Different types of communications/
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
