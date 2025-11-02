# Test Suite Documentation

Comprehensive test suite for the Machine Learning Pipeline API, covering PostgreSQL and MongoDB endpoints.

## Test Structure

```
tests/
├── __init__.py                    # Test suite initialization
├── conftest.py                    # Pytest fixtures and configuration
├── test_postgres_endpoints.py     # PostgreSQL endpoint tests
├── test_mongodb_endpoints.py      # MongoDB endpoint tests
├── test_integration.py            # Integration tests
└── test_utils.py                  # Test utility functions
```

## Test Coverage

### PostgreSQL Endpoints (`test_postgres_endpoints.py`)
- **Patient Endpoints**: Create, Update, Delete
- **Health Condition Endpoints**: Create, Update, Delete
- **Lifestyle Factor Endpoints**: Create, Update, Delete
- **Health Metric Endpoints**: Create, Update, Delete
- **Healthcare Access Endpoints**: Create, Update, Delete
- **Validation Tests**: Invalid data handling, foreign key constraints

### MongoDB Endpoints (`test_mongodb_endpoints.py`)
- **Patient Endpoints**: Create, Update, Delete
- **Health Condition Endpoints**: Create, Update, Delete
- **Lifestyle Factor Endpoints**: Create, Update, Delete
- **Health Metric Endpoints**: Create, Update, Delete
- **Healthcare Access Endpoints**: Create, Update, Delete
- **Validation Tests**: Invalid ObjectId, data validation, timestamps

### Integration Tests (`test_integration.py`)
- **Complete Workflows**: End-to-end patient data management
- **Cascade Deletes**: Foreign key constraint verification
- **Cross-Database**: Data consistency across PostgreSQL and MongoDB
- **Multiple Records**: Independent record management

## Running Tests

### Prerequisites

```bash
# Install test dependencies
pip install pytest pytest-asyncio httpx
```

### Run All Tests

```bash
# Using pytest directly
pytest tests/ -v

# Using the test runner script
./run_tests.sh
```

### Run Specific Test Files

```bash
# PostgreSQL tests only
pytest tests/test_postgres_endpoints.py -v

# MongoDB tests only
pytest tests/test_mongodb_endpoints.py -v

# Integration tests only
pytest tests/test_integration.py -v
```

### Run Specific Test Classes

```bash
# Test only Patient endpoints
pytest tests/test_postgres_endpoints.py::TestPostgresPatientEndpoints -v

# Test only Health Condition endpoints
pytest tests/test_mongodb_endpoints.py::TestMongoDBHealthConditionEndpoints -v
```

### Run Specific Test Methods

```bash
# Test a single test method
pytest tests/test_postgres_endpoints.py::TestPostgresPatientEndpoints::test_create_patient -v
```

### Run with Coverage

```bash
# Install coverage
pip install pytest-cov

# Run tests with coverage report
pytest tests/ --cov=app --cov-report=html

# View coverage report
open htmlcov/index.html
```

## Test Fixtures

### Database Fixtures
- `test_db`: Creates a fresh SQLite test database for PostgreSQL tests
- `test_mongo_db`: Creates a test MongoDB database

### Client Fixture
- `client`: FastAPI TestClient for making HTTP requests

### Data Fixtures
- `sample_patient_data`: Sample patient data for testing
- `sample_health_condition_data`: Sample health condition data
- `sample_lifestyle_factor_data`: Sample lifestyle factor data
- `sample_health_metric_data`: Sample health metric data
- `sample_healthcare_access_data`: Sample healthcare access data

## Test Utilities

The `test_utils.py` file provides helper functions:

```python
from tests.test_utils import (
    generate_patient_data,
    generate_health_condition_data,
    assert_patient_response,
    assert_timestamps_exist
)

# Generate random test data
patient = generate_patient_data(override={"Age": 50})

# Assert response correctness
assert_patient_response(response.json(), expected_data)

# Assert MongoDB timestamps
assert_timestamps_exist(response.json())
```

## Writing New Tests

### Example Test Structure

```python
class TestNewEndpoint:
    """Test cases for new endpoint."""
    
    def test_create(self, client, test_db):
        """Test creating a new record."""
        data = {"field": "value"}
        response = client.post("/api/v1/endpoint/", json=data)
        
        assert response.status_code == 201
        assert response.json()["field"] == "value"
    
    def test_update(self, client, test_db):
        """Test updating a record."""
        # Create first
        create_response = client.post("/api/v1/endpoint/", json={"field": "value"})
        record_id = create_response.json()["id"]
        
        # Then update
        update_response = client.put(f"/api/v1/endpoint/{record_id}", json={"field": "new_value"})
        
        assert update_response.status_code == 200
        assert update_response.json()["field"] == "new_value"
    
    def test_delete(self, client, test_db):
        """Test deleting a record."""
        # Create first
        create_response = client.post("/api/v1/endpoint/", json={"field": "value"})
        record_id = create_response.json()["id"]
        
        # Then delete
        delete_response = client.delete(f"/api/v1/endpoint/{record_id}")
        
        assert delete_response.status_code == 200
```

## Continuous Integration

To integrate with CI/CD pipelines:

```yaml
# Example GitHub Actions workflow
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.10'
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
    - name: Run tests
      run: |
        pytest tests/ -v --tb=short
```

## Troubleshooting

### Common Issues

**ImportError**: Ensure the app is importable
```bash
export PYTHONPATH="${PYTHONPATH}:/path/to/project"
```

**Database Connection Errors**: Check `.env` file configuration
```bash
# Ensure test databases are configured
TEST_POSTGRES_URL=sqlite:///./test.db
TEST_MONGO_DB=test_healthcare_ml
```

**Fixture Not Found**: Check `conftest.py` is in the tests directory

**Tests Hang**: Ensure background processes are not blocking
```bash
# Kill any running uvicorn instances
pkill -f uvicorn
```

## Best Practices

1. **Isolation**: Each test should be independent and not rely on other tests
2. **Cleanup**: Always clean up created resources (fixtures handle this automatically)
3. **Descriptive Names**: Use clear, descriptive test method names
4. **Assertions**: Test one thing per test method when possible
5. **Documentation**: Add docstrings explaining what each test verifies
6. **Data Generation**: Use fixtures and utility functions for test data

## Test Metrics

Current test coverage:
- **Total Tests**: 50+ test cases
- **Endpoints Covered**: All POST, PUT, DELETE endpoints
- **Database Coverage**: Both PostgreSQL and MongoDB
- **Integration Tests**: Complete workflows and cross-database operations
