"""Pytest configuration and fixtures for ml-docker tests."""
import pytest
import subprocess
import platform
from pathlib import Path


@pytest.fixture(scope="session")
def project_root():
    """Return the project root directory."""
    return Path(__file__).parent.parent


@pytest.fixture(scope="session")
def docker_available():
    """Check if Docker is available and running."""
    try:
        result = subprocess.run(
            ["docker", "info"],
            capture_output=True,
            text=True,
            timeout=5
        )
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False


@pytest.fixture(autouse=True)
def skip_if_no_docker(docker_available):
    """Skip tests if Docker is not available."""
    if not docker_available:
        pytest.skip("Docker is not available")


@pytest.fixture
def docker_build_timeout():
    """Timeout for Docker build operations in seconds."""
    return 1200  # 20 minutes


@pytest.fixture(scope="session")
def is_arm_mac():
    """Check if running on ARM-based Mac."""
    return platform.system() == "Darwin" and platform.machine() == "arm64"


@pytest.fixture
def cleanup_docker_images():
    """Cleanup test Docker images after test completion."""
    images_to_cleanup = []
    
    def _add_image(image_tag):
        images_to_cleanup.append(image_tag)
    
    yield _add_image
    
    # クリーンアップ処理
    for image in images_to_cleanup:
        try:
            subprocess.run(
                ["docker", "rmi", "-f", image],
                capture_output=True,
                timeout=30
            )
        except subprocess.TimeoutExpired:
            pass  # 削除に失敗しても続行


def pytest_sessionfinish(session, exitstatus):
    """Clean up all test Docker images after test session."""
    # テスト用イメージを全て削除
    try:
        # cuda-condaテストイメージを検索して削除
        result = subprocess.run(
            ["docker", "images", "--format", "{{.Repository}}:{{.Tag}}", 
             "--filter", "reference=cuda-conda-test:*"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0 and result.stdout:
            images = result.stdout.strip().split('\n')
            for image in images:
                if image:
                    subprocess.run(
                        ["docker", "rmi", "-f", image],
                        capture_output=True,
                        timeout=30
                    )
        
        # cuda-jupyterテストイメージを検索して削除
        result = subprocess.run(
            ["docker", "images", "--format", "{{.Repository}}:{{.Tag}}", 
             "--filter", "reference=cuda-jupyter-test:*"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0 and result.stdout:
            images = result.stdout.strip().split('\n')
            for image in images:
                if image:
                    subprocess.run(
                        ["docker", "rmi", "-f", image],
                        capture_output=True,
                        timeout=30
                    )
    except (subprocess.TimeoutExpired, Exception):
        pass  # クリーンアップが失敗しても続行