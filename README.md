# Nostalgia: A Social Media Platform for Elderly Users

Welcome to Nostalgia, the social media platform dedicated to the elderly community. Our platform is designed to cater to the unique needs and interests of seniors, providing a safe, secure, and enjoyable online environment for connection, health management, and community engagement.

## 📋 Table of Contents

- [Overview](#overview)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Features](#features)
- [Installation & Setup](#installation--setup)
- [Running the Project](#running-the-project)
- [Database](#database)
- [API Documentation](#api-documentation)
- [Contributing](#contributing)
- [License](#license)

## 🎯 Overview

Nostalgia is a comprehensive Django-based backend API for a social media platform specifically tailored for elderly users. It provides features for social connectivity, health management, friend discovery using AI, and community engagement. The platform includes both user and overseer (caregiver) roles for enhanced safety and support.

**Key Technologies:**
- **Django 5.0.2** - Web framework for backend development
- **Django REST Framework 3.15.1** - RESTful API development
- **SimpleJWT** - JWT-based authentication
- **PostgreSQL (recommended)** - Database management (use with `pgvector` extension for vector storage)
- **Python** - Backend programming language

## 🛠 Tech Stack

### Backend Framework
- **Django 5.0.2** - High-level Python web framework
- **Django REST Framework 3.15.1** - Powerful and flexible toolkit for building REST APIs
- **djangorestframework-simplejwt 5.3.1** - JWT authentication for secure API access

### Database
- **PostgreSQL (recommended) / MySQL** - Relational database management system; PostgreSQL is recommended for `pgvector` integration

### Security & Authentication
- **PyJWT 2.8.0** - JSON Web Token library
- **django-cors-headers 4.3.1** - CORS support for cross-origin requests

### Vector & Task Integration
- **pgvector** - PostgreSQL vector column support for storing embeddings used by the recommender
- **django-tasks** - Background task framework used for embedding generation (`api/tasks.py`)

### Media & Processing
- **Pillow 10.2.0** - Python Imaging Library for image processing
- **requests 2.31.0** - HTTP library for API calls

### Utilities
- **asgiref 3.8.1** - ASGI utilities
- **sqlparse 0.4.4** - SQL parsing library
- **certifi, charset-normalizer, idna, urllib3** - Network and encoding utilities
- **tzdata 2024.1** - Timezone data

## 📁 Project Structure

```
Nostalgia/
├── api/                          # Main Django REST API app
│   ├── models.py                 # Database models
│   ├── serializers.py            # DRF serializers
│   ├── views.py                  # API views and endpoints
│   ├── urls.py                   # API URL routing
│   ├── admin.py                  # Django admin configuration
│   ├── backends.py               # Custom authentication backends
│   ├── lines.py                  # Utility functions
│   ├── apps.py                   # App configuration
│   ├── tests.py                  # Unit tests
│   └── migrations/               # Database migrations
│
├── web/                          # Web app for serving frontend/templates
│   ├── models.py                 # Web app models
│   ├── views.py                  # Web views
│   ├── urls.py                   # Web URL routing
│   ├── backends.py               # Web app backends
│   ├── templates/                # HTML templates
│   ├── admin.py                  # Django admin config
│   ├── tests.py                  # Tests
│   └── migrations/               # Database migrations
│
├── nostalgia/                    # Main Django project settings
│   ├── settings.py               # Django configuration
│   ├── urls.py                   # Main URL configuration
│   ├── asgi.py                   # ASGI configuration
│   └── wsgi.py                   # WSGI configuration
│
├── static/                       # Static files (CSS, JS, images)
├── media/                        # User-uploaded media files
├── manage.py                     # Django management script
├── requirements.txt              # Python dependencies
├── .env                          # Environment variables
├── db.sqlite3                    # SQLite database (development)
├── LICENSE                       # Project license
└── README.md                     # This file
```

## ✨ Features

### Authentication & User Management
1. **Sign Up** - Users create accounts with personal details (name, email, username, address)
2. **Login** - Dual login systems:
   - User login with username/email and password
   - Overseer login for caregivers and trusted relatives
3. **Profile Management** - Edit profile and add/manage overseer accounts
4. **Account Verification** - OCR and deep learning-based verification using official ID documents (National IDs, passports)

### Social Connectivity
5. **Find Friends** - AI-powered friend discovery using image matching (current images matched with youth photos)
6. **Friend Suggestions** - Machine learning algorithms suggest friends based on shared interests
7. **Make Friends** - Add friends or acquaintances with unfriend options
8. **Acquaintance Connections** - Maintain lighter social connections

### Content & Community
9. **Blogs** - Share life experiences and advice with personalized recommendations
10. **Interest-Based Groups** - Create or join groups based on interests with ML-powered recommendations
11. **Plan Events** - Suggest and organize intergenerational events
12. **Community Engagement** - Foster discussions and knowledge sharing

### Health & Wellness
13. **Medication Alerts** - Medication reminders with note-taking and completion tracking
14. **Caregiver Information** - Access to trustworthy healthcare professionals and caregivers
15. **Find Walking Buddy** - Match users for fitness activities based on goals and preferences
16. **Plan a Trip** - Organize trips with like-minded individuals for social and recreational purposes

### Overseer Features
- **Medication Tracking** - Monitor elderly users' medication adherence
- **Walking Buddy Monitoring** - Supervise walking activities and fitness goals
- **User Oversight** - Care and support management for elderly users

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- PostgreSQL Server (recommended, with `pgvector` extension) or MySQL
- pip (Python package manager)

### Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Nostalgia
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/Scripts/activate  # On Windows
   # or
   source venv/bin/activate      # On Linux/macOS
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   - Copy `.env` and configure:
     ```
     DEBUG=True
     SECRET_KEY=your-secret-key
     DATABASE_URL=mysql://username:password@localhost:3306/nostalgia
     ```

5. **Database setup**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create a superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Collect static files**
   ```bash
   python manage.py collectstatic
   ```

## 🏃 Running the Project

### Development Server
```bash
python manage.py runserver
```
The development server will run at `http://localhost:8000/`

### Admin Panel
Access Django admin at `http://localhost:8000/admin/` with superuser credentials

### API Endpoints
API is available at `http://localhost:8000/api/`

## 🗄️ Database

The project uses MySQL as the primary database. Database configuration can be found in `nostalgia/settings.py`.

### Models
Key models managed by the API app:
- User (with overseer support)
- Friends/Connections
- Blogs/Posts
- Groups
- Medication Records
- Events
- Trips
- Caregiver Information

## 📚 API Documentation

The API follows RESTful principles and uses JWT for authentication. Key endpoints include:

- `/api/auth/` - Authentication endpoints
- `/api/users/` - User management
- `/api/friends/` - Friend management
- `/api/blogs/` - Blog management
- `/api/groups/` - Group management
- `/api/medication/` - Medication tracking
- `/api/events/` - Event management
- `/api/trips/` - Trip planning
- `/api/caregivers/` - Caregiver information

For detailed API documentation, see the API endpoints configuration in `api/urls.py`

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

**Project Version**: 1.0.0
**Last Updated**: February 2026

For questions or support, please contact the development team.
