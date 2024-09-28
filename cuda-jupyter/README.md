# CUDA Jupyter

This repository contains a Dockerfile for building a CUDA-enabled JupyterLab image.

## Requirements

- Docker
- NVIDIA GPU
- [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html)

## Usage

```bash
docker run -v workspace:/workspace -p 10000:8888 --rm --gpus all ghcr.io/akriaueno/cuda-jupyter:11.8.0-ubuntu22.04-python3.9
```

Go to http://localhost:10000 and enter the token shown in the terminal.

## Check environment
Open notebook in JupyterLab and check CUDA and Python versions.

```python
!nvcc --version
!python3 --version
nvcc: NVIDIA (R) Cuda compiler driver
Copyright (c) 2005-2022 NVIDIA Corporation
Built on Wed_Sep_21_10:33:58_PDT_2022
Cuda compilation tools, release 11.8, V11.8.89
Build cuda_11.8.r11.8/compiler.31833905_0
Python 3.9.20
```

## Base Image

The base image is NVIDIA CUDA with the specified CUDA version.
`devel` version is selected as the base image.

https://hub.docker.com/r/nvidia/cuda

## Image Tag

You can find the images in [ghcr.io](https://github.com/akriaueno/ml-docker/pkgs/container/cuda-jupyter).

Image tag is based on the following format.

```
ghcr.io/akriaueno/cuda-jupyter:<cuda_version>-ubuntu<ubuntu_version>-python<python_version>
```

Example:

```
ghcr.io/akriaueno/cuda-jupyter:11.8.0-ubuntu22.04-python3.9
```
