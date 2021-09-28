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

Let us try to furhter consolidate these ideas by implementing them in the following exercise!

## 1.2 E: Rotating information around a ring (non-blocking)

In this exercise you will get to experiment with blocking and non-blocking communication. With use of non-blocking communications we want to avoid idle time, deadlocks and serializations. This is the second part of a two part exercise. 

This is a continuation of the previous exercise with ring communication and when you used blocking communication to solve it. Now you will repeat the exercise but you are now solving the deadlock in an optimal way using non-blocking communication. 

~~~c
#include <mpi.h>

int rank, size;
int snd_buf, rcv_buf;
int right, left;
int sum, i;
MPI_Status status;

MPI_Init(NULL, NULL);
MPI_Comm_rank(MPI_COMM_WORLD, &rank);
MPI_Comm_size(MPI_COMM_WORLD, &size);

right = (rank+1)      % size;
left  = (rank-1+size) % size;

sum = 0;
snd_buf = rank; //store rank value in send buffer
for(i = 0; i < size; i++) 
{
    MPI_Send(&snd_buf, 1, MPI_INT, right, 17, MPI_COMM_WORLD); //send data to the right neighbour
    MPI_Recv(&rcv_buf, 1, MPI_INT, left,  17, MPI_COMM_WORLD, &status); //receive data from the left neighbour
    snd_buf = rcv_buf; //prepare send buffer for next iteration
    sum += rcv_buf; //sum of all received values
}
printf ("PE%i:\tSum = %i\n", rank, sum);

MPI_Finalize();
~~~

## Exercise

1. Substitute `MPI_Send` with `MPI_Issend` (non-blocking synchronous send) and put the wait statement at the correct place. Keep the normal blocking `MPI_Recv`. Run the program. 

* Do you already have any experience with preventing deadlocks? Which methods have you used in the past? Have you ever thought about serialization?

[Jupyter notebook: Ring2](https://mybinder.org/v2/gh/kosl/ihipp-examples/HEAD?filepath=/MPI/Exercise-Ring2.ipynb)

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
We will understand in depth about the arguments of these functions in the following exercise. But before we get into that another important thing that we need to discuss is the Synchronization. If you remember we discussed this concept briefly in the (number) week when we were learning about the concepts of OpenMP. 
In MPI in one sided communication (image S24)  the target process  calls the function to create the window in order to give access of its memory to other processes. However, in the case of multiple users it is already quite plain to see that if these users try to simultaneously access this data can already lead to some problems. For example, lets say two users access the window to put data using the MPI_Put function this is clealry a race condition that needs to be avoided. This is where synchronisation comes into the play. So in order to avoid this before and after each 'one sided communication' function i.e MPI-Get and MPI_Put we need to use this function
~~~c
MPI_Win_fence(0, MPI_Win win);
~~~
This function actually helps us to synchronise the data in a way that if multiple processes would like to access the same window it makes sure that they go in an order. So the program will allow different processes to access the window but it will ensure that it is not happening in the same time. So it is important that the  one-sided function calls are surrounded by this fucntion.

## 1.4 E: One sided communication in a ring

You are already familiar with communication in a ring. In this exercise the goal is to substitute nonblocking communication with one sided communication. 

We want to substitute calls to send and receive routines by using MPI_Put or MPI_Get. So we have 2 options:

1. The process that previously called send, now calls **MPI_Put**: The send buffer is a local buffer and the receive buffer must be a window. 

2. The process that previously called receive, now calls **MPI_Get**: The send buffer is a window and the receive buffer is a local buffer. 

For this exercise, you will use the **1.** option. So what you need to do is create a window for the receive buffer and substitute the sending and receiving by calling MPI_Put on the process that previously called MPI_Send. Also don't forget to do synchronization with MPI_Win_fence. 

### Exercise

1. Go to the exercise and fill out the skeleton to create all `rcv_buf` as windows in their processes. 

2. Substitute the Issend/Recv/Wait with Win_fence/Put/Win_fence sequence. 

### Discussion

There are two solutions to substituting nonblocking communication with one-sided communication. Do you have any idea, why would we preffer using MPI_Put instead of MPI_Get? What is your preferred way, and why?

[Jupyter notebook: One sided communication](https://mybinder.org/v2/gh/kosl/ihipp-examples/HEAD?filepath=/MPI/One-sided-ring.ipynb)

## 1.5 Q: Do you understand advanced communication in MPI?

This quiz will test your knowledge on MPI’s advanced communication. 

### Question 1
Which of the following MPI communication types suspends execution of the calling program until the current communication is completed?
 
* Blocking
* Nonblocking
* Asynchronous
* None of the above

### Question 2
A message from a non-blocking send MPI_Isend is safe to be accessed immediately after the MPI_Irecv command.
 
* True
* False

### Question 3
What is a valid reason for wanting to use one-sided communication in MPI?
 
* Less synchronization overhead
* Lower hardware latency
* Easier programming of irregular communication events
* All of the above

### Question 4
Which of the following steps comes first in setting up MPI one-sided communication?
 
* Starting a communication interval using MPI_Win_fence
* Defining a transfer with put or get
* Initializing a window
* The order doesn’t matter

### Question 5
If you execute an MPI_Put, where is the send and where is the receive buffer?
 
* The sendbuf is a local buffer and the rcvbuf must be a window.
* The sendbuf is a window and the rcvbuf is a local buffer.

### Question 6
What units are used to define the size of a window in a call to MPI_Win_create?
 
* Bytes
* The units specified by the MPI_Datatype argument
* Words

### Question 7
Immediately after returning from a MPI_Put call, it is safe to overwrite the buffer containing the data that was sent.
 
* True
* False

### Question 8
What is the simplest way to end a one-sided communication interval and re-synchronize, in just one step?

MPI_Win_ __ ?

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

[Jupyter notebook: Threading methods](https://mybinder.org/v2/gh/kosl/ihipp-examples/HEAD?filepath=/MPI/Threading-methods.ipynb)

## 2.2 Calculate pi! Using MPI_THREAD_FUNNELED

The safest and the easiest way to use threading is to use `MPI_THREAD_FUNNELED`. This level of thread safety assures multithreading, but only the main thread makes the MPI calls (the one that called MPI_Init_thread). All MPI calls are made by the master thread, outside the OpenMP parallel regions or in OpenMP master regions. 

This example notebook shows how to calculate the value of pi by solving this integral approximation. 

$$Pi = \int_{0}^1 \frac{4}{1+x^2} dx \approx \sum_{i=0}^{n-1}f(x_i+h/2)h$$

You have already computed this with [OpenMP](https://www.futurelearn.com/courses/interactive-hands-on-introduction-to-parallel-programming/1/steps/1147436) and [MPI](https://www.futurelearn.com/courses/interactive-hands-on-introduction-to-parallel-programming/1/steps/1169705) in the previous weeks. What we did in this example is use both. The goal is to minimaly use MPI for inter-node communication and inside the node to do everything by shared memory computing with OpenMP. This is the complete code shown below. 

~~~c
#include <omp.h>
#include <mpi.h>
#include <stdio.h>
#define N 1000000

int main(int argc, char *argv[])
{
  int rank;
  int size;
  double subsum = 0.0;

  MPI_Init(&argc, &argv);
  MPI_Comm_rank(MPI_COMM_WORLD, &rank);
  MPI_Comm_size(MPI_COMM_WORLD, &size);
  omp_set_num_threads(2);
  
  int nthreads = omp_get_num_threads();
  #pragma omp parallel
  {  
    int tid = omp_get_thread_num();
    printf("Thread %d within rank %d started.\n", tid, rank);
    #pragma omp for reduction(+:subsum)
    for(int i = rank; i < N; i += size*nthreads)
      {
        double x = (i+0.5)/N;
        subsum += 4/(1 + x*x);
      }
  }
  double sum;
  MPI_Reduce(&subsum, &sum, 1, MPI_DOUBLE, MPI_SUM, 0, MPI_COMM_WORLD);
  if (rank == 0)
     printf("pi = %.10lf\n", sum/N);
  MPI_Finalize();
  return 0;
}
~~~

When we have threading it is important to think about how to split up the workload. You can see how the workload is split with this line below so we follow the same principles asked by the MPI. If we have `nthreads`, then we need to increase the jump to the next chunk by the value of `size*nthreads`. Each chunk is computed this way. 

~~~c
for(int i = rank; i < N; i += size*nthreads)
~~~

The collection of `subsum`, that is actually a shared variable within the threads and starts for each MPI process as `0.0`, is collected from each thread in one rank, so we get subsum for each MPI process at the end of OpenMP parallel region. After that the master thread reduces this `subsum` together as `sum` with MPI. 

We run this program on 3 processes and by setting 2 threads inside the code we have 6 threads in total within 3 ranks (rank 0, 1 and 2). 

~~~c
mpicc -fopenmp pi-hybrid.c && mpirun -n 3 –allow-run-as-root a.out
~~~

Look and run the code in the notebook at the end of this article. 

### Learning outcomes for the exercise

This program was done in the first way of threading methods (MPI + OpenMP). 

* This way of parallelization that we just did in the notebook example fits nicely with most OpenMP models. 
* Expensive loops are parallelized with OpenMP and that is faster. You can utilize many of the processor cores, so doubling the number of threads, instead of cores. So running programs this way surely has some potential. 
* Communication and MPI calls between loops
* Eliminates need for true “thread-safe” MPI

[Jupyter notebook: Compute Pi Funneled](https://mybinder.org/v2/gh/kosl/ihipp-examples/HEAD?filepath=/MPI/Compute-Pi-Funneled.ipynb)

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

In OpenMP the MPI is called inside of a parallel region, with “OMP MASTER”• It requires MPI_THREAD_FUNNELED, and we saw in the previous subsection this implies that only master thread will make MPI-calls. However we need to take care that there isn’t any synchronization with “OMP MASTER”! There is no implicit barrier in the master workshare construct. Therefore, with the “OMP BARRIER” normally necessary to guarantee, that data or buffer space from/for other threads is available before/after the MPI call!

~~~Fortran
!$OMP BARRIER
!$OMP MASTER
call MPI_Xxx(...)
!$OMP END MASTER
!$OMP BARRIER
~~~

~~~c
#pragma omp barrier
#pragma omp master
{
    MPI_Xxx(...);
}
#pragma omp barrier
~~~

We can see above that it implies that all threads are sleeping, and the additional barrier implies the necessary cache flush! The barrier is necessary to prevent data races. 

Through the following exercise we will see why the barrier is necessary. 

### Example with MPI_recv

In the example, the master thread will execute a single MPI call within the OMP_MASTER construct, while all the other threads are idle. As illustrated barriers may be required in two places:

* Before the MPI call, in case the MPI call needs to wait on the results of other threads. 
* After the MPI call, in case other threads immediately need the results of the MPI call. 

~~~Fortran
!$OMP parallel
    !$OMP do
        do i=1, 1000
            a(i) = buf(i)
        end do
    !$OMP end do nowait

    !$OMP barrier
    !$OMP master
        call MPI_Recv(buf, …)
    !$OMP end master
    !$OMP barrier

    !$OMP do
        do i=1, 1000
            c(i) = buf(i)
        end do
    !$OMP end do nowait
!$OMP end parallel
~~~

~~~c
#pragma omp parallel
{
    #pragma omp for nowait
    for (i = 0; i < 1000; i++)
        a[i] = buf[i];

    #pragma omp barrier
    #pragma omp master
    {
        MPI_Recv(buf,....);
    } 
    #pragma omp barrier

    #pragma omp for nowait
    for (i = 0; i < 1000; i++)
        c[i] = buf[i];
}
~~~



## 2.5 Q: Quiz on Hybrid programming with OpenMP and MPI

Do you understand how OpenMP can be included and used with MPI? Test your understanding of this topic with this quiz.

### Question 1
An MPI process is generally single-threaded unless the code has been augmented with multithreading directives or library calls.

* True
* False

### Question 2
If MPI_Init_thread returns MPI_THREAD_FUNNELED, MPI messages can only be passed between main threads.

* True
* False

### Question 3
Which argument to MPI_Send my be used to identify the destination thread?

* rank
* count
* tag
* communicator

### Question 4
MPI messages can be passed between any two threads, provided each is enclosed in an omp single construct, when MPI_Init_thread returns what value?

* MPI_THREAD_SINGLE
* MPI_THREAD_FUNNELED
* MPI_THREAD_SERIALIZED
* MPI_THREAD_MULTIPLE


## 3. User defined datatypes

## 3.1 Derived data type
So far we have learnt to send messeages that were a continuous sequence of elements and  mostly of the basic data types such as buf, count etc. In this section we will learn how to transfer of any data in memory in one message. We will learn to communicate strided data i.e a chunk of data with holes between the portions and how to communicate various basic datatypes within one message.

So if we have many different types of datatypes such as int, float etc. with gaps how would (image S4)we do that communication in one way with one command. To do this we would first of all need to start by describing the memory layout that we would like to transfer.
Following this the processor that compiled the derived type layout will then do the transfer for us in the loop in a correct way. This can even be acheived with all kinds of broadcasts.

Since we would not need to copy data into a continuous array, to be transferred as a single chunk of memory, there is no waste of memory bandwidth in such a way. Therefore derived types are usually structures of 
- vectors
- subarrays
- structs etc.

Or they could be simple types that are being combined into one data layout without the need of copying into one piece to be transferred efficiently or in one block of message. It is not uncommon to have a message of sizes over 60 or more kilobytes. So, if you would like to transfer the results of some programs that could be larger files then actually this is the most efficient way to do it. Of course there are other altenatives such as writing the results into file and to open the file. Quite often the codes do not actually return results, but they just write their results into a file, and eventually we'll need to combine the results into one representation. This is quite similar to how we do it in profiler or tracer creating a file for each processor. So it is already quite easy to understand that if we are debugging a code with  two thousand cores (which is not that big) we will easily end up with two thousand files to be read that need to be interpreted that will definitely take some time. We will learn about it more in the following subsections of parallel I/O.

### Derived Datatypes — Type Maps

A derived datatype is logically a pointer to a list of entries. However, once this data type has been saved somewhere, it is not communicated over the network. When the need comes we just use this type simply as it would be a basic data type. However the only prerequisite is that for each of these data types we need to compute the displacement. (table S6) Quite obviuosly MPI does not communicate these displacements over the network.

(table S7) Here you can see the displacement of the basic datatypes such as int, char etc. For e.g MPI_INT can be displaced for four or eight bytes and MPI_doubles can be displaced for sixteen bytes  and so on. A derived datatype describes the memory layout of, e.g. structures, common blocks, subarrays and some variables in the memory etc.

### Contiguous Data
The is the simplest derived datatype as it consists of a number of contiguous items of the same datatype
In C we use the following function to define it

~~~c
int MPI_Type_contiguous(int count, MPI_Datatype oldtype, MPI_Datatype *newtype)
~~~

### Committing and Freeing a Datatype

Before a dataytype handle is used in message passing communication, it needs to be committed with MPI_TYPE_COMMIT. This need be done only once by each MPI process. So when we commit, this implies that data type recites a description inside that can be used over as we mentioned earlier simliar to a basic datatype. However, if at some point  this changes or we would like to release some memory, or if the usage is over we may call MPI_TYPE_FREE() to free the datatype and its internal resources.
The routine used is as follows

~~~c
int MPI_Type_commit(MPI_Datatype *datatype);
~~~



### Example

Here in this example (S5) we can see the real need for derived data types. We have a structure of fixed size integers values and then there are double values. So this is one single data that we would like to describe as data type so that we could then send this structure in one command i.e send or receive. We do not really care whether it is blocking or blocking at this point. So, in order to achieve this we describe the data type called "buf_datatype". This is actually a name that we commit to this type. So we push the type after we create it and compile it to the MPI subsystem. Afterwards, the subsystem refers to that data type inside the system itself and knows how to convert, the integers etc. with the type that we use inside. Of course, there can also be some kind of gaps that we would not actually see if we are using some other languages such as Fortran and sometimes we even have memory alignments for it. So there maybe a gap of one integer (image S5) to start. But this is not an error on our part but it just an adjustment, like some kind of performance adjustment so the next array starts at the multiple of four. So while describing such an array the MPI knows how to do it most efficiently.

## 3.2 E: Derived data type

In this exercise you will pass data around a ring with a derived datatype instead of an integer or an array like we did so far. You send and receive buffer will be a struct with two integers. 

### Exercise

You will use a modified pass-around-the-ring program which already includes a struct with two integers. In the exercise you will:

1. Produce a new datatype that can be used as a buffer with the routines that you have learned in the previous step. 

2. Initialize the struct intigers with `rank` and `10*rank`. Therefore we will pass around two values and calculate two separate sums. 

3. Use the new datatype in the send and receive routine calls. Currently, the data is send with the description `snd_buf, 2, MPI_INTEGER` which you must modify by using a derived datatype and with a type map of “two integers”. 

[Jupyter notebook: Derived datatypes](https://mybinder.org/v2/gh/kosl/ihipp-examples/HEAD?filepath=/MPI/Derived-datatypes.ipynb)

## 3.3 V/A: Layout of struct data types


### Vector datatypes
(image S13)

What we learnt so far in the previous subsection and the exercise were more like continous vectors. Sometimes we would need to communicate vectors with holes that we do not want to be trnasferred. This implies that we would not send each element but just selected elements or sequence of elements. Therefore the blocklength and the offset of each can be used to create a "stride". When we want to communicate just a portion of a contionus chunk of memory the destination and source may not be the same. Usually we have one element to receive the results back from the array of cluster. As we saw in the previous pi example how the integrals were colelcted back so that we could see the complete sums we could such vector datatypes. We suse the following routine for vector datdtypes:

~~~c
int MPI_Type_vector(int count, int blocklength, int stride, MPI_Datatype oldtype, MPI_Datatype *newtype)
~~~

The structure of the routine is similiar to most we have learnt previously. So 
- 'count' suggests how many elements. 
- 'blocklength' is the number of elements per block.
- 'stride' is the offset to the next portion of the result. 
- the datatype of course we could also have only one type and it could be a derived one. Of course we can strided array of slots and integers and subsequently we will get a * newtype created that can be used in send and recieve routines.


### Struct datatype

So we you could have old types that are of different sizes and then we could combine two old types into a single vector or block that can be also with holes and these holes will not be communicated. It would be quite often the way how to describe out type instead of doing what we saw earlier. The previous method is not optimal for large numbers of such kinds of array. In such cases we use the struct datatypes so that communication is executed in the correct way. 
The routine for this datatype looks like  

~~~c
int MPI_Type_create_struct(int count, int *array_of_blocklengths, MPI_Aint *array_of_displacements,
MPI_Datatype *array
~~~

(image S15)
This is how memory layout of struct data types could look like with gaps inside that we don't actualy want, but are imposed by the compiler itself or the underlying operating system or hardware processor.

Let us assume that we have the following parameters. 
- count = 2
- array_of_blocklengths = ( 3, 5 )
- array_of_displacements = ( 0, addr_1 – addr_0 ) 
- array_of_types = ( MPI_INT, MPI_DOUBLE )
In this case the, prototype for fixed memory layout of the struct datatype would be as following
~~~c
struct buff
{ int i_val[3];
double d_val[5];
}
~~~

## 3.4 Computing displacements

We actually need to compute the displacements. So if we would like to see the size of each structure in bytes, that would need to be prescribed as a buffer the displacement needs to be known.
In MPI1 before we started with derived types we saw there were some differences with MPI3 and MPI1 similar to kind of problems that fortran had. These issues are now resolved with MPI3.1. Now there is a deprecated way of doing upper and lower bound for the structure. These are the recommended way how to compute the distance from one type to another. The standard procedure for obtaining displacement is 

~~~c
array_of_displacements[i] := address(block_i) – address(block_0)
~~~

And in order to get the absolute address we would need the routine

~~~c
int MPI_Get_address(void* location, MPI_Aint *address)
~~~

In the MPI3.1 version the relative displacement can be calculated as the diffference between absolute address 1 and absolute address 2  and the new absolute address can be denoted as the sum of the existing absolute address and the relative displacement. So,

- Relative displacement:= absolute address 1 – absolute address 2
with the routine that looks like
~~~
MPI_Aint MPI_Aint_diff(MPI_Aint addr1, MPI_Aint addr2)
~~~

- New absolute address := existing absolute address + relative displacement \
with the routine that looks like
~~~c
MPI_Aint MPI_Aint_add(MPI_Aint base, MPI_Aint disp)
~~~

### Example

In example we see how we compute the address. 'Aint' address variable or 'disp' displacements could be computed by prescribing the start of the first element. The 'snd_buf.i[0]' isactually the correct way of defining that address. 
~~~c
struct buff {
    int i[3];
    double d[5];
} snd_buf;

MPI_Aint iaddr0, iaddr1, disp;

MPI_Init(NULL, NULL);

// the address value &snd_buf.i[0] is stored into variavle iaddr0
MPI_Get_address(&snd_buf.i[0], &iaddr0);
MPI_Get_address(&snd_buf.d[0], &iaddr1);
disp = MPI_Aint_diff(iaddr1, iaddr0);

MPI_Finalize();
~~~

## 3.5 D: Which is the fastest neighbor communication with strided data?

Using derived datatype handles

- Copying the strided data in a contiguous scratch send-buffer, communicating this send-buffer into a contiguous recv-buffer, and copying the rcv-buffer back into the strided application array

- And which of the communication routines should be used?

## 3.6 Q: Quiz on derived datatypes

This quiz tests your knowledge of user derived datatypes.

### Question 1
Which of the following general datatypes assumes that the stride is equal to 1?
 
* Contiguous
* Vector
* Struct

### Question 2
Which of the following general datatypes may constist of more than one basic datatype?
 
* Contiguous
* Vector
* Struct

### Question 3
If you have an array of a structure in your memory, how would you describe this?
 
Using function MPI_ __ for the structure and the  __  argument in the MPI communication procedure for the size of the array.

### Question 4
Which additional MPI procedure call is required, before a newly generated datatype handle can be used in message passing communication?

* MPI_Type_contiguous
* MPI_Type_create_resized
* MPI_Type_commit
* MPI_Type_free

## 4. Parallel File I/O

## 4.1 E: Pass-around-the-ring exercise

In this exercise you will pass data around a ring with a derived datatype instead of an integer or an array like we did so far. Your send and receive buffer will be a struct with one integer and one floating point. 

### Exercise

You will use a modified pass-around-the-ring program which already includes a struct with one integer and one floting point. In the exercise you will fill out the blank spaces and modify the call routines to use the new datatype. 

1. Set MPI datatypes for sending and receiving partial sums with the routines that you have learned in the previous step. You should use `MPI_Type_create_struct`. You are using the same fixed memory layout for send and receive buffer. 

2. Initialize the struct intigers with `rank` and `10*rank`. Therefore we will pass around two values and calculate two separate sums: rank integer sum and rank floating point sum. 

3. Use the new datatype in the send and receive routine calls. 

[Jupyter notebook: Derived datatypes 2](https://mybinder.org/v2/gh/kosl/ihipp-examples/HEAD?filepath=/MPI/Derived-datatypes-2.ipynb)

## 4.2 A: Brief explanation of size, extent and alignment rules

Before we go further into the Parallel file I/O we need to get some basic knowledge about the terminology of size, extent, true extent etc. and get some background about the alignment rules.  
- Size is the number of bytes that have to be transferred.
- Extent represents the spans from first to last byte including all the holes.
- True extent spans from first to last true byte but in this case excluding holes at beginning and the end.
For most of the basic datatypes the Size = Extent = number of bytes used by the compiler. This can be seen easily in the image (S25)

Extent, alignment and holes can be problems for some compilers or architecture, especially, these are optimized. However, MPI3 has a lot of these problems fixed by introducing new interfaces that solve certain issues and offer a better usable interface. However, in standard these parameters always hold true:
- There are automatic holes at the end for necessary alignment purpose
- There can be additional holes at begin and by lb and ub markers: MPI_TYPE_CREATE_RESIZED
- And as mentioned already, basic datatypes: Size = Extent = number of bytes used by the compiler. 

### Alignment rule, holes and resizing of structures 
At times, the compiler might add additional alignment holes either within a structure (for example between a float and a double) or at the end of a structure (i.e after elemets different sizes). However, alignment holes are important at the end when using an array of structures!
To imply this if an array of structures (in C/C++) or derived types (in Fortran) should be communicated then it is recommended that we create a portable datatype handle and additionally MPI_TYPE_CREATE_RESIZED to this datatype handle. 
(EXAMPLE)
Quite often, due to the alignment gaps the holws may cause a signigicant loss of bandwidth. Technically, by definition, MPI is not allowed to transfer the holes. There we need to fill holes with dummy elements.
(EXAMPLE)

Sometimes certain problems might arise such as the MPI extent of a structure is not the same or equal as the real size of the structure. This could be because the MPI adds n alignment hole at the end a because the MPI library has wrong expectations about compiler rules that is 
- For a basic datatype within the structure
- For the allowed size of the whole structure (e.g. multiple of 16)

To rectify this problem we can call the 
~~~c
MPI_Type_create_resized(...);  //with lb=0 and
new_extent = sizeof(one structure);
~~~

~~~Fortran
integer(kind=MPI_ADDRESS_KIND) :: address1, address2, lb, new_extent
call MPI_Get_address(my_struct(1), address1, ierror)
call MPI_Get_address(my_struct(2), address2, ierror)
new_extent = MPI_Aint_diff(address2, address1)
lb = 0
call MPI_Type_create_resized(&old_struct_type, lb, new_extent, correct_struct_type, ierror)
~~~

### Example: Correcting problem with array of structures

This is a example program where we have an array of structures containing a double and an integer. A new datatype handle is implemented by resizing the old one and doing the commit. We use the new resized datatype handle in the send and receive call routines. 

These are the important new additions to the code:

~~~c
MPI_Datatype send_recv_type, send_recv_resized;
...
MPI_Type_create_struct(2, ..., &send_recv_type);
MPI_Type_create_resized(send_recv_type, (MPI_Aint) 0, (MPI_Aint) sizeof(snd_buf[0]), &send_recv_resized);
MPI_Type_commit(&send_recv_resized);
~~~

~~~Fortran
integer(kind=MPI_ADDRESS_KIND) :: first_var_address, second_var_address, lb, extent
integer :: send_recv_type, send_recv_resized
...
call MPI_Type_create_struct(2, ..., send_recv_type, error)
call MPI_Get_address(snd_buf(1), first_var_address, error)
call MPI_Get_address(snd_buf(2), second_var_address, error)
lb = 0
extent = MPI_Aint_diff(second_var_address, first_var_address)
call MPI_Type_create_resized(send_recv_type, lb, extent, send_recv_resized, error)
call MPI_Type_commit(send_recv_resized, error)
~~~

[Jupyter notebook: Correcting problem with array of structures](https://mybinder.org/v2/gh/kosl/ihipp-examples/HEAD?filepath=/MPI/Correcting-array-of-structures.ipynb)

## 4.3 V:Parallel file I/O


Many parallel applications need a coordinated parallel access to a file by a group of processes and at times this could be simultaneous. Frequently all the processes may read/write many (small) non-contiguous pieces of the file i.e. the data may be distributed amongst the processes according to a partitioning scheme. Writing of the results can be done by all compute nodes at once or even compute cores, writing their own portion of the result and having a huge amount (not by size but by the number) of files is very inefficient in such a way.
In this subsection we are addressing classic File I/O. We will when we will be using such kind of IO and for what purpose and are there any other means to do the same. Although there are some object file systems also being used in HPC that do not have a clasiccal file layout and we would need to address, such objects or chunks of data that are saved into the file system differently but we will not adress these issues here.

The are quite a lot of problem of file systems with high performance computing. Usually, large codes read large data as input and  write large data as output. Since many computations are done iteratively, meaning that they are convergent or they progress the solution in a stepwise manner the storage can be occupied quite fast. For example if we are  simulating a system of particles in HPC or solving a fluid equations or doing some kind of time evolution simulation we would need to  store large amounts of data . So finding petabytes of disks to be full is not uncommon. A lot of data being saved to the disk should not impact the computation i.e if we would like to store results into disk, it should not impact communication and the overall progress of the code.

This is where the Parrallel File I/O comes into play so that we could save results by for example a timestep, or by proccessors that are already combined together at progress or computation time. 

So it is quite difficult if we have a running large code that  would  like to store all the resources or at least the state of current simulation. Since quite often it is not just the results that are being saved, but also intermediate results or steps at selected times.
So for example, if a simulation crashes, it can be restarted at that point. This is problematic owing to the fact that the usual scheduling on clusters limits the time of how long one code can run and usually that is actually limited to twenty four hours and  for some clusters it could be even smaller number. In an case where we would have code that we would like to run for a month it would be meticulous if it need to stop at some point and we can start from the previous state and continue simulation. This would imply that somehow we need to store the last state into the disk and restart from that so-called check point or saving the current state. 
This is overcome with  Parallel file I/O that lowers the number of files and performs the  writing in an efficient way. This is acheived  because  the parallel file systems allows us to write to several file servers at the same time through metadata orchestrator. When we open a file the metadata server informs the node (that it's handling network file system) to which of the available data file or targets do they need to send the data. If there are thousands of compute nodes, then there are let's say, at least dozens of file servers that handle hundreds of disks to allow parallel file transfers. 

Thus, at any given time, many of compute nodes are sending network files over through the file server. Therefore in Parallel File I/O we could actually write a chunks of the single file for several of those compute nodes. Reading and writing files are analological to sending and receiving messages respectively that we have learnt earlier. The only exception in that this is a persistent memory, meaning that such kind of writing is done correctly. Additionaly for codes that do computation in parts meaning, that if we have a code  that does domain composition before we start,  then some of the compute nodes or compute cores, already know which portion of the file needs to be read in order to start processing. In this case having a single file for saving timestep is something that it is very useful for large clusters that would like to handle millions of files, with the minimum number of (feets)????. 

This allows us to use parallel I/O functions that do not block computation allowing us to to put overlapped computation and reading/writing through it. This is possible through some standard formats that look like a readable file at the end; not just by the code that has written it, but also for general purpose file readers. For example, a prominent format for the file that is Parallel is HDF, i.e hierarchical data format. It is used  quite often by many codes and it provides MPI Parallel I/O. Consequently, instead of learning of what we can do with the Parallel I/O, it would be more efficient if we learn how to do MPI I/O with HDF format in parallel way. The MPI I/O features provided by MPI standards are actually part of hierarchical data formats and other net CDF and similar formats. To summarise the MPI-I/O features are to provide a high-level interface to support:
-  data file partitioning among processes
-  transfer global data between memory and files (collective I/O)
-  asynchronous transfers
-  strided access

Some basic principles of MPI-I/O are that
- MPI file contains elements of a single MPI datatype (etype)
- partitioning the file among processes with an access template (filetype)
- all file accesses transfer to/from a contiguous or non-contiguous user buffer (MPI datatype)
- nonblocking / blocking and collective / individual read / write routines
- individual and shared file pointers, explicit offsets
- binary I/O
- automatic data conversion in heterog. systems
- file interoperability with external representation

(image S9)

So we will learn these principles of MPI I/O to see that we could create a file that perhaps looks like a single file. However in reality there are many of the processes that started work on different nodes actually open the same file and writes the results into one physical file, while a logical way there may be gaps that are not allowed to be used or to be written. This is because the striking from a logical way to physical way is done in such a way that we already know what place we can save our portion of the file. 

(image S10)
Simply put, we need to know the size of one chunk and the file system just needs to move the file pointer to the correct place where it writes . This is quite simple because even the  serial file I/O allows us to move backwards and forwards in the file if it is in a binary way so that we know, with what offset we can expect something. In this case we could have a single file that can create many cores writing at the same time to the different servers and in the end it looks like a single file for you. To ease out these terms 
- A file is an an ordered collection of typed data items
- etypes refer to the the unit of data access and positioning / offsets that can be any basic or derived datatype. It is usually with non-negative, monotonically non-decreasing, non-absolute displacement and is generally contiguous but it does not need to be typically same at all processes.
- filetypes are the basis for partitioning a file among processes. They define a template for accessing the file. They are usualy different at each process.
- Each process has its own "view" that is defined by a displacement, an etype, and a filetype. The file type is repeated,starting at displacement.
- An "offset is the position relative to current view, in units of etype.

To open and MPI file we use the routine 

~~~c
MPI_FILE_OPEN(comm, filename, amode, info, fh)
~~~

and the parameters in this routine are

- MPI_FILE_OPEN is collective over comm
- filename’s namespace is implementation-dependent
- filename must reference the same file on all processes
- process-local files can be opened by passing MPI_COMM_SELF as comm
- returns a file handle fh

However, the default is:
- displacement = 0
- etype = MPI_BYTE
- filetype = MPI_BYTE

We prescribe the way of discplacements that is needed. You can check the PDF in the attachment for the list of all the Access Modes. 

Sometimes we might need to close or delete a file. We use the follwing routines for
- Close: collective
~~~c
MPI_FILE_CLOSE(fh)
~~~

- Delete 
~~~c
MPI_FILE_DELETE(filename, info)
~~~
However, if access mode "amode=MPI_DELETE_ON_CLOSE" was specified in MPI_FILE_OPEN then the file is obvioudly automatically deleted on close. 

We will learn further about the MPI-I/O principles through a simple example. 

## 4.4 E: Four processes write a file in parallel

In this exercise your program should write a file in parallel using four processes. 

### Exercise

1. Each process should write its rank (as one character) ten times to the offsets = `rank + i * size`, where `i=0..9`. 

2. Each process uses the default view. 

### Tip

When checking if your file is correctly written, you should:

- use `ls -l` to look at the number of bytes and it should be 40 bytes

- use `cat my_file` to look at the content of your file and the expected result is `0123012301230123012301230123012301230123`

- use `rm my_file` to remove the file before running the program again because it will rewrite the file

[Jupyter notebook: Write a file in parallel](https://mybinder.org/v2/gh/kosl/ihipp-examples/HEAD?filepath=/MPI/IO/Write-file-parallel.ipynb)

