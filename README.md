# Micro-project-fullstack-9
# Smart Hostel Management System (Django)

A simple Smart Hostel Management System built with **Django**.  
Provides separate dashboards for **Staff** (Django auth) and **Student** (session-based login via USN + name). Staff can manage Students, Rooms and Bookings. Students can sign in with USN to view their bookings.

## Features
- Staff login (username/password) — Django authentication.
- Student login (USN + name) — session-based (no password).
- Separate dashboards:
  - **Staff Dashboard**: staff-only, CRUD for Students, Rooms, Bookings.
  - **Student Dashboard**: session-based, shows student's room and bookings.
- Simple room capacity enforcement and occupancy tracking.
- Templates + static CSS (no Bootstrap) with a clean, minimal UI.

---

## Repo structure (important files)


Team members group[9]
1) Anupriya UV  -  4MC23IS009
2) Ashika UP    -  4MC23IS014
3) Bhoomika KB  -  4MC23IS017
4) Impana UD    -  4MC23IS045
5) Meghana HA   -  4MC23IS060

# 🏠 Smart Hostel Management System  

A full-stack web application built using **Django (Python)** for efficiently managing hostel operations — including student details, room allocations, and bookings.  
This system provides separate dashboards for **staff** and **students**, ensuring smooth management and transparency.

---

## 🚀 Features

### 👩‍🏫 Staff Dashboard
- Add, update, and manage student information  
- Manage hostel rooms and view availability  
- Handle room bookings and allocations  
- View overall hostel statistics (total students, rooms, and bookings)  
- Secure staff login/logout system  

### 🎓 Student Dashboard
- Student login using credentials  
- View personal room details and booking status  
- Update contact details (optional extension)  
- Easy logout and session management  

---

## 🧠 Tech Stack
- **Backend:** Django (Python)  
- **Frontend:** HTML, CSS  
- **Database:** SQLite3 (default Django DB)  
- **IDE:** Visual Studio Code  
- **Version Control:** Git & GitHub  

---

## ⚙️ Project Setup Instructions

Follow these simple steps to run the project locally 👇

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/Bhoomika1267/Micro-project-fullstack-9.git
cd Micro-project-fullstack-9
2️⃣ Create and Activate a Virtual Environment
bash
Copy code
python3 -m venv venv
source venv/bin/activate      # macOS / Linux
venv\Scripts\activate         # Windows
3️⃣ Install Required Packages
bash
Copy code
pip install -r requirements.txt
4️⃣ Run Database Migrations
bash
Copy code
python manage.py makemigrations
python manage.py migrate
5️⃣ Create a Superuser (for admin access)
bash
Copy code
python manage.py createsuperuser
Then enter a username, email, and password.

6️⃣ Start the Development Server
bash
Copy code
python manage.py runserver
Open your browser and go to 👉 http://127.0.0.1:8000/

📁 Folder Structure
php
Copy code
hostel_pro/                # Main Django project folder
├── malnad_app/            # Application folder
├── templates/             # HTML templates
├── static/                # CSS / JS files (optional)
├── db.sqlite3             # SQLite database file
└── manage.py              # Django project manager
