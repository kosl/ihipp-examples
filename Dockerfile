FROM jupyter/minimal-notebook:d990a62010ae
# See https://mybinder.readthedocs.io/en/latest/tutorials/dockerfile.html
# https://jupyter-docker-stacks.readthedocs.io/en/latest/
# See https://hub.docker.com/r/jupyter/minimal-notebook/tags 
# and https://hub.docker.com/r/jupyter/base-notebook/tags for latest tags
   
# create user with a home directory
ARG NB_USER
ARG NB_UID
ENV USER ${NB_USER}
ENV HOME /home/${NB_USER}
# Add RUN statements to install packages as the $NB_USER defined in the base images.
# Add a "USER root" statement followed by RUN statements to install system packages using apt-get,
# change file permissions, etc.
USER root
RUN rm -f /opt/conda/lib/libtinfo.so.6 # use system provided terminfo
# Make sure the contents of our repo are in ${HOME}
RUN ln -s /usr/lib/x86_64-linux-gnu/libc.so.6 /lib64
RUN ln -s /opt/conda/x86_64-conda-linux-gnu/sysroot/usr/lib64/libc_nonshared.a /usr/lib64
COPY . ${HOME}
USER root
RUN chown -R ${NB_UID} ${HOME}
USER ${NB_USER}

# If you do switch to root, always be sure to add a "USER $NB_USER" command at the end of the
# file to ensure the image runs as a unprivileged user by default.
#RUN conda update -n base conda
RUN conda config --set allow_conda_downgrades true
RUN conda config --set notify_outdated_conda false

RUN conda install -c conda-forge xeus-cling=0.12.1 openmpi=4.1.2 openmp openssh mpi4py gfortran_linux-64 numpy
#RUN conda install openmpi -c conda-forge
#RUN conda install openmp -c conda-forge
#RUN conda install openssh -c conda-forge
#RUN conda install mpi4py -c conda-forge

#RUN conda install git -c conda-forge
# Add RISE to the mix as well so user can show live slideshows from their notebooks
# More info at https://rise.readthedocs.io
# Note: Installing RISE with --no-deps because all the neeeded deps are already present.
#RUN conda install rise
# Add nbgitpuller
#RUN pip install nbgitpuller jupyter-resource-usage

# including inline help
COPY inline-help/omp.json /opt/conda/etc/xeus-cling/tags.d
COPY inline-help/mpi.json /opt/conda/etc/xeus-cling/tags.d
COPY inline-help/openmp-doxygen-web.tag /opt/conda/share/xeus-cling/tagfiles
COPY inline-help/mpi-doxygen-web.tag /opt/conda/share/xeus-cling/tagfiles

# Prepare kernels for OpenMP and MPI
RUN sed -i -e '/display_name/s/",/ with OpenMP and MPI",/' \
   -e '/-std=c++/s/$/, "-fopenmp"/' /opt/conda/share/jupyter/kernels/xcpp*/kernel.json
ENV LIBRARY_PATH /opt/conda/lib
ENV LD_LIBRARY_PATH=/opt/conda/lib:$LD_LIBRARY_PATH
#ENV PATH=/usr/bin:$PATH

USER root
# Disable Save icon on the toolbar 
RUN sed -i -e '/var grps =/{n;N;N;N;d}' /opt/conda/lib/python*/site-packages/notebook/static/notebook/js/maintoolbar.js
RUN sed -i -e '/var grps =/{n;N;N;N;d}' /opt/conda/lib/python*/site-packages/notebook/static/notebook/js/main.min.js
# Disable detection of dirty notebook so that beforeunload will not be called
RUN sed -i -e "/events.trigger(.set_dirty.Notebook./d" -e '/env.notebook.set_dirty(true)/d' \
    /opt/conda/lib/python*/site-packages/notebook/static/notebook/js/*.js
    

