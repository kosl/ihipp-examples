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
We will understand this more clearly with the help of the examples.

### Non-blocking Send
(imageD2P2S20) *would be ideal as an animation*


