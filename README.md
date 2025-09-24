# afriremotely
A Django backend server built as an API interface for a job board platform, React frontend. The backend include Postgres server, Django Rest APIs, for job postings, role-based access control, and efficient job search features. It integrates advanced database optimization and comprehensive API documentation.


```markdown
# AfriRemotely Job Board  

AfriRemotely is a job board platform built with **Django** to connect African talent with remote job opportunities worldwide.  
The platform provides employers with a way to post jobs and applicants with tools to apply, track status, and manage applications.  

---

## Features  

### For Job Seekers  
- View available remote job postings  
- Apply with resume and cover letter  
- Track application status (Pending, Reviewed, Accepted, Rejected)  
- User-friendly application dashboard  

### For Employers  
- Post remote job listings  
- Manage job applications  
- Review candidate profiles and resumes  

### API & Documentation  
- RESTful API powered by **Django REST Framework (DRF)**  
- Interactive API documentation available via **Swagger UI** & **ReDoc**  

---

## Tech Stack  

- **Backend**: Django, Django REST Framework  
- **Database**: PostgreSQL (production), SQLite (development)  
- **Authentication**: Django Auth (JWT optional for APIs)  
- **Deployment**: Render.com with **Whitenoise** for static file serving  
- **API Docs**: DRF-Spectacular (Swagger, ReDoc)  

---

## Project Structure  

```

Afriremotely/
│── afriremotely/         # Project configuration
│── jobs/                 # Job postings app
│── applications/         # Job applications app
│── users/                # Custom user model app
│── templates/            # HTML templates (homepage, docs links, etc.)
│── static/               # Static files (CSS, JS, Images)
│── manage.py             # Django management script

````

---

## Setup Instructions  

### Clone Repository  
```bash
git clone https://github.com/tomogolla/afriremotely.git
cd afriremotely
````

### Create Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate   # Linux / Mac
.venv\Scripts\activate      # Windows
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Database Setup

```bash
python manage.py migrate
```

### Create Superuser (Admin)

```bash
python manage.py createsuperuser
```

### Run Development Server

```bash
python manage.py runserver
```

---

## Deployment on Render

1. Push project to GitHub
2. Create a new **Web Service** on Render
3. Set **Build Command**:

   ```bash
   pip install -r requirements.txt
   python manage.py collectstatic --noinput
   python manage.py migrate
   ```
4. Set **Start Command**:

   ```bash
   gunicorn afriremotely.wsgi
   ```
5. Add environment variables in Render dashboard:

   * `SECRET_KEY`
   * `DEBUG=False`
   * `DATABASE_URL` (PostgreSQL)

---

## API Documentation

* Swagger UI → `/api/schema/swagger-ui/`
* ReDoc → `/api/schema/redoc/`
* Raw OpenAPI Schema → `/api/schema/`

---

## Authors

* **Thomas Ogolla (ALX SE Student)**

---

## License

This project is licensed under the MIT License – see the [LICENSE](LICENSE) file for details.



# API endpoints

## **Authentication Endpoints**
- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login (JWT tokens)
- `POST /api/auth/logout/` - User logout
- `POST /api/auth/refresh/` - Refresh JWT token
- `GET /api/auth/me/` - Get current user profile
- `PUT /api/auth/me/` - Update current user profile

## **User Management Endpoints** (Admin only)
- `GET /api/users/` - List all users
- `GET /api/users/{id}/` - Get user details
- `PUT /api/users/{id}/` - Update user (admin)
- `DELETE /api/users/{id}/` - Delete user (admin)

## **Categories Endpoints**
- `GET /api/categories/` - List all categories
- `GET /api/categories/{id}/` - Get category details
- `POST /api/categories/` - Create category (admin only)
- `PUT /api/categories/{id}/` - Update category (admin only)
- `DELETE /api/categories/{id}/` - Delete category (admin only)

## **Jobs Endpoints**
- `GET /api/jobs/` - List all jobs (with filtering)
- `GET /api/jobs/{id}/` - Get job details
- `POST /api/jobs/` - Create job (employers & admin)
- `PUT /api/jobs/{id}/` - Update job (owner or admin)
- `DELETE /api/jobs/{id}/` - Delete job (owner or admin)
- `GET /api/jobs/my-jobs/` - Get jobs posted by current user
- `PATCH /api/jobs/{id}/toggle-active/` - Toggle job active status

## **Job Search & Filtering Endpoints**
- `GET /api/jobs/search/` - Search jobs by keyword
- `GET /api/jobs/filter/` - Filter jobs by:
  - Category
  - Location
  - Job type
  - Salary range
  - Company
  - Date posted

## **Applications Endpoints**
- `GET /api/applications/` - List applications (employer sees their jobs' apps, job seeker sees their apps)
- `GET /api/applications/{id}/` - Get application details
- `POST /api/jobs/{job_id}/apply/` - Apply for a job
- `PUT /api/applications/{id}/status/` - Update application status (employer/admin)
- `GET /api/applications/job/{job_id}/` - Get applications for specific job (employer)
- `GET /api/applications/my-applications/` - Get current user's applications

## **Dashboard & Analytics Endpoints** (Admin/Employers)
- `GET /api/dashboard/stats/` - Get platform statistics
- `GET /api/dashboard/employer-stats/` - Get employer-specific stats
- `GET /api/dashboard/recent-activity/` - Get recent activity

## **File Upload Endpoints**
- `POST /api/upload/resume/` - Upload resume file
- `POST /api/upload/profile-picture/` - Upload profile picture

## **Notification Endpoints** (Optional)
- `GET /api/notifications/` - Get user notifications
- `POST /api/notifications/mark-read/` - Mark notifications as read
- `POST /api/notifications/subscribe/` - Subscribe to job alerts

##  **Public Endpoints** (No authentication required)
- `GET /api/public/jobs/` - List active jobs (for landing page)
- `GET /api/public/categories/` - List categories
- `GET /api/public/stats/` - Get public platform statistics



## **location filtering api** 
-- `GET /api/location/jobs` - list jobs in each country

##  **Endpoint Features Summary**

**Authentication Required**: Most endpoints
**Role-Based Access**: Different permissions for admin, employer, job seeker
**Filtering & Search**: Extensive query parameters for jobs
**Pagination**: All list endpoints
**File Handling**: Resume and image uploads
**Statistics**: Dashboard and analytics data




### My Django Apps
1. **Users**
   - **Purpose**: Manages user authentication, registration, and role-based access control.
   - **Functionality**:
     - User model (with roles: admin, user).
     - JWT-based authentication (login, logout, token refresh).
     - User profile management (e.g., name, email).
     - Role-based permissions (e.g., admins manage jobs, users apply for jobs).
   - **Key Models**: User

2. **Jobs**
   - **Purpose**: Handles job postings and related operations.
   - **Functionality**:
     - Create, update, delete, and retrieve job postings.
     - Categorize jobs by industry, location, and type.
     - APIs for job listing and details.
   - **Key Models**: JobPosting, Category, Location

3. **Applications**
   - **Purpose**: Manages job applications submitted by users.
   - **Functionality**:
     - Create and track job applications.
     - Allow users to view their application history.
     - Allow admins to review and update application statuses.
     - APIs for application submission and management.
   - **Key Models**: JobApplication

4. **Search**
   - **Purpose**: Handles optimized job search and filtering functionality.
   - **Functionality**:
     - Implement search APIs with filters (e.g., by category, location, job type).
     - Optimize queries using indexing for performance.
     - Support advanced filtering (e.g., keyword search, location-based search).
   - **Key Models**: (Relies on JobPosting, Category, Location from the Jobs app; no new models needed unless adding specific search-related data like search history)

5. **API**
   - **Purpose**: Centralizes API configurations and documentation.
   - **Functionality**:
     - Define REST API endpoints using Django REST Framework.
     - Integrate Swagger for API documentation (hosted at `/api/docs`).
     - Consolidate API views, serializers, and routes for all apps.
   - **Key Models**: None (focuses on API logic, not database models)
