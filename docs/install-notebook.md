# Installing xeus-cling notebook under WSL2
WSL2 insider preview installed with Debian 10 and CUDA drivers
~~~sh
sudo apt-get install wget openssh-client git build-essential
wget https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Linux-x86_64.sh
bash ./Miniforge3-Linux-x86_64.sh
rm Miniforge3-Linux-x86_64.sh
conda create -n xeus-cling xeus-cling=0.12.1 openmp notebook
conda activate xeus-cling
sed -i -e '/display_name/s/",/ OpenMP and MPI",/' \
       -e '/-std=c++/s/$/, "-fopenmp"/' \
       ~/miniforge3/envs/*/share/jupyter/kernels/xcpp*/kernel.json
sudo ln -s $HOME//miniforge3/envs/xeus-cling/lib/gcc/*/* /usr/lib/gcc/x86_64-linux-gnu/
conda install -y binutils openmpi openssh mpi4py gfortran_linux-64
jupyter-notebook
~~~
Clang uses the latest GCC toolchain installed. Alternatively, 
one can specify linker flag such as 
    --gcc-toolchain=/home/lecad/miniforge3/envs/xeus-cling
Ob Debian 10 system installed GCC is version 8. 
Conda installs GCC 9.4.0 and that's why symbolic link (see above) in system dir 
is needed so that we don't need to force --gcc-toolchain flag at every %%executable directive
