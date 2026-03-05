# AutoPulse

Our app will be used to help others with car maintenance. 
The app will be a sort of forum where anybody can upload a question regarding any lights on their dash, weird noises, or leaking fluids.
Additionaly, we will add general information about each light and popular solutions/forums. 

## Description
The purpose is to help people save money and learn how to properly maintenance their own vehicles.
What problem does it solve?  
What technologies or languages are used?

## Features
- Upload question / solution
- Information about each light on the dash
- Able to search for a specific question

# SoftwareEng Django Project

This project is a Django web application developed for the Software Engineering I course.

---

# Project Setup

## 1. Clone the Repository

bash
git clone https://github.com/crivera193/SoftwareEngProject.git
cd SoftwareEngProject


---

# First Time Setup

Create a virtual environment:

bash
python -m venv virtualenv


Activate the virtual environment:

Linux / Mac:

bash
source virtualenv/bin/activate


Windows:

bash
virtualenv\Scripts\activate


---

# Install Dependencies

bash
pip install django


If a requirements file exists:

bash
pip install -r requirements.txt


---

# Run Database Migrations

bash
python manage.py migrate


---

# Run the Django Server

bash
python manage.py runserver


Open the project in your browser:


http://127.0.0.1:8000/


---

# Project Structure


SoftwareEng/
│
├── manage.py
├── README.md
├── mysite/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── newApp/
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── signals.py
│   ├── urls.py
│   └── templates/
│
└── virtualenv/


---

# Git Workflow (Team Development)

We use the following branches:


main
christina
alexandra
omar


main should always contain stable working code.

Each teammate works on their *own branch*.

---

# Starting Work (IMPORTANT)

Always update main first:

bash
git checkout main
git pull origin main


Switch to your personal branch:

Example:

bash
git checkout christina


Merge latest changes from main:

bash
git merge main


---

# Saving Your Work

Add changes:

bash
git add .


Commit changes:

bash
git commit -m "Describe your changes"


Push to your branch:

bash
git push


---

# Merging Into Main

Only merge when the code runs correctly.

Switch to main:

bash
git checkout main


Pull latest changes:

bash
git pull origin main


Merge branch:

Example:

bash
git merge christina


Push updated main branch:

bash
git push origin main


---

# Technologies Used

- Python
- Django
- HTML
- Bootstrap
- SQLite
- Git / GitHub

---

# Team Members

- Christina
- Alex
- Omar
