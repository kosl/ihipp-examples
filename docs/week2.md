# Introduction to OpenMP

## Getting started with OpenMP 

## V: Runtime functions, variables and constructs
### Runtime functions
So for C++ and C, you can add to the cache, include OLP that H can apply that to your code in the beginning of the file and then display that includes basically all the runtime functions that you need and you want to use some of the more standard runtime functions. And the ones that are using our tutorial today are seen on the screen. So for example, when he said as a threat, so in your part of the program that open up, you can specify the desired number of threats that you want to use.

For example, if you want your plot on your program on, let's say, 12 threats, you put no threats to the program, only use the only [00:20:00] word test. So we set a number of threats and we will return the current number of threats. So if you specify a number of threats. To 12 and then you use this function, so get contest is getting on offense will return to that number of steps that are being used in their program. So help you get further down. Here is the idea of this track. So when you are in a specific time, then you call these functions, these functions return an integer. And this integer is unique for every thread that you use. In your coat of the two pair of eyes, your task, some. And the functional area in parallel will return true, this function will return true if it is specified inside of the region. If it is not, it is specified in the region to return false. And again, so if you want to those functions, you need to specify the appropriate header file at the beginning of your second. Of course, there are multiple other open and parenting functions that are available in open entities are not the only ones. So you can click on the link on the on the slide and you will see all the open entry functions with some tutorials and explanations on how to use them in your program. OK, so now we have taken a look at runtime functions, so these runtime functions are basically used inside your code.

### Environment Varibales
The next thing that we have to take a look at our environment, that in this environment, variables are not used in the recording but are specified in the environment, whereas you are compiling them down on your code.

And so the purpose of unfettered access to control the execution of. Part of the program and basically the programs that we're compiling. So this is not specified in the code, but you specified in a saying that it looks to me not only for you compiling that on your program and so on the screen, that basically the three environmental factors that are the same are common. So the only underscore no text specifies a number of threats to use. Yes. So you can send see my handwriting written very well by, for example, if you're using the best you can export this matter. This is very good and specified a number of threats and the program will only work with.

The number of threats to specify the environment better, but the same goes for use in other countries, for example, age, the usage of the virus is about using the word set and the key safe. And you can specify the number of threats use the most similar way. The next society places, so this message specifies on which city visitors should be placed and the displayed in an environment basically shows the open, empty version and that you are then, of course, again, there are multiple other environmental NGOs that you can use. For example, for the GCSE compiler, we can tweak the link and check the environment that it was that you want to use yourself on and all the explanation and examples on how to use those environment.

### Parallel Constructs
The next thing that we take a look at is a parrallel constructs.
So part of the parallel construct is the basic or the fundamental contruct using open pit. So every trade basically executes the same statements which are inside this, the so-called parallel region simultaneously, as you can see on the right image. So first, we have a master plan that executes the serial portion of the code. Then we come to this statement. Yes. So the master first encountered this on construct and creates multiple so-called slave trade safe tracks that run in parallel and master and slave traders then divide between each other. And in the end, we specify an implicit barrier. So when these batteries when these batteries reached, basically the threats finish and we wait for all threats to finish the execution, and when all the tests have finished, the execution will go back to M. M.. That basically presumes the execution of the code. And the threats are, of course, gone because they have completed their test, so this is embedded in the CI A. specified with. You can see the specification for the police that on the bottom left side and trying to specify the bitcoin and bottom line. Yes, and this is basically the end of your bottom of the region and the message that moves on to execute the code in Syria and the slave states and all the other threats and part of the finish line drop in the.




## V: Clauses and directive format
### Directive format
So now we will take a look at Clauses and directives inside openmp. So so far we have just specified a parrallel region and that was it. Then the code came executed in serial and master fed. 
(IMAGE: 
Directive format • Format:
#pragma omp directive_name [clause[clause]...]
• Conditionals: #ifdef _OPENMP
block of code to be executed if code was compiled with OpenMP, for example
      printf(“Number of threads: %d“, omp_get_num_threads);
   #else
block of code to be executed if code was compiled without OpenMP
#endif
)
You get no such file or directory for dot. F opening T So f openmp is a flag is so if I put a command you mean when you compile the file, I assume this this is the problem and that you get so yes, so I will put the comment in the chat. So how do you compile it? So you put GC c - F open pee 


And then you specify the flex of - F open in D. So this - F open until basically tells the compiler that we are compiling the problem with openmp if you don't specify this.

You have you will not be able to run a comparable. So this - F openmp is basically a flag for the GCC compiler and for other compilers you have let's say different flags do for Intel compiler is just open empty without DF and so on. I have those Flex specified in the lighting in the fourth slide if you go back so


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

## E: For and critical directive

