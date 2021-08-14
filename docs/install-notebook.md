# Installing xeus-cling notebook under WSL2
WSL2 installed with Debian 10 and CUDA drivers
~~~sh
sudo apt-get install wget
wget https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Linux-x86_64.sh
bash ./Miniforge3-Linux-x86_64.sh
rm Miniforge3-Linux-x86_64.sh
conda create -n xeus-cling xeus-cling=0.12.1 openmp notebook
conda activate xeus-cling
sed -i -e '/display_name/s/",/ OpenMP and MPI",/' \
       -e '/-std=c++/s/$/, "-fopenmp"/' \
       ~/miniforge3/envs/*/share/jupyter/kernels/xcpp*/kernel.json
jupyter-notebook
~~~
