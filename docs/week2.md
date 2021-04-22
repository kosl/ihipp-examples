
# Week 2: Getting started with OpenMP 

## 1.V: Runtime functions, variables and constructs
## Runtime functions

The purpose of runtime functions is the management or modification of the parallel processes that we want to use in our code. They come with the OMP library.  
For C++ and C, you can add the 

~~~c
#include<omp.h>  
~~~ 

header file to your code in the beginning of the file and then this library includes all the standard runtime functions that you need and you want to use. The functions that we would be using in our tutorial today can be accessed from the link in the transcript or in the resources. So for example, 
 
 To set the desired number of threads

 ~~~c

 omp_set_num_threads(n)

  ~~~

For example, if you want to 'parallelise'  your program with, let's say, 12 threads, you specify number of threads to the program using the function

~~~c

omp_set_num_threads(n)

~~~

With this the program will only work with 12 threads. 

To return the current number of threads

 ~~~c

 omp_get_num_threads()

 ~~~

With this we set a number of threads and we will return the current number of threads. So, like our previous example, if you specify the number of threads to 12 then calling this function will return the number of threads that are being used in the program. 

To return the ID of this thread

~~~c

omp_get_thread_num() 

~~~

So calling this function, when you are in a specific thread would return an integer that is unique for every thread that is used in the code to 'parallelise'  your task. 

– To return 'true' if inside parallel region

 ~~~c

 omp_in_parallel()

 ~~~

This function returns 'true' if it is specified inside a parallel region. If it is not, i.e if it is specified in serial region it will return false. And again, so if you want to use those functions, you need to specify the appropriate header file at the beginning of your C code. Of course, there are multiple other runtime functions that are available in openMP . So you can click on the link on the on the slide and you will see all the openMP functions with some tutorials and explanations on how to use them in your program.

## Environment Variables

The next thing that we have to take a look at are environment variables. Contrary to runtime functions, environment variables are not used in the code but are specified in the environment, where you are compiling and running your code. Purpose of environment variables is to control the execution of parallel program at runtime. As these are not specified in the code, you could specify them for example in a linux terminal before you compile and run your program. Let's go through the three most common environment variables.

To specify the number of threads to use

~~~c

OMP_UM_THREADS 

~~~

With this you can set the environment variable. For example, if you're using the batch terminal you can export this variable and specify a fixed number of threads and the program will only work with this specified number of threads. The same goes if you are using other terminals. For example, TCSH, the usage of the environment variable is achieved through using the word set and the key  word 'setenv' and you can specify the number of threads to be used in the similar way :

~~~csh

setenv OMP_NUM_THREADS n

~~~

To  specify on which CPUs the threads should be placed

~~~c

 OMP_PLACES 

~~~

To show OpenMP version and environment

~~~c

OMP_DISPLAY_ENV  

~~~

This basically shows the openMP version and that you are in. 
Of course, there are multiple other environmental variables that you can use. 
For GCC compiler you can check the link and check the environment variables that you want to use yourself along with all the explanation and examples on how to use those environment.

## Parallel constructs
Parallel construct is the basic or the fundamental construct using openMP. So every thread basically executes the same statements which are inside the 'parallel region' simultaneously, as you can see on the right image. So first, we have a master thread that executes the serial portion of the code. Then we come to this 'pragma omp' statement. We can see here that the master first encounters this omp construct and creates multiple, what we call 'slave threads' that run in parallel. Subsequently the master and slave threads divide the tasks between each other. In the end, we specify an implicit barrier,  so,  when these barrier is  reached, the threads finish and we wait for all threads to finish the execution. Following this, when all the threads have finished the execution we go back to master thread that finally resumes the execution of the code. In this step, of course,  the slave threats are gone because they have completed their task.
In 'C' this implicit barrier is specified with:   

~~~c

#pragma omp parallel
{
...
 }

~~~





## 2. V: Clauses and directive format
## Directive format

So far we have just specified a parallel region and the code was executed in serial. Now we will move ahead to see directives for the openMP. The format for using a directive is as follows

~~~c

#pragma omp directive_name [clause[clause]...]

~~~

We have already seen and used 'pragma omp parallel'  that was a directive to execute the region in parallel. In this format we also have 'clauses' in order to specify different parameters.  For example, what is private variable i.e a variable that has access to only one thread whereas a shared variable is one that will be updated anytime a thread gets access to it. We will explore the clauses more in the following subsection. For now we will learn about the  'conditionals'. Similar to any programming language openMP also has conditional statements. So for example we can also specify an 'if' statement in openMP in the following way

~~~c

 #ifdef _OPENMP
//block of code to be executed if code was compiled with OpenMP, for example
      printf(“Number of threads: %d“, omp_get_num_threads);
   #else
//block of code to be executed if code was compiled without OpenMP
#endif

~~~
When we specify  '#ifdef _OPENMP' then the code will execute and when it comes to this 'if' statement, it will track whether the code is compiled with openMP. In this case if it was compiled with openMP with the flag ' #ifdef _OPENMP'  then it will enter the subsequent block of code to execute it. Otherwise, if the code was compiled 'serially', the block of code following the 'else' statement would be executed . And of course we close the conditional statements with 'endif'

## Clauses

The directive format we just learnt:

~~~c

#pragma omp directive_name [clause[clause]...]

~~~
Is an important keyword with openMP that we put in the beginning of our code on the line where we want the 'parallel' region to start and then we mention  the 'directive name' and the 'clause'. In this subsection we will learn about 'clauses'.

There are basically two kind of clauses. i.e private or shared. 
A private variable would be a variable that is private to each thread. So if we execute [image D1P2S18] 

~~~c
int A;
#pragma omp parallel private(A) {
A=omp_get_thread_num();
...
}
~~~

So, here we define an integer A in C code Then we Define the OMP directive i.e the 'omp parallel' and the 'private A'. So what happens here is that any time we will get a new thread this variable 'A' will be assigned inside of each thread individually. This would imply that the value of 'A' will go to the number of threads. So in the in the first thread it will be '0' in the second thread the value of this variable will be '1' because this would be the 'id' of the thread and in the third the value will be '2' and so on. We can see clearly that these variables are basically private, meaning that they are existing inside each thread.  This implies that the variable 'A' (0) in the first thread can can not be accessed by the variable 'A' (1) in the second thread. 
So this infers that this variable is basically private to each individual thread in our program. 
And of course the opposite of this is the shared variable. If we specify that a variable is a shared variable this would signify that  the variable will be shared between the threads. If we specify the variable outside of the parallel region, so right before the 

~~~c

#pragma omp parallel

~~~
this variable will be accessed by every thread. To exemplify, let's say if we have a 'for' loop and you we add a number to it  in every iteration we can just specify it to be a shared. In this case whenever any thread that will update the shared variable simultaneously therefore adding numbers to it. This is a adequate way to use the 'for' Loop that we will see soon in the following subsections. 

So, to sum up the distinction between private and shared, the private variable is available only to one thread and cannot be accessed by any other thread whereas a  shared variable can not only be accessed by every thread in the part of the program but it can also be updated, changed and modified by by each thread simultaneously.


## 3. E: Calculate pi!
### Goal
To use runtime library calls, conditional compilations, environment variables and parallel regions by calculating pi constant.
### Excercise
1. Open file e2.c and add an if clause if omp is used. Inside add a parallel region that prints the ID of each thread (with omp_get_thread_num()) and the number of all threads (with omp_get_num_threads()).
2. Compile and run on 4 CPUs and then on 12 CPUs. Observe output.
3. Add an else clause if program is not compiled with OpenMP. Add a print statement that says: „The program is not compiled with OpenMP“. Compile the program without OpenMP and run it. Observe the output.
4. Add a private clause to omp parallel directive for the variable associated with omp_get_thread_num() and observe the difference in the output.
• Race condition:
• Two threads access the same shared variable and at least one thread modifies the variable and the accesses are unsynchronized
• Outcome of the program depends on timing of the threads in the team
• This is caused by unintended shared of data
### Solution
~~~c
#include <stdio.h>
#include <time.h>
#include <sys/time.h>
#ifdef _OPENMP
#  include <omp.h>
#endif

#define f(A) (4.0/(1.0+A*A))

const int n = 10000000;

int main(int argc, char** argv)
{
  int i;
  double w,x,sum,pi;
  clock_t t1,t2;
  struct timeval tv1,tv2; struct timezone tz;
# ifdef _OPENMP
    double wt1,wt2;
# endif

/* Begin of SPACE for second exercise */


/* End of SPACE for second exercise */

  gettimeofday(&tv1, &tz);
# ifdef _OPENMP
    wt1=omp_get_wtime();
# endif
  t1=clock();
 
/* calculate pi = integral [0..1] 4/(1+x**2) dx */
  /* Begin of SPACE for third exercise */
  w=1.0/n;
  sum=0.0;
  for (i=1;i<=n;i++)
  {
    x=w*((double)i-0.5);
    sum=sum+f(x);
  }
  pi=w*sum;
/* End of SPACE for third exercise */
  t2=clock();
# ifdef _OPENMP
    wt2=omp_get_wtime();
# endif
  gettimeofday(&tv2, &tz);
  printf( "computed pi = %24.16g\n", pi );
  printf( "CPU time (clock)                = %12.4g sec\n", (t2-t1)/1000000.0 );
# ifdef _OPENMP
    printf( "wall clock time (omp_get_wtime) = %12.4g sec\n", wt2-wt1 );
# endif
  printf( "wall clock time (gettimeofday)  = %12.4g sec\n", (tv2.tv_sec-tv1.tv_sec) + (tv2.tv_usec-tv1.tv_usec)*1e-6 );
  return 0;
}

~~~
### Expected output
• If compiled with OpenMP, the program should output and ID of each thread and number of all threads
• If not compiled with OpenMP, the program should output “The program was not compiled with OpenMP“

## 4. V: OpenMP constructs and Synchronisations 
## Worksharing constructs
The work-sharing constructs divides the execution of the code region among different members of team threads. These are the constructs that do not launch the new threads and they are enclosed dynamically within the parallel region
 Some of the examples of the work sharing constructs are:
• sections
• for
• task
• single

### Section construct

We will first see the code for using the sections construct where we can we specify it through directive sections .

~~~c

#pragma omp parallel {
#pragma omp sections {{a=...; b=...;} #pragma omp section
{ c=...; d=...; }
}// end of sections }// end of parallel

~~~

When we use sections construct multiple blocks of code are executed in parallel. (image D1P2S22). When we specify section and we put a task into it, this specific task will execute in one thread. And then when we go on to another section that will execute its task in a different thread. In this way we can add these sections inside our 'pragma OMP parallel' code by specifying a section per each thread that will be executed in that each individual thread.

In the example code above we can see that inside the section we have specified variables 'a' and 'b'. When this code is executed a new thread is generated with these variables and the same follows for the variables 'c' and 'd' which are specified in a different section and hence are in a different thread. 


### For construct
~~~

2. For construct

And the next one is the for construct. So for constant basically means let's say a for Loop that is paralyzed app. So you can see how we can specify this for constructs. So again, we start with pragma OMP and then. We use the for keyword and we can use different closes again. So private shared and so on. And the corresponding for Loop has a canonical shape. So this is we can see that this is basically a c Syntax for the for the for Loop and the iterator is not modified inside the loop body. So because each let's say iterator is by default a private variable and is shared by only one threat escrow that this is not. Excess by every threatened because otherwise our for Loop would get corrupted.
So the closes again private and then we have a few other. So for example, the schedule close classifies car detailing how the iterations of Loops are divided among different tracks one. For example, the collapse close can move the iterations into just one larger iteration space. So we take a look at this later.
So here for example, you can see an example of the for construct used in the code. Yes. So let's say we start with pregnant went a parallel then we added a private variable named F. And then we do pragma OMP and for construct. Yeah, so we write a for Loop and let's say this for Loop will go from 0 to 10.So that would be 10 different iterations. And private variable f is then fixed in every threat and the a list is updated in parallel because because the index need of each

Each array is let's say individual of each other. So every thread can access just one place of the
So this is why we can update this list in part of it. Yeah. So for example on the right screen we can see.If we are working on two threads, yes. Oh and we have let's say 10. Ten iterations. So this iterations will let us say be split between two threats from 0 to 4 and 5 to 9 and each place in on a list will be updated by itself is for which the citrate it modifies just one place of ASL because this iterators are independent of each other and we can do this you can update the
Each place of the a list quite easy. Yes. This is an example of the for construct.
~~~c
#pragma omp parallel private(f) {
f=10;
#pragma omp for
for (i=0; i<10; i++)
a[i] = b[i]*f;
} /* omp end parallel */
~~~

3. Synchronization

Then the next thing is the synchronization. So synchronization can be said by either increasing barrier or an ecstasy barrier. So implicit value we have been using it in both examples. So implicit barrier basically represents a barrier for the beginning and end of a parallel construct. Yes. So this is achieved with let's say in C++ with with parentheses. Yes. There is an example here. So let's let's say this first segment statement drag my only comparable. This would be the implicit barrier you specify the entry into parallel region and the last parentheses is basically the implicit barrier that specifies the end of the parallel crop construct and then we move to the
To the serial execution of the code as well. And so in case you increase interested, you can try to use the Google the no wait clothes for the overall openmp and we check some examples of how we can remove the indices synchronization with this Clause there. But of course we have the other one, which is excess in value. So explicit value is basically means that you can
Use a class and we disclose your basically specified it here is the barrier. So this is the so called critical cross so cold it is enclosed in critical classes executed by everything. That's all but is restricted to only one-third at a time. So you specify with pragma OMP critical then the name so we will maybe take a look at it here.
Yes, so here you can see that say the scheme of the critical process. So if we go over this code quickly, so we have specified variables CMT and F and in the parallel region, we specified the for construct.
And inside the if statement we specified the pragma OMP critical for the next Plant which is in t plus plus here and then we close it. So pragma OMP critical is valid only for this variable and we can observe what is happening basically in the execution of the threats on the right side. Yes, so we have
Before we enter the park pragma OMP parallel region, we were in serial execution style. This was executed cereal seriously, then we entered our momentum parallel and this is basically divided. So again, we are doing a for Loop for let's say two to threats. So everything is executed parallely until the first read in counters the CNT. Yeah the same thing variable. So in this case is simply variable is
First executed and during this time the second thread is trying to access it. It cannot do it because CMT is already Modified by the first treasure. So after the first thread modifies the CNT plus plus the specified.
Then the next thread will get access to it and it will execute in between modified in whichever way you specify after all the threats have let's say modified it the code begins to execute in parallel as well.
So further until we reach the implicit barrier that we have specified at the end and then we go back to then we go back to Syria execution. Yes, so due to click critical cloths as I explained only one thread at a time is executed for this sin T variable s so if you the critical flaws and you paralyze the program so whenever you will reach the critical. Cross only one thread will be able to modify or to run the the code that you specified in the critical closed hand. And then when the when the when the first red finish is the next word is executed and so on for all the other threats and well all the other all the threats have modified this variable. Then the program will start to execute back in parallel until we until we reach the implicit better.
~~~c
cnt = 0;
f=10;
#pragma omp parallel
{
#pragma omp for
     for (i=0; i<10; i++) {
       if (b[i] == 0) {
          #pragma omp critical
          cnt ++;
       } /* endif */
       a[i] = b[i]*f;
} /* end for */
} /*omp end parallel */
~~~




## 5. E: For and critical directive

### Goal
To use a worksharing construct for and critical directive.

### Excercise
1.Use the result from Exercise 2.
2.Add parallel region and for directive in e2.c and compile it
3.Set environment variable OMP_NUM_THREADS to 2 and run the file. 
• The result is wrong
4.Set environment variable OMP_NUM_THREADS to 12 and run again 
• The result is wrong
5.Add private (x) clause in e2.c and compile
6.Set environment variable OMP_NUM_THREADS to 2 and run 
• Still incorrect
7.Set environment variable OMP_NUM_THREADS to 12 and run 
• Still incorrect
8.Add critical directive in e2.c before the sum variable in for loop and compile again
• What is the CPU time?
9.How to optimize the code? Try to modify the code and move the critical directive outside for loop to decrease computational time

### Solution



