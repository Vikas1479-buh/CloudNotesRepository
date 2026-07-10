# Cloud-Based Student Notes Repository

A Flask-based web application that enables faculty members to upload academic notes and allows students to browse, preview, bookmark, and download study materials securely.

---

## Features

### Admin
- Manage Departments
- Manage Subjects
- Manage Faculty & Students
- Dashboard

### Faculty
- Upload PDF, PPT, PPTX notes
- Edit Notes
- Delete Notes
- View Uploaded Notes
- Download Statistics

### Student
- Browse Notes
- Search Notes
- Filter by Semester
- Filter by Subject
- Preview Notes
- Download Notes
- Bookmark Notes
- View Download History
- Profile

---

## Technology Stack

| Component | Technology |
|-----------|------------|
| Backend | Flask |
| Database | PostgreSQL (Supabase) |
| ORM | SQLAlchemy |
| Database Migration | Flask-Migrate |
| Authentication | Flask-Login |
| Password Hashing | Werkzeug Security |
| Cloud Storage | Supabase Storage |
| Frontend | HTML, CSS, Bootstrap 5, JavaScript |

---

## Prerequisites

- Python 3.12 or above
- Git
- PostgreSQL (Supabase)
- Supabase Storage Bucket

---

## Installation

### Clone Repository

```bash
git clone https://github.com/Vikas1479-buh/CloudNotesRepository.git

cd CloudNotesRepository
```

---

### Create Virtual Environment

```bash
python -m venv venv
```

---

### Activate Virtual Environment

Windows PowerShell

```bash
.\venv\Scripts\Activate.ps1
```

Windows CMD

```bash
venv\Scripts\activate
```

Linux / macOS

```bash
source venv/bin/activate
```

---

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file.

```env
SECRET_KEY=your_secret_key

DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=your_host
DB_PORT=5432
DB_NAME=postgres

SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_service_key
```

---

## Database Migration

```bash
flask db upgrade
```

---

## Seed Admin Account

```bash
python seed.py
```

Default Admin Login

Email

```
admin@cloudnotes.com
```

Password

```
Admin@123
```

---

## Run the Project

```bash
python run.py
```

Open

```
http://127.0.0.1:5000
```

---

## Generate Requirements File

After installing packages

```bash
pip freeze > requirements.txt
```

Whenever someone clones the project

```bash
pip install -r requirements.txt
```

---

## Important Python Packages

- Flask
- Flask-SQLAlchemy
- Flask-Migrate
- Flask-Login
- psycopg2-binary
- Supabase
- python-dotenv
- Werkzeug

---

## Project Structure

```
CloudNotesRepository
│
├── app
│   ├── models
│   ├── routes
│   ├── templates
│   ├── utils
│   └── extensions.py
│
├── migrations
├── config.py
├── run.py
├── seed.py
├── requirements.txt
└── README.md
```

---

## Future Enhancements

- Faculty Analytics
- Student Dashboard Statistics
- QR Code Sharing
- Pagination
- PDF Viewer
- Dark Mode
- Popular Notes
- Email Notifications

---

## Developed By

**Vikas B U**

Cloud-Based Student Notes Repository Project