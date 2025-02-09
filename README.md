# Django Final Project: Work Time Tracker App

Render URL: https://final-wtt.onrender.com/

Git Repo: https://github.com/ahaseeb235/final_wtt.git

A web application built with Django to track employee working hours

## Table of Contents
- [Project Background](#project-background)
- [User Stories](#user-stories)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Project Structure](#project-structure)

---
## Project Background
Small-to-medium organisations have budgetary constraints that may prevent them to deploy and train their staff to use more complex and advanced applications such as Hubstaff, Wrike, Clockify, QuickBooks, etc. 

The aim of this endeavour is to provide a simple solution to track employee work hours, sick leave, annual leave, etc, and have it ready to send to payroll department. Target Audience will mainly be adults > 18+ years who are part of a small organisation.


## User Stories
- **Three Types of Users based on Position**
  - Staff: General users
  - Manager: Would have CRUD permissions, such as edit/delete some records. 
    - Can view User List
    - Can change position of User
  - System Admin: Superuser with all CRUD permissions. 
    - Can view User List
    - Can change position of User
    - Can delete posts and workday records.


## Features
- **User Management**: 
  - Registration and login system
  - User password change
  - User details and profile update with image
  - users can create, view, delete and edit only their own records
  - admin/superuser can CRUD all. Manager can CRUD all. 
  
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
   git clone https://github.com/ahaseeb235/final_wtt.git
   


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


