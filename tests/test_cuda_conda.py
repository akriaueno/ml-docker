"""Tests for cuda-conda Docker images."""
import subprocess
import pytest
import platform
from pathlib import Path


# Test matrix for cuda-conda images
CUDA_CONDA_MATRIX = [
    # CUDA 11.8 - Ubuntu 22.04
    pytest.param("11.8.0", "22.04", "3.8", marks=[pytest.mark.cuda11]),
    pytest.param("11.8.0", "22.04", "3.9", marks=[pytest.mark.cuda11]),
    pytest.param("11.8.0", "22.04", "3.10", marks=[pytest.mark.cuda11]),
    pytest.param("11.8.0", "22.04", "3.11", marks=[pytest.mark.cuda11]),
    pytest.param("11.8.0", "22.04", "3.12", marks=[pytest.mark.cuda11]),
    # CUDA 12.1 - Ubuntu 22.04
    pytest.param("12.1.1", "22.04", "3.8", marks=[pytest.mark.cuda12]),
    pytest.param("12.1.1", "22.04", "3.9", marks=[pytest.mark.cuda12]),
    pytest.param("12.1.1", "22.04", "3.10", marks=[pytest.mark.cuda12]),
    pytest.param("12.1.1", "22.04", "3.11", marks=[pytest.mark.cuda12]),
    pytest.param("12.1.1", "22.04", "3.12", marks=[pytest.mark.cuda12]),
    # CUDA 12.4 - Ubuntu 22.04
    pytest.param("12.4.1", "22.04", "3.8", marks=[pytest.mark.cuda12]),
    pytest.param("12.4.1", "22.04", "3.9", marks=[pytest.mark.cuda12]),
    pytest.param("12.4.1", "22.04", "3.10", marks=[pytest.mark.cuda12]),
    pytest.param("12.4.1", "22.04", "3.11", marks=[pytest.mark.cuda12]),
    pytest.param("12.4.1", "22.04", "3.12", marks=[pytest.mark.cuda12]),
    # CUDA 12.6 - Ubuntu 24.04
    pytest.param("12.6.3", "24.04", "3.9", marks=[pytest.mark.cuda12]),
    pytest.param("12.6.3", "24.04", "3.10", marks=[pytest.mark.cuda12]),
    pytest.param("12.6.3", "24.04", "3.11", marks=[pytest.mark.cuda12]),
    pytest.param("12.6.3", "24.04", "3.12", marks=[pytest.mark.cuda12]),
    # CUDA 12.8 - Ubuntu 22.04
    pytest.param("12.8.1", "22.04", "3.9", marks=[pytest.mark.cuda12]),
    pytest.param("12.8.1", "22.04", "3.10", marks=[pytest.mark.cuda12]),
    pytest.param("12.8.1", "22.04", "3.11", marks=[pytest.mark.cuda12]),
    pytest.param("12.8.1", "22.04", "3.12", marks=[pytest.mark.cuda12]),
    # CUDA 12.8 - Ubuntu 24.04
    pytest.param("12.8.1", "24.04", "3.9", marks=[pytest.mark.cuda12]),
    pytest.param("12.8.1", "24.04", "3.10", marks=[pytest.mark.cuda12]),
    pytest.param("12.8.1", "24.04", "3.11", marks=[pytest.mark.cuda12]),
    pytest.param("12.8.1", "24.04", "3.12", marks=[pytest.mark.cuda12]),
    # CUDA 12.9 - Ubuntu 22.04
    pytest.param("12.9.0", "22.04", "3.9", marks=[pytest.mark.cuda12]),
    pytest.param("12.9.0", "22.04", "3.10", marks=[pytest.mark.cuda12]),
    pytest.param("12.9.0", "22.04", "3.11", marks=[pytest.mark.cuda12]),
    pytest.param("12.9.0", "22.04", "3.12", marks=[pytest.mark.cuda12]),
]


@pytest.mark.cuda_conda
class TestCudaCondaBuild:
    """Tests for cuda-conda Docker images."""
    
    @pytest.mark.parametrize("cuda_version,ubuntu_version,python_version", CUDA_CONDA_MATRIX)
    def test_build_cuda_conda(self, cuda_version, ubuntu_version, python_version, 
                            project_root, docker_build_timeout, cleanup_docker_images, is_arm_mac):
        """Test building cuda-conda image with various configurations."""
        # ARM Macでのビルドに関する注意
        if is_arm_mac:
            pytest.skip("Skipping x86_64 CUDA image build on ARM Mac. Use '--platform linux/amd64' flag or test on x86_64 machine.")
            
        tag = f"cuda-conda-test:{cuda_version}-ubuntu{ubuntu_version}-python{python_version}"
        cleanup_docker_images(tag)
        
        # Build the image with platform specification
        build_cmd = [
            "docker", "build",
            "--platform", "linux/amd64",  # 明示的にx86_64を指定
            "--build-arg", f"CUDA_VERSION={cuda_version}",
            "--build-arg", f"UBUNTU_VERSION={ubuntu_version}",
            "--build-arg", f"PYTHON_VERSION={python_version}",
            "-t", tag,
            "-f", "cuda-conda/Dockerfile",
            "cuda-conda/"
        ]
        
        result = subprocess.run(
            build_cmd, 
            cwd=project_root, 
            capture_output=True, 
            text=True, 
            timeout=docker_build_timeout
        )
        
        if result.returncode != 0:
            # プラットフォーム関連のエラーをチェック
            if "rosetta error" in result.stderr or "exec format error" in result.stderr:
                pytest.skip("Platform compatibility issue detected. This test requires x86_64 architecture.")
            
            assert False, f"Build failed:\nCommand: {' '.join(build_cmd)}\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
        
        # Verify the image runs (basic test)
        verify_result = subprocess.run([
            "docker", "run", "--rm", "--platform", "linux/amd64", 
            "--entrypoint", "/opt/conda/envs/ml/bin/python", tag, 
            "-c", "print('Container is working')"
        ], capture_output=True, text=True, timeout=30)
        
        assert verify_result.returncode == 0, f"Failed to run container:\n{verify_result.stderr}"
        assert "Container is working" in verify_result.stdout, "Container test failed"
        
        # Verify Python version
        python_check = subprocess.run([
            "docker", "run", "--rm", "--platform", "linux/amd64",
            "--entrypoint", "/opt/conda/envs/ml/bin/python", tag,
            "-c", "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')"
        ], capture_output=True, text=True, timeout=30)
        
        assert python_check.returncode == 0, f"Failed to check Python version:\n{python_check.stderr}"
        assert python_version in python_check.stdout, f"Expected Python {python_version}, got: {python_check.stdout.strip()}"
        
        # Verify CUDA version
        cuda_check = subprocess.run([
            "docker", "run", "--rm", "--platform", "linux/amd64",
            "--entrypoint", "bash", tag,
            "-c", "nvcc --version | grep 'release' | sed 's/.*release //' | sed 's/,.*//'"
        ], capture_output=True, text=True, timeout=30)
        
        assert cuda_check.returncode == 0, f"Failed to check CUDA version:\n{cuda_check.stderr}"
        # CUDAバージョンの確認（メジャー・マイナーバージョンのみ）
        cuda_version_short = '.'.join(cuda_version.split('.')[:2])
        assert cuda_version_short in cuda_check.stdout, f"Expected CUDA {cuda_version_short}, got: {cuda_check.stdout.strip()}"
        
        # Verify conda is working
        conda_check = subprocess.run([
            "docker", "run", "--rm", "--platform", "linux/amd64",
            "--entrypoint", "bash", tag,
            "-c", "source /opt/conda/etc/profile.d/conda.sh && conda activate ml && conda --version"
        ], capture_output=True, text=True, timeout=30)
        
        assert conda_check.returncode == 0, f"Failed to check conda:\n{conda_check.stderr}"
        assert "conda" in conda_check.stdout, f"Conda not found in output: {conda_check.stdout}"
        
        # Verify conda can install packages
        conda_install_check = subprocess.run([
            "docker", "run", "--rm", "--platform", "linux/amd64",
            "--entrypoint", "bash", tag,
            "-c", "source /opt/conda/etc/profile.d/conda.sh && conda activate ml && conda install -y numpy --override-channels -c conda-forge && python -c 'import numpy; print(f\"NumPy {numpy.__version__} installed\")'"
        ], capture_output=True, text=True, timeout=120)
        
        assert conda_install_check.returncode == 0, f"Failed to install with conda:\n{conda_install_check.stderr}"
        assert "NumPy" in conda_install_check.stdout and "installed" in conda_install_check.stdout, f"NumPy installation failed: {conda_install_check.stdout}"


@pytest.mark.cuda_conda
@pytest.mark.slow
def test_minimal_cuda_conda_build(project_root, docker_build_timeout, cleanup_docker_images, is_arm_mac):
    """Test a minimal cuda-conda build configuration."""
    if is_arm_mac:
        pytest.skip("Skipping x86_64 CUDA image build on ARM Mac.")
        
    tag = "cuda-conda-test:minimal"
    cleanup_docker_images(tag)
    
    result = subprocess.run([
        "docker", "build",
        "--platform", "linux/amd64",
        "--build-arg", "CUDA_VERSION=12.4.1",
        "--build-arg", "UBUNTU_VERSION=22.04",
        "--build-arg", "PYTHON_VERSION=3.11",
        "-t", tag,
        "-f", "cuda-conda/Dockerfile",
        "cuda-conda/"
    ], cwd=project_root, capture_output=True, text=True, timeout=docker_build_timeout)
    
    if result.returncode != 0 and ("rosetta error" in result.stderr or "exec format error" in result.stderr):
        pytest.skip("Platform compatibility issue detected.")
        
    assert result.returncode == 0, f"Minimal build failed:\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
    
    # Verify the image runs
    verify_result = subprocess.run([
        "docker", "run", "--rm", "--platform", "linux/amd64",
        "--entrypoint", "/opt/conda/envs/ml/bin/python", tag,
        "-c", "print('Minimal test passed')"
    ], capture_output=True, text=True, timeout=30)
    
    assert verify_result.returncode == 0, f"Failed to run container:\n{verify_result.stderr}"
    
    # Verify Python version for minimal build
    python_check = subprocess.run([
        "docker", "run", "--rm", "--platform", "linux/amd64",
        "--entrypoint", "/opt/conda/envs/ml/bin/python", tag,
        "-c", "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')"
    ], capture_output=True, text=True, timeout=30)
    
    assert python_check.returncode == 0
    assert "3.11" in python_check.stdout