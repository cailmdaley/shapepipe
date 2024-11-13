FROM python:3.12-bookworm

LABEL Description="Conda-Free ShapePipe Docker Image"
ENV SHELL=/bin/bash

# Install system dependencies
RUN apt-get update -y --quiet --fix-missing && \
    apt-get dist-upgrade -y --quiet --fix-missing && \
    apt-get install -y --quiet \
    acl \
    apt-utils \
    autoconf \
    automake \
    build-essential \
    cmake  \
    curl \
    ffmpeg \
    g++ \
    gcc  \
    gfortran \
    git-lfs \
    libatlas-base-dev  \
    libblas-dev \
    libcfitsio-dev \
    libfftw3-bin  \
    libfftw3-dev \
    libgl1-mesa-glx \
    liblapack-dev \
    libopenmpi-dev \
    libtool  \
    libtool-bin  \
    libtool-doc \
    locales \
    locate \
    make \
    openmpi-bin \
    pandoc \
    protobuf-compiler \
    psfex=3.21.1-1 \
    sextractor=2.25.0+ds-3 \
    sssd \
    weightwatcher \
    vim \
    xterm && \
    apt-get clean -y && \
    apt-get autoremove --purge --quiet -y && \
    rm -rf /var/lib/apt/lists/* /var/tmp/*

# Install python dependencies
RUN pip install --no-cache-dir \ 
    astropy \
    cs_util \
    galsim \
    joblib \
    matplotlib \
    mccd \
    modopt \
    mpi4py \
    numba \
    numpy \
    numpydoc \
    pandas \
    PyQt5 \
    pyqtgraph \
    python-pysap \
    pytest \
    pytest-cov \
    pytest-pycodestyle \
    pytest-pydocstyle \
    reproject \
    sf_tools \
    sip_tpv \
    skaha \
    sqlitedict \
    termcolor \
    tqdm \
    treecorr \
    vos \
    git+https://github.com/aguinot/ngmix@stable_version \
    git+https://github.com/tobias-liaudat/Stile@v0.1

WORKDIR /app
COPY . /app/.


# Install shapepipe and symlink scripts
RUN pip install --no-cache-dir -e . && \ 
    for ext in .py .sh .bash; do \
    for script in /app/scripts/*/*$ext; do \
    link_name=`basename $script $ext`; \
    ln -s $script /usr/local/bin/$link_name; \
    done; \
    done

ENV PATH="/app/scripts:${PATH}"

CMD ["bash"]
