FROM ubuntu:16.04

ENV LANG C.UTF-8
ENV PYTHONUNBUFFERED 1
ENV CONDA_DIR /opt/conda
ENV PATH $CONDA_DIR/bin:$PATH

RUN mkdir -p $CONDA_DIR && \
    echo export PATH=$CONDA_DIR/bin:'$PATH' > /etc/profile.d/conda.sh && \
    apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y wget git bzip2 --no-install-recommends && \
    apt-get clean && rm -rf /var/cache/apt/archives/* /var/lib/apt/lists/* && \
    wget --quiet --no-check-certificate https://repo.continuum.io/miniconda/Miniconda3-4.2.12-Linux-x86_64.sh && \
    echo "c59b3dd3cad550ac7596e0d599b91e75d88826db132e4146030ef471bb434e9a *Miniconda3-4.2.12-Linux-x86_64.sh" | sha256sum -c - && \
    /bin/bash /Miniconda3-4.2.12-Linux-x86_64.sh -f -b -p $CONDA_DIR && \
    rm Miniconda3-4.2.12-Linux-x86_64.sh

ARG NB_USER=user
ARG NB_UID=1001

RUN useradd -m -s /bin/bash -N -u $NB_UID $NB_USER && \
    mkdir -p $CONDA_DIR && \
    chown $NB_USER $CONDA_DIR -R && \
    mkdir -p /src && \
    chown $NB_USER /src

USER $NB_USER


ARG python_version=2.7

RUN conda install -y python=${python_version} && \
    pip install --upgrade pip && \
    conda install opencv && \
    conda install pytorch torchvision -c soumith && \
    conda clean -yt

RUN pip install tornado

ENV PYTHONPATH='/src/:$PYTHONPATH'

WORKDIR /src
