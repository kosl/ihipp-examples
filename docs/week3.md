
### MPI

## 1.V: Communicator in MPI
In the introduction to MPI in the first week we already saw the simple excercise of 'Hello world'. In order to actually write some useful applications, we will need to learn some basic routines. To begin with we need to understand what is a communicator in MPI. As we launch MPI, the entire environment puts all the processes and the cores that are involved in this application and binds them together in what is reffered to as a 'communicator' (image D2P1S12). A communicator  is like a set that binds all the processes together corroborates that only those processses are together in application can communicate with each other. The default communicator that we will use most often is the 
~~~c
MPI_COMM_WORLD
~~~ 
that is already predefined in the header file
~~~c
mpi.h
~~~
### Ranks and Size

Frequently, we use the MPI com world when we will need to use a communicator. Once we actually initialize the MPI environment, all the processes would then be in the communicator. As we can predict it would be nice to be able to distinguish between different processes and this is where the 'ranks' come in. When we initialize the environment, MPI communicator will dedicate a number to each process. This is known as the 'rank'. It is a number that is starting from zero and ends with the size minus one. In this example, as you can see, we have launched the application with seven cores and each of them is given a rank. So this application we have different processes that have been given ranks from zero to six.
This helps us in identifying and using a specific processor. For instance, if we would the processor number two to do perform a certain task, we can command execution of the task, if the rank is '2'.  Later on  when we progress further to learn sending messages between specific processors, we will see how rank is useful. So to say if rank is '2' send a message to rank '6'. This is how we do the sending and receiving of the messages between different processess in MPI.

In order to actually get these numbers, we have two basic routines in MPI. We know now that when we initialize the MPI environment, rank is the number that each of the processor is given and is the number by which you can identify a process. The 'size' is the number that tells us number of processes that are contained within a communicator or simply how many processes are in our application. For instance, when the size is 10, rank goes from zero to nine and so on. 
There are two basic routines for the 'rank'
~~~c
MPI_Comm_rank(MPI_Comm comm, int *rank)
~~~
and for the 'size'
~~~c
MPI_Comm_size(MPI_Comm comm, int *size);
~~~
 (image S13)
 
 ## 2.E: Hello World 2.0
 We modify our excercise from the first week.
 
### Goal:
Modify "Hello World" excercise so that
- every process writes its rank and the size of MPI_COMM_WORLD,

- only process ranked 0 in MPI_COMM_WORLD prints "hello world".

## 3.D: 
What do you observe when you run the program multiple times?

## 4. V: Messages and communications

Until now, we have introduced the MPI and we have used some simple routines such as rank and size, to distinguish between different processes and to actually assign them some numbers that we can recognise and use later. But until now, we haven't done anything useful in a way that we haven't sent any information between the processes. This is where we need to gain an understanding in messages.  For example when we are developing different advanced applications, at one point you will need to exchange information from one process to another.  Usually, this information could be some integer, some values or some arrays etc. This is where messages are used. Messages are packets of data moving between sub-programs. So, as said earlier, if we pack this information to be shred between processses into some message, we can send them over communication network so the other process can receive this message. This is how the data and information is shared bewteen the processes. And you will learn throughout the state, actually, when you will be using those routines that there are some important information that you will always need to specify in order for the message to actually be sent and received. So suppose, as in this example, we are trying to send a message from ranking zero to rank due process, and in order for this to work, you have to specify some information. So first of all, you will need to know the sender will need to specify what so what data we are sending. Basically, what is the size of the data? So number of data, suppose we are sending an array.



