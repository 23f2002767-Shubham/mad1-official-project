# MAD-1-Official-Project-Placement-Portal-
This is the official final project

# 🎓 Institute Placement Portal

A **role-based Placement Portal Web Application** built using **Flask, SQLAlchemy, SQLite, and Jinja2** to manage campus recruitment activities involving **Admin, Companies, and Students**.

This project was developed as part of the **MAD-1 (Modern Application Development) course** at **IIT Madras BS Degree Program**.

---

# 🚀 Features

## 👨‍💼 Admin (Placement Cell)

- Pre-existing system administrator
- Approve or reject **company registrations**
- Approve or reject **placement drives**
- View and manage **students, companies, and applications**
- Blacklist or activate users
- Monitor overall placement activities

---

## 🏢 Company

- Register company profile
- Login after **admin approval**
- Create and manage **placement drives**
- View student applications
- **Shortlist, select, or reject candidates**

---

## 🎓 Student

- Register and login
- Update student profile
- Upload resume
- View approved placement drives
- Apply for placement drives
- Track application status
- View placement history

---

# 🛠️ Technology Stack

| Layer | Technology |
|------|------------|
| Backend | Flask |
| ORM | SQLAlchemy |
| Database | SQLite |
| Authentication | Flask-Login |
| Frontend | Jinja2 Templates |
| UI Styling | Bootstrap 5 |
| Language | Python |

---

# 📂 Project Structure :
 The placement_portal project structure is mentioned in Project_Structure.txt file


---

# 🗄️ Database Design

The system uses the following main tables:

- **users** – authentication and role management  
- **students** – student profile information  
- **companies** – company profile and approval status  
- **placement_drives** – job postings created by companies  
- **applications** – student applications for placement drives  

### Relationships

- User → Student (**1:1**)  
- User → Company (**1:1**)  
- Company → PlacementDrive (**1:N**)  
- Student → Application (**1:N**)  
- PlacementDrive → Application (**1:N**)

---

# 🔄 Application Workflow
Student registers → uploads resume
↓
Company registers → Admin approval
↓
Company creates placement drive
↓
Admin approves drive
↓
Students apply to drive
↓
Company shortlists candidates
↓
Company selects or rejects candidates


---

# ⚙️ Setup Instructions

## 1️⃣ Clone the repository

```bash
git clone <repository-url>
cd placement_portal


2️⃣ Create virtual environment

python -m venv venv

Activate it:

1. Windows
venv\Scripts\activate

2. Mac/Linux
source venv/bin/activate

3️⃣ Install dependencies
pip install -r requirements.txt

4️⃣ Initialize the Admin User
python scripts/seed_admin.py
This creates the default admin account.

5️⃣ Run the application
python run.py

The application will run at:
http://127.0.0.1:5000

🔐 Default Roles
| Role    | Description                         |
| ------- | ----------------------------------- |
| Admin   | Placement cell administrator        |
| Company | Recruiter creating placement drives |
| Student | Candidate applying for jobs         |


📡 API Documentation
Basic API endpoints are documented in: 
api.yaml

Example endpoints:
| Endpoint                              | Method | Description              |
| ------------------------------------- | ------ | ------------------------ |
| `/api/auth/login`                     | POST   | Authenticate user        |
| `/api/student/apply/<drive_id>`       | POST   | Apply to placement drive |
| `/api/admin/approve-drive/<drive_id>` | POST   | Approve drive            |


📈 Future Enhancements

Possible extensions include:

Email notifications for application updates
Placement analytics dashboard 
Interview scheduling system
Resume parsing for candidate filtering
Migration to React (MERN stack)

The architecture separates business logic and presentation layers, making the system easily extensible for REST APIs and modern frontend frameworks.


📄 License

This project is developed for academic purposes under the IIT Madras BS Degree Program.
