# ml-docker
Docker file/image for ML

## Available Images

### cuda-jupyter
CUDA-enabled JupyterLab Docker images with Python virtual environment.
- See [cuda-jupyter/README.md](cuda-jupyter/README.md) for details

### cuda-conda
CUDA-enabled Conda environment Docker images with JupyterLab.
- See [cuda-conda/README.md](cuda-conda/README.md) for details

## Local Testing

### Quick Test
Test a single configuration:
```bash
./test/quick-test.sh cuda-conda 12.4.1 22.04 3.11
```

### Comprehensive Test
Test multiple configurations:
```bash
./test/test-build.sh                    # Test all images
./test/test-build.sh cuda-conda         # Test only cuda-conda
./test/test-build.sh cuda-jupyter       # Test only cuda-jupyter
```
