# Django Final Project: Work Time Tracker App

Render URL: #

Git Repo: #

A web application built with Django to track employee working hours

## Table of Contents
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Project Structure](#project-structure)

---

## Features
- **User Management**: 
  - Registration and login system
  - users can create, view, delete and edit only their own records
  - admin/superuser can CRUD all.
  (more functionality could be added)
- **Time Tracking**:
  - Log daily working hours with time-in and time-out.
  - calculation of total work hours
  - when workday_type is Bank Holiday or Sick Leave or Annual Leave, then time_in/time_out are not required. 
  - Categorize workdays as Work, Sick Leave, Annual Leave, Bank Holiday.
- **Dashboard**:
  - List view of total hours worked per month and categorized hours (e.g., Sick Leave, Overtime).
  - pagination on dashboard page
- **Data Management and hosting**:
  - use of postgreSQL 
  - hosting on render.com
- **Responsive Design**:
  - Bootstrap-based layouts for seamless use across devices.
- **Use of Javascript**:
  - Use of JS for success messages on the pages
  - To add calendar and time functionality for the form. (Flatpicker library)

---

## Technologies Used
- **Backend**: Django 5.1.4
- **Database**: PostgreSQL
- **Frontend**: HTML5, CSS3, JavaScript
- **Libraries/Frameworks**:
  - Bootstrap for UI components - bootswatch.
  - JavaScript for dynamic and interactive elements - Flatpicker.

---

## Installation

### Prerequisites
- Python 3.8+
- PostgreSQL 12+
- Git

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/ahaseeb235/wtt_djangoframework_v1.git
   


2. To setup environment
    ```bash
    python -m venv venv
    source venv/bin/activate   # On Windows, use `venv\Scripts\activate`


3. setup dependencies
    ```bash
    pip install -r requirements.txt

4. database migration
    ```bash
    python manage.py makemigrations
    python manage.py migrate


5. for admin access setup
    ```bash
    python manage.py createsuperuser

6. run server
    ```bash
    python manage.py runserver


## Project Structure
/worktimetracker          # Root directory of the project
│
├── /worktimetracker      # Main project folder
│   ├── __init__.py       # Initializes the project as a Python package
│   ├── settings.py       # Configuration settings for the project
│   ├── urls.py           # URL routing for the project
│   ├── wsgi.py           # WSGI application entry point
│   └── asgi.py           # ASGI application entry point
│
├── /webapp                 # Main app folder 
│   ├── admin.py            # Admin panel configurations
│   ├── apps.py             # App configuration
│   ├── models.py           # Database models
│   ├── views.py            # Application views
│   ├── forms.py            # Forms for user input
│   ├── urls.py             # App-specific URL routing
│   ├── templates/          # HTML templates for the app
│   └── static/             # Static files (CSS, JS, images)
│
├── /static                 # Project-wide static files
│   ├── /css                # Stylesheets
│   ├── /js                 # JavaScript files
│   
│
├── /templates              # Project-wide templates
│   ├── base.html           # Base template for the project
│   ├── index.html          # Home page template
│   ├── create-record.html  # create-record page template
│   ├── update-record.html  # update page template
|   ├── view-record.html    # view records page template
|   ├── nabar.html          # template for navbar
|   ├── login.html          # view records page template
|   ├── dashboard.html      # template for dashboard
|   └── regist.html         # register user template
│
├── manage.py               # Django management script
├── requirements.txt        # List of Python dependencies
├── README.md               # Project documentation
└── .gitignore              # Files and folders to ignore in Git

