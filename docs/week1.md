# Week 1

## A->V:Intro to parallel programming
### V: Intro to Week 1, Serial vs Parallel

This week, we will be introducing you to the basics of understanding's, and the second part is somehow advanced to that. So it is more or less introduction in the sense that we will not go deep in each topic that we will be introducing, whether this is introductory course of each topics or even advanced. So even in the advanced topics, we will briefly describe just what it is important to know.
And to give you pointers or where to learn more so that at some point you will be able. To do your own coding and using HPC environment, the environment that we are now using for the course today, we will be.

Important things that we think you will need to understand to be not afraid of, let's say, taking the knowledge further by doing your own course. So overall, there are many scientific and visioneering challenges that can be tackled by existing codes and there are a lot of research issues. But only by upgrading, let's say, existing codes, you will actually be able to bring up new knowledge, whether this is the, let's say, engineering, physics.

Such demands were dominantly used in the past. Now just everybody could get in touch, and that's what the intent is for the supercomputing to show that it can be very easy to to use it can be fun, cool to get involved, and you can make your living out of that, especially if you are going to use some domain understanding for preparing. So a lot of let's say. Work for the new knowledge is getting developing, moving data into the correct format so that you can see it and so on, so analyzing the results and so on. And for that, we do have. To let's say we on the computing line.

That is so-called commercial version of the offerings.

But.

Of course, if you are a serious user, you will quickly find out that buying a car. It's cheaper than renting it on the long term, so there will never be a commercial offering that will match, let's say. Individual purchases for the machine that is usually 90 or 100 percent utilized. So it is not like a car that you buy for fun and you've spent a lot. Supercomputers are usually very heavily utilized, meaning that during its lifetime, the computer gets out there, its bits on the peak performance.

So for the parallel computing that we said, it cannot be done better on the single machine or many single machines. So that's how you do that. You will do a serial execution. In parliament, you divide the problem into separate commands that are done in parliament. There are different approaches or programming models that were developed. During the years, and they are still being developed. Along with the languages that might help you to resolve some of the issues of the hardware underlying hardware technology that we see usually as. A combination of memory and sleepless in the past, there were just a single processor and memory, but a lot and many of those notes were combined together to make a cluster. A cluster of compute nodes, so called Bill Wolff and so on, are being in the recent years upgraded many parts Clarksburg. And shared memory, so of course, I do share a memory. The day there can be many sulcus and the. Programming model for such a thing is a combination of languages, so we do have open and paralyzation that can be easily done on a single computer, whether this is your. PC laptop or remote computer? And for that, this is quite an easy way to do automatic politicisation means that you will start with serial program and create with the command comments and you'll get more titrated.


### D: What team are you on?
###  E: Hello, World!
### A->V: Architectures, Memory models, Amdahl and Gustafson law explained

Code that rules Foster, while over the years there were different other rules to note. Approaches and the only really. Interesting system was a message passing interface for that, we will have the introduction to full day tomorrow and a combination of both models is actually a simple upgrade of those to, let's say, again, a bit of performance regarding the memory utilisation or let's say secure utilisation. Because the latest computers. Have non-uniform memory, meaning that. The memory speed is not. Uniform, so it is not a symmetric memory. But mostly isometric regarding the. Of course, so far. Parallel computing, we usually. Look for as many as possible. Computing, of course, available to us to personalize the court and the idea of. Problem that can be. Resolved or using. The father of computing with 200 percent of palm utilisation is embarrassingly simple, parallel processing, as I said, for such kind of computing. You actually don't need HGC, you have many other solutions, I have mentioned a grid computing that usually these are distributed cloud computing that you can rent. And the problems that are being solved are not actually interdependent, so the polarization here is 100 percent and no communication is needed between the processes, meaning that if you're running such a problem on HPC, you are under utilizing a supercomputer because the main point of the HPC is having closely coupled.

Compute course notes on Malti, not so in such case, of course, you have quite good scaling, meaning that your program can run. Equally well on one car is on one million cars because there is no interdependence, sorts of problems are. For example, searching an optimal. Of some function for which you do not know where it is, so you greedily search the domain. You may say I have some intelligence behind like a genetic algorithms or what, but this is just actually complicating this problem because there can be overlap of the search domains. And such algorithms were just maybe empirically. Describing the order, let's say. The theory behind Donoso. That's what actually supercomputing is not, although we are very fine with such kind of computers, computer problems. There are also others that can be highly correlated, but for example, some kind of direct medical. Computing so DNA simulations could be or some kind of QinetiQ could be very close to what we do have here for embarrassingly simple computer, while for the large racks of computers, as we see here, the usual setup is like this.

We have two, maybe four sockets of C.P.U.

That are interconnected by a bus or fast bus and. The notes are then. Connected also with. First, Internet or infinity bent the network that has small latency and so on, and that consists of, let's say, usual, a way of what computers were, let's say, 10 years ago in the recent years. We also have a main stream computers that besides the C.P.U sockets, have also accelerator's meaning, general-purpose graphical processing units that can do also speed up the limited memory that it has. So the non uniform memory is even more non uniform and. Clothing or sporting old coats that were assuming, let's say, message box interface and accelerating parts of it has become increasingly difficult to do. And part of that, we will be doing some kind of introduction to, let's say, accelerated programming on. Thursday or Friday, actually, where we will show you some kind of crude programming. So how to run some part of the code in the accelerator's and combining everything into running code that will run on a large classer takes quite a lot of, let's say, experience to be or let's say trial and error so that you can find the bottlenecks and so on in order to simplify that. Interconnection problems between the. Infinium van, then into the. Not between the sockets and from the processor sockets to accelerators or details is somehow being tried to be improved by some newer languages or upgrades of the existing programming languages. But that utilize needs to do new tricks with the old code, and usually it requires rethinking or rewrite of it.

If you would like to use the new code approaches or for example, cholerae for transitions of intelligence behind how to do the non-uniform and where you. Operations on vacances and so on. Without the intervention of. Programmer or thinking, but actually you will need to understand, he thinks so. Before we can do anything, it is good that you understand how this works. So on the top of these four blocks here, we see the first. And on the bottom, the president would accelerate or that would be actually attached to the memory from the other side, sort of distributed computing in such a sense means that nodes are interconnected with some kind of topology. The many nodes message exchange with each passing interface or API is done through high speed and low latency, meaning usually infinite bent or some kind of, let's say, similar technology like tofu aureus and similar names, which are actually. Dependent on the vendor, but let's say it's quite, quite common and less agreed. Among that many randazza that you can build a Kloster with different Manderson's, it will still work for you. So that was actually the initial idea to use commodity hardware and to interconnect to buy a high speed network. And you get a single fast machine that shares a memory and processors and can act well in any code. For many years, the development and these codes were tested by Classico Park system will show you a few things about it. But before that, we just assume I have just two slides more after this.

So for the development of Parro codes.

You need to have quite a good overview of the architecture that you are doing, there are quite different machines in the world or being available. Usually many computing centers provide different machines, depending on what kind of user is. But general is usually not the best way to start programming. You need to understand the bottlenecks. So how to give. And there are also some theoretical implications and we do optimize parts of it. To that consume most of the time, and that is the usual approach for the. Parallelization.


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
