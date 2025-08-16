# CUDA Conda

This repository contains a Dockerfile for building a CUDA-enabled Conda environment with JupyterLab.

## Requirements

- Docker
- NVIDIA GPU
- [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html)

## Usage

```bash
docker run -v workspace:/workspace -p 10000:8888 --rm --gpus all ghcr.io/akriaueno/cuda-conda:11.8.0-ubuntu22.04-python3.9
```

Go to http://localhost:10000 and enter the token shown in the terminal.

## Check environment
Open notebook in JupyterLab and check CUDA, Python versions, and Conda environment.

```python
!nvcc --version
!python3 --version
!conda info --envs
!conda list
```

Example output:
```
nvcc: NVIDIA (R) Cuda compiler driver
Copyright (c) 2005-2024 NVIDIA Corporation
Built on Wed_Apr_17_19:19:55_PDT_2024
Cuda compilation tools, release 12.4, V12.4.131
Build cuda_12.4.r12.4/compiler.34097967_0
Python 3.12.0
# conda environments:
#
base                     /opt/conda
ml                    *  /opt/conda/envs/ml
```

## Base Image

The base image is NVIDIA CUDA with the specified CUDA version.
`devel` version is selected as the base image.

https://hub.docker.com/r/nvidia/cuda

## Conda Environment

The Docker image includes Miniconda3 with a dedicated conda environment named `ml`.
This environment is automatically activated when the container starts.

## Image Tag

You can find the images in [ghcr.io](https://github.com/akriaueno/ml-docker/pkgs/container/cuda-conda).

Image tag is based on the following format.

```
ghcr.io/akriaueno/cuda-conda:<cuda_version>-ubuntu<ubuntu_version>-python<python_version>
```

Example:

```
ghcr.io/akriaueno/cuda-conda:11.8.0-ubuntu22.04-python3.9
```

## Features

- Pre-installed Miniconda3 with conda environment management
- Dedicated `ml` conda environment with specified Python version
- JupyterLab pre-installed in the conda environment
- Support for multiple CUDA, Ubuntu, and Python version combinations
- Easy package management with conda/pip

## Supported Versions

| CUDA Version | Ubuntu 22.04 | Ubuntu 24.04 |
|--------------|--------------|--------------|
| 11.8.0       | ✓            | ✗            |
| 12.1.1       | ✓            | ✗            |
| 12.4.1       | ✓            | ✗            |
| 12.6.3       | ✓            | ✓            |
| 12.8.1       | ✓            | ✓            |
| 12.9.1       | ✓            | ✓            |

Each CUDA version supports Python 3.8, 3.9, 3.10, 3.11, and 3.12 (Ubuntu 24.04 supports Python 3.9-3.12 only).