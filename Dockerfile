FROM jupyter/minimal-notebook
#FROM jupyter/minimal-notebook:612aa5710bf9
#FROM jupyter/base-notebook

# Add RUN statements to install packages as the $NB_USER defined in the base images.

# Add a "USER root" statement followed by RUN statements to install system packages using apt-get,
# change file permissions, etc.
USER root
RUN ln -s /usr/lib/x86_64-linux-gnu/libc.so.6 /lib64
RUN ln -s /opt/conda/x86_64-conda-linux-gnu/sysroot/usr/lib64/libc_nonshared.a /usr/lib64
#RUN apt-get install openssh-server
USER $NB_USER
# If you do switch to root, always be sure to add a "USER $NB_USER" command at the end of the
# file to ensure the image runs as a unprivileged user by default.
ENV LIBRARY_PATH /opt/conda/lib
RUN conda install xeus-cling=0.12.1 -c conda-forge
RUN conda install openmpi -c conda-forge
RUN conda install openmp -c conda-forge
RUN conda install openssh -c conda-forge
#RUN conda install git -c conda-forge
ENV LD_LIBRARY_PATH=/opt/conda/lib:$LD_LIBRARY_PATH
# Add RISE to the mix as well so user can show live slideshows from their notebooks
# More info at https://rise.readthedocs.io
# Note: Installing RISE with --no-deps because all the neeeded deps are already present.
#RUN conda install rise
# Add nbgitpuller
#RUN pip install nbgitpuller jupyter-resource-usage
RUN sed -i -e '/display_name/s/",/ with OpenMP and MPI",/' -e '/-std=c++/s/$/, "-fopenmp"/' /opt/conda/share/jupyter/kernels/xcpp*/kernel.json


# Disable Save icon on the toolbar 
RUN sed -i -e '/var grps =/{n;N;N;N;d}' /opt/conda/lib/python3.8/site-packages/notebook/static/notebook/js/maintoolbar.js
RUN sed -i -e '/var grps =/{n;N;N;N;d}' /opt/conda/lib/python3.8/site-packages/notebook/static/notebook/js/main.min.js
# Disable detection of dirty notebook so that beforeunload will not be called
RUN sed -i -e "/events.trigger(.set_dirty.Notebook./d" -e '/env.notebook.set_dirty(true)/d' \
    /opt/conda/lib/python3.8/site-packages/notebook/static/notebook/js/*.js
