# Installing Jupyter Notebook on *gpu02* login node of the HPCFS cluster

## Cloning the repository

~~~bash
git clone https://github.com/kosl/ihipp-examples.git
~~~

## Loading modules

Open a new *Konsole* shell and load the modules:

~~~bash
module use /opt/pkg/ITER/modules/all
module load NVHPC/21.2
module load OpenMPI/4.1.2-GCC-10.2.0
module load Python/3.8.6-GCCcore-10.2.0
~~~

This must be done every time a new shell is opened.

## Creating a Python virtual environment with needed Python packages

~~~bash
python3 -m venv notebook
notebook/bin/pip install --upgrade pip jupyterlab mpi4py pycuda pyopencl
~~~

This is done only once.

## Activating the virtual environment `notebook` and starting Jupyter Notebook in browser:

~~~bash
source notebook/bin/activate
(notebook) [bogdanl@gpu02 ~]$ cd ihipp-examples
(notebook) [bogdanl@gpu02 ihipp-examples]$ jupyter notebook
~~~

This must be done every time a new shell is opened. In the browser you can navigate through the repository, open the notebooks (`*.ipynb`) and run (or modify and run) them.

Note, that you must be in the home directory (`~`) to activate the virtual environment 

After quitting Jupyter Notebook in browser, the virtual environment in the shell can be deactivated with:

~~~bash
(notebook) [bogdanl@gpu02 ihipp-examples]$ deactivate
[bogdanl@gpu02 ihipp-examples]$
~~~