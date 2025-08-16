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

# Create conda environment with specified Python version
RUN ${CONDA_DIR}/bin/conda create -n ml python=${PYTHON_VERSION} -y && \
    echo "conda activate ml" >> ~/.bashrc

# Install JupyterLab in the conda environment
SHELL ["/bin/bash", "-c"]
RUN source ${CONDA_DIR}/etc/profile.d/conda.sh && \
    conda activate ml && \
    pip install jupyterlab

# Set working directory
WORKDIR /workspace

# Expose JupyterLab port
EXPOSE 8888

# Set the default conda environment
ENV CONDA_DEFAULT_ENV=ml
ENV CONDA_PREFIX=${CONDA_DIR}/envs/ml

# Start JupyterLab with conda environment
ENTRYPOINT ["conda", "run", "--no-capture-output", "-n", "ml", "jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root"]