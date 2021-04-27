
### MPI

## 1.1 V: Communicator in MPI
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
 
 ## 1.2.E: Hello World 2.0
 We modify our excercise from the first week.
 
### Goal:
Modify "Hello World" excercise so that
- every process writes its rank and the size of MPI_COMM_WORLD,

- only process ranked 0 in MPI_COMM_WORLD prints "hello world".

## 1.3.D: 
What do you observe when you run the program multiple times?

## 1.4. V: Messages and communications

Until now, we have introduced the MPI and we have used some simple routines such as rank and size, to distinguish between different processes and to actually assign them some numbers that we can recognise and use later. But until now, we haven't done anything useful in a way that we haven't sent any information between the processes. This is where we need to gain an understanding of messages in MPI. For example when we are developing different advanced applications, at one point we will need to exchange information from one process to another.  Usually, this information could be some integer, some values or even arrays etc. This is where messages are used. Messages are packets of data moving between sub-programs. So, as said earlier, if we pack this information to be shared between processses into some message, we can send them over communication network so the other process can receive this message. This is how the data and information is shared bewteen the processes. And of course there is some important information that we will always need to specify in order for the messages to be sent and received efficiently. 
 (image S16)
As we can see in this example, we are trying to send a message from a process at rank '0' to process at rank '2', and in order for this to work, we have to specify some information. 
-Data size and type
First of all, we will need to know, that means that the sender will need to specify what kind of data are we sending. Size of the data inferrs, what is the the 'number'. So for example if we are sending an array of lets say 100 numbers the size would be 100. And as you probably already guessed we would also need to mention what the 'type' of the data is. So is it a character? Is it a double integer? and so on. 
- Pointer to sent or received data
For this data exchange we would need two pointers.These pointers are from the sender that will need to point to its own memory to say, OK, the data I'm trying to send is here. And then the receiver will need to specify the memory where he would like to receive this data. 
-Sending process and receiving process, i.e., the 'ranks'
The MPI environment will need to know who is the sender and who is the receiver. This is where the 'ranks come in'. So in our previous exapmle we will specify that the rank '0' is the sender and the rank '2' is the receiver. 
-Tag of the message
The next information we will need to specify is the 'tag' of the message. A tag is a simple number that we can assign any value from which a receiver can identify the message. For instance, if we would send two messages we can assign one tag as let's say '0' and the other one as tag '1'. This helps the receiver identify and differentiate which message is which. But usually if we will have only one message, we can just put the tag as '0'.
-The communicator, i.e. MPI_COMM_WORLD
The last argument we will need to specify is what is the communicator in which we are sending the messages. In our case here it would be the MPI_COMM_WORLD, but we would eventually learn better about the functions as we will do more excercises and hands on practice. 

### MPI Datatypes
(table S17)
The MPI environment defines its own basic data types. However, if you're familiar with 'C' they're really simple because what you have to do is just put MPI in capital letters before the variable and change everything to capital case. 
So simply put, if you're trying to send an integer, then the type is
~~~
MPI_INT
~~~
and similarly with double, long, character and so on. 
However, as we will get more involved with MPI, we will explore that there is also a way for the user to define its own derived data type. For instance if we're using 'struct' in C, then we  can define that struct as a new MPI data type. This proves to be very useful  because we can just send everything in one message. So this would not require us to send portions of the struct with different messages. But we will dwell deeper into the derived data types in the coming weeks. For today's section we're only using simple data types and that would mostly mean either an int or a double or maybe even a character. 

## 2. Types of communication in MPI
There are two criterias by which we divide the types of communications in MPI. 




