#!/bin/bash
# Test runner script for Machine Learning Pipeline API

echo "==========================================="
echo "Running Machine Learning Pipeline API Tests"
echo "==========================================="
echo ""

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
    echo "✓ Virtual environment activated"
else
    echo "⚠ Virtual environment not found. Using system Python."
fi

# Check if pytest is installed
if ! command -v pytest &> /dev/null; then
    echo "✗ pytest not found. Installing test dependencies..."
    pip install pytest pytest-asyncio httpx
fi

echo ""
echo "Installing/Updating test dependencies..."
pip install -q pytest pytest-asyncio httpx

echo ""
echo "==========================================="
echo "Running All Tests"
echo "==========================================="
pytest tests/ -v

echo ""
echo "==========================================="
echo "Test Coverage Summary"
echo "==========================================="
pytest tests/ --tb=line -q

echo ""
echo "==========================================="
echo "Running PostgreSQL Tests Only"
echo "==========================================="
pytest tests/test_postgres_endpoints.py -v

echo ""
echo "==========================================="
echo "Running MongoDB Tests Only"
echo "==========================================="
pytest tests/test_mongodb_endpoints.py -v

echo ""
echo "==========================================="
echo "Running Integration Tests"
echo "==========================================="
pytest tests/test_integration.py -v

echo ""
echo "==========================================="
echo "Test Run Complete!"
echo "==========================================="
