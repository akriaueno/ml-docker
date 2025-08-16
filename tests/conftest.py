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
    return 600  # 10 minutes


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