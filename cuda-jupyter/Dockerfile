ARG CUDA_VERSION=12.6.1
ARG UBUNTU_VERSION=24.04

FROM nvidia/cuda:${CUDA_VERSION}-devel-ubuntu${UBUNTU_VERSION}

ARG PYTHON_VERSION=3.12
ENV PYTHON_VERSION=${PYTHON_VERSION}

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
    curl \
    git \
    software-properties-common \
    wget

RUN add-apt-repository ppa:deadsnakes/ppa && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
    python${PYTHON_VERSION}-full \
    python${PYTHON_VERSION}-dev \
    && rm -rf /var/lib/apt/lists/*

RUN ln -s /usr/bin/python${PYTHON_VERSION} /usr/local/bin/python
RUN ln -s /usr/bin/python${PYTHON_VERSION} /usr/local/bin/python3

RUN python -m venv /opt/jupyterlab
ENV PATH="/opt/jupyterlab/bin:$PATH"

RUN pip install jupyterlab

WORKDIR /workspace

EXPOSE 8888

ENTRYPOINT ["/opt/jupyterlab/bin/jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root"]
