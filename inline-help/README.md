# Inline documentation for jupyter notebook

This folder contains scripts [create_openmp_tagfile.py](/inline-help/create_openmp_tagfile.py) and
[create_mpi_tagfile.py](/inline-help/create_mpi_tagfile.py) which 
create a json file and a doxygen tag file for the OpenMP and MPI documentation from online pages. 

[create_openmp_tagfile.py](/inline-help/create_openmp_tagfile.py) produces [openmp-doxygen-web.tag.xml](/inline-help/openmp-doxygen-web.tag.xml) and [omp.json](/inline-help/omp.json). 

[create_mpi_tagfile.py](/inline-help/create_mpi_tagfile.py) produces [mpi-doxygen-web.tag.xml](/inline-help/mpi-doxygen-web.tag.xml) and [mpi.json](/inline-help/mpi.json). 

Include tagfile and matching json file in the xeus-cling directory 
(from instructions on [xeus-cling documentation](https://xeus-cling.readthedocs.io/en/latest/inline_help.html)). 

Example calling help:

~~~c
?MPI::MPI_Send
?mpi::MPI_Send
?MPI_Send

?omp::sections
?sections

?omp::parallel_sections
?omp::parallelsections
 ~~~
