# DataPulse - Enterprise Data Analysis & Visualization Dashboard

A full-stack, enterprise-grade Data Analysis & Visualization Dashboard built with **Django 6.1**, **Django REST Framework (DRF)**, **Pandas**, **SciPy**, **Scikit-Learn**, **Plotly**, and **Seaborn**.

---

## 🌟 Key Features

- 📁 **Multi-Format Dataset Management**: Upload and parse CSV, Excel (.xlsx, .xls), JSON, and Parquet files.
- 🔍 **Automated Data Profiling**: Extracts column types, missing values, duplicates, skewness, kurtosis, and summary stats.
- 📐 **Statistical Analysis Engine**:
  - Full descriptive statistics (mean, median, variance, IQR, quantiles).
  - Pearson & Spearman correlation matrices with heatmap rankings.
  - Outlier detection via **IQR (Interquartile Range)** and **Z-Score** algorithms.
  - **Machine Learning**: K-Means clustering with cluster profiling, Principal Component Analysis (PCA), and Linear Regression.
  - Automated AI-driven domain insights and smart data cleaning recommendations.
- 📊 **Dynamic Visualizations**:
  - Interactive **Plotly** charts (Line, Bar, Scatter, 3D Scatter, Histogram, Box, Violin, Pie, Treemap, Bubble, Heatmap).
  - High-resolution static image export in PNG, SVG, and PDF via **Seaborn & Matplotlib**.
- 🛡️ **Authentication & Permissions**: Custom User model, JWT tokens (SimpleJWT), Session auth, role-based dataset access control.
- ⚡ **Asynchronous Task Architecture**: Redis & Celery integration ready for long-running ETL and model training tasks.
- 🎨 **Modern Responsive UI**: Clean Bootstrap 5 dashboard with responsive charts and dark/light theme support.

---

## 🏗️ Project Architecture

```
data-analysis-dashboard/
├── config/                 # Root settings, URLs, ASGI/WSGI, Celery config
├── accounts/               # CustomUser, UserProfile, UserPreferences, Auth APIs
├── datasets/               # File uploads, parsers, DataColumn, DataSample, profiler
├── analysis/               # DataAnalyzer engine (SciPy/Sklearn/Pandas), Analysis models
├── visualizations/         # ChartGenerator (Plotly & Seaborn), Chart configs, Export API
├── api/                    # Consolidated API root, system health, and metrics
├── templates/              # Bootstrap 5 responsive templates (Home, Dashboard, Datasets, Charts)
├── static/                 # Stylesheets, JavaScript, Chart utilities
├── sample_data/            # 4 real-world sample datasets (Sales, Education, Weather, Stocks)
├── tests/                  # Automated unit and integration test suite
├── requirements.txt        # Production dependencies
├── manage.py
├── .env.example
├── README.md
├── API.md
├── INSTALLATION.md
└── FEATURES.md
```

---

## 🚀 Quick Start Guide

### 1. Clone & Navigate
```bash
git clone https://github.com/your-username/data-analysis-dashboard.git
cd data-analysis-dashboard
```

### 2. Set Up Virtual Environment
```bash
python -m venv venv
# Windows:
.\venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Database Setup & Seeding
```bash
python manage.py migrate
python manage.py seed_analysis_data
```

### 5. Run the Server
```bash
python manage.py runserver
```

Open your browser at: **http://127.0.0.1:8000/**

- **Django Admin:** [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)
  - Email: `admin@admin.com`
  - Password: `Admin1234!`
- **REST API Explorer:** [http://127.0.0.1:8000/api/v1/](http://127.0.0.1:8000/api/v1/)

---

## 🧪 Running Tests

```bash
python manage.py test tests
```

---

## 📄 License
MIT License. Built with ❤️ for Data Science and Engineering.
