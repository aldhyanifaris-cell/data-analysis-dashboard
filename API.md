# REST API Documentation (v1)

Base URL: `http://127.0.0.1:8000/api/v1/`

### 1. Authentication Endpoints
- `POST /api/v1/auth/token/` - Obtain JWT access & refresh tokens.
- `POST /api/v1/auth/token/refresh/` - Refresh expired access token.
- `POST /api/v1/auth/register/` - Register a new user account.
- `GET/PATCH /api/v1/auth/profile/` - View/update user profile.

### 2. Dataset Endpoints
- `GET /api/v1/datasets/` - List all available datasets (paginated, searchable, filterable).
- `POST /api/v1/datasets/` - Upload new dataset file (multipart/form-data).
- `GET /api/v1/datasets/{id}/` - Retrieve full dataset details with columns metadata.
- `GET /api/v1/datasets/{id}/preview/` - Retrieve sample rows (JSON).
- `GET /api/v1/datasets/{id}/columns/` - List statistical properties of columns.
- `POST /api/v1/datasets/{id}/toggle_favorite/` - Toggle favorite flag.

### 3. Analysis Endpoints
- `GET /api/v1/analysis/` - List analyses.
- `POST /api/v1/analysis/` - Trigger statistical/ML analysis.
- `GET /api/v1/analysis/{id}/` - Retrieve analysis details and execution status.
- `GET /api/v1/analysis/{id}/statistics/` - Detailed metrics JSON.
- `GET /api/v1/analysis/{id}/insights/` - AI-generated domain insights.
- `GET /api/v1/analysis/{id}/recommendations/` - Actionable next steps.

### 4. Visualization Endpoints
- `GET /api/v1/visualizations/` - List charts.
- `POST /api/v1/visualizations/` - Create dynamic Plotly or static chart.
- `GET /api/v1/visualizations/{id}/` - Retrieve Plotly JSON figure specification.
- `GET /api/v1/visualizations/{id}/export/?format=png` - Download high-res PNG/SVG/PDF chart.

### 5. System Endpoints
- `GET /api/v1/` - API Root and endpoint map.
- `GET /api/v1/system-stats/` - Aggregated dataset, analysis, and visualization statistics.
- `GET /api/v1/health/` - Service health status.
