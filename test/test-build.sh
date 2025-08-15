#!/bin/bash

# Test build script for ml-docker images
# Run from the test directory: ./test-build.sh

set -e

# Change to parent directory for proper path resolution
cd "$(dirname "$0")/.."

echo "================================"
echo "ML Docker Test Build Script"
echo "================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to test build
test_build() {
    local image_type=$1
    local cuda_version=$2
    local ubuntu_version=$3
    local python_version=$4
    local tag="${image_type}-test:cuda${cuda_version}-ubuntu${ubuntu_version}-python${python_version}"
    
    echo -e "\n${YELLOW}Testing build: ${tag}${NC}"
    
    if docker build \
        --build-arg CUDA_VERSION=${cuda_version} \
        --build-arg UBUNTU_VERSION=${ubuntu_version} \
        --build-arg PYTHON_VERSION=${python_version} \
        -t ${tag} \
        -f ${image_type}/Dockerfile \
        ${image_type}/; then
        echo -e "${GREEN}✓ Build successful: ${tag}${NC}"
        
        # Test if the image runs
        echo -e "${YELLOW}Testing image startup...${NC}"
        if docker run --rm ${tag} jupyter --version > /dev/null 2>&1; then
            echo -e "${GREEN}✓ Image runs successfully${NC}"
        else
            echo -e "${RED}✗ Failed to run image${NC}"
        fi
        
        # Clean up test image
        docker rmi ${tag} > /dev/null 2>&1
        return 0
    else
        echo -e "${RED}✗ Build failed: ${tag}${NC}"
        return 1
    fi
}

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo -e "${RED}Error: Docker is not running${NC}"
    echo "Please start Docker Desktop and try again"
    exit 1
fi

# Parse command line arguments
IMAGE_TYPE=${1:-"all"}
CUDA_VERSION=${2:-""}
UBUNTU_VERSION=${3:-""}
PYTHON_VERSION=${4:-""}

# Test configurations
declare -A test_configs=(
    ["minimal"]="12.4.1,22.04,3.11"
    ["cuda11"]="11.8.0,22.04,3.10"
    ["cuda12"]="12.1.1,22.04,3.11"
    ["latest"]="12.4.1,24.04,3.12"
)

# Function to run specific test
run_test() {
    local type=$1
    if [[ -n "$CUDA_VERSION" && -n "$UBUNTU_VERSION" && -n "$PYTHON_VERSION" ]]; then
        test_build $type $CUDA_VERSION $UBUNTU_VERSION $PYTHON_VERSION
    else
        echo -e "${YELLOW}Running predefined test configurations${NC}"
        for config_name in "${!test_configs[@]}"; do
            IFS=',' read -r cuda ubuntu python <<< "${test_configs[$config_name]}"
            echo -e "\n${YELLOW}Configuration: ${config_name}${NC}"
            test_build $type $cuda $ubuntu $python
        done
    fi
}

# Main execution
case $IMAGE_TYPE in
    "cuda-jupyter")
        echo "Testing cuda-jupyter builds..."
        run_test "cuda-jupyter"
        ;;
    "cuda-conda")
        echo "Testing cuda-conda builds..."
        run_test "cuda-conda"
        ;;
    "all")
        echo "Testing all image types..."
        if [[ -d "cuda-jupyter" ]]; then
            echo -e "\n${YELLOW}=== Testing cuda-jupyter ===${NC}"
            run_test "cuda-jupyter"
        fi
        if [[ -d "cuda-conda" ]]; then
            echo -e "\n${YELLOW}=== Testing cuda-conda ===${NC}"
            run_test "cuda-conda"
        fi
        ;;
    *)
        echo "Usage: $0 [image-type] [cuda-version] [ubuntu-version] [python-version]"
        echo ""
        echo "image-type: cuda-jupyter, cuda-conda, or all (default: all)"
        echo ""
        echo "Examples:"
        echo "  $0                                    # Test all images with predefined configs"
        echo "  $0 cuda-conda                         # Test only cuda-conda with predefined configs"
        echo "  $0 cuda-conda 12.4.1 22.04 3.11       # Test specific configuration"
        exit 1
        ;;
esac

echo -e "\n${GREEN}Test build completed!${NC}"