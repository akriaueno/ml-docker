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
Open notebook in JupyterLab and check GPU information.

```python
!nvidia-smi
!python3 --version
+-----------------------------------------------------------------------------------------+
| NVIDIA-SMI 560.35.03              Driver Version: 560.35.03      CUDA Version: 12.6     |
|-----------------------------------------+------------------------+----------------------+
| GPU  Name                 Persistence-M | Bus-Id          Disp.A | Volatile Uncorr. ECC |
| Fan  Temp   Perf          Pwr:Usage/Cap |           Memory-Usage | GPU-Util  Compute M. |
|                                         |                        |               MIG M. |
|=========================================+========================+======================|
|   0  NVIDIA GeForce RTX xxxx ...    Off |   00000000:01:00.0 Off |                  N/A |
|  0%   38C    P8              7W /  285W |       2MiB /  16376MiB |      0%      Default |
|                                         |                        |                  N/A |
+-----------------------------------------+------------------------+----------------------+
                                                                                         
+-----------------------------------------------------------------------------------------+
| Processes:                                                                              |
|  GPU   GI   CI        PID   Type   Process name                              GPU Memory |
|        ID   ID                                                               Usage      |
|=========================================================================================|
|  No running processes found                                                             |
+-----------------------------------------------------------------------------------------+
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
