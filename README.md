# ml-docker

Docker images for ML with CUDA support.

## Images

- **cuda-jupyter**: JupyterLab with Python venv ([details](cuda-jupyter/README.md))
- **cuda-conda**: JupyterLab with Conda environment ([details](cuda-conda/README.md))

## Quick Start

```bash
# Use pre-built images
docker run -p 8888:8888 --gpus all ghcr.io/akriaueno/cuda-conda:12.4.1-ubuntu22.04-python3.11
```

## Testing

```bash
# Setup (first time only)
curl -LsSf https://astral.sh/uv/install.sh | sh
uv sync

# Run tests
uv run pytest                    # All tests
uv run pytest -n auto            # Parallel execution
uv run pytest -m cuda_conda      # Only cuda-conda
uv run pytest -m cuda_jupyter    # Only cuda-jupyter
uv run pytest -k "12.4.1"        # Specific version
```

**Note**: Tests are automatically skipped on Apple Silicon Macs as CUDA images require x86_64.