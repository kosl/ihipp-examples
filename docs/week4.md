## MPI Continued

## 1.1 V: Non Blocking communications
We saw in the previous week that the types of communication in MPI can be divided by two arguments i.e based on the number of processes involved so
- Point-to-Point Communication
- Collective communication

And another way of dividing would be relating to the completion of an operation i.e
- Blocking Operations
- Non-Blocking Operations

We have seen some problems in the previous modes of communication we have learnt until now. For instance, in the Ring example (image D2P2S18) where we have a cyclic distribution of processes that we would like to send messages along the ring, blocking routines are somehow not suitable for this. The problem is that for the second or third process in order to actually receive something, would have to wait for the message to be sent to the first one and so on. So evidently we are losing time and not producing a good parallel application. While using blocking routines, when we profile the code it happens quite often that we either have some problem with the deadlocks that we discussed previously, i.e either there is some 'sent' data  that we just never received or vice versa. Even though this situation can be solved, however, there is another more complex problem that can arise.  Suppose in the previous example if we would do it using blocking communication, we would basically 'serialize' our code (image) and as we see that because some of the processes would need to wait our resources are wasted. This clarifies the need for some other clever way to send messages via this ring without so much waiting time and this is where the non blocking communication comes into play.
As we saw already in the previous week that Non blocking routine returns immediately and allows the sub-program to perform other work so we can do some work between and this is useful because you can, for instance, we can send a message, do some stuff, and then we can receive the message. So these three parts are essential in the Non Blocking communications. 

So Non Blocking communication is divided into three phases. 
- First phase is obviously to initiate non-blocking communication. We will distinguish all imperative which are non blocking with the capital 'I". So immediately after MPI and underscore there will be the capital 'I' so MPI_Isend, which means immediately and MPI_Irecv. So the protocols will look like
~~~C
MPI_Isend(void *buf, int count, MPI_Datatype datatype,int dest, int tag, MPI_Comm comm, MPI_Request *request);
//and
MPI_Irecv(void *buf, int count, MPI_Datatype datatype, int source, int tag, MPI_Comm comm, MPI_Request *request);
~~~
- Then we can do some other work because when we use this routine, it does not block us, so we can do some stuff after this. However, later on we actually have to check whether the message has been received.
- To do this final phase we need to wait for nonblocking communication to complete and we do this by calling the MPI_wait function. This completes the whole process.  This request is just another struct in MPI similar to 'status', so we just define it as similar to status and then put on the pointer there. The prototype of this function looks like
~~~c
MPI_Wait(MPI_Request *request, MPI_Status *status);
~~~
We will understand this more clearly with the help of the following two examples.

### Non-blocking send and receive
(imageD2P2S20) *would be ideal as an animation*
In this examples let us assume that all the processes would like to share some information along the ring. As the picture shows, process zero would like to send something to one, six would like something to zero and so on. The idea here is that first we initialize the non blocking send and we send the message. So, firstly we initiate non-blocking send to the right neighbour. As we know in non blocking communication after we have done that we can do some work. In our case we will receive the message via the classical receive function. So, in this ring example, receive the message from the left neighbour. And finally at the end, we have to call the MPI_wait function in order to check if everything was done and  for the non-blocking send to complete.  
Perhaps you can already see it clearly that fundametally it is non blocking in this ring example that helps us so that every process can start the sending i.e we can send information, so send a message, but at the same time, we can still do something else.

In similiar ways we can initiate the non blocking receive. So in our ring example it would mean that we initiate non-blocking receive from the left neighbour. This would imply that we will receive something, but maybe not not now, maybe later, and we do some work. In this case it would mean sending information to the following receiver so, send the message to the right neighbour. Finally, we would call the MPI_wait function to wait for non-blocking receive to complete.

Let us try to furhter consolidate these ideas by implementing them in the following excercise!

## 1.2 E: Rotating information around a ring (non-blocking)

### Goal
- A set of processes are arranged in a ring. Initialize sum to 0. 

a)
1. Each process stores its rank into snd_buf. 
2. 2. Each process passes this on to its neighbour on the right.
3. Each process adds snd_buf to sum. 

b)
1. Repeat 1-2-3 with size (number of process) iterations, i.e. each process computes the sum of all ranks.
2. Use non-blocking MPI_Isend.

## 1.3 V: One sided communication
As we already learnt in the begining that in MPI the parellelisation is based on the distributed memory. This means that if we run a program on different cores each core has its own private memory. Since, the memory is private to each process we send messages to exchange data from one process to another. 
In two-sided (i.e point to point communication) and collective communication models the problem is that (even with the that non blocking) both sender and receiver have to participate in data exchange (i.e send and receive) operations explicitly, which requires synchronization. 
(image S24) In this example we can see when we have the non blocking routine the problem is that when we call the MPI_send and until the message has been recieved my the MPI_recv, there is this time in which both the processes have to wait and they can not do anything. Therefore a signinficant drawback of this approach is that the sender has to wait for the receiver to be ready to receive the data before it can send the data, or vice versa. This causes idle time. To avoid this we use the one sided communication. 

Although MPI is using a distributed memory approach, the MPI standard introduced Remote Memory Access (RMA) routines also called one-sided communication because it requires only one process to transfer data. Simply put it enables a process to access some data from the memory of the other processes. The idea is that  process can have direct access to the memory address space of a remote process without intervention of that remote process.
(image S25)So we do not have to explicitly call the 'send' and 'receive' routines from both the sides. The process can just 'put' and 'get' the data from the memory of the other processor. This is helpful because the target process can continue executings its tasks, doing its work without waiting for anything. So the most important benefit of one sided communication is that while a process puts or gets data from remote process, the remote process can continue to compute instead of waiting for the data. This reduces communication time and can resolve some problems with scalability of the programs (i.e. on thousands of MPI processes)
In order to allow other processes to have access into its memory, a process has to explicitly expose its own memory to others. This means that for the origin process to access the memory in the target process, the target process has to allow that the memory can be accessed and used. It does this by declaring a shared memory region, also called a window. This window becomes the region in the memory that is available to all the other processes in the communicator allowing them to put and get data from its memory. The window is created by callin the function 
~~~c
MPI_Win_create(void *base, MPI_Aint size, int disp_unit, MPI_Info info, MPI_Comm comm, MPI_Win *win);
~~~
The arguments in this function are quite different. They are as follows
- 'base' is the pointer to local data to expose. i.e the data we would want access to. 
- 'size' denotes the size of local data in bytes.
- disp_unit is the  unit size displacements
- 'info' is the info argument. Most oftenly we use info_NULL. 
- 'comm' is the communicator that we know from all the previous functions.
- 'win' represents the window object. 

And at the end of the MPI application we have to free this window with the function
~~~C
MPI_Win_free(MPI_Win *win);
~~~
So with these functions we create a window around the memory that would be accessible to others. That is why at the end of we have to call this Win_free function to free this window. 
To better understand lets go through a classic example
~~~c
MPI_Win win;
int shared_buffer[NUM_ELEMENTS];
MPI_Win_create(shared_buffer, NUM_ELEMENT, sizeof(int), MPI_INFO_NULL, MPI_COMM_WORLD, &win);
... MPI_Win_free(&win);
~~~
So here we define an MPI struct variable 'win'. Then we define some data or storage through either dynamic allocation or something similiar. Using this buffer we actually then create the window. So in the MPI_win_create you can see that we would like to share this 'shared_buffer' buffer. The size here is the '{NUM_ELEMENTS}'. Since each data type is 'int' so the discplacement becomes lets say probably 4 bytes wide. The info is usually 'NULL' and the communicator as always is the 'comm_world'.
Once this is called, this shared buffer can be shared by all the processes by calling the MPI_Put and MPI_Get routines. Of course at the end of the application we free the 'win' window. 

### MPI_Put and MPI_Get

To access the data we need the two routines we talked about earlier i.e the MPI_Put and MPI_Get. MPI_Put operation is equivalent to a send by origin process and a matching receive by the target process. The prototype of these functions have a bit too many arguments and they look like this
~~~c
MPI_Put(void *origin_addr, int origin_count, MPI_Datatype origin_datatype, int target_rank, MPI_Aint target_disp, int target_count, MPI_Datatype_target_datatype, MPI_Win win)
~~~
In the same manner MPI_Get is similar to the put operation, except that data is transfered from the target memory to the origin process. The prototype of this function looks like this
~~~c
MPI_Get(void *origin_addr, int origin_count, MPI_Datatype origin_datatype, int target_rank, MPI_Aint target_disp, int target_count, MPI_Datatype_target_datatype, MPI_Win win);
~~~
We will understand in depth about the arguments of these functions in the following excercise. But before we get into that another important thing that we need to discuss is the Synchronization. If you remember we discussed this concept briefly in the (number) week when we were learning about the concepts of OpenMP. 
In MPI in one sided communication (image S24)  the target process  calls the function to create the window in order to give access of its memory to other processes. However, in the case of multiple users it is already quite plain to see that if these users try to simultaneously access this data can already lead to some problems. For example, lets say two users access the window to put data using the MPI_Put function this is clealry a race condition that needs to be avoided. This is where synchronisation comes into the play. So in order to avoid this before and after each 'one sided communication' function i.e MPI-Get and MPI_Put we need to use this function
~~~c
MPI_Win_fence(0, MPI_Win win);
~~~
This function actually helps us to synchronise the data in a way that if multiple processes would like to access the same window it makes sure that they go in an order. So the program will allow different processes to access the window but it will ensure that it is not happening in the same time. So it is important that the  one-sided function calls are surrounded by this fucntion.

## 1.4 E: One sided communication in a ring

### Goal

- Write a MPI program that uses MPI_Get and MPI_Put to pass data around in a ring.
- Each process creates a window containing an array with numbers [10*rank, 10*rank + 1, ..., 10*rank + 9].
- Each process gets the data from the preceding process and sets this data into the window of the next process.
- Each process prints its final data.

## 2. MPI + OpenMP

## 2.1 MPI + threading methods
In this subsection we will build up upon the introduction of OpenMP we did in the first two weeks and we will see how to include it into MPI. There are numerous reasons we need to dwell into this, however the most important is that in High-performance computing (HPC) the Computer systems feature a hierarchical hardware design. So we need to discuss how the multi- core nodes that are connected via a network can be orchestrated efficiently. We will also see where are the bottlenecks of each approach. Of course we will discuss these challenges through simple examples and not through theory! During this subsection we will also discuss or try to find out whether the hybrid code performs better than MPI code and see how it co-relates to whether the communication advantage outcomes the thread overhead, etc. or not.
Finally. we will also ask ourselves whether the MPI approach is the best approach and whether there are  any other approaches that may offer different speeds or heirarchy within the nodes more efficiently. We will see how the other approaches can provide work load balancing that becomes operative when we are dealing with the large programs that are running on many cores. In the interest of knowing how much effort we will need to make sure that all CPUs are being utilized at maximum efficiency (100%?) i.e there are no sleeping processors, or sleeping GPU, or sleeping threads that are available so that everything is utilized. This would provide us with the opportunity to explore if there is some other  possible approaches to solving these problems more easily and getting the Jjob done in a more efficient way for example with some other language etc. 
This is our introduction to parallel programming, meaning that we will just build up on the simple MPI plus threading methods. 
To exemplify, lets compare I.B.M. Power eight processors with Intel or AMD i,e the classical X-64 architecture. We see that it has much more threads per core. So instead of the usual hyper threading that we find on our laptops where we usually have one thread into the addition to the core; meaning that if we have, for example eight process cores on one circuit, then we may get additional eight threads to be run so that the share cache and so on doubles the performance if we are running an OpenMP program. This implies that the programs and threads share the variables, memory and so on. Hopefully in the initial OpenMP course that we had in the first two weeks it was quite simple to do. 
The two main threading paradigms we will share are:
- MPI + OpenMP
- MPI + MPI-3 shared memory

### MPI + OpenMP
MPI+ OpenMP is usually a better approach for non uniform memory architectures and also in cases where we have the many sockets i.e cache coherent non-uniform memory. It can be optimised in such a way that if we utilize just a smaller amount of MPI threads and the rest are OpenMP. As usual, the pre-requisite is that libraries must be thread safe for C, which is not that complicated because C itself utilizes a lot of internal variables that are allocated near by the compute, so the stack or the nearby heap. In the previous week we have been introduced to MPI and we have seen that MPI has a lot of different message passing routines. So the approach of MPI is to provide all means of communicating from simple to extended ways. The OpenMP or rahter the threading model for it was introduced with MPI-2 so that we can use some threading within the MPI-2. From that  library, we are usually using OpenMPI, but there are also some other vendor specific MPI libraries, especially if you buy from prominent vendors. There are tuned MPI libraries that work best on the cluster that you buy, meaning that it takes into account the topology, the latencies and all architectural differences within the MPI library itself.
So there are three libraries in C that we can initially query
~~~c
int MPI_Init_thread(int * argc, char ** argv[], int thread_level_required,
                    int * thread_level_provided);
int MPI_Query_thread(int * thread_level_provided);
int MPI_Is_main_thread(int * flag);
~~~
However we require certain values prior to this to mention the kind of or rather the level of threading we can get from. So, the required values for example are
~~~c
MPI_THREAD_SINGLE
~~~
- Here only one thread will execute the MPI calls

~~~c
MPI_THREAD_FUNNELED
~~~
- Here only the master thread will make MPI-calls

~~~c
MPI_THREAD_SERIALIZED
~~~
- In this case multiple threads may make MPI-calls, but only one at a time.

~~~c
MPI_THREAD_MULTIPLE
~~~
- Here multiple threads may call MPI, without any restrictions.

## 2.2 E: Calculate pi! Using MPI_THREAD_FUNNLED

### Learning outcomes for the excercise 
We will see through this excercise that with MPI_THREAD_FUNNLED
- It Fits nicely with most OpenMP models
- Expensive loops parallelized with OpenMP
- Communication and MPI calls between loops
- Eliminates need for true “thread-safe” MPI

## 2.3 D:

- Can the parallel scaling efficiency may be limited (Amdahl’s law) by MPI_THREAD_FUNNLED approach?
- Does moving to MPI_THREAD_MULTIPLE come at a performance price (and programming challenge)?

## 2.4 V: Hybrid MPI

### Hybrid MPI+OpenMP Masteronly Style
We saw in the previous exercise and the discussion that the scaling efficiency may be limited by the Amdahl's law. It means that, of course, even though all of the computation actually is parallelised we still  have large chunks of serial code actually still present. Serial code means the code that follows after "#pragma omp for reduction" in the previous example. So the reduction clause is a serial portion of code even though it utilizes parallel threads. But this is the last command and the following MPI_Reduce is actually collective communication as we have already learnt. 

If we are doing something like this in the loop, you for surely get a definite amount of serial code, meaning that we will anyways be limited by the Ahmdal's law in scaling. This directly implies that we cannot utilize the abundant thousands or more cores (even a million) that are popping out each day on new and recent hardwares. 

An efficient solution to these problems would be an overlap. Some kind of region where we could do  MPI simultaneously with doing OpenMP so that we would overcome these communications issues. This can be achieved by the Hybrid MPI+OpenMP Masteronly Style. There are quite a few advantages of using this Hybrid however the most prominent are that:

- There are no message passing inside of the SMP nodes
- There are no topology problems

An efficient example to explain the need and efficiency of this is lets say if we have do a ray tracing in a room. And the problem of ray tracing is that the volume that we are describing is quite complex. So lets say if we have to do the light tracing and reflections that we see from the lightning and so on, we would need to compute for each ray. This is already several gigabytes of memory and if we have just 60 gigabytes of memory per node, then we are limited by memory to solve the problem. So we cannot do large problems with many cores because each core in MPI actually gets its own problem inside it. There is no sharing of the problem among the empty threads, empty processes or core and this is the problem that we would usually solve quite fine with going to MPI+ OpenMP. 
So this tracing is one kind of such problems, which is best done with MPI + OpenMP because the description of environment, which is complex, takes a lot of memory. 

### Calling MPI inside of OMP MASTER
If we would like to do communication, then it is usually best to do OMP master thread. This ensures that one thread only communicates with the SMPI. However, we will still need to do some synchronization. As we learnt in the previous weeks about synchronisation that sometimes in parallel programming, when dealing with multiple threads running in parallel, we want to pause the execution of threads and instead run only one thread at the time. Synchronization means that  whenever we do MPI, the old threads will need to stop at some point and do the barrier.

In OpenMP the MPI is called inside of a parallel region, with “OMP MASTER”• It requires MPI_THREAD_FUNNELED, and we saw in the previous subsection this implies that only master thread will make MPI-calls. However we need to take care that there isn’t any synchronization with “OMP MASTER”! Therefore, with the “OMP BARRIER” normally necessary to guarantee, that data or buffer space from/for other threads is available before/after the MPI call!

~~~c
!$OMP BARRIER
!$OMP MASTER
call MPI_Xxx(...)
!$OMP END MASTER
!$OMP BARRIER
#pragma omp barrier
#pragma omp master
MPI_Xxx(...);
#pragma omp barrier
~~~

We can see above that it implies that all threads are sleeping, and the additional barrier implies the necessary cache flush!

Barriere is necessary and you do, for example, NPI receiving this example here is. And so on, and now we come to the. Question. Can we do, let's say, pure MPI with some shared memory, because we have seen that a lot of. MPI problems comes with the. Problem  description, as I said before, MPI would be a good way to do it. Most protesters are done in such a way that NPI works on them quite well. So why we would do. Shared memory or open MP and tred safety and social programming, if we could still live with MPI Pure and nobody really cares unless you do have problems with the.














