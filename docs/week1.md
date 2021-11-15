# Introduction to parallel programming

## A->V:Intro to parallel programming
### V: Intro to Week 1, Serial vs Parallel

This week, we will be introducing you to the basics of understanding's, and the second part is somehow advanced to that. So it is more or less introduction in the sense that we will not go deep in each topic that we will be introducing, whether this is introductory course of each topics or even advanced. So even in the advanced topics, we will briefly describe just what it is important to know.
And to give you pointers or where to learn more so that at some point you will be able to do your own coding and using HPC environment, the environment that we are now using for the course today, we will be somehow introducing today.

It is our intent to show you important things that we think you will need to understand to be not afraid of, let's say, taking the knowledge further by doing your own course (cause?). So overall, there are many scientific and engineering challenges that can be tackled by existing codes and there are a lot of research issues. But only by upgrading, let's say, existing codes, you will actually be able to bring up new knowledge, whether this is the, let's say, engineering, physics or other domains.

Such domains were dominantly used in the past. Now just everybody could get in touch, and that's what the intent is for the supercomputing to show that it can be very easy tool to use, it can be fun tool to get involved, and you can make your living out of that, especially if you are good in some domain understanding and preparing. So a lot of let's say work for the new knowledge is getting developing, moving data into the correct format so that you can see it and so on, so analyzing the results and so on. And for that, we do have two let's say views on the computing. One is distributed serial computing meaning that you have many problems to solve and anybody can check if some problem is solvable and so on. And you don't care about time. And the other is parallel computing where the problem needs to be divided into many cores or nodes or computers because it is too big to fit into one or it is too slow to be solved by one computer. So while you can have the so called grid computing the opposite of it is let's say supercomputing where you need a super computer to solve your problem. And of course you heard of cloud computing and all, that is so-called commercial version of the offerings.

But of course, if you are a serious user, you will quickly find out that buying a car is cheaper than renting it on the long term, so there will never be a commercial offering that will match, let's say, individual purchases for the machine that is usually 90 or 100 percent utilized. So it is not like a car that you buy for fun and you've spent a lot. Supercomputers are usually very heavily utilized, meaning that during its lifetime, the computer gets out there, its bits on the peak performance.

So for the parallel computing that we said, it cannot be done better on the single machine or many single machines. So that's how you do that. You will do a serial execution in parallel. You divide the problem into separate commands that are done in parallel. There are different approaches or programming models that were developed during the years, and they are still being developed. Along with the languages that might help you to resolve some of the issues of the hardware, underlying hardware topology that we see usually as a combination of memory and CPUs in the past, there were just a single processor and memory per node, and many of those nodes were combined together to make a cluster. A cluster of compute nodes, so called "Beowulf" and so on, are being in the recent years upgraded with many cores per node and shared memory. So the cores do share a memory, there can be many sockets and the programming model for such a thing is a combination of languages. So we do have OpenMP, a parallelization that can be easily done on a single computer, whether this is your PC laptop or remote computer. And for that, this is quite an easy way to do automatic parallelization. It means that you will start with a serial program and upgrade it with the command comments (directives?) and you will get multi-threaded code that runs faster.


### D: What team are you on?
###  E: Hello, World!
### A->V: Architectures, Memory models, Amdahl and Gustafson law explained

While over the years there were different other multi node approaches and the only really interesting system was Message Passing Interface (MPI). For that we will have the introduction to the whole day tomorrow. And a combination of both models is actually a simple upgrade of those two, let's say, again, a bit of performance regarding the memory utilisation or let's say CPU utilisation. Because the latest computers have non-uniform memory, meaning that the memory speed is not uniform, so it is not a symmetric memory but mostly asymmetric regarding the cores. So far, parallel computing we usually look for as many as possible computing cores available to us to parallelize the code. And the idea or problem that can be resolved or using the parallel computing with 100% of parallel utilisation is embarrassingly simple parallel processing. As I said, for such kind of computing you actually don't need HPC. You have many other solutions, I have mentioned grid computing that usually is distributed, cloud computing that you can rent. And the problems that are being solved are not actually interdependent, so the parallelization here is 100 percent and no communication is needed between the processes, meaning that if you're running such a problem on HPC, you are under utilizing a supercomputer because the main point of the HPC is having closely coupled compute cores on multiple nodes. So in such case, of course, you have quite good scaling, meaning that your program can run equally well on one core as on one million cores because there is no interdependence. Such problems are, for example, searching an optimum of some function for which you do not know where it is, so you greedily search the domain. You may say I have some intelligence behind like a genetic algorithms or what, but this is just actually complicating this problem because there can be overlap of the search domains. And such algorithms are just maybe empirically describing, let's say, the theory behind those. That's what actually supercomputing is not, although we are very fine with such kind of computers, computer problems. There are also others that can be highly parallel, but for example, some kind of direct numerical computing so DNA simulations could be, or some kind of kinetic could be very close to what we do have here for embarrassingly simple computer (computing?), while for the large racks of computers, as we see here, the usual setup is like this.

We have two, maybe four sockets of CPU that are interconnected by a bus or fast bus and the nodes are then connected also with fast internet or Infiniband, the network that has small latency and so on. And that consists of, let's say, usual, a way of what computers were, let's say, 10 years ago. In the recent years we also have main-stream computers that besides the CPU sockets have also accelerators, meaning general-purpose graphical processing units that can do also speed up in the limited memory that it has. So the non uniform memory is even more non uniform and coding or porting old codes that were assuming, let's say, message passing interface and accelerating parts of it has become increasingly difficult to do. And part of that, we will be doing some kind of introduction to, let's say, accelerated programming on Thursday or Friday, actually, where we will show you some kind of CUDA programming, so how to run some part of the code in the accelerators. And combining everything into running code that will run on a large cluster takes quite a lot of, let's say, experience to be or let's say trial and error so that you can find the bottlenecks and so on. In order to simplify that interconnection problems between the Infiniband, then into the node between the sockets and from the processor sockets to accelerators or GPUs is somehow being tried to be improved by some newer languages or upgrades of the existing programming languages. But to utilize that we need to do new tricks with the old code, and usually it requires rethinking or rewrite of it.

If you would like to use the new code approaches or for example, Coarray Fortran has some of intelligence behind how to do the non-uniform memory operations on matrices and so on without the intervention of a programmer or thinking, but actually you will need to understand a few things. So, before we can do anything, it is good that you understand how this works. So on the top of these four blocks here, we see the past and on the bottom the present with accelerators or that would be actually attached to the memory from the other side, so the distributed computing in such a sense means that nodes are interconnected with some kind of topology. The many nodes message exchange, with message passing interface or MPI, is done through high speed and low latency, meaning usually Infiniband or some kind of, let's say, similar technology like Tofu Interconnect, RES and similar names, which are actually dependent on the vendor, but Infiniband, let's say, is quite common and mostly agreed among many vendors, so that you can build a cluster with different vendors, and it will still work for you. So, that was actually the initial idea that you use commodity hardware and you interconnect them by a high speed network. And you get a single fast machine that shares a memory and processors and can act well in any code. For many years, the development and these codes were tested by a classical LINPACK system. I will show you a few things about it. But before that, we just assume I have just two slides more after this.

So for the development of parallel codes, you need to have quite a good overview of the architecture that you are doing, there are quite different machines in the world or being available. Usually many computing centers provide different machines, depending on what kind of user is. But general purpose is usually not the best way to start programming. You need to understand the bottlenecks. So how to give and there are also some theoretical implications and we do optimize parts of it. To that consume most of the time, and that is the usual approach for the parallelization of the code.


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
