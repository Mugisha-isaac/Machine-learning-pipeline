# Machine Learning Pipeline - API Documentation

**Version:** 1.0.0  
**Base URL:** `http://localhost:8000/api/v1`  
**API Type:** RESTful  
**Authentication:** None (Configure as needed)

---

## Table of Contents

1. [Overview](#overview)
2. [Getting Started](#getting-started)
3. [Response Format](#response-format)
4. [Error Handling](#error-handling)
5. [MongoDB API Endpoints](#mongodb-api-endpoints)
6. [PostgreSQL API Endpoints](#postgresql-api-endpoints)
7. [Training Data Endpoints](#training-data-endpoints)
8. [Health Check](#health-check)
9. [Rate Limiting](#rate-limiting)
10. [Examples](#examples)

---

## Overview

The Machine Learning Pipeline API provides comprehensive healthcare data management capabilities across two specialized databases:

- **MongoDB**: Document-based storage for flexible data structures and ML workflows
- **PostgreSQL**: Relational database for structured healthcare records with strong consistency

All endpoints follow RESTful conventions and return JSON responses.

---

## Getting Started

### Base URL

```
http://localhost:8000/api/v1
```

For production environments, replace with your deployed URL.

### Interactive Documentation

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

### Content Type

All requests and responses use `application/json` content type.

### Common Headers

```http
Content-Type: application/json
Accept: application/json
```

---

## Response Format

### Success Response

```json
{
  "PatientID": 1,
  "Sex": true,
  "Age": 45,
  "Education": 4,
  "Income": 6
}
```

### List Response

```json
[
  {
    "PatientID": 1,
    "Sex": true,
    "Age": 45
  },
  {
    "PatientID": 2,
    "Sex": false,
    "Age": 52
  }
]
```

### Pagination Response

Pagination is supported through query parameters:
- `skip`: Number of records to skip (default: 0)
- `limit`: Maximum number of records to return (default: 100)

---

## Error Handling

### Error Response Format

```json
{
  "detail": "Error message describing what went wrong"
}
```

### HTTP Status Codes

| Status Code | Description |
|-------------|-------------|
| 200 | OK - Request successful |
| 201 | Created - Resource created successfully |
| 400 | Bad Request - Invalid input data |
| 404 | Not Found - Resource not found |
| 422 | Unprocessable Entity - Validation error |
| 500 | Internal Server Error - Server error |

---

## MongoDB API Endpoints

### Patients

#### Get All Patients

```http
GET /api/v1/mongodb/patients/
```

**Query Parameters:**
- `skip` (integer, optional): Records to skip (default: 0)
- `limit` (integer, optional): Maximum records (default: 100)

**Response:**
```json
[
  {
    "_id": "507f1f77bcf86cd799439011",
    "PatientID": 1,
    "Sex": true,
    "Age": 45,
    "Education": 4,
    "Income": 6,
    "created_at": "2025-11-01T10:00:00Z",
    "updated_at": "2025-11-01T10:00:00Z"
  }
]
```

#### Get Latest Patients

```http
GET /api/v1/mongodb/patients/latest
```

**Query Parameters:**
- `limit` (integer, optional): Maximum records (default: 10)

#### Get Patient by ID

```http
GET /api/v1/mongodb/patients/{id}
```

**Path Parameters:**
- `id` (string, required): MongoDB ObjectId

**Response:**
```json
{
  "_id": "507f1f77bcf86cd799439011",
  "PatientID": 1,
  "Sex": true,
  "Age": 45,
  "Education": 4,
  "Income": 6
}
```

#### Create Patient

```http
POST /api/v1/mongodb/patients/
```

**Request Body:**
```json
{
  "PatientID": 1,
  "Sex": true,
  "Age": 45,
  "Education": 4,
  "Income": 6
}
```

**Response:** 201 Created
```json
{
  "_id": "507f1f77bcf86cd799439011",
  "PatientID": 1,
  "Sex": true,
  "Age": 45,
  "Education": 4,
  "Income": 6,
  "created_at": "2025-11-01T10:00:00Z",
  "updated_at": "2025-11-01T10:00:00Z"
}
```

#### Update Patient

```http
PUT /api/v1/mongodb/patients/{id}
```

**Path Parameters:**
- `id` (string, required): MongoDB ObjectId

**Request Body:**
```json
{
  "Age": 46,
  "Income": 7
}
```

#### Delete Patient

```http
DELETE /api/v1/mongodb/patients/{id}
```

**Response:**
```json
{
  "message": "Patient deleted successfully"
}
```

---

### Health Conditions

#### Get All Health Conditions

```http
GET /api/v1/mongodb/health-conditions/
```

**Query Parameters:**
- `skip` (integer, optional): Records to skip
- `limit` (integer, optional): Maximum records

#### Get Latest Health Conditions

```http
GET /api/v1/mongodb/health-conditions/latest
```

**Query Parameters:**
- `limit` (integer, optional): Maximum records (default: 10)

#### Get Health Conditions by Patient

```http
GET /api/v1/mongodb/health-conditions/patient/{patient_id}
```

**Path Parameters:**
- `patient_id` (integer, required): Patient ID

#### Get Health Condition by ID

```http
GET /api/v1/mongodb/health-conditions/{id}
```

#### Create Health Condition

```http
POST /api/v1/mongodb/health-conditions/
```

**Request Body:**
```json
{
  "PatientID": 1,
  "Diabetes_012": true,
  "HighBP": true,
  "HighChol": false,
  "Stroke": false,
  "HeartDiseaseorAttack": false,
  "DiffWalk": false
}
```

#### Update Health Condition

```http
PUT /api/v1/mongodb/health-conditions/{id}
```

#### Delete Health Condition

```http
DELETE /api/v1/mongodb/health-conditions/{id}
```

---

### Lifestyle Factors

#### Get All Lifestyle Factors

```http
GET /api/v1/mongodb/lifestyle-factors/
```

#### Get Latest Lifestyle Factors

```http
GET /api/v1/mongodb/lifestyle-factors/latest
```

#### Get Lifestyle Factors by Patient

```http
GET /api/v1/mongodb/lifestyle-factors/patient/{patient_id}
```

#### Get Lifestyle Factor by ID

```http
GET /api/v1/mongodb/lifestyle-factors/{id}
```

#### Create Lifestyle Factor

```http
POST /api/v1/mongodb/lifestyle-factors/
```

**Request Body:**
```json
{
  "PatientID": 1,
  "BMI": 28.5,
  "Smoker": false,
  "PhysActivity": true,
  "Fruits": true,
  "Veggies": true,
  "HvyAlcoholConsump": false
}
```

#### Update Lifestyle Factor

```http
PUT /api/v1/mongodb/lifestyle-factors/{id}
```

#### Delete Lifestyle Factor

```http
DELETE /api/v1/mongodb/lifestyle-factors/{id}
```

---

### Health Metrics

#### Get All Health Metrics
  
```http
GET /api/v1/mongodb/health-metrics/
```

#### Get Latest Health Metrics

```http
GET /api/v1/mongodb/health-metrics/latest
```

#### Get Health Metrics by Patient

```http
GET /api/v1/mongodb/health-metrics/patient/{patient_id}
```

#### Get Health Metric by ID

```http
GET /api/v1/mongodb/health-metrics/{id}
```

#### Create Health Metric

```http
POST /api/v1/mongodb/health-metrics/
```

**Request Body:**
```json
{
  "PatientID": 1,
  "CholCheck": true,
  "GenHlth": 3,
  "MentHlth": 5,
  "PhysHlth": 2
}
```

#### Update Health Metric

```http
PUT /api/v1/mongodb/health-metrics/{id}
```

#### Delete Health Metric

```http
DELETE /api/v1/mongodb/health-metrics/{id}
```

---

### Healthcare Access

#### Get All Healthcare Access Records

```http
GET /api/v1/mongodb/healthcare-access/
```

#### Get Latest Healthcare Access Records

```http
GET /api/v1/mongodb/healthcare-access/latest
```

#### Get Healthcare Access by Patient

```http
GET /api/v1/mongodb/healthcare-access/patient/{patient_id}
```

#### Get Healthcare Access by ID

```http
GET /api/v1/mongodb/healthcare-access/{id}
```

#### Create Healthcare Access Record

```http
POST /api/v1/mongodb/healthcare-access/
```

**Request Body:**
```json
{
  "PatientID": 1,
  "AnyHealthcare": true,
  "NoDocbcCost": false
}
```

#### Update Healthcare Access Record

```http
PUT /api/v1/mongodb/healthcare-access/{id}
```

#### Delete Healthcare Access Record

```http
DELETE /api/v1/mongodb/healthcare-access/{id}
```

---

## PostgreSQL API Endpoints

### Patients

#### Get All Patients

```http
GET /api/v1/postgres/patients/
```

**Query Parameters:**
- `skip` (integer, optional): Records to skip (default: 0)
- `limit` (integer, optional): Maximum records (default: 100)

**Response:**
```json
[
  {
    "PatientID": 1,
    "Sex": true,
    "Age": 45,
    "Education": 4,
    "Income": 6
  }
]
```

#### Get Latest Patients

```http
GET /api/v1/postgres/patients/latest
```

**Query Parameters:**
- `limit` (integer, optional): Maximum records (default: 10)

#### Get Patient by ID

```http
GET /api/v1/postgres/patients/{patient_id}
```

**Path Parameters:**
- `patient_id` (integer, required): Patient ID

#### Create Patient

```http
POST /api/v1/postgres/patients/
```

**Request Body:**
```json
{
  "Sex": true,
  "Age": 45,
  "Education": 4,
  "Income": 6
}
```

**Response:** 201 Created
```json
{
  "PatientID": 1,
  "Sex": true,
  "Age": 45,
  "Education": 4,
  "Income": 6
}
```

#### Update Patient

```http
PUT /api/v1/postgres/patients/{patient_id}
```

**Request Body:**
```json
{
  "Age": 46,
  "Income": 7
}
```

#### Delete Patient

```http
DELETE /api/v1/postgres/patients/{patient_id}
```

**Response:**
```json
{
  "message": "Patient deleted successfully"
}
```

---

### Health Conditions (PostgreSQL)

All endpoints follow the same pattern as MongoDB but use integer IDs instead of ObjectIds.

#### Get All Health Conditions

```http
GET /api/v1/postgres/health-conditions/
```

#### Get Latest Health Conditions

```http
GET /api/v1/postgres/health-conditions/latest
```

#### Get Health Conditions by Patient

```http
GET /api/v1/postgres/health-conditions/patient/{patient_id}
```

#### Get Health Condition by ID

```http
GET /api/v1/postgres/health-conditions/{condition_id}
```

#### Create Health Condition

```http
POST /api/v1/postgres/health-conditions/
```

**Request Body:**
```json
{
  "PatientID": 1,
  "Diabetes_012": true,
  "HighBP": true,
  "HighChol": false,
  "Stroke": false,
  "HeartDiseaseorAttack": false,
  "DiffWalk": false
}
```

#### Update Health Condition

```http
PUT /api/v1/postgres/health-conditions/{condition_id}
```

#### Delete Health Condition

```http
DELETE /api/v1/postgres/health-conditions/{condition_id}
```

---

### Lifestyle Factors (PostgreSQL)

#### Get All Lifestyle Factors

```http
GET /api/v1/postgres/lifestyle-factors/
```

#### Get Latest Lifestyle Factors

```http
GET /api/v1/postgres/lifestyle-factors/latest
```

#### Get Lifestyle Factors by Patient

```http
GET /api/v1/postgres/lifestyle-factors/patient/{patient_id}
```

#### Get Lifestyle Factor by ID

```http
GET /api/v1/postgres/lifestyle-factors/{lifestyle_id}
```

#### Create Lifestyle Factor

```http
POST /api/v1/postgres/lifestyle-factors/
```

**Request Body:**
```json
{
  "PatientID": 1,
  "BMI": 28.5,
  "Smoker": false,
  "PhysActivity": true,
  "Fruits": true,
  "Veggies": true,
  "HvyAlcoholConsump": false
}
```

#### Update Lifestyle Factor

```http
PUT /api/v1/postgres/lifestyle-factors/{lifestyle_id}
```

#### Delete Lifestyle Factor

```http
DELETE /api/v1/postgres/lifestyle-factors/{lifestyle_id}
```

---

### Health Metrics (PostgreSQL)

#### Get All Health Metrics

```http
GET /api/v1/postgres/health-metrics/
```

#### Get Latest Health Metrics

```http
GET /api/v1/postgres/health-metrics/latest
```

#### Get Health Metrics by Patient

```http
GET /api/v1/postgres/health-metrics/patient/{patient_id}
```

#### Get Health Metric by ID

```http
GET /api/v1/postgres/health-metrics/{metric_id}
```

#### Create Health Metric

```http
POST /api/v1/postgres/health-metrics/
```

**Request Body:**
```json
{
  "PatientID": 1,
  "CholCheck": true,
  "GenHlth": 3,
  "MentHlth": 5,
  "PhysHlth": 2
}
```

#### Update Health Metric

```http
PUT /api/v1/postgres/health-metrics/{metric_id}
```

#### Delete Health Metric

```http
DELETE /api/v1/postgres/health-metrics/{metric_id}
```

---

### Healthcare Access (PostgreSQL)

#### Get All Healthcare Access Records

```http
GET /api/v1/postgres/healthcare-access/
```

#### Get Latest Healthcare Access Records

```http
GET /api/v1/postgres/healthcare-access/latest
```

#### Get Healthcare Access by Patient

```http
GET /api/v1/postgres/healthcare-access/patient/{patient_id}
```

#### Get Healthcare Access by ID

```http
GET /api/v1/postgres/healthcare-access/{access_id}
```

#### Create Healthcare Access Record

```http
POST /api/v1/postgres/healthcare-access/
```

**Request Body:**
```json
{
  "PatientID": 1,
  "AnyHealthcare": true,
  "NoDocbcCost": false
}
```

#### Update Healthcare Access Record

```http
PUT /api/v1/postgres/healthcare-access/{access_id}
```

#### Delete Healthcare Access Record

```http
DELETE /api/v1/postgres/healthcare-access/{access_id}
```

---

## Training Data Endpoints

### MongoDB Training Data

#### Get All Latest Records

```http
GET /api/v1/mongodb/all/latest
```

Retrieves the most recent records from all collections.

**Query Parameters:**
- `limit` (integer, optional): Records per collection (default: 10)

**Response:**
```json
{
  "patients": [...],
  "health_conditions": [...],
  "lifestyle_factors": [...],
  "health_metrics": [...],
  "healthcare_access": [...]
}
```

#### Get Latest Training Data

```http
GET /api/v1/mongodb/training-data/latest
```

Retrieves aggregated training data with joined information.

**Query Parameters:**
- `limit` (integer, optional): Maximum records (default: 100)

**Response:**
```json
{
  "total": 100,
  "limit": 100,
  "records": [
    {
      "PatientID": 1,
      "Sex": true,
      "Age": 45,
      "Diabetes_012": true,
      "BMI": 28.5,
      "HighBP": true,
      ...
    }
  ]
}
```

#### Get Complete Training Data

```http
GET /api/v1/mongodb/training-data/complete
```

Retrieves only complete records (no null values).

**Query Parameters:**
- `skip` (integer, optional): Records to skip (default: 0)
- `limit` (integer, optional): Maximum records (default: 1000)

---

### PostgreSQL Training Data

#### Get Latest Training Data

```http
GET /api/v1/postgres/training-data/latest
```

**Query Parameters:**
- `limit` (integer, optional): Maximum records (default: 100)

**Response:**
```json
{
  "total": 100,
  "limit": 100,
  "records": [
    {
      "PatientID": 1,
      "Sex": true,
      "Age": 45,
      "Education": 4,
      "Income": 6,
      "Diabetes_012": true,
      "HighBP": true,
      "BMI": 28.5,
      ...
    }
  ]
}
```

#### Get Complete Training Data

```http
GET /api/v1/postgres/training-data/complete
```

Returns only patients with complete data across all tables using SQL joins.

**Query Parameters:**
- `skip` (integer, optional): Records to skip (default: 0)
- `limit` (integer, optional): Maximum records (default: 1000)

**Response:**
```json
{
  "total": 5000,
  "skip": 0,
  "limit": 1000,
  "returned": 1000,
  "records": [...]
}
```

---

## Health Check

### Check API Health

```http
GET /api/v1/health
```

**Response:**
```json
{
  "status": "healthy",
  "databases": ["postgresql", "mongodb"]
}
```

### Root Endpoint

```http
GET /
```

**Response:**
```json
{
  "message": "Machine Learning Pipeline API",
  "version": "1.0.0",
  "docs": "/docs"
}
```

---

## Rate Limiting

Currently, no rate limiting is implemented. For production use, consider implementing:

- Rate limiting per IP address
- Authentication-based rate limits
- Different limits for different endpoint categories

---

## Examples

### Example 1: Create a Complete Patient Record

**Step 1:** Create Patient
```bash
curl -X POST "http://localhost:8000/api/v1/postgres/patients/" \
  -H "Content-Type: application/json" \
  -d '{
    "Sex": true,
    "Age": 45,
    "Education": 4,
    "Income": 6
  }'
```

**Step 2:** Create Health Condition
```bash
curl -X POST "http://localhost:8000/api/v1/postgres/health-conditions/" \
  -H "Content-Type: application/json" \
  -d '{
    "PatientID": 1,
    "Diabetes_012": true,
    "HighBP": true,
    "HighChol": false,
    "Stroke": false,
    "HeartDiseaseorAttack": false,
    "DiffWalk": false
  }'
```

**Step 3:** Create Lifestyle Factor
```bash
curl -X POST "http://localhost:8000/api/v1/postgres/lifestyle-factors/" \
  -H "Content-Type: application/json" \
  -d '{
    "PatientID": 1,
    "BMI": 28.5,
    "Smoker": false,
    "PhysActivity": true,
    "Fruits": true,
    "Veggies": true,
    "HvyAlcoholConsump": false
  }'
```

### Example 2: Get Training Data

```bash
curl -X GET "http://localhost:8000/api/v1/postgres/training-data/complete?limit=100"
```

### Example 3: Update Patient Information

```bash
curl -X PUT "http://localhost:8000/api/v1/postgres/patients/1" \
  -H "Content-Type: application/json" \
  -d '{
    "Age": 46,
    "Income": 7
  }'
```

### Example 4: Search by Patient ID

```bash
# Get all health data for a specific patient
curl -X GET "http://localhost:8000/api/v1/postgres/health-conditions/patient/1"
curl -X GET "http://localhost:8000/api/v1/postgres/lifestyle-factors/patient/1"
curl -X GET "http://localhost:8000/api/v1/postgres/health-metrics/patient/1"
curl -X GET "http://localhost:8000/api/v1/postgres/healthcare-access/patient/1"
```

---

## Data Models

### Patient

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| PatientID | integer | Auto | Unique identifier (auto-generated in PostgreSQL) |
| Sex | boolean | Optional | Patient gender (true/false) |
| Age | integer | Optional | Patient age |
| Education | integer | Optional | Education level (1-6) |
| Income | integer | Optional | Income level (1-8) |

### Health Condition

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| ConditionID | integer | Auto | Unique identifier (PostgreSQL only) |
| PatientID | integer | Required | Reference to patient |
| Diabetes_012 | boolean | Optional | Diabetes status |
| HighBP | boolean | Optional | High blood pressure |
| HighChol | boolean | Optional | High cholesterol |
| Stroke | boolean | Optional | Stroke history |
| HeartDiseaseorAttack | boolean | Optional | Heart disease/attack history |
| DiffWalk | boolean | Optional | Difficulty walking |

### Lifestyle Factor

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| LifestyleID | integer | Auto | Unique identifier (PostgreSQL only) |
| PatientID | integer | Required | Reference to patient |
| BMI | float | Optional | Body Mass Index |
| Smoker | boolean | Optional | Smoking status |
| PhysActivity | boolean | Optional | Physical activity |
| Fruits | boolean | Optional | Fruit consumption |
| Veggies | boolean | Optional | Vegetable consumption |
| HvyAlcoholConsump | boolean | Optional | Heavy alcohol consumption |

### Health Metric

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| MetricsID | integer | Auto | Unique identifier (PostgreSQL only) |
| PatientID | integer | Required | Reference to patient |
| CholCheck | boolean | Optional | Cholesterol check |
| GenHlth | integer | Optional | General health (1-5) |
| MentHlth | integer | Optional | Mental health days (0-30) |
| PhysHlth | integer | Optional | Physical health days (0-30) |

### Healthcare Access

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| AccessID | integer | Auto | Unique identifier (PostgreSQL only) |
| PatientID | integer | Required | Reference to patient |
| AnyHealthcare | boolean | Optional | Has any healthcare coverage |
| NoDocbcCost | boolean | Optional | Could not see doctor due to cost |

---

## Best Practices

1. **Always validate input data** before sending requests
2. **Use pagination** for large datasets to avoid timeouts
3. **Handle errors gracefully** with appropriate error messages
4. **Use the training data endpoints** for ML model training instead of manual joins
5. **Monitor the health endpoint** for system status
6. **Refer to Swagger UI** for real-time API testing and exploration

---

## Support

For questions or issues with this API:

- Check the interactive documentation at `/docs`
- Review error messages for detailed information
- Contact the development team

---

**Last Updated:** November 2, 2025  
**API Version:** 1.0.0
