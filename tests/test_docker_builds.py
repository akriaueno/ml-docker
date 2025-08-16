"""Tests for Docker image builds."""
import subprocess
import pytest
import platform
from pathlib import Path


# Test matrix definitions
CUDA_CONDA_MATRIX = [
    # CUDA 11.8
    pytest.param("11.8.0", "22.04", "3.8", marks=[pytest.mark.cuda11, pytest.mark.cuda_conda]),
    pytest.param("11.8.0", "22.04", "3.9", marks=[pytest.mark.cuda11, pytest.mark.cuda_conda]),
    pytest.param("11.8.0", "22.04", "3.10", marks=[pytest.mark.cuda11, pytest.mark.cuda_conda]),
    pytest.param("11.8.0", "22.04", "3.11", marks=[pytest.mark.cuda11, pytest.mark.cuda_conda]),
    pytest.param("11.8.0", "22.04", "3.12", marks=[pytest.mark.cuda11, pytest.mark.cuda_conda]),
    # CUDA 12.1
    pytest.param("12.1.1", "22.04", "3.8", marks=[pytest.mark.cuda12, pytest.mark.cuda_conda]),
    pytest.param("12.1.1", "22.04", "3.9", marks=[pytest.mark.cuda12, pytest.mark.cuda_conda]),
    pytest.param("12.1.1", "22.04", "3.10", marks=[pytest.mark.cuda12, pytest.mark.cuda_conda]),
    pytest.param("12.1.1", "22.04", "3.11", marks=[pytest.mark.cuda12, pytest.mark.cuda_conda]),
    pytest.param("12.1.1", "22.04", "3.12", marks=[pytest.mark.cuda12, pytest.mark.cuda_conda]),
    # CUDA 12.4
    pytest.param("12.4.1", "22.04", "3.8", marks=[pytest.mark.cuda12, pytest.mark.cuda_conda]),
    pytest.param("12.4.1", "22.04", "3.9", marks=[pytest.mark.cuda12, pytest.mark.cuda_conda]),
    pytest.param("12.4.1", "22.04", "3.10", marks=[pytest.mark.cuda12, pytest.mark.cuda_conda]),
    pytest.param("12.4.1", "22.04", "3.11", marks=[pytest.mark.cuda12, pytest.mark.cuda_conda]),
    pytest.param("12.4.1", "22.04", "3.12", marks=[pytest.mark.cuda12, pytest.mark.cuda_conda]),
    # CUDA 12.1 - Ubuntu 24.04
    pytest.param("12.1.1", "24.04", "3.8", marks=[pytest.mark.cuda12, pytest.mark.cuda_conda]),
    pytest.param("12.1.1", "24.04", "3.9", marks=[pytest.mark.cuda12, pytest.mark.cuda_conda]),
    pytest.param("12.1.1", "24.04", "3.10", marks=[pytest.mark.cuda12, pytest.mark.cuda_conda]),
    pytest.param("12.1.1", "24.04", "3.11", marks=[pytest.mark.cuda12, pytest.mark.cuda_conda]),
    pytest.param("12.1.1", "24.04", "3.12", marks=[pytest.mark.cuda12, pytest.mark.cuda_conda]),
    # CUDA 12.4 - Ubuntu 24.04
    pytest.param("12.4.1", "24.04", "3.8", marks=[pytest.mark.cuda12, pytest.mark.cuda_conda]),
    pytest.param("12.4.1", "24.04", "3.9", marks=[pytest.mark.cuda12, pytest.mark.cuda_conda]),
    pytest.param("12.4.1", "24.04", "3.10", marks=[pytest.mark.cuda12, pytest.mark.cuda_conda]),
    pytest.param("12.4.1", "24.04", "3.11", marks=[pytest.mark.cuda12, pytest.mark.cuda_conda]),
    pytest.param("12.4.1", "24.04", "3.12", marks=[pytest.mark.cuda12, pytest.mark.cuda_conda]),
]

CUDA_JUPYTER_MATRIX = [
    # CUDA 11.8
    pytest.param("11.8.0", "22.04", "3.9", marks=[pytest.mark.cuda11, pytest.mark.cuda_jupyter]),
    pytest.param("11.8.0", "22.04", "3.10", marks=[pytest.mark.cuda11, pytest.mark.cuda_jupyter]),
    pytest.param("11.8.0", "22.04", "3.11", marks=[pytest.mark.cuda11, pytest.mark.cuda_jupyter]),
    pytest.param("11.8.0", "22.04", "3.12", marks=[pytest.mark.cuda11, pytest.mark.cuda_jupyter]),
    # CUDA 12.1
    pytest.param("12.1.1", "22.04", "3.9", marks=[pytest.mark.cuda12, pytest.mark.cuda_jupyter]),
    pytest.param("12.1.1", "22.04", "3.10", marks=[pytest.mark.cuda12, pytest.mark.cuda_jupyter]),
    pytest.param("12.1.1", "22.04", "3.11", marks=[pytest.mark.cuda12, pytest.mark.cuda_jupyter]),
    pytest.param("12.1.1", "22.04", "3.12", marks=[pytest.mark.cuda12, pytest.mark.cuda_jupyter]),
    # CUDA 12.4
    pytest.param("12.4.1", "22.04", "3.9", marks=[pytest.mark.cuda12, pytest.mark.cuda_jupyter]),
    pytest.param("12.4.1", "22.04", "3.10", marks=[pytest.mark.cuda12, pytest.mark.cuda_jupyter]),
    pytest.param("12.4.1", "22.04", "3.11", marks=[pytest.mark.cuda12, pytest.mark.cuda_jupyter]),
    pytest.param("12.4.1", "22.04", "3.12", marks=[pytest.mark.cuda12, pytest.mark.cuda_jupyter]),
    # CUDA 12.6
    pytest.param("12.6.1", "22.04", "3.9", marks=[pytest.mark.cuda12, pytest.mark.cuda_jupyter]),
    pytest.param("12.6.1", "22.04", "3.10", marks=[pytest.mark.cuda12, pytest.mark.cuda_jupyter]),
    pytest.param("12.6.1", "22.04", "3.11", marks=[pytest.mark.cuda12, pytest.mark.cuda_jupyter]),
    pytest.param("12.6.1", "22.04", "3.12", marks=[pytest.mark.cuda12, pytest.mark.cuda_jupyter]),
    pytest.param("12.6.1", "24.04", "3.9", marks=[pytest.mark.cuda12, pytest.mark.cuda_jupyter]),
    pytest.param("12.6.1", "24.04", "3.10", marks=[pytest.mark.cuda12, pytest.mark.cuda_jupyter]),
    pytest.param("12.6.1", "24.04", "3.11", marks=[pytest.mark.cuda12, pytest.mark.cuda_jupyter]),
    pytest.param("12.6.1", "24.04", "3.12", marks=[pytest.mark.cuda12, pytest.mark.cuda_jupyter]),
]


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
        
        # Verify the image runs
        verify_result = subprocess.run([
            "docker", "run", "--rm", "--platform", "linux/amd64", tag, "jupyter", "--version"
        ], capture_output=True, text=True, timeout=30)
        
        assert verify_result.returncode == 0, f"Failed to run jupyter:\n{verify_result.stderr}"
        assert "jupyter" in verify_result.stdout.lower(), "Jupyter version not found in output"


class TestCudaJupyterBuild:
    """Tests for cuda-jupyter Docker images."""
    
    @pytest.mark.parametrize("cuda_version,ubuntu_version,python_version", CUDA_JUPYTER_MATRIX)
    def test_build_cuda_jupyter(self, cuda_version, ubuntu_version, python_version,
                              project_root, docker_build_timeout, cleanup_docker_images, is_arm_mac):
        """Test building cuda-jupyter image with various configurations."""
        # ARM Macでのビルドに関する注意
        if is_arm_mac:
            pytest.skip("Skipping x86_64 CUDA image build on ARM Mac. Use '--platform linux/amd64' flag or test on x86_64 machine.")
            
        tag = f"cuda-jupyter-test:{cuda_version}-ubuntu{ubuntu_version}-python{python_version}"
        cleanup_docker_images(tag)
        
        # Build the image with platform specification
        build_cmd = [
            "docker", "build",
            "--platform", "linux/amd64",  # 明示的にx86_64を指定
            "--build-arg", f"CUDA_VERSION={cuda_version}",
            "--build-arg", f"UBUNTU_VERSION={ubuntu_version}",
            "--build-arg", f"PYTHON_VERSION={python_version}",
            "-t", tag,
            "-f", "cuda-jupyter/Dockerfile",
            "cuda-jupyter/"
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
        
        # Verify the image runs
        verify_result = subprocess.run([
            "docker", "run", "--rm", "--platform", "linux/amd64", tag, "jupyter", "--version"
        ], capture_output=True, text=True, timeout=30)
        
        assert verify_result.returncode == 0, f"Failed to run jupyter:\n{verify_result.stderr}"
        assert "jupyter" in verify_result.stdout.lower(), "Jupyter version not found in output"


@pytest.mark.slow
class TestQuickValidation:
    """Quick validation tests for smoke testing."""
    
    def test_minimal_cuda_conda_build(self, project_root, docker_build_timeout, cleanup_docker_images, is_arm_mac):
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
            
        assert result.returncode == 0, f"Minimal build failed:\n{result.stderr}"