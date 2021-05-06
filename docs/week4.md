## MPI Continued

### 1.1 V: Non Blocking communications
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
- Then we can do soome other work because when we use this routine, it does not block us, so we can do some stuff after this. However, later on we actually have to check whether the message has been received.
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

### 1.2 E: Rotating information around a ring (non-blocking)

### Goal
- A set of processes are arranged in a ring. Initialize sum to 0. 

a)
1. Each process stores its rank into snd_buf. 
2. 2. Each process passes this on to its neighbour on the right.
3. Each process adds snd_buf to sum. 

b)
1. Repeat 1-2-3 with size (number of process) iterations, i.e. each process computes the sum of all ranks.
2. Use non-blocking MPI_Isend.

### 1.3 V: One sided communication
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

And at the end of the MPI application we have to free this window with the fucntion
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
