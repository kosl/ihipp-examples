# Appendix

## Solutions to Quizzes

Correct answers to questions in Quizzes are marked in bold.

### Quiz: Intro to parallel programming

This quiz tests your knowledge of basic parallel programming principles and paradigms.

#### Question 1
What are typical advantages of using parallel codes?

* Faster execution than for serial codes
* Large amounts of required memory can be distributed
* **All of the above**

#### Question 2
What is a necessary condition for the successful parallelization of the code?

* **Work can be divided into relatively independent tasks with little communication**.
* Work can be divided into totally independent tasks with no communication.

#### Question 3
OpenMP is a good choice for code parallelization if (multiple choice answer):

* **It can be run on a shared memory machine**
* It can be run on a distributed memory machine
* The data of the problem can't be partitioned
* **The data of the problem can be divided into chunks**

#### Question 4
What limits the scaling of parallel codes, i.e., their speed up? (multiple choice answer)

* **Communication bottlenecks**
* Memory resources
* **Synchronization overhead**
* **Serial portion of the code**
* Number of processors/cores

#### Question 5
What is the ideal speed up (according to Amdahl's law) for a code that has a parallel portion of 75%?

* 2
* 3
* **4**
* 5

For an infinite number of processors the speed up can be calculated by the formula $\frac{1}{1-p}$ or in this case $\frac{1}{1-0.75}=4$.

### Quiz: Intro to OpenMP

This quiz tests your knowledge of the basic principles and programming/execution model of OpenMP.

#### Question 1
Which of the following about OpenMP is incorrect?

* OpenMP is an API that enables explicit multi-threaded parallelism
* The primary components of OpenMP are compiler directives, runtime library, and environment variables
* OpenMP implementations exist for the Microsoft Windows platform
* **OpenMP is designed for distributed memory parallel systems and guarantees efficient use of memory**
* OpenMP supports UMA and NUMA architectures

OpenMP is not designed for distributed memory parallel systems.

#### Question 2
OpenMP’s execution model is the *fork-join model* of parallel execution.

* **True**
* False

#### Question 3
What statements about the OpenMP execution model are correct? (multiple choice answer)

* **threads can exist only within the resources of a single process**
* threads can exist within the resources of multiple processes
* **the maximum number of threads is equal to the number of processor cores times threads per core available**
* the number of threads to use can't be defined by the user
* a master thread is executed in parallel until the first sequential region construct is encountered
* **a master thread is executed sequentially until the first parallel region construct is encountered**

#### Question 4
Which flag has to be used to tell the `gcc` compiler to take OpenMP directives into account?

* `#pragma omp parallel`
* `./openmp`
* `-openmp`
* **`-fopenmp`**
* None of the above

#### Question 5
Which of these is a correct way to set the number of available threads for an OpenMP program to 4?

* In an OpenMP program, use the library function `omp_get_num_threads(4)` to set the number of threads to 4 at the beginning of the main function.
* In an OpenMP program, use the library function `num_threads(4)` to set the number of threads to 4 at the beginning of the main function.
* **In bash, `export OMP_NUM_THREADS=4`**
* In an OpenMP program, use the library function `omp_max_threads(4)` to set the number of threads to 4 at the beginning of the main function.

All the above library functions can't be used at the beginning of the main function to set the number of available threads.

### Quiz: Intro to MPI

This quiz tests your knowledge of the basic principles and programming/execution model of MPI.

#### Question 1
What is Message Passing Interface (MPI) in principle?

* a language for message passing 
* a library for message passing
* **a specification a library for message passing**

MPI is in principle a standard or specification for message passing libraries.

#### Question 2
What statements about point to point communication and collective communication in MPI are correct? (multiple choice answer)

* **in point to point communication only two processors take part**
* in point to point communication many processors can take part
* collective communication can be from one to one, one to many, many to one, or many to many processors
* **collective communication can be from one to many, many to one, or many to many processors**

#### Question 3
In a blocking MPI routine the call returns only after completion of operations.

* **True**
* False

In blocking routines the call returns only after the data is sent out from user buffer to the system buffer in case of `MPI_Send` (or received by the user buffer from the system buffer in case of `MPI_Recv`).

#### Question 4
What is the difference between `MPI_Bcast` and `MPI_Scatter` routines?

* `MPI_Scatter` sends the same piece of data to all processes, `MPI_Bcast` sends chunks of data to different processes
* **`MPI_Bcast` sends the same piece of data to all processes, `MPI_Scatter` sends chunks of data to different processes**
* There is no difference, the result of both routines is the same

#### Question 5
What is the correct syntax to run an MPI program `prg` with (on) 4 processes (processors)?

* `./prg -np 4`
* **`mpirun -np 4 ./prg`**
* `OMP_NUM_THREADS=4 mpirun ./prg`
* `OMP_NUM_THREADS=4 ./prg`

MPI programs are typically run with the `mpirun` command followed by the flag `-np` to specify the number of processes (processors).

### Quiz on OpenMP basics

We just covered the basics of OpenMP, runtime functions, constructs and directive format. This quiz tests your knowledge of OpenMP basics.

#### Question 1
Directives appear just before a block of code, which is delimited by:
 
* `( … )`
* `[ … ]`
* **`{ … }`**
* `< … >`

#### Question 2
Which of these is a correct way for an OpenMP program to set the number of available threads to 4?
 
* At the beginning of an OpenMP program, use the library function `omp_get_num_threads(4)` to set the number of threads to 4.
* At the beginning of an OpenMP program, use the library function `num_threads(4)` to set the number of threads to 4.
* **In bash, `export OMP_NUM_THREADS=4`**.
* At the beginning of an OpenMP program, use the library function `omp_num_threads(4)` to set the number of threads to 4.

#### Question 3
Variables defined in the shared clause are shared among all threads.

* **True**
* False

#### Question 4
When compiling an OpenMP program with gcc, what flag must be included?

* **`-fopenmp`**
* `-o hello`
* `./openmp`
* None of the answers

#### Question 5
Code in an OpenMP program that is not covered by a pragma is executed by how many threads?

* **Single thread**
* Two threads
* All threads

#### Question 6
If a variable is defined in the private clause within a construct, a separate copy of the same variable is created for every thread.

* **True**
* False

#### Question 7
How many iterations are executed if 4 threads execute the below program?

~~~c
#pragma omp parallel private(i)
{
    #pragma omp for
    for (int i = 0; i < 100; i++)
    {
        a[i] = i;
    }
}
~~~

* 20
* 40
* **25**
* 35

### Quiz: Do you understand worksharing directives?

This quiz covers various aspects of worksharing directives that have been discussed so far this Chapter.

#### Question 1
The purpose of `#pragma omp for` is

* Loop work is to be divided into user defined sections
* Work to be done in a loop when done, don’t wait
* **Work to be done in a loop**

#### Question 2
What is the purpose of `#pragma omp sections`?

* **Loop work is to be divided into user defined sections**
* Work to be done in a loop when done, don’t wait
* Work to be done in a loop

#### Question 3
What is the output of the following program?

~~~c
#pragma omp parallel num_threads(2)
{
    #pragma omp single
    printf("read input\n");
    printf("compute results\n");
    #pragma omp single
    Printf("write output\n");
}
~~~

* read input, compute results, write output
* read input, read input, compute results, write output, write output
* **read input, compute results, compute results, write output**
* Error in program

#### Question 4
What is the purpose of `#pragma omp for nowait`?

* Loop work is to be divided into user defined sections
* **Work to be done in a loop when done, don’t wait**
* Work to be done in a loop

#### Question 5
Which directive must come before the directive `#pragma omp sections`?

* `#pragma omp section`
* **`#pragma omp parallel`**
* None
* `#pragma omp master`

#### Question 6
The following code forces threads to wait till all are done:

* `#pragma omp parallel`
* **`#pragma omp barrier`**
* `#pragma omp critical`
* `#pragma omp sections`

#### Question 7
What is the output of the following code when run with OMP_NUM_THREADS=4?

~~~c
int arr[4] = {1,2,3,4};
int x=0, y=0, j;

#pragma omp parallel
{
    #pragma omp for
    for (j = 0; j < 4; j++)
    {
        #pragma omp critical
        x += arr[j];
    }
}
    

#pragma omp parallel
{
    #pragma omp single
    for (j = 0; j < 4; j++)
    {
        #pragma omp critical
        y += arr[j];
    }
}

printf("%d %d", x, y);
~~~

* **10, 10**
* 10, 40
* 40, 10
* 40, 40

### Quiz: Do you understand combined constructs?

This quiz tests your knowledge on OpenMP data environment and combined constructs.

#### Question 1
Within a parallel region, declared variables are by default

* private
* local
* **shared**
* firstprivate

#### Question 2
What is the output of the following code when run with `OMP_NUM_THREADS=4`?

~~~c
int arr[4] = {1,2,3,4};

int x = 1, j;
#pragma omp parallel for reduction(*:x)
for(j = 0; j < 4; j++) {
    x *= arr[j];
}
printf("%d", x);
~~~

* **24**
* 0
* 10
* 4

#### Question 3
What does the `nowait` clause do?

* Skips to the next OpenMP construct
* Prioritizes the following OpenMP construct
* Removes the synchronization barrier from the previous construct
* **Removes the synchronization barrier from the current construct**

#### Question 4
What is the data scoping of the variables a, b, c and d in following code snippet in the parallel region (multiple choice answer)?

~~~c
int a = 0;
int b = 23;
int c = -3;
#pragma omp parallel num_threads(2) private(a) reduction(+:c)
{
    int d = omp_get_thread_num();
    a = 42 + d;
    #pragma omp critical
    b = 1;
    c += a + b;
}
c = c / 2;
printf("a=%d, b=%d, c=%d\n", a, b, c);
~~~

* a: shared
* **a: private**
* **b: shared**
* b: private
* c: shared
* c: private
* **c: reduction**
* d: shared
* **d: private**

#### Question 5
What is printed when executing the below code?

~~~c
int a = 0;
int b = 23;
int c = -3;
#pragma omp parallel num_threads(2) private(a) reduction(+:c)
{
    int d = omp_get_thread_num();
    a = 42 + d;
    #pragma omp critical
    b = 1;
    c += a + b;
}
c = c / 2;
printf("a=%d, b=%d, c=%d\n", a, b, c);
~~~

* a=0, b=23, c=-3
* a=44, b=23, c=84
* a=0, b=23, c=42
* **a=0, b=1, c=42**

#### Question 6
Which of the following clauses specifies that the enclosing context’s version of the variable is set equal to the private version of whichever thread executes the final iteration?

* private
* firstprivate
* **lastprivate**
* default

#### Question 7
The following code will result in a data race:

~~~c
#pragma omp parallel for
for (int i = 1; i < 10; i++)
{
    factorial[i] = i * factorial[i-1];
}
~~~

* **True**
* False

#### Question 8
Which of these parallel programming errors is impossible in the given OpenMP construct?

* Data dependency in `#pragma omp for`
* **Data conflict in `#pragma omp critical`**
* Data race in `#pragma omp parallel`
* Deadlock in `#pragma omp parallel`

### Quiz on OpenMP tasking

This quiz tests your knowledge on OpenMP tasking with which we will finish this Chapter’s material.

#### Question 1
The default clause sets the default scheduling of threads in a loop constructs.

* True
* **False**

#### Question 2
Which tasks are synchronized with a `taskwait` construct?

* All tasks of the same thread team.
* All descendant tasks.
* **The direct child tasks**.

#### Question 3
Look at the following code snippet.

~~~c
int x = 42;
#pragma omp parallel private(x)
{
    #pragma omp task
    {
        x = 3;
    }
}
printf("x=%d\n", x);
~~~
What is the data scope of x in the task region and what is printed at the end?

* shared, x=3
* firstprivate, x=3
* **firstprivate, x=42**

#### Question 4
Look at the following code snippet.

~~~c
int x = 42;
int y = 0;
#pragma omp parallel num_threads(4)
{
    #pragma omp task
    {
        #pragma omp critical
        {
            y += x;
        }
    }
}
printf("y=%d\n", y);
~~~

What is the data scope of y in the task region and what is printed at the end?

* shared, y=42
* **shared, y=168**
* firstprivate, y=168

#### Question 5
What happens to tasks at a `barrier` construct?

* All existing tasks are guaranteed to be completed at barrier exit.
* **All tasks of the current thread team are guaranteed to be completed at barrier exit**.
* Only the direct child tasks are guaranteed to be completed at barrier exit.

### Quiz on MPI basics

We just covered the basics of MPI, communicators and messages. This quiz tests your knowledge of MPI basics and terminology. 

#### Question 1
Which is the predefined communicator that can be used to exchange a message from process rank 2 to process rank 4?
 
* `MPI_COMM_DEFAULT`
* `MPI_COMM_SELF`
* **`MPI_COMM_WORLD`**
* `MPI_COMM_NULL`

#### Question 2
What does `MPI_Comm_rank()` return?

* Number of processes in an MPI program
* Priority of the current process
* **Numerical identifier of the current process within the MPI communicator**
* Linux process ID

#### Question 3
What purpose does a communicator serve?

* It prevents your main program’s MPI calls from being confused with a library’s MPI calls
* It can be used to identify a subgroup of processes that will participate in message passing
* If equal to `MPI_COMM_WORLD`, it shows that the communication involves all processes
* **All of the above**

#### Question 4
A rank number from 0 to N-1 is assigned to each process in an MPI process group, and the higher rank processes are given higher resource priority.

* True
* **False**

#### Question 5
Which of the following is not required for a message passing call:

* The starting memory address of your message
* Message type
* **Size of the message in number of bytes**
* Number of elements of data in the message

#### Question 6
What does the parameter tag mean in a message passing call:

* The message type of the incoming message
* Type of communication method
* **A user-assigned number that must match on both sender and receiver**
* The type of the process group

### Quiz: Do you understand point-to-point communication?

This quiz covers various aspects of point-to-point communication that have been discussed so far this Chapter.

#### Question 1
You must specify the rank for both source and destination processes, when sending a message using `MPI_Send`:
 
* True
* **False**

#### Question 2
In the following function call, a message is sent to which process?

~~~c
MPI_Send(message, 4, MPI_CHAR, 5, tag, MPI_COMM_WORLD)
~~~
 
* Process 4
* **Process 5**

#### Question 3
If you call `MPI_Recv` and there is no incoming message, what happens?

* the Recv fails with an error
* the Recv reports that there is no incoming message
* **the Recv waits until a message arrives (potentially waiting forever)**
* the Recv times out after some system-specified delay

#### Question 4
The MPI receive routine has a parameter `count` – what does this mean?

* The size of the incoming message (in bytes)
* The size of the incoming message (in items, e.g. integers)
* The size you have reserved dor storing the message (in bytes)
* **The size you have reserved for storing the message (in items, e.g. integers)**

MPI tries to avoid talking about bytes – counting is almost always done in number of items. For the receive, count is the size of the local receive buffer, not of the incoming send buffer, although of course in some programs they may be the same. 

#### Question 5
What happens if the incoming message is larger than `count`?

* **The receive fails with an error**
* The receive reports zero data received
* The message writes beyond the end of the available storage
* Only the first `count` items are received

MPI checks that the incoming message will fit into the supplied storage before receiving it. The standard behaviour on error is for the whole MPI program to exit immediately with a fatal error. 

#### Question 6
What happens if the incoming message (of size `n`) is smaller than `count`?

* The receive fails with an error
* The receive reports zero data received
* **Only the first `count` items are received**

In some situations you may not know how many items are being sent so you must ensure that you have enough storage locally and you may have more than enough.

#### Question 7
You want to send a buffer that is an array buf with 5 double precision values. How do you describe your message in the call to `MPI_Send` in C and Fortran? (fill in the blank lines)

in C: **`buf, 5, MPI_DOUBLE`**

in Fortran: **`buf, 5, MPI_DOUBLE_PRECISION`**

#### Question 8
You want to receive a buffer that is an array buf with 5 double precision values. When calling `MPI_Recv` to receive this message which count values would be correct? (multiple choice answer)

* 1
* 2
* **5**
* **6**

#### Question 9
When using one of the MPI send routines, how many messages do you send?

* 1
* **2**
* 4

#### Question 10
How is the actual size of the incoming message reported?

* The value of `count` in the receive is updated
* MPI cannot tell you
* **It is stored in the Status parameter**
* With the associated tag

Various pieces of metadata about the received message are stored in the Status such as the origin, tag and its size.

### Quiz: Do you understand collective communication?

This quiz covers various aspects of collective communication that have been discussed this Chapter.

#### Question 1
Which are the major rules when using collective communication routines and do not apply to point-to-point communication?

Choose the one true statement.

* Only the sending process must call this routine.
* The destination provess of a communicator must call this routine.
* **All processes of a communicator must call this routine**.

#### Question 2
Which are the major rules when using collective communication routines and do not apply to point-to-point communication?

Choose the one true statement.

* The message size argument on the receive side must be larger than the message size argument on the sender side.
* **The message size argument on the receive side must match the message size argument on the sender side**. 
* The message size argument on the receive side must be smaller than the message size argument on the sender side.

#### Question 3
Which are the major rules when using collective communication routines and do not apply to point-to-point communication?

Choose the one true statement.

* Nonblocking collectives match with blocking collectives.
* **Nonblocking collectives do not match with blocking collectives**.

#### Question 4
Which operation may be though of as the ‘inverse’ of the MPI_SCATTER function?

* **`MPI_GATHER`**
* `MPI_RECV`
* `MPI_BROADCAST`
* `MPI_REDUCE`

#### Question 5
Some MPI collective calls specify both a send type and a receive type, e.g. `MPI_Scatter(sendbuf, sendcount, sendtype, recvbuf, recvcount,  recvtype, …)`. 

However, most times when you see this call used in practice we have sendtype = recvtype. 

Why does MPI make you specify both types?

* So it can check at runtime that you haven't made a silly mistake
* So it can do type conversion if required
* **The types and counts can be different provided that at least one of them is an MPI derived type**
* The types and counts can be different provided that the two buffers are the same length in bytes

The MPI datatypes do not have to be the same, they just have to be compatible. For example, if you create a datatype containing three integers then a send with this type will match a receive of 3 x `MPI_INTEGER`.

#### Question 6
In a scatter operation, what is the best way to use the sending and receiving buffers:

* It is generally OK for the sendbuf and recvbuf to be the same buffer
* **Allocate the senbuf only on the root process and recvbuf on all other processes**

#### Question 7
Which collective communication call should be used when simple synchronization across a communicator is required?

* `MPI_REDUCE`
* **`MPI_BARRIER`**
* `MPI_BROADCAST`

#### Question 8
What is the output of this MPI code on 8 processes, i.e. on running ranks 0, 1, 2, 3, 4, 5, 6 and 7?

~~~c
if (rank % 2 == 0) { //even processes
	MPI_Allreduce(&rank, &evensum, 1, MPI_INT, MPI_SUM, MPI_COMM_WORLD);
	if (rank == 0) printf("evensum = %d\n", evensum);
} else { //odd processes
	MPI_Allreduce(&rank, &oddsum, 1, MPI_INT, MPI_SUM, MPI_COMM_WORLD);
	if (rank == 1) printf("oddsum = %d\n", oddsum);
}
~~~

Options:
* evensum = 16, oddsum = 12
* **evensum = 28, oddsum = 28**
* evensum = 12, oddsum = 16
* evensum = 8, oddsum = 7

It does not matter that different processes call a collective routine from different lines of code. MPI as a library has no idea what route a proces stook before calling any MPI function. Here, since they are all operating in COMM_WORLD, all processes participate in the same global collective.

### Quiz: Do you understand advanced communication in MPI?

This quiz will test your knowledge on MPI’s advanced communication. 

#### Question 1
Which of the following MPI communication types suspends execution of the calling program until the current communication is completed?
 
* **Blocking**
* Nonblocking
* Asynchronous
* None of the above

#### Question 2
A message from a non-blocking send MPI_Isend is safe to be accessed immediately after the `MPI_Irecv` command.
 
* True
* **False**

#### Question 3
What is a valid reason for wanting to use one-sided communication in MPI?
 
* Less synchronization overhead
* Lower hardware latency
* Easier programming of irregular communication events
* **All of the above**

#### Question 4
Which of the following steps comes first in setting up MPI one-sided communication?
 
* Starting a communication interval using MPI_Win_fence
* Defining a transfer with put or get
* **Initializing a window**
* The order doesn’t matter

#### Question 5
If you execute an `MPI_Put`, where is the send and where is the receive buffer?
 
* **The `sendbuf` is a local buffer and the `rcvbuf` must be a window.**
* The `sendbuf` is a window and the `rcvbuf` is a local buffer.

#### Question 6
What units are used to define the size of a window in a call to `MPI_Win_create`?
 
* **Bytes**
* The units specified by the MPI_Datatype argument
* Words

#### Question 7
Immediately after returning from an `MPI_Put call`, it is safe to overwrite the buffer containing the data that was sent.
 
* True
* **False**

#### Question 8
What is the simplest way to end a one-sided communication interval and re-synchronize, in just one step? (fill in the blank lines)

**`MPI_Win_fence`**

### Quiz on Hybrid programming with OpenMP and MPI

Do you understand how OpenMP can be included and used with MPI? Test your understanding of this topic with this quiz.

#### Question 1
An MPI process is generally single-threaded unless the code has been augmented with multithreading directives or library calls.

* **True**
* False

#### Question 2
If `MPI_Init_thread` returns `MPI_THREAD_FUNNELED`, MPI messages can only be passed between main threads.

* **True**
* False

#### Question 3
Which argument to `MPI_Send` my be used to identify the destination thread?

* rank
* count
* **tag**
* communicator

#### Question 4
MPI messages can be passed between any two threads, provided each is enclosed in an `omp single` construct, when `MPI_Init_thread` returns what value?

* `MPI_THREAD_SINGLE`
* `MPI_THREAD_FUNNELED`
* **`MPI_THREAD_SERIALIZED`**
* `MPI_THREAD_MULTIPLE`

### Quiz on derived datatypes

This quiz tests your knowledge of user derived datatypes.

#### Question 1
Which of the following general datatypes assumes that the stride is equal to 1?
 
* **Contiguous**
* Vector
* Struct

#### Question 2
Which of the following general datatypes may constist of more than one basic datatype?
 
* Contiguous
* Vector
* **Struct**

#### Question 3
If you have an array of a structure in your memory, how would you describe this? (fill in the blank lines)

Using function **`MPI_Type_create_struct`** for the structure and the **`count`** argument in the MPI communication procedure for the size of the array.

#### Question 4
Which additional MPI procedure call is required, before a newly generated datatype handle can be used in message passing communication?

* `MPI_Type_contiguous`
* `MPI_Type_create_resized`
* **`MPI_Type_commit`**
* `MPI_Type_free`

### Quiz: GPU basics and architecture

This quiz tests your knowledge of GPU basics and architecture. For GPU basics you should also go through steps in the Accelerators overview activity in Week 1.

#### Question 1
Modern supercomputers (clusters) are equipped with (multiple choice answer):
 
* **CPUs**
* **CPUs and GPUs**
* GPUs
* **CPUs and GPUs on dedicated compute nodes**

#### Question 2
Consumer-grade GPUs compared to professional high-end GPUs (multiple choice answer):
 
* Do not share same technology, do not allow GPGPU computing
* Share same technology, do not allow GPGPU computing
* **Share same technology, allow GPGPU computing**
* Can’t have comparable performance
* **Can have comparable performance for single precision (FP32) operations**
* Can have comparable performance for double precision (FP64) operations

The theoretical FP32 performances for the gaming card NVIDIA GeForce RTX 3090 and high-end professional card NVIDIA Tesla A100 are 35.58 TFLOPS and 19.49 TFLOPS, respectively, on the other hand the theoretical FP64 performances are 0.556 TFLOPS and 9.746 TFLOPS, respectively. The gaming card is superior for single precision operations, while quite inferior for double precision operations.

#### Question 3
GPGPU computing is often referred to heterogeneous computing because:
 
* Many GPU models exist to be combined into a compute node
* A GPU typically runs different kernels over the course of a computation
* **Computing with a GPU typically also involves a CPU, i.e., two different kinds of hardware with different strengths**

In GPGPU computing a GPU can be seen as a coprocessor to a CPU.

#### Question 4
What are the characteristics of GPU memory compared to CPU memory?
 
* **Less cache, longer latency, higher memory bandwidth**
* Less cache, shorter latency, higher memory bandwidth
* More cache, longer latency, lower memory bandwidth
* More cache, shorter latency, lower memory bandwidth

#### Question 5
A GPU core is the same as a CPU core:
 
* True
* **False**

The equivalent of a CPU core in a GPU is a streaming multiprocessor with many GPU "cores".

### Quiz: CUDA and OpenCL programming and execution models

This quiz tests your knowledge about the basics of CUDA and OpenCL programming and execution models.

#### Question 1
What statements about CUDA and OpenCL are correct? (multiple choice answer):
 
* Both CUDA and OpenCL are supported by many GPU vendors.
* **CUDA is supported only by NVIDIA GPUs, while OpenCL is supported by many GPU vendors**.
* **CUDA and OpenCL execution models are similar, but have a different terminology**.
* CUDA and OpenCL execution models are different.

#### Question 2
Which of the following correctly describes the relationship between warps, thread blocks and CUDA cores?
 
* A warp is divided into one or more thread blocks and each thread block executes on a single CUDA core.
* A thread block is divided into one or more warps and each warp executes on a single CUDA core.
* **A thread block is divided into one or more warps and in each warp, every thread executes on a separate CUDA core**.

Each CUDA core executes a different thread from a single warp.

#### Question 3
In a CPU, what is the closest equivalent of a GPU warp?
 
* float
* **vector**
* thread
* core

#### Question 4
A function with the `__global__` or `__kernel` prefix can be called from the host or the device and can run on either of them.
 
* True
* **False**

This prefix specifies that the function can be called from either host or device, but it runs on the device alone.

#### Question 5
Which of the following correctly describes a GPU kernel?
 
* A kernel may contain a mix of host and GPU code.
* **All thread blocks (work-groups with work-items) involved in the same computation use the same kernel**.
* A kernel is part of the GPU’s internal micro-operating system, allowing it to act as an independent host.

#### Question 6
Threads in a thread block (work-items in a work-group) can be distributed across two or more streaming multiprocessors (SMs).

* True
* **False**

A thread block (work-group) must be run entirely on a single SM.

#### Question 7
Which internal variable in OpenCL is used to identify the work-item among all other work-items executed in the kernel?

* `get_local_id()`
* **`get_global_id()`**
* `blockIdx`
* `threadIdx`

#### Question 8
CPUs and GPUs can use the same memory address space:

* For every CUDA and OpenCL version on every GPU architecture
* **For newer CUDA and OpenCL versions and newer GPU architectures**
* For CUDA versions only
* Same memory address space is not supported yet

#### Question 9
Threads in CUDA or work-items in OpenCL can synchronize:

* **In a single block (work-group)**
* In many blocks (work-groups) associated with a single kernel
* Can’t synchronize

Threads (work-items) can synchronize only in shared (local) memory in a single block (work-group).

#### Question 10
Which of the following statements is true about compute capability in CUDA?

* Code compiled for hardware of one compute capability will not need to be re-compiled to run on hardware of another.
* **Different compute capabilities may imply a different amount of local memory per thread**.
* Compute capability is measured by the number of FLOPS a GPU accelerator can compute.

Every NVIDIA GPU supports a compute capability according to its microarchitecture and associated hardware design, number of cores, cache size and supported arithmetic instructions.