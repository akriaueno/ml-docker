ARG CUDA_VERSION=12.4.1
ARG UBUNTU_VERSION=24.04

FROM nvidia/cuda:${CUDA_VERSION}-devel-ubuntu${UBUNTU_VERSION}

ARG PYTHON_VERSION=3.12
ENV PYTHON_VERSION=${PYTHON_VERSION}

# Install system dependencies
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    curl \
    wget \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Install Miniconda
ENV CONDA_DIR=/opt/conda
ENV PATH="${CONDA_DIR}/bin:${PATH}"

# Detect architecture and download appropriate Miniconda installer
RUN ARCH=$(uname -m) && \
    if [ "$ARCH" = "aarch64" ]; then \
        MINICONDA_URL="https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-aarch64.sh"; \
    else \
        MINICONDA_URL="https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh"; \
    fi && \
    wget --quiet $MINICONDA_URL -O ~/miniconda.sh && \
    /bin/bash ~/miniconda.sh -b -p ${CONDA_DIR} && \
    rm ~/miniconda.sh && \
    ${CONDA_DIR}/bin/conda clean -a -y

# Configure conda to use only conda-forge channel (avoids ToS issues)
RUN ${CONDA_DIR}/bin/conda config --remove channels defaults || true && \
    ${CONDA_DIR}/bin/conda config --add channels conda-forge && \
    ${CONDA_DIR}/bin/conda config --set channel_priority strict

# Create conda environment with specified Python version
# Retry logic for conda operations to handle intermittent network issues
RUN for i in 1 2 3; do \
        ${CONDA_DIR}/bin/conda create -n ml python=${PYTHON_VERSION} -y --override-channels --channel conda-forge && \
        echo "conda activate ml" >> ~/.bashrc && \
        break || \
        (echo "Retry $i failed, waiting..." && sleep 10); \
    done

# Install JupyterLab in the conda environment
SHELL ["/bin/bash", "-c"]
RUN source ${CONDA_DIR}/etc/profile.d/conda.sh && \
    conda activate ml && \
    for i in 1 2 3; do \
        conda install -y jupyterlab --override-channels -c conda-forge && \
        break || \
        (echo "Retry $i failed, waiting..." && sleep 10); \
    done

# Set working directory
WORKDIR /workspace

# Expose JupyterLab port
EXPOSE 8888

# Set the default conda environment
ENV CONDA_DEFAULT_ENV=ml
ENV CONDA_PREFIX=${CONDA_DIR}/envs/ml

