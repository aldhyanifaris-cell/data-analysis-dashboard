# Installation & Deployment Guide

## System Prerequisites
- Python 3.10+
- SQLite (included) or PostgreSQL 14+
- Redis (Optional, for Celery asynchronous queues)

## Local Development Setup
1. `python -m venv venv`
2. `.\venv\Scripts\activate`
3. `pip install -r requirements.txt`
4. `python manage.py migrate`
5. `python manage.py seed_analysis_data`
6. `python manage.py runserver`
