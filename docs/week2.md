# Introduction to OpenMP

## Getting started with OpenMP 

## V: Runtime functions, variables and constructs
### Runtime functions
So for C++ and C, you can add to the cache, include OLP that H can apply that to your code in the beginning of the file and then display that includes basically all the runtime functions that you need and you want to use some of the more standard runtime functions. And the ones that are using our tutorial today are seen on the screen. So for example, when he said as a thread, so in your part of the program that open up, you can specify the desired number of threats that you want to use.
 Examples:
 
 – To set the desired number of threads
 ~~~c
  omp_set_num_threads(n)
  ~~~
 – To return the current number of threads
 ~~~c
 omp_get_num_threads()
 ~~~
– To return the ID of this thread
~~~c
omp_get_thread_num() 
~~~
 – To return .true. If inside parallel region
 ~~~c
 omp_in_parallel()
 ~~~

For example, if you want your plot on your program on, let's say, 12 threads, you put no threads to the program, only use the only [00:20:00] word test. So we set a number of threats and we will return the current number of threats. So if you specify a number of threats. To 12 and then you use this function, so get contest is getting on offense will return to that number of steps that are being used in their program. So help you get further down. Here is the idea of this track. So when you are in a specific time, then you call these functions, these functions return an integer. And this integer is unique for every thread that you use. In your coat of the two pair of eyes, your task, some. And the functional area in parallel will return true, this function will return true if it is specified inside of the region. If it is not, it is specified in the region to return false. And again, so if you want to those functions, you need to specify the appropriate header file at the beginning of your second. Of course, there are multiple other open and parenting functions that are available in open entities are not the only ones. So you can click on the link on the on the slide and you will see all the open entry functions with some tutorials and explanations on how to use them in your program. OK, so now we have taken a look at runtime functions, so these runtime functions are basically used inside your code.

### Environment Varibales
The next thing that we have to take a look at our environment, that in this environment, variables are not used in the recording but are specified in the environment, whereas you are compiling them down on your code.

And so the purpose of unfettered access to control the execution of. Part of the program and basically the programs that we're compiling. So this is not specified in the code, but you specified in a saying that it looks to me not only for you compiling that on your program and so on the screen, that basically the three environmental factors that are the same are common. So the only underscore no text specifies a number of threats to use. Yes. So you can send see my handwriting written very well by, for example, if you're using the best you can export this matter. This is very good and specified a number of threats and the program will only work with.

Purpose of environment variables is to control the execution of parallel program at runtime. These variables are not specified in the code itself but in the environment in which the parallel program is executed.
 – To specify the number of threads to use
 ~~~c
 OMP_NUM_THREADS
 ~~~
– To specify on which CPUs the threads should be placed
~~~c
OMP_PLACES 
~~~
– To show OpenMP version and environment
~~~c
 OMP_DISPLAY_ENV
 ~~~

The number of threads to specify the environment better, but the same goes for use in other countries, for example, age, the usage of the virus is about using the word set and the key safe. And you can specify the number of threats use the most similar way. The next society places, so this message specifies on which city visitors should be placed and the displayed in an environment basically shows the open, empty version and that you are then, of course, again, there are multiple other environmental NGOs that you can use. For example, for the GCSE compiler, we can tweak the link and check the environment that it was that you want to use yourself on and all the explanation and examples on how to use those environment.

### Parallel Constructs
The next thing that we take a look at is a parrallel constructs.
So part of the parallel construct is the basic or the fundamental contruct using open pit. So every trade basically executes the same statements which are inside this, the so-called parallel region simultaneously, as you can see on the right image. So first, we have a master plan that executes the serial portion of the code. Then we come to this statement. Yes. So the master first encountered this on construct and creates multiple so-called slave trade safe tracks that run in parallel and master and slave traders then divide between each other. And in the end, we specify an implicit barrier. So when these batteries when these batteries reached, basically the threats finish and we wait for all threats to finish the execution, and when all the tests have finished, the execution will go back to M. M.. That basically presumes the execution of the code. And the threats are, of course, gone because they have completed their test, so this is embedded in the CI A. specified with. You can see the specification for the police that on the bottom left side and trying to specify the bitcoin and bottom line. Yes, and this is basically the end of your bottom of the region and the message that moves on to execute the code in Syria and the slave states and all the other threats and part of the finish line drop in the.




## V: Clauses and directive format
### Directive format
So now we will take a look at Clauses and directives inside openmp. So so far we have just specified a parrallel region and that was it. Then the code came executed in serial and master fed. 
 
Directive format 
~~~c
#pragma omp directive_name [clause[clause]...]
~~~
Conditionals: 
~~~c 
#ifdef _OPENMP
~~~
-Block of code to be executed if code was compiled with OpenMP, for example
~~~c
printf(“Number of threads: %d“, omp_get_num_threads);
#else
   ~~~
-Block of code to be executed if code was compiled without OpenMP
~~~c
#endif
~~~ 

You get no such file or directory for dot. F opening T So f openmp is a flag is so if I put a command you mean when you compile the file, I assume this this is the problem and that you get so yes, so I will put the comment in the chat. So how do you compile it? So you put GC c - F open pee 


And then you specify the flex of - F open in D. So this - F open until basically tells the compiler that we are compiling the problem with openmp if you don't specify this.

You have you will not be able to run a comparable. So this - F openmp is basically a flag for the GCC compiler and for other compilers you have let's say different flags do for Intel compiler is just open empty without DF and so on. I have those Flex specified in the lighting in the fourth slide if you go back so

### Clauses
In C/C++ clauses can be:
• private (list) – in this case the variable is private to each thread
• shared (list) – in this case the variable is shared between threads
C/C++:
~~~c
int A;
#pragma omp parallel private(A) {
A=omp_get_thread_num();
...
}
~~~

## E: Calculate pi!
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

## V: OpenMP constructs and Synchronisations 
### Worksharing constructs
So we will take a look at the so called work-sharing construct the same so work-sharing constructs divides the execution of the code region among different members of Team threads threads teams. So these are would say constructed do not launch the new threads and they are.

They divide the execution of code region among the members of the team. Constructs do not launch new threads
They are enclosed dynamically within the parallel region. Examples:
• sections
• for
• task
• single

1. Section constuct

So we have sections. We have a foreclosed and tasks and single so maybe you will know the for Clause so which is basically the for Loop that is executed in parallel.So here we will take a look at the sections construct. So on the left side, you can let's see the code we can specify the sections concert by specifying directive sections and you can see on the screen and when you use sections construct multiple blocks of code are executed in parallel. Yes, so if I specify section and good. Let's say at asking to it. Then this specific task will execute in one thread. And then if I go on to another section this section will execute in in a different in a different direction and so on so you can add this sections. So you can see here, for example, so we move we specify section inside this section heaven and be variable and then when the code is executed a new trade is generated with those with variables and the same goes for C and D variables which are specified in a different section and plus mean a different threat.
~~~c
#pragma omp parallel {
#pragma omp sections {{a=...; b=...;} #pragma omp section
{ c=...; d=...; }
}// end of sections }// end of parallel
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




## E: For and critical directive

