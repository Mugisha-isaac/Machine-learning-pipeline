# Machine Learning Pipeline API

A comprehensive healthcare data management system with dual-database architecture, built with FastAPI for high-performance API operations.

## Overview

This project provides a robust RESTful API for managing healthcare data across two specialized databases:
- **PostgreSQL** for structured, relational healthcare records
- **MongoDB** for flexible, document-based ML training data and analytics

The API enables seamless CRUD operations, data aggregation, and machine learning model training data preparation.

## Key Features

### Dual Database Architecture
- **PostgreSQL**: Optimized for structured healthcare data with strict schema validation
- **MongoDB**: Flexible document storage for ML workflows and training datasets
- Seamless integration between both databases
- Independent scaling and optimization strategies

### Comprehensive API Endpoints
- Patient demographic management
- Health conditions tracking
- Lifestyle factors monitoring
- Health metrics recording
- Healthcare access information
- ML training data aggregation

### Modern Technology Stack
- **FastAPI**: High-performance async API framework
- **SQLAlchemy**: Powerful ORM for PostgreSQL operations
- **Pydantic**: Data validation and serialization
- **PyMongo**: MongoDB driver for document operations
- **Uvicorn**: Lightning-fast ASGI server

### Developer-Friendly Features
- Auto-generated OpenAPI documentation (Swagger UI)
- Modular controller architecture
- Type hints and data validation
- CORS support for frontend integration
- Health check endpoints
- Comprehensive error handling

## Prerequisites

- Python 3.8 or higher
- PostgreSQL database (cloud or local)
- MongoDB database (cloud or local)
- pip package manager

## Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/Mugisha-isaac/Machine-learning-pipeline.git
cd Machine-learning-pipeline
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Environment Configuration

Create a `.env` file in the root directory with your database credentials:

```env
# PostgreSQL Configuration
POSTGRES_URL=your_postgresql_connection_string

# MongoDB Configuration
MONGO_URI=your_mongodb_connection_string
MONGO_DB=your_database_name

# API Configuration
API_V1_PREFIX=/api/v1
PROJECT_NAME=Machine Learning Pipeline
```

**Note**: Never commit your `.env` file to version control. Use `.env.example` as a template.

### 4. Database Schema Setup

Initialize the PostgreSQL database using the provided schema:

```bash
psql your_postgres_url -f dbdesign.sql
```

### 5. Start the Application

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## Project Structure

```
Machine-learning-pipeline/
├── app/
│   ├── api/
│   │   ├── mongodb/          # MongoDB API controllers
│   │   │   ├── patients.py
│   │   │   ├── health_conditions.py
│   │   │   ├── lifestyle_factors.py
│   │   │   ├── health_metrics.py
│   │   │   ├── healthcare_access.py
│   │   │   ├── training_data.py
│   │   │   └── routes.py     # MongoDB router aggregator
│   │   └── postgres/         # PostgreSQL API controllers
│   │       ├── patients.py
│   │       ├── health_conditions.py
│   │       ├── lifestyle_factors.py
│   │       ├── health_metrics.py
│   │       ├── healthcare_access.py
│   │       ├── training_data.py
│   │       ├── schemas.py    # Pydantic models
│   │       └── routes.py     # PostgreSQL router aggregator
│   ├── core/
│   │   ├── config.py         # Application settings
│   │   ├── database.py       # Database connections
│   │   ├── models.py         # SQLAlchemy models
│   │   └── mongo_models.py   # MongoDB Pydantic schemas
│   └── main.py               # FastAPI application entry point
├── dbdesign.sql              # PostgreSQL schema definition
├── requirements.txt          # Python dependencies
└── README.md
```

## Database Schema

### PostgreSQL Tables

| Table | Description | Key Fields |
|-------|-------------|------------|
| **Patients** | Patient demographics | PatientID, Sex, Age, Education, Income |
| **Health_Conditions** | Medical conditions | Diabetes, HighBP, HighChol, Stroke, HeartDiseaseorAttack |
| **Lifestyle_Factors** | Lifestyle data | BMI, Smoker, PhysActivity, Fruits, Veggies |
| **Health_Metrics** | Health screenings | CholCheck, GenHlth, MentHlth, PhysHlth |
| **Healthcare_Access** | Access information | AnyHealthcare, NoDocbcCost |

### MongoDB Collections

| Collection | Description | Purpose |
|------------|-------------|---------|
| **patients** | Patient documents | Flexible patient data storage |
| **health_conditions** | Condition records | Health condition tracking |
| **lifestyle_factors** | Lifestyle documents | Lifestyle data management |
| **health_metrics** | Metrics records | Health metrics storage |
| **healthcare_access** | Access documents | Healthcare access tracking |
| **training_data** | Aggregated data | ML model training datasets |

## API Documentation

Once the application is running, comprehensive interactive API documentation is available:

- **Swagger UI**: Navigate to `http://localhost:8000/docs` for interactive API testing
- **ReDoc**: Navigate to `http://localhost:8000/redoc` for detailed API documentation

Both interfaces provide:
- Complete endpoint listings organized by category
- Request/response schemas
- Try-it-out functionality
- Authentication details
- Example payloads

## Testing

### Health Check
Verify the application and database connections:

```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "databases": ["postgresql", "mongodb"]
}
```

### Endpoint Testing
Use the Swagger UI at `/docs` for interactive testing of all endpoints.

## Development

### Code Organization
- **Modular Controllers**: Separate files for each resource type
- **Consistent Patterns**: Similar structure across MongoDB and PostgreSQL
- **Type Safety**: Full type hints and Pydantic validation
- **Error Handling**: Comprehensive exception handling

### Adding New Endpoints

1. Create controller file in appropriate directory (`mongodb/` or `postgres/`)
2. Define router with appropriate tags
3. Implement endpoint functions with proper schemas
4. Add router to main `routes.py` aggregator
5. Update tags metadata in `main.py`

## Security Considerations

- Store sensitive credentials in `.env` file (never commit)
- Use environment-specific configuration
- Implement proper authentication (recommended: JWT)
- Enable HTTPS in production
- Validate and sanitize all inputs
- Use parameterized queries (SQLAlchemy ORM)
- Implement rate limiting for production

## Deployment

### Production Checklist

- [ ] Set `--reload` flag to `False`
- [ ] Use production-grade ASGI server (Gunicorn + Uvicorn workers)
- [ ] Configure proper logging
- [ ] Set up monitoring and alerting
- [ ] Enable HTTPS/SSL
- [ ] Configure CORS appropriately
- [ ] Use database connection pooling
- [ ] Implement caching strategy
- [ ] Set up automated backups

### Docker Deployment (Optional)

Consider containerizing the application for consistent deployments across environments.

## Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch
3. Make your changes with clear commit messages
4. Write/update tests as needed
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Authors

- **Yassin Hagenimana**
- **Mugisha Isaac**
- **Mitali Desnis**
- **Tuyishime Jean Damour**

## Acknowledgments

- FastAPI for the excellent framework
- SQLAlchemy for robust ORM capabilities
- MongoDB team for flexible document storage
- The open-source community

## Support

For issues, questions, or contributions:

- Open an issue on GitHub
- Check existing documentation
- Review the API docs at `/docs`

---

**Note**: This is a healthcare data management system. Always ensure compliance with relevant healthcare data regulations (HIPAA, GDPR, etc.) when deploying to production.

