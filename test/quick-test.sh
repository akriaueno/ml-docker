#!/bin/bash

# Quick test for a single configuration
# Run from the test directory: ./quick-test.sh

set -e

# Change to parent directory for proper path resolution
cd "$(dirname "$0")/.."

echo "Quick Docker Build Test"
echo "======================="

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "Error: Docker is not running"
    echo "Please start Docker Desktop and try again"
    exit 1
fi

# Default test configuration
IMAGE_TYPE=${1:-"cuda-conda"}
CUDA_VERSION=${2:-"12.4.1"}
UBUNTU_VERSION=${3:-"22.04"}
PYTHON_VERSION=${4:-"3.11"}

TAG="${IMAGE_TYPE}-test:cuda${CUDA_VERSION}-ubuntu${UBUNTU_VERSION}-python${PYTHON_VERSION}"

echo "Building: $TAG"
echo "This may take a few minutes..."

# Build the image
if docker build \
    --build-arg CUDA_VERSION=${CUDA_VERSION} \
    --build-arg UBUNTU_VERSION=${UBUNTU_VERSION} \
    --build-arg PYTHON_VERSION=${PYTHON_VERSION} \
    -t ${TAG} \
    -f ${IMAGE_TYPE}/Dockerfile \
    ${IMAGE_TYPE}/; then
    echo "✓ Build successful!"
    
    # Show image info
    echo ""
    echo "Image info:"
    docker images ${TAG}
    
    # Test run
    echo ""
    echo "Testing jupyter version..."
    docker run --rm ${TAG} jupyter --version
    
    echo ""
    echo "Success! You can now run:"
    echo "docker run -p 8888:8888 --rm ${TAG}"
else
    echo "✗ Build failed"
    exit 1
fi