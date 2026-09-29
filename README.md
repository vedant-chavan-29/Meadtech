# 🏥 MeadTech — Cloud Healthcare Management System

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)
![Flask](https://img.shields.io/badge/Flask-3.0.0-black?style=for-the-badge&logo=flask)
![AWS](https://img.shields.io/badge/AWS-Ready-orange?style=for-the-badge&logo=amazonaws)
![Vercel](https://img.shields.io/badge/Deployed%20on-Vercel-black?style=for-the-badge&logo=vercel)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

**A full-stack, cloud-ready healthcare management platform built with Python Flask.**  
Enables patients, doctors, and administrators to seamlessly manage appointments, diagnoses, and medical records — architected for AWS DynamoDB & SNS integration in Phase 2.

[📂 Repository](https://github.com/vedant-chavan-29/MeadTech)

</div>

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [User Roles & Credentials](#user-roles--credentials)
- [API Endpoints](#api-endpoints)
- [Local Setup](#local-setup)
- [Deployment](#deployment)
- [AWS Architecture (Phase 2)](#aws-architecture-phase-2)
- [Screenshots](#screenshots)

---

## 🔍 Overview

**MeadTech** is a cloud-ready healthcare management system designed to bridge the gap between patients and healthcare providers. Built as a Python Flask web application, it supports three distinct user roles — **Patient**, **Doctor**, and **Admin** — each with a dedicated portal and set of capabilities.

The system currently uses **in-memory data storage** (Phase 1) and is architected for seamless migration to **AWS DynamoDB** and **AWS SNS** (Phase 2), following cloud-native best practices.

---

## ✨ Features

### 👤 Patient Portal
- Secure **registration & login** with hashed passwords (Werkzeug)
- Personalized **patient dashboard** with appointment history and diagnoses
- **Book appointments** with available doctors, select date/time/reason
- View **medical history** and diagnosis reports submitted by doctors
- Real-time **notifications** for appointment status updates

### 🩺 Doctor Portal
- Dedicated **doctor dashboard** with upcoming appointments and patient list
- **Submit clinical diagnosis reports** (symptoms, findings, prescription)
- **Update appointment status** (Confirmed / Pending / Completed / Cancelled)
- View full patient records and **medical history**

### 🛡️ Admin Portal
- Complete **admin dashboard** with system-wide overview
- Manage all **users, doctors, patients, appointments, diagnoses** in one place
- Monitor **real-time notification logs**
- View **debug API state** at `/api/debug/state`

### 🔔 Notification System *(AWS SNS Simulation)*
- Automatic real-time alerts on:
  - Appointment bookings (patient & doctor notified)
  - Status changes (Confirmed / Completed / Cancelled)
  - New diagnosis report published
  - New user registration (welcome message)

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Backend** | Python 3.10+, Flask 3.0 |
| **Security** | Werkzeug (bcrypt password hashing), Flask Sessions |
| **Frontend** | HTML5, CSS3, Jinja2 Templating |
| **Storage (Phase 1)** | In-Memory Python Data Structures |
| **Storage (Phase 2)** | AWS DynamoDB *(planned)* |
| **Notifications (Phase 2)** | AWS SNS *(simulated in Phase 1)* |
| **Deployment** | Vercel (Serverless Python) |
| **Process Manager** | Gunicorn |

---

## 📁 Project Structure

```
MeadTech/
│
├── app.py                  # Main Flask application (routes, logic, data)
├── requirements.txt        # Python dependencies
├── Procfile                # Gunicorn process config (for Heroku/Render)
├── vercel.json             # Vercel serverless deployment config
│
├── api/
│   └── index.py            # Vercel serverless entrypoint
│
├── templates/              # Jinja2 HTML templates
│   ├── base.html           # Master layout template (navbar, flash messages)
│   ├── index.html          # Landing/Home page
│   ├── about.html          # About page
│   ├── contact.html        # Contact form
│   ├── login.html          # Login page
│   ├── signup.html         # Registration page
│   ├── home1.html          # Post-login redirect hub
│   ├── patient_dashboard.html    # Patient portal
│   ├── doctor_dashboard.html     # Doctor portal
│   ├── admin_dashboard.html      # Admin portal
│   ├── book_appointment.html     # Appointment booking form
│   ├── appointments.html         # Appointments list view
│   ├── submit_diagnosis.html     # Diagnosis submission form
│   ├── medical_history.html      # Medical records viewer
│   └── notifications.html        # Notifications page
│
└── static/                 # Static assets (CSS, JS, images)
    ├── css/
    │   └── style.css
    └── js/
        └── main.js
```

---

## 👥 User Roles & Credentials

> Use these demo credentials to explore the system:

### 🩺 Doctors
| Name | Email | Password |
|------|-------|----------|
| Dr. Sarah Jenkins | `dr.jenkins@medtrack.com` | `doctor123` |
| Dr. Robert Chen | `dr.chen@medtrack.com` | `doctor123` |
| Dr. Emily Vance | `dr.vance@medtrack.com` | `doctor123` |

### 🧑 Patients
| Name | Email | Password |
|------|-------|----------|
| John Doe | `john.doe@example.com` | `patient123` |
| Kusuma Sharma | `xyz@gmail.com` | `patient123` |

### 🛡️ Admin
| Name | Email | Password |
|------|-------|----------|
| System Administrator | `admin@medtrack.com` | `admin123` |

---

## 🔗 API Endpoints

| Method | Route | Access | Description |
|--------|-------|--------|-------------|
| GET | `/` | Public | Landing page |
| GET | `/about` | Public | About page |
| GET/POST | `/contact_us` | Public | Contact form |
| GET/POST | `/login` | Public | User login |
| GET/POST | `/signup` | Public | User registration |
| GET | `/logout` | Auth | Logout session |
| GET | `/home1` | Auth | Role-based redirect hub |
| GET | `/patient/dashboard` | Patient | Patient dashboard |
| GET | `/doctor/dashboard` | Doctor/Admin | Doctor dashboard |
| GET | `/admin/dashboard` | Admin | Admin dashboard |
| GET/POST | `/book_appointment` | Auth | Book an appointment |
| GET | `/appointments` | Auth | View appointments |
| POST | `/appointment/update_status/<id>` | Doctor/Admin | Update appointment status |
| GET/POST | `/submit_diagnosis` | Doctor/Admin | Submit diagnosis report |
| GET | `/medical_history` | Auth | View medical records |
| GET | `/notifications` | Auth | View notifications |
| GET | `/api/debug/state` | Public | Full system state (JSON) |

---

## ⚙️ Local Setup

### Prerequisites
- Python 3.10+
- pip

### Steps

```bash
# 1. Clone the repository
git clone https://github.com/vedant-chavan-29/MeadTech.git
cd MeadTech

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the application
python app.py
```

The app will start at: **http://127.0.0.1:5050**

### Environment Variables (Optional)

| Variable | Default | Description |
|----------|---------|-------------|
| `SECRET_KEY` | `medtrack_cloud_secret_key_2026_super_secure!` | Flask session secret key |
| `PORT` | `5050` | Port to run the server on |

---

## 🚀 Deployment

### Vercel (Current)

The project is deployed on Vercel as a serverless Python application.

```bash
# Push to GitHub — Vercel auto-deploys on every push to main
git add .
git commit -m "Your commit message"
git push origin main
```

**Vercel config** (`vercel.json`):
```json
{
  "rewrites": [
    { "source": "/(.*)", "destination": "/api/index.py" }
  ]
}
```

### Render / Heroku (Alternative)

```bash
# Start command
gunicorn app:app
```

The `Procfile` is already configured:
```
web: gunicorn app:app
```

---

## ☁️ AWS Architecture (Phase 2)

> The system is architecturally designed and ready for AWS cloud migration:

```
┌─────────────────────────────────────────────────────────────┐
│                     AWS Cloud Infrastructure                │
│                                                             │
│  ┌──────────┐    ┌───────────┐    ┌──────────────────────┐ │
│  │  Route53 │───▶│ CloudFront│───▶│  EC2 / Lambda        │ │
│  │  (DNS)   │    │   (CDN)   │    │  (Flask Application) │ │
│  └──────────┘    └───────────┘    └──────────────────────┘ │
│                                            │                │
│                          ┌─────────────────┼───────────┐   │
│                          ▼                 ▼           ▼   │
│                    ┌──────────┐     ┌──────────┐  ┌──────┐ │
│                    │ DynamoDB │     │   SNS    │  │  S3  │ │
│                    │(Data DB) │     │ (Alerts) │  │(Files│ │
│                    └──────────┘     └──────────┘  └──────┘ │
└─────────────────────────────────────────────────────────────┘
```

**Planned Migrations:**
- **In-Memory Lists** → **AWS DynamoDB** (NoSQL, scalable, serverless)
- **Print-based notifications** → **AWS SNS** (real email/SMS alerts)
- **Static files** → **AWS S3 + CloudFront**
- **App server** → **AWS Elastic Beanstalk / Lambda**

---

## 📄 Requirements

```
flask>=3.0.0
werkzeug>=3.0.0
boto3>=1.34.0
gunicorn>=21.2.0
```

---

## 📃 License

This project is licensed under the **MIT License**.

---

## 👨‍💻 Author

**Vedant Chavan**  
GitHub: [@vedant-chavan-29](https://github.com/vedant-chavan-29)

---

<div align="center">
  <i>Built with ❤️ using Python Flask — Architected for AWS Cloud</i>
</div>
